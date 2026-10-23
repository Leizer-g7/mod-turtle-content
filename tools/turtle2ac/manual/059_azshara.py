"""Azshara - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp, _3.cpp, custom_exploration_triggers.cpp
and quest start script 40247) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- Flaxwhisker Front: Analyzor 53G turning on the player ("The Analyzation Chip", 40044), Fendo Wobblefizz building the gear
  ("Wobble-free Fizz Gear", 40068).
- Keepers of Eldarath: Keeper Iselus's ritual on accepting "Staff of Eldara" (40247), the Way-Stones of Eldarath and Dorath
  (teleport with the Staff of Eldara), the Ashan Stone ("Restoring the Ley Lines", 40253).
- Bloodfist Point: Keeper Iselus's answer for Katokar ("A Blademaster's Request", 40285), Katokar's memory ("To Honor the
  Forgotten", 40289), Yharg'osh's ritual ("Ritual of the Farseer", 40293), the shore at Lake Mennar ("Mystery of Lake
  Mennar", 40295: Turtle's custom exploration trigger objects).
- Magus Bromley: the Spitelash Shrines ("Interfering Naga", 40124 - Turtle's Dispelling Scroll is a Turtle-only dummy spell
  whose handler is not in the source; here the shrine itself takes the scroll), his words after 40124 and 40127.
- Archmage Xylem: Tharessa turning on the player ("A Cause Of Concern", 41314), the Resonating Pedestal summoning the two
  arcane monstrosities ("Unveiling The Mystery", 41315).
- Akh Z'ador: his story ("Learn Of My Past", 41320) is offered only while the quest is in progress and completes it.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
ANALYZOR, FENDO, ISELUS, KATOKAR, YHARGOSH, BROMLEY, THARESSA = 91775, 91770, 91722, 92196, 92197, 91350, 61979
WAY_ELDARATH, WAY_DORATH, ASHAN, MENNAR, SHRINE, PEDESTAL = 2010849, 2010850, 2010851, 2010868, 2010801, 2020099
S.names.update({ANALYZOR: 'Analyzor 53G', FENDO: 'Fendo Wobblefizz', ISELUS: 'Keeper Iselus', KATOKAR: 'Katokar Bladewind',
                YHARGOSH: "Yharg'osh", BROMLEY: 'Magus Bromley', THARESSA: 'Tharessa', WAY_ELDARATH: 'Way-Stone of Eldarath',
                WAY_DORATH: 'Way-Stone of Dorath', ASHAN: 'Ashan Stone', MENNAR: 'Quest 40295 Trigger', SHRINE: 'Spitelash Shrine',
                PEDESTAL: 'Resonating Pedestal'})
q, TW, item = ctx['q'], ctx['TW'], ctx['item']


def npc_text(i, default=None):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these. Some menus the C++
    sends have no npc_text row in Turtle's DB (the client then shows its generic greeting): `default` is used there"""
    r_ = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)
    if not r_:
        assert default, f'npc_text {i} is not in the Turtle DB'
        return default
    b = r_[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def hostile(entry, list_id, lines=(), faction=14):
    """Turtle SetFactionTemporary(faction, RESTORE_COMBAT_STOP) + attack: hostile until the fight ends"""
    S.actionlist(list_id, [(0, A(72, [], 'invoker', note='Close Gossip'))] + [(0, a) for a in lines] + [
        (0, A(5, [36], 'self', note='Emote Attack')),
        (0, A(2, [faction], 'self', note=f'Hostile (faction {faction})')),
        (0, A(49, [], 'invoker', note='Attack'))], S.names[entry])
    S.on(entry, 'evade', A(2, [0], 'self', note='Default faction again'))
    S.on(entry, 'respawn', A(2, [0], 'self', note='Default faction again'))


def creature_gossip(entry, menu):
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={menu}, `npcflag`=`npcflag`|1 WHERE `entry`={entry};")


def go_gossip(entry, menu):
    """a Turtle button/door object opened by C++: here a gossip object (type 2) with the module's menu"""
    S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data0`=0, `Data1`=0, `Data2`=0, `Data3`={menu}, "
                       f"`AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={entry};")


# ---- Analyzor 53G: "The Analyzation Chip" (40044) - he turns on the player
S.btext(ANALYZOR, 0, 66820)
M = OFF + ANALYZOR
S.gossip(M, npc_text(91775), [(0, 66636, 0, 0, [(47, 40044, IN_PROGRESS, 0)])])
S.row(ANALYZOR, 0, 62, [M, 0], A(80, [ANALYZOR * 100 + 1, 0, 0], 'self', note='Turns hostile (action list)'))
hostile(ANALYZOR, ANALYZOR * 100 + 1, [S.talk(0)])
creature_gossip(ANALYZOR, M)

# ---- Fendo Wobblefizz: accepting "Wobble-free Fizz Gear" (40068) - he builds it
S.btext(FENDO, 0, 66821)
S.btext(FENDO, 1, 66822)
S.on(FENDO, 'accepted_quest', A(80, [FENDO * 100 + 1, 0, 0], 'self', note='Building the gear (action list)'), ep=[40068])
S.actionlist(FENDO * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, A(17, [69], 'self', note='Emote State Work')),
    (4000, S.talk(0)),
    (4000, S.talk(1)),
    (4000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(17, [0], 'self', note='Emote State None')),
    (0, A(33, [60319], 'invoker', note='Quest Credit 60319'))], 'Fendo Wobblefizz')

# ---- Keeper Iselus: Katokar's question (40285) and the ritual of "Staff of Eldara" (40247, Turtle start script 40247)
S.btext(ISELUS, 0, 66677)
S.btext(ISELUS, 1, 90261)
S.btext(ISELUS, 2, 90262)
S.btext(ISELUS, 3, 4450)
I0 = OFF + ISELUS
S.gossip(I0, npc_text(91722), [(0, 66676, 0, 0, [(47, 40285, IN_PROGRESS, 0)])])
S.row(ISELUS, 0, 62, [I0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(ISELUS, 0, 62, [I0, 0], A(80, [ISELUS * 100 + 1, 0, 0], 'self', note="Katokar's answer (action list)"))
S.actionlist(ISELUS * 100 + 1, [
    (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(33, [60340], 'invoker', note='Quest Credit 60340'))], 'Keeper Iselus')
creature_gossip(ISELUS, I0)
S.on(ISELUS, 'accepted_quest', A(80, [ISELUS * 100 + 2, 0, 0], 'self', note='The staff ritual (action list)'), ep=[40247])
rit = [(0, A(83, [2], 'self', note='Remove npcflag questgiver'))]
c1 = S.cast(23017, 'self')
if c1:
    rit.append((0, c1))
rit += [(5000, S.talk(1)), (15000, S.talk(2))]
c2 = S.cast(24171, 'self')
if c2:
    rit.append((13000, c2))
    rit.append((2000, S.talk(3)))
else:
    rit.append((15000, S.talk(3)))
rit += [(0, A(33, [60335], 'invoker', note='Quest Credit 60335')),
        (0, A(82, [2], 'self', note='Add npcflag questgiver'))]
S.actionlist(ISELUS * 100 + 2, rit, 'Keeper Iselus')

# ---- the Way-Stones of Eldarath and Dorath: with the Staff of Eldara they carry the player to the other stone
STAFF = item(60372)
TELE = {WAY_ELDARATH: (66678, (3814.92, -5526.18, 131.00, 3.70)), WAY_DORATH: (66679, (4011.45, -7131.67, 24.81, 3.70))}
for go_, (txt_, xyz_) in TELE.items():
    G = OFF + go_
    S.gossip(G, npc_text(100304, "An ancient stone hums with the ley lines of Eldarath."), [(0, txt_, 0, 0, [(2, STAFF, 1, 0)])])
    go_gossip(go_, G)
    S.row(go_, 1, 62, [G, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.row(go_, 1, 62, [G, 0], A(62, [1], 'invoker', xyz=xyz_, note='Teleport to the other Way-Stone'))

# ---- the Ashan Stone: "Restoring the Ley Lines" (40253)
G = OFF + ASHAN
S.gossip(G, npc_text(100400, "The stone is cold to the touch."), [(0, 66680, 0, 0, [(47, 40253, IN_PROGRESS, 0)])])
go_gossip(ASHAN, G)
S.row(ASHAN, 1, 62, [G, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(ASHAN, 1, 62, [G, 0], A(33, [60336], 'invoker', note='Quest Credit 60336'))

# ---- Katokar Bladewind: "To Honor the Forgotten" (40289)
S.btext(KATOKAR, 0, 66688)
K0 = OFF + KATOKAR
S.gossip(K0, npc_text(92196), [(0, 66687, 0, 0, [(47, 40289, IN_PROGRESS, 0)])])
S.row(KATOKAR, 0, 62, [K0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(KATOKAR, 0, 62, [K0, 0], A(80, [KATOKAR * 100 + 1, 0, 0], 'self', note='The memory (action list)'))
S.actionlist(KATOKAR * 100 + 1, [
    (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(33, [60341], 'invoker', note='Quest Credit 60341'))], 'Katokar Bladewind')
creature_gossip(KATOKAR, K0)

# ---- Yharg'osh: accepting "Ritual of the Farseer" (40293) - he walks to the cliff, calls the winds and kneels
S.btext(YHARGOSH, 0, 66428, 'yell')
for g_, b_ in enumerate((66416, 66417, 66418, 66419, 66420), 1):
    S.btext(YHARGOSH, g_, b_)
P1, P2, P3, P4 = (4993.68, -6042.01, 89.09, 2.05), (4985.88, -6026.60, 88.69, 0.61), (4993.11, -6020.67, 89.27, 0.14), (5009.55, -6018.99, 86.59, 0.11)
S.on(YHARGOSH, 'accepted_quest', A(80, [YHARGOSH * 100 + 1, 0, 0], 'self', note='The ritual (action list)'), ep=[40293])
S.actionlist(YHARGOSH * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, A(69, [0, 0, 0], 'pos', xyz=P1, note='Walk')),
    (1300, A(69, [0, 0, 0], 'pos', xyz=P2, note='Walk')),
    (4700, A(69, [0, 0, 0], 'pos', xyz=P3, note='Walk')),
    (4000, A(69, [0, 0, 0], 'pos', xyz=P4, note='Walk to the edge')),
    (8000, S.talk(0)), (0, A(5, [22], 'self', note='Emote Shout')),
    (8000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (8000, S.talk(2)), (0, A(5, [1], 'self', note='Emote Talk')),
    (8000, S.talk(3)), (0, A(5, [1], 'self', note='Emote Talk')),
    (8000, S.talk(4)), (0, A(5, [1], 'self', note='Emote Talk')),
    (8000, S.talk(5)), (0, A(17, [68], 'self', note='Emote State Kneel')),
    (8000, A(17, [0], 'self', note='Emote State None')),
    (0, A(69, [0, 0, 0], 'pos', xyz=(4993.11, -6020.67, 89.27, 3.28), note='Walk back')),
    (4700, A(69, [0, 0, 0], 'pos', xyz=(4985.88, -6026.60, 88.69, 3.75), note='Walk back')),
    (4000, A(69, [0, 0, 0], 'pos', xyz=(4994.63, -6041.35, 89.09, 4.20), note='Walk back')),
    (3800, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (500, A(69, [0, 0, 0], 'pos', xyz=(4992.68, -6045.22, 89.02, 2.46), note='Home')),
    (0, A(33, [60342], 'invoker', note='Quest Credit 60342'))], "Yharg'osh")

# ---- Lake Mennar: "Mystery of Lake Mennar" (40295) - Turtle's exploration trigger objects credit every player within 30 yd
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={MENNAR};")
S.row(MENNAR, 1, 1, [2500, 2500, 2500, 2500], A(33, [60343], 'player_range', tp=[0, 30, 0], note='Quest Credit 60343 (players within 30 yd)'))

# ---- the Spitelash Shrines: "Interfering Naga" (40124) - the scroll is read at a shrine
G = OFF + SHRINE
SCROLL = item(60113)
S.gossip(G, "The shrine hums with naga magic.", [(0, "<Read Bromley's Dispelling Scroll at the shrine.>", 0, 0,
                                                    [(47, 40124, IN_PROGRESS, 0), (2, SCROLL, 1, 0)])])
go_gossip(SHRINE, G)
S.row(SHRINE, 1, 62, [G, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(SHRINE, 1, 62, [G, 0], A(33, [60312], 'invoker', note='Quest Credit 60312'))

# ---- Magus Bromley: his words after "Interfering Naga" (40124) and "The Dampening Must End" (40127)
S.btext(BROMLEY, 0, 67017)
S.btext(BROMLEY, 1, 67018)
S.btext(BROMLEY, 2, 67034)
S.on(BROMLEY, 'reward_quest', S.talk(2), ep=[40127])
S.on(BROMLEY, 'reward_quest', A(80, [BROMLEY * 100 + 1, 0, 0], 'self', note='The scroll (action list)'), ep=[40124])
bl = [(0, S.talk(0))]
c3 = S.cast(23017, 'self')
if c3:
    bl.append((0, c3))
bl += [(6000, S.talk(1)), (0, A(5, [274], 'self', note='Emote No'))]
S.actionlist(BROMLEY * 100 + 1, bl, 'Magus Bromley')

# ---- Tharessa: "A Cause Of Concern" (41314) - she turns on the player
S.btext(THARESSA, 0, 30180)
T0 = OFF + THARESSA
S.gossip(T0, npc_text(61979), [(0, 30179, 0, 0, [(47, 41314, IN_PROGRESS, 0)])])
S.row(THARESSA, 0, 62, [T0, 0], A(80, [THARESSA * 100 + 1, 0, 0], 'self', note='Turns hostile (action list)'))
hostile(THARESSA, THARESSA * 100 + 1, [S.talk(0)], faction=16)
creature_gossip(THARESSA, T0)

# ---- the Resonating Pedestal: "Unveiling The Mystery" (41315) - two arcane monstrosities, while the player lacks the remains
G = OFF + PEDESTAL
S.gossip(G, npc_text(30181), [(0, 30182, 0, 0, [(47, 41315, IN_PROGRESS, 0), (2, item(41377), 1, 1)])])
S.extra_sql.append(f"UPDATE `gameobject_template` SET `Data3`={G}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={PEDESTAL};")
S.row(PEDESTAL, 1, 62, [G, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(PEDESTAL, 1, 62, [G, 0], S.summon(61980, 3925.58, -4733.38, 266.56, 1.60, kind=1, duration=15000))
S.row(PEDESTAL, 1, 62, [G, 0], S.summon(61981, 3941.27, -4719.79, 266.57, 4.36, kind=1, duration=15000))

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Mistwing Rogues (Mistwing Horn),
#      the blue dragonflight of Azshara (Azure Scale, Azure Crystal), Coralshell Lurkers (Pristine Lurker Shell), the Legashi satyrs
#      (Aged Deep-Rod, Legashi Horns, Akh Z'ador's Riftwalker Cane), Immol'thar in Dire Maul (Pure Ley Essence), Jaedenar demons in
#      Felwood (Fel Conduit), Mosshoof stags (Stag Flank, Mosshoof Antler), Thunderhead hippogryphs (Thunderhead Claw), the Blood Elf
#      surveyors (Vermillion Crystal), Jammal'an the Prophet in the Sunken Temple (Mojo of Jammal'an), Spitelash Sirens (Siren Brain)
#      and the makrura of the coast (Zesty Makrura Claw) for Akh Z'ador's "Rift Fatigue"
STOCK_DROPS = S.stock_quest_drops([60141, 60158, 60325, 60328, 60332, 60396, 60399, 60401, 60402, 60403, 41374, 41375, 41383, 41384,
                                   41380, 41381])

# ---- a 3.3.5 Coralshell Lurker on the sea floor that Turtle raised 1.5 yd at Flaxwhisker Front (ground check): moved onto it
z_ = q(f"select position_z z from {ctx['AC']}.creature where guid=%s", 36088)[0]['z']
S.stock_spawn('creature', 36088, position_z=round(z_ + 1.5, 3))

# ---- Akh Z'ador: "Learn Of My Past" (41320). His story (menu 60077 option 0 -> ... -> 30191 "Continue.", whose Turtle
#      script completes the quest; the build ports that script) is offered only while the quest is in progress. Turtle's
#      condition also checks that he is sitting (a stand-state condition 3.3.5 has no counterpart for): only the quest part is kept.
S.extra_sql.append(
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
    "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
    "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(15, 60077, 0, 0, 0, 47, 0, 41320, {IN_PROGRESS}, 0, 0, 0, 0, '', 'mod-turtle-content: Learn Of My Past in progress');")
# the quest has no objectives: Turtle's "exploration or event" flag (the build keeps only the repeatable bit) makes it wait for the story
S.extra_sql.append("UPDATE `quest_template_addon` SET `SpecialFlags`=`SpecialFlags`|2 WHERE `ID`=41320;")

SQL = S.sql()
