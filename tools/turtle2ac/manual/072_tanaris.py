"""Tanaris - Turtle's quest scripts (src/scripts/world/tanaris.cpp, miscellaneous/random_scripts_1.cpp and _3.cpp) as SmartAI.

Quest progress (without these the quests cannot be finished):
- Slickwick's four pump stations (go_slickwick_control_panel): "A Deal Worth Taking" (41762, Alliance: sabotage them) and
  "Oil-Based Grievances" (41764, Horde: shut them off with Kalke's Energy Regulator). Turtle credits the panel objects
  themselves; a SmartAI script can only give creature credit, so both quests ask for four credit creatures instead (new
  templates 9100001-9100004, never spawned, objective texts named after the panels). Each panel has its own menu: the
  option shows only while that panel's objective is open (and, for 41764, while the regulator is in the bags).
- "Sandfury Redemption III" (40524): Vol'jin (3.3.5, Orgrimmar) hears the player out over three pages (credit 60377).
- "VIP Invites" (80382): Gazlowe (3.3.5, Ratchet) takes the invitation (credit 81000). Baron Revilgaz's part (credit 81001)
  is in manual/058_stranglethorn_vale.py, which owns his SmartAI.
- "Sharks Are Friends, Not Food" (80383): /shoo at the shark (credit 81002); it swims off.
- "Intricate Artwork" (41763): Kwabit's Chest needs Kwabit's Chest Key in Turtle (a lock 3.3.5 cannot express:
  config.json lock_substitutions gives it a plain lock); here the drawing drops only for a player carrying the key.
Flavour: Seer Maz'ek's and Ekka's words when "Desert Voodoo" (40521) / "Meat for Viceclaw!" (40528) are turned in.
Turtle's quest drops on 3.3.5 Tanaris creatures (STOCK_DROPS).
Left out: Ka'fai's option (his quest "Wisdom From Failure" is not in the build).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
from lib.sqlw import lit
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
NO_SELECT = 0x2000000
q, TW, AC, item = ctx['q'], ctx['TW'], ctx['AC'], ctx['item']
MAZEK, EKKA, VICECLAW, SHARK, GAZLOWE, VOLJIN = 60752, 60750, 60755, 81006, 3391, 10540
PANELS = [(2020225, 'Control Panel Alpha'), (2020226, 'Control Panel Beta'), (2020227, 'Control Panel Gamma'),
          (2020228, 'Control Panel Delta')]
CREDIT_BASE = 9100001                 # module creature templates (Turtle ids end at 2.5 M, 3.3.5's at 3.5 M)
SABOTAGE, DEACTIVATE, REGULATOR = 41762, 41764, 41995
S.names.update({MAZEK: "Seer Maz'ek", EKKA: 'Ekka', VICECLAW: 'Viceclaw', SHARK: 'Shark', GAZLOWE: 'Gazlowe', VOLJIN: "Vol'jin"})
for go_, nm_ in PANELS:
    S.names[go_] = nm_


def npc_text(i, default=None):
    r_ = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)
    if not r_:
        return default
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", r_[0]['b'])[0]
    return r['male_text'] or r['female_text']


def cond(src, group, entry, sid, ctype, v1, v2=0, v3=0, neg=0, comment=''):
    return ("INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
            "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
            "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
            f"({src}, {group}, {entry}, {sid}, 0, {ctype}, 0, {v1}, {v2}, {v3}, {neg}, 0, 0, '', {lit('mod-turtle-content: ' + comment)});")


# ---- Slickwick pump stations: credit templates, quest objectives, one menu per panel
credits = [CREDIT_BASE + k for k in range(4)]
cl_ = ','.join(map(str, credits))
S.extra_sql.append(f"DELETE FROM `creature_template` WHERE `entry` IN ({cl_});\n"
                   f"DELETE FROM `creature_template_model` WHERE `CreatureID` IN ({cl_});")
for k, (go_, nm_) in enumerate(PANELS):
    S.extra_sql.append("INSERT INTO `creature_template` (`entry`, `name`, `subname`, `minlevel`, `maxlevel`, `faction`, `unit_flags`, "
                       "`type`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES "
                       f"({credits[k]}, {lit(nm_)}, 'Quest credit', 1, 1, 35, {NO_SELECT}, 10, 128, '', 0);")
    S.extra_sql.append("INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, "
                       f"`VerifiedBuild`) VALUES ({credits[k]}, 0, 11686, 1, 1, 0);")
for qid_ in (SABOTAGE, DEACTIVATE):
    S.extra_sql.append("UPDATE `quest_template` SET " + ', '.join(
        f"`RequiredNpcOrGo{k + 1}`={credits[k]}, `ObjectiveText{k + 1}`={lit(nm_)}" for k, (_, nm_) in enumerate(PANELS)) +
        f" WHERE `ID`={qid_};")
PANEL_TEXT = npc_text(2020225, 'A control panel full of levers, dials and blinking lights.')
for k, (go_, nm_) in enumerate(PANELS):
    M_ = OFF + go_
    S.gossip(M_, PANEL_TEXT, [(0, '<Sabotage the pump station.>', 0, 0, [(47, SABOTAGE, IN_PROGRESS, 0)]),
                              (1, '<Deactivate the buzzing control panel.>', 0, 0,
                               [(47, DEACTIVATE, IN_PROGRESS, 0), (2, item(REGULATOR), 1, 0)])])
    # S.gossip writes conditions without a third value: add "this panel's objective has no credit yet" (48: quest, objective, 0)
    S.extra_sql.append(cond(15, M_, 0, 0, 48, SABOTAGE, k, 0, 0, f'{nm_} - objective {k + 1} of {SABOTAGE} open'))
    S.extra_sql.append(cond(15, M_, 1, 0, 48, DEACTIVATE, k, 0, 0, f'{nm_} - objective {k + 1} of {DEACTIVATE} open'))
    S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data0`=0, `Data1`=0, `Data2`=0, `Data3`={M_}, "
                       f"`AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={go_};")
    for opt_ in (0, 1):
        S.row(go_, 1, 62, [M_, opt_], A(33, [credits[k]], 'invoker', note=f'Quest Credit {credits[k]}'))
        S.row(go_, 1, 62, [M_, opt_], A(72, [], 'invoker', note='Close Gossip'))

# ---- Vol'jin (3.3.5, Orgrimmar): "Sandfury Redemption III" (40524) - three pages, then the credit
S.mark_stock(VOLJIN)
V1, V2, V3 = OFF + 30028, OFF + 30029, OFF + 30030
S.gossip(V3, npc_text(30030))
S.gossip(V2, npc_text(30029), [(0, 66749, 0, 0, [])])
S.gossip(V1, npc_text(30028), [(0, 66748, 0, V2, [])])
S.stock_gossip_option(7339, 50, 66747, 0, [(47, 40524, IN_PROGRESS, 0)])
S.row(VOLJIN, 0, 62, [7339, 50], A(98, [V1, V1], 'invoker', note='Send gossip page 2'))
S.row(VOLJIN, 0, 62, [V2, 0], A(33, [60377], 'invoker', note='Quest Credit 60377'))
S.row(VOLJIN, 0, 62, [V2, 0], A(98, [V3, V3], 'invoker', note='Send gossip page 4'))

# ---- Gazlowe (3.3.5, Ratchet): "VIP Invites" (80382) - Turtle gives him a menu with the invitation option
S.mark_stock(GAZLOWE)
GZ = OFF + GAZLOWE
S.gossip(GZ, 'Greetings, $c.', [(0, 66841, 0, 0, [(47, 80382, IN_PROGRESS, 0)])])
old_ = q(f"select npcflag from {AC}.creature_template where entry=%s", GAZLOWE)[0]['npcflag']
S.stock_template(GAZLOWE, gossip_menu_id=GZ, npcflag=old_ | 1)
S.btext(GAZLOWE, 100, 66115)
S.row(GAZLOWE, 0, 62, [GZ, 0], S.talk(100))
S.row(GAZLOWE, 0, 62, [GZ, 0], A(33, [81000], 'invoker', note='Quest Credit 81000'))
S.row(GAZLOWE, 0, 62, [GZ, 0], A(72, [], 'invoker', note='Close Gossip'))

# ---- the shark at the beach: "Sharks Are Friends, Not Food" (80383) - /shoo (text emote 129) while the quest is open
S.btext(SHARK, 0, 66840, 'emote')
sid_ = None
for a_ in (A(33, [81002], 'invoker', note='Quest Credit 81002'), S.talk(0), A(89, [15], 'self', note='Swims off (random move 15 yd)')):
    i_ = S.row(SHARK, 0, 22, [129, 0, 0], a_)
    S.extra_sql.append(cond(22, i_ + 1, SHARK, 0, 47, 80383, IN_PROGRESS, 0, 0, 'Sharks Are Friends, Not Food in progress'))
S.extra_sql.insert(0, f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=22 AND `SourceEntry`={SHARK} AND `SourceId`=0;")

# ---- Seer Maz'ek: "Desert Voodoo" (40521) turned in
S.on(MAZEK, 'reward_quest', A(80, [MAZEK * 100 + 1, 0, 0], 'self', note='Calls on the Loa (action list)'), ep=[40521])
steps = []
for n_, (ms, bid) in enumerate(((0, 66451), (5000, 66452), (5000, 66453))):
    S.btext(MAZEK, n_, bid)
    steps += [(ms, S.talk(n_)), (0, A(5, [4], 'self', note='Emote Cheer'))]
S.actionlist(MAZEK * 100 + 1, steps, "Seer Maz'ek")

# ---- Ekka: "Meat for Viceclaw!" (40528) turned in
S.btext(EKKA, 0, 66454)
S.btext(EKKA, 1, 66455)
S.btext(VICECLAW, 0, 66750, 'emote')
S.on(EKKA, 'reward_quest', A(80, [EKKA * 100 + 1, 0, 0], 'self', note='Feeds Viceclaw (action list)'), ep=[40528])
S.actionlist(EKKA * 100 + 1, [(0, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
                              (3000, A(1, [0, 0, 0], 'closest_creature', tp=[VICECLAW, 15, 0], note='Viceclaw cackles')),
                              (2000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk'))], 'Ekka')

# ---- Kwabit's Chest (Slickwick): the drawing drops only for a player carrying Kwabit's Chest Key
ck_ = q(f"select data1 from {TW}.gameobject_template where entry=2020217")[0]['data1']
S.extra_sql.append(f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=4 AND `SourceGroup`={ck_} AND `SourceEntry`={item(41860)};")
S.extra_sql.append(cond(4, ck_, item(41860), 0, 2, item(41905), 1, 0, 0, "Kwabit's Salacious Pictorial needs Kwabit's Chest Key"))

# ---- a 3.3.5 Rabid Blisterpaw at Land's End stands 2.5 yd under the ground Turtle raised there (stock-spawn ground
#      check against the shipped Kalimdor_36_49): put on the new ground (the rollback restores the height)
S.stock_spawn('creature', 22595, position_z=14.4)

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): the rocs and Greater
#      Firebirds and the Blisterpaw hyenas (Da Unforgiving Lands), Dunemaul ogre casters (Desert Voodoo), Glasshide Gazers and
#      Coast Striders (Gelwig's quests), Gusting Vortexes (The Gusting Vortex)
STOCK_DROPS = S.stock_quest_drops([60760, 60761, 60763, 60833, 60834, 60836])

SQL = S.sql()
