"""Stranglethorn Vale - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp and _3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- Garfield Sparkblast's Bloodsail chain: "Red Flag over the Sea" (40172, join the pirates), "Captain of the Bloodsail Buccaneers"
  (40187, the toast), "Naming the Vessel" (40354); the Blast Powder Kegs (40174 pour water, 40186 ignite), the Huge Keg of Rum (40178),
  Morgan the Storm turning on the player (40179), Baron Revilgaz receiving the Jolly Roger ("Making a Statement", 40180).
- Turtle sets reputation in C++ (Bloodsail to Neutral at 40172, Booty Bay to Hated at 40180); AzerothCore cannot set it, so the quests
  reward it: 40172 +6,500 Bloodsail (a character who never killed pirates lands at Neutral, as on Turtle), 40180 -50,000 Booty Bay
  (Hated; 3.3.5 passes half of it to Gadgetzan, Everlook and Ratchet). Both quests open with a warning (Max, 2026-10-08).
- Vil'do One-Tusk's chain: Fazgel Mechaflame (Feralas) turning on the player (40360), Lyvdia Dawnbird handing over the statue and
  the notes (40361), Arcanist Sovatir (40362); Vil'do's "set sail for Feralas" talk.
- Turtle's quest drops on 3.3.5 creatures (naga, gorillas, scorpids, Ironpatch) and Barkeep Morag's Jug of Orgrimmar Brown.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
TAKEN = 2 | 8 | 64                    # complete, incomplete or rewarded
GARFIELD_BB, GARFIELD, MORGAN, VILDO, FAZGEL, SOVATIR = 60453, 60496, 51607, 60459, 60643, 60644
REVILGAZ, MORAG = 2496, 5611
POWDER_KEG, RUM_KEG, LYVDIA = 2010834, 2010836, 2010871
S.names.update({GARFIELD_BB: 'Garfield Sparkblast', GARFIELD: 'Garfield Sparkblast', MORGAN: 'Morgan the Storm', VILDO: "Vil'do One-Tusk",
                FAZGEL: 'Fazgel Mechaflame', SOVATIR: 'Arcanist Sovatir', REVILGAZ: 'Baron Revilgaz', POWDER_KEG: 'Blast Powder Keg', RUM_KEG: 'Huge Keg of Rum', LYVDIA: 'Lyvdia Dawnbird'})
q, TW, AC, item = ctx['q'], ctx['TW'], ctx['AC'], ctx['item']


def npc_text(i):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these"""
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def hostile(entry, list_id, lines=()):
    """Turtle SetFactionTemporary(14, RESTORE_COMBAT_STOP) + attack: hostile until the fight ends"""
    S.actionlist(list_id, [(0, A(72, [], 'invoker', note='Close Gossip'))] + [(0, a) for a in lines] + [
        (0, A(5, [36], 'self', note='Emote Attack')),
        (0, A(2, [14], 'self', note='Hostile (faction 14)')),
        (0, A(49, [], 'invoker', note='Attack'))], S.names[entry])
    S.on(entry, 'evade', A(2, [0], 'self', note='Default faction again'))
    S.on(entry, 'respawn', A(2, [0], 'self', note='Default faction again'))


# ---- the reputation the chain sets on Turtle, as quest rewards, and the warning Max asked for
WARN_CHAIN = ("<WARNING: this quest chain sides you with the Bloodsail Buccaneers. Finishing it will drastically lower your reputation "
              "with Booty Bay, Gadgetzan, Everlook and Ratchet, down to a hostile standing.>$B$B")
WARN_STEP = ("<WARNING: completing this quest will drastically lower your reputation with Booty Bay, Gadgetzan, Everlook and Ratchet, "
             "down to a hostile standing: their goblins and guards will turn on you.>$B$B")
S.extra_sql.append("UPDATE `quest_template` SET `RewardFactionID1`=87, `RewardFactionValue1`=0, `RewardFactionOverride1`=650000, "
                   f"`QuestDescription`=CONCAT('{WARN_CHAIN}', `QuestDescription`) WHERE `ID`=40172;")
S.extra_sql.append("UPDATE `quest_template` SET `RewardFactionID2`=21, `RewardFactionValue2`=0, `RewardFactionOverride2`=-5000000, "
                   f"`QuestDescription`=CONCAT('{WARN_STEP}', `QuestDescription`) WHERE `ID`=40180;")

# ---- Garfield Sparkblast (Booty Bay and Bloodsail Retreat; one C++ script for both)
G0 = OFF + 60496
S.gossip(G0, npc_text(60496), [(0, 66659, 0, 0, [(47, 40172, IN_PROGRESS, 0)]),
                               (1, 66660, 0, 0, [(47, 40187, IN_PROGRESS, 0)]),
                               (2, 66661, 0, 0, [(47, 40354, IN_PROGRESS, 0)])])
for g in (GARFIELD_BB, GARFIELD):
    S.btext(g, 0, 66662)
    S.btext(g, 1, 66663)
    S.btext(g, 2, 66426, 'yell')
    S.btext(g, 3, 66427, 'yell')
    S.btext(g, 4, 66404)
    S.row(g, 0, 62, [G0, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.row(g, 0, 62, [G0, 0], A(5, [21], 'self', note='Emote Applaud'))
    S.row(g, 0, 62, [G0, 0], A(33, [60332], 'invoker', note='Quest Credit 60332'))
    S.row(g, 0, 62, [G0, 1], A(72, [], 'invoker', note='Close Gossip'))
    S.row(g, 0, 62, [G0, 1], A(80, [g * 100 + 1, 0, 0], 'self', note='The toast (action list)'))
    S.actionlist(g * 100 + 1, [
        (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
        (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
        (2000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
        (5000, S.talk(2)), (0, A(5, [21], 'self', note='Emote Applaud')),
        (4000, S.talk(3)), (0, A(5, [4], 'self', note='Emote Cheer')),
        (0, A(33, [60331], 'invoker', note='Quest Credit 60331')),
        (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], 'Garfield Sparkblast')
    S.row(g, 0, 62, [G0, 2], A(72, [], 'invoker', note='Close Gossip'))
    S.row(g, 0, 62, [G0, 2], A(80, [g * 100 + 2, 0, 0], 'self', note='Naming the vessel (action list)'))
    S.actionlist(g * 100 + 2, [
        (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
        (0, S.talk(4)), (0, A(5, [1], 'self', note='Emote Talk')),
        (5000, A(33, [60354], 'invoker', note='Quest Credit 60354')),
        (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], 'Garfield Sparkblast')
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={G0}, `npcflag`=`npcflag`|1 WHERE `entry`={g};")

# ---- Morgan the Storm: "Exterminate the Rat" (40179) - spit in his face and he fights
M0 = OFF + MORGAN
S.gossip(M0, 'Greetings, $n.', [(0, 66658, 0, 0, [(47, 40179, IN_PROGRESS, 0)])])
S.row(MORGAN, 0, 62, [M0, 0], A(80, [MORGAN * 100 + 1, 0, 0], 'self', note='Turns hostile (action list)'))
hostile(MORGAN, MORGAN * 100 + 1)
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M0}, `npcflag`=`npcflag`|1 WHERE `entry`={MORGAN};")

# ---- Blast Powder Kegs: "A Cannon's Misfortune" (40174, pour water: 10 kegs) and "Land ho?" (40186, ignite one)
#      (a button in Turtle opened by C++: here a gossip object, as the Northwind keg)
K0 = OFF + POWDER_KEG
S.gossip(K0, npc_text(2010834), [(0, 66655, 0, 0, [(47, 40174, IN_PROGRESS, 0), (2, item(60373), 1, 0)]),
                                 (1, 66656, 0, 0, [(47, 40186, IN_PROGRESS, 0), (2, item(60257), 1, 0)])])
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data0`=0, `Data1`=0, `Data2`=0, `Data3`={K0}, `AIName`='SmartGameObjectAI', "
                   f"`ScriptName`='' WHERE `entry`={POWDER_KEG};")
S.row(POWDER_KEG, 1, 62, [K0, 0], A(33, [60328], 'invoker', note='Quest Credit 60328'))
S.row(POWDER_KEG, 1, 62, [K0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(POWDER_KEG, 1, 62, [K0, 0], A(105, [NO_SELECT], 'self', note='Watered (not selectable)'))
S.row(POWDER_KEG, 1, 62, [K0, 0], A(80, [POWDER_KEG * 100 + 1, 0, 0], 'self', note='Usable again (action list)'))
S.actionlist(POWDER_KEG * 100 + 1, [(150000, A(106, [NO_SELECT], 'self', note='Selectable again'))], 'Blast Powder Keg')
S.row(POWDER_KEG, 1, 62, [K0, 1], A(57, [item(60257), 1], 'invoker', note='Remove the fuse'))
S.row(POWDER_KEG, 1, 62, [K0, 1], A(33, [60330], 'invoker', note='Quest Credit 60330'))
S.row(POWDER_KEG, 1, 62, [K0, 1], A(72, [], 'invoker', note='Close Gossip'))

# ---- Huge Keg of Rum: "Loss of Good Rum" (40178): a quest object (goober) gives the object credit; using it takes the poison
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=10, `Data0`=0, `Data1`=40178, `Data2`=0, `Data3`=0, `AIName`='SmartGameObjectAI', "
                   f"`ScriptName`='' WHERE `entry`={RUM_KEG};")
S.row(RUM_KEG, 1, 64, [], A(57, [item(60252), 1], 'invoker', note='Remove the item poured into the keg'))

# ---- Baron Revilgaz (3.3.5): "Making a Statement" (40180) - the Jolly Roger with Morgan's head
S.mark_stock(REVILGAZ)
S.btext(REVILGAZ, 100, 66117, 'yell')
S.stock_gossip_option(6685, 50, 66843, 0, [(47, 40180, IN_PROGRESS, 0), (2, item(60254), 1, 0)])
S.row(REVILGAZ, 0, 62, [6685, 50], A(72, [], 'invoker', note='Close Gossip'))
S.row(REVILGAZ, 0, 62, [6685, 50], A(57, [item(60254), 1], 'invoker', note='Take the Jolly Roger'))
S.row(REVILGAZ, 0, 62, [6685, 50], S.talk(100))
S.row(REVILGAZ, 0, 62, [6685, 50], A(33, [60333], 'invoker', note='Quest Credit 60333'))
# "VIP Invites" (80382, Tanaris - the beach party; the rest of it is in manual/072_tanaris.py): this file owns Revilgaz's
# SmartAI, so his part of that quest is here
S.btext(REVILGAZ, 101, 66116)
S.stock_gossip_option(6685, 51, 66842, 0, [(47, 80382, IN_PROGRESS, 0)])
S.row(REVILGAZ, 0, 62, [6685, 51], S.talk(101))
S.row(REVILGAZ, 0, 62, [6685, 51], A(33, [81001], 'invoker', note='Quest Credit 81001'))
S.row(REVILGAZ, 0, 62, [6685, 51], A(72, [], 'invoker', note='Close Gossip'))

# ---- Vil'do One-Tusk: "Golden Elves of Feralas" talk (40358 taken)
V0, V1 = OFF + 60459, OFF + 30015
S.gossip(V1, npc_text(30015), [(0, 66712, 0, 0, [])])
S.gossip(V0, npc_text(60459), [(0, 66711, 0, V1, [(47, 40358, TAKEN, 0)])])
S.row(VILDO, 0, 62, [V1, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={V0}, `npcflag`=`npcflag`|1 WHERE `entry`={VILDO};")

# ---- Fazgel Mechaflame (Feralas): "Highly Unexpected Event" (40360)
F0 = OFF + 60643
S.btext(FAZGEL, 0, 66714)
S.gossip(F0, npc_text(60643), [(0, 66713, 0, 0, [(47, 40360, IN_PROGRESS, 0)])])
S.row(FAZGEL, 0, 62, [F0, 0], A(80, [FAZGEL * 100 + 1, 0, 0], 'self', note='Turns hostile (action list)'))
hostile(FAZGEL, FAZGEL * 100 + 1, [S.talk(0)])
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={F0}, `npcflag`=`npcflag`|1 WHERE `entry`={FAZGEL};")

# ---- Lyvdia Dawnbird (Feralas): accepting "Taking the Booty Home" (40361) gives the statue and Sovatir's notes
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={LYVDIA};")
S.row(LYVDIA, 1, 19, [40361], A(56, [item(60510), 1], 'invoker', note='Give Highborne Golden Statue'))
S.row(LYVDIA, 1, 19, [40361], A(56, [item(60512), 1], 'invoker', note="Give Arcanist Sovatir's Torn Notes"))

# ---- Arcanist Sovatir (Bloodsail Retreat): "A Historian Finds You" (40362)
O0, O1 = OFF + 60644, OFF + 30016
S.gossip(O1, npc_text(30016))
S.gossip(O0, npc_text(60644), [(0, 66715, 0, O1, [(47, 40362, IN_PROGRESS, 0)])])
S.row(SOVATIR, 0, 62, [O0, 0], A(33, [60355], 'invoker', note='Quest Credit 60355'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={O0}, `npcflag`=`npcflag`|1 WHERE `entry`={SOVATIR};")

# ---- Barkeep Morag (Orgrimmar, 3.3.5) sells the Jug of Orgrimmar Brown, as on Turtle ("Smuggling Ale", 40198)
JUG = item(60271)
S.extra_sql.append(f"DELETE FROM `npc_vendor` WHERE `entry`={MORAG} AND `item`={JUG};\n"
                   f"INSERT INTO `npc_vendor` (`entry`, `slot`, `item`, `maxcount`, `incrtime`, `ExtendedCost`, `VerifiedBuild`) VALUES ({MORAG}, 0, {JUG}, 0, 0, 0, 0);")
S.rollback.append(f"DELETE FROM `npc_vendor` WHERE `entry`={MORAG} AND `item`={JUG};")

# ---- Turtle's quest drops on 3.3.5 creatures: Naga Explorers (Naga Trident, Highborne Necklace), the Mistvale gorillas (Pristine
#      Gorilla Pelt), Scorpid Hunters (Potent Scorpid Venom), Ironpatch (Ironpatch's Head, "The Iron Patch")
STOCK_DROPS = S.stock_quest_drops([60474, 60483, 60476, 60478, 51895])

# ---- the Highborne Golden Statues (Feralas) stand 1-3 yd under the 3.3.5 ground (AzerothCore server map): raised onto it
#      (Turtle's tile there was not extracted; unverified in game)
for tw_guid_, z_ in ((5003322, 27.6), (5003323, 19.8), (5003324, 19.1), (5003325, 21.5)):
    S.extra_sql.append(f"UPDATE `gameobject` SET `position_z`={z_} WHERE `guid`={ctx['gguid'](tw_guid_)};")

# ---- three 3.3.5 Skymane Gorillas stand where Turtle built Bloodsail Retreat (Turtle removed them): taken out; the rollback
#      puts them back. (The other 63 3.3.5 spawns on tiles 32_59/33_59 keep their ground within 0.7 yd.)
for guid_ in (802, 808, 919):
    S.stock_spawn_remove('creature', guid_)

SQL = S.sql()
