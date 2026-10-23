"""Small helpers for writing SmartAI scripts as Python (tools/turtle2ac/manual/<zone>.py).

A manual script gets a `Smart` object and returns SQL text:

    S = Smart(ctx)                       # ctx: q, TW, spell, sound_ok, cguid, gguid
    S.text(62547, 0, -1999962)           # creature_text group 0 from Turtle script_texts -1999962
    S.ic(62547, 'victim', 3393, (6000, 8000), (12000, 16000))
    S.on(62547, 'aggro', S.talk(0))
    sql = S.sql()

Ids: rows are numbered per (entry, source_type) from 100 up (ids < 100 belong to the generated spell lists).
"""
from lib.sqlw import lit

EV = dict(ic=0, ooc=1, hp=2, aggro=4, kill=5, death=6, evade=7, los=10, respawn=11, reset=25, data=38, summoned=54,
          timed=59, created=63, hello=64, counter=77, accepted_quest=19, reward_quest=20, gossip_select=62)
TG = dict(none=0, self=1, victim=2, second=3, last=4, random=5, random_not_top=6, invoker=7, pos=8, creature_range=9, player_range=17,
          creature_guid=10, stored=12, invoker_party=16, go_guid=14, closest_creature=19, closest_go=20, closest_player=21, threat_list=24)
TEXT_TYPE = {0: 12, 1: 14, 2: 16, 3: 41, 4: 15, 5: 42, 6: 14}     # vmangos script_texts.type -> creature_text.Type
UNIT_FLAG_NON_ATTACKABLE = 0x2
UNIT_FLAG_NOT_SELECTABLE = 0x2000000
COLS = ['entryorguid', 'source_type', 'id', 'link', 'event_type', 'event_phase_mask', 'event_chance', 'event_flags',
        'event_param1', 'event_param2', 'event_param3', 'event_param4', 'event_param5', 'event_param6',
        'action_type', 'action_param1', 'action_param2', 'action_param3', 'action_param4', 'action_param5', 'action_param6',
        'target_type', 'target_param1', 'target_param2', 'target_param3', 'target_param4',
        'target_x', 'target_y', 'target_z', 'target_o', 'comment']


class A:
    """an action: type, params, target"""
    def __init__(self, t, p=(), tgt='self', tp=(), xyz=(0, 0, 0, 0), note=''):
        self.t, self.p, self.tgt, self.tp, self.xyz, self.note = t, list(p), tgt, list(tp), xyz, note


class Smart:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rows = []
        self.texts = []
        self.next_id = {}
        self.names = {}
        self.notes = []
        self.ai_creatures = set()
        self.ai_gos = set()
        self.extra_sql = []
        self.rollback = []          # lines the zone's rollback file runs (stock rows this script changes)
        self.stock = set()          # 3.3.5 creatures this script adds to: their texts use groups 100+, their AIName is not touched

    # ------------------------------------------------------------------ actions
    def talk(self, group):
        return A(1, [group, 0, 0], 'self', note=f'Say Line {group}')

    def cast(self, spell, target='victim', triggered=False, tp=()):
        sp, why = self.ctx['spell'](spell)
        if why:
            self.notes.append(why)
        if not sp:
            return None
        return A(11, [sp, 2 if triggered else 0], target, tp, note=f'Cast {sp}')

    def summon(self, entry, x=None, y=None, z=None, o=0.0, kind=2, duration=60000):
        if x is None:
            return A(12, [entry, kind, duration], 'self', note=f'Summon {entry}')
        return A(12, [entry, kind, duration], 'pos', xyz=(x, y, z, o), note=f'Summon {entry}')

    def summon_go(self, entry, despawn_s):
        return A(50, [entry, despawn_s], 'self', note=f'Summon Object {entry}')

    def raw(self, t, p=(), tgt='self', tp=(), xyz=(0, 0, 0, 0), note=''):
        return A(t, p, tgt, tp, xyz, note)

    # ------------------------------------------------------------------ rows
    def _id(self, key):
        self.next_id.setdefault(key, 100 if key[1] in (0, 1) else 0)
        v = self.next_id[key]
        self.next_id[key] += 1
        return v

    def row(self, entry, src, ev, ep=(), act=None, phase=0, flags=0, chance=100, link=0, name=''):
        if act is None:
            return None
        ep = list(ep) + [0] * (6 - len(ep))
        ap = act.p + [0] * (6 - len(act.p))
        tp = act.tp + [0] * (4 - len(act.tp))
        i = self._id((entry, src))
        nm = name or self.names.get(entry, str(entry))
        self.rows.append(dict(zip(COLS, [entry, src, i, link, ev, phase, chance, flags] + ep + [act.t] + ap + [TG[act.tgt]] + tp +
                                  list(act.xyz) + [f'{nm} - {act.note}'])))
        if src == 0:
            self.ai_creatures.add(entry)
        if src == 1:
            self.ai_gos.add(entry)
        return i

    def on(self, entry, event, *acts, ep=(), phase=0, once=False, chance=100):
        """one row per action for a creature event (all rows share the event)"""
        for a in acts:
            self.row(entry, 0, EV[event], ep, a, phase=phase, flags=1 if once else 0, chance=chance)

    def ic(self, entry, target, spell, first, repeat, phase=0, then=()):
        """in-combat timer cast (Turtle: DoCastSpellIfCan on a timer). `then` = more actions on the same timer."""
        a = self.cast(spell, target)
        if not a:
            return
        self.row(entry, 0, EV['ic'], [first[0], first[1], repeat[0], repeat[1]], a, phase=phase)
        for b in then:
            self.row(entry, 0, EV['ic'], [first[0], first[1], repeat[0], repeat[1]], b, phase=phase)

    def actionlist(self, list_id, steps, owner_name=''):
        """timed action list: steps = [(delay_ms, action), ...]; delays are relative to the previous step.
        A step with action None only waits (its delay is added to the next real step)."""
        assert not self.ctx['q'](f"select 1 from {self.ctx['AC']}.smart_scripts where source_type=9 and entryorguid=%s limit 1", list_id), \
            f'action list {list_id} is a 3.3.5 one (a stock creature: pick an id it does not use)'
        carry = 0
        for delay, a in steps:
            carry += delay
            if a is not None:
                self.row(list_id, 9, 0, [carry, carry], a, name=owner_name)
                carry = 0
        return list_id

    def text(self, entry, group, script_text_id, idx=0):
        r = self.ctx['q'](f"select * from {self.ctx['TW']}.script_texts where entry=%s", script_text_id)[0]
        snd = r['sound'] if self.ctx['sound_ok'](r['sound']) else 0
        self.texts.append(dict(CreatureID=entry, GroupID=group, ID=idx, Text=r['content_default'], Type=TEXT_TYPE.get(r['type'], 12),
                               Language=r['language'], Probability=100, Emote=r['emote'], Duration=0, Sound=snd, BroadcastTextId=0,
                               TextRange=0, comment=r['comment'] or ''))

    def btext(self, entry, group, broadcast_id, chat='say', idx=0):
        """creature_text group from a Turtle broadcast_text row (what Turtle C++ MonsterSay/MonsterYell(id) uses)"""
        r = self.ctx['q'](f"select * from {self.ctx['TW']}.broadcast_text where entry=%s", broadcast_id)[0]
        snd = r['sound_id'] if self.ctx['sound_ok'](r['sound_id']) else 0
        self.texts.append(dict(CreatureID=entry, GroupID=group, ID=idx, Text=r['male_text'] or r['female_text'],
                               Type={'say': 12, 'yell': 14, 'emote': 16}[chat], Language=r['language_id'], Probability=0,
                               Emote=r['emote_id1'], Duration=0, Sound=snd, BroadcastTextId=0, TextRange=0,
                               comment=f'Turtle broadcast text {broadcast_id}'))

    def ltext(self, entry, group, text, chat='yell', idx=0):
        """creature_text group from a literal string (Turtle C++ MonsterYell("...") with no text id)"""
        self.texts.append(dict(CreatureID=entry, GroupID=group, ID=idx, Text=text, Type={'say': 12, 'yell': 14, 'emote': 16}[chat],
                               Language=0, Probability=0, Emote=0, Duration=0, Sound=0, BroadcastTextId=0, TextRange=0,
                               comment='Turtle C++ literal text'))

    # ------------------------------------------------------------------ gossip (menus Turtle builds in C++)
    def gossip(self, menu, text_broadcast, options=()):
        """A gossip menu the module owns (id = Turtle text id + 9,000,000): npc_text from a Turtle broadcast text,
        plus options [(option_id, broadcast id or literal text, icon, action menu, [condition rows], (option type, npcflag))]
        (the last item is optional: default (1, 1) = plain gossip; (3, 128) vendor, (5, 16) trainer). Conditions are
        (type, value1, value2, negative), e.g. (47, quest, 8, 0) = quest in progress, (2, item, 1, 0) = has the item."""
        q, TW = self.ctx['q'], self.ctx['TW']

        def btxt(b):
            if isinstance(b, str):
                return b
            r = q(f"select * from {TW}.broadcast_text where entry=%s", b)[0]
            return r['male_text'] or r['female_text']
        t = btxt(text_broadcast)
        self.extra_sql.append(
            f"DELETE FROM `npc_text` WHERE `ID`={menu};\nDELETE FROM `gossip_menu` WHERE `MenuID`={menu};\n"
            f"DELETE FROM `gossip_menu_option` WHERE `MenuID`={menu};\n"
            f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=15 AND `SourceGroup`={menu};\n"
            f"INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `Probability0`, `VerifiedBuild`) VALUES ({menu}, {lit(t)}, {lit(t)}, 1, 0);\n"
            f"INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES ({menu}, {menu});")
        for opt in options:
            oid, otext, icon, action_menu, conds = opt[:5]
            otype, onpc = opt[5] if len(opt) > 5 else (1, 1)       # e.g. (3, 128) vendor, (5, 16) trainer
            self.extra_sql.append(
                "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
                "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
                f"VALUES ({menu}, {oid}, {icon}, {lit(btxt(otext))}, 0, {otype}, {onpc}, {action_menu}, 0, 0, 0, NULL, 0, 0);")
            for ct, v1, v2, neg in conds:
                self.extra_sql.append(
                    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
                    "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
                    "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
                    f"(15, {menu}, {oid}, 0, 0, {ct}, 0, {v1}, {v2}, 0, {neg}, 0, 0, '', 'mod-turtle-content gossip option');")
        return menu

    # ------------------------------------------------------------------ changes to 3.3.5 (stock) rows, with rollback
    def stock_template(self, entry, **cols):
        """UPDATE a 3.3.5 creature_template (e.g. give a stock NPC a gossip menu); the rollback restores the old values"""
        self.stock.add(entry)
        q, AC = self.ctx['q'], self.ctx['AC']
        old = q(f"select {', '.join('`%s`' % c for c in cols)} from {AC}.creature_template where entry=%s", entry)
        assert old, f'creature {entry} is not a 3.3.5 creature'
        self.extra_sql.append(f"UPDATE `creature_template` SET {', '.join(f'`{c}`={lit(v)}' for c, v in cols.items())} WHERE `entry`={entry};")
        self.rollback.append(f"UPDATE `creature_template` SET {', '.join(f'`{c}`={lit(v)}' for c, v in old[0].items())} WHERE `entry`={entry};")

    def stock_spawn(self, table, guid, **cols):
        """UPDATE a 3.3.5 spawn (creature / gameobject row, e.g. its height where Turtle reshaped the ground); the rollback restores it"""
        q, AC = self.ctx['q'], self.ctx['AC']
        assert table in ('creature', 'gameobject')
        old = q(f"select {', '.join('`%s`' % c for c in cols)} from {AC}.{table} where guid=%s", guid)
        assert old, f'{table} {guid} is not a 3.3.5 spawn'
        self.extra_sql.append(f"UPDATE `{table}` SET {', '.join(f'`{c}`={lit(v)}' for c, v in cols.items())} WHERE `guid`={guid};")
        self.rollback.append(f"UPDATE `{table}` SET {', '.join(f'`{c}`={lit(v)}' for c, v in old[0].items())} WHERE `guid`={guid};")
        return old[0]

    def stock_spawn_remove(self, table, guid):
        """DELETE a 3.3.5 spawn Turtle removed (it stood where Turtle built something new); the rollback re-inserts the whole row.
        Only for spawns with no pool, event, formation or SmartAI rows and no waypoint path (asserted); a plain addon row goes and comes back with it."""
        q, AC = self.ctx['q'], self.ctx['AC']
        assert table in ('creature', 'gameobject')
        old = q(f"select * from {AC}.{table} where guid=%s", guid)
        assert old, f'{table} {guid} is not a 3.3.5 spawn'
        for t_, c_ in ((f'pool_{table}', 'guid'), (f'game_event_{table}', 'guid'), ('linked_respawn', 'guid')):
            assert not q(f"select 1 from {AC}.{t_} where {c_}=%s limit 1", guid), f'{table} {guid} has {t_} rows'
        # a plain addon row (sheath state, emote; no waypoint path) goes with the spawn and comes back with it
        addon = q(f"select * from {AC}.{table}_addon where guid=%s", guid)
        assert not addon or not addon[0].get('path_id'), f'{table} {guid} walks a waypoint path'
        assert not q(f"select 1 from {AC}.smart_scripts where entryorguid=%s and source_type=%s", -guid, 0 if table == 'creature' else 1)
        if table == 'creature':
            assert not q(f"select 1 from {AC}.creature_formations where memberGUID=%s or leaderGUID=%s", guid, guid)
        row = old[0]
        self.extra_sql.append(f"DELETE FROM `{table}` WHERE `guid`={guid};")
        self.rollback.append(f"DELETE FROM `{table}` WHERE `guid`={guid};\n"
                             f"INSERT INTO `{table}` ({', '.join('`%s`' % c for c in row)}) VALUES ({', '.join(lit(v) for v in row.values())});")
        if addon:
            a_ = addon[0]
            self.extra_sql.append(f"DELETE FROM `{table}_addon` WHERE `guid`={guid};")
            self.rollback.append(f"DELETE FROM `{table}_addon` WHERE `guid`={guid};\n"
                                 f"INSERT INTO `{table}_addon` ({', '.join('`%s`' % c for c in a_)}) VALUES ({', '.join(lit(v) for v in a_.values())});")
        return row

    def stock_gossip_option(self, menu, oid, text, icon=0, conds=()):
        """an option added to a 3.3.5 gossip menu (option ids 50+ are the module's); the rollback deletes it and its conditions.
        text: Turtle broadcast id or literal; conds as in gossip()"""
        q, TW, AC = self.ctx['q'], self.ctx['TW'], self.ctx['AC']
        assert oid >= 50 and not q(f"select 1 from {AC}.gossip_menu_option where MenuID=%s and OptionID=%s", menu, oid), (menu, oid)
        if not isinstance(text, str):
            r = q(f"select * from {TW}.broadcast_text where entry=%s", text)[0]
            text = r['male_text'] or r['female_text']
        dl = (f"DELETE FROM `gossip_menu_option` WHERE `MenuID`={menu} AND `OptionID`={oid};\n"
              f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=15 AND `SourceGroup`={menu} AND `SourceEntry`={oid};")
        self.extra_sql.append(dl)
        self.extra_sql.append(
            "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
            "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
            f"VALUES ({menu}, {oid}, {icon}, {lit(text)}, 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);")
        for ct, v1, v2, neg in conds:
            self.extra_sql.append(
                "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
                "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
                "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
                f"(15, {menu}, {oid}, 0, 0, {ct}, 0, {v1}, {v2}, 0, {neg}, 0, 0, '', 'mod-turtle-content gossip option');")
        self.rollback.append(dl)

    def mark_stock(self, entry):
        """a 3.3.5 creature this script gives events/texts to (texts: groups 100+)"""
        self.stock.add(entry)

    def stock_quest_drops(self, items):
        """Turtle items that Turtle added to the loot of 3.3.5 creatures: the same rows (group 0; quest-only where Turtle's chance is negative) go into
        those creatures' loot tables; the rollback deletes exactly them. -> [(creature entry, item, chance)]"""
        q, TW, AC, imap = self.ctx['q'], self.ctx['TW'], self.ctx['AC'], self.ctx['item']
        out = []
        for it in items:
            for r in q(f"select t.entry, l.ChanceOrQuestChance ch, l.mincountOrRef mn, l.maxcount mx from {TW}.creature_loot_template l "
                       f"join {TW}.creature_template t on t.loot_id=l.entry where l.item=%s", it):
                ac = q(f"select lootid from {AC}.creature_template where entry=%s", r['entry'])
                if not ac or not ac[0]['lootid'] or not q(f"select 1 from {AC}.creature where id1=%s limit 1".replace('id1', self.ctx['cre_id']), r['entry']):
                    continue                        # not a 3.3.5 creature, or not spawned in 3.3.5
                lid, item = ac[0]['lootid'], imap(it)
                ch = abs(float(r['ch']))
                qreq = 1 if float(r['ch']) < 0 else 0      # Turtle: negative chance = quest-only drop
                self.extra_sql.append(f"DELETE FROM `creature_loot_template` WHERE `Entry`={lid} AND `Item`={item};\n"
                                      "INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, "
                                      f"`GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES ({lid}, {item}, 0, {ch:g}, {qreq}, 1, 0, {max(1, r['mn'])}, "
                                      f"{max(1, r['mx'])}, 'mod-turtle-content quest drop');")
                self.rollback.append(f"DELETE FROM `creature_loot_template` WHERE `Entry`={lid} AND `Item`={item};")
                out.append((r['entry'], item, ch))
        return out

    # ------------------------------------------------------------------ output
    def sql(self):
        out = []
        ents = sorted({r['entryorguid'] for r in self.rows if r['source_type'] == 0 and r['entryorguid'] > 0})
        guid_c = sorted({r['entryorguid'] for r in self.rows if r['source_type'] == 0 and r['entryorguid'] < 0})
        gos = sorted({r['entryorguid'] for r in self.rows if r['source_type'] == 1})
        lists = sorted({r['entryorguid'] for r in self.rows if r['source_type'] == 9})
        tents = sorted({t['CreatureID'] for t in self.texts})
        if tents:
            # groups 50+ belong to the build's EventAI conversion; 3.3.5 creatures keep their own groups (ours are 100+)
            tw_ = [e for e in tents if e not in self.stock]
            st_ = [e for e in tents if e in self.stock]
            assert all(t['GroupID'] >= 100 for t in self.texts if t['CreatureID'] in self.stock), 'stock creature texts must use groups 100+'
            if tw_:
                out.append(f"DELETE FROM `creature_text` WHERE `CreatureID` IN ({','.join(map(str, tw_))}) AND `GroupID` < 50;")
            if st_:
                out.append(f"DELETE FROM `creature_text` WHERE `CreatureID` IN ({','.join(map(str, st_))}) AND `GroupID` >= 100;")
            out.append(_insert('creature_text', self.texts))
        if ents:
            tw_ = [e for e in ents if e not in self.stock]
            st_ = [e for e in ents if e in self.stock]
            if tw_:
                out.append(f"UPDATE `creature_template` SET `AIName`='SmartAI', `ScriptName`='' WHERE `entry` IN ({','.join(map(str, tw_))});")
            for e in st_:                # a 3.3.5 creature: SmartAI only when it has no AI/script of its own (else the script is not added)
                old = self.ctx['q'](f"select AIName, ScriptName from {self.ctx['AC']}.creature_template where entry=%s", e)[0]
                assert old['AIName'] in ('', 'SmartAI') and not old['ScriptName'], f'3.3.5 creature {e} has its own AI {old}'
                if old['AIName'] != 'SmartAI':
                    out.append(f"UPDATE `creature_template` SET `AIName`='SmartAI' WHERE `entry`={e};")
                    self.rollback.append(f"UPDATE `creature_template` SET `AIName`='' WHERE `entry`={e};")
            out.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({','.join(map(str, ents))}) AND `id` >= 100;")
        if guid_c:
            out.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({','.join(map(str, guid_c))});")
        if gos:
            out.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=1 AND `entryorguid` IN ({','.join(map(str, gos))});")
        if lists:
            out.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=9 AND `entryorguid` IN ({','.join(map(str, lists))});")
        out += self.extra_sql
        out.append(_insert('smart_scripts', self.rows))
        return '\n'.join(o for o in out if o) + '\n'


def _insert(table, rows):
    if not rows:
        return ''
    cols = list(rows[0].keys())
    return f"INSERT INTO `{table}` ({', '.join('`' + c + '`' for c in cols)}) VALUES\n" + \
        ',\n'.join('(' + ', '.join(lit(r[c]) for c in cols) + ')' for r in rows) + ';'
