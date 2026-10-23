#!/usr/bin/env python3
"""turtle2ac - build mod-turtle-content from a Turtle (Tortoise/vmangos) world DB.

    python3 build.py              # build every zone listed in config.json
    python3 build.py --check DB   # also validate the output after it was applied to DB

Outputs (relative to the module root):
    data/sql/db-world/mod_turtle_000_common.sql      items, item_dbc, reference loot (shared by all zones)
    data/sql/db-world/mod_turtle_<slot>_<zone>.sql   one file per zone (auto-applied by the AzerothCore DB updater)
    sql_rollback/*.sql                                undo files (NOT auto-applied)
    client/patch-y.mpq                                client patch (terrain tiles, AreaTable, GameObjectDisplayInfo, Item.dbc)
    server-data/maps/*.map, tiles.json                server map tiles for the converted terrain
    docs/zones/<zone>.md, docs/ZONES.md               human-readable reports
    tools/turtle2ac/reports/<zone>.json               machine-readable reports
"""
import os, sys, re, json, struct, collections, argparse, datetime, shutil, subprocess, hashlib, functools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pymysql
from lib.dbc import load
from lib.terrain import MapSet, ZoneLookup, AdtAreas, Client335Areas
from lib.displays import Displays
from lib.sqlw import Sql, lit, in_list

ap = argparse.ArgumentParser()
ap.add_argument('--check', help='database to validate after applying the output')
args = ap.parse_args()

CFG = json.load(open(os.path.join(HERE, 'config.json')))
ROOT = os.path.normpath(os.path.join(HERE, CFG['module_root']))
TW, AC = CFG['tw_db'], CFG['ac_db']
IDS = CFG['ids']
conn = pymysql.connect(unix_socket=CFG['db'].get('unix_socket'), user=CFG['db']['user'], password=CFG['db']['password'],
                       charset='utf8mb4') if CFG['db'].get('unix_socket') else \
       pymysql.connect(host=CFG['db']['host'], port=CFG['db']['port'], user=CFG['db']['user'], password=CFG['db']['password'], charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)


# Text that went through a latin1 connection on its way into the database is stored double-encoded
# ("butâ€”sadly" for "but—sadly"). MySQL's latin1 is cp1252 with the five undefined bytes kept as is.
_CP = {}
for _b in range(256):
    try:
        _CP[bytes([_b]).decode('cp1252')] = _b
    except UnicodeDecodeError:
        _CP[chr(_b)] = _b


def fix_text(v):
    if not isinstance(v, str) or v.isascii():
        return v
    try:
        b = bytes(_CP[c] for c in v)
        return b.decode('utf-8')
    except (KeyError, UnicodeDecodeError):
        return v


def q(sql, *a):
    cur.execute(sql, a if a else None)
    rows = cur.fetchall()
    for r in rows:
        for k, v in r.items():
            if isinstance(v, str) and not v.isascii():
                r[k] = fix_text(v)
    return rows


# --------------------------------------------------------------------------- target schema
# Column lists of the pristine world DB. It must be built from the server's own core (Grimfeather b4bbae96 has
# creature.id, upstream AzerothCore has creature.id1..3): every INSERT is checked and renamed against it.
import lib.sqlw as _sqlw
for _r in q("select table_name t, column_name c from information_schema.columns where table_schema=%s order by ordinal_position", AC):
    _sqlw.SCHEMA.setdefault(_r['t'], []).append(_r['c'])
CRE_ID = _sqlw.col('creature', 'id1')          # 'id' or 'id1'

# --------------------------------------------------------------------------- shared reference data
print('loading reference data ...')
ac_ct = {r['entry']: r['name'] for r in q(f"select entry,name from {AC}.creature_template")}
# 3.3.5 test templates nothing uses, whose ids Turtle gave to real creatures (Frostmane Hollow: 19, 67, 82, 108). The zone
# that spawns them writes Turtle's template over the stock one; its rollback puts the stock rows back (config
# creature_id_takeover: id -> the 3.3.5 name, checked so a used template is never taken).
TAKEOVER = {int(k): v for k, v in CFG.get('creature_id_takeover', {}).items() if not k.startswith('_')}
for _e, _n in TAKEOVER.items():
    assert ac_ct.get(_e) == _n, f'creature_id_takeover {_e}: 3.3.5 has {ac_ct.get(_e)!r}, not {_n!r}'
    assert not q(f"select 1 from {AC}.creature where id=%s limit 1".replace('id=', CRE_ID + '='), _e), f'creature_id_takeover {_e} is spawned in 3.3.5'
    del ac_ct[_e]
# Turtle creatures whose id 3.3.5 gives to a creature it spawns (Elder Moonhoof 29479 = Shoveltusk Forager): the build
# treats them as Turtle-only creatures and every row it writes uses creature_remap_base + the Turtle id (remap_creatures)
CREMAP = {}
for _k, _n in CFG.get('creature_id_remap', {}).items():
    if _k.startswith('_'):
        continue
    _e, _new = int(_k), IDS['creature_remap_base'] + int(_k)
    assert ac_ct.get(_e) == _n, f'creature_id_remap {_e}: 3.3.5 has {ac_ct.get(_e)!r}, not {_n!r}'
    assert _new not in ac_ct and not q(f"select 1 from {TW}.creature_template where entry=%s", _new), f'creature_id_remap: {_new} is taken'
    CREMAP[_e] = _new
    del ac_ct[_e]
CREMAP_COLS = [('creature', 'id1'), ('creature_template', 'entry'), ('creature_template_model', 'CreatureID'), ('creature_template_movement', 'CreatureId'),
               ('creature_template_addon', 'entry'), ('creature_template_resistance', 'CreatureID'), ('creature_template_spell', 'CreatureID'),
               ('creature_equip_template', 'CreatureID'), ('creature_text', 'CreatureID'), ('creature_onkill_reputation', 'creature_id'),
               ('creature_queststarter', 'id'), ('creature_questender', 'id'), ('npc_vendor', 'entry'), ('creature_default_trainer', 'CreatureId')]


def remap_creatures(rows):
    """creature_id_remap: the Turtle id -> the module's id in a zone's rows"""
    if not CREMAP:
        return
    for t_, c_ in CREMAP_COLS:
        for r_ in rows.get(t_, []):
            if r_.get(c_) in CREMAP:
                r_[c_] = CREMAP[r_[c_]]
    for r_ in rows.get('smart_scripts', []):
        if r_['source_type'] == 0 and r_['entryorguid'] in CREMAP:
            r_['entryorguid'] = CREMAP[r_['entryorguid']]
        if r_['action_type'] == 12 and r_['action_param1'] in CREMAP:          # summon creature
            r_['action_param1'] = CREMAP[r_['action_param1']]
    for r_ in rows.get('quest_template', []):
        for n_ in (1, 2, 3, 4):
            if r_.get(f'RequiredNpcOrGo{n_}') in CREMAP:
                r_[f'RequiredNpcOrGo{n_}'] = CREMAP[r_[f'RequiredNpcOrGo{n_}']]
    for r_ in rows.get('conditions', []):
        if r_['SourceTypeOrReferenceId'] == 22 and r_['SourceId'] == 0 and r_['SourceEntry'] in CREMAP:
            r_['SourceEntry'] = CREMAP[r_['SourceEntry']]
        if r_['ConditionTypeOrReference'] == 29 and r_['ConditionValue1'] in CREMAP:   # creature near
            r_['ConditionValue1'] = CREMAP[r_['ConditionValue1']]
    for r_ in rows.get('creature_template', []):
        for c_, lt_ in (('lootid', 'creature_loot_template'), ('skinloot', 'skinning_loot_template'), ('pickpocketloot', 'pickpocketing_loot_template')):
            if r_[c_] in CREMAP:                 # a loot table under the clashing id would replace the 3.3.5 creature's
                for l_ in rows.get(lt_, []):
                    if l_['Entry'] == r_[c_]:
                        l_['Entry'] = CREMAP[r_[c_]]
                r_[c_] = CREMAP[r_[c_]]


TAKEOVER_TABLES = [('creature_template', 'entry'), ('creature_template_model', 'CreatureID'), ('creature_template_movement', 'CreatureId'),
                   ('creature_template_addon', 'entry'), ('creature_template_resistance', 'CreatureID'), ('creature_template_spell', 'CreatureID'),
                   ('creature_equip_template', 'CreatureID'), ('creature_loot_template', 'Entry'), ('creature_text', 'CreatureID'),
                   ('creature_onkill_reputation', 'creature_id')]


def takeover_restore(entries):
    """rollback lines that put back the stock rows of taken-over 3.3.5 templates"""
    out = ''
    for e_ in sorted(set(entries) & set(TAKEOVER)):
        for t_, c_ in TAKEOVER_TABLES:
            out += f"DELETE FROM `{t_}` WHERE `{c_}`={e_};\n"
            for r_ in q(f"select * from {AC}.{t_} where {c_}=%s", e_):
                out += f"INSERT INTO `{t_}` ({', '.join('`%s`' % k for k in r_)}) VALUES ({', '.join(lit(v) for v in r_.values())});\n"
        out += f"DELETE FROM `smart_scripts` WHERE `entryorguid`={e_} AND `source_type`=0;\n"
        for r_ in q(f"select * from {AC}.smart_scripts where entryorguid=%s and source_type=0", e_):
            out += f"INSERT INTO `smart_scripts` ({', '.join('`%s`' % k for k in r_)}) VALUES ({', '.join(lit(v) for v in r_.values())});\n"
    return out
ac_it = {r['entry'] for r in q(f"select entry from {AC}.item_template")}
ac_gt = {r['entry']: r['name'] for r in q(f"select entry,name from {AC}.gameobject_template")}
ac_qt = {r['ID'] for r in q(f"select ID from {AC}.quest_template")}
ac_menu = {r['MenuID'] for r in q(f"select distinct MenuID from {AC}.gossip_menu")}
ac_text = {r['ID'] for r in q(f"select ID from {AC}.npc_text")}
ac_loot = {r['Entry'] for r in q(f"select distinct Entry from {AC}.creature_loot_template")}
ac_skin = {r['Entry'] for r in q(f"select distinct Entry from {AC}.skinning_loot_template")}
ac_pick = {r['Entry'] for r in q(f"select distinct Entry from {AC}.pickpocketing_loot_template")}
ac_page = {r['ID'] for r in q(f"select ID from {AC}.page_text")}
# Spells that are talents (any rank): AzerothCore rejects them in trainer_spell ("is a talent")
TALENT_SPELLS = {v for r in load(CFG['ac_dbc'] + '/Talent.dbc')[3] for v in r[4:13] if v}
cls = {(r['level'], r['class']): r for r in q(f"select * from {AC}.creature_classlevelstats")}

tw_area = load(CFG['tw_dbc'] + '/AreaTable.dbc')[3]
ac_area_ids = {r[0] for r in load(CFG['ac_dbc'] + '/AreaTable.dbc')[3]}
twmaps = MapSet(CFG['tw_maps'], 'tw')
acmaps = MapSet(CFG['ac_maps'], 'ac')
zones = ZoneLookup(twmaps, tw_area)
adt_zones = AdtAreas(CFG['tw_client_assets'], {0: 'Azeroth', 1: 'Kalimdor'}, tw_area, zones)


def _tile335(m_, X_, Y_):
    d_ = {0: 'Azeroth', 1: 'Kalimdor'}.get(m_)
    return client335_file(f"World\\Maps\\{d_}\\{d_}_{X_}_{Y_}.adt") if d_ else None


# zone_from_335_tiles (Stranglethorn): where Turtle did not change a tile, the zone comes from the 3.3.5 tile's areas
# (Turtle's server maps miss the north of Stranglethorn: Nesingwary's camp, Kurzen's Compound)
adt335_zones = AdtAreas(CFG['tw_client_assets'], {0: 'Azeroth', 1: 'Kalimdor'}, tw_area,
                        Client335Areas(lambda m_, X_, Y_: _tile335(m_, X_, Y_), load(CFG['ac_dbc'] + '/AreaTable.dbc')[3], zones))
disp = Displays(CFG['tw_dbc'], CFG['ac_dbc'])
TLOCK = {r[0]: r for r in load(CFG['tw_dbc'] + '/Lock.dbc')[3]}
ALOCK = {r[0]: r for r in load(CFG['ac_dbc'] + '/Lock.dbc')[3]}
ALOCK_BY_SIG = {}
for _k, _r in sorted(ALOCK.items()):
    ALOCK_BY_SIG.setdefault(tuple(_r[1:33]), _k)
AC_SOUND = {r[0] for r in load(CFG['ac_dbc'] + '/SoundEntries.dbc')[3]}
GO_SUB = {k.lower(): v for k, v in CFG.get('go_model_substitutions', {}).items() if not k.startswith('_')}
_man = json.load(open(os.path.join(CFG['tw_client_assets'], 'manifest.json')))
VANILLA_ASSETS = {k.lower() for k in _man['vanilla_only']}
LOCK_FIELD = {0: 1, 1: 1, 2: 0, 3: 0, 6: 0, 10: 0, 13: 0, 24: 0, 25: 4, 26: 0}   # GO type -> dataN holding the lock id
go_new_disp = {}           # turtle display id -> (new 3.3.5 display id, model path, sounds)


def conv_condition(cid, depth=0):
    """Turtle (vmangos) condition id -> list of AzerothCore condition groups [[(type, v1, v2, v3, negative), ...], ...]
    (the groups are ORed, the conditions inside a group ANDed), or None when a part has no AzerothCore equivalent."""
    r = q(f"select * from {TW}.conditions where condition_entry=%s", cid)
    if not r or depth > 3:
        return None
    r = r[0]
    t, v1, v2, neg = r['type'], r['value1'], r['value2'], 1 if r['flags'] & 1 else 0
    if t == 9:                                   # quest taken: value2 0 any state, 1 incomplete, 2 complete
        return [[(47, v1, {0: 2 | 8, 1: 8, 2: 2}.get(v2, 10), 0, neg)]]
    if t == 8:                                   # quest rewarded
        return [[(8, v1, 0, 0, neg)]]
    if t == 22:                                  # quest neither taken nor rewarded
        return [[(47, v1, 1, 0, neg)]]
    if t == -1 and not neg:                      # AND of up to 4 conditions
        out = [[]]
        for sub in (r['value1'], r['value2'], r['value3'], r['value4']):
            if not sub:
                continue
            g = conv_condition(sub, depth + 1)
            if g is None:
                return None
            out = [a + b for a in out for b in g]
        return out
    if t == -2 and not neg:                      # OR
        out = []
        for sub in (r['value1'], r['value2'], r['value3'], r['value4']):
            if not sub:
                continue
            g = conv_condition(sub, depth + 1)
            if g is None:
                return None
            out += g
        return out
    return None


def condition_rows(src_type, group, entry, cid, comment):
    groups = conv_condition(cid)
    if groups is None:
        return None
    return [dict(SourceTypeOrReferenceId=src_type, SourceGroup=group, SourceEntry=entry, SourceId=0, ElseGroup=eg,
                 ConditionTypeOrReference=c[0], ConditionTarget=0, ConditionValue1=c[1], ConditionValue2=c[2], ConditionValue3=c[3],
                 NegativeCondition=c[4], ErrorType=0, ErrorTextId=0, ScriptName='', Comment=comment)
            for eg, g in enumerate(groups) for c in g]


LOCK_SUB = {int(k): v for k, v in CFG.get('lock_substitutions', {}).items() if not k.startswith('_')}


def lock_map(lk):
    """Turtle lock id -> 3.3.5 lock id with the same requirements, or None (Turtle-only lock type).
    config.json lock_substitutions: a Turtle lock whose key item 3.3.5 cannot know -> a 3.3.5 lock (the key is then
    asked for by the zone's manual script, e.g. as a loot condition)."""
    if lk in LOCK_SUB:
        return LOCK_SUB[lk]
    t = TLOCK.get(lk)
    if not t:
        return None
    if lk in ALOCK and tuple(ALOCK[lk][1:33]) == tuple(t[1:33]):
        return lk
    return ALOCK_BY_SIG.get(tuple(t[1:33]))


def go_display(td, model):
    """Display for a Turtle GO model that has no 3.3.5 GameObjectDisplayInfo row.
    -> (display id or None, note). New rows go to the client patch and gameobjectdisplayinfo_dbc."""
    ml = model.lower().replace('/', '\\')
    sub = GO_SUB.get(ml)
    if isinstance(sub, int):
        return sub, f'stand-in display {sub} ({disp.wgs(disp.wg[sub][1])})'
    path = sub or model
    pl = path.lower()
    pb = os.path.splitext(pl)[0]
    known = sub is not None or any(x in VANILLA_ASSETS for x in (pl, pb + '.m2', pb + '.mdx')) or \
        pl.startswith(('world\\expansion01\\', 'world\\expansion02\\'))
    if not known:
        return None, 'Turtle-only model with no stand-in (add one to go_model_substitutions)'
    if td not in go_new_disp:
        nid = IDS['go_display_base'] + td
        assert nid not in disp.wg, f'GO display {nid} already exists'
        t = disp.tg[td]
        go_new_disp[td] = (nid, path, [x if x in AC_SOUND else 0 for x in t[2:12]])
    return go_new_disp[td][0], ('new display row' if sub is None else f'new display row with stand-in model {path}')
_tsp = load(CFG['tw_dbc'] + '/Spell.dbc')
TSPELL = {r[0]: r for r in _tsp[3]}
_asp = load(CFG['ac_dbc'] + '/Spell.dbc')
ASPELL = {r[0]: r for r in _asp[3]}
TSPELL_NAME = {k: _tsp[4](r[120]) for k, r in TSPELL.items()}
ASPELL_NAME = {k: _asp[4](r[136]) for k, r in ASPELL.items()}
QXP = {r[0]: r[1:11] for r in load(CFG['ac_dbc'] + '/QuestXP.dbc')[3]}
_wma = load(CFG['tw_dbc'] + '/WorldMapArea.dbc')[3]
WMA = {r[2]: [struct.unpack('<f', struct.pack('<I', v))[0] for v in r[4:8]] for r in _wma}
SPELL_SUB = {int(k): v for k, v in CFG['spell_substitutions'].items() if not k.startswith('_')}


def spell_conv(s):
    """Turtle spell id -> (3.3.5 spell id or None, note or None).
    An id only counts as present in 3.3.5 when the spell there has the same name: Turtle re-used many ids
    that are different spells in 3.3.5 (e.g. 47386 Mind Flay is 'Reagent Check' there)."""
    if not s:
        return None, None
    if s in SPELL_SUB:
        n = SPELL_SUB[s]
        return (n or None), f"spell {s} {TSPELL_NAME.get(s, '?')} -> " + (f"stand-in {n} {ASPELL_NAME.get(n, '?')}" if n else 'dropped (no 3.3.5 equivalent)')
    if s in ASPELL and (s not in TSPELL_NAME or ASPELL_NAME[s].lower() == TSPELL_NAME[s].lower()):
        return s, None
    if s in ASPELL:
        return None, f"spell {s} {TSPELL_NAME.get(s)} is '{ASPELL_NAME[s]}' in 3.3.5 - dropped (add a stand-in to spell_substitutions)"
    return None, f"spell {s} {TSPELL_NAME.get(s, '?')} does not exist in 3.3.5 - dropped (add a stand-in to spell_substitutions)"
ITEM_SPELL_REPL = {int(k): v for k, v in CFG['item_spell_replacements'].items()}
MOUNT_BY_ITEM = {int(k): v for k, v in CFG.get('mount_spell_by_item', {}).items() if not k.startswith('_')}
# Turtle bag family (a number) -> 3.3.5 bag family (bit mask). Turtle's cooking meat (10) and fish (11) have no 3.3.5 bag.
BAG_FAMILY = {1: 1, 2: 2, 3: 4, 6: 32, 7: 64, 8: 128, 9: 256, 12: 8, 13: 1024}
EXCL = CFG['global_excludes']

# Turtle reused item ids that 3.3.5 gives to other items (Balor quest items sit on Wrath gladiator gear ids).
#  - same item renamed by Blizzard ("Slayer's Shoulderguards"): names close -> the 3.3.5 item is used as is
#  - 3.3.5 moved the item to a new id and turned the old one into junk (TBC thrown weapons: "Broken Balanced
#    Throwing Dagger"): a 3.3.5 item with Turtle's exact name and class exists -> that item is used (ITEM_ALIAS)
#  - anything else is a different item: the Turtle item moves to item_remap_base + its Turtle id (ITEM_REMAP)
import difflib
_ac_items = q(f"select entry,name,class,subclass from {AC}.item_template")
ac_it_name = {r['entry']: r['name'] for r in _ac_items}
ac_it_class = {r['entry']: r['class'] for r in _ac_items}
_ac_by_name = {}
for _r in sorted(_ac_items, key=lambda r: r['entry']):
    _ac_by_name.setdefault(((_r['name'] or '').lower(), _r['class'], _r['subclass']), _r['entry'])
ITEM_REMAP, ITEM_ALIAS = {}, {}
for _r in q(f"select entry,name,class,subclass from {TW}.item_template"):
    _a = ac_it_name.get(_r['entry'])
    _n = (_r['name'] or '').lower()
    if _a is None or _a.lower() == _n:
        continue
    _same = _ac_by_name.get((_n, _r['class'], _r['subclass']))
    if _same:
        ITEM_ALIAS[_r['entry']] = _same
    elif difflib.SequenceMatcher(None, _n, _a.lower()).ratio() < (0.7 if ac_it_class[_r['entry']] != _r['class'] else 0.45):
        # (an item of another class needs a much closer name to count as the same item)
        ITEM_REMAP[_r['entry']] = IDS['item_remap_base'] + _r['entry']


def I(i):
    """Turtle item id -> id in the module"""
    return ITEM_ALIAS.get(i) or ITEM_REMAP.get(i, i) if i else i


def ac_item(i):
    """the Turtle item exists in 3.3.5 (same id, or ITEM_ALIAS) - nothing to port"""
    return i in ITEM_ALIAS or (i in ac_it and i not in ITEM_REMAP)


# vanilla XP per quest-level baseline (median "full" reward of vanilla quests), used to keep Turtle's relative tier
_xp = collections.defaultdict(list)
for r in q(f"select a.QuestLevel l, a.RewardXPDifficulty d, t.RewXP x from {AC}.quest_template a join {TW}.quest_template t on t.entry=a.ID where a.ID<10000 and t.RewXP>0 and a.RewardXPDifficulty=5 and a.QuestLevel=t.QuestLevel"):
    _xp[r['l']].append(r['x'])
VANILLA_FULL = {l: sorted(v)[len(v) // 2] for l, v in _xp.items()}
TIER = {1: 0.1, 2: 0.25, 3: 0.5, 4: 0.75, 5: 1.0, 6: 1.25, 7: 1.5, 8: 2.0}


def xp_difficulty(level, xp):
    full = VANILLA_FULL.get(level) or VANILLA_FULL.get(min(VANILLA_FULL, key=lambda l: abs(l - level))) * level / min(VANILLA_FULL, key=lambda l: abs(l - level))
    return min(TIER, key=lambda d: abs(TIER[d] * full - xp))


NPCFLAG = {1: 1, 2: 2, 4: 128, 8: 8192, 16: 16, 32: 16384, 64: 32768, 128: 65536, 256: 131072, 512: 262144,
           1024: 524288, 2048: 1048576, 4096: 2097152, 8192: 4194304, 16384: 4096}


def conv_npcflag(v):
    return sum(n for b, n in NPCFLAG.items() if v & b)


def conv_races(m):
    if not m or m < 0:
        return 0
    out = m & 0xFF
    alliance = (m & 0x4D) == 0x4D or bool(m & 512)
    horde = (m & 0xB2) == 0xB2 or bool(m & 256)
    if alliance and not (m & 0xB2):
        out |= 1024
    if horde and not (m & 0x4D):
        out |= 512
    return out


def item_excluded(i):
    for lo, hi in EXCL['item_ids_min_max_excluded']:
        if lo <= i['entry'] <= hi and i['entry'] not in quest_items:     # a quest's own reward/objective is always ported
            return True
    # recipe-like names ("Plans: ...") are Turtle-only recipes; a quest item with such a name (class 12) is kept
    return any((i['name'] or '').startswith(p) for p in EXCL['item_name_prefixes']) and not ac_item(i['entry']) and i['class'] != 12


def learned_spell(teach):
    r = TSPELL.get(teach)
    if not r:
        return None
    for e, t in zip(r[61:64], r[109:112]):
        if e == 36 and t:
            return t
    return None


# vmangos EventAI -> SmartAI ---------------------------------------------------------------------------
EAI_EVENT = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 12: 12, 13: 13, 14: 14, 16: 16, 17: 17, 18: 18, 21: 21}
EAI_SWAP_MINMAX = {2, 3, 12, 18}          # EventAI: max%, min%   SmartAI: min%, max%
EAI_TARGET = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 1}


EAI_TEXT_TYPE = {0: 12, 1: 14, 2: 16, 3: 41, 4: 15, 5: 42, 6: 14}     # Turtle ChatType -> creature_text.Type


def eventai_to_smart(entry, name, first_id):
    """Turtle EventAI -> SmartAI rows. Script commands: cast (15), talk (0, texts become creature_text groups 50+),
    flee (47). Returns (smart rows, notes, creature_text rows)."""
    out, notes, texts = [], [], []
    sid = first_id
    tgroup = 50
    for ev in q(f"select * from {TW}.creature_ai_events where creature_id=%s order by id", entry):
        et = ev['event_type']
        if et == 11:                         # spawned -> on creation and on every respawn
            smart_events = [(63, [0, 0, 0, 0]), (11, [0, 0, 0, 0])]
        elif et in EAI_EVENT:
            p = [ev[f'event_param{i}'] for i in range(1, 5)]
            if et in EAI_SWAP_MINMAX:
                p[0], p[1] = p[1], p[0]
            smart_events = [(EAI_EVENT[et], p)]
        else:
            notes.append(f"EventAI event type {et} ({ev['comment']}) has no SmartAI conversion - left out")
            continue
        acts = []
        for col in ('action1_script', 'action2_script', 'action3_script'):
            if not ev[col]:
                continue
            for sc in q(f"select * from {TW}.creature_ai_scripts where id=%s order by delay, priority", ev[col]):
                if sc['command'] == 0:                       # talk: one creature_text group, random among the given texts
                    bids = [b for b in (sc['dataint'], sc['dataint2'], sc['dataint3'], sc['dataint4']) if b]
                    bts = [q(f"select * from {TW}.broadcast_text where entry=%s", b) for b in bids]
                    bts = [b[0] for b in bts if b]
                    if not bts:                              # negative ids: Turtle's script_texts (their type decides say / yell)
                        sts = [q(f"select * from {TW}.script_texts where entry=%s", b) for b in bids if b < 0]
                        bts = [dict(male_text=r[0]['content_default'], female_text='', sound_id=r[0]['sound'], language_id=r[0]['language'],
                                    emote_id1=r[0]['emote'], _type=r[0]['type']) for r in sts if r]
                    if not bts:
                        notes.append(f"talk ({sc['comments']}): broadcast text {bids} not in the Turtle DB - left out")
                        continue
                    for i_, bt in enumerate(bts):
                        snd = bt.get('sound_id') or 0
                        texts.append(dict(CreatureID=entry, GroupID=tgroup, ID=i_, Text=bt['male_text'] or bt['female_text'],
                                          Type=EAI_TEXT_TYPE.get(bt.get('_type', sc['datalong']), 12), Language=bt['language_id'] or 0, Probability=0,
                                          Emote=bt['emote_id1'] or 0, Duration=0, Sound=snd if snd in AC_SOUND else 0, BroadcastTextId=0,
                                          TextRange=0, comment=f"{name} - {sc['comments'] or 'EventAI'}"))
                    acts.append(dict(t=1, p=[tgroup, 0, 0], tt=7 if bts[0].get('_type', sc['datalong']) in (4, 5) else 1, cm=sc['comments'] or 'Say'))
                    tgroup += 1
                    continue
                if sc['command'] == 47:                      # flee (Turtle: optionally looking for help)
                    acts.append(dict(t=25, p=[1, 0, 0], tt=1, cm=sc['comments'] or 'Flee'))
                    continue
                if sc['command'] != 15:
                    notes.append(f"script command {sc['command']} ({sc['comments']}) not converted")
                    continue
                sp, why = spell_conv(sc['datalong'])
                if why:
                    notes.append(why)
                if not sp:
                    continue
                if sc['data_flags'] & 4 or sc['target_type'] == 6:
                    tt = 1
                elif sc['target_type'] in (0, 15) and et in (14, 15, 16, 17):
                    tt = 7
                else:
                    tt = EAI_TARGET.get(sc['target_type'], 2)
                acts.append(dict(t=11, p=[sp, sc['datalong2'] & 0x03, 0], tt=tt, cm=sc['comments']))
        repeat = bool(ev['event_flags'] & 1)
        for smart_ev, p in smart_events:
            for a_ in acts:
                tt, cm = a_['tt'], a_['cm']
                out.append(dict(entryorguid=entry, source_type=0, id=sid, link=0, event_type=smart_ev, event_phase_mask=0,
                                event_chance=ev['event_chance'] or 100,
                                event_flags=0 if (repeat or smart_ev in (4, 6, 7, 11, 63)) else 1,
                                event_param1=p[0], event_param2=p[1], event_param3=p[2], event_param4=p[3], event_param5=0, event_param6=0,
                                action_type=a_['t'], action_param1=a_['p'][0], action_param2=a_['p'][1], action_param3=a_['p'][2],
                                action_param4=0, action_param5=0, action_param6=0, target_type=tt, target_param1=0, target_param2=0, target_param3=0, target_param4=0,
                                target_x=0, target_y=0, target_z=0, target_o=0, comment=f"{name} - {cm} (Turtle EventAI {ev['id']})"))
                sid += 1
    return out, notes, texts


# --------------------------------------------------------------------------- global state across zones
owned = {'creature': {}, 'quest': {}, 'gameobject': {}, 'menu': {}, 'text': {}, 'loot': {}, 'skin': {}, 'pick': {}}   # id -> zone slug
pages_needed = set()       # Turtle page_text ids (items, text objects, goobers) -> exported in the common file
GO_PAGE_FIELD = {9: (0,), 10: (7,)}     # gameobject type -> Data field holding a page_text id (text object, goober)
_go_fixed = set()


def page_ref(pid):
    """a page id the module refers to: 3.3.5's own page when it has that id, otherwise Turtle's chain is exported"""
    if pid and pid not in ac_page:
        pages_needed.add(pid)
    return pid
items_needed = set()
quest_items = set()        # Turtle items a ported quest gives, asks for or starts from
refs_needed = set()
all_reports = []

common = Sql()
zone_files = {}
pending_render = []
ORDER = ['creature_template', 'creature_template_model', 'creature_template_resistance', 'creature_template_movement',
         'creature_template_addon', 'creature_equip_template', 'creature', 'creature_addon', 'waypoint_data',
         'npc_text', 'gossip_menu', 'gossip_menu_option', 'conditions', 'npc_vendor', 'trainer', 'trainer_spell', 'creature_default_trainer',
         'creature_loot_template', 'skinning_loot_template', 'pickpocketing_loot_template',
         'creature_onkill_reputation', 'creature_text', 'smart_scripts',
         'quest_template', 'quest_template_addon', 'quest_offer_reward', 'quest_request_items',
         'creature_queststarter', 'creature_questender', 'gameobject_queststarter', 'gameobject_questender',
         'gameobject_template', 'gameobject_template_addon', 'gameobject_loot_template', 'gameobject',
         'pool_template', 'pool_pool', 'pool_gameobject', 'pool_creature', 'areatable_dbc']
client_tiles = []          # (archive path, fixed ADT bytes) for the client patch + server map extraction


def add_tile(ap_, data, m):
    """Every shipped tile goes through here: orphan MCLQ bytes are removed and the client-style MCNK walk must
    pass (an unreferenced sub-chunk crashes the 3.3.5 client, error #132 in the MCNK parser). Area ids 3.3.5 uses for
    another area are rewritten (config area_id_remap)."""
    if AREA_REMAP:
        data = remap_tile_areas(data)
    from lib.adt import strip_orphan_mclq, mcnk_problems
    data, n_ = strip_orphan_mclq(data)
    pr_ = mcnk_problems(data)
    assert not pr_, f'{ap_}: {pr_[:3]}'
    for i_, (a_, _, _) in enumerate(client_tiles):
        if a_ == ap_:                     # a tile an earlier zone already shipped (merged again on top of it)
            client_tiles[i_] = (ap_, data, m)
            return
    client_tiles.append((ap_, data, m))


def remap_tile_areas(data):
    """MCNK area ids of a shipped tile: Turtle ids 3.3.5 uses for another area -> config area_id_remap"""
    from lib.adt import mcnk_offsets
    d = bytearray(data)
    for off in mcnk_offsets(d):
        a_ = struct.unpack_from('<I', d, off + 8 + 52)[0]
        if a_ in AREA_REMAP:
            struct.pack_into('<I', d, off + 8 + 52, AREA_REMAP[a_])
    return bytes(d)


def shipped_tile(ap_):
    """the bytes of a tile an earlier zone of this build already ships, or None"""
    for a_, d_, _ in client_tiles:
        if a_ == ap_:
            return d_
    return None
client_areas = []          # 3.3.5 AreaTable rows (36 fields, strings as text) for the client patch
used_area_bits = {}        # bit -> area id, across all zones
AC_AREA = {r[0]: r for r in load(CFG['ac_dbc'] + '/AreaTable.dbc')[3]}
for _r in AC_AREA.values():
    used_area_bits[_r[3]] = _r[0]
TW_AREA = {r[0]: r for r in tw_area}
# Turtle area ids 3.3.5 uses for another area (Turtle reused ids of Northrend areas): new ids everywhere they are written
AREA_REMAP = {int(k): v for k, v in CFG.get('area_id_remap', {}).items() if not k.startswith('_')}
assert not set(AREA_REMAP.values()) & (set(r[0] for r in tw_area) | ac_area_ids), 'area_id_remap: a new id is used by Turtle or 3.3.5'


def AR(a):
    """a Turtle area id as the module writes it"""
    return AREA_REMAP.get(a, a)
_tw_area_str = load(CFG['tw_dbc'] + '/AreaTable.dbc')[4]
NEW_AREA = {}              # area id -> 3.3.5 AreaTable row added by this build
keep_335_minimap = set()   # merged tiles whose minimap image stays the 3.3.5 one
turtle_chunks = {}         # merged tile -> chunks taken from Turtle, over all zones that merge into it
wdt_tiles = {}             # map directory -> {(x, y)} tiles shipped (added to the WDT when the 3.3.5 one lacks them)
ship_files = {}            # archive path -> local path or bytes (Turtle buildings, textures, WDTs ...)
new_maps_dir = {}          # map id -> directory, for maps this build adds
zone_extras = []           # (zone json, slug, notes) for the map/taxi/world-map pass after all zones
guid_maps = {}             # slug -> {'creature': {tw guid: new guid}, 'gameobject': {...}}
from lib.assets import TurtleAssets
ASSETS = TurtleAssets(CFG['tw_client_assets'], CFG.get('m2_substitutions', {}), CFG.get('never_ship', []))


def tw_asset_path(ap_):
    """path of a Turtle client file in the extract folder; the extract keeps the case of Turtle's archives
    (world\\maps\\tanarisinstance\\... in lower case), so fall back to a case-insensitive lookup"""
    p_ = os.path.join(CFG['tw_client_assets'], *ap_.split('\\'))
    if os.path.exists(p_):
        return p_
    return ASSETS.local.get(ap_.replace('/', '\\').lower(), p_)


ZONE_MUSIC_SUB = {int(k): v for k, v in CFG.get('zone_music_substitutions', {}).items() if not k.startswith('_')}
INTRO_SUB = {int(k): v for k, v in CFG.get('intro_music_substitutions', {}).items() if not k.startswith('_')}


# =========================================================================== per zone
AREA_COLS = ['ID', 'ContinentID', 'ParentAreaID', 'AreaBit', 'Flags', 'SoundProviderPref', 'SoundProviderPrefUnderwater', 'AmbienceID',
             'ZoneMusic', 'IntroSound', 'ExplorationLevel'] + \
            ['AreaName_Lang_' + l for l in ('enUS', 'enGB', 'koKR', 'frFR', 'deDE', 'enCN', 'zhCN', 'enTW', 'zhTW', 'esES', 'esMX',
                                            'ruRU', 'ptPT', 'ptBR', 'itIT', 'Unk')] + \
            ['AreaName_Lang_Mask', 'FactionGroupMask', 'LiquidTypeID_1', 'LiquidTypeID_2', 'LiquidTypeID_3', 'LiquidTypeID_4',
             'MinElevation', 'Ambient_Multiplier', 'Lightid']


_planned = None


def planned_creatures():
    """creature templates spawned in any zone of this build (computed once, from Turtle spawn positions)"""
    global _planned
    if _planned is None:
        _planned = set()
        for z_ in CFG['zones']:
            Zp = json.load(open(os.path.join(HERE, 'zones', z_ + '.json')))
            for r_ in q(f"select id, position_x x, position_y y from {TW}.creature where map=%s", Zp['map']):
                if Zp.get('all_spawns') or zone_of_tw(Zp['map'], r_['x'], r_['y'], Zp)[0] == Zp['zone_id']:
                    _planned.add(r_['id'])
            _planned |= set(Zp.get('extra_creature_templates', []))
            if Zp.get('extra_spawns'):
                _planned |= {r_['id'] for r_ in q(f"select id from {TW}.creature where guid in ({in_list(Zp['extra_spawns'])})")}
    return _planned


def other_zone_extras(slug, key):
    """Turtle guids another zone of this build spawns as its extra_spawns / extra_gameobject_spawns -> that zone
    (a quest NPC brought along early, e.g. Feralas' Larodar Wildwhisper with Gilneas): this zone leaves them to it"""
    out = {}
    for z_ in CFG['zones']:
        if z_ == slug:
            continue
        for g_ in json.load(open(os.path.join(HERE, 'zones', z_ + '.json'))).get(key, []):
            out[g_] = z_
    return out


def zone_of_tw(m, x, y, Z=None):
    if Z and Z.get('zone_from_335_tiles'):
        return adt335_zones.zone_of(m, x, y)
    if Z and Z.get('zone_from_adt'):
        return adt_zones.zone_of(m, x, y)
    return zones.zone_of(m, x, y)


def archive_rank(a):
    """Load priority of a 3.3.5 client archive (higher wins). Tested on the server owner's client: a table in
    Data\\patch-y.mpq beats the same table in Data\\enUS\\patch-enUS-z.mpq, and Data\\patch-z beats patch-y. So:
    Data\\patch-<char> > enUS\\patch-enUS-<char> > enUS\\patch-enUS > Data\\patch > the base archives;
    inside each group alphabetical (digits before letters, case ignored), last wins."""
    folder_enus = '\\' in a
    n = os.path.splitext(a.split('\\')[-1])[0].lower()
    if n.startswith('patch-enus-') or (n.startswith('patch-') and len(n) == 7):
        suf = n.split('-')[-1]
        key = (0 if suf.isdigit() else 1, suf)
        return (4 if not folder_enus and not n.startswith('patch-enus') else 3, key)
    if n == 'patch-enus':
        return (2, (0, ''))
    if n == 'patch':
        return (1, (0, ''))
    order = ['common', 'common-2', 'expansion', 'lichking', 'locale-enus', 'expansion-locale-enus', 'lichking-locale-enus', 'base-enus', 'backup-enus']
    return (0, (order.index(n) if n in order else -1, ''))


def client335_archive(path):
    """the archive whose copy of a 3.3.5 client file the client really loads (from the client335 extract), or None"""
    rep = json.load(open(os.path.join(CFG['client335'], 'report.json')))
    # HD terrain archives are ignored for map tiles only (the user's choice); tables and other files come from
    # whichever archive the client really loads
    skip = set(CFG.get('client335_skip_archives', {}).get('list', [])) if path.lower().endswith('.adt') else set()
    have = [a for a, fs in rep['files'].items() if path in fs and a not in skip]
    return max(have, key=archive_rank) if have else None


def client335_file(path):
    """the copy of a 3.3.5 client file the client really loads (from the client335 extract), or None"""
    a = client335_archive(path)
    return os.path.join(CFG['client335'], a.replace('\\', '_'), *path.split('\\')) if a else None


def build_zone(slug):
    Z = json.load(open(os.path.join(HERE, 'zones', slug + '.json')))
    zid, m, slot = Z['zone_id'], Z['map'], Z['slot']
    gbase = IDS['guid_base'] + slot * IDS['guid_per_zone']
    notes = collections.defaultdict(list)
    print(f"[{slug}] {Z['name']}")
    custom_sub = {r[0] for r in tw_area if r[2] == zid and (r[0] not in ac_area_ids or r[0] in AREA_REMAP)}
    # y-left, y-right, x-top, x-bottom; a 3.3.5 dungeon Turtle added to (Zul'Farrak) has no world-map rectangle: its
    # spawns are found with all_spawns or listed in extra_spawns
    assert zid in WMA or Z.get('all_spawns'), f'zone {zid} has no WorldMapArea row: set all_spawns'
    left, right, top, bottom = WMA.get(zid, (0, 0, 0, 0))
    xs, ys = sorted((top, bottom)), sorted((left, right))
    if Z.get('merge_region') and Z.get('spawns_in_whole_region'):
        # spawns are looked for over the whole merged region too (the world-map rectangle can be smaller than the zone:
        # Captain Ironhoof's ship off Lapidis Isle). Opt-in: on Northwind it would add 13 NPCs and 125 objects (not yet checked)
        mr_ = Z['merge_region']
        xs = [min(xs[0], (32 - mr_['y'][1] - 1) * 533.3333), max(xs[1], (32 - mr_['y'][0]) * 533.3333)]
        ys = [min(ys[0], (32 - mr_['x'][1] - 1) * 533.3333), max(ys[1], (32 - mr_['x'][0]) * 533.3333)]

    zl = adt335_zones if Z.get('zone_from_335_tiles') else adt_zones if Z.get('zone_from_adt') else zones

    def in_zone(x, y):
        return True if Z.get('all_spawns') else zl.zone_of(m, x, y)[0] == zid
    if Z.get('all_spawns'):                    # instance map: everything on the map belongs to this zone
        xs, ys = (-1e6, 1e6), (-1e6, 1e6)

    def subzone(x, y):
        return zl.zone_of(m, x, y)[1]

    # ---------------- terrain (client tiles, new subzones)
    terrain_mode = Z.get('terrain', 'stock')
    area_rows = []
    wmap = Z.get('map_dir') or {0: 'Azeroth', 1: 'Kalimdor'}[m]
    # (a WMO-only instance map has no tiles: its area rows (area_bits) and client files are still made here)
    if terrain_mode == 'turtle' and (Z.get('terrain_tiles') or Z.get('merge_region') or Z.get('area_bits')):
        from lib.adt import fix as adt_fix, area_ids as adt_area_ids, UID_BASE, substitute_models as adt_subst
        uid_map, seq = {}, [0]

        def alloc():
            seq[0] += 1
            assert seq[0] < 0x10000
            return UID_BASE + slot * 0x10000 + seq[0]
        tile_areas = set()
        zone_tiles = []
        closure_names = ([], [])            # (textures, WMOs) the merged tiles take from Turtle
        for t in Z.get('terrain_tiles', []):
            ap_ = f"World\\Maps\\{wmap}\\{wmap}_{t}.adt"
            src = tw_asset_path(ap_)
            data, st = adt_fix(open(src, 'rb').read(), uid_map, alloc)
            data, ch = adt_subst(data, ASSETS.model_sub)
            add_tile(ap_, data, m)
            zone_tiles.append(data)
            tile_areas |= adt_area_ids(data)
            x_, y_ = map(int, t.split('_'))
            wdt_tiles.setdefault(wmap, set()).add((x_, y_))
            notes['client_tiles'].append(f"{wmap}_{t}: {st['mclq_ff']} empty-liquid offsets fixed, {st['mh2o_dedup']} duplicated water layers collapsed, "
                                         f"{st['mclq_dropped']} legacy liquid blocks dropped, {st['uids']} object ids moved"
                                         + (f", {len(ch)} Turtle models replaced" if ch else ''))
        if Z.get('merge_region'):
            # tiles shared with live 3.3.5 land: the 3.3.5 tile, with Turtle's chunks wherever the chunk belongs to
            # this zone or Turtle reshaped the ground (so Turtle's own slopes meet 3.3.5's where Turtle left it as it was)
            from lib import adtmerge
            mr = Z['merge_region']
            tol = mr.get('height_tolerance', 0.5)
            fam = {a for a, r_ in TW_AREA.items() if a == zid or r_[2] == zid}
            fam_new = {a for a in fam if a not in AC_AREA or a in AREA_REMAP}
            own_mode = mr.get('own', 'all')
            own_excl = set(mr.get('own_exclude_areas', []))   # the zone's sea areas Turtle reshaped for other zones (Wetlands)
            own_excl_ch = set(mr.get('own_exclude_chunks', []))  # "X_Y:chunk": a zone chunk Turtle barely touched that would meet ground left 3.3.5 in a cliff
            # exclude_chunks (Eastern Plaguelands): "X_Y:chunk" never taken from Turtle, neither as the zone's own ground nor as
            # reshaped ground next to it (Turtle's rim raised to meet a Turtle zone that is not ported: left 3.3.5, no cliff)
            excl_ch_all = set(mr.get('exclude_chunks', []))
            sources, taken, areas_kept = {}, {}, {}
            own_g, reshaped_g = set(), set()
            ocean_built = set()                  # region tiles 3.3.5 does not have (ocean_base)
            for X in range(mr['x'][0], mr['x'][1] + 1):
                for Y in range(mr['y'][0], mr['y'][1] + 1):
                    ap_ = f"World\\Maps\\{wmap}\\{wmap}_{X}_{Y}.adt"
                    bp = client335_file(ap_)
                    src = tw_asset_path(ap_)
                    if not os.path.exists(src) or f'{X}_{Y}' in Z.get('terrain_tiles', []):
                        continue
                    prev_ = shipped_tile(ap_)
                    if prev_ is not None:
                        # an earlier zone of this build merged Turtle chunks into this tile (neighbouring Turtle zones,
                        # e.g. Gillijim's Isle and Lapidis Isle): its result is the base, so both zones' chunks stay
                        base = adtmerge.Tile(prev_)
                        notes['client_tiles'].append(f"{wmap}_{X}_{Y}: merged on top of an earlier zone's tile")
                    elif bp:
                        base = adtmerge.Tile(open(bp, 'rb').read())
                    elif mr.get('ocean_base'):
                        # 3.3.5 has no tile here (the WDT ends): a stock open-sea tile moved to this position is the base,
                        # and the tile is added to the client's WDT
                        ob = client335_file(mr['ocean_base'])
                        assert ob, f"ocean_base {mr['ocean_base']} is not in the 3.3.5 extract"
                        base = adtmerge.Tile(adtmerge.moved_tile(open(ob, 'rb').read(), X, Y))
                        ocean_built.add((X, Y))
                    else:
                        continue
                    data, st = adt_fix(open(src, 'rb').read(), uid_map, alloc)
                    data, ch = adt_subst(data, ASSETS.model_sub)
                    don = adtmerge.Tile(data)
                    sources[(X, Y)] = (base, don)
                    # take_new_wmos: a chunk holding the origin of a building Turtle added (a WMO 3.3.5's tile does not
                    # have at that place) counts as changed even when its ground is not (a cave mouth cut with holes,
                    # a hut on flat ground): without it own=changed drops the building (Windhorn Canyon's entrance cave)
                    new_wmo_ch_ = {}
                    take_wmo_names_ = {n_.lower() for n_ in mr.get('take_wmo_names', [])}
                    if mr.get('take_new_wmos') or take_wmo_names_:
                        def _wp(t_, r_):
                            n_ = struct.unpack_from('<I', r_, 0)[0]
                            px_, py_, pz_ = struct.unpack_from('<3f', r_, 8)
                            return (t_.wmos[n_].lower() if n_ < len(t_.wmos) else n_), px_, py_, pz_
                        base_w_ = [_wp(base, r_) for r_ in base.modf]
                        for r_ in don.modf:
                            nm_, px_, py_, pz_ = _wp(don, r_)
                            if not any(b_[0] == nm_ and abs(b_[1] - px_) < 3 and abs(b_[2] - py_) < 3 and abs(b_[3] - pz_) < 3 for b_ in base_w_):
                                c_ = adtmerge.chunk_of((X, Y), px_, pz_)
                                if c_ is not None:
                                    new_wmo_ch_.setdefault(c_, str(nm_).split(chr(92))[-1])
                    for i in range(256):
                        g_ = (X * 16 + i % 16, Y * 16 + i // 16)          # chunk in whole-map coordinates
                        changed_ = max(abs(a_ - b_) for a_, b_ in zip(don.heights(i), base.heights(i))) > tol or i in new_wmo_ch_
                        if mr.get('take_hole_changes') and not changed_ and \
                                (struct.unpack_from('<I', don.mcnk[i], 0x3C)[0] & 0xFFFF) != (struct.unpack_from('<I', base.mcnk[i], 0x3C)[0] & 0xFFFF):
                            # take_hole_changes: a chunk where Turtle cut or filled terrain holes (a cave mouth into a new
                            # WMO, Zul'Farrak's ritual cave) counts as changed even when its heights did not move
                            changed_ = True
                            notes['client_tiles'].append(f"{wmap}_{X}_{Y}: chunk {i} taken for its terrain holes")
                        if f'{X}_{Y}:{i}' in excl_ch_all:
                            continue
                        if i in new_wmo_ch_ and new_wmo_ch_[i] in take_wmo_names_:
                            # take_wmo_names: a Turtle building the zone needs whose origin chunk lies over the zone's
                            # border (Windhorn Canyon's entrance cave MooCave, origin in Dustwallow Marsh)
                            own_g.add(g_)
                            notes['client_tiles'].append(f"{wmap}_{X}_{Y}: chunk {i} (area {don.area(i)}) taken for Turtle's {new_wmo_ch_[i]}")
                        elif don.area(i) in fam and don.area(i) not in own_excl and f'{X}_{Y}:{i}' not in own_excl_ch:
                            # own: "changed" (a 3.3.5 zone Turtle reworked, e.g. the Wetlands): only the zone's chunks Turtle
                            # reshaped or gave a new area; its other chunks stay 3.3.5 (3.3.5 spawns stand on them)
                            if own_mode == 'all' or changed_ or don.area(i) in fam_new:
                                own_g.add(g_)
                                if i in new_wmo_ch_:
                                    notes['client_tiles'].append(f"{wmap}_{X}_{Y}: chunk {i} taken for Turtle's {new_wmo_ch_[i]}")
                        elif changed_:
                            reshaped_g.add(g_)
            if mr.get('reshaped', 'all') == 'sea':
                # Turtle land on 3.3.5 open sea: every Turtle chunk differs from the deep 3.3.5 sea floor, so "connected"
                # would run into the neighbouring Turtle zones. Take only the sea bed around the zone: chunks under water
                # in both tiles, reached from the zone through such chunks, never in a zone listed in reshaped_skip_zones
                # (a Turtle zone not ported yet). Without it the zone's shallow sea bed ends in a cliff to the 3.3.5 floor.
                sea_below = mr.get('sea_below', -2.0)
                skip_z = set(mr.get('reshaped_skip_zones', []))

                def ring(g_):                    # a chunk next to a tile outside the merge (no seam can be made there)
                    return any(((g_[0] + dx_) // 16, (g_[1] + dy_) // 16) not in sources
                               for dx_, dy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)))

                sx_, sy_ = mr.get('sea_take', mr)['x'], mr.get('sea_take', mr)['y']

                def under(g_):
                    if ring(g_) or not (sx_[0] <= g_[0] // 16 <= sx_[1] and sy_[0] <= g_[1] // 16 <= sy_[1]):
                        return False             # sea bed only inside sea_take (the margin tiles are seam partners)
                    base, don = sources[(g_[0] // 16, g_[1] // 16)]
                    i_ = (g_[1] % 16) * 16 + g_[0] % 16
                    a_ = don.area(i_)
                    zf = (TW_AREA[a_][2] or a_) if a_ in TW_AREA else None
                    if zf is None and mr.get('take_unnamed_land'):
                        return True              # Turtle ground with no area of its own (small islets): belongs to no other zone
                    return zf not in skip_z and max(don.heights(i_)) < sea_below and max(base.heights(i_)) < sea_below
                keep_g, stack_ = set(), list(own_g)
                while stack_:
                    gx_, gy_ = stack_.pop()
                    for n_ in ((gx_ + 1, gy_), (gx_ - 1, gy_), (gx_, gy_ + 1), (gx_, gy_ - 1)):
                        if n_ in reshaped_g and n_ not in keep_g and under(n_):
                            keep_g.add(n_)
                            stack_.append(n_)
                notes['client_tiles'].append(f"{len(keep_g)} sea-bed chunks around the zone taken from Turtle (keep their 3.3.5 area); "
                                             f"{len(reshaped_g - keep_g)} other reshaped chunks left as 3.3.5 (reshaped: sea)")
                reshaped_g = keep_g
            elif mr.get('reshaped', 'all') == 'none':
                # nothing outside the zone: Turtle's edits of the zones around stay 3.3.5 (seams are stitched)
                notes['client_tiles'].append(f"{len(reshaped_g)} reshaped chunks outside the zone left as 3.3.5 (reshaped: none)")
                reshaped_g = set()
            elif mr.get('reshaped', 'all') == 'connected':
                # only reshaped ground that touches the zone (its slopes down to the 3.3.5 land); Turtle's edits
                # elsewhere in the region (other zones it reworked) stay 3.3.5
                # connect_depth: at most that many chunks away from the zone (the Wetlands: Turtle's Dun Morogh slopes
                # under Dun Agrath, not the whole of Turtle's Dun Morogh rework)
                depth_ = mr.get('connect_depth', 10 ** 6)
                # reshaped_skip_zones (Azshara): never into ground Turtle gave to these zones (Moonwhisper Coast, a Turtle
                # zone not ported yet; Hyjal, already merged; Winterspring's furbolg village) - their seams are stitched
                cskip_ = set(mr.get('reshaped_skip_zones', []))
                # reshaped_take_areas (Stonetalon): areas taken even though their zone is skipped (the Veiled Sea off
                # Desolace/Ashenvale, whose sea bed Turtle raised into Stonetalon's new coast: left 3.3.5 it is a 500-yd drop)
                ctake_ = set(mr.get('reshaped_take_areas', []))

                def cskipped(g_):
                    if not cskip_:
                        return False
                    don_ = sources[(g_[0] // 16, g_[1] // 16)][1]
                    a_ = don_.area((g_[1] % 16) * 16 + g_[0] % 16)
                    return a_ not in ctake_ and a_ in TW_AREA and (TW_AREA[a_][2] or a_) in cskip_
                keep_g, front_, lvl_ = set(), list(own_g), 0
                while front_ and lvl_ < depth_:
                    nxt_ = []
                    for gx_, gy_ in front_:
                        for dx_ in (-1, 0, 1):
                            for dy_ in (-1, 0, 1):
                                n_ = (gx_ + dx_, gy_ + dy_)
                                if n_ in reshaped_g and n_ not in keep_g and not cskipped(n_):
                                    keep_g.add(n_)
                                    nxt_.append(n_)
                    front_, lvl_ = nxt_, lvl_ + 1
                notes['client_tiles'].append(f"{len(keep_g)} reshaped chunks next to the zone taken (keep their 3.3.5 area); "
                                             f"{len(reshaped_g - keep_g)} reshaped chunks away from the zone left as 3.3.5")
                reshaped_g = keep_g
            # include_chunks (Burning Steppes): chunks always taken from Turtle as reshaped ground (keep the area of the
            # tile below). Used where an earlier zone already took the Turtle chunk next door and stitched its edge
            # onto 3.3.5: taking it again puts the Turtle edge back, without a dip along the line between the two.
            for s_ in mr.get('include_chunks', []):
                t_, ic_ = s_.split(':')
                X_, Y_ = map(int, t_.split('_'))
                if (X_, Y_) in sources:
                    g_ = (X_ * 16 + int(ic_) % 16, Y_ * 16 + int(ic_) // 16)
                    if g_ not in own_g:
                        reshaped_g.add(g_)
            for g_ in sorted(own_g | reshaped_g):
                X, Y = g_[0] // 16, g_[1] // 16
                i = (g_[1] % 16) * 16 + g_[0] % 16
                taken.setdefault((X, Y), set()).add(i)
                if g_ in reshaped_g:               # reshaped ground outside the zone keeps its 3.3.5 area
                    base, don = sources[(X, Y)]
                    c_ = bytearray(don.mcnk[i])
                    struct.pack_into('<I', c_, 0x34, base.area(i))
                    don.mcnk[i] = bytes(c_)
                    areas_kept[(X, Y)] = areas_kept.get((X, Y), 0) + 1
            full_ = dict(sources)
            sources = {k_: (v_[0], v_[1] if k_ in taken else None) for k_, v_ in sources.items()}
            if mr.get('heal_turtle_seams'):
                hn_ = adtmerge.heal_donor_seams({k_: (sources[k_][1], tk_) for k_, tk_ in taken.items() if sources[k_][1] is not None})
                notes['client_tiles'].append(f"{hn_} edge points where Turtle's own tiles do not meet: both sides set to the average")
            slog_ = []
            moved, worst = adtmerge.stitch(sources, taken, log=slog_, onto=mr.get('stitch_onto', 'base'))
            notes['client_tiles'].append(f"seams between Turtle and 3.3.5 chunks: {moved} edge points aligned (largest step {worst:.2f} yd"
                                         + (", 3.3.5 side moved)" if mr.get('stitch_onto') == 'donor' else ")"))
            big_ = {}
            for X_, Y_, i_, r_, k_, dv_ in slog_:          # Turtle edge points moved more than 5 yd, per chunk (where to look in game)
                if dv_ > mr.get('seam_report_yd', 5):
                    key_ = (X_, Y_, i_)
                    big_[key_] = max(big_.get(key_, 0), dv_)
            for (X_, Y_, i_), dv_ in sorted(big_.items(), key=lambda kv_: -kv_[1])[:mr.get('seam_report_count', 8)]:
                wx_ = (32 - Y_ - (i_ // 16 + 0.5) / 16) * 533.3333
                wy_ = (32 - X_ - (i_ % 16 + 0.5) / 16) * 533.3333
                notes['client_tiles'].append(f"  seam step {dv_:.1f} yd at {wmap}_{X_}_{Y_} chunk {i_} (world x {wx_:.0f}, y {wy_:.0f}, {TW_AREA.get(sources[(X_, Y_)][1].area(i_), [0] * 12)[0]})")
            for k_ in getattr(adtmerge.stitch, 'base_tiles_edited', set()) if mr.get('stitch_onto') == 'donor' else set():
                if k_ not in taken:              # a 3.3.5 tile whose sea floor was raised at the seam: shipped too
                    taken[k_] = set()
                    sources[k_] = full_[k_]

            def _nb_tile(X_, Y_):              # (base, donor or None, taken chunks) of a neighbouring tile
                if (X_, Y_) in sources:
                    b_, d_ = sources[(X_, Y_)]
                    return b_, d_, taken.get((X_, Y_), set())
                p_ = client335_file(f"World\\Maps\\{wmap}\\{wmap}_{X_}_{Y_}.adt")
                return (adtmerge.Tile(open(p_, 'rb').read()), None, set()) if p_ else None
            for k_ in sorted(ocean_built & set(taken)):
                mn_ = adtmerge.match_tile_edges(sources[k_][0], k_[0], k_[1], taken[k_], _nb_tile)
                if mn_:
                    notes['client_tiles'].append(f"{wmap}_{k_[0]}_{k_[1]}: {mn_} sea-floor edge points matched to the 3.3.5 tiles next to it")
            if mr.get('match_stock_edges'):
                # Turtle's taken chunks at the rim of the region meet 3.3.5 tiles Turtle did not change: snap their edge
                # to those tiles (Stonetalon: a 0.9-yd crack against the Barrens' 34_30)
                me_ = 0
                for k_ in sorted(taken):
                    if sources[k_][1] is not None and taken[k_]:
                        me_ += adtmerge.match_stock_edges(sources[k_][1], k_[0], k_[1], taken[k_],
                                                          lambda X_, Y_: None if (X_, Y_) in sources else _nb_tile(X_, Y_))
                notes['client_tiles'].append(f"{me_} edge points at the rim matched to the 3.3.5 tiles next to it")
            for k_ in sorted(ocean_built & set(taken)):
                wdt_tiles.setdefault(wmap, set()).add(k_)
                notes['client_tiles'].append(f"{wmap}_{k_[0]}_{k_[1]}: no 3.3.5 tile - built on open sea (stock tile moved here), added to {wmap}.wdt")
            G_ = adtmerge.TILE

            def donor_owns(px, pz):
                k_ = (int(px // G_), int(pz // G_))
                return k_ in taken and adtmerge.chunk_of(k_, px, pz) in taken[k_]
            if mr.get('ship_replaced_wmo_tiles'):
                # a WMO that crosses tiles is placed by every tile it touches: a region tile with no chunk of its own taken
                # still has to be shipped when Turtle replaced a building whose origin is in a taken chunk, or it keeps
                # drawing the old building next to the new one (Zul'Farrak: TanarisRuins07/09 -> Turtle's 16/17; use with
                # drop_removed_wmos)
                for k_, (b_, d_) in sorted(full_.items()):
                    if k_ in taken:
                        continue
                    bn_ = {(b_.wmos[struct.unpack_from('<I', r_, 0)[0]].lower(), tuple(round(v_) for v_ in struct.unpack_from('<3f', r_, 8)))
                           for r_ in b_.modf}
                    dn_ = {(d_.wmos[struct.unpack_from('<I', r_, 0)[0]].lower(), tuple(round(v_) for v_ in struct.unpack_from('<3f', r_, 8)))
                           for r_ in d_.modf}
                    if any(donor_owns(p_[0], p_[2]) for _, p_ in bn_ ^ dn_):
                        taken[k_] = set()
                        sources[k_] = full_[k_]
                        notes['client_tiles'].append(f"{wmap}_{k_[0]}_{k_[1]}: shipped for a building Turtle replaced (no ground change)")
            for (X, Y), tk in sorted(taken.items()):
                base, don = sources[(X, Y)]
                data = adtmerge.merge(base, don, tk, (X, Y), donor_owns, drop_removed_wmos=mr.get('drop_removed_wmos', False))
                ap_ = f"World\\Maps\\{wmap}\\{wmap}_{X}_{Y}.adt"
                add_tile(ap_, data, m)
                turtle_chunks[ap_] = turtle_chunks.get(ap_, 0) + len(tk)
                if turtle_chunks[ap_] < 128:      # mostly 3.3.5 ground: keep the 3.3.5 minimap image for it
                    keep_335_minimap.add(ap_)
                else:
                    keep_335_minimap.discard(ap_)
                tile_areas |= {don.area(i) for i in tk}
                # Turtle files these chunks need: their textures and the Turtle buildings that stand in them
                for i in tk:
                    c_ = don.mcnk[i]
                    o_ = struct.unpack_from('<I', c_, 0x1C)[0] - 8
                    n_ = struct.unpack_from('<I', c_, o_ + 4)[0] // 16
                    closure_names[0].extend(don.mtex[struct.unpack_from('<I', c_, o_ + 8 + k * 16)[0]] for k in range(n_))
                closure_names[1].extend(don.wmos[struct.unpack_from('<I', r_, 0)[0]] for r_ in don.modf
                                        if donor_owns(*struct.unpack_from('<f', r_, 8), struct.unpack_from('<f', r_, 16)[0]))
                notes['client_tiles'].append(f"{wmap}_{X}_{Y}: merged - {len(tk)} of 256 chunks from Turtle"
                                             + (f" ({areas_kept[(X, Y)]} of them reshaped ground that keeps its 3.3.5 area)" if areas_kept.get((X, Y)) else ''))
        if Z.get('ship_wdt'):
            wp = f"World\\Maps\\{wmap}\\{wmap}.wdt"
            # Turtle's WDT, rewritten in the 3.3.5 layout: MPHD flags cleared (its MCCV/big-alpha bits do not match
            # these texture-less tiles) and the MWMO chunk 3.3.5 expects added
            src_w = open(os.path.join(CFG['tw_client_assets'], *wp.split('\\')), 'rb').read()
            main_ = src_w[src_w.index(b'NIAM') + 8:src_w.index(b'NIAM') + 8 + 32768]
            ch_ = lambda tag, b_: tag[::-1] + struct.pack('<I', len(b_)) + bytes(b_)
            ship_files[wp] = ch_(b'MVER', struct.pack('<I', 18)) + ch_(b'MPHD', bytes(32)) + ch_(b'MAIN', main_) + ch_(b'MWMO', b'')
            new_maps_dir[m] = wmap
        if Z.get('ship_assets'):
            ls_ = Z.get('instance', {}).get('loading_screen')     # a Windows path: os.path.basename would not split it here
            extra = [ls_] + ([ls_[:-4] + 'Wide.blp'] if ls_ and ASSETS.is_turtle(ls_[:-4] + 'Wide.blp') else []) if ls_ else []
            got = ASSETS.closure(zone_tiles, extra, textures=closure_names[0], wmos=closure_names[1] + Z.get('ship_wmos', []))
            # ship_wmos (the Deadmines): a Turtle building shipped whole although no shipped tile places it (a WMO-only map's building Turtle extended)
            ship_files.update(got)
            notes['client_assets'].append(f"{len(got)} Turtle files (buildings, textures) shipped in the client patch")
            for a, b in sorted(ASSETS.changed.items()):
                notes['model_stand_in'].append(f"{a} -> {b}")
        new_areas = sorted(a for a in tile_areas | {int(k) for k in Z.get('area_bits', {})}
                           if a and (a not in AC_AREA or a in AREA_REMAP) and AR(a) not in NEW_AREA and a in TW_AREA)   # NEW_AREA: made by an earlier zone of this build
        new_areas.sort(key=lambda a: (TW_AREA[a][2] != 0, a))           # zones before their subzones
        bits = {int(k): v for k, v in Z.get('area_bits', {}).items()}
        tmpl = {int(k): v for k, v in Z.get('area_templates', {}).items()}
        for a in new_areas:
            tr = TW_AREA[a]
            if a not in bits:
                bits[a] = max(b for b in used_area_bits if b < 4096) + 1
                print(f"  !! area {a} has no exploration bit in the zone file; using {bits[a]} - add it to area_bits")
            b = bits[a]
            assert b < 4096 and used_area_bits.get(b, AR(a)) == AR(a), f'area bit {b} already used by {used_area_bits.get(b)}'
            used_area_bits[b] = AR(a)
            parent = tr[2]
            if parent == 0:
                t_ = AC_AREA[tmpl[a]]                       # e.g. Duskwood for Balor
                flags, mask, amb_mult = t_[4], t_[27], struct.unpack('<f', struct.pack('<I', t_[34]))[0]
            else:
                base = parent if parent in AC_AREA and parent not in AREA_REMAP else tmpl.get(parent)
                assert base, f'area {a}: parent {parent} is new - give it an area_templates entry'
                sib = collections.Counter(r[4] for r in AC_AREA.values() if r[2] == base)
                flags = sib.most_common(1)[0][0] if sib else AC_AREA[base][4]
                mask = AC_AREA[base][27]
                amb_mult = 0.0
            name = _tw_area_str(tr[11])
            music = ZONE_MUSIC_SUB.get(tr[8], tr[8])
            intro = INTRO_SUB.get(tr[9], tr[9])
            if music != tr[8]:
                notes['music_stand_in'].append(f"area {a} {name}: zone music {tr[8]} -> {music}")
            amap = TW_AREA[parent][1] if parent and parent in TW_AREA else tr[1]   # a subzone lies on its zone's map
            if amap != tr[1]:                                                         # (Turtle's Barkskin Hold says map 0)
                notes['new_areas'].append(f"{a}: Turtle gives map {tr[1]}, its zone {parent} is on map {amap} - map {amap} used")
            row = [AR(a), amap, AR(parent), b, flags, tr[5], tr[6], tr[7], music, intro, tr[10]] + [name] * 16 + \
                  [mask, tr[20], 0, 0, 0, 0, -500.0, amb_mult, 0]
            client_areas.append(row)
            NEW_AREA[AR(a)] = row
            area_rows.append(dict(zip(AREA_COLS, row)))
            notes['new_areas'].append(f"{a}{' (written as ' + str(AR(a)) + ': 3.3.5 uses ' + str(a) + ')' if a in AREA_REMAP else ''} {name} ({'zone' if not parent else 'subzone of ' + str(parent)}, map {amap}, exploration bit {b}, level {tr[10]})")
    # ---------------- creatures
    sp = [r for r in q(f"""select c.*, t.name from {TW}.creature c join {TW}.creature_template t on t.entry=c.id
                           where c.map=%s and c.position_x between %s and %s and c.position_y between %s and %s""",
                       m, xs[0] - 50, xs[1] + 50, ys[0] - 50, ys[1] + 50) if in_zone(r['position_x'], r['position_y'])]
    for bx_ in Z.get('spawn_boxes', []):
        # spawn_boxes [[x0, x1, y0, y1]]: the zone's spawns on ground Turtle files under another area (Dun Morogh: the
        # Gnomeregan Reclamation quest mobs north of Gnomeregan stand on chunks Turtle still calls The Great Sea)
        # (optional 5th/6th values: z range - Undercity: the city under Tirisfal's Ruins of Lordaeron)
        sp += [r for r in q(f"select c.*, t.name from {TW}.creature c join {TW}.creature_template t on t.entry=c.id where c.map=%s and "
                            f"c.position_x between %s and %s and c.position_y between %s and %s", m, *bx_[:4])
               if r['guid'] not in {x['guid'] for x in sp} and (len(bx_) < 6 or bx_[4] <= r['position_z'] <= bx_[5])]
    if Z.get('extra_spawns'):            # Turtle NPCs outside the zone that its quests need (e.g. quest givers in Stormwind)
        sp += [r for r in q(f"select c.*, t.name from {TW}.creature c join {TW}.creature_template t on t.entry=c.id where c.guid in ({in_list(Z['extra_spawns'])})")
               if r['guid'] not in {x['guid'] for x in sp}]
    _oth = other_zone_extras(slug, 'extra_spawns')
    for r_ in [r for r in sp if r['guid'] in _oth and r['guid'] not in Z.get('extra_spawns', [])]:
        notes['spawned_elsewhere'].append(f"{r_['name']} (tw guid {r_['guid']}): already spawned by {_oth[r_['guid']]} (its extra_spawns)")
    sp = [r for r in sp if r['guid'] not in _oth or r['guid'] in Z.get('extra_spawns', [])]
    # exclude_boxes [[x0, x1, y0, y1, z0, z1], ...]: spawns inside belong to another zone file although the ground above
    # them is this zone's (Tirisfal: Undercity under the Ruins of Lordaeron, spawned by its own file with spawn_boxes)
    def _in_xbox(r_):
        return any(b_[0] <= r_['position_x'] <= b_[1] and b_[2] <= r_['position_y'] <= b_[3] and b_[4] <= r_['position_z'] <= b_[5]
                   for b_ in Z.get('exclude_boxes', []))
    _nxb = [r for r in sp if _in_xbox(r)]
    if _nxb:
        notes['excluded_in_box'].append(f"{len(_nxb)} creature spawns inside exclude_boxes left out")
        sp = [r for r in sp if not _in_xbox(r)]
    excl = set(Z.get('exclude_creatures', []))
    # spawns Turtle shows only during a seasonal event (game_event_creature, event > 0): this module has no event
    # linking, so they would stand there all year - left out (negative events = despawned during an event: kept)
    ev_c = {r['guid'] for r in q(f"select guid from {TW}.game_event_creature where event > 0")}
    n_ev = len([r for r in sp if r['guid'] in ev_c])
    if n_ev:
        notes['seasonal_spawns'].append(f"{n_ev} creature spawns that Turtle shows only during seasonal events left out")
    sp = [r for r in sp if r['guid'] not in ev_c]
    cspawns = [r for r in sp if r['id'] not in ac_ct and r['id'] not in excl]
    # a zone that is new land in 3.3.5 also needs the spawns of creatures/objects 3.3.5 already has (herbs, critters, spirit healer ...)
    existing = Z.get('spawn_existing_templates', False)
    # a 3.3.5 zone Turtle reworked: the 3.3.5 spawns stay; only in the subzones Turtle built new (spawn_existing_in_subzones)
    # are Turtle's spawns of 3.3.5 templates added (critters, guards, chairs ...), never next to a 3.3.5 spawn of the same template
    ex_subs = set(Z.get('spawn_existing_in_subzones', []))
    ex_skip = set(Z.get('spawn_existing_skip', []))

    def ex_here(r, table):
        if existing:
            return True
        if not ex_subs or subzone(r['position_x'], r['position_y']) not in ex_subs or r['id'] in ex_skip:
            return False
        return not q(f"select 1 from {AC}.{table} where map=%s and {CRE_ID if table == 'creature' else 'id'}=%s and "
                     f"abs(position_x-%s)<5 and abs(position_y-%s)<5 limit 1", m, r['id'], r['position_x'], r['position_y'])
    # an extra spawn of a 3.3.5 template is spawned as asked (Dustwallow's Falgran Hastil: 3.3.5 only summons him for a moment)
    cspawns_ac = [r for r in sp if r['id'] in ac_ct and r['id'] not in excl and (ex_here(r, 'creature') or r['guid'] in Z.get('extra_spawns', []))]
    if Z.get('ship_wmos') and not (terrain_mode == 'turtle' and (Z.get('terrain_tiles') or Z.get('merge_region') or Z.get('area_bits'))):
        # ship_wmos on a zone without Turtle terrain (the Deadmines, a WMO-only map): the building is shipped whole
        got_ = ASSETS.closure([], (), wmos=Z['ship_wmos'])
        ship_files.update(got_)
        notes['client_assets'].append(f"{len(got_)} Turtle files (buildings, textures) shipped in the client patch: "
                                      + ', '.join(Z['ship_wmos']) + ' with its parts')
        for a, b in sorted(ASSETS.changed.items()):
            notes['model_stand_in'].append(f"{a} -> {b}")
    held = set(Z.get('hold_until_terrain_patch', [])) if Z.get('terrain', 'stock') == 'stock' else set()
    if held:
        held_sp = [r for r in cspawns if subzone(r['position_x'], r['position_y']) in held]
        cspawns = [r for r in cspawns if subzone(r['position_x'], r['position_y']) not in held]
        notes['held_until_terrain_patch'].append(f"{len(held_sp)} creature spawns in subzones {sorted(held)} (Turtle rebuilt the terrain there)")
    ids = sorted({r['id'] for r in cspawns} | set(Z.get('extra_creature_templates', [])))
    ctpl = {r['entry']: r for r in q(f"select * from {TW}.creature_template where entry in ({in_list(ids)})")}
    ids = [e for e in ids if ctpl[e]['script_name'] not in EXCL['creature_script_names']]
    new_ids = [e for e in ids if e not in owned['creature']]
    for e in new_ids:
        owned['creature'][e] = slug
    cspawns = [r for r in cspawns if r['id'] in ids] + cspawns_ac
    if cspawns_ac:
        notes['existing_templates'].append(f"{len(cspawns_ac)} creature spawns of {len({r['id'] for r in cspawns_ac})} templates 3.3.5 already has (AzerothCore's template is used)")

    # ---------------- quests
    L = in_list(ids)
    qs = sorted({r['quest'] for r in q(f"select quest from {TW}.creature_questrelation where id in ({L}) union select quest from {TW}.creature_involvedrelation where id in ({L})")})
    qs = [x for x in qs if x not in ac_qt and x not in owned['quest'] and x not in Z.get('exclude_quests', [])]
    # the zone's own quests (quest log category = this zone) whose giver and turn-in live elsewhere, in 3.3.5 or in this build
    tw_names = {}

    def npc_ok(i_):
        if i_ in planned_creatures():
            return True
        if i_ not in tw_names:
            r_ = q(f"select name from {TW}.creature_template where entry=%s", i_)
            tw_names[i_] = r_[0]['name'] if r_ else None
        return i_ in ac_ct and ac_ct[i_] == tw_names[i_]
    _qsub = {(int(qk), int(nk)) for qk, m_ in CFG.get('quest_npc_substitutions', {}).items() if not qk.startswith('_') for nk in m_}

    def qnpc_ok(x_, i_):                 # the NPC is in the build / 3.3.5, or quest_npc_substitutions gives it a 3.3.5 stand-in
        return npc_ok(i_) or (x_, i_) in _qsub
    for r_ in q(f"select entry from {TW}.quest_template where ZoneOrSort=%s", zid):
        x = r_['entry']
        if x in qs or x in ac_qt or x in owned['quest'] or x in Z.get('exclude_quests', []):
            continue
        st_ = [a_['id'] for a_ in q(f"select id from {TW}.creature_questrelation where quest=%s", x)]
        en_ = [a_['id'] for a_ in q(f"select id from {TW}.creature_involvedrelation where quest=%s", x)]
        if st_ and en_ and any(qnpc_ok(x, a_) for a_ in st_) and any(qnpc_ok(x, a_) for a_ in en_):
            qs.append(x)
            notes['zone_quests_elsewhere'].append(f"quest {x}: given and turned in outside the zone ({st_} / {en_})")
    for x in Z.get('extra_quests', []):     # a link of the zone's chains filed under another zone (e.g. a dungeon step)
        if x in qs or x in ac_qt or x in owned['quest']:
            continue
        st_ = [a_['id'] for a_ in q(f"select id from {TW}.creature_questrelation where quest=%s", x)]
        en_ = [a_['id'] for a_ in q(f"select id from {TW}.creature_involvedrelation where quest=%s", x)]
        # an object of this zone's map can start / end it too (a tablet in a dungeon); the object pass spawns it
        gst_ = [a_['id'] for a_ in q(f"select g.id from {TW}.gameobject_questrelation g join {TW}.gameobject s on s.id=g.id "
                                     f"where g.quest=%s and s.map=%s", x, m)]
        gen_ = [a_['id'] for a_ in q(f"select g.id from {TW}.gameobject_involvedrelation g join {TW}.gameobject s on s.id=g.id "
                                     f"where g.quest=%s and s.map=%s", x, m)]
        assert (gst_ or any(qnpc_ok(x, a_) for a_ in st_)) and (gen_ or any(qnpc_ok(x, a_) for a_ in en_)), \
            f'extra quest {x}: its giver {st_ + gst_} or turn-in {en_ + gen_} is neither in this build nor in 3.3.5'
        qs.append(x)
        notes['zone_quests_elsewhere'].append(f"quest {x}: extra quest, given and turned in outside the zone or by an object "
                                              f"({st_ + [f'object {g_}' for g_ in gst_]} / {en_ + [f'object {g_}' for g_ in gen_]})")
    qs = sorted(qs)
    if held:
        spawned_ids = {r['id'] for r in cspawns} | set(ac_ct)
        keep = []
        for x in qs:
            starters = {r['id'] for r in q(f"select id from {TW}.creature_questrelation where quest=%s", x)}
            enders = {r['id'] for r in q(f"select id from {TW}.creature_involvedrelation where quest=%s", x)}
            tq = q(f"select ReqCreatureOrGOId1 a,ReqCreatureOrGOId2 b,ReqCreatureOrGOId3 c,ReqCreatureOrGOId4 d from {TW}.quest_template where entry=%s", x)[0]
            objs = {v for v in tq.values() if v and v > 0}
            objs_ok = all(o in spawned_ids or o in Z.get('extra_creature_templates', []) for o in objs)
            if starters & spawned_ids and (not enders or enders & spawned_ids) and objs_ok:
                keep.append(x)
            else:
                notes['held_until_terrain_patch'].append(f"quest {x} held (its quest giver/turn-in is in a held subzone)")
        qs = keep
    for x in qs:
        owned['quest'][x] = slug
    qtpl = {r['entry']: r for r in q(f"select * from {TW}.quest_template where entry in ({in_list(qs)})")}

    # ---------------- gameobjects
    gs = [r for r in q(f"""select g.*, t.name, t.type from {TW}.gameobject g join {TW}.gameobject_template t on t.entry=g.id
                           where g.map=%s and g.position_x between %s and %s and g.position_y between %s and %s""",
                       m, xs[0] - 50, xs[1] + 50, ys[0] - 50, ys[1] + 50) if in_zone(r['position_x'], r['position_y'])]
    for bx_ in Z.get('spawn_boxes', []):
        gs += [r for r in q(f"select g.*, t.name, t.type from {TW}.gameobject g join {TW}.gameobject_template t on t.entry=g.id where g.map=%s and "
                            f"g.position_x between %s and %s and g.position_y between %s and %s", m, *bx_[:4])
               if r['guid'] not in {x['guid'] for x in gs} and (len(bx_) < 6 or bx_[4] <= r['position_z'] <= bx_[5])]
    if Z.get('extra_gameobject_spawns'):  # Turtle objects outside the zone that its quests need (e.g. a chest in a 3.3.5 dungeon)
        gs += [r for r in q(f"select g.*, t.name, t.type from {TW}.gameobject g join {TW}.gameobject_template t on t.entry=g.id where g.guid in ({in_list(Z['extra_gameobject_spawns'])})")
               if r['guid'] not in {x['guid'] for x in gs}]
    _oth = other_zone_extras(slug, 'extra_gameobject_spawns')
    for r_ in [r for r in gs if r['guid'] in _oth and r['guid'] not in Z.get('extra_gameobject_spawns', [])]:
        notes['spawned_elsewhere'].append(f"{r_['name']} (tw guid {r_['guid']}): already spawned by {_oth[r_['guid']]} (its extra_gameobject_spawns)")
    gs = [r for r in gs if r['guid'] not in _oth or r['guid'] in Z.get('extra_gameobject_spawns', [])]
    _nxg = [r for r in gs if _in_xbox(r)]
    if _nxg:
        notes['excluded_in_box'].append(f"{len(_nxg)} object spawns inside exclude_boxes left out")
        gs = [r for r in gs if not _in_xbox(r)]
    gexcl = set(Z.get('exclude_gameobjects', []))
    # exclude_gameobject_boxes [[x0, x1, y0, y1], ...]: Turtle's objects inside a place 3.3.5 already has in its own form
    # (Dustwallow's Mudsprocket: Turtle's decorations of its copy of the town would double 3.3.5's)
    _gbox = Z.get('exclude_gameobject_boxes', [])
    _nb = [r for r in gs if any(b_[0] <= r['position_x'] <= b_[1] and b_[2] <= r['position_y'] <= b_[3] for b_ in _gbox)]
    if _nb:
        notes['excluded_in_box'].append(f"{len(_nb)} object spawns inside exclude_gameobject_boxes left out")
        gs = [r for r in gs if r not in _nb]
    ev_g = {r['guid'] for r in q(f"select guid from {TW}.game_event_gameobject where event > 0")}
    n_ev = len([r for r in gs if r['guid'] in ev_g])
    if n_ev:
        notes['seasonal_spawns'].append(f"{n_ev} object spawns that Turtle shows only during seasonal events left out")
    gs = [r for r in gs if r['guid'] not in ev_g]
    def same_go(r):          # 3.3.5 has this object id for the same object (names can differ: "Alliance Mailbox" / "Mailbox")
        a, n = (ac_gt.get(r['id']) or '').lower(), (r['name'] or '').lower()
        return r['id'] in ac_gt and (a == n or a in n or n in a or difflib.SequenceMatcher(None, a, n).ratio() >= 0.6)
    other = sorted({(r['id'], r['name'], ac_gt[r['id']]) for r in gs if r['id'] in ac_gt and not same_go(r)})
    for e_, n_, a_ in other:
        notes['object_id_taken'].append(f"{e_} {n_}: 3.3.5 uses this id for '{a_}' - not spawned")
    gspawns = [r for r in gs if r['id'] not in ac_gt and r['id'] not in gexcl]
    gspawns_ac = [r for r in gs if r['id'] in ac_gt and r['id'] not in gexcl and same_go(r)
                  and (ex_here(r, 'gameobject') or r['guid'] in Z.get('extra_gameobject_spawns', []))]
    if held:
        n0 = len(gspawns)
        gspawns = [r for r in gspawns if subzone(r['position_x'], r['position_y']) not in held]
        notes['held_until_terrain_patch'].append(f"{n0 - len(gspawns)} gameobject spawns in held subzones")
    gids = sorted({r['id'] for r in gspawns})
    gtpl = {r['entry']: r for r in q(f"select * from {TW}.gameobject_template where entry in ({in_list(gids)})")}

    out = Sql()
    rb = Sql()
    rows = collections.defaultdict(list)
    rows['areatable_dbc'] = area_rows

    # ---------- creature templates
    equip = {}
    for e in new_ids:
        t = ctpl[e]
        lv = (t['level_min'] + t['level_max']) // 2
        b = cls.get((lv, t['unit_class'] or 1)) or cls.get((lv, 1))
        hp = (t['health_min'] + t['health_max']) / 2
        mana = (t['mana_min'] + t['mana_max']) / 2
        atk = (t['base_attack_time'] or 2000) / 1000.0
        tw_dmg = ((t['dmg_min'] + t['dmg_max']) / 2 + (t['attack_power'] or 0) / 14.0) * (t['dmg_multiplier'] or 1)
        ac_dmg = (b['damage_base'] * 1.25 + b['attackpower'] / 14.0) * atk
        npcflag = conv_npcflag(t['npc_flags'])
        trainer_rows = list(q(f"select * from {TW}.npc_trainer where entry=%s", e))
        if t['trainer_id']:
            trainer_rows += list(q(f"select * from {TW}.npc_trainer_template where entry=%s", t['trainer_id']))
        if trainer_rows and not t['npc_flags'] & 16:
            # Turtle keeps npc_trainer rows on creatures that are not trainers (hunter NPCs and their pets, tamable beasts):
            # without the trainer flag the client never offers them, so they are not trainers here either
            notes['trainer'].append(f"{e} {t['name']}: Turtle trainer rows but no trainer flag - not a trainer")
            trainer_rows = []
        if trainer_rows or t['trainer_id']:
            npcflag |= 16 | (64 if t['trainer_type'] == 2 else 32 if t['trainer_type'] == 0 else 0)
        lootid = t['loot_id'] or 0
        if lootid and lootid != e and lootid in ac_loot and lootid not in owned['loot']:
            notes['loot'].append(f"{e}: uses vanilla loot table {lootid} - AzerothCore's version of it is kept")
        rows['creature_template'].append(dict(
            entry=e, difficulty_entry_1=0, difficulty_entry_2=0, difficulty_entry_3=0, KillCredit1=0, KillCredit2=0,
            name=t['name'], subname=t['subname'] or None, IconName=None, gossip_menu_id=t['gossip_menu_id'] or 0,
            minlevel=t['level_min'], maxlevel=t['level_max'], exp=0, faction=FTMAP(t['faction']), npcflag=npcflag,
            speed_walk=t['speed_walk'] or 1, speed_run=t['speed_run'] or 1.14286, speed_swim=1, speed_flight=1,
            detection_range=20, rank=t['rank'], dmgschool=t['dmg_school'],
            DamageModifier=round(tw_dmg / ac_dmg, 3) if ac_dmg and tw_dmg else 1,
            BaseAttackTime=t['base_attack_time'] or 2000, RangeAttackTime=t['ranged_attack_time'] or 2000,
            BaseVariance=1, RangeVariance=1, unit_class=t['unit_class'] or 1,
            unit_flags=t['unit_flags'] & 0x3FFFFFFF, unit_flags2=2048, dynamicflags=0,
            family=t['beast_family'], type=t['type'], type_flags=0,
            lootid=lootid, pickpocketloot=t['pickpocket_loot_id'] or 0, skinloot=t['skinning_loot_id'] or 0,
            PetSpellDataId=0, VehicleId=0, mingold=t['gold_min'], maxgold=t['gold_max'], AIName='',
            MovementType=t['movement_type'] or 0, HoverHeight=1,
            HealthModifier=round(hp / b['basehp0'], 3) if hp and b['basehp0'] else 1,
            ManaModifier=round(mana / b['basemana'], 3) if mana and b['basemana'] else 1,
            ArmorModifier=round(t['armor'] / b['basearmor'], 3) if t['armor'] and b['basearmor'] else 1,
            ExperienceModifier=1, RacialLeader=0, movementId=0, RegenHealth=1, CreatureImmunitiesId=0,
            flags_extra=t['flags_extra'] & 0x2, ScriptName='', VerifiedBuild=0))
        idx = 0
        for k in ('display_id1', 'display_id2', 'display_id3', 'display_id4'):
            d = t[k]
            if not d:
                continue
            nd, st = disp.creature(d)
            if str(e) in Z.get('force_display', {}):
                nd, st = Z['force_display'][str(e)], 'forced'
            if nd is None:
                nd = 11686
                notes['display_missing'].append(f"{e} {t['name']}: display {d} has no 3.3.5 equivalent - invisible placeholder")
            elif st == 'substitute':
                notes['display_stand_in'].append(f"{e} {t['name']}: Turtle display {d} -> stand-in {nd}")
            rows['creature_template_model'].append(dict(CreatureID=e, Idx=idx, CreatureDisplayID=nd, DisplayScale=t['scale'] or 1, Probability=1, VerifiedBuild=0))
            idx += 1
        for school, col in enumerate(('holy_res', 'fire_res', 'nature_res', 'frost_res', 'shadow_res', 'arcane_res'), start=1):
            if t[col]:
                rows['creature_template_resistance'].append(dict(CreatureID=e, School=school, Resistance=t[col], VerifiedBuild=0))
        ih = t['inhabit_type'] or 3
        rows['creature_template_movement'].append(dict(CreatureId=e, Ground=1 if ih & 1 else 0, Swim=1 if ih & 2 else 0, Flight=1 if ih & 4 else 0, Rooted=0, Chase=0, Random=0, InteractionPauseTimer=None))
        if t['auras']:
            auras = ' '.join(str(spell_conv(int(a))[0]) for a in t['auras'].split() if spell_conv(int(a))[0])
            if auras:
                rows['creature_template_addon'].append(dict(entry=e, path_id=0, mount=0, bytes1=0, bytes2=1, emote=0, visibilityDistanceType=0, auras=auras))
        if t['equipment_id']:
            eq = q(f"select * from {TW}.creature_equip_template where entry=%s", t['equipment_id'])
            if eq:
                its = [I(x) if ac_item(x) else 0 for x in (eq[0]['equipentry1'], eq[0]['equipentry2'], eq[0]['equipentry3'])]
                if any(its):
                    rows['creature_equip_template'].append(dict(CreatureID=e, ID=1, ItemID1=its[0], ItemID2=its[1], ItemID3=its[2], VerifiedBuild=0))
                    equip[e] = 1
        # trainer
        stock_tid = None
        if trainer_rows and t['trainer_type'] == 0 and t['trainer_class']:
            # a class trainer teaches 3.3.5's own list for its class (Turtle's lists stop at the vanilla ranks, and many of
            # their spells are not 3.3.5's): the most used stock trainer list of that class
            st_ = q(f"select t.Id from {AC}.trainer t join {AC}.creature_default_trainer d on d.TrainerId=t.Id "
                    f"where t.Type=0 and t.Requirement=%s group by t.Id order by count(*) desc, t.Id limit 1", t['trainer_class'])
            if st_:
                stock_tid = st_[0]['Id']
                rows['creature_default_trainer'].append(dict(CreatureId=e, TrainerId=stock_tid))
                notes['trainer'].append(f"{e} {t['name']}: class trainer (class {t['trainer_class']}) - uses 3.3.5's trainer list {stock_tid}")
        if trainer_rows and stock_tid is None:
            tid = e
            rows['trainer'].append(dict(Id=tid, Type=t['trainer_type'], Requirement=t['trainer_class'] if t['trainer_type'] == 0 else (t['trainer_race'] if t['trainer_type'] == 1 else 0), Greeting='', VerifiedBuild=0))
            rows['creature_default_trainer'].append(dict(CreatureId=e, TrainerId=tid))
            for r in trainer_rows:
                learn = learned_spell(r['spell']) or r['spell']
                if learn in TALENT_SPELLS:
                    notes['trainer'].append(f"{e}: trainer spell {r['spell']} -> {learn} is a talent in 3.3.5 (learned from the talent tree), skipped")
                    continue
                if not spell_conv(learn)[0] or spell_conv(learn)[0] != learn:
                    notes['trainer'].append(f"{e}: trainer spell {r['spell']} -> {learn} not in 3.3.5, skipped")
                    continue
                base = q(f"select * from {AC}.trainer_spell where SpellId=%s limit 1", learn)
                base = base[0] if base else None
                rows['trainer_spell'].append(dict(TrainerId=tid, SpellId=learn, MoneyCost=r['spellcost'],
                                                  ReqSkillLine=base['ReqSkillLine'] if base else r['reqskill'],
                                                  ReqSkillRank=base['ReqSkillRank'] if base else r['reqskillvalue'],
                                                  ReqAbility1=base['ReqAbility1'] if base else 0, ReqAbility2=0, ReqAbility3=0,
                                                  ReqLevel=r['reqlevel'], VerifiedBuild=0))
        # spell list -> SmartAI
        n_id = 0
        if t['spell_list_id']:
            sl = q(f"select * from {TW}.creature_spells where entry=%s", t['spell_list_id'])
            TGT = {0: 2, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 1}
            for slr in sl[:1]:
                for n in range(1, 9):
                    s = slr[f'spellId_{n}']
                    if not s:
                        continue
                    ns, why = spell_conv(s)
                    if why:
                        notes['spell_sub' if ns else 'spell_dropped'].append(f"{t['name']}: {why}")
                    if not ns:
                        continue
                    s = ns
                    rows['smart_scripts'].append(dict(
                        entryorguid=e, source_type=0, id=n_id, link=0, event_type=0, event_phase_mask=0,
                        event_chance=max(1, min(100, slr[f'probability_{n}'] or 100)), event_flags=0,
                        event_param1=slr[f'delayInitialMin_{n}'] * 1000, event_param2=slr[f'delayInitialMax_{n}'] * 1000,
                        event_param3=slr[f'delayRepeatMin_{n}'] * 1000, event_param4=slr[f'delayRepeatMax_{n}'] * 1000,
                        event_param5=0, event_param6=0, action_type=11, action_param1=s, action_param2=0, action_param3=0,
                        action_param4=0, action_param5=0, action_param6=0, target_type=TGT.get(slr[f'castTarget_{n}'], 2),
                        target_param1=0, target_param2=0, target_param3=0, target_param4=0, target_x=0, target_y=0, target_z=0, target_o=0,
                        comment=f"{t['name']} - In Combat - Cast {s} (Turtle spell list {t['spell_list_id']})"))
                    n_id += 1
            if n_id:
                rows['creature_template'][-1]['AIName'] = 'SmartAI'
        if t['ai_name'] == 'EventAI':
            ev_rows, ev_notes, ev_texts = eventai_to_smart(e, t['name'], n_id if t['spell_list_id'] else 0)
            rows['smart_scripts'] += ev_rows
            rows['creature_text'] += ev_texts
            for x in ev_notes:
                notes['eventai'].append(f"{e} {t['name']}: {x}")
            if ev_rows:
                rows['creature_template'][-1]['AIName'] = 'SmartAI'
        if t['script_name']:
            notes['cpp_script'].append(f"{e} {t['name']}: Turtle C++ script '{t['script_name']}' (see manual/{slug}.sql)")

    # ---------- spawns
    terrain = Z.get('terrain', 'stock')
    guid = gbase
    gmap = guid_maps.setdefault(slug, {'creature': {}, 'gameobject': {}})
    for s in sorted(cspawns, key=lambda r: (r['id'], r['guid'])):
        guid += 1
        x, y, z = s['position_x'], s['position_y'], s['position_z']
        mt, path = s['movement_type'], 0
        if terrain == 'stock':
            htw, hac = twmaps.height(s['map'], x, y), acmaps.height(s['map'], x, y)
            sub = subzone(x, y)
            if htw is not None and hac is not None:
                above = z - htw
                if abs(htw - hac) > 1.5 or (sub in custom_sub and above > 2.5):
                    nz = hac + (above if 0 <= above <= 2.5 else 0.05)
                    notes['moved_to_stock_ground'].append(f"{s['name']} (tw {s['guid']}): z {z:.1f} -> {nz:.1f}" + (" (was on a Turtle-only structure)" if above > 2.5 else " (Turtle reshaped the terrain here)"))
                    z = nz
                    if mt == 2:
                        mt = 1
        if mt == 2:
            pts = q(f"select * from {TW}.creature_movement where id=%s order by point", s['guid'])
            if pts:
                path = guid * 10
                for p in pts:
                    rows['waypoint_data'].append(dict(id=path, point=p['point'], position_x=p['position_x'], position_y=p['position_y'],
                                                      position_z=p['position_z'], orientation=p['orientation'] if p['orientation'] < 100 else None,
                                                      velocity=0, delay=p['waittime'], smoothTransition=0, move_type=0, action=0, action_chance=100, wpguid=0))
            else:
                mt = 0
        gmap['creature'][s['guid']] = guid
        rows['creature'].append(dict(guid=guid, id1=s['id'], map=s['map'], zoneId=0, areaId=0, spawnMask=1, phaseMask=1,
                                     equipment_id=equip.get(s['id'], 0) if s['id'] in equip else (1 if s['id'] not in CREMAP and q(f"select 1 from {AC}.creature_equip_template where CreatureID=%s", s['id']) else 0),
                                     position_x=x, position_y=y, position_z=z, orientation=s['orientation'],
                                     spawntimesecs=s['spawntimesecsmin'], wander_distance=(s['wander_distance'] or 5) if mt == 1 else 0,
                                     currentwaypoint=0, curhealth=1, curmana=0, MovementType=mt, npcflag=0, unit_flags=0, dynamicflags=0,
                                     ScriptName='', VerifiedBuild=0, CreateObject=0, Comment=f"turtle {slug}: {s['name']} (tw guid {s['guid']})"))
        ad = q(f"select * from {TW}.creature_addon where guid=%s", s['guid'])
        if ad or path:
            a = ad[0] if ad else {}
            auras = ' '.join(str(spell_conv(int(x_))[0]) for x_ in (a.get('auras') or '').split() if spell_conv(int(x_))[0]) or None
            rows['creature_addon'].append(dict(guid=guid, path_id=path, mount=max(0, a.get('mount_display_id') or 0), bytes1=a.get('stand_state') or 0,
                                               bytes2=a.get('sheath_state') if a.get('sheath_state') is not None else 1, emote=a.get('emote_state') or 0,
                                               visibilityDistanceType=0, auras=auras))
    assert guid - gbase < IDS['guid_per_zone'], 'zone GUID range overflow'

    # ---------- gossip
    menus = sorted({r['gossip_menu_id'] for r in rows['creature_template'] if r['gossip_menu_id']})
    # quest-giver objects (type 2) open the gossip menu in data3
    go_menu = {e: gtpl[e]['data3'] for e in gids if gtpl[e]['type'] == 2 and gtpl[e]['data3'] and e not in owned['gameobject']
               and q(f"select 1 from {TW}.gossip_menu where entry=%s union select 1 from {TW}.gossip_menu_option where menu_id=%s",
                     gtpl[e]['data3'], gtpl[e]['data3'])}
    menus = sorted(set(menus) | set(go_menu.values()))
    go_smart = set()
    remap = {}

    def stock_menu_same(mn_):
        """Turtle's menu is 3.3.5's menu of the same id (stock innkeeper menu 342): same texts, and every option Turtle shows
        without a condition is in 3.3.5's menu too -> the NPC uses 3.3.5's menu (with 3.3.5's own holiday conditions)"""
        if mn_ not in ac_menu:
            return False
        tt_ = {r['text_id'] for r in q(f"select text_id from {TW}.gossip_menu where entry=%s", mn_)}
        at_ = {r['TextID'] for r in q(f"select TextID from {AC}.gossip_menu where MenuID=%s", mn_)}
        ao_ = [(r['OptionText'] or '').lower() for r in q(f"select OptionText from {AC}.gossip_menu_option where MenuID=%s", mn_)]
        for o_ in q(f"select option_text, condition_id from {TW}.gossip_menu_option where menu_id=%s", mn_):
            if o_['condition_id']:
                continue
            t_ = fix_text(o_['option_text'] or '').lower()
            if not any(difflib.SequenceMatcher(None, t_, x_).ratio() >= 0.8 for x_ in ao_):
                return False
        return tt_ == at_
    stock_menus = {mn for mn in menus if stock_menu_same(mn)}
    for mn in sorted(stock_menus):
        notes['gossip'].append(f"menu {mn}: same as 3.3.5's menu {mn} - 3.3.5's menu is used")
        owned['menu'].setdefault(mn, slug)
    for mn in menus:
        remap[mn] = mn if mn in stock_menus else (mn + IDS['text_offset'] if mn in ac_menu else mn)
    menus = [mn for mn in menus if mn not in stock_menus]
    for r in rows['creature_template']:
        if r['gossip_menu_id']:
            r['gossip_menu_id'] = remap[r['gossip_menu_id']]
    queue = list(menus)
    seen = set()
    menu_parent = {}              # sub-menu -> menus whose options open it (a sub-menu's scripts run on its root's owner)

    def menu_owners(nm_, depth=0):
        c_ = [r['entry'] for r in rows['creature_template'] if r['gossip_menu_id'] == nm_]
        g_ = [e_ for e_, m_ in go_menu.items() if remap.get(m_, m_) == nm_]
        if depth < 5:
            for p_ in menu_parent.get(nm_, ()):
                c2, g2 = menu_owners(p_, depth + 1)
                c_ += [x for x in c2 if x not in c_]
                g_ += [x for x in g2 if x not in g_]
        return c_, g_
    while queue:
        mn = queue.pop(0)
        if mn in seen or mn in owned['menu']:
            continue
        seen.add(mn); owned['menu'][mn] = slug
        nm = remap.setdefault(mn, mn + IDS['text_offset'] if mn in ac_menu else mn)
        for g in q(f"select * from {TW}.gossip_menu where entry=%s", mn):
            tid = g['text_id']
            ntid = tid + IDS['text_offset'] if tid in ac_text else tid
            if g['condition_id']:
                cr = condition_rows(14, nm, ntid, g['condition_id'], f"Turtle condition {g['condition_id']}")
                if cr is None:
                    notes['gossip'].append(f"menu {mn}: text {tid} has Turtle condition {g['condition_id']} (not ported - always shown)")
                else:
                    rows['conditions'] += cr
            if tid not in owned['text']:
                owned['text'][tid] = slug
                nt = q(f"select * from {TW}.npc_text where ID=%s", tid)
                if nt:
                    nt = nt[0]
                    row = dict(ID=ntid)
                    for i in range(8):
                        bid = nt[f'BroadcastTextID{i}']
                        bt = q(f"select * from {TW}.broadcast_text where entry=%s", bid)[0] if bid else None
                        row[f'text{i}_0'] = bt['male_text'] if bt else None
                        row[f'text{i}_1'] = bt['female_text'] if bt else None
                        row[f'BroadcastTextID{i}'] = 0
                        row[f'lang{i}'] = bt['language_id'] if bt else 0
                        row[f'Probability{i}'] = nt[f'Probability{i}'] if bt else 0
                        for j in range(6):
                            row[f'em{i}_{j}'] = 0
                        if bt:
                            row[f'em{i}_1'] = bt['emote_id1'] or 0
                    row['VerifiedBuild'] = 0
                    rows['npc_text'].append(row)
            if not q(f"select 1 from {TW}.npc_text where ID=%s", tid):
                if tid in ac_text:
                    ntid = tid                     # only AzerothCore has it: use theirs
                else:
                    notes['gossip'].append(f"menu {mn}: text {tid} does not exist in the Turtle DB - NPC shows the default greeting")
                    continue
            rows['gossip_menu'].append(dict(MenuID=nm, TextID=ntid))
        def _cond_ok(cid_):
            """a Turtle condition we can port, and not one about a quest this zone leaves out (a condition on a quest that
            does not exist is dropped by the core, which would show the option to everyone)"""
            cr_ = condition_rows(15, nm, 0, cid_, '')
            return cr_ is not None and not any(
                r_['ConditionTypeOrReference'] in (8, 9, 14, 28, 47) and r_['ConditionValue1'] in Z.get('exclude_quests', [])
                and r_['ConditionValue1'] not in ac_qt and r_['ConditionValue1'] not in owned['quest'] for r_ in cr_)
        for o in q(f"select * from {TW}.gossip_menu_option where menu_id=%s", mn):
            if o['condition_id'] and o['action_script_id'] and o['action_menu_id'] <= 0 and \
                    not _cond_ok(o['condition_id']) and \
                    not all(x['command'] in (0, 7, 8, 10, 17) for x in q(f"select command from {TW}.gossip_scripts where id=%s", o['action_script_id'])):
                # an option that only runs a Turtle script we cannot port, behind a condition we cannot port (e.g. the
                # Hallow's End "Trick or Treat!" on innkeepers): it would always show and do nothing - left out
                notes['gossip'].append(f"menu {mn} option {o['id']}: Turtle condition {o['condition_id']} and script {o['action_script_id']} not ported - option left out")
                continue
            if o['condition_id']:
                cr = condition_rows(15, nm, o['id'], o['condition_id'], f"Turtle condition {o['condition_id']}")
                if cr is None:
                    notes['gossip'].append(f"menu {mn} option {o['id']}: Turtle condition {o['condition_id']} not ported - option always shown")
                else:
                    rows['conditions'] += cr
            if o['action_script_id']:
                # simple Turtle gossip scripts become SmartAI on the NPC / object that owns the menu:
                #   SCRIPT_COMMAND_KILL_CREDIT (8)          -> quest credit for the player
                #   SCRIPT_COMMAND_TEMP_SUMMON_CREATURE (10) -> summon at the script's position (attacks the player when told to)
                #   SCRIPT_COMMAND_CREATE_ITEM (17)          -> item for the player
                #   SCRIPT_COMMAND_QUEST_EXPLORED (7)        -> the player's exploration/event quest is complete
                sc = q(f"select * from {TW}.gossip_scripts where id=%s order by delay, priority", o['action_script_id'])
                c_own, g_own = menu_owners(nm)
                if sc and (c_own or g_own) and all(x['command'] in (0, 7, 8, 10, 17) for x in sc) and any(x['command'] != 0 for x in sc):
                    acts = []
                    for x in sc:
                        if x['command'] == 0:
                            # a line of text around the action: shown by no one here (objects cannot speak through SmartAI)
                            notes['gossip_text_dropped'].append(f"menu {mn} option {o['id']}: Turtle script {o['action_script_id']} text line not shown")
                        elif x['command'] == 7:
                            acts.append((15, [x['datalong'], 0, 0, 0], 7, (0, 0, 0, 0), f"Quest {x['datalong']} complete (event)"))
                        elif x['command'] == 8:
                            acts.append((33, [x['datalong'], 0, 0, 0], 7, (0, 0, 0, 0), f"Quest credit {x['datalong']}"))
                        elif x['command'] == 17:
                            if not ac_item(x['datalong']):
                                items_needed.add(x['datalong'])
                            acts.append((56, [I(x['datalong']), max(1, x['datalong2']), 0, 0], 7, (0, 0, 0, 0), f"Give item {I(x['datalong'])}"))
                        else:
                            dur = x['datalong2'] or 0
                            stype = x['dataint4'] or (1 if dur else 8)
                            acts.append((12, [x['datalong'], stype, dur, 1 if x['dataint3'] == 6 else 0], 8,
                                         (x['x'], x['y'], x['z'], x['o']), f"Summon {x['datalong']}"))
                            if x['dataint'] & 0x0C and x['datalong4']:
                                # Turtle only summons when none is near: hide the option while one is alive within that range
                                groups = sorted({r_['ElseGroup'] for r_ in rows['conditions']
                                                 if r_['SourceTypeOrReferenceId'] == 15 and r_['SourceGroup'] == nm and r_['SourceEntry'] == o['id']}) or [0]
                                for eg in groups:
                                    rows['conditions'].append(dict(
                                        SourceTypeOrReferenceId=15, SourceGroup=nm, SourceEntry=o['id'], SourceId=0, ElseGroup=eg,
                                        ConditionTypeOrReference=29, ConditionTarget=0, ConditionValue1=x['datalong'],
                                        ConditionValue2=x['datalong4'], ConditionValue3=0, NegativeCondition=1, ErrorType=0, ErrorTextId=0,
                                        ScriptName='', Comment=f"only one {x['datalong']} at a time (Turtle unique summon)"))
                    for src, owners in ((0, c_own), (1, g_own)):
                        for e_ in owners:
                            nxt = 90 + sum(1 for r in rows['smart_scripts'] if r['entryorguid'] == e_ and r['source_type'] == src and r['id'] >= 90)
                            for at, ap, tt, xyz, cm in acts + [(72, [0, 0, 0, 0], 7, (0, 0, 0, 0), 'Close gossip')]:
                                rows['smart_scripts'].append(dict(
                                    entryorguid=e_, source_type=src, id=nxt, link=0, event_type=62, event_phase_mask=0, event_chance=100,
                                    event_flags=0, event_param1=nm, event_param2=o['id'], event_param3=0, event_param4=0, event_param5=0,
                                    event_param6=0, action_type=at, action_param1=ap[0], action_param2=ap[1], action_param3=ap[2],
                                    action_param4=ap[3], action_param5=0, action_param6=0, target_type=tt, target_param1=0, target_param2=0,
                                    target_param3=0, target_param4=0, target_x=xyz[0], target_y=xyz[1], target_z=xyz[2], target_o=xyz[3],
                                    comment=f"Gossip option {o['id']} selected - {cm} (Turtle gossip script {o['action_script_id']})"))
                                nxt += 1
                            if src == 0:
                                for r in rows['creature_template']:
                                    if r['entry'] == e_:
                                        r['AIName'] = 'SmartAI'
                            else:
                                go_smart.add(e_)
                    notes['gossip'].append(f"menu {mn} option {o['id']}: Turtle gossip script {o['action_script_id']} -> SmartAI "
                                           + ', '.join(a_[4] for a_ in acts)
                                           + (' (Turtle delays of up to %ds dropped)' % max(x['delay'] for x in sc) if any(x['delay'] for x in sc) else ''))
                else:
                    notes['gossip'].append(f"menu {mn} option {o['id']}: runs Turtle gossip script {o['action_script_id']} "
                                           f"(commands {sorted({x['command'] for x in sc})}; not ported)")
            txt = o['option_text']
            if o['option_broadcast_text']:
                bt = q(f"select * from {TW}.broadcast_text where entry=%s", o['option_broadcast_text'])
                txt = bt[0]['male_text'] if bt else txt
            am = o['action_menu_id']
            if am > 0:
                queue.append(am)
                menu_parent.setdefault(am, set()).add(nm)
                remap.setdefault(am, am + IDS['text_offset'] if am in ac_menu else am)
            rows['gossip_menu_option'].append(dict(MenuID=nm, OptionID=o['id'], OptionIcon=o['option_icon'], OptionText=txt, OptionBroadcastTextID=0,
                                                   OptionType=o['option_id'], OptionNpcFlag=conv_npcflag(o['npc_option_npcflag']),
                                                   ActionMenuID=remap.get(am, am) if am > 0 else 0, ActionPoiID=0, BoxCoded=o['box_coded'],
                                                   BoxMoney=o['box_money'], BoxText=o['box_text'] or None, BoxBroadcastTextID=0, VerifiedBuild=0))

    used_menus = {r['MenuID'] for r in rows['gossip_menu']} | {r['MenuID'] for r in rows['gossip_menu_option']}
    for r in rows['creature_template']:
        if r['gossip_menu_id'] and r['gossip_menu_id'] not in used_menus and r['gossip_menu_id'] not in ac_menu:
            r['gossip_menu_id'] = 0                 # menu had nothing left (its text is missing in the Turtle DB)

    # ---------- vendors
    vend = list(q(f"select * from {TW}.npc_vendor where entry in ({in_list(new_ids)}) order by entry, slot"))
    for t in (ctpl[e] for e in new_ids):
        if t['vendor_id']:
            for r in q(f"select * from {TW}.npc_vendor_template where entry=%s order by slot", t['vendor_id']):
                r = dict(r); r['entry'] = t['entry']; vend.append(r)
    seen_v = set()
    for r in vend:
        if (r['entry'], r['item']) in seen_v:
            continue
        seen_v.add((r['entry'], r['item']))
        it = r['item']
        if not ac_item(it):
            items_needed.add(it)
        rows['npc_vendor'].append(dict(entry=r['entry'], slot=r['slot'], item=I(it), maxcount=r['maxcount'], incrtime=r['incrtime'], ExtendedCost=0, VerifiedBuild=0))

    # ---------- creature loot
    loot_ids = []
    for r in rows['creature_template']:
        lid = r['lootid']
        if not lid or lid in owned['loot'] or (lid != r['entry'] and lid in ac_loot):
            continue
        lr_ = q(f"select * from {TW}.creature_loot_template where entry=%s", lid)
        if not lr_:                        # Turtle points at a loot table it never filled: the core would log it missing
            notes['loot'].append(f"{r['entry']}: lootid {lid} has no rows in Turtle's creature_loot_template - cleared")
            r['lootid'] = 0
            continue
        owned['loot'][lid] = slug
        loot_ids.append(lid)
        for l in lr_:
            rows['creature_loot_template'].append(loot_row(lid, l))
    # skinning and pickpocket loot: Turtle ids 3.3.5 also has keep the 3.3.5 table (same vanilla creatures); others are exported.
    # An id with no Turtle rows at all is cleared, so the server never sees a creature pointing at a missing table.
    extra_loot = {'skinning_loot_template': [], 'pickpocketing_loot_template': []}
    for col_, tab_, own_, ac_set in (('skinloot', 'skinning_loot_template', 'skin', ac_skin), ('pickpocketloot', 'pickpocketing_loot_template', 'pick', ac_pick)):
        for r in rows['creature_template']:
            lid = r[col_]
            if not lid or lid in ac_set or lid in owned[own_]:
                continue
            lr = q(f"select * from {TW}.{tab_} where entry=%s", lid)
            if not lr:
                notes['loot'].append(f"{r['entry']}: {col_} {lid} has no rows in Turtle's {tab_} - cleared")
                r[col_] = 0
                continue
            owned[own_][lid] = slug
            extra_loot[tab_].append(lid)
            for l in lr:
                rows[tab_].append(loot_row(lid, l))
    rows['creature_onkill_reputation'] = [dict(r, RewOnKillRepFaction1=FMAP(r['RewOnKillRepFaction1']), RewOnKillRepFaction2=FMAP(r['RewOnKillRepFaction2']))
                                          for r in q(f"select * from {TW}.creature_onkill_reputation where creature_id in ({in_list(new_ids)})")]

    # ---------- quests started by an item that drops here (boss drops); kept when the turn-in NPC exists in this build or in 3.3.5
    if loot_ids:
        for r_ in q(f"""select distinct i.start_quest qid, i.name from {TW}.creature_loot_template l join {TW}.item_template i on i.entry=l.item
                        where l.entry in ({in_list(loot_ids)}) and i.start_quest>0"""):
            x = r_['qid']
            if x in qs or x in ac_qt or x in owned['quest'] or x in Z.get('exclude_quests', []):
                continue
            enders = q(f"select r.id, t.name from {TW}.creature_involvedrelation r join {TW}.creature_template t on t.entry=r.id where r.quest=%s", x)
            ok = [e for e in enders if e['id'] in ids or ac_ct.get(e['id']) == e['name'] or e['id'] in planned_creatures()]
            tq = q(f"select * from {TW}.quest_template where entry=%s", x)
            if ok and tq:
                qs.append(x)
                owned['quest'][x] = slug
                qtpl[x] = tq[0]
                notes['item_quests'].append(f"quest {x} {tq[0]['Title']}: started by {r_['name']}, turned in to {ok[0]['name']}")
            else:
                notes['item_quests'].append(f"quest {x} (started by {r_['name']}) left out: its turn-in NPC "
                                            f"{', '.join(e['name'] for e in enders) or '(none)'} is not in this build")

    # ---------- quests
    for e in qs:
        t = qtpl[e]
        for k in ['ReqItemId1', 'ReqItemId2', 'ReqItemId3', 'ReqItemId4', 'ReqSourceId1', 'ReqSourceId2', 'ReqSourceId3', 'ReqSourceId4',
                  'RewChoiceItemId1', 'RewChoiceItemId2', 'RewChoiceItemId3', 'RewChoiceItemId4', 'RewChoiceItemId5', 'RewChoiceItemId6',
                  'RewItemId1', 'RewItemId2', 'RewItemId3', 'RewItemId4', 'SrcItemId']:
            if t[k] and not ac_item(t[k]):
                items_needed.add(t[k])
                quest_items.add(t[k])
        _rsp = {}
        for k_ in ('RewSpell', 'RewSpellCast'):         # a Turtle spell id is only kept when 3.3.5 has the same spell
            _rsp[k_], n_ = spell_conv(t[k_])
            if n_:
                notes['quest_spell'].append(f"quest {e} {t['Title']}: {k_} {n_}")
        r = dict(ID=e, QuestType=2, QuestLevel=t['QuestLevel'], MinLevel=t['MinLevel'], QuestSortID=AR(t['ZoneOrSort']), QuestInfoID=t['Type'],
                 SuggestedGroupNum=t['SuggestedPlayers'], RequiredFactionId1=FMAP(t['RepObjectiveFaction']), RequiredFactionId2=0,
                 RequiredFactionValue1=t['RepObjectiveValue'], RequiredFactionValue2=0, RewardNextQuest=t['NextQuestInChain'],
                 RewardXPDifficulty=xp_difficulty(t['QuestLevel'], t['RewXP']) if t['RewXP'] else 0, RewardMoney=t['RewOrReqMoney'],
                 RewardMoneyDifficulty=0, RewardDisplaySpell=_rsp['RewSpell'] or 0, RewardSpell=_rsp['RewSpellCast'] or 0, RewardHonor=0, RewardKillHonor=0,
                 StartItem=I(t['SrcItemId']), Flags=t['QuestFlags'] & 0xFFFF, RequiredPlayerKills=0)
        for n in range(1, 5):
            r[f'RewardItem{n}'] = I(t[f'RewItemId{n}']); r[f'RewardAmount{n}'] = t[f'RewItemCount{n}']
            r[f'ItemDrop{n}'] = I(t[f'ReqSourceId{n}']); r[f'ItemDropQuantity{n}'] = t[f'ReqSourceCount{n}']
        for n in range(1, 7):
            r[f'RewardChoiceItemID{n}'] = I(t[f'RewChoiceItemId{n}']); r[f'RewardChoiceItemQuantity{n}'] = t[f'RewChoiceItemCount{n}']
        r.update(POIContinent=t['PointMapId'], POIx=t['PointX'], POIy=t['PointY'], POIPriority=t['PointOpt'], RewardTitle=0, RewardTalents=0, RewardArenaPoints=0)
        for n in range(1, 6):
            r[f'RewardFactionID{n}'] = FMAP(t[f'RewRepFaction{n}']); r[f'RewardFactionValue{n}'] = 0; r[f'RewardFactionOverride{n}'] = t[f'RewRepValue{n}'] * 100
        r.update(TimeAllowed=t['LimitTime'], AllowableRaces=conv_races(t['RequiredRaces']), LogTitle=t['Title'], LogDescription=t['Objectives'],
                 QuestDescription=t['Details'], AreaDescription=t['EndText'], QuestCompletionLog='')
        for n in range(1, 5):
            r[f'RequiredNpcOrGo{n}'] = t[f'ReqCreatureOrGOId{n}']; r[f'RequiredNpcOrGoCount{n}'] = t[f'ReqCreatureOrGOCount{n}']
        for n in range(1, 7):
            r[f'RequiredItemId{n}'] = I(t[f'ReqItemId{n}']) if n <= 4 else 0
            r[f'RequiredItemCount{n}'] = t[f'ReqItemCount{n}'] if n <= 4 else 0
        r['Unknown0'] = 0
        for n in range(1, 5):
            r[f'ObjectiveText{n}'] = t[f'ObjectiveText{n}'] or ''
        r['VerifiedBuild'] = 0
        rows['quest_template'].append(r)
        rows['quest_template_addon'].append(dict(ID=e, MaxLevel=t['MaxLevel'], AllowableClasses=t['RequiredClasses'], SourceSpellID=t['SrcSpell'],
                                                 PrevQuestID=t['PrevQuestId'], NextQuestID=t['NextQuestId'], ExclusiveGroup=t['ExclusiveGroup'],
                                                 BreadcrumbForQuestId=0, RewardMailTemplateID=0, RewardMailDelay=0, RequiredSkillID=t['RequiredSkill'],
                                                 RequiredSkillPoints=t['RequiredSkillValue'], RequiredMinRepFaction=FMAP(t['RequiredMinRepFaction']),
                                                 RequiredMaxRepFaction=FMAP(t['RequiredMaxRepFaction']), RequiredMinRepValue=t['RequiredMinRepValue'],
                                                 RequiredMaxRepValue=t['RequiredMaxRepValue'], ProvidedItemCount=t['SrcItemCount'], SpecialFlags=t['SpecialFlags'] & 1))
        if t['OfferRewardText']:
            rows['quest_offer_reward'].append(dict(ID=e, Emote1=t['OfferRewardEmote1'], Emote2=t['OfferRewardEmote2'], Emote3=t['OfferRewardEmote3'], Emote4=t['OfferRewardEmote4'],
                                                   EmoteDelay1=t['OfferRewardEmoteDelay1'], EmoteDelay2=t['OfferRewardEmoteDelay2'], EmoteDelay3=t['OfferRewardEmoteDelay3'],
                                                   EmoteDelay4=t['OfferRewardEmoteDelay4'], RewardText=t['OfferRewardText'], VerifiedBuild=0))
        if t['RequestItemsText']:
            rows['quest_request_items'].append(dict(ID=e, EmoteOnComplete=t['CompleteEmote'], EmoteOnIncomplete=t['IncompleteEmote'], CompletionText=t['RequestItemsText'], VerifiedBuild=0))
        if t['StartScript'] or t['CompleteScript']:
            notes['quest_scripts'].append(f"{e} {t['Title']}: Turtle start/complete script {t['StartScript']}/{t['CompleteScript']} (not ported)")
    known = set(ac_ct) | set(owned['creature'])
    for r in q(f"select * from {TW}.creature_questrelation where quest in ({in_list(qs)})"):
        if r['id'] in known:
            rows['creature_queststarter'].append(dict(id=r['id'], quest=r['quest']))
    for r in q(f"select * from {TW}.creature_involvedrelation where quest in ({in_list(qs)})"):
        if r['id'] in known:
            rows['creature_questender'].append(dict(id=r['id'], quest=r['quest']))

    # ---------- gameobjects
    gdisp, pending = {}, []
    new_g = [e for e in gids if e not in owned['gameobject']]
    for e in gids:
        t = gtpl[e]
        nd, st = disp.gameobject(t['displayId'])
        if nd is None and st.startswith('needs-client-patch:'):
            nd, why = go_display(t['displayId'], st.split(':', 1)[1])
            if e in new_g:
                notes['go_display_added' if nd else 'go_no_model'].append(f"{e} {t['name'][:60]}: {why}")
        gtype = t['type']
        lk_field = LOCK_FIELD.get(gtype)
        lk_new = None
        lock_out = False
        if nd is not None and lk_field is not None and t[f'data{lk_field}']:
            lk_new = lock_map(t[f'data{lk_field}'])
            if lk_new is None:
                if e in new_g:
                    notes['turtle_only_lock'].append(f"{e} {t['name'][:60]}: lock {t[f'data{lk_field}']} is a Turtle-only lock type (e.g. Survival gathering) - left out")
                nd = None
                lock_out = True
        gdisp[e] = nd
        if nd is None:
            if e in new_g and not lock_out:
                pending.append(dict(entry=e, name=t['name'], turtle_display=t['displayId'], model=st.split(':', 1)[-1]))
            continue
        if e not in new_g:
            continue
        owned['gameobject'][e] = slug
        if gtype == 14:     # Turtle uses "MO transport" for static WMO decorations; 3.3.5 would treat it as a transport
            gtype = 5
            notes['go_type_changed'].append(f"{e} {t['name'][:60]}: type 14 (static WMO) -> 5 (generic)")
        r = dict(entry=e, type=gtype, displayId=nd, name=t['name'], IconName='', castBarCaption='', unk1='', size=t['size'])
        for n in range(24):
            r[f'Data{n}'] = t[f'data{n}'] if gtype == t['type'] else 0
        if lk_new is not None:
            r[f'Data{lk_field}'] = lk_new
        if gtype == 2:
            r['Data3'] = remap[go_menu[e]] if e in go_menu else 0      # gossip menu (only when it was ported)
        for pf_ in GO_PAGE_FIELD.get(gtype, ()):
            if r[f'Data{pf_}']:
                r[f'Data{pf_}'] = page_ref(r[f'Data{pf_}'])
        if gtype == 25 and r['Data2'] > r['Data3']:     # fishing hole min/max opens: the core asserts min <= max (urand)
            notes['go_data_fixed'].append(f"{e} {t['name'][:60]}: fishing hole opens {r['Data2']}..{r['Data3']} -> 2..6")
            r['Data2'], r['Data3'] = 2, 6
        r.update(AIName='SmartGameObjectAI' if e in go_smart else '', ScriptName='', VerifiedBuild=0)
        rows['gameobject_template'].append(r)
        if t['faction'] or t['flags']:
            rows['gameobject_template_addon'].append(dict(entry=e, faction=FTMAP(t['faction']), flags=t['flags'], mingold=t['mingold'], maxgold=t['maxgold'], artkit0=0, artkit1=0, artkit2=0, artkit3=0))
        if t['type'] in (3, 25) and t['data1'] and not any(r_['Entry'] == t['data1'] for r_ in rows['gameobject_loot_template']):
            # chest / fishing hole loot (once per loot id: two of Stonetalon's Trash objects share one)
            for l in q(f"select * from {TW}.gameobject_loot_template where entry=%s", t['data1']):
                rows['gameobject_loot_template'].append(loot_row(t['data1'], l))
    for r in q(f"select * from {TW}.gameobject_questrelation where quest in ({in_list(qs)})"):
        rows['gameobject_queststarter'].append(dict(id=r['id'], quest=r['quest']))
    for r in q(f"select * from {TW}.gameobject_involvedrelation where quest in ({in_list(qs)})"):
        rows['gameobject_questender'].append(dict(id=r['id'], quest=r['quest']))
    gguid = gbase
    for r_ in gspawns_ac:
        gdisp[r_['id']] = 'ac'
    # 3.3.5 templates that 3.3.5 itself never spawns can hold junk the core asserts on (fishing hole 180184 has
    # minSuccessOpens 10 > maxSuccessOpens 0 -> worldserver shutdown in GameObject::Create)
    go_fix = {}
    if gspawns_ac:
        for r_ in q(f"select entry, name, Data2, Data3 from {AC}.gameobject_template where type=25 and Data2 > Data3 and entry in ({in_list({x['id'] for x in gspawns_ac})})"):
            if r_['entry'] not in _go_fixed:
                go_fix[r_['entry']] = (r_['Data2'], r_['Data3'])
                _go_fixed.add(r_['entry'])
                notes['go_data_fixed'].append(f"{r_['entry']} {r_['name']} (3.3.5 template): fishing hole opens {r_['Data2']}..{r_['Data3']} -> 2..6")
    if gspawns_ac:
        notes['existing_templates'].append(f"{len(gspawns_ac)} object spawns of {len({r['id'] for r in gspawns_ac})} templates 3.3.5 already has (herbs, ore, chests ...)")
    for s in sorted(gspawns + gspawns_ac, key=lambda r: (r['id'], r['guid'])):
        if gdisp.get(s['id']) is None:
            continue
        x, y, z = s['position_x'], s['position_y'], s['position_z']
        if terrain == 'stock':
            htw, hac = twmaps.height(s['map'], x, y), acmaps.height(s['map'], x, y)
            if htw is not None and hac is not None:
                above = z - htw
                if abs(htw - hac) > 1.5 or (subzone(x, y) in custom_sub and above > 2.5):
                    if gtpl[s['id']]['type'] == 5:
                        notes['props_left_out'].append(f"{s['name'][:60]} (tw {s['guid']})")
                        continue
                    z = hac
        gguid += 1
        gmap['gameobject'][s['guid']] = gguid
        rows['gameobject'].append(dict(guid=gguid, id=s['id'], map=s['map'], zoneId=0, areaId=0, spawnMask=1, phaseMask=1,
                                       position_x=x, position_y=y, position_z=z, orientation=s['orientation'],
                                       rotation0=s['rotation0'], rotation1=s['rotation1'], rotation2=s['rotation2'], rotation3=s['rotation3'],
                                       spawntimesecs=s['spawntimesecsmin'] if s['spawntimesecsmin'] > 0 else 300,
                                       animprogress=s['animprogress'] or 100, state=s['state'] if s['state'] is not None else 1,
                                       ScriptName='', VerifiedBuild=0, Comment=f"turtle {slug}: {s['name'][:60]} (tw guid {s['guid']})"))
    assert gguid - gbase < IDS['guid_per_zone'], 'zone GO GUID range overflow'

    # ---------- spawn pools (herbs, ore, chests ...): Turtle pool ids -> pool_base + slot*1000 + n
    pool_base = IDS['pool_base'] + slot * 1000
    pmap = {}
    for kind, table in (('gameobject', 'pool_gameobject'), ('creature', 'pool_creature')):
        if not gmap[kind]:
            continue
        for r in q(f"select * from {TW}.{table} where guid in ({in_list(gmap[kind])})"):
            pe = r['pool_entry']
            pmap.setdefault(pe, pool_base + len(pmap) + 1)
            rows[table].append(dict(guid=gmap[kind][r['guid']], pool_entry=pmap[pe], chance=r['chance'], description=(r['description'] or '')[:255]))
    for pe in list(pmap):
        for pp in q(f"select * from {TW}.pool_pool where pool_id=%s", pe):
            pmap.setdefault(pp['mother_pool'], pool_base + len(pmap) + 1)
            rows['pool_pool'].append(dict(pool_id=pmap[pe], mother_pool=pmap[pp['mother_pool']], chance=pp['chance'], description=(pp['description'] or '')[:255]))
    for pe, npe in sorted(pmap.items(), key=lambda x: x[1]):
        t_ = q(f"select * from {TW}.pool_template where entry=%s", pe)
        rows['pool_template'].append(dict(entry=npe, max_limit=t_[0]['max_limit'] if t_ else 1, description=((t_[0]['description'] if t_ else '') or '')[:255]))
    assert len(pmap) < 1000
    if pmap:
        notes['pools'].append(f"{len(pmap)} spawn pools ({len(rows['pool_gameobject'])} objects, {len(rows['pool_creature'])} creatures)")

    # ---------- write zone file
    remap_creatures(rows)
    loot_ids = [CREMAP.get(l_, l_) for l_ in loot_ids]
    hdr = f"""-- ============================================================================
-- mod-turtle-content : {Z['name']} (zone {zid}, slot {slot})
-- Generated by tools/turtle2ac/build.py on {datetime.date.today()} - do not edit by hand;
-- put hand-written changes in tools/turtle2ac/manual/{slug}.sql instead.
-- Terrain mode: {terrain}
-- ============================================================================
"""
    ce = in_list(r['entry'] for r in rows['creature_template'])
    qe = in_list(qs)
    ge = in_list(r['entry'] for r in rows['gameobject_template'])
    gl = in_list({r['Entry'] for r in rows['gameobject_loot_template']})
    mn = in_list({r['MenuID'] for r in rows['gossip_menu']} | {r['MenuID'] for r in rows['gossip_menu_option']})
    tx = in_list(r['ID'] for r in rows['npc_text'])
    tr = in_list(r['Id'] for r in rows['trainer'])
    g1, g2 = gbase + 1, gbase + IDS['guid_per_zone'] - 1
    dels = f"""DELETE FROM `creature` WHERE `guid` BETWEEN {g1} AND {g2};
DELETE FROM `creature_addon` WHERE `guid` BETWEEN {g1} AND {g2};
DELETE FROM `waypoint_data` WHERE `id` BETWEEN {g1 * 10} AND {g2 * 10 + 9};
DELETE FROM `gameobject` WHERE `guid` BETWEEN {g1} AND {g2};
DELETE FROM `pool_gameobject` WHERE `guid` BETWEEN {g1} AND {g2};
DELETE FROM `pool_creature` WHERE `guid` BETWEEN {g1} AND {g2};
DELETE FROM `pool_pool` WHERE `pool_id` BETWEEN {pool_base + 1} AND {pool_base + 999};
DELETE FROM `pool_template` WHERE `entry` BETWEEN {pool_base + 1} AND {pool_base + 999};
DELETE FROM `creature_template` WHERE `entry` IN ({ce});
DELETE FROM `creature_template_model` WHERE `CreatureID` IN ({ce});
DELETE FROM `creature_template_resistance` WHERE `CreatureID` IN ({ce});
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN ({ce});
DELETE FROM `creature_template_addon` WHERE `entry` IN ({ce});
DELETE FROM `creature_equip_template` WHERE `CreatureID` IN ({ce});
DELETE FROM `creature_loot_template` WHERE `Entry` IN ({in_list(set(loot_ids) | {r['entry'] for r in rows['creature_template']})});
DELETE FROM `skinning_loot_template` WHERE `Entry` IN ({in_list(extra_loot['skinning_loot_template'])});
DELETE FROM `pickpocketing_loot_template` WHERE `Entry` IN ({in_list(extra_loot['pickpocketing_loot_template'])});
DELETE FROM `creature_onkill_reputation` WHERE `creature_id` IN ({ce});
DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({ce}) AND `id` < 100;
DELETE FROM `creature_text` WHERE `CreatureID` IN ({ce}) AND `GroupID` >= 50;
DELETE FROM `smart_scripts` WHERE `source_type`=1 AND `entryorguid` IN ({in_list(new_g)}) AND `id` < 100;
DELETE FROM `npc_vendor` WHERE `entry` IN ({ce});
DELETE FROM `trainer` WHERE `Id` IN ({tr});
DELETE FROM `trainer_spell` WHERE `TrainerId` IN ({tr});
DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN ({ce});
DELETE FROM `gossip_menu` WHERE `MenuID` IN ({mn});
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN ({mn});
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` IN (14, 15) AND `SourceGroup` IN ({mn});
DELETE FROM `npc_text` WHERE `ID` IN ({tx});
DELETE FROM `quest_template` WHERE `ID` IN ({qe});
DELETE FROM `quest_template_addon` WHERE `ID` IN ({qe});
DELETE FROM `quest_offer_reward` WHERE `ID` IN ({qe});
DELETE FROM `quest_request_items` WHERE `ID` IN ({qe});
DELETE FROM `creature_queststarter` WHERE `quest` IN ({qe});
DELETE FROM `creature_questender` WHERE `quest` IN ({qe});
DELETE FROM `gameobject_queststarter` WHERE `quest` IN ({qe});
DELETE FROM `gameobject_questender` WHERE `quest` IN ({qe});
DELETE FROM `gameobject_template` WHERE `entry` IN ({ge});
DELETE FROM `gameobject_template_addon` WHERE `entry` IN ({ge});
DELETE FROM `gameobject_loot_template` WHERE `Entry` IN ({gl});
DELETE FROM `areatable_dbc` WHERE `ID` IN ({in_list(r['ID'] for r in area_rows)});
"""
    man = os.path.join(HERE, 'manual', slug + '.sql')
    fname = f"mod_turtle_{slot + 1:03d}_{slug.split('_', 1)[1]}.sql"
    pending_render.append(dict(slug=slug, fname=fname, hdr=hdr, dels=dels, rows=rows, manual=man if os.path.exists(man) else None, ce=ce, name=Z['name'], go_fix=go_fix,
                               emitted={r['entry'] for r in rows['creature_template']} | set(ac_ct)))
    rep = dict(zone=slug, name=Z['name'], file=fname, terrain=terrain, custom_subzones=sorted(custom_sub),
               counts={k: len(v) for k, v in rows.items() if v}, go_pending=pending, notes=notes)
    all_reports.append(rep)
    zone_extras.append((Z, slug, notes, rows))
    return rep


KEY_COL = dict(map_dbc='ID', mapdifficulty_dbc='ID', instance_template='map', dungeon_access_template='id', areatrigger='entry',
               areatrigger_teleport='ID', areatrigger_tavern='id', game_graveyard='ID', graveyard_zone='ID', taxinodes_dbc='ID', taxipath_dbc='ID',
               taxipathnode_dbc='ID', wmoareatable_dbc='ID', game_tele='id')


def manual_blocks(path, emitted):
    """Manual SQL is split into blocks: '-- @block requires=ID,ID' ... '-- @end'.
    A block is only emitted when every creature it requires is part of the build."""
    out, cur_req, buf, inside = [], None, [], False
    for ln in open(path).read().split('\n'):
        m_ = re.match(r'--\s*@block\s+requires=([\d,\s]+)', ln)
        if m_:
            inside, cur_req, buf = True, {int(x) for x in m_.group(1).replace(' ', '').split(',') if x}, []
            continue
        if inside and re.match(r'--\s*@end', ln):
            inside = False
            if cur_req <= emitted:
                out += buf
            else:
                out.append(f"-- (block skipped: needs creatures {sorted(cur_req - emitted)} which are held back)")
            continue
        (buf if inside else out).append(ln)
    return '\n'.join(out)


def loot_row(entry, l):
    if l['mincountOrRef'] < 0:
        ref = -l['mincountOrRef']
        refs_needed.add(ref)
        return dict(Entry=entry, Item=IDS['reference_loot_base'] + ref, Reference=IDS['reference_loot_base'] + ref, Chance=abs(l['ChanceOrQuestChance']),
                    QuestRequired=0, LootMode=1, GroupId=l['groupid'], MinCount=1, MaxCount=l['maxcount'], Comment=f'Turtle reference {ref}')
    if not ac_item(l['item']):
        items_needed.add(l['item'])
    return dict(Entry=entry, Item=I(l['item']), Reference=0, Chance=abs(l['ChanceOrQuestChance']), QuestRequired=1 if l['ChanceOrQuestChance'] < 0 else 0,
                LootMode=1, GroupId=l['groupid'], MinCount=l['mincountOrRef'], MaxCount=l['maxcount'], Comment=None)


# =========================================================================== maps, triggers, flight paths, world map, lights
from lib.dbcw import Table, loc
_CT = {}


CT_BASE = {}       # table -> (archive, path) of the client copy each shipped table was built from


def CT(name):
    """the client's effective copy of a DBC (highest-priority archive in the client335 extract), loaded once;
    rows added here end up in the client patch"""
    if name not in _CT:
        a = client335_archive(f'DBFilesClient\\{name}.dbc')
        assert a, f'{name}.dbc is in no archive of the client335 extract - add it to client335_extract.py DBCS and re-run it'
        p_ = client335_file(f'DBFilesClient\\{name}.dbc')
        CT_BASE[name] = (a, p_)
        _CT[name] = Table(p_, name)
        _CT[name].reserved = set(CFG.get('reserved_client_ids', {}).get(name, []))
    return _CT[name]


def f32(v):
    return struct.unpack('<f', struct.pack('<I', v))[0]


def tw_dbc(name):
    n_, f_, rs_, rows_, s_, _ = load(CFG['tw_dbc'] + f'/{name}.dbc')
    return {r[0]: r for r in rows_}, s_


TW_TAXI_NODES, _tn_s = tw_dbc('TaxiNodes')
TW_TAXI_PATH, _ = tw_dbc('TaxiPath')
TW_WSL, _wsl_s = tw_dbc('WorldSafeLocs')
TW_AT, _ = tw_dbc('AreaTrigger')
TW_WMA_ROWS, _wma_s = tw_dbc('WorldMapArea')
TW_WMO, _wmo_s = tw_dbc('WMOAreaTable')
taxi_node_map = {}         # Turtle taxi node -> 3.3.5 node
SCRIPTED_TAXI = {}         # Turtle taxi path started by a script -> 3.3.5 path (scripted_taxi_paths)
next_ids = dict(taxi_node=IDS['taxi_node_base'], taxi_path=IDS['taxi_path_base'], taxi_path_node=IDS['taxi_path_node_base'],
                areatrigger=IDS['areatrigger_base'], graveyard=IDS['graveyard_base'], game_tele=IDS.get('game_tele_base', 9100),
                dungeon_access=IDS.get('dungeon_access_base', 9100))
zone_sql = collections.defaultdict(list)       # slug -> [(table, rows)]
zone_undo = collections.defaultdict(list)      # slug -> [sql]


TAXI_NODE_SPARE = list(range(437, 405, -1))   # 3.3.5 ids no client/server TaxiNodes row uses, used once 441-447 are taken


def take(kind, n=1):
    if kind == 'taxi_node' and next_ids[kind] >= 448:
        # the 3.3.5 client's known-nodes mask ends at 447: continue downwards in the free block 437..406
        # (earlier zones keep 441-447, so their node ids do not move)
        assert n == 1 and TAXI_NODE_SPARE, 'no free taxi node id below 448 left'
        return TAXI_NODE_SPARE.pop(0)
    if kind == 'dungeon_access' and next_ids[kind] >= 256:
        # dungeon_access_template.id is a TINYINT: past 255 continue downwards from 249 (earlier dungeons keep 250-255)
        assert n == 1
        v = 249 - (next_ids[kind] - 256)
        next_ids[kind] += 1
        assert v > 121 and not q(f"select 1 from {AC}.dungeon_access_template where id=%s", v), f'dungeon_access_template id {v} is taken'
        return v
    v = next_ids[kind]
    next_ids[kind] += n
    return v


def srv_row(table, values):
    """3.3.5 DBC row (python values) -> dict for the server-side <name>_dbc table (same column order)."""
    cols = SRV_COLS[table]
    assert len(cols) == len(values), f'{table}: {len(cols)} columns, row has {len(values)}'
    # DBC fields are stored unsigned; the server tables use signed INTs for fields like -1 (WMOGroupID, TimeOfDayOverride)
    return dict(zip(cols, [v - (1 << 32) if isinstance(v, int) and v >= (1 << 31) else v for v in values]))


SRV_COLS = {t: [r['column_name'] for r in q(
    "select column_name from information_schema.columns where table_schema=%s and table_name=%s order by ordinal_position", AC, t)]
    for t in ('map_dbc', 'mapdifficulty_dbc', 'taxinodes_dbc', 'taxipath_dbc', 'taxipathnode_dbc', 'wmoareatable_dbc', 'faction_dbc', 'factiontemplate_dbc')}


# =========================================================================== factions (reputations) and faction templates
# Turtle's own factions reuse ids 3.3.5 gives to other factions (Kul Tiras 1011 = Lower City, Earthen Ring 1014 = Spirits of
# Shadowmoon 2, Durotar Labor Union 1001 = Bladespire Clan ...), and its faction templates reuse 3.3.5 template ids
# (Kul Tiras' 1693 is a hostile monster template in 3.3.5). FMAP / FTMAP give every Turtle faction / template the module's
# content uses its 3.3.5 meaning: the same id where 3.3.5 means the same, else a new row (client patch + faction_dbc /
# factiontemplate_dbc). A Turtle reputation 3.3.5 knows only as a non-reputation faction (Revantusk Trolls 893) keeps its
# id and gets a reputation index. New reputations take free reputation indexes (3.3.5 uses 0-104; the client has 128).
TW_FAC, _fac_s = tw_dbc('Faction')
TW_FT, _ = tw_dbc('FactionTemplate')
FAC_MAP, FT_MAP, FAC_ROWS, FT_ROWS = {}, {}, {}, {}      # Turtle id -> 3.3.5 id; new/changed 3.3.5 id -> row
FAC_NOTES = []
_next_fac = [IDS['faction_base']]
_next_ft = [IDS['faction_template_base']]
_next_rep = [IDS['reputation_index_base']]
_TW_ALLY, _TW_HORDE = 1 | 4 | 8 | 64, 2 | 16 | 32 | 128      # vanilla race bits (Turtle's extra races use the 3.3.5 bits of other races)


def _race_mask(m):
    out = m & 0xFF
    if m and not out:
        return 256                        # only Turtle's own races (High Elf, Goblin): race 9, which no 3.3.5 player is
    if m and out & _TW_ALLY == _TW_ALLY:
        out |= 1024                       # all Alliance races: Draenei too
    if m and out & _TW_HORDE == _TW_HORDE:
        out |= 512                        # all Horde races: Blood Elves too
    return out


def _class_mask(m):
    return m | 32 if m and m & 1503 == 1503 else m     # all vanilla classes: Death Knights too


def FMAP(f):
    """Turtle faction id -> 3.3.5 faction id with the same meaning (adds the faction when 3.3.5 has none)"""
    if not f or f in FAC_MAP:
        return FAC_MAP.get(f, f)
    if f in CFG.get('faction_keep_335', []):
        # config faction_keep_335: 3.3.5's row as it is, even where Turtle gave the faction a reputation (Battleground
        # Neutral 709, Tirisfal's Scarlet camp: a hidden reputation nobody gains; 3.3.5's template 1194 is the same)
        FAC_MAP[f] = f
        return f
    tw = TW_FAC.get(f)
    if tw is None:
        FAC_MAP[f] = f
        return f
    ac = CT('Faction').get(f)
    tname = _fac_s(tw[19])
    tw_rep = tw[1] < 0x80000000
    if ac is not None and (not tw_rep or (ac[23] == tname and ac[1] < 0x80000000)):
        # same reputation in 3.3.5, or no reputation at all: only the templates' group masks matter there, and 3.3.5's
        # row under that id stands for the same creatures (Turtle's "Horde Affiliates" is 3.3.5's "Horde Generic")
        FAC_MAP[f] = f
        return f
    if ac is not None and ac[23] == tname:
        nid = f                           # 3.3.5 has it, but not as a reputation (Revantusk Trolls): it gets one
    elif ac is None and f < IDS['faction_base']:
        nid = f                           # a faction 3.3.5 does not have (Draenei Exiles 10): Turtle's id is free
    else:
        while CT('Faction').get(_next_fac[0]) is not None:
            _next_fac[0] += 1
        nid = _next_fac[0]
        _next_fac[0] += 1
    FAC_MAP[f] = nid
    rep = 0xFFFFFFFF
    if tw_rep:
        rep = _next_rep[0]
        _next_rep[0] += 1
        assert rep < 128, 'no free reputation index left (the client has 128)'
    parent = tw[18]
    parent = FMAP(parent) if parent else (1118 if tw_rep and CT('Faction').get(1118) is not None else 0)   # 1118: "Classic"
    row = [nid, rep] + [_race_mask(v) for v in tw[2:6]] + [_class_mask(v) for v in tw[6:10]] + list(tw[10:14]) + list(tw[14:18]) \
        + [parent, 0.0, 0.0, 0, 0] + loc(tname) + [16712190] + loc(_fac_s(tw[28])) + [16712190]
    CT('Faction').add(row, replace=ac is not None)
    FAC_ROWS[nid] = row
    FAC_NOTES.append(f"Turtle faction {f} {tname}" + (f" -> {nid}" if nid != f else '') + (f" (reputation index {rep})" if tw_rep else '')
                     + (f" - 3.3.5's {f} is {ac[23]}" if ac is not None and ac[23] != tname else ''))
    return nid


def FTMAP(ft):
    """Turtle faction template id -> 3.3.5 template id that behaves the same (adds the template when needed)"""
    if not ft or ft in FT_MAP:
        return FT_MAP.get(ft, ft)
    tw = TW_FT.get(ft)
    if tw is None:
        FT_MAP[ft] = ft
        return ft
    row = [ft, FMAP(tw[1]), tw[2], tw[3], tw[4], tw[5]] + [FMAP(v) for v in tw[6:10]] + [FMAP(v) for v in tw[10:14]]
    ac = CT('FactionTemplate').get(ft)
    if ac is not None and ac[1] == row[1] and ac[3] == row[3] and ac[5] == row[5]:
        FT_MAP[ft] = ft                   # same faction, same group and enemy masks
        return ft
    while CT('FactionTemplate').get(_next_ft[0]) is not None:
        _next_ft[0] += 1
    nid = _next_ft[0]
    _next_ft[0] += 1
    row[0] = nid
    CT('FactionTemplate').add(row)
    FT_ROWS[nid] = row
    FT_MAP[ft] = nid
    FAC_NOTES.append(f"Turtle faction template {ft} (faction {tw[1]} {_fac_s(TW_FAC[tw[1]][19]) if tw[1] in TW_FAC else '?'}) -> {nid}"
                     + (f" - 3.3.5's {ft} is faction {ac[1]}" if ac is not None else ''))
    return nid


def world_pass(Z, slug, notes):
    out = zone_sql[slug]
    undo = zone_undo[slug]
    m = Z['map']
    # ---------------- instance map
    I = Z.get('instance')
    if I:
        # existing_map (Stormwind Vault, map 35): 3.3.5 already has the map (an unused non-instance map with the same WMO);
        # its Map row is replaced by an instance row (client patch + map_dbc override; the rollback's DELETE brings the
        # stock row back). Otherwise the map must be new.
        if I.get('existing_map'):
            old_ = CT('Map').get(m)
            assert old_ is not None and old_[1].lower() == Z['map_dir'].lower(), f"map {m} is not the 3.3.5 map {Z['map_dir']}"
        else:
            assert CT('Map').get(m) is None, f'map {m} already exists in the 3.3.5 client'
        # a loading screen 3.3.5 already ships (LoadScreenDungeon.blp) reuses its stock row; otherwise a new row
        stock_ls_ = [r[0] for r in CT('LoadingScreens').rows.values()
                     if r[0] not in CT('LoadingScreens').added and r[2].lower() == I['loading_screen'].lower()]
        if stock_ls_:
            ls_id = min(stock_ls_)
        else:
            ls_id = CT('LoadingScreens').free_id(IDS['loading_screen_base'])
            CT('LoadingScreens').add([ls_id, 'Instance' + re.sub(r'\W', '', I['map_name']), I['loading_screen'], 0])
        t = list(CT('Map').get(I['template_map']))
        row = [m, Z['map_dir'], I['instance_type'], t[3], 0] + loc(I['map_name']) + [t[21], Z['zone_id']] + loc('') + [t[39]] + loc('') + [t[56]] + \
              [ls_id, 1.0, I['corpse'][0], I['corpse'][1], I['corpse'][2], t[62], 0, 0, I['max_players']]
        CT('Map').add(row, replace=bool(I.get('existing_map')))
        out.append(('map_dbc', [srv_row('map_dbc', row)]))
        md = [r for r in CT('MapDifficulty').rows.values() if r[1] == I['template_map']][0]
        own_md = [r for r in CT('MapDifficulty').rows.values() if r[1] == m and r[2] == 0]
        if I.get('existing_map') and own_md:
            md_id = own_md[0][0]           # 3.3.5's own row for the map (map 35: id 9, no player limit) becomes the dungeon's
        else:
            md_id = CT('MapDifficulty').free_id(IDS['map_difficulty_base'])     # never stock max + 1: other modules (individual-progression) use those
        mrow = [md_id, m] + list(md[2:21]) + [I['max_players'], md[22]]
        CT('MapDifficulty').add(mrow, replace=bool(I.get('existing_map') and own_md))
        out.append(('mapdifficulty_dbc', [srv_row('mapdifficulty_dbc', mrow)]))
        out.append(('instance_template', [dict(map=m, parent=0, script='', allowMount=0)]))
        da = take('dungeon_access')
        out.append(('dungeon_access_template', [dict(id=da, map_id=m, difficulty=0, min_level=I['min_level'], max_level=0, min_avg_item_level=0,
                                                     comment=I['map_name'])]))
        # area triggers (new ids: Turtle's collide with 3.3.5 ones)
        at_rows, tp_rows = [], []
        for tw_id, kind in I['areatriggers']:
            a = TW_AT[tw_id]
            nid = take('areatrigger')
            assert CT('AreaTrigger').get(nid) is None
            vals = [f32(v) for v in a[2:10]]
            CT('AreaTrigger').add([nid, a[1]] + vals)
            at_rows.append(dict(entry=nid, map=a[1], x=vals[0], y=vals[1], z=vals[2], radius=vals[3], length=vals[4], width=vals[5],
                                height=vals[6], orientation=vals[7]))
            tp = q(f"select * from {TW}.areatrigger_teleport where id=%s", tw_id)[0]
            tp_rows.append(dict(ID=nid, Name=tp['name'].replace('–', '-'), target_map=tp['target_map'], target_position_x=tp['target_position_x'],
                                target_position_y=tp['target_position_y'], target_position_z=tp['target_position_z'],
                                target_orientation=tp['target_orientation']))
            notes['area_triggers'].append(f"Turtle trigger {tw_id} {tp['name']} -> {nid}")
        out.append(('areatrigger', at_rows))
        out.append(('areatrigger_teleport', tp_rows))
        if I.get('graveyard'):
            g = I['graveyard']
            # {map,x,y,z,o}: a list was once read as [map,x,y,z] while it held an orientation -> graveyard 130 yd underground
            assert isinstance(g, dict) and {'map', 'x', 'y', 'z'} <= set(g), f"{slug}: instance.graveyard must be {{map,x,y,z,o}}"
            gid = take('graveyard')
            out.append(('game_graveyard', [dict(ID=gid, Map=g['map'], x=g['x'], y=g['y'], z=g['z'], Comment=f"{I['map_name']} - entrance (mod-turtle-content)")]))
            out.append(('graveyard_zone', [dict(ID=gid, GhostZone=Z['zone_id'], Faction=0, Comment=I['map_name'])]))
        new_maps_dir[m] = Z['map_dir']
    # ---------------- inn rest areas (Turtle area trigger + areatrigger_tavern; new trigger ids, Turtle's collide)
    if Z.get('taverns'):
        at_rows, tav_rows = [], []
        for tw_id in Z['taverns']:
            a = TW_AT[tw_id]
            nid = take('areatrigger')
            assert CT('AreaTrigger').get(nid) is None
            vals = [f32(v) for v in a[2:10]]
            CT('AreaTrigger').add([nid, a[1]] + vals)
            at_rows.append(dict(entry=nid, map=a[1], x=vals[0], y=vals[1], z=vals[2], radius=vals[3], length=vals[4], width=vals[5],
                                height=vals[6], orientation=vals[7]))
            tv = q(f"select * from {TW}.areatrigger_tavern where id=%s", tw_id)
            name = (tv[0]['name'] if tv else '') or f"{Z['name']} inn"
            tav_rows.append(dict(id=nid, name=name, faction=0))
            notes['area_triggers'].append(f"Turtle trigger {tw_id} {name} (rest area) -> {nid}")
        out.append(('areatrigger', at_rows))
        out.append(('areatrigger_tavern', tav_rows))
    # ---------------- graveyards (Turtle WorldSafeLocs)
    for wid in Z.get('graveyards', []):
        w = TW_WSL[wid]
        gid = take('graveyard')
        out.append(('game_graveyard', [dict(ID=gid, Map=w[1], x=f32(w[2]), y=f32(w[3]), z=f32(w[4]), Comment=f"{_wsl_s(w[5])} (mod-turtle-content)")]))
        fr = q(f"select faction from {TW}.game_graveyard_zone where id=%s and ghost_zone=%s", wid, Z['zone_id'])
        fac = fr[0]['faction'] if fr and fr[0]['faction'] in (67, 469) else 0          # 469 Alliance, 67 Horde, 0 both
        out.append(('graveyard_zone', [dict(ID=gid, GhostZone=Z['zone_id'], Faction=fac, Comment=Z['name'])]))
        notes['graveyards'].append(f"Turtle graveyard {wid} {_wsl_s(w[5])} -> {gid}" + {469: ' (Alliance)', 67: ' (Horde)'}.get(fac, ''))
    # ---------------- flight masters
    if Z.get('taxi_nodes'):
        nodes = []
        for tn in Z['taxi_nodes']:
            r = TW_TAXI_NODES[tn]
            nid = take('taxi_node')
            assert nid < 448 and CT('TaxiNodes').get(nid) is None, f'taxi node {nid} not usable'
            taxi_node_map[tn] = nid
            row = [nid, r[1], f32(r[2]), f32(r[3]), f32(r[4])] + loc(_tn_s(r[5])) + [16712190, r[14], r[15]]
            CT('TaxiNodes').add(row)
            nodes.append(srv_row('taxinodes_dbc', row))
            notes['flight_paths'].append(f"node {nid} {_tn_s(r[5])} (Turtle {tn})")
        out.append(('taxinodes_dbc', nodes))
        paths, pnodes = [], []
        n_tpn, _, _, tpn_rows, _, _ = load(CFG['tw_dbc'] + '/TaxiPathNode.dbc')
        by_path = collections.defaultdict(list)
        for r in tpn_rows:
            by_path[r[1]].append(r)
        for pid, r in sorted(TW_TAXI_PATH.items()):
            if r[1] not in Z['taxi_nodes'] and r[2] not in Z['taxi_nodes']:
                continue
            a, b = taxi_node_map.get(r[1], r[1]), taxi_node_map.get(r[2], r[2])
            def stock_node(tn_):          # a Turtle node not ported here: only usable if 3.3.5 has the same node (same id and place)
                c_, t_ = CT('TaxiNodes').get(tn_), TW_TAXI_NODES.get(tn_)
                return c_ is not None and t_ is not None and c_[1] == t_[1] and \
                    abs(c_[2] - f32(t_[2])) < 10 and abs(c_[3] - f32(t_[3])) < 10
            if (r[1] not in taxi_node_map and not stock_node(r[1])) or (r[2] not in taxi_node_map and not stock_node(r[2])):
                notes['flight_paths'].append(f"Turtle path {pid} {r[1]}->{r[2]} skipped (other end is not a 3.3.5 node)")
                continue
            npid = take('taxi_path')
            prow = [npid, a, b, r[3]]
            CT('TaxiPath').add(prow)
            paths.append(srv_row('taxipath_dbc', prow))
            for pn in sorted(by_path[pid], key=lambda x: x[2]):
                nn = take('taxi_path_node')
                nrow = [nn, npid, pn[2], pn[3], f32(pn[4]), f32(pn[5]), f32(pn[6]), pn[7], pn[8], 0, 0]
                CT('TaxiPathNode').add(nrow)
                pnodes.append(srv_row('taxipathnode_dbc', nrow))
            notes['flight_paths'].append(f"path {npid}: {a} -> {b}, {len(by_path[pid])} points, cost {r[3]}")
        out.append(('taxipath_dbc', paths))
        out.append(('taxipathnode_dbc', pnodes))
    # ---------------- scripted flights (a Turtle gossip script starts a taxi path that no flight master offers)
    # The start is a new node with no flight master (no path leads into it, so flight-master routes never use it); the
    # end is a node already ported (taxi_node_map). The path's points are Turtle's. manual scripts: ctx['taxi_path'](id).
    if Z.get('scripted_taxi_paths'):
        nodes, paths, pnodes = [], [], []
        tpn_rows = load(CFG['tw_dbc'] + '/TaxiPathNode.dbc')[3]
        for sp in Z['scripted_taxi_paths']:
            r = TW_TAXI_PATH[sp['path']]
            assert sp['to'] in taxi_node_map, f"scripted taxi path {sp['path']}: Turtle node {sp['to']} is not ported"
            src = TW_TAXI_NODES[r[1]]
            nid = take('taxi_node')
            assert nid < 448 and CT('TaxiNodes').get(nid) is None, f'taxi node {nid} not usable'
            # 'at': the node where the script's NPC stands (the core lets a scripted flight start only within 10 yd of its node)
            xyz_ = [float(v) for v in sp['at']] if sp.get('at') else [f32(src[2]), f32(src[3]), f32(src[4])]
            row = [nid, src[1]] + xyz_ + loc(sp['name']) + [16712190, src[14], src[15]]
            CT('TaxiNodes').add(row)
            nodes.append(srv_row('taxinodes_dbc', row))
            npid = take('taxi_path')
            prow = [npid, nid, taxi_node_map[sp['to']], r[3]]
            CT('TaxiPath').add(prow)
            paths.append(srv_row('taxipath_dbc', prow))
            pts = sorted([x for x in tpn_rows if x[1] == sp['path']], key=lambda x: x[2])
            for pn in pts:
                nn = take('taxi_path_node')
                nrow = [nn, npid, pn[2], pn[3], f32(pn[4]), f32(pn[5]), f32(pn[6]), pn[7], pn[8], 0, 0]
                CT('TaxiPathNode').add(nrow)
                pnodes.append(srv_row('taxipathnode_dbc', nrow))
            SCRIPTED_TAXI[sp['path']] = npid
            notes['flight_paths'].append(f"scripted path {npid} (Turtle {sp['path']}): new node {nid} {sp['name']} -> "
                                         f"{taxi_node_map[sp['to']]}, {len(pts)} points")
        out.append(('taxinodes_dbc', nodes))
        out.append(('taxipath_dbc', paths))
        out.append(('taxipathnode_dbc', pnodes))
    # ---------------- WMO area names (buildings / dungeon rooms)
    wrows = []
    for wid in Z.get('wmo_area_ids', []):
        # wmo_area_groups: only these WMO group ids (Turtle's new rooms of a 3.3.5 building whose own rooms 3.3.5 names already)
        for r in sorted((r for r in TW_WMO.values() if r[1] == wid and (not Z.get('wmo_area_groups') or r[3] in Z['wmo_area_groups'])),
                        key=lambda r: r[0]):
            nid = r[0] if CT('WMOAreaTable').get(r[0]) is None else CT('WMOAreaTable').free_id(IDS['wmo_area_base'])
            row = [nid, r[1], r[2], r[3], r[4], r[5], r[6], ZONE_MUSIC_SUB.get(r[7], r[7]), INTRO_SUB.get(r[8], r[8]), r[9], AR(r[10])] + \
                  loc(_wmo_s(r[11])) + [16712190 if _wmo_s(r[11]) else 0]
            CT('WMOAreaTable').add(row)
            wrows.append(srv_row('wmoareatable_dbc', row))
    if wrows:
        out.append(('wmoareatable_dbc', wrows))
        notes['wmo_areas'].append(f"{len(wrows)} WMOAreaTable rows (room names) for WMO ids {Z['wmo_area_ids']}")
    # ---------------- world map
    wm = Z.get('world_map')
    if wm:
        tw_wma = [r for r in TW_WMA_ROWS.values() if r[2] == wm['tw_area']][0]
        wid = CT('WorldMapArea').free_id(IDS['world_map_area_base'])
        name = _wma_s(tw_wma[3])
        CT('WorldMapArea').add([wid, tw_wma[1], tw_wma[2], name] + [f32(v) for v in tw_wma[4:8]] + [0xFFFFFFFF, 0, 0])
        n_ov, _, _, ov_rows, ov_s, _ = load(CFG['tw_dbc'] + '/WorldMapOverlay.dbc')
        k = 0
        for r in ov_rows:
            if r[1] != tw_wma[0]:
                continue
            oid = CT('WorldMapOverlay').free_id(IDS['world_map_overlay_base'])
            CT('WorldMapOverlay').add([oid, wid] + [AR(v) for v in r[2:6]] + list(r[6:8]) + [ov_s(r[8])] + list(r[9:17]))
            k += 1
        folder = f"interface\\worldmap\\{name.lower()}\\"
        art = {p: lp for p, lp in ASSETS.local.items() if p.startswith(folder)}
        for p, lp in art.items():
            ship_files[ASSETS.turtle.get(p, p)] = lp
        notes['world_map'].append(f"WorldMapArea {wid} '{name}' + {k} subzone overlays, {len(art)} map images")
    # ---------------- lights (sky colours / fog)
    if Z.get('lights'):
        port_lights(Z['lights'], notes)
    # ---------------- teleports for GMs
    for r in ([] if not (Z.get('spawn_existing_templates') or I) else q(f"select * from {TW}.game_tele where (map=%s and (name like %s or name like %s))", m, '%' + Z['name'].split()[0].lower() + '%',
               '%' + Z['name'].replace(' ', '').lower() + '%')):
        out.append(('game_tele', [dict(id=take('game_tele'), position_x=r['position_x'], position_y=r['position_y'], position_z=r['position_z'],
                                       orientation=r['orientation'], map=r['map'], name=r['name'])]))
    if I:
        tp = q(f"select * from {TW}.areatrigger_teleport where id=%s", I['areatriggers'][0][0])[0]
        out.append(('game_tele', [dict(id=take('game_tele'), position_x=tp['target_position_x'], position_y=tp['target_position_y'],
                                       position_z=tp['target_position_z'], orientation=tp['target_orientation'], map=m,
                                       name=re.sub(r'\W', '', I['map_name']))]))


TW_LIGHT, _ = tw_dbc('Light')
TW_LP, _ = tw_dbc('LightParams')
light_param_map = {}


def port_lights(ids, notes):
    n_, f_, rs_, ib, _, _ = load(CFG['tw_dbc'] + '/LightIntBand.dbc')
    n_, f_, rs_, fb, _, _ = load(CFG['tw_dbc'] + '/LightFloatBand.dbc')
    IB = {r[0]: r for r in ib}
    FB = {r[0]: r for r in fb}
    vanilla_params = 4             # Turtle param ids <= this are the stock death/underwater params
    for lid in ids:
        r = TW_LIGHT[lid]
        params = []
        for p in r[7:12]:
            if p <= vanilla_params or p in light_param_map:
                params.append(light_param_map.get(p, p))
                continue
            # new LightParams id whose 18 int bands and 6 float bands are free too
            np_ = CT('LightParams').free_id(IDS['light_params_base'])
            while any(CT('LightIntBand').get(np_ * 18 - 17 + i) for i in range(18)) or any(CT('LightFloatBand').get(np_ * 6 - 5 + i) for i in range(6)):
                np_ += 1
            lp = TW_LP[p]
            CT('LightParams').add([np_, lp[1], 0, 0] + [f32(v) for v in lp[4:9]])
            for i in range(18):
                b = IB[p * 18 - 17 + i]
                CT('LightIntBand').add([np_ * 18 - 17 + i] + list(b[1:]))
            for i in range(6):
                b = FB[p * 6 - 5 + i]
                CT('LightFloatBand').add([np_ * 6 - 5 + i] + list(b[1:18]) + [f32(v) for v in b[18:34]])
            light_param_map[p] = np_
            params.append(np_)
        nid = CT('Light').free_id(IDS['light_base'])
        CT('Light').add([nid, r[1]] + [f32(v) for v in r[2:7]] + params + [0, 0, 0])
        notes['lights'].append(f"Light {nid} (Turtle {lid}) params {params}")


for z in CFG['zones']:
    build_zone(z)
for Z_, slug_, notes_, rows_ in zone_extras:
    world_pass(Z_, slug_, notes_)

# =========================================================================== common: references + items
print('[common] references and items')
# containers (Turtle items that are opened, e.g. the Oversized Lugnut Ring holding 'Rightful' Jade): their contents are
# ported with them (item_loot_template); the rows register the items and references they need
cont_src, _seen_c = {}, set()
while set(items_needed) - _seen_c:
    for i_ in sorted(set(items_needed) - _seen_c):
        _seen_c.add(i_)
        rows_ = q(f"select * from {TW}.item_loot_template where entry=%s", i_)
        if rows_:
            cont_src[i_] = rows_
            for l_ in rows_:
                loot_row(0, l_)
ref_rows = []
done = set()
while refs_needed - done:
    ref = min(refs_needed - done)
    done.add(ref)
    for l in q(f"select * from {TW}.reference_loot_template where entry=%s", ref):
        ref_rows.append(loot_row(IDS['reference_loot_base'] + ref, l))

# decide which needed items are ported
tw_items = {r['entry']: r for r in q(f"select * from {TW}.item_template where entry in ({in_list(items_needed)})")}
ported, dropped = {}, []
for i in sorted(items_needed):
    it = tw_items.get(i)
    if not it or item_excluded(it):
        dropped.append(i)
        continue
    ported[i] = it
item_ok = {i for i in ac_it if i not in ITEM_REMAP} | {I(i) for i in ported}
# filter loot rows referencing dropped items (in refs) - zone loot is filtered at write time below
ref_rows = [r for r in ref_rows if r['Reference'] or r['Item'] in item_ok]
# references left empty (all their items were dropped, e.g. Turtle Jewelcrafting plans) are removed with every row pointing at them
empty_refs = set()
while True:
    have_ref = {r['Entry'] for r in ref_rows}
    new_empty = {r['Reference'] for r in ref_rows if r['Reference'] and r['Reference'] not in have_ref} - empty_refs
    if not new_empty:
        break
    empty_refs |= new_empty
    ref_rows = [r for r in ref_rows if r['Reference'] not in empty_refs]
empty_refs |= {IDS['reference_loot_base'] + x for x in refs_needed} - {r['Entry'] for r in ref_rows}

it_rows, idbc, item_notes = [], [], []
for i, t in ported.items():
    d, st = disp.item(t['display_id'])
    if d is None:
        d = 3109 if t['inventory_type'] == 23 else 1288
        item_notes.append(f"{i} {t['name']}: Turtle display {t['display_id']} not in 3.3.5 ({st}) - stand-in {d}")
    elif st not in ('same',):
        item_notes.append(f"{i} {t['name']}: display {t['display_id']} -> {d} ({st})")
    r = dict(entry=I(i), **{'class': t['class']}, subclass=t['subclass'], SoundOverrideSubclass=-1, name=t['name'], displayid=d,
             Quality=t['quality'], Flags=t['flags'] & 0xFFFF, FlagsExtra=0, BuyCount=t['buy_count'] or 1, BuyPrice=t['buy_price'],
             SellPrice=t['sell_price'], InventoryType=t['inventory_type'], AllowableClass=t['allowable_class'],
             AllowableRace=-1 if t['allowable_race'] in (-1, 0x7FF, 0x1FF, 0x3FF, 0xFF) else conv_races(t['allowable_race']),
             ItemLevel=t['item_level'], RequiredLevel=t['required_level'], RequiredSkill=t['required_skill'],
             RequiredSkillRank=t['required_skill_rank'], requiredspell=t['required_spell'], requiredhonorrank=0, RequiredCityRank=0,
             RequiredReputationFaction=FMAP(t['required_reputation_faction']), RequiredReputationRank=t['required_reputation_rank'],
             maxcount=t['max_count'], stackable=t['stackable'], ContainerSlots=t['container_slots'])
    stats = [(t[f'stat_type{n}'], t[f'stat_value{n}']) for n in range(1, 11) if t[f'stat_type{n}']]
    for n in range(1, 6):
        s = t[f'spellid_{n}']
        if s in ITEM_SPELL_REPL and 'stat' in ITEM_SPELL_REPL[s]:
            stats.append(tuple(ITEM_SPELL_REPL[s]['stat']))
            item_notes.append(f"{i} {t['name']}: spell {s} -> {ITEM_SPELL_REPL[s]['note']}")
    for n in range(1, 11):
        a, v = stats[n - 1] if n <= len(stats) else (0, 0)
        r[f'stat_type{n}'] = a; r[f'stat_value{n}'] = v
    r.update(ScalingStatDistribution=0, ScalingStatValue=0, dmg_min1=t['dmg_min1'], dmg_max1=t['dmg_max1'], dmg_type1=t['dmg_type1'],
             dmg_min2=t['dmg_min2'], dmg_max2=t['dmg_max2'], dmg_type2=t['dmg_type2'], armor=max(0, t['armor']), holy_res=t['holy_res'],
             fire_res=t['fire_res'], nature_res=t['nature_res'], frost_res=t['frost_res'], shadow_res=t['shadow_res'],
             arcane_res=t['arcane_res'], delay=t['delay'], ammo_type=t['ammo_type'], RangedModRange=t['range_mod'])
    for n in range(1, 6):
        s = t[f'spellid_{n}']
        if s in ITEM_SPELL_REPL and 'spell' in ITEM_SPELL_REPL[s]:
            item_notes.append(f"{i} {t['name']}: spell {s} -> {ITEM_SPELL_REPL[s]['spell']} ({ITEM_SPELL_REPL[s]['note']})")
            s = ITEM_SPELL_REPL[s]['spell']
        elif s and (s in ITEM_SPELL_REPL or spell_conv(s)[0] != s):
            if s not in ITEM_SPELL_REPL:
                ns, why = spell_conv(s)
                item_notes.append(f"{i} {t['name']}: {why}")
                s = ns or 0
            else:
                s = 0
        r[f'spellid_{n}'] = s
        r[f'spelltrigger_{n}'] = t[f'spelltrigger_{n}'] if s else 0
        r[f'spellcharges_{n}'] = t[f'spellcharges_{n}'] if s else 0
        r[f'spellppmRate_{n}'] = t[f'spellppmrate_{n}'] if s else 0
        r[f'spellcooldown_{n}'] = t[f'spellcooldown_{n}'] if s else -1
        r[f'spellcategory_{n}'] = t[f'spellcategory_{n}'] if s else 0
        r[f'spellcategorycooldown_{n}'] = t[f'spellcategorycooldown_{n}'] if s else -1
    if i in MOUNT_BY_ITEM:
        # Turtle summons every mount through one spell (46499, Turtle-only): a 3.3.5 mount item teaches its mount instead
        # (Learning 55884 + the mount spell, trigger 6), as the stock mount items do
        ms_ = MOUNT_BY_ITEM[i]
        for n in (1, 2):
            r.update({f'spellid_{n}': (55884, ms_)[n - 1], f'spelltrigger_{n}': (0, 6)[n - 1], f'spellcharges_{n}': 0, f'spellppmRate_{n}': 0,
                      f'spellcooldown_{n}': -1, f'spellcategory_{n}': 0, f'spellcategorycooldown_{n}': -1})
        r.update(RequiredSkill=762, RequiredSkillRank=150 if t['quality'] >= 4 else 75)    # epic mounts are 100 % mounts in 3.3.5: journeyman riding
        item_notes.append(f"{i} {t['name']}: Turtle mount spell 46499 -> teaches 3.3.5 mount {ms_} {ASPELL_NAME.get(ms_, '?')} (riding {r['RequiredSkillRank']})")
    r.update(bonding=t['bonding'], description=t['description'] or '', PageText=page_ref(t['page_text']) if t['page_text'] else 0, LanguageID=t['page_language'],
             PageMaterial=t['page_material'], startquest=t['start_quest'] if t['start_quest'] in ac_qt or t['start_quest'] in owned['quest'] else 0,
             lockid=(lock_map(t['lock_id']) or 0) if t['lock_id'] else 0, Material=t['material'], sheath=t['sheath'],
             RandomProperty=t['random_property'], RandomSuffix=0, block=t['block'], itemset=0, MaxDurability=t['max_durability'], area=0, Map=0,
             BagFamily=BAG_FAMILY.get(t['bag_family'], 0), TotemCategory=0, socketColor_1=0, socketContent_1=0, socketColor_2=0, socketContent_2=0,
             socketColor_3=0, socketContent_3=0, socketBonus=0, GemProperties=0, RequiredDisenchantSkill=1 if t['disenchant_id'] else -1,
             ArmorDamageModifier=0, duration=t['duration'], ItemLimitCategory=0, HolidayId=0, ScriptName='', DisenchantID=t['disenchant_id'],
             FoodType=t['food_type'], minMoneyLoot=t['min_money_loot'], maxMoneyLoot=t['max_money_loot'], flagsCustom=0, VerifiedBuild=0)
    it_rows.append(r)
    idbc.append(dict(ID=I(i), ClassID=t['class'], SubclassID=t['subclass'], Sound_Override_Subclassid=-1, Material=t['material'],
                     DisplayInfoID=d, InventoryType=t['inventory_type'], SheatheType=t['sheath']))

il = in_list(I(i) for i in ported)
cont_rows = [loot_row(I(i), l_) for i in ported for l_ in cont_src.get(i, [])]
cont_rows = [r for r in cont_rows if (r['Reference'] and r['Reference'] not in empty_refs) or (not r['Reference'] and r['Item'] in item_ok)]
ref_lo, ref_hi = IDS['reference_loot_base'], IDS['reference_loot_base'] + 999999
common.raw(f"""-- ============================================================================
-- mod-turtle-content : shared data (items, item_dbc, reference loot)
-- Generated by tools/turtle2ac/build.py on {datetime.date.today()} - do not edit by hand.
-- ============================================================================
SET NAMES utf8mb4;
DELETE FROM `item_template` WHERE `entry` IN ({il});
DELETE FROM `item_dbc` WHERE `ID` IN ({il});
DELETE FROM `reference_loot_template` WHERE `Entry` BETWEEN {ref_lo} AND {ref_hi};
""")
common.comment('items'); common.insert('item_template', it_rows)
common.comment('server-side Item.dbc rows'); common.insert('item_dbc', idbc)
common.comment('reference loot (Turtle reference id + %d)' % ref_lo); common.insert('reference_loot_template', ref_rows)
if cont_rows:
    common.raw(f"DELETE FROM `item_loot_template` WHERE `Entry` IN ({in_list(sorted({r['Entry'] for r in cont_rows}))});\n")
    common.comment('contents of Turtle containers'); common.insert('item_loot_template', cont_rows)
# book / letter / plaque pages (items' PageText, text objects, goobers), whole next-page chains
page_rows, _seen = [], set()
_todo = sorted(pages_needed)
while _todo:
    pid = _todo.pop()
    if pid in _seen or pid in ac_page:
        continue
    _seen.add(pid)
    pr_ = q(f"select * from {TW}.page_text where entry=%s", pid)
    if not pr_:
        print(f'  ! page {pid} is referenced but not in Turtle page_text')
        continue
    page_rows.append(dict(ID=pid, Text=pr_[0]['text'], NextPageID=pr_[0]['next_page'], VerifiedBuild=0))
    if pr_[0]['next_page']:
        _todo.append(pr_[0]['next_page'])
page_rows.sort(key=lambda r: r['ID'])
pl = in_list(r['ID'] for r in page_rows)
common.raw(f"DELETE FROM `page_text` WHERE `ID` IN ({pl});\n")
common.comment('page text (books, letters, plaques)'); common.insert('page_text', page_rows)
gdi_rows = [dict(ID=nid, ModelName=path, **{f'Sound_{i + 1}': snd[i] for i in range(10)}, GeoBoxMinX=0, GeoBoxMinY=0, GeoBoxMinZ=0,
                 GeoBoxMaxX=0, GeoBoxMaxY=0, GeoBoxMaxZ=0, ObjectEffectPackageID=0) for nid, path, snd in sorted(go_new_disp.values())]
gdi_lo, gdi_hi = IDS['go_display_base'], IDS['go_display_base'] + 99999
common.raw(f"DELETE FROM `gameobjectdisplayinfo_dbc` WHERE `ID` BETWEEN {gdi_lo} AND {gdi_hi};\n")
common.comment('object models with no 3.3.5 display row (also in the client patch)'); common.insert('gameobjectdisplayinfo_dbc', gdi_rows)
# Turtle's factions / faction templates (see FMAP): server overrides of the client patch rows
fac_ids, ft_ids = in_list(sorted(FAC_ROWS)), in_list(sorted(FT_ROWS))
if FAC_ROWS:
    common.raw(f"DELETE FROM `faction_dbc` WHERE `ID` IN ({fac_ids});\n")
    common.comment("Turtle's factions (reputations; also in the client patch)")
    def _fac_srv(row_):
        # the server only reads the enUS strings; its other locale columns are short (Description_Lang_Unk: 100)
        d_ = srv_row('faction_dbc', row_)
        for c_ in d_:
            if c_.startswith(('Name_Lang_', 'Description_Lang_')) and not c_.endswith(('_enUS', '_Mask')):
                d_[c_] = ''
        d_['Description_Lang_enUS'] = d_['Description_Lang_enUS'][:300]
        return d_
    common.insert('faction_dbc', [_fac_srv(FAC_ROWS[k]) for k in sorted(FAC_ROWS)])
if FT_ROWS:
    common.raw(f"DELETE FROM `factiontemplate_dbc` WHERE `ID` IN ({ft_ids});\n")
    common.comment("Turtle's faction templates (also in the client patch)")
    common.insert('factiontemplate_dbc', [srv_row('factiontemplate_dbc', FT_ROWS[k]) for k in sorted(FT_ROWS)])

dropped_set = {I(i) for i in dropped}
owned_all_loot = {'lootid': owned['loot'], 'skinloot': owned['skin'], 'pickpocketloot': owned['pick']}   # loot id -> zone that exports it
sql_dir = os.path.join(ROOT, 'data', 'sql', 'db-world')
rb_dir = os.path.join(ROOT, 'sql_rollback')
os.makedirs(sql_dir, exist_ok=True); os.makedirs(rb_dir, exist_ok=True)
for d_ in (sql_dir, rb_dir):
    for f in os.listdir(d_):
        if 'mod_turtle_' in f:
            os.remove(os.path.join(d_, f))
open(os.path.join(sql_dir, 'mod_turtle_000_common.sql'), 'w').write(common.text())
quests_built = set(ac_qt) | set(owned['quest'])
# quest givers / turn-ins: every Turtle relation whose NPC or object exists in the end (built by any zone, or the same
# creature in 3.3.5), whichever zone was built first
_ac_go_name = {r['entry']: r['name'] for r in q(f"select entry, name from {AC}.gameobject_template")}
QUEST_NPC_SUB = {(int(qk), int(nk)): v for qk, m_ in CFG.get('quest_npc_substitutions', {}).items() if not qk.startswith('_') for nk, v in m_.items()}
_tw_names = {}
_qg_fixed = set()
for pr in pending_render:
    rows = pr['rows']
    pr['qg_fix'] = {}
    qs_ = [r['ID'] for r in rows.get('quest_template', [])]
    if not qs_:
        continue
    for tab_, tw_tab, kind in (('creature_queststarter', 'creature_questrelation', 'creature'), ('creature_questender', 'creature_involvedrelation', 'creature'),
                               ('gameobject_queststarter', 'gameobject_questrelation', 'gameobject'), ('gameobject_questender', 'gameobject_involvedrelation', 'gameobject')):
        keep = []
        for r in q(f"select r.id, r.quest, t.name from {TW}.{tw_tab} r join {TW}.{kind}_template t on t.entry=r.id where r.quest in ({in_list(qs_)})"):
            sub = QUEST_NPC_SUB.get((r['quest'], r['id'])) if kind == 'creature' else None
            if sub:
                keep.append(dict(id=sub, quest=r['quest']))
                next(x for x in all_reports if x['zone'] == pr['slug'])['notes']['quest_npc_stand_in'].append(
                    f"quest {r['quest']}: {r['name']} ({r['id']}) has no spawn in 3.3.5 - {ac_ct.get(sub)} ({sub}) stands in")
                continue
            if r['id'] in owned[kind] or (ac_ct if kind == 'creature' else _ac_go_name).get(r['id']) == r['name']:
                keep.append(dict(id=CREMAP.get(r['id'], r['id']) if kind == 'creature' else r['id'], quest=r['quest']))
        if {(x['id'], x['quest']) for x in keep} != {(x['id'], x['quest']) for x in rows.get(tab_, [])}:
            rows[tab_] = keep
    # 3.3.5 NPCs that give or take a Turtle quest but have no quest-giver flag there (e.g. Lord Falconcrest, Anduin)
    used_ = sorted({x['id'] for x in rows.get('creature_queststarter', []) + rows.get('creature_questender', [])
                    if x['id'] in ac_ct and x['id'] not in owned['creature'] and x['id'] not in _qg_fixed})
    pr['qg_fix'] = {}
    if used_:
        for r_ in q(f"select entry, npcflag from {AC}.creature_template where entry in ({in_list(used_)})"):
            if not r_['npcflag'] & 2:
                pr['qg_fix'][r_['entry']] = r_['npcflag']
                _qg_fixed.add(r_['entry'])
        if pr['qg_fix']:
            next(x for x in all_reports if x['zone'] == pr['slug'])['notes']['quest_giver_flag'].append(
                f"quest-giver flag added to 3.3.5 NPCs {sorted(pr['qg_fix'])} ({', '.join(ac_ct[e_] for e_ in sorted(pr['qg_fix']))})")
    for qid in qs_:
        if not any(x['quest'] == qid for x in rows.get('creature_queststarter', []) + rows.get('gameobject_queststarter', [])) and \
                not any(r['ID'] == qid and r.get('StartItem') for r in rows['quest_template']):
            if not q(f"select 1 from {TW}.item_template where start_quest=%s", qid):
                next(x for x in all_reports if x['zone'] == pr['slug'])['notes']['quest_no_giver'].append(f"quest {qid}: no quest giver in this build")
for pr in pending_render:
    rows = pr['rows']
    # chain links to quests that are not in this build (excluded, or in a zone not ported yet) would lock the rest of
    # the chain forever: drop the link so the quest is available on its own
    for r in rows.get('quest_template_addon', []):
        for k in ('PrevQuestID', 'NextQuestID'):
            if r[k] and abs(r[k]) not in quests_built:
                print(f"  quest {r['ID']}: {k} {r[k]} is not in this build - link removed")
                next(x for x in all_reports if x['zone'] == pr['slug'])['notes']['quest_chain'].append(
                    f"quest {r['ID']}: {k} {r[k]} is not in this build - link removed")
                r[k] = 0
    for r in rows.get('quest_template', []):
        if r['RewardNextQuest'] and r['RewardNextQuest'] not in quests_built:
            r['RewardNextQuest'] = 0
    for tname, key in (('creature_loot_template', 'Item'), ('skinning_loot_template', 'Item'), ('pickpocketing_loot_template', 'Item'),
                       ('gameobject_loot_template', 'Item'), ('npc_vendor', 'item')):
        before = len(rows.get(tname, []))
        rows[tname] = [r for r in rows.get(tname, []) if (r.get('Reference') and r['Reference'] not in empty_refs) or
                       (not r.get('Reference') and r[key] not in dropped_set)]
    # a loot table left empty by the filter above (all its items dropped) must not stay referenced
    for col_, tname in (('lootid', 'creature_loot_template'), ('skinloot', 'skinning_loot_template'), ('pickpocketloot', 'pickpocketing_loot_template')):
        have_ = {r['Entry'] for r in rows.get(tname, [])}
        for r in rows.get('creature_template', []):
            if r[col_] and r[col_] not in have_ and owned_all_loot[col_].get(r[col_]) == pr['slug']:
                next(x for x in all_reports if x['zone'] == pr['slug'])['notes']['loot'].append(
                    f"{r['entry']}: {col_} {r[col_]} lost all its items (Turtle-only items left out) - cleared")
                r[col_] = 0
    out = Sql()
    out.raw(pr['hdr'] + 'SET NAMES utf8mb4;\n' + pr['dels'])
    for tname in ORDER:
        if rows.get(tname):
            out.comment(tname)
            out.insert(tname, rows[tname])
    extra_dels = ''
    for tname, xrows in zone_sql[pr['slug']]:
        if not xrows:
            continue
        key = KEY_COL[tname]
        extra_dels += f"DELETE FROM `{tname}` WHERE `{key}` IN ({in_list(r[key] for r in xrows)});\n"
    if extra_dels:
        out.raw('\n-- maps, area triggers, graveyards, flight paths, room names, teleports\n' + extra_dels)
        for tname, xrows in zone_sql[pr['slug']]:
            if xrows:
                out.comment(tname)
                out.insert(tname, xrows)
    if pr['qg_fix']:
        out.raw('\n-- 3.3.5 NPCs that give or take this zone\'s quests: quest-giver flag (the rollback restores the original flags)\n'
                f"UPDATE `creature_template` SET `npcflag`=`npcflag`|2 WHERE `entry` IN ({in_list(sorted(pr['qg_fix']))});\n")
    if pr['go_fix']:
        out.raw('\n-- 3.3.5 fishing-hole templates with min opens > max opens (the core asserts on them); the rollback restores them\n'
                f"UPDATE `gameobject_template` SET `Data2`=2, `Data3`=6 WHERE `type`=25 AND `entry` IN ({in_list(sorted(pr['go_fix']))});\n")
    rb_flags = ''.join(f"UPDATE `creature_template` SET `npcflag`={v_} WHERE `entry`={e_};\n" for e_, v_ in sorted(pr['qg_fix'].items()))
    rb_flags += ''.join(f"UPDATE `gameobject_template` SET `Data2`={a_}, `Data3`={b_} WHERE `entry`={e_};\n" for e_, (a_, b_) in sorted(pr['go_fix'].items()))
    rb = f"-- Undo {pr['name']} ({pr['fname']})\n" + pr['dels'] + extra_dels + rb_flags + \
         f"DELETE FROM `creature_text` WHERE `CreatureID` IN ({pr['ce']});\n" + \
         f"DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid` IN ({pr['ce']});\n"
    mpy = os.path.join(HERE, 'manual', pr['slug'] + '.py')
    if os.path.exists(mpy):
        from lib.smartgen import Smart
        gm_ = guid_maps.get(pr['slug'], {})
        homes = {}
        for r_ in rows.get('creature', []):
            homes.setdefault(r_.get('id1', r_.get('id')), (r_['position_x'], r_['position_y'], r_['position_z'], r_['orientation']))

        def _gg(kind):
            def f(tw_guid):
                assert tw_guid in gm_.get(kind, {}), f"{pr['slug']}.py: Turtle {kind} guid {tw_guid} is not spawned"
                return gm_[kind][tw_guid]
            return f
        ctx = dict(q=q, TW=TW, AC=AC, spell=spell_conv, sound_ok=lambda s_: s_ in AC_SOUND, cguid=_gg('creature'), gguid=_gg('gameobject'),
                   home=lambda e_: homes[e_], item=lambda i_: ITEM_REMAP.get(i_, i_), cre_id=CRE_ID,
                   taxi_path=lambda p_: SCRIPTED_TAXI[p_])
        S_ = Smart(ctx)
        env = dict(S=S_, ctx=ctx)
        exec(compile(open(mpy).read(), mpy, 'exec'), env)
        stxt = env['SQL']
        out.raw('\n-- ---------------------------------------------------------------------------\n'
                f"-- Scripts from tools/turtle2ac/manual/{pr['slug']}.py\n" + stxt)
        rb += ''.join(l + '\n' for l in stxt.split('\n') if l.startswith('DELETE FROM'))
        rb += ''.join(l + '\n' for l in S_.rollback)
        for x_ in S_.notes:
            for rep_ in all_reports:
                if rep_['zone'] == pr['slug']:
                    rep_['notes'].setdefault('script_spells', []).append(x_)
    if pr['manual']:
        mtxt = manual_blocks(pr['manual'], pr['emitted'])
        gm = guid_maps.get(pr['slug'], {})

        def _guid(mo):
            kind = 'creature' if mo.group(1) == 'cguid' else 'gameobject'
            tw_guid = int(mo.group(2))
            assert tw_guid in gm.get(kind, {}), f"{pr['slug']}: manual SQL refers to Turtle {kind} guid {tw_guid}, which is not spawned"
            return str(gm[kind][tw_guid])
        mtxt = re.sub(r'\{(cguid|gguid):(\d+)\}', _guid, mtxt)
        out.raw('\n' + mtxt)
        for al in sorted(set(re.findall(r"\((\d+), 9, ", mtxt))):
            rb += f"DELETE FROM `smart_scripts` WHERE `source_type`=9 AND `entryorguid`={al};\n"
        rb += ''.join(l + '\n' for l in mtxt.split('\n') if l.startswith('DELETE FROM'))
    open(os.path.join(sql_dir, pr['fname']), 'w').write(out.text())
    rb += takeover_restore(r_['entry'] for r_ in rows.get('creature_template', []))
    open(os.path.join(rb_dir, 'undo_' + pr['fname']), 'w').write(rb)
open(os.path.join(rb_dir, 'undo_mod_turtle_000_common.sql'), 'w').write(
    f"DELETE FROM `item_template` WHERE `entry` IN ({il});\nDELETE FROM `item_dbc` WHERE `ID` IN ({il});\n"
    f"DELETE FROM `reference_loot_template` WHERE `Entry` BETWEEN {ref_lo} AND {ref_hi};\n"
    + (f"DELETE FROM `item_loot_template` WHERE `Entry` IN ({in_list(sorted({r['Entry'] for r in cont_rows}))});\n" if cont_rows else '')
    + f"DELETE FROM `page_text` WHERE `ID` IN ({pl});\n"
    f"DELETE FROM `gameobjectdisplayinfo_dbc` WHERE `ID` BETWEEN {gdi_lo} AND {gdi_hi};\n"
    + (f"DELETE FROM `faction_dbc` WHERE `ID` IN ({fac_ids});\n" if FAC_ROWS else '')
    + (f"DELETE FROM `factiontemplate_dbc` WHERE `ID` IN ({ft_ids});\n" if FT_ROWS else ''))

# =========================================================================== client patch
from lib.mkmpq import make
from lib import wmo as wmolib
tmp = os.path.join(HERE, '.build', 'DBFilesClient')
if os.path.isdir(os.path.join(HERE, '.build')):
    shutil.rmtree(os.path.join(HERE, '.build'))
os.makedirs(tmp)
patch_files = []

# Item.dbc: the client's copy + ported items
it_tbl = CT('Item')
for x in idbc:
    it_tbl.add([x['ID'], x['ClassID'], x['SubclassID'], -1, x['Material'], x['DisplayInfoID'], x['InventoryType'], x['SheatheType']], replace=True)
# AreaTable.dbc: + new zones/subzones
for r in client_areas:
    assert CT('AreaTable').get(r[0]) is None, f'area {r[0]} already in the client AreaTable'
    CT('AreaTable').add(r)
# GameObjectDisplayInfo.dbc: + display rows for Turtle object models
for nid, path, snd in go_new_disp.values():
    CT('GameObjectDisplayInfo').add([nid, path] + snd + [0.0] * 6 + [0])

# tile fixes (config tile_fixes; Max's fixes 2026-10-09): placements dropped, terrain textures replaced
from lib import adtmerge
_tf = CFG.get('tile_fixes', {})
_rm = {k.lower(): set(v) for k, v in _tf.get('remove_placements', {}).items() if not k.startswith('_')}
_ts = {k.lower(): v for k, v in _tf.get('texture_substitutions', {}).items() if not k.startswith('_')}
_ts.update({k.replace('\\', '/'): v for k, v in list(_ts.items())})        # Turtle tiles name textures with / too
_tf_log = []
for i_, (ap_, data, mid) in enumerate(client_tiles):
    t_ = adtmerge.Tile(data)
    drop_ = _rm.get(ap_.lower(), set())
    hit_ = drop_ & {struct.unpack_from('<I', r_, 4)[0] for r_ in t_.mddf + t_.modf}
    tx_ = [n_ for n_ in t_.mtex if n_.lower() in _ts]
    if hit_ or tx_:
        xy_ = tuple(int(v_) for v_ in ap_[:-4].split('_')[-2:])
        data = adtmerge.rewrite(data, xy_, drop_uids=hit_, tex_sub=_ts)
        from lib.adt import mcnk_problems
        assert not mcnk_problems(data), ap_
        client_tiles[i_] = (ap_, data, mid)
        _tf_log.append(f"{ap_.split(chr(92))[-1]}: {len(hit_)} placements dropped, {len(tx_)} textures replaced")
for k_ in _rm:
    assert any(a_.lower() == k_ for a_, _, _ in client_tiles), f'tile_fixes: {k_} is not shipped'
if _tf_log:
    print('tile fixes:', '; '.join(_tf_log))
# sea floor (Max, 2026-10-09): stock -516 open-sea chunks left next to a Turtle island (and 3.3.5 chunks whose edge was raised
# onto a Turtle neighbour) are pits far below Turtle's sea floor: dark squares in the water and a server ground of -500.
# Those chunks take Turtle's own server heights (TWoW Data\maps), their edges meet the unchanged chunks next to them, and
# their MH2O depth follows the new ground (3.3.5's 1.72 per yard).
_sb = CFG.get('tile_fixes', {}).get('seabed_from_turtle_server', {})
if _sb.get('enabled', True):
    from lib.terrain import read_tw_grid
    _sb_tiles, _sb_changed, _sb_idx = {}, {}, {}
    for i_, (ap_, data, mid) in enumerate(client_tiles):
        wn_ = ap_.split('\\')[2]
        xy_ = tuple(int(v_) for v_ in ap_[:-4].split('_')[-2:])
        _sb_idx[(wn_,) + xy_] = (i_, mid)
        g_ = read_tw_grid(CFG['tw_maps'], mid, *xy_)
        if g_ is None:
            continue
        t_ = adtmerge.Tile(data)
        skip_ = set(_sb.get('skip_chunks', {}).get(ap_.split('\\')[-1][:-4], []))
        pits_ = [c_ for c_ in adtmerge.sea_pits(t_, g_, _sb.get('deeper_than', 30.0)) if c_ not in skip_]
        if pits_:
            for c_ in pits_:
                adtmerge.set_heights(t_, c_, adtmerge.grid_chunk(g_, c_))
            _sb_tiles[(wn_,) + xy_] = t_
            _sb_changed[(wn_,) + xy_] = set(pits_)
    _sb_moved = 0
    for wn_ in sorted({k_[0] for k_ in _sb_tiles}):
        def _sb_other(X, Y, wn_=wn_):
            k_ = (wn_, X, Y)
            if k_ in _sb_idx:
                return adtmerge.Tile(client_tiles[_sb_idx[k_][0]][1])
            b_ = client335_file(f'World\\Maps\\{wn_}\\{wn_}_{X}_{Y}.adt')
            return adtmerge.Tile(open(b_, 'rb').read()) if b_ and os.path.exists(b_) else None
        tl_ = {k_[1:]: v_ for k_, v_ in _sb_tiles.items() if k_[0] == wn_}
        ch_ = {k_[1:]: v_ for k_, v_ in _sb_changed.items() if k_[0] == wn_}
        mv_, worst_ = adtmerge.stitch_to_neighbours(tl_, ch_, functools.lru_cache(None)(_sb_other))
        _sb_moved += mv_
    for k_, t_ in _sb_tiles.items():
        for c_ in _sb_changed[k_]:
            adtmerge.set_water_depth(t_, c_, _sb.get('depth_per_yard', 1.72), CFG.get('tile_fixes', {}).get('dark_water_below', -60.0))
        i_, mid = _sb_idx[k_]
        data = adtmerge.merge(t_, t_, set(), k_[1:])
        from lib.adt import mcnk_problems
        assert not mcnk_problems(data), client_tiles[i_][0]
        client_tiles[i_] = (client_tiles[i_][0], data, mid)
    print(f"sea floor: {sum(map(len, _sb_changed.values()))} chunks on {len(_sb_tiles)} tiles from Turtle's server heights "
          f"({_sb_moved} edge vertices matched): " + ', '.join(f"{k_[0]}_{k_[1]}_{k_[2]} {len(v_)}" for k_, v_ in sorted(_sb_changed.items())))
# dark water (Max, 2026-10-09): Turtle water flagged "deep" right off the beach made the server's .map dark water (Fatigue
# a few yards from the shore). The flag is kept only where the ground is below dark_water_below (open sea).
_dw_lim = CFG.get('tile_fixes', {}).get('dark_water_below', -60.0)
_dw_n, _dw_t = 0, 0
for i_, (ap_, data, mid) in enumerate(client_tiles):
    t_ = adtmerge.Tile(data)
    b_ = client335_file(ap_)
    n_ = adtmerge.fix_dark_water(t_, adtmerge.Tile(open(b_, 'rb').read()) if b_ else None, _dw_lim)
    if n_:
        xy_ = tuple(int(v_) for v_ in ap_[:-4].split('_')[-2:])
        data = adtmerge.merge(t_, t_, set(), xy_)
        from lib.adt import mcnk_problems
        assert not mcnk_problems(data), ap_
        client_tiles[i_] = (ap_, data, mid)
        _dw_n += n_
        _dw_t += 1
print(f'dark water: {_dw_n} cells on {_dw_t} tiles no longer deep (ground above {_dw_lim})')
# grass (Max, 2026-10-09): Turtle's ground-effect rows are empty in the 3.3.5 client (no clutter on the new zones), untagged
# dirt layers get rows of their own, and cells under water or whose most visible texture is a road or sand get no clutter.
_ge = CFG.get('ground_effects', {})
if _ge.get('rows'):
    from lib import grass
    _get = CT('GroundEffectTexture')
    _gdd = CT('GroundEffectDoodad')
    _gdd_by_name = {}
    for i_, r_ in _gdd.rows.items():
        _gdd_by_name.setdefault(os.path.splitext(r_[1].lower())[0], i_)
    _tw_get, _ = tw_dbc('GroundEffectTexture')
    _n_, _f_, _rs_, _tw_gdd_rows, _tw_gdd_s, _ = load(CFG['tw_dbc'] + '/GroundEffectDoodad.dbc')
    _tw_gdd = {r_[0]: _tw_gdd_s(r_[2]) for r_ in _tw_gdd_rows}
    _ge_log = []
    for k_, spec_ in sorted(_ge['rows'].items()):
        if k_.startswith('_'):
            continue
        id_ = int(k_)
        old_ = _get.get(id_)
        if 'copy' in spec_:
            src_ = _get.get(spec_['copy'])
            assert src_, f"ground_effects {id_}: stock row {spec_['copy']} not in the client table"
            dd_, tt_ = list(src_[1:5]), src_[10]
        elif 'doodads' in spec_:
            dd_, tt_ = list(spec_['doodads']), spec_.get('terrain', old_[10] if old_ else 0)
        else:                                   # Turtle's own doodads, matched to the 3.3.5 models by name
            tw_ = _tw_get[id_]
            dd_ = []
            for d_ in tw_[1:5]:
                nm_ = os.path.splitext(_tw_gdd.get(d_, '').lower())[0]
                if nm_ in _gdd_by_name and _gdd_by_name[nm_] not in dd_:
                    dd_.append(_gdd_by_name[nm_])
            assert dd_, f'ground_effects {id_}: no Turtle doodad model of this row exists in the 3.3.5 client'
            dd_ += [dd_[0]] * (4 - len(dd_))
            tt_ = spec_.get('terrain', old_[10] if old_ else tw_[6])      # footstep terrain type: the client's own
        for d_ in dd_:
            assert d_ in _gdd.rows, f'ground_effects {id_}: GroundEffectDoodad {d_} not in the client table'
        _get.add([id_] + dd_ + [1, 1, 1, 1, spec_['density'], tt_], replace=bool(old_))
        _ge_log.append(f"{id_}{'' if old_ else ' (new)'}")
    print('ground effects:', ', '.join(_ge_log))
    # zone of a chunk's area id
    _tw_parent = {r_[0]: r_[2] for r_ in tw_area}
    _unremap = {v_: k_ for k_, v_ in AREA_REMAP.items()}

    def _zone_of(a_):
        a_ = _unremap.get(a_, a_)
        for _ in range(4):
            p_ = _tw_parent.get(a_, 0)
            if not p_:
                return a_
            a_ = p_
        return a_
    _zone_ids = {sl_: json.load(open(os.path.join(HERE, 'zones', sl_ + '.json')))['zone_id'] for sl_ in CFG['zones']}
    _rules = []
    for r_ in _ge.get('retag', []):
        _rules.append(({_zone_ids[z_] for z_ in r_['zones']}, r_['texture'].lower(), set(r_['from']), r_['to']))
    _nc = _ge.get('no_clutter', {})
    _road, _sand, _sand_not = _nc.get('road', []), _nc.get('sand', []), _nc.get('sand_not', [])
    _above = _nc.get('water_above', 0.2)
    _tot = collections.Counter()
    for i_, (ap_, data, mid) in enumerate(client_tiles):
        t_ = adtmerge.Tile(data)
        b_ = client335_file(ap_)
        base_ = adtmerge.Tile(open(b_, 'rb').read()) if b_ and os.path.exists(b_) else None
        hit_ = False
        for c_ in range(256):
            if base_ is not None and grass.same_ground(t_, c_, base_):
                continue
            _tot['chunks'] += 1
            z_ = _zone_of(t_.area(c_))
            rl_ = [(tx_, fr_, to_) for zs_, tx_, fr_, to_ in _rules if z_ in zs_]
            if rl_:
                n_ = grass.retag(t_, c_, rl_)
                _tot['layers retagged'] += n_
                hit_ |= bool(n_)
            w_, r_, s_ = grass.no_clutter(t_, c_, _road, _sand, _sand_not, _above)
            _tot['water cells'] += w_
            _tot['road cells'] += r_
            _tot['sand cells'] += s_
            hit_ |= bool(w_ or r_ or s_)
        if hit_:
            data = adtmerge.merge(t_, t_, set(), tuple(int(v_) for v_ in ap_[:-4].split('_')[-2:]))
            from lib.adt import mcnk_problems
            assert not mcnk_problems(data), ap_
            client_tiles[i_] = (ap_, data, mid)
    print('grass:', ', '.join(f'{v_} {k_}' for k_, v_ in _tot.items()))
# client tables (after the tile passes: the grass pass fills GroundEffectTexture rows)
for name, tbl in sorted(_CT.items()):
    if tbl.added:
        patch_files.append((tbl.save(os.path.join(tmp, name + '.dbc')), f'DBFilesClient\\{name}.dbc'))
print('client tables:', ', '.join(f"{n} +{len(t.added)}" for n, t in sorted(_CT.items()) if t.added))
if ASSETS.not_shipped:
    print('not shipped (never_ship):', sorted(ASSETS.not_shipped))

# map tiles
adt_dir = os.path.join(HERE, '.build', 'adt')
for ap_, data, mid in client_tiles:
    lp = os.path.join(adt_dir, *ap_.split('\\'))
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    open(lp, 'wb').write(data)
    patch_files.append((lp, ap_))

# WDTs: tiles the 3.3.5 client does not know are added to its copy of the continent WDT
wdt_out = {}
for wname, tl in wdt_tiles.items():
    key = f"World\\Maps\\{wname}\\{wname}.wdt"
    base = client335_file(key)
    if not base:
        continue                                       # a map this build adds: its own WDT is shipped (ship_wdt)
    b = bytearray(open(base, 'rb').read())
    p_ = 0
    while p_ + 8 <= len(b):
        tag = bytes(b[p_:p_ + 4][::-1])
        sz = struct.unpack_from('<I', b, p_ + 4)[0]
        if tag == b'MAIN':
            main_off = p_ + 8
        p_ += 8 + sz
    added = []
    for x_, y_ in sorted(tl):
        o_ = main_off + (y_ * 64 + x_) * 8
        if not struct.unpack_from('<I', b, o_)[0] & 1:
            struct.pack_into('<I', b, o_, struct.unpack_from('<I', b, o_)[0] | 1)
            added.append(f'{x_}_{y_}')
    if added:
        lp = os.path.join(HERE, '.build', wname + '.wdt')
        open(lp, 'wb').write(b)
        patch_files.append((lp, key))
        wdt_out[wname] = added
        print(f'{wname}.wdt: tiles added {added}')

# minimap (Max, 2026-10-09): every tile with new-zone ground gets its own image, shipped as Textures\Minimap\<Dir>\mapX_Y.blp
# with a trs line naming it after itself, in its directory's block of the client's full md5translate.trs. Tiles that mix a
# new zone with stock land are composed per chunk: new-zone and water chunks from Turtle's image, stock dry land from the
# stock 3.3.5 image (stock zones keep their picture). Tiles without new-zone ground keep the stock image.
trs_key = 'Textures\\Minimap\\md5translate.trs'
if client335_file(trs_key) and (client_tiles or ship_files):
    from lib import minimap as mmlib
    from lib import grass as _grass
    tw_trs = {}
    for line in open(os.path.join(CFG['tw_client_assets'], *trs_key.split('\\')), encoding='latin-1'):
        parts = line.rstrip('\r\n').split('\t')
        if len(parts) == 2:
            tw_trs[parts[0].lower()] = parts
    trs = mmlib.Trs(open(client335_file(trs_key), encoding='latin-1').read())
    stock_mm = trs.entries()
    sea = stock_mm.get('azeroth\\map25_47.blp', (None, None))[1]       # 3.3.5 open-sea minimap image

    def _stock_img(plain):
        e_ = stock_mm.get(plain.lower())
        f_ = client335_file('Textures\\Minimap\\' + e_[1]) if e_ else None
        return open(f_, 'rb').read() if f_ and os.path.exists(f_) else None

    def _has_water(t_, i_):
        if t_.water[i_] and t_.water[i_][1]:
            return True
        o_, sz_ = struct.unpack_from('<II', t_.mcnk[i_], 0x60)
        return bool(o_ and sz_ > 8)
    mm_stats, mm_no_image = collections.Counter(), []
    for ap_, data, mid in client_tiles:
        wname = ap_.split('\\')[2]
        x_, y_ = ap_[:-4].split('_')[-2:]
        plain = f'{wname}\\map{x_}_{y_}.blp'
        t_ = adtmerge.Tile(data)
        b_ = client335_file(ap_)
        base_ = adtmerge.Tile(open(b_, 'rb').read()) if b_ and os.path.exists(b_) else None
        if base_ is None:
            new_ = set(range(256))
        else:
            new_ = {i_ for i_ in range(256) if not _grass.same_ground(t_, i_, base_)}
            if not new_:
                mm_stats['stock ground, stock image kept'] += 1
                continue
        tw_ = tw_trs.get(plain.lower())
        if tw_ and tw_[1].lower() == '_sea.blp':
            if base_ is None and sea:
                trs.set(plain, sea)
                mm_stats['open sea (stock sea image)'] += 1
            else:
                mm_stats['Turtle shows open sea, stock image kept'] += 1
            continue
        src_ = ASSETS.local.get(('textures\\minimap\\' + tw_[1]).lower()) if tw_ and tw_[1].lower() != '_void.blp' else None
        if not src_:
            mm_no_image.append(plain)
            continue
        turtle_ch = new_ | {i_ for i_ in range(256) if _has_water(t_, i_)}
        simg = _stock_img(plain) if base_ is not None else None
        if base_ is None or len(turtle_ch) == 256:
            ship_files['Textures\\Minimap\\' + plain] = src_
            mm_stats['Turtle image'] += 1
        elif simg is None:
            ship_files['Textures\\Minimap\\' + plain] = src_
            mm_stats['Turtle image (no stock image in the client335 extract)'] += 1
        else:
            rgb_ = mmlib.compose(mmlib.load_rgb(simg), mmlib.load_rgb(open(src_, 'rb').read()), turtle_ch)
            ship_files['Textures\\Minimap\\' + plain] = mmlib.blp_dxt1(rgb_)
            mm_stats['composed (Turtle + stock chunks)'] += 1
        mm_stats['trs lines ' + trs.set(plain, plain)] += 1
    # dungeon room maps of the Turtle buildings the patch ships: Turtle's images under their own names
    wmo_stems = {os.path.splitext(w.lower())[0][len('world\\'):] + '_' for w in ship_files
                 if w.lower().startswith('world\\wmo\\') and w.lower().endswith('.wmo') and not w[-8:-4].lstrip('_').isdigit()}
    for k_ in sorted(k_ for k_ in tw_trs if any(k_.startswith(st) for st in wmo_stems)):
        plain, target = tw_trs[k_]
        src_ = ASSETS.local.get(('textures\\minimap\\' + target).lower())
        if not src_:
            continue
        ship_files['Textures\\Minimap\\' + target] = src_
        mm_stats['room maps'] += 1
        trs.set(plain, target)
    lp = os.path.join(HERE, '.build', 'md5translate.trs')
    open(lp, 'w', encoding='latin-1', newline='').write(trs.text())
    patch_files.append((lp, trs_key))
    print('minimap:', ', '.join(f'{v_} {k_}' for k_, v_ in mm_stats.items()))
    if mm_no_image:
        print(f'NOTE: no Turtle minimap image for {len(mm_no_image)} new-zone tiles (left as they are):', mm_no_image)

# Turtle buildings, textures, world map art, WDTs
blob_dir = os.path.join(HERE, '.build', 'files')
for ap_, src_ in sorted(ship_files.items()):
    if isinstance(src_, (bytes, bytearray)):
        lp = os.path.join(blob_dir, *ap_.split('\\'))
        os.makedirs(os.path.dirname(lp), exist_ok=True)
        open(lp, 'wb').write(src_)
        src_ = lp
    patch_files.append((src_, ap_))
seen_ap = set()
for lp, ap_ in patch_files:
    assert ap_.lower() not in seen_ap, f'{ap_} twice in the client patch'
    seen_ap.add(ap_.lower())
# ---- pre-ship checks on the client patch (each of these once crashed or broke the live client)
ship_err = []
for lp, ap_ in patch_files:
    low = ap_.lower()
    blob = open(lp, 'rb').read()
    if low.endswith('.adt'):                     # client-style MCNK walk (orphan MCLQ -> crash #132)
        from lib.adt import mcnk_problems
        ship_err += [f'{ap_}: {x}' for x in mcnk_problems(blob)[:3]]
    elif low.endswith('.wmo') and re.search(r'_\d{3}\.wmo$', low):    # WMO group: liquid type must match the root flag
        root_ = re.sub(r'_\d{3}\.wmo$', '.wmo', low)
        rsrc = next((l_ for l_, a_ in patch_files if a_.lower() == root_), None)
        if rsrc:
            cur_, want_ = wmolib.group_liquid_wanted(wmolib.root_flags(open(rsrc, 'rb').read()), blob)
            if cur_ != want_:
                ship_err.append(f'{ap_}: groupLiquid {cur_}, expected {want_} (lava/water filling the building)')
for name, tbl in sorted(_CT.items()):
    if not tbl.added:
        continue
    try:
        tbl.sorted_ids()                          # stock row order kept (AreaTrigger by map: portals)
    except AssertionError as e_:
        ship_err.append(str(e_))
    if name == 'LoadingScreens':                  # every loading screen the module adds is in the patch
        for i_ in tbl.added:
            row_ = tbl.get(i_)
            need_ = [row_[2]] + ([row_[2][:-4] + 'Wide.blp'] if row_[3] else [])
            for f_ in need_:
                if f_.lower() not in seen_ap:
                    ship_err.append(f'LoadingScreens {i_}: {f_} is not in the client patch')
assert not ship_err, 'client patch checks failed:\n  ' + '\n  '.join(ship_err[:30])
# what the patch was built against: client/check_client.py compares the player's client with this
os.makedirs(os.path.join(ROOT, 'client'), exist_ok=True)
json.dump(dict(
    patch=CFG['client_patch_name'],
    tables={n: dict(archive=CT_BASE[n][0], md5=hashlib.md5(open(CT_BASE[n][1], 'rb').read()).hexdigest())
            for n, t in sorted(_CT.items()) if t.added},
    files=sorted(a_ for _, a_ in patch_files),
    based_on={k_: dict(archive=client335_archive(k_), md5=hashlib.md5(open(client335_file(k_), 'rb').read()).hexdigest())
              for k_ in sorted(a_ for _, a_ in patch_files)       # merged copies of client files (WDT, minimap index); tiles replace theirs on purpose
              if k_.lower().endswith(('.wdt', '.trs')) and client335_archive(k_) and os.path.exists(client335_file(k_))},
), open(os.path.join(ROOT, 'client', 'client_tables.json'), 'w'), indent=1)
os.makedirs(os.path.join(ROOT, 'client'), exist_ok=True)
make(os.path.join(ROOT, 'client', CFG['client_patch_name']), patch_files)
print(f"client patch: {len(patch_files)} files, {os.path.getsize(os.path.join(ROOT, 'client', CFG['client_patch_name'])) / 1e6:.1f} MB")
if ASSETS.missing:
    print('NOTE: Turtle files referenced but not in the extract folder:', len(ASSETS.missing), sorted(ASSETS.missing)[:20])
print(f'WMO groups whose liquid type was corrected (Turtle MOHD flag 0x4 + groupLiquid 15 = lava): {ASSETS.liquid_fixed}')
if ASSETS.unchecked_groups:
    print('NOTE: Turtle WMO roots with the liquid-type flag whose groups are 3.3.5 originals (check in game for lava):',
          sorted(ASSETS.unchecked_groups)[:20])
    json.dump(sorted(ASSETS.missing), open(os.path.join(HERE, 'reports', 'missing_assets.json'), 'w'), indent=1)

# server .map files for the tiles, made with AzerothCore's own map_extractor from a minimal client
smaps = os.path.join(ROOT, 'server-data', 'maps')
if os.path.isdir(smaps):
    shutil.rmtree(smaps)
if client_tiles:
    fc = os.path.join(HERE, '.build', 'fakeclient')
    if os.path.isdir(fc):
        shutil.rmtree(fc)
    os.makedirs(os.path.join(fc, 'Data', 'enUS'))
    os.makedirs(os.path.join(fc, 'out'))
    comp = os.path.join(fc, 'component.txt')
    open(comp, 'w').write('<componentinfo>\n<component name="WoW" version="12340" />\n</componentinfo>\n')
    map_dbc = os.path.join(tmp, 'Map.dbc') if os.path.exists(os.path.join(tmp, 'Map.dbc')) else client335_file('DBFilesClient\\Map.dbc')
    files = [(comp, 'component.wow-enUS.txt'), (map_dbc, 'DBFilesClient\\Map.dbc'),
             (CFG['ac_dbc'] + '/LiquidType.dbc', 'DBFilesClient\\LiquidType.dbc')]
    by_map = collections.defaultdict(list)
    for ap_, data, mid in client_tiles:
        by_map[ap_.split('\\')[2]].append(ap_)
        files.append((os.path.join(adt_dir, *ap_.split('\\')), ap_))
    for wname, tl in by_map.items():
        main = bytearray(64 * 64 * 8)
        for ap_ in tl:
            x, y = map(int, ap_[:-4].split('_')[-2:])
            struct.pack_into('<II', main, (y * 64 + x) * 8, 1, 0)
        ch = lambda tag, b: tag[::-1] + struct.pack('<I', len(b)) + bytes(b)
        wp = os.path.join(fc, wname + '.wdt')
        open(wp, 'wb').write(ch(b'MVER', struct.pack('<I', 18)) + ch(b'MPHD', bytes(32)) + ch(b'MAIN', main) + ch(b'MWMO', b''))
        files.append((wp, f"World\\Maps\\{wname}\\{wname}.wdt"))
    make(os.path.join(fc, 'Data', 'enUS', 'locale-enUS.MPQ'), files)
    # relative paths: the extractor truncates long paths (MAX_PATH_LENGTH)
    r = subprocess.run([CFG['map_extractor'], '-i', '..', '-o', '.', '-e', '1'], cwd=os.path.join(fc, 'out'),
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert r.returncode == 0, 'map_extractor failed: ' + r.stderr.decode(errors='replace')[-500:]
    os.makedirs(smaps)
    got = sorted(os.listdir(os.path.join(fc, 'out', 'maps')))
    assert len(got) == len(client_tiles), f'expected {len(client_tiles)} map tiles, got {got}'
    for g in got:
        shutil.copy(os.path.join(fc, 'out', 'maps', g), smaps)
    json.dump(dict(maps=got, tiles=[(ap_, mid) for ap_, _, mid in client_tiles]), open(os.path.join(ROOT, 'server-data', 'tiles.json'), 'w'), indent=1)
    print(f"server maps: {len(got)} tiles")
    # assets the tiles and the new object displays use, checked against the 3.3.5 client by server-data/install_server_data.py
    from lib.adt import top_chunks
    req = set()
    for ap_, data, mid in client_tiles:
        for t_, o_, s_ in top_chunks(data):
            if t_ in ('MTEX', 'MMDX', 'MWMO'):
                req |= {x.decode('latin-1').replace('/', '\\') for x in data[o_:o_ + s_].split(b'\0') if x}
    req |= {path for nid, path, snd in go_new_disp.values()}
    open(os.path.join(ROOT, 'server-data', 'required_assets.txt'), 'w').write('\n'.join(sorted(req, key=str.lower)) + '\n')

# =========================================================================== reports
os.makedirs(os.path.join(HERE, 'reports'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'docs', 'zones'), exist_ok=True)
common_rep = dict(items=len(it_rows), reference_rows=len(ref_rows), items_dropped=dropped, item_notes=item_notes, factions=FAC_NOTES)
json.dump(common_rep, open(os.path.join(HERE, 'reports', 'common.json'), 'w'), indent=1)
idx = ['# Zones in mod-turtle-content\n', '| Zone ID | Zone | File | Terrain | NPCs | Spawns | Quests | Objects | Held back (client patch) |', '|---|---|---|---|---|---|---|---|---|']
for rep in all_reports:
    json.dump(rep, open(os.path.join(HERE, 'reports', rep['zone'] + '.json'), 'w'), indent=1, default=str)
    c = rep['counts']
    idx.append(f"| {rep['zone'][:3]} | {rep['name']} | `{rep['file']}` | {rep['terrain']} | {c.get('creature_template', 0)} | {c.get('creature', 0)} | "
               f"{c.get('quest_template', 0)} | {c.get('gameobject', 0)} | {len(rep['go_pending'])} prop types |")
    md = [f"# {rep['name']}\n", f"File: `data/sql/db-world/{rep['file']}`  ", f"Terrain mode: **{rep['terrain']}**\n", '## Counts\n']
    md += [f"- {k}: {v}" for k, v in sorted(c.items())]
    for k, v in rep['notes'].items():
        md.append(f"\n## {k.replace('_', ' ').capitalize()} ({len(v)})\n")
        md += [f"- {x}" for x in v[:400]]
    if rep['go_pending']:
        md.append(f"\n## Objects waiting for the client patch ({len(rep['go_pending'])})\n")
        md += [f"- {p['entry']} {p['name'][:70]} - `{p['model']}`" for p in rep['go_pending']]
    open(os.path.join(ROOT, 'docs', 'zones', rep['zone'] + '.md'), 'w').write('\n'.join(md) + '\n')
idx.append(f"\nShared: {len(it_rows)} items, {len(ref_rows)} reference-loot rows in `mod_turtle_000_common.sql`.")
open(os.path.join(ROOT, 'docs', 'ZONES.md'), 'w').write('\n'.join(idx) + '\n')
for rep in all_reports:
    print(rep['zone'], rep['counts'])
print('common', {k: (len(v) if isinstance(v, list) else v) for k, v in common_rep.items()})
missing = twmaps.missing | acmaps.missing
if missing:
    print('NOTE: map tiles not available (heights unchecked there):', sorted(missing)[:20])
