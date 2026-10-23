"""Dun Morogh - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp, custom_exploration_triggers.cpp) as SmartAI.

- "The Azurestone" (40338): Tholdan Mountainheart (Ironforge, the Mystic Ward) tells the tale of the Azurestone over 48 s
  (three lines), unselectable meanwhile, then gives the credit (Turtle's dummy 60347, a module credit template).
- Master Chemist Volterwhite: a line when "Mastering the Formula II" (40868) is turned in, a bow for part III (40869).
- "Curiosity Leads Us Forward" (39001): Turtle's exploration trigger object in the Gol'Bolar Quarry cave credits every player
  within 30 yd every 2.5 s (objective creature 20120, as Turtle has it).
- "Backup System Activation" (40856): the Alpha Channel Valve and the Reserve Pump Lever in Gnomeregan give the player's
  group their credits (Turtle's dummies 60042 / 60043).
- "Mastering the Formula II" (40868): Prospector Gehn (3.3.5) gives the Shipment of Gol'Bolar Ore through a menu option.
- Turtle's quest drops on 3.3.5 creatures (Rockjaw troggs, Old Icebeard, Frostmane Seers).
- Masey Wirefuse (Tinker Town): Turtle put her on the spot where it had removed Klockmort Spannerspan; 3.3.5 keeps
  Klockmort there, so she stands 2.5 yd to his side instead of inside him (same floor height; unverified in game).
- 3.3.5 spawns on ground Turtle reshaped (stock-spawn ground check against the shipped tiles): one creature and two copper
  veins that would sit 2-3 yd under the new ground are lifted onto it. The rollback puts every row back.
Run by build.py with `S` and `ctx`.
"""
A = S.raw
THOLDAN, VOLTERWHITE = 60629, 61436
CREDIT_40338 = 60347                 # Turtle's quest_40338_dummy_triger (extra_creature_templates)
TRIGGER_39001 = 3000102              # Quest 39001 Custom Trigger (custom_exploration_trigger)
S.names.update({THOLDAN: 'Tholdan Mountainheart', VOLTERWHITE: 'Master Chemist Volterwhite'})
IN_PROGRESS = 8                      # condition 47 quest state: incomplete
NOT_SELECTABLE = 0x2000000

# ---- Tholdan Mountainheart: the tale of the Azurestone
MENU = 9060629                       # the module's copy of his menu (Turtle text 60629) with the quest option
S.gossip(MENU, 60629, [(0, 66694, 0, 0, [(47, 40338, IN_PROGRESS, 0)])])
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={MENU} WHERE `entry`={THOLDAN};")
for g_, b_ in enumerate((66695, 66696, 66697)):
    S.btext(THOLDAN, g_, b_, 'say')
TALE = THOLDAN * 100 + 1
S.actionlist(TALE, [(1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote talk')),
                    (20000, S.talk(1)), (0, A(5, [1], 'self', note='Emote talk')),
                    (20000, S.talk(2)), (0, A(5, [1], 'self', note='Emote talk')),
                    (7000, A(33, [CREDIT_40338], 'stored', tp=[1], note=f'Quest Credit {CREDIT_40338}')),
                    (0, A(19, [NOT_SELECTABLE], 'self', note='Selectable again'))], S.names[THOLDAN])
for a_ in (A(72, [], 'invoker', note='Close Gossip'), A(64, [1], 'invoker', note='Remember the listener'),
           A(18, [NOT_SELECTABLE], 'self', note='Not selectable while telling the tale'), A(80, [TALE, 0, 0], 'self', note='The tale (action list)')):
    S.row(THOLDAN, 0, 62, [MENU, 0], a_)
S.on(THOLDAN, 'reset', A(19, [NOT_SELECTABLE], 'self', note='Selectable'))

# ---- Master Chemist Volterwhite
S.btext(VOLTERWHITE, 0, 66605, 'say')
S.on(VOLTERWHITE, 'reward_quest', S.talk(0), A(5, [1], 'self', note='Emote talk'), ep=[40868])
S.on(VOLTERWHITE, 'reward_quest', A(5, [2], 'self', note='Emote bow'), ep=[40869])

# ---- "Curiosity Leads Us Forward" (39001): the exploration trigger in the Gol'Bolar Quarry cave
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={TRIGGER_39001};")
S.row(TRIGGER_39001, 1, 1, [2500, 2500, 2500, 2500], A(33, [20120], 'player_range', tp=[0, 30, 0], note='Quest Credit 20120 (players within 30 yd)'))

# ---- "Backup System Activation" (40856, Gnomeregan): the Alpha Channel Valve and the Reserve Pump Lever (Turtle objects the
#      zone spawns in 3.3.5's Gnomeregan) each give their credit (Turtle's dummies 60042 / 60043) to the player and the group
for go_, menu_text, opt_text, credit_ in ((2020017, 30113, 66807, 60042), (2020018, 30114, 66808, 60043)):
    S.names[go_] = {2020017: 'Alpha Channel Valve', 2020018: 'Reserve Pump Lever'}[go_]
    M_ = 9000000 + menu_text
    S.gossip(M_, menu_text, [(0, opt_text, 0, 0, [(47, 40856, IN_PROGRESS, 0)])])
    S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data0`=0, `Data1`=0, `Data2`=0, `Data3`={M_}, "
                       f"`AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={go_};")
    S.row(go_, 1, 62, [M_, 0], A(33, [credit_], 'invoker_party', note=f'Quest Credit {credit_} (the group)'))
    S.row(go_, 1, 62, [M_, 0], A(72, [], 'invoker', note='Close Gossip'))

# ---- "Mastering the Formula II" (40868): Prospector Gehn (3.3.5, Gol'Bolar Quarry) hands over the Shipment of Gol'Bolar Ore.
#      3.3.5 gives him no menu: the module's copy of Turtle's (text 1255) with the option; the rollback restores his template.
GEHN, ORE = 1255, ctx['item'](61403)
S.names[GEHN] = 'Prospector Gehn'
GM = 9001255
S.gossip(GM, 1255, [(0, 66809, 0, 0, [(47, 40868, IN_PROGRESS, 0), (2, ORE, 1, 1)])])
S.stock_template(GEHN, gossip_menu_id=GM, npcflag=3)
S.btext(GEHN, 100, 66810, 'say')
for a_ in (A(72, [], 'invoker', note='Close Gossip'), A(56, [ORE, 1], 'invoker', note='Shipment of Gol\'Bolar Ore'),
           S.talk(100), A(5, [1], 'self', note='Emote talk')):
    S.row(GEHN, 0, 62, [GM, 0], a_)

# ---- Masey Wirefuse beside Klockmort Spannerspan (3.3.5) instead of on his spot
S.extra_sql.append(f"UPDATE `creature` SET `position_x`=-4816.5 WHERE `guid`={ctx['cguid'](2571625)};")

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): The Mercy of Humility (Rockjaw
#      Ambushers and Backbreakers), Old Icebeard's Beard, Snowvale Root (Frostmane Seers)
STOCK_DROPS = S.stock_quest_drops([61395, 51823, 61402])

# ---- 3.3.5 spawns lifted onto Turtle's new ground
S.stock_spawn('creature', 2276, position_z=394.3)          # Snow Leopard (1201) east of Kharanos
S.stock_spawn('gameobject', 205235, position_z=411.4)      # Copper Vein, same slope
S.stock_spawn('gameobject', 205392, position_z=435.4)      # Copper Vein, east of Gol'Bolar

SQL = S.sql()
