"""Burning Steppes - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) as SmartAI.

- "Hearing Orvak's Story" (40460): while the quest is in progress Orvak Sternrock offers "Tell me your story Orvak."; he tells
  it in four lines (1 s, 15 s, 30 s, 50 s) and the listener gets the credit (Turtle's dummy 60375) at 58 s. Turtle blocks a
  second telling with an invisible controller NPC; here his gossip flag is off while he talks (his quests stay available).
- "The True High Foreman" (40463) turned in to Orvak: he thanks you and salutes.
- Darkseer Geshtol: "Fueling the Blood Fury" (40492) - a line; (40493) - he enrages (3.3.5 Enrage 8599: Turtle's 24318 is
  Frenzy in 3.3.5), shouts his line and laughs 5 s later.
- "Raider's New Mount" (40497): with the Worg Cage (60720) and the quest in progress a Young Blackrock Worg offers "Capture
  the wolf into Worg Cage."; it gives the Caged Worg (60731), takes the empty cage and the worg despawns (normal respawn).
  Turtle checks for bag space first; SmartAI cannot, so with full bags the cage is used up without the worg (unverified;
  the player can buy/loot a cage again the same way as before).
- Karfang: "Take No Chances" (40508) - a line, then he, Molk and Councilor Vargek salute; "The Final Crack" (40509) - two
  lines and a bow.
- "Investigating Hateforge" (40486): Turtle's exploration trigger object at the quarry credits players within 30 yd.
- Turtle's quest drops on 3.3.5 creatures (10 items, see STOCK_DROPS).
- "To Purchase Secret Information" (40466) is Jabbey's (Gadgetzan) - in manual/071 with his other Turtle option.
- 3.3.5 ore/herb spawns on ground Turtle reshaped (stock-spawn ground check against the shipped tiles): a Thorium /
  Truesilver / Dark Iron pool point near Karfang Hold lifted 1.9 yd onto the new ground, a Mountain Silversage point on
  Azeroth_33_46 lowered 3 yd onto it. The rollback puts every row back.
Run by build.py with `S` and `ctx`.
"""
A, item = S.raw, ctx['item']
ORVAK, GESHTOL, WORG, KARFANG, MOLK, VARGEK = 60833, 60763, 60873, 60770, 60769, 60772
S.names.update({ORVAK: 'Orvak Sternrock', GESHTOL: 'Darkseer Geshtol', WORG: 'Young Blackrock Worg', KARFANG: 'Karfang'})
IN_PROGRESS = 8
EMOTE_TALK, EMOTE_BOW, EMOTE_LAUGH, EMOTE_SALUTE = 1, 2, 11, 66
GOSSIP = 1


def emote(e, tgt='self', tp=()):
    return A(5, [e], tgt, tp, note=f'Emote {e}')


# ---- Orvak Sternrock: "Hearing Orvak's Story" (40460), "The True High Foreman" (40463)
ORVAK_MENU = 41152                      # his Turtle gossip menu (text 60833), built by the zone
for g_, b_ in enumerate((66429, 66430, 66431, 66432, 66433)):
    S.btext(ORVAK, g_, b_)
S.extra_sql.append(
    "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
    "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
    f"VALUES ({ORVAK_MENU}, 0, 0, 'Tell me your story Orvak.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);\n"
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, "
    "`ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(15, {ORVAK_MENU}, 0, 0, 0, 47, 0, 40460, {IN_PROGRESS}, 0, 0, 0, 0, '', 'mod-turtle-content: Orvak - Hearing Orvak''s Story in progress');")
S.row(ORVAK, 0, 62, [ORVAK_MENU, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(ORVAK, 0, 62, [ORVAK_MENU, 0], A(83, [GOSSIP], 'self', note='No gossip while he talks'))
S.row(ORVAK, 0, 62, [ORVAK_MENU, 0], A(80, [ORVAK * 100 + 1, 0, 0], 'self', note="His story (action list)"))
S.actionlist(ORVAK * 100 + 1, [
    (1000, S.talk(0)), (0, emote(EMOTE_TALK)),
    (14000, S.talk(1)), (0, emote(EMOTE_TALK)),
    (15000, S.talk(2)), (0, emote(EMOTE_TALK)),
    (20000, S.talk(3)), (0, emote(EMOTE_TALK)),
    (8000, A(33, [60375], 'invoker', note='Quest Credit 60375 (Hearing Orvak\'s Story)')),
    (0, A(82, [GOSSIP], 'self', note='Gossip back'))], 'Orvak Sternrock - Story')
S.on(ORVAK, 'reset', A(82, [GOSSIP], 'self', note='Gossip back (after an interrupted story)'))
S.row(ORVAK, 0, 20, [40463], S.talk(4))
S.row(ORVAK, 0, 20, [40463], emote(EMOTE_SALUTE))

# ---- Darkseer Geshtol: "Fueling the Blood Fury" (40492, 40493)
S.btext(GESHTOL, 0, 66444)
S.btext(GESHTOL, 1, 66445)
S.row(GESHTOL, 0, 20, [40492], S.talk(0))
S.row(GESHTOL, 0, 20, [40492], emote(EMOTE_TALK))
S.row(GESHTOL, 0, 20, [40493], A(11, [8599, 2], 'self', note='Cast 8599 Enrage (stand-in for Turtle 24318)'))
S.row(GESHTOL, 0, 20, [40493], A(80, [GESHTOL * 100 + 1, 0, 0], 'self', note='Shout and laugh (action list)'))
S.actionlist(GESHTOL * 100 + 1, [(0, S.talk(1)), (0, emote(EMOTE_TALK)), (5000, emote(EMOTE_LAUGH))], 'Darkseer Geshtol - Blood Fury')

# ---- Young Blackrock Worg: "Raider's New Mount" (40497)
WORG_MENU = 41174                       # its Turtle gossip menu (text 60873), built by the zone
CAGE, CAGED = item(60720), item(60731)
S.extra_sql.append(
    "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
    "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
    f"VALUES ({WORG_MENU}, 0, 0, 'Capture the wolf into Worg Cage.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);\n"
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, "
    "`ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(15, {WORG_MENU}, 0, 0, 0, 47, 0, 40497, {IN_PROGRESS}, 0, 0, 0, 0, '', 'mod-turtle-content: Young Blackrock Worg - Raider''s New Mount in progress'),\n"
    f"(15, {WORG_MENU}, 0, 0, 0, 2, 0, {CAGE}, 1, 0, 0, 0, 0, '', 'mod-turtle-content: Young Blackrock Worg - carries a Worg Cage');")
S.row(WORG, 0, 62, [WORG_MENU, 0], A(56, [CAGED, 1], 'invoker', note='Give Caged Worg'))
S.row(WORG, 0, 62, [WORG_MENU, 0], A(57, [CAGE, 1], 'invoker', note='Take the Worg Cage'))
S.row(WORG, 0, 62, [WORG_MENU, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(WORG, 0, 62, [WORG_MENU, 0], A(41, [0, 0], 'self', note='Despawn (normal respawn)'))

# ---- Karfang: "Take No Chances" (40508), "The Final Crack" (40509)
for g_, b_ in enumerate((66446, 66447, 66448)):
    S.btext(KARFANG, g_, b_)
S.row(KARFANG, 0, 20, [40508], A(80, [KARFANG * 100 + 1, 0, 0], 'self', note='Honour Raz\'gol (action list)'))
S.actionlist(KARFANG * 100 + 1, [
    (0, S.talk(0)), (0, emote(EMOTE_TALK)),
    (2000, emote(EMOTE_SALUTE)),
    (0, emote(EMOTE_SALUTE, 'closest_creature', [MOLK, 15, 0])),
    (0, emote(EMOTE_SALUTE, 'closest_creature', [VARGEK, 15, 0]))], 'Karfang - Take No Chances')
S.row(KARFANG, 0, 20, [40509], A(80, [KARFANG * 100 + 2, 0, 0], 'self', note='Thank the hero (action list)'))
S.actionlist(KARFANG * 100 + 2, [
    (0, S.talk(1)), (0, emote(EMOTE_TALK)),
    (6000, S.talk(2)),
    (2000, emote(EMOTE_BOW))], 'Karfang - The Final Crack')

# ---- Hateforge Quarry: "Investigating Hateforge" (40486) - Turtle's exploration trigger object credits every player within 30 yd
HF_TRIGGER = 2010903
S.names[HF_TRIGGER] = 'Quest 40486 Trigger'
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={HF_TRIGGER};")
S.row(HF_TRIGGER, 1, 1, [2500, 2500, 2500, 2500], A(33, [60376], 'player_range', tp=[0, 30, 0], note='Quest Credit 60376 (players within 30 yd)'))

# ---- Turtle's quest drops on 3.3.5 creatures (Blackrock orcs, War Reavers, Thaurissan agents, Flamekin, Felguard Sentries,
#      Deathlash / Venomtip Scorpids; War Master Voone and Golem Lord Argelmach in their dungeons)
STOCK_DROPS = S.stock_quest_drops([60335, 60669, 60671, 60711, 60712, 60713, 60714, 60716, 60721, 60722])

# ---- 3.3.5 spawns on Turtle's new ground
for guid_, z_ in ((206179, 163.7), (206212, 163.7), (206245, 163.7),     # Thorium / Truesilver / Dark Iron pool point (Azeroth_37_46)
                  (206115, 205.6)):                                      # Mountain Silversage point (Azeroth_33_46)
    S.stock_spawn('gameobject', guid_, position_z=z_)

SQL = S.sql()
