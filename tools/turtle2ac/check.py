#!/usr/bin/env python3
"""Validate mod-turtle-content after it was applied to a world database.

    python3 check.py <database>

Checks every reference the module makes (displays, spells, items, quests, loot, gossip, locks)
against that database and the server DBCs in config.json. Exit code 1 on problems.
"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pymysql
from lib.dbc import load

CFG = json.load(open(os.path.join(HERE, 'config.json')))
DB = sys.argv[1]
G0, G1 = CFG['ids']['guid_base'], CFG['ids']['guid_base'] + 900000
ids = lambda name: {r[0] for r in load(CFG['ac_dbc'] + '/' + name)[3]}
CDI, GDI, LOCK, ITEMDBC, SPELL, FT = (ids('CreatureDisplayInfo.dbc'), ids('GameObjectDisplayInfo.dbc'), ids('Lock.dbc'),
                                      ids('Item.dbc'), ids('Spell.dbc'), ids('FactionTemplate.dbc'))
FACTIONS = ids('Faction.dbc')
c = pymysql.connect(unix_socket=CFG['db'].get('unix_socket'), user=CFG['db']['user'], password=CFG['db']['password'], database=DB).cursor()


def col(sql):
    c.execute(sql)
    return [r[0] for r in c.fetchall()]


bad = collections.defaultdict(list)
# creature.id (Grimfeather and older cores) or creature.id1 (upstream AzerothCore)
CID = 'id1' if 'id1' in col(f"select column_name from information_schema.columns where table_schema='{DB}' and table_name='creature'") else 'id'
GDI |= set(col("select ID from gameobjectdisplayinfo_dbc"))      # server-side DBC overrides count too
AREAS = ids('AreaTable.dbc') | set(col("select ID from areatable_dbc"))
CRE = f"(select {CID} from creature where guid between {G0} and {G1})"
GOS = f"(select id from gameobject where guid between {G0} and {G1})"
cre = set(col(f"select distinct {CID} from creature where guid between {G0} and {G1}"))
mod_cre = set(col(f"select entry from creature_template where entry in {CRE} or entry in (select RequiredNpcOrGo1 from quest_template where ID in (select quest from creature_queststarter where id in {CRE}))"))
items = set(col("select entry from item_template"))
tpl = set(col("select entry from creature_template"))
ctext = set(col("select ID from npc_text"))

for d in col(f"select CreatureDisplayID from creature_template_model where CreatureID in {CRE}"):
    if d not in CDI: bad['creature display not in CreatureDisplayInfo.dbc'].append(d)
for e in cre - tpl: bad['spawn without template'].append(e)
FT_DB = set(col("select ID from factiontemplate_dbc"))      # the module's own templates (Turtle's factions) are server rows
for f in col(f"select distinct faction from creature_template where entry in {CRE}"):
    if f not in FT and f not in FT_DB: bad['faction template missing'].append(f)
FAC_DB = set(col("select ID from faction_dbc"))
for f in col(f"select faction from factiontemplate_dbc where ID >= {CFG['ids']['faction_template_base']}"):
    if f not in FAC_DB and f not in FACTIONS: bad['faction template of a missing faction'].append(f)
for d in col(f"select displayId from gameobject_template where entry in {GOS}"):
    if d not in GDI: bad['gameobject display not in GameObjectDisplayInfo.dbc'].append(d)
for d in col(f"select Data0 from gameobject_template where type in (3,10) and entry in {GOS}"):
    if d and d not in LOCK: bad['lock missing'].append(d)
for b in col("select AreaBit from areatable_dbc"):
    if b >= 4096: bad['area exploration bit out of range'].append(b)
_bits = {r[3]: r[0] for r in load(CFG['ac_dbc'] + '/AreaTable.dbc')[3]}
c.execute("select ID, AreaBit, ParentAreaID from areatable_dbc")
for aid, bit, par in c.fetchall():
    if bit in _bits and _bits[bit] != aid: bad['area exploration bit already used'].append((aid, bit, _bits[bit]))
    if par and par not in AREAS: bad['area parent missing'].append((aid, par))
QS = col(f"select quest from creature_queststarter where id in {CRE}")
QL = ','.join(map(str, QS)) or 'NULL'
c.execute(f"select ID,RequiredNpcOrGo1,RequiredNpcOrGo2,RequiredNpcOrGo3,RequiredNpcOrGo4 from quest_template where ID in ({QL})")
for r in c.fetchall():
    for n in r[1:]:
        if n > 0 and n not in tpl: bad['quest objective creature missing'].append((r[0], n))
for r in col(f"select concat_ws(',',RequiredItemId1,RequiredItemId2,RequiredItemId3,RequiredItemId4,RewardItem1,RewardItem2,RewardItem3,RewardItem4,"
             f"RewardChoiceItemID1,RewardChoiceItemID2,RewardChoiceItemID3,RewardChoiceItemID4,RewardChoiceItemID5,RewardChoiceItemID6,ItemDrop1,ItemDrop2,StartItem) from quest_template where ID in ({QL})"):
    for i in map(int, r.split(',')):
        if i and i not in items: bad['quest item missing'].append(i)
qe = set(col(f"select quest from creature_questender where quest in ({QL})")) | set(col(f"select quest from gameobject_questender where quest in ({QL})"))
for qid in set(QS) - qe: bad['quest without ender'].append(qid)
lootE = f"(select lootid from creature_template where entry in {CRE})"
for i in col(f"select Item from creature_loot_template where Entry in {lootE} and Reference=0 union select Item from reference_loot_template where Entry>={G0} and Reference=0 "
             f"union select Item from gameobject_loot_template where Entry in (select Data1 from gameobject_template where type=3 and entry in {GOS}) and Reference=0"):
    if i not in items: bad['loot item missing'].append(i)
# an item id the module uses must be the same item Turtle meant (Turtle reused ids 3.3.5 gives to other items)
import difflib
from lib.sqlw import lit
_used = set()
for r in col(f"select concat_ws(',',RequiredItemId1,RequiredItemId2,RequiredItemId3,RequiredItemId4,RewardItem1,RewardItem2,RewardItem3,RewardItem4,"
             f"RewardChoiceItemID1,RewardChoiceItemID2,RewardChoiceItemID3,RewardChoiceItemID4,RewardChoiceItemID5,RewardChoiceItemID6,ItemDrop1,ItemDrop2,StartItem) from quest_template where ID in ({QL})"):
    _used |= {int(x) for x in r.split(',') if int(x)}
_used |= set(col(f"select Item from creature_loot_template where Entry in {lootE} and Reference=0 union select Item from reference_loot_template where Entry>={G0} and Reference=0 "
                 f"union select Item from gameobject_loot_template where Entry in (select Data1 from gameobject_template where type=3 and entry in {GOS}) "
                 f"union select item from npc_vendor where entry in {CRE}"))
_used = {i for i in _used if i < CFG['ids']['item_remap_base']}
if _used:
    c.execute(f"select a.entry, a.name, t.name, a.class, t.class from item_template a join {CFG['tw_db']}.item_template t on t.entry=a.entry where a.entry in ({','.join(map(str, _used))})")
    for e, an, tn, ac_, tc_ in c.fetchall():
        if an.lower() != tn.lower() and difflib.SequenceMatcher(None, an.lower(), tn.lower()).ratio() < (0.7 if ac_ != tc_ else 0.45) and \
                not col(f"select 1 from {CFG['tw_db']}.item_template where name={lit(an)} and class={ac_} and entry<>{e} limit 1"):
            # (not when a Turtle item of this name and class stands on another id: build.py ITEM_ALIAS uses this 3.3.5 item for it)
            bad['item id is a different 3.3.5 item'].append((e, tn, an))
for qid, prev in c.execute(f"select ID, PrevQuestID from quest_template_addon where ID in ({QL}) and PrevQuestID<>0") and c.fetchall() or []:
    if not col(f"select 1 from quest_template where ID={abs(prev)}"): bad['quest prerequisite missing'].append((qid, prev))
refs = set(col("select distinct Entry from reference_loot_template"))
for r in col(f"select Reference from creature_loot_template where Reference>0 and Entry in {lootE} union select Reference from reference_loot_template where Reference>0 and Entry>={G0}"):
    if r not in refs: bad['reference loot missing'].append(r)
for s in col(f"select action_param1 from smart_scripts where action_type in (11,85,86) and ((source_type=0 and entryorguid in {CRE}) or source_type=9 and entryorguid in (select action_param1 from smart_scripts where action_type=80 and entryorguid in {CRE}))"):
    if s not in SPELL: bad['smart spell missing'].append(s)
for s in col(f"select SpellId from trainer_spell where TrainerId in (select TrainerId from creature_default_trainer where CreatureId in {CRE})"):
    if s not in SPELL: bad['trainer spell missing'].append(s)
for i in col(f"select ItemID1 from creature_equip_template where CreatureID in {CRE} union select ItemID2 from creature_equip_template where CreatureID in {CRE} union select ItemID3 from creature_equip_template where CreatureID in {CRE}"):
    if i and i not in ITEMDBC: bad['equipment not in Item.dbc'].append(i)
for i in col(f"select item from npc_vendor where entry in {CRE}"):
    if i not in items: bad['vendor item missing'].append(i)
for i in col(f"select TextID from gossip_menu where MenuID in (select gossip_menu_id from creature_template where entry in {CRE})"):
    if i not in ctext: bad['npc_text missing'].append(i)
for g in col(f"select gossip_menu_id from creature_template where entry in {CRE} and gossip_menu_id>0"):
    if not col(f"select 1 from gossip_menu where MenuID={g} union select 1 from gossip_menu_option where MenuID={g}"): bad['gossip menu missing'].append(g)
item_dbc_rows = set(col("select ID from item_dbc"))
for i in col(f"select distinct Item from reference_loot_template where Entry>={G0} union select RewardItem1 from quest_template where ID in ({QL})"):
    if i and i not in ITEMDBC and i not in item_dbc_rows: bad['custom item without Item.dbc/item_dbc row'].append(i)
for sp in col(f"select spellid_1 from item_template where entry in (select ID from item_dbc) union select spellid_2 from item_template where entry in (select ID from item_dbc)"):
    if sp and sp not in SPELL: bad['item spell missing'].append(sp)
# hand-written / generated scripts (bosses, summons, action lists, objects by guid)
SCR = "((source_type=0 and entryorguid between 50000 and 99999) or (source_type=9 and entryorguid between 5000000 and 9999999) or (source_type=1 and (entryorguid < 0 or entryorguid >= 300000)))"
for s in col(f"select action_param1 from smart_scripts where action_type=11 and {SCR}"):
    if s not in SPELL: bad['smart spell missing'].append(s)
for e in col(f"select action_param1 from smart_scripts where action_type=12 and {SCR}"):
    if e not in tpl: bad['smart summon of missing creature'].append(e)
gtpl = set(col("select entry from gameobject_template"))
for e in col(f"select action_param1 from smart_scripts where action_type=50 and {SCR}"):
    if e not in gtpl: bad['smart summon of missing object'].append(e)
for g in col("select -entryorguid from smart_scripts where source_type=1 and entryorguid<0"):
    if not col(f"select 1 from gameobject where guid={g}"): bad['object script for a guid that is not spawned'].append(g)
for l in col(f"select action_param1 from smart_scripts where action_type=80 and {SCR}"):
    if not col(f"select 1 from smart_scripts where source_type=9 and entryorguid={l}"): bad['action list missing'].append(l)
maps = set(col("select ID from map_dbc")) | {r[0] for r in load(CFG['ac_dbc'] + '/Map.dbc')[3]}
for m in col("select map from instance_template") + col("select target_map from areatrigger_teleport"):
    if m not in maps: bad['map missing'].append(m)
for a in col("select ID from areatrigger_teleport"):
    if not col(f"select 1 from areatrigger where entry={a}"): bad['teleport trigger without areatrigger row'].append(a)
for gy in col("select ID from graveyard_zone where GhostZone in (select ID from areatable_dbc)"):
    if not col(f"select 1 from game_graveyard where ID={gy}"): bad['graveyard missing'].append(gy)
nodes = set(col("select ID from taxinodes_dbc")) | {r[0] for r in load(CFG['ac_dbc'] + '/TaxiNodes.dbc')[3]}
c.execute("select ID, FromTaxiNode, ToTaxiNode from taxipath_dbc")
for pid, a_, b_ in c.fetchall():
    if a_ not in nodes or b_ not in nodes: bad['flight path to unknown node'].append(pid)
    if not col(f"select 1 from taxipathnode_dbc where PathID={pid}"): bad['flight path without points'].append(pid)
for n in col("select ID from taxinodes_dbc"):
    if n >= 448: bad['taxi node id too high for the client (max 447)'].append(n)
# ---- what the worldserver itself complains about at startup (Errors.log), compared with the pristine world DB so
# only problems this module adds are reported. Each of these was seen on the live server once.
TALENT = {v for r in load(CFG['ac_dbc'] + '/Talent.dbc')[3] for v in r[4:13] if v}
_md_file = {r[0]: (r[1], r[2]) for r in load(CFG['ac_dbc'] + '/MapDifficulty.dbc')[3]}


def startup_problems(db):
    def q1(sql):
        c.execute(sql.replace('{db}', db))
        return c.fetchall()
    cid = 'id1' if q1("select 1 from information_schema.columns where table_schema='{db}' and table_name='creature' and column_name='id1'") else 'id'
    p = collections.defaultdict(set)
    for tab in ('creature_queststarter', 'creature_questender'):
        for e, qq in q1(f"select s.id, s.quest from {{db}}.{tab} s join {{db}}.creature_template t on t.entry=s.id where t.npcflag & 2 = 0"):
            p[f'{tab}: creature lacks UNIT_NPC_FLAG_QUESTGIVER'].add((e, qq))
    for col_, tab in (('lootid', 'creature_loot_template'), ('skinloot', 'skinning_loot_template'), ('pickpocketloot', 'pickpocketing_loot_template')):
        for e, l in q1(f"select entry, {col_} from {{db}}.creature_template where {col_}>0 and {col_} not in (select Entry from {{db}}.{tab})"):
            p[f'{tab} entry used by a creature does not exist'].add((e, l))
    for e, pg in q1("select entry, PageText from {db}.item_template where PageText>0 and PageText not in (select ID from {db}.page_text)"):
        p['item has non existing first page'].add((e, pg))
    for e, pg in q1("select entry, Data0 from {db}.gameobject_template where type=9 and Data0>0 and Data0 not in (select ID from {db}.page_text) "
                    "union select entry, Data7 from {db}.gameobject_template where type=10 and Data7>0 and Data7 not in (select ID from {db}.page_text)"):
        p['gameobject has non existing page'].add((e, pg))
    for i_, n_ in q1("select ID, NextPageID from {db}.page_text where NextPageID>0 and NextPageID not in (select ID from {db}.page_text)"):
        p['page_text next page missing'].add((i_, n_))
    for t_, s_ in q1("select TrainerId, SpellId from {db}.trainer_spell"):
        if s_ in TALENT:
            p['trainer_spell is a talent'].add((t_, s_))
    for e, a_, b_ in q1("select distinct t.entry, t.Data2, t.Data3 from {db}.gameobject g join {db}.gameobject_template t on t.entry=g.id where t.type=25 and t.Data2>t.Data3"):
        p['fishing hole min opens > max opens (worldserver assert)'].add((e, a_, b_))
    md = dict(_md_file)
    for i_, m_, d_ in q1("select ID, MapID, Difficulty from {db}.mapdifficulty_dbc"):
        md[i_] = (m_, d_)
    diffs = collections.defaultdict(set)
    for m_, d_ in md.values():
        diffs[m_].add(d_)
    for tab, idc in (('creature', cid), ('gameobject', 'id')):
        for g_, m_, sm in q1(f"select guid, map, spawnMask from {{db}}.{tab} where map in ({','.join(map(str, diffs)) or 'NULL'})"):
            allowed = sum(1 << d_ for d_ in diffs[m_])
            if sm & ~allowed:
                p[f'{tab} spawn mask includes a difficulty the map does not have'].add((g_, m_, sm))
    return p


_base = startup_problems(CFG['ac_db'])
for k, v in startup_problems(DB).items():
    new_ = v - _base.get(k, set())
    if new_:
        bad['startup: ' + k] += sorted(new_)
cnt = dict(creatures=len(cre), spawns=len(col(f"select guid from creature where guid between {G0} and {G1}")),
           gameobjects=len(col(f"select guid from gameobject where guid between {G0} and {G1}")), quests=len(QS))
print('module content in', DB, cnt)
if bad:
    for k, v in bad.items():
        print(f'  PROBLEM {k}: {len(v)} e.g. {sorted(set(map(str, v)))[:10]}')
    sys.exit(1)
print('  all references resolve')
