"""Balor - quest scripts that live in Turtle's C++ (src/scripts/world/balor.cpp), re-expressed as SmartAI.

"Explosives Make My Heart Go BOOM!" (41698): the barrel at the forge, the crate at the watchtower and the box at the
outer wall each offer "<Place the explosives.>" while that objective is still open; choosing it gives the objective's
credit (dummy NPCs 60075-60077) and closes the window.

"To The Darkest Places" (41694) needs no hand-written script: its credits are plain Turtle gossip scripts, which the
build converts by itself (gossip option -> SmartAI quest credit, option shown only while the quest is in progress).

Run by build.py: `S` (lib.smartgen.Smart) and `ctx` are provided; the result is the module text SQL.
"""
from lib.sqlw import lit
QUEST = 41698
TEXT = "<This seems to be a fitting place for Rufus' explosives.>"
OPTION = "<Place the explosives.>"
MENU_BASE = 4169801                     # Turtle's gossip text id for these objects (balor.cpp GOSSIP_EXPLOSIVES_TEXT)

# (object entry, name, credit NPC, objective index)
OBJECTS = [(2020178, 'Unremarkable Barrel', 60075, 0),
           (2020179, 'Unremarkable Crate', 60076, 1),
           (2020180, 'Unremarkable Box', 60077, 2)]

sql = []
menus = []
for n, (go, name, credit, idx) in enumerate(OBJECTS):
    menu = MENU_BASE + n
    menus.append(menu)
    S.names[go] = name
    # one menu per object, so each option can check its own objective
    sql.append(f"INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES ({menu}, {MENU_BASE});")
    sql.append("INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
               "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
               f"VALUES ({menu}, 0, 0, {lit(OPTION)}, 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);")
    # shown only while this objective has no credit yet (the condition is false when the quest is not in the log)
    sql.append("INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
               "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, "
               "`ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) "
               f"VALUES (15, {menu}, 0, 0, 0, 48, 0, {QUEST}, {idx}, 0, 0, 0, 0, '', '{name} - objective {idx + 1} of quest {QUEST} not done');")
    # quest-giver type objects open their gossip menu (Data3) when used
    sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data3`={menu}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={go};")
    S.row(go, 1, 62, [menu, 0], S.raw(33, [credit], 'invoker', note=f'Quest Credit {credit}'))
    S.row(go, 1, 62, [menu, 0], S.raw(72, [], 'invoker', note='Close Gossip'))

ml = ','.join(map(str, menus))
S.extra_sql.append(
    f"DELETE FROM `npc_text` WHERE `ID`={MENU_BASE};\n"
    f"DELETE FROM `gossip_menu` WHERE `MenuID` IN ({ml});\n"
    f"DELETE FROM `gossip_menu_option` WHERE `MenuID` IN ({ml});\n"
    f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=15 AND `SourceGroup` IN ({ml});\n"
    "INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `Probability0`, `VerifiedBuild`) "
    f"VALUES ({MENU_BASE}, {lit(TEXT)}, {lit(TEXT)}, 1, 0);\n" + '\n'.join(sql))

SQL = S.sql()
