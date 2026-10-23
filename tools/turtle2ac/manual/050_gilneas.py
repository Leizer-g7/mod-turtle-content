"""Gilneas - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "The Upper Binding IV" (41014): Parnabus channels when the quest is accepted; 14 s later the player gets the credit.
- "In Memory of Franklin" (40982): the Grave of Franklin Blackheart offers "Place the necklace on the grave" while the
  quest is in progress and the necklace is in the bags; it takes the necklace, gives the credit, Harrison speaks.
- "The Rebellion" (40972): Lord Darius Ravenwood's three-page debrief gives the credit.
- Aliattan's Campfire (40908): "Inspect the fire more closely" makes Willow appear and attack.
- "Rendezvous with the Infiltrator" (40847): Greta Longpike's passphrases; the right one hands over her item.
Flavour: Dark Bishop Mordren (40993), Lord Darius Ravenwood (40956) and Orvan Darkeye (40880) when quests are handed in.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
GO_NO_SELECT = 0x10
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
PARNABUS, MORDREN, RAVENWOOD, ORVAN, GRETA, HARRISON, WILLOW = 61570, 61281, 61259, 61286, 61379, 61287, 61514
GRAVE, CAMPFIRE = 2020035, 2020026
S.names.update({PARNABUS: 'Parnabus', MORDREN: 'Dark Bishop Mordren', RAVENWOOD: 'Lord Darius Ravenwood', ORVAN: 'Orvan Darkeye',
                GRETA: 'Greta Longpike', HARRISON: 'Harrison Blackheart', WILLOW: 'Willow', GRAVE: 'Grave of Franklin Blackheart',
                CAMPFIRE: "Aliattan's Campfire"})

# ---- Parnabus: The Upper Binding IV (41014)
S.btext(PARNABUS, 0, 66621, 'emote')
S.btext(PARNABUS, 1, 66616)
S.on(PARNABUS, 'accepted_quest', A(80, [PARNABUS * 100 + 1, 0, 0], 'self', note='Binding (action list)'), ep=[41014])
S.actionlist(PARNABUS * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.cast(23017, 'self')),                                              # Arcane Channeling
    (10000, S.talk(0)),
    (2000, S.cast(1449, 'self')),                                            # Arcane Explosion
    (1500, S.talk(1)),
    (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (500, A(33, [60049], 'invoker', note='Quest Credit 60049'))], 'Parnabus')

# ---- Dark Bishop Mordren: Through Greater Magic (40993) handed in
for g, b in enumerate((66613, 66614, 66615)):
    S.btext(MORDREN, g, b)
S.on(MORDREN, 'reward_quest', A(80, [MORDREN * 100 + 1, 0, 0], 'self', note='The Eye (action list)'), ep=[40993])
S.actionlist(MORDREN * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (1000, S.cast(21157, 'self')),
    (4000, S.talk(1)),
    (5000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(92, [0], 'self', note='Interrupt')),
    (0, S.talk(2)), (0, A(5, [1], 'self', note='Emote Talk'))], 'Dark Bishop Mordren')

# ---- Orvan Darkeye: We Take It From The Living (40880) handed in
S.btext(ORVAN, 0, 66620, 'emote')
S.btext(ORVAN, 1, 66606)
S.on(ORVAN, 'reward_quest', A(80, [ORVAN * 100 + 1, 0, 0], 'self', note='Concoction (action list)'), ep=[40880])
S.actionlist(ORVAN * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, A(17, [69], 'self', note='Emote state Work')),
    (5000, A(17, [0], 'self', note='Emote state none')),
    (0, S.talk(0)),
    (3000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, S.talk(1))], 'Orvan Darkeye')

# ---- Lord Darius Ravenwood: The Fall and Rise of Greymane (40956) handed in + The Rebellion (40972) debrief
S.btext(RAVENWOOD, 0, 66625, 'yell')
S.on(RAVENWOOD, 'reward_quest', S.talk(0), A(5, [15], 'self', note='Emote Roar'), ep=[40956])
M0, M1, M2, M3 = OFF + 61259, OFF + 30123, OFF + 30124, OFF + 30125
S.gossip(M0, 61259, [(0, 66812, 0, M1, [(47, 40972, IN_PROGRESS, 0)])])
S.gossip(M1, 30123, [(0, 66813, 0, M2, [])])
S.gossip(M2, 30124, [(0, 66813, 0, M3, [])])
S.gossip(M3, 30125, [(0, 66814, 0, 0, [])])
S.row(RAVENWOOD, 0, 62, [M3, 0], A(33, [60046], 'invoker', note='Quest Credit 60046'))
S.row(RAVENWOOD, 0, 62, [M3, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M0}, `npcflag`=`npcflag`|1 WHERE `entry`={RAVENWOOD};")

# ---- Greta Longpike: Rendezvous with the Infiltrator (40847) - the right passphrase hands over item 61351
G0, G_OK, G_WRONG = OFF + 61379, OFF + 30109, OFF + 30108
S.gossip(G0, 61379, [(0, 66803, 0, G_OK, [(47, 40847, IN_PROGRESS, 0), (2, 61351, 1, 1)]),
                     (1, 66804, 0, G_WRONG, [(47, 40847, IN_PROGRESS, 0)]),
                     (2, 66805, 0, G_WRONG, [(47, 40847, IN_PROGRESS, 0)]),
                     (3, 66806, 0, 0, [(47, 40847, IN_PROGRESS, 0)])])
S.gossip(G_OK, 30109, [(0, 66806, 0, 0, [])])
S.gossip(G_WRONG, 30108, [(0, 66806, 0, 0, [])])
S.row(GRETA, 0, 62, [G0, 0], A(56, [61351, 1], 'invoker', note='Give the item'))
for m, o in ((G0, 3), (G_OK, 0), (G_WRONG, 0)):
    S.row(GRETA, 0, 62, [m, o], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={G0}, `npcflag`=`npcflag`|1 WHERE `entry`={GRETA};")

# ---- Grave of Franklin Blackheart: In Memory of Franklin (40982)
S.btext(HARRISON, 0, 66611)
GM = OFF + 30126
S.gossip(GM, 30126, [(0, 66815, 0, 0, [(47, 40982, IN_PROGRESS, 0), (2, 61632, 1, 0)])])
S.row(GRAVE, 1, 62, [GM, 0], A(57, [61632, 1], 'invoker', note='Take the necklace'))
S.row(GRAVE, 1, 62, [GM, 0], A(33, [60047], 'invoker', note='Quest Credit 60047'))
S.row(GRAVE, 1, 62, [GM, 0], A(1, [0, 0, 0], 'closest_creature', tp=[HARRISON, 40, 0], note='Harrison speaks'))
S.row(GRAVE, 1, 62, [GM, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data3`={GM}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={GRAVE};")

# ---- Aliattan's Campfire (40908): Willow appears and attacks (once every 2 minutes)
S.btext(WILLOW, 0, 66607)
CM = OFF + 30115
S.gossip(CM, 30115, [(0, 66811, 0, 0, [(47, 40908, IN_PROGRESS, 0)])])
S.row(CAMPFIRE, 1, 62, [CM, 0], A(12, [WILLOW, 2, 120000], 'pos', xyz=(-1717.13, 1811.13, 59.90, 1.02), note='Summon Willow'))
S.row(CAMPFIRE, 1, 62, [CM, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(CAMPFIRE, 1, 62, [CM, 0], A(105, [GO_NO_SELECT], 'self', note='Not usable while Willow is out'))
S.row(CAMPFIRE, 1, 62, [CM, 0], A(80, [CAMPFIRE * 100 + 1, 0, 0], 'self', note='Usable again later'))
S.actionlist(CAMPFIRE * 100 + 1, [(120000, A(106, [GO_NO_SELECT], 'self', note='Usable again'))], "Aliattan's Campfire")
S.on(WILLOW, 'summoned', S.talk(0), A(49, [], 'closest_player', tp=[50, 0, 0], note='Attack the nearest player'))
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data3`={CM}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={CAMPFIRE};")

# ---- rain (Turtle: 60 % in every season, like its game_weather row)
S.extra_sql.append("DELETE FROM `game_weather` WHERE `zone`=5179;\n"
                   "INSERT INTO `game_weather` (`zone`, `spring_rain_chance`, `spring_snow_chance`, `spring_storm_chance`, `summer_rain_chance`, "
                   "`summer_snow_chance`, `summer_storm_chance`, `fall_rain_chance`, `fall_snow_chance`, `fall_storm_chance`, `winter_rain_chance`, "
                   "`winter_snow_chance`, `winter_storm_chance`, `ScriptName`) VALUES (5179, 60, 0, 0, 60, 0, 0, 60, 0, 0, 60, 0, 0, '');")

SQL = S.sql()
