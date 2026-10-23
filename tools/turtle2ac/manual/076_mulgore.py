"""Mulgore - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp, random_scripts_3.cpp) as SmartAI.

- "Hookah for Your Troubles" (40003): using Shagu's Shisha (Bloodhoof Village) while the quest is open gives the credit
  (Turtle's dummy 60301) and the puff (spell 26389: 'Strawberry Schnapps' on Turtle, 'Moonglow Alcohol' in 3.3.5 - both
  the same drunk effect).
- "Bond Through Battle" (40536): Sunchaser, Trainer Tokala's young wind serpent at Red Cloud Roost, gets the option
  "Present the meat." while the quest is open; it turns hostile and fights, and at half health gives every player fighting
  it the credit (Turtle's dummy 60382), goes friendly again and leaves combat. Turtle has no menu text for it: the module's
  text is a short description (unverified wording).
- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Prairie Stalker Pelts
  (Kherra's 'A Trial of Sincerity'), Pristine Harpy Feathers (Windfury Harpies / Wind Witches, 'Eager Little One'), the
  Satchel of Mixed Herbs (Razormane Scouts, Barrens, 'Grand Herbal Theft').
- 3.3.5 spawns on ground Turtle reshaped (stock-spawn ground check against the shipped tiles): four creatures and three
  copper veins that would stand 1-10 yd under the new ground are lifted onto it. The rollback puts every row back.
Run by build.py with `S` and `ctx`.
"""
from lib.sqlw import lit
A = S.raw
SHISHA, SUNCHASER = 2010700, 60821
S.names.update({SHISHA: "Shagu's Shisha", SUNCHASER: 'Sunchaser'})
IN_PROGRESS = 8


def cond(src, group, entry, sid, ctype, v1, v2=0, v3=0, neg=0, comment=''):
    return ("INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
            "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
            "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
            f"({src}, {group}, {entry}, {sid}, 0, {ctype}, 0, {v1}, {v2}, {v3}, {neg}, 0, 0, '', {lit('mod-turtle-content: ' + comment)});")


# ---- Shagu's Shisha: "Hookah for Your Troubles" (40003)
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={SHISHA};")
S.extra_sql.append(f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=22 AND `SourceEntry`={SHISHA} AND `SourceId`=1;")
for a_ in (A(33, [60301], 'invoker', note='Quest Credit 60301'), A(85, [26389, 2], 'invoker', note='The puff (26389, cast by the player)'),
           A(72, [], 'invoker', note='Close Gossip')):
    i_ = S.row(SHISHA, 1, 64, [0], a_)
    S.extra_sql.append(cond(22, i_ + 1, SHISHA, 1, 47, 40003, IN_PROGRESS, 0, 0, 'Hookah for Your Troubles in progress'))

# ---- Sunchaser: "Bond Through Battle" (40536)
MENU = 9060821
S.gossip(MENU, '<Sunchaser watches you hungrily.>', [(0, 66754, 0, 0, [(47, 40536, IN_PROGRESS, 0)])])
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={MENU} WHERE `entry`={SUNCHASER};")
for a_ in (A(72, [], 'invoker', note='Close Gossip'), A(2, [14], 'self', note='Faction hostile'),
           A(5, [36], 'self', note='Emote attack'), A(49, [], 'invoker', note='Attack the player')):
    S.row(SUNCHASER, 0, 62, [MENU, 0], a_)
for a_ in (A(33, [60382], 'threat_list', note='Quest Credit 60382 (everyone fighting it)'), A(2, [0], 'self', note='Faction restored'),
           A(24, [], 'self', note='Evade')):
    S.row(SUNCHASER, 0, 2, [0, 50, 2000, 2000], a_)
S.on(SUNCHASER, 'evade', A(2, [0], 'self', note='Faction restored'))

# ---- Turtle's quest drops on 3.3.5 creatures
STOCK_DROPS = S.stock_quest_drops([60513, 60769, 60000])

# ---- 3.3.5 spawns lifted onto Turtle's new ground
for guid_, z_ in ((25869, 18.6), (25872, 21.7), (25922, 5.8), (19373, 62.6)):     # Windfury harpies (Suntail Pass), an Ornery Plainstrider
    S.stock_spawn('creature', guid_, position_z=z_)
for guid_, z_ in ((214209, 143.5), (214227, 32.6), (214229, 39.6)):                # Copper Veins
    S.stock_spawn('gameobject', guid_, position_z=z_)

SQL = S.sql()
