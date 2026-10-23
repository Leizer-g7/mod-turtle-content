"""Lapidis Isle - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "The Boran Family" (40141): Arnold Boran hands over the two letters when the quest is accepted.
- "Sailors Innovation" (40142): Chef Jenkel gives the Pinch of Salt ("Slim is asking for salt.").
- "The Maul'ogg Crisis III" (40266, a Gillijim's Isle quest): Seer Bol'ukk's tale gives the credit.
- "The Boran Family" (40141): Samual (Southshore) and Karl Boran (Menethil Harbor) trade letters.
- "The Tower of Lapidis IV" (40166): Archmage Ansirem Runeweaver works the spell.
- Turtle's quest drops on 3.3.5 creatures in Kalimdor (Thunderhead Horn, Volcanic Ember, Aqua Orb, Jadefire Felhorn).
Flavour: Colonel Hardinus's cheer when "The Tower of Lapidis X" (40303) is handed in, Arch Hydromancer Lapidis's
lines, Captain Ironhoof's line when pulled. Insom'ni (a Gillijim's Isle NPC) is scripted in manual/052_gillijims_isle.py.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
BORAN, JENKEL, BOLUKK, HARDINUS, LAPIDIS, IRONHOOF = 91883, 91950, 91854, 92002, 60467, 92142
S.names.update({BORAN: 'Arnold Boran', JENKEL: 'Chef Jenkel', BOLUKK: "Seer Bol'ukk", HARDINUS: 'Colonel Hardinus',
                LAPIDIS: 'Arch Hydromancer Lapidis', IRONHOOF: 'Captain Ironhoof'})

# ---- Arnold Boran: The Boran Family (40141) - the two letters
S.on(BORAN, 'accepted_quest', A(56, [60204, 1], 'invoker', note='Give letter 60204'), A(56, [60205, 1], 'invoker', note='Give letter 60205'),
     ep=[40141])

# ---- Chef Jenkel: cooking trainer + the Pinch of Salt for Sailors Innovation (40142)
S.btext(JENKEL, 0, 66650)
J0 = OFF + 91950
S.gossip(J0, 91950, [(0, 66648, 3, 0, [], (5, 16)),
                     (1, 66649, 0, 0, [(47, 40142, IN_PROGRESS, 0), (2, 60207, 1, 1)])])
S.row(JENKEL, 0, 62, [J0, 1], A(56, [60207, 1], 'invoker', note='Give the Pinch of Salt'))
S.row(JENKEL, 0, 62, [J0, 1], A(1, [0, 0, 0], 'invoker', note='Say Line 0'))
S.row(JENKEL, 0, 62, [J0, 1], A(5, [1], 'self', note='Emote Talk'))
S.row(JENKEL, 0, 62, [J0, 1], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={J0}, `npcflag`=`npcflag`|1 WHERE `entry`={JENKEL};")

# ---- Seer Bol'ukk: The Maul'ogg Crisis III (40266)
S.btext(BOLUKK, 0, 66685)
S.btext(BOLUKK, 1, 66686)
B0 = OFF + 91854
S.gossip(B0, 91854, [(0, 66684, 0, 0, [(47, 40266, IN_PROGRESS, 0)])])
S.row(BOLUKK, 0, 62, [B0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(BOLUKK, 0, 62, [B0, 0], A(80, [BOLUKK * 100 + 1, 0, 0], 'self', note='Tale (action list)'))
S.actionlist(BOLUKK * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (3000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (20000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (10000, A(33, [60338], 'invoker', note='Quest Credit 60338')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], "Seer Bol'ukk")
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={B0}, `npcflag`=`npcflag`|1 WHERE `entry`={BOLUKK};")

# ---- Colonel Hardinus: The Tower of Lapidis X (40303) handed in - his men cheer
S.btext(HARDINUS, 0, 67028)
S.on(HARDINUS, 'reward_quest', A(80, [HARDINUS * 100 + 1, 0, 0], 'self', note='Cheer (action list)'), ep=[40303])
S.actionlist(HARDINUS * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, A(5, [4], 'self', note='Emote Cheer')),
    (1750, S.talk(0)), (0, A(5, [22], 'self', note='Emote Shout')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (550, A(5, [4], 'closest_creature', tp=[92004, 100, 0], note='Cheer')),
    (200, A(5, [4], 'closest_creature', tp=[91882, 100, 0], note='Cheer')),
    (200, A(5, [4], 'closest_creature', tp=[91889, 100, 0], note='Cheer')),
    (200, A(5, [4], 'closest_creature', tp=[92025, 100, 0], note='Cheer'))], 'Colonel Hardinus')

# ---- Arch Hydromancer Lapidis and Captain Ironhoof: their lines
S.btext(LAPIDIS, 0, 66414)
S.btext(LAPIDIS, 1, 66415)
S.on(LAPIDIS, 'aggro', S.talk(0))
S.on(LAPIDIS, 'death', S.talk(1))
S.btext(IRONHOOF, 0, 66402)
S.on(IRONHOOF, 'aggro', S.talk(0))

# ---- The Boran Family (40141): Samual Boran in Southshore (a Turtle NPC, added to this zone) and Karl Boran in Menethil
#      Harbor (a 3.3.5 NPC: he gets a gossip menu; the rollback restores him) each take Arnold's letter and hand over theirs.
SAMUAL, KARL = 92936, 1242
S.names.update({SAMUAL: 'Samual Boran', KARL: 'Karl Boran'})
for npc, menu_text, give, take, credit, lines, grp in ((SAMUAL, 92936, 60203, 60205, 60326, (66643, 66644), 0),
                                                       (KARL, 1042, 60202, 60204, 60325, (66645, 66646), 100)):
    if npc == KARL:
        S.mark_stock(KARL)
    S.btext(npc, grp, lines[0])
    S.btext(npc, grp + 1, lines[1])
    M = OFF + menu_text
    S.gossip(M, menu_text, [(0, 66642, 0, 0, [(47, 40141, IN_PROGRESS, 0), (2, take, 1, 0)])])
    S.row(npc, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.row(npc, 0, 62, [M, 0], A(57, [take, 1], 'invoker', note="Take Arnold's letter"))
    S.row(npc, 0, 62, [M, 0], A(80, [npc * 100 + 1, 0, 0], 'self', note='The letter (action list)'))
    S.actionlist(npc * 100 + 1, [
        (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
        (1000, A(1, [grp, 0, 0], 'invoker', note=f'Say Line {grp}')), (0, A(5, [1], 'self', note='Emote Talk')),
        (4000, A(1, [grp + 1, 0, 0], 'invoker', note=f'Say Line {grp + 1}')), (0, A(5, [1], 'self', note='Emote Talk')),
        (0, A(56, [give, 1], 'invoker', note='Give his letter')),
        (0, A(33, [credit, 1], 'invoker', note=f'Quest Credit {credit}')),
        (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], S.names[npc])
    if npc == KARL:
        S.stock_template(KARL, gossip_menu_id=M, npcflag=3)
    else:
        S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M}, `npcflag`=`npcflag`|1 WHERE `entry`={SAMUAL};")

# ---- Archmage Ansirem Runeweaver (3.3.5 NPC, Dalaran): The Tower of Lapidis IV (40166) - he works the spell, then the credit
ANSIREM = 2543
S.names[ANSIREM] = 'Archmage Ansirem Runeweaver'
S.mark_stock(ANSIREM)
S.btext(ANSIREM, 100, 66991)
S.on(ANSIREM, 'accepted_quest', A(80, [ANSIREM * 100 + 1, 0, 0], 'self', note='The spell (action list)'), ep=[40166])
S.actionlist(ANSIREM * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.cast(23017, 'self')),                                   # Arcane Channeling
    (18000, A(5, [273], 'self', note='Emote Yes')),
    (0, S.cast(1449, 'self')),                                    # Arcane Explosion (visual)
    (2000, A(1, [100, 0, 0], 'invoker', note='Say Line 100')), (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(33, [60327, 1], 'invoker', note='Quest Credit 60327')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], 'Archmage Ansirem Runeweaver')
# Dustwallow Marsh's "Preparation for Divination" (40561, file 027): he gives the player Magus Halister's focus (Turtle
# GossipHello_npc_ansirem); here, because this file owns Ansirem's SmartAI
AM = 9000000 + 2543
_b = ctx['q'](f"select BroadcastTextID0 b from {ctx['TW']}.npc_text where ID=2543")[0]['b']
_t = ctx['q'](f"select male_text, female_text from {ctx['TW']}.broadcast_text where entry=%s", _b)[0]
S.gossip(AM, _t['male_text'] or _t['female_text'], [(0, 66993, 0, 0, [(47, 40561, 8, 0), (2, ctx['item'](60815), 1, 1)])])
S.stock_template(ANSIREM, gossip_menu_id=AM, npcflag=3)
S.btext(ANSIREM, 101, 66187)
S.row(ANSIREM, 0, 62, [AM, 0], A(56, [ctx['item'](60815), 1], 'invoker', note='Give the focus'))
S.row(ANSIREM, 0, 62, [AM, 0], A(1, [101, 0, 0], 'self', note='Say Line 101'))
S.row(ANSIREM, 0, 62, [AM, 0], A(5, [1], 'self', note='Emote Talk'))
S.row(ANSIREM, 0, 62, [AM, 0], A(72, [], 'invoker', note='Close Gossip'))

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them)
#      Pristine Thunderhead Horn (Thunderhead hippogryphs, Azshara), Pure Volcanic Ember (Un'Goro fire elementals),
#      Pure Aqua Orb (Sea Elementals / Sea Spray), Jadefire Felhorn (Jadefire satyrs, Felwood)
STOCK_DROPS = S.stock_quest_drops([60231, 60232, 60241, 60295])

SQL = S.sql()
