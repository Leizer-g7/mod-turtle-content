"""Ashenvale - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp, _3.cpp, custom_exploration_triggers.cpp
and the gossip scripts of its hippogryph-master menus) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "Old Greypaw" (40197): Old Greypaw hears the player out, then turns on them (npc_old_greypaw); killing him is the objective.
- "Words of Wisdom" (40799): the four Kalimdor hippogryph masters (Teloren, Baritanas Skyriver, Daelyshia, Vesprystus - 3.3.5
  NPCs) each get Turtle's extra gossip option; it gives their credit (60031, 60028, 60029, 60030) and shows their advice.
- "The Family Name" (40800): Sharptalon (3.3.5 rare) talks to players on the quest and gives credit 60031.
- "Patience is the Key" / "Pressure is the Key" (40801 / 40807): Brolthan Ironglade and Commander Starwind tell their side over
  five gossip pages each; the last page gives credit 60032 / 60033 (npc_brolthan_ironglade, npc_commander_starwind).
- "What We Know" (70029): Turtle's exploration trigger object by the Barrow Den credits players within 30 yd (credit 70028).
Flavour: Daela Evermoon cries when "Old Greypaw" is turned in; reward lines of Brolthan (40806), Starwind (40812), Ardaen
Evermoon (40121), Norvok Hawkspear and Taupo Foreststrider (70022); Naxiar's aggro line.
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
GREYPAW, DAELA, ARDAEN, STARWIND, BROLTHAN, NORVOK, TAUPO, NAXIAR = 60470, 91287, 91288, 61143, 61147, 70022, 70020, 60409
TELOREN, BARITANAS, DAELYSHIA, VESPRYSTUS, SHARPTALON = 4407, 6706, 4267, 3838, 12676
TRIGGER_70029 = 3000101
S.names.update({GREYPAW: 'Old Greypaw', DAELA: 'Daela Evermoon', ARDAEN: 'Ardaen Evermoon', STARWIND: 'Commander Starwind',
                BROLTHAN: 'Brolthan Ironglade', NORVOK: 'Norvok Hawkspear', TAUPO: 'Taupo Foreststrider', NAXIAR: 'Naxiar',
                TELOREN: 'Teloren', BARITANAS: 'Baritanas Skyriver', DAELYSHIA: 'Daelyshia', VESPRYSTUS: 'Vesprystus',
                SHARPTALON: 'Sharptalon', TRIGGER_70029: 'Quest 70029 Custom Trigger'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def creature_gossip(entry, menu):
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={menu}, `npcflag`=`npcflag`|1 WHERE `entry`={entry};")


# ---- "Old Greypaw" (40197): he listens, then attacks (Turtle: SetFactionTemporary(14, RESTORE_COMBAT_STOP) after 5 s)
S.btext(GREYPAW, 0, 66668)
S.btext(GREYPAW, 1, 66669)
G0 = OFF + GREYPAW
S.gossip(G0, npc_text(60470), [(0, 66667, 0, 0, [(47, 40197, IN_PROGRESS, 0)])])
S.row(GREYPAW, 0, 62, [G0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(GREYPAW, 0, 62, [G0, 0], A(80, [GREYPAW * 100 + 1, 0, 0], 'self', note='Turns on the player (action list)'))
S.actionlist(GREYPAW * 100 + 1, [
    (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (4000, S.talk(1)),
    (0, A(5, [36], 'self', note='Emote Attack')),
    (0, A(2, [14], 'self', note='Hostile (faction 14)')),
    (0, A(49, [], 'invoker', note='Attack'))], 'Old Greypaw')
S.on(GREYPAW, 'evade', A(2, [0], 'self', note='Default faction again'))
S.on(GREYPAW, 'respawn', A(2, [0], 'self', note='Default faction again'))
creature_gossip(GREYPAW, G0)
# Daela Evermoon cries when the quest is turned in
S.on(DAELA, 'reward_quest', A(5, [18], 'self', note='Emote Cry'), ep=[40197])

# ---- "Patience is the Key" (40801) / "Pressure is the Key" (40807): two tellings, five pages each
for who_, first_, pages_, credit_ in ((BROLTHAN, 66790, [(30082, 66791), (30083, 66792), (30084, 66793), (30085, 66794), (30086, None)], 60032),
                                      (STARWIND, 66789, [(30087, 66795), (30088, 66796), (30089, 66797), (30090, 66794), (30091, None)], 60033)):
    m0 = OFF + who_
    S.gossip(m0, npc_text(who_), [(0, first_, 0, OFF + pages_[0][0], [(47, 40801, IN_PROGRESS, 0)]),
                                  (1, first_, 0, OFF + pages_[0][0], [(47, 40807, IN_PROGRESS, 0)])])
    for n_, (t_, opt_) in enumerate(pages_):
        S.gossip(OFF + t_, npc_text(t_), [(0, opt_, 0, OFF + pages_[n_ + 1][0], [])] if opt_ else [])
    S.row(who_, 0, 62, [OFF + pages_[3][0], 0], A(33, [credit_], 'invoker', note=f'Quest Credit {credit_}'))
    creature_gossip(who_, m0)
# their words when the relic quests are turned in
S.btext(BROLTHAN, 0, 66599)
S.on(BROLTHAN, 'reward_quest', S.talk(0), A(5, [1], 'self', note='Emote Talk'), ep=[40806])
S.btext(STARWIND, 0, 66600)
S.on(STARWIND, 'reward_quest', S.talk(0), A(5, [1], 'self', note='Emote Talk'), ep=[40812])

# ---- Ardaen Evermoon: "Alpha Aggression" (40121) turned in
S.btext(ARDAEN, 0, 67033)
S.on(ARDAEN, 'reward_quest', S.talk(0), ep=[40121])

# ---- Norvok Hawkspear (70022 turned in), then Taupo Foreststrider (within 10 yd) 3 s later
S.btext(NORVOK, 0, 66175)
S.on(NORVOK, 'reward_quest', S.talk(0), A(45, [1, 1], 'closest_creature', tp=[TAUPO, 10, 0], note='Taupo answers'), ep=[70022])
S.btext(TAUPO, 0, 66176)
S.on(TAUPO, 'data', A(80, [TAUPO * 100 + 1, 0, 0], 'self', note='Answers Norvok (action list)'), ep=[1, 1])
S.actionlist(TAUPO * 100 + 1, [(3000, A(5, [1], 'self', note='Emote Talk')), (0, S.talk(0))], 'Taupo Foreststrider')

# ---- Naxiar's aggro line
S.btext(NAXIAR, 0, 66189)
S.on(NAXIAR, 'aggro', S.talk(0))

# ---- "Words of Wisdom" (40799): the hippogryph masters' extra option (Turtle gave them menus 59012-59015: the 3.3.5 taxi
#      option plus this one). Teloren and Baritanas share 3.3.5 menu 6944 (Turtle's text 7778 + "Show me where I can fly."),
#      Vesprystus has 4302; Daelyshia has no menu in 3.3.5 and gets 6944 (the same text and taxi option Turtle gave her).
#      The option is added once per menu; each master's own SmartAI gives its credit and shows its advice.
WISDOM = "The young Moonfeather daughter in Forest Song requires your advice. She is struggling in her hippogryph handling training."
for menu_ in (6944, 4302):
    S.stock_gossip_option(menu_, 50, WISDOM, 0, [(47, 40799, IN_PROGRESS, 0)])
S.stock_template(DAELYSHIA, gossip_menu_id=6944, npcflag=8195)
for who_, menu_, credit_, text_ in ((TELOREN, 6944, 60031, 30077), (BARITANAS, 6944, 60028, 30078),
                                    (DAELYSHIA, 6944, 60029, 30079), (VESPRYSTUS, 4302, 60030, 30080)):
    S.mark_stock(who_)
    S.gossip(OFF + text_, npc_text(text_))
    S.row(who_, 0, 62, [menu_, 50], A(33, [credit_], 'invoker', note=f'Quest Credit {credit_}'))
    S.row(who_, 0, 62, [menu_, 50], A(98, [OFF + text_, OFF + text_], 'invoker', note='Their advice (gossip page)'))

# ---- "The Family Name" (40800): Sharptalon talks to players on the quest (Turtle: menu 41389, text 30081, shown and credited
#      while 40800 is in progress). Here the text is conditioned the same way; the credit counts only for players on the quest.
SH = OFF + 30081
S.gossip(SH, npc_text(30081))
S.extra_sql.append(f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=14 AND `SourceGroup`={SH};\n"
                   "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
                   "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
                   "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
                   f"(14, {SH}, {SH}, 0, 0, 47, 0, 40800, {IN_PROGRESS}, 0, 0, 0, 0, '', 'mod-turtle-content gossip text');")
S.rollback.append(f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=14 AND `SourceGroup`={SH};")
S.mark_stock(SHARPTALON)
S.stock_template(SHARPTALON, gossip_menu_id=SH, npcflag=1)
S.row(SHARPTALON, 0, 64, [], A(33, [60031], 'invoker', note='Quest Credit 60031'))

# ---- "What We Know" (70029): Turtle's exploration trigger object (custom_exploration_triggers.cpp) credits every player within 30 yd
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={TRIGGER_70029};")
S.row(TRIGGER_70029, 1, 1, [2500, 2500, 2500, 2500], A(33, [70028], 'player_range', tp=[0, 30, 0], note='Quest Credit 70028 (players within 30 yd)'))

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Ghostpaw Runners, Saltspittle
#      murlocs, the Bleakheart / Xavian / Felmusk satyrs (horns; Foul Effigy), Clattering and Spined Crawlers, Ashenvale bears,
#      Giant Foreststriders, the Shadethicket ancients, Diathorus the Seeker and the Demon Fall Canyon demons
STOCK_DROPS = S.stock_quest_drops([60110, 60313, 61150, 61151, 61152, 61153, 61157, 61159, 61160, 70021, 70022, 70026, 70027])

SQL = S.sql()
