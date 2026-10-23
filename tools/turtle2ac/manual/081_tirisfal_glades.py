"""Tirisfal Glades - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) as SmartAI.

- "Ways of Magic" (40280): Duke Nargelas (Glenshire) hands over Darlthos' Jewelry Box and his letter when the quest is
  accepted (Turtle's QuestAccept_npc_duke_nargelas). Turtle drops the quest when the bags are full; here the items are just
  not given then (the player can abandon and take it again).
- "Attack from the Inside" (40099): using one of the Garrick Stead's Grain Sacks while carrying Grelda's Poison Vial gives a
  poisoned-sack credit (Turtle's dummy 60323); the sack despawns for 150 s (Turtle deactivates it for 150 s and shows a purple
  smoke object, left out).
- Turtle's quest drop on 3.3.5 creatures: Human Blood ('Virulence', 60113) from Tirisfal Farmers / Farmhands.
- 3.3.5 spawns on ground Turtle reshaped (stock-spawn ground check against the shipped tiles): murlocs, a wild turkey and two
  herbs at the Whispering Shore lifted onto the new ground, a copper vein lowered onto it. The rollback puts every row back.
Run by build.py with `S` and `ctx`.
"""
from lib.sqlw import lit
A, item = S.raw, ctx['item']
NARGELAS, SACK = 91712, 2010824
S.names.update({NARGELAS: 'Duke Nargelas', SACK: 'Grain Sack'})
IN_PROGRESS = 8


def cond(src, group, entry, sid, ctype, v1, v2=0, v3=0, neg=0, comment='', else_group=0):
    return ("INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
            "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
            "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
            f"({src}, {group}, {entry}, {sid}, {else_group}, {ctype}, 0, {v1}, {v2}, {v3}, {neg}, 0, 0, '', {lit('mod-turtle-content: ' + comment)});")


# ---- Duke Nargelas: "Ways of Magic" (40280)
S.extra_sql.append(f"UPDATE `creature_template` SET `ScriptName`='' WHERE `entry`={NARGELAS};")
for it_, nm_ in ((60189, "Darlthos' Jewelry Box"), (60190, "Nargelas's letter")):
    S.row(NARGELAS, 0, 19, [40280], A(56, [item(it_), 1], 'invoker', note=f'Give {nm_}'))

# ---- Grain Sacks: "Attack from the Inside" (40099)
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={SACK};")
S.extra_sql.append(f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=22 AND `SourceEntry`={SACK} AND `SourceId`=1;")
for a_ in (A(33, [60323], 'invoker', note='Quest Credit 60323 (a poisoned sack)'), A(41, [0, 150], 'self', note='Despawn, back in 150 s')):
    i_ = S.row(SACK, 1, 64, [0], a_)
    S.extra_sql.append(cond(22, i_ + 1, SACK, 1, 47, 40099, IN_PROGRESS, 0, 0, 'Attack from the Inside in progress'))
    S.extra_sql.append(cond(22, i_ + 1, SACK, 1, 2, item(5438), 1, 0, 0, "carries Grelda's Poison Vial"))

# ---- Turtle's quest drops on 3.3.5 creatures
STOCK_DROPS = S.stock_quest_drops([51822])

# ---- 3.3.5 spawns on Turtle's new ground (Whispering Shore, Azeroth_28_27)
for guid_, z_ in ((37905, 26.9), (38251, 23.3), (38252, 30.6), (41849, 20.3), (41851, 30.5), (243146, 23.3), (243175, 33.8), (243208, 26.7)):
    S.stock_spawn('creature', guid_, position_z=z_)
for guid_, z_ in ((201443, 30.4), (201543, 29.8), (201695, 30.9)):     # Silverleaf, Peacebloom, Copper Vein
    S.stock_spawn('gameobject', guid_, position_z=z_)

SQL = S.sql()
