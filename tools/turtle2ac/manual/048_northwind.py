"""Northwind - Turtle's C++ (src/scripts/world/northwind.cpp) re-expressed as SmartAI.

1) Dark Iron Gunpowder Kegs ("Darker than Iron" 41677, Alliance / "Vile Dwarven Pigs" 41682, Horde).
   Using a keg while one of the two quests is in progress offers "Blow up the keg"; choosing it gives the quest credit
   (NPC 60070), the keg goes off 5 seconds later and comes back after 5 minutes. Turtle's C++ only checks the
   Alliance quest, which leaves the Horde quest impossible there; here both work.

2) The Jousting Grounds show: every 90 minutes Duke Sherwood announces one of five jousts. The two knights ride in,
   charge, the winner slams the loser, and the Duke and a spectator comment, with Turtle's timing and texts.

Run by build.py: `S` (lib.smartgen.Smart) and `ctx` are provided; the result is the module text SQL.
"""
from lib.sqlw import lit
A = S.raw

# ---------------------------------------------------------------------------------------------------------- kegs
KEG = 2020173
KEG_MENU = 9030589                     # Turtle text id 30589 + the module's text offset
KEG_TEXT = "<A single spark could obliterate everything around.>"
KEG_OPTION = "Blow up the keg"
S.names[KEG] = 'Dark Iron Gunpowder Keg'
NO_SELECT = 0x10                       # GO_FLAG_NOT_SELECTABLE while the fuse burns

S.extra_sql.append(
    f"DELETE FROM `npc_text` WHERE `ID`={KEG_MENU};\n"
    f"DELETE FROM `gossip_menu` WHERE `MenuID`={KEG_MENU};\n"
    f"DELETE FROM `gossip_menu_option` WHERE `MenuID`={KEG_MENU};\n"
    f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=15 AND `SourceGroup`={KEG_MENU};\n"
    "INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `Probability0`, `VerifiedBuild`) "
    f"VALUES ({KEG_MENU}, {lit(KEG_TEXT)}, {lit(KEG_TEXT)}, 1, 0);\n"
    f"INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES ({KEG_MENU}, {KEG_MENU});\n"
    "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
    "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
    f"VALUES ({KEG_MENU}, 0, 0, {lit(KEG_OPTION)}, 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);\n"
    # option shown while either keg quest is in progress (else groups = OR)
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, "
    "`ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(15, {KEG_MENU}, 0, 0, 0, 47, 0, 41677, 8, 0, 0, 0, 0, '', 'Keg - Darker than Iron in progress'),\n"
    f"(15, {KEG_MENU}, 0, 0, 1, 47, 0, 41682, 8, 0, 0, 0, 0, '', 'Keg - Vile Dwarven Pigs in progress');\n"
    # Turtle's keg is a button; a quest-giver type object opens the gossip menu in Data3
    f"UPDATE `gameobject_template` SET `type`=2, `Data0`=0, `Data1`=0, `Data2`=0, `Data3`={KEG_MENU}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={KEG};")

S.row(KEG, 1, 62, [KEG_MENU, 0], A(33, [60070], 'invoker', note='Quest Credit 60070'))
S.row(KEG, 1, 62, [KEG_MENU, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(KEG, 1, 62, [KEG_MENU, 0], A(105, [NO_SELECT], 'self', note='Fuse lit (not selectable)'))
S.row(KEG, 1, 62, [KEG_MENU, 0], A(80, [KEG * 100 + 1, 0, 0], 'self', note='Explode (action list)'))
boom = S.cast(27745, 'self', triggered=True)
S.actionlist(KEG * 100 + 1, [(5000, boom),
                             (0, A(41, [0, 300], 'self', note='Despawn, respawn in 5 minutes'))], 'Dark Iron Gunpowder Keg')

# ---------------------------------------------------------------------------------------------------------- jousting
DUKE, SPECTATOR = 62162, 62452
SPECTATOR_GUID = 2589385               # the spectator Turtle's script talks through
S.names.update({DUKE: 'Duke Sherwood', SPECTATOR: 'Jousting Spectator'})

# Turtle path points (x, y, z, o)
W_SPAWN, W_READY, W_CHARGE = (-7554.149902, 1074.199951, 50.003101, 5.452280), (-7534.890137, 1064.020020, 49.945896, 4.729720), \
    (-7534.830078, 1030.020020, 49.185257, 4.729720)
D_SPAWN, D_READY, D_CHARGE = (-7519.589844, 985.340027, 47.424301, 2.242360), (-7540.109863, 996.851990, 48.820190, 1.558290), \
    (-7540.229980, 1029.890015, 49.327801, 1.558290)
W_VICTORY, W_EXIT = (-7534.549805, 996.187012, 48.697422, 4.729720), (-7519.589844, 985.340027, 48.402988, 5.529270)

# (winner, defeated, Duke intro text, Duke victory text, Duke glory text) - Turtle broadcast texts
JOUSTS = [(62705, 62704, 6216210, 6216217, 6216222),      # Sir Lorenz of Theramore vs Fritz of Kul Tiras
          (62703, 62702, 6216211, 6216218, 6216223),      # Lumiere of Dalaran vs Sir Barnabas of Strom
          (62691, 62692, 6216212, 6216219, 6216224),      # Sir Reginald of Stormwind vs Rudolf of Strom
          (62694, 62695, 6216213, 6216220, 6216225),      # The Black Knight vs Halfar of Kul Tiras
          (62696, 62693, 6216214, 6216221, 6216226)]      # Ferdinand of Theramore vs Estanor of Dalaran
G_DETERMINE, G_ONWARD = 0, 1
S.btext(DUKE, G_DETERMINE, 6216215, 'yell')
S.btext(DUKE, G_ONWARD, 6216216, 'yell')
S.btext(SPECTATOR, 0, 6269001)
S.btext(SPECTATOR, 1, 6269002)
S.btext(SPECTATOR, 2, 6269003)
spec = dict(tgt='creature_guid', tp=[ctx['cguid'](SPECTATOR_GUID), SPECTATOR])

CHARGE, CHARGE_LEN, SLAM_LEAD, HIT_PAUSE = 24500, 4251, 500, 3000
IMMUNE = 0x100 | 0x200 | 0x20000       # immune to players, immune to NPCs, pacified
lists = []
for n, (win, lose, intro, victory, glory) in enumerate(JOUSTS):
    gi, gv, gg = 2 + n * 3, 3 + n * 3, 4 + n * 3
    S.btext(DUKE, gi, intro, 'yell')
    S.btext(DUKE, gv, victory, 'yell')
    S.btext(DUKE, gg, glory, 'yell')
    lid = DUKE * 100 + n + 1
    lists.append(lid)
    # the Duke: summons both knights and runs the commentary (times are Turtle's, from the start of the joust)
    S.actionlist(lid, [
        (0, S.summon(win, *W_SPAWN, kind=3, duration=43000)),
        (0, S.summon(lose, *D_SPAWN, kind=3, duration=43000)),
        (0, S.talk(gi)),
        (4500, A(1, [0, 0, 0], **spec, note='Spectator: dust')),
        (11500, S.talk(G_DETERMINE)),                                       # 16000
        (8500, S.talk(G_ONWARD)),                                           # 24500
        (0, A(1, [1, 0, 0], **spec, note='Spectator: here it comes')),
        (CHARGE_LEN + HIT_PAUSE, S.talk(gv)),                               # 31751
        (2249, A(1, [2, 0, 0], **spec, note='Spectator: praise')),          # 34000
        (2500, S.talk(gg))], 'Duke Sherwood - Joust')                       # 36500
    # the knights run their own paths from the moment they are summoned
    S.names.update({win: f'Jouster {win}', lose: f'Jouster {lose}'})
    for who in (win, lose):
        S.on(who, 'summoned', A(8, [0], 'self', note='Passive'), A(18, [IMMUNE], 'self', note='Immune + pacified'),
             A(59, [1], 'self', note='Run'),
             A(80, [who * 100 + 1, 0, 0], 'self', note='Joust path (action list)'))
    S.actionlist(win * 100 + 1, [
        (4500, A(69, [0, 0, 1], 'pos', xyz=W_READY, note='Ride to the lists')),
        (CHARGE - 4500, A(69, [0, 0, 1], 'pos', xyz=W_CHARGE, note='Charge')),
        (CHARGE_LEN - SLAM_LEAD, S.cast(42035, 'closest_creature', triggered=True, tp=[lose, 60, 0])),
        (SLAM_LEAD, A(51, [], 'closest_creature', tp=[lose, 60, 0], note='Unseat the opponent')),
        (HIT_PAUSE, A(69, [0, 0, 1], 'pos', xyz=W_VICTORY, note='Victory lap')),
        (36500 - (CHARGE + CHARGE_LEN + HIT_PAUSE), A(69, [0, 0, 1], 'pos', xyz=W_EXIT, note='Leave the lists'))],
        f'Jouster {win}')
    S.actionlist(lose * 100 + 1, [
        (4500, A(69, [0, 0, 1], 'pos', xyz=D_READY, note='Ride to the lists')),
        (CHARGE - 4500, A(69, [0, 0, 1], 'pos', xyz=D_CHARGE, note='Charge'))],
        f'Jouster {lose}')

# every 90 minutes, out of combat: one of the five jousts at random (Turtle: first one 90 minutes after spawn)
S.row(DUKE, 0, 1, [90 * 60000, 90 * 60000, 90 * 60000, 90 * 60000], A(87, lists + [0] * (6 - len(lists)), 'self', note='Start a random joust'))

SQL = S.sql()
