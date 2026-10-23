"""Moonwhisper Coast - Turtle's gossip/quest scripts that the build cannot convert, as SmartAI.

- Moro'gai K'la (Moro'gai Village), "Answers from Father" (41915): Turtle gossip script 6285002. He stops being
  interactible, Ar'lia appears beside him, he speaks his seven lines over 102 s and the player gets the credit (Turtle's
  dummy 60083). Turtle's summon flags (dataint2 57100) are not known here: Ar'lia stays for the scene (110 s).
- Riftmaster Ral'pekta (Moro'gai Village), "An Ill Omen" (41912): Turtle gossip script 6292002. He inspects and channels
  the crystal (Arcane Channeling 23017, the same spell in 3.3.5), and the Crystal Entity (the quest's kill objective)
  appears and attacks the player.
- Farmer Denphar, "Farm Raiders" (41946): Turtle quest start script 41946. Three waves of Fallen One Raiders, the last
  with Ghin'taru; when Ghin'taru dies Denphar cheers (Turtle's EventAI 6308901) and becomes interactible again. Turtle's
  scripts never complete the quest (it is an "event" quest with no objective; Turtle completes it elsewhere, perhaps in
  C++): here Ghin'taru's death completes it for players within 60 yd (unverified). Denphar is interactible again after
  5 minutes in any case, so a failed defence does not lock him.
- Elder Starstrider, "The Moonhoof Celebration" (42085): Turtle's C++ script npc_elder_starstrider is not in the Turtle
  source we have. Rebuilt from its texts (broadcast texts 2593100-2593114) and the Embodiment of Ancestors template
  (63202): he calls the tribe, the celebrators dance, the Embodiment appears in front of him and speaks, and the
  players within 40 yd get the quest. The order, timing and speakers are a guess (unverified).
Run by build.py with `S` and `ctx`.
"""
A = S.raw
IN_PROGRESS = 8
NPCFLAGS = 3                                         # gossip + quest giver
TALK, CHEER, KNEEL, STATE_DANCE = 1, 4, 16, 10
MORO, ARLIA, RIFT, CRYSTAL, DENPHAR, RAIDER, GHINTARU, STARSTRIDER, EMBODIMENT, CELEBRATOR = \
    62850, 571, 62920, 62989, 62922, 63082, 63089, 63083, 63202, 63093
S.names.update({MORO: "Moro'gai K'la", ARLIA: "Ar'lia", RIFT: "Riftmaster Ral'pekta", CRYSTAL: 'Crystal Entity',
                DENPHAR: 'Farmer Denphar', RAIDER: 'Fallen One Raider', GHINTARU: "Ghin'taru", STARSTRIDER: 'Elder Starstrider',
                EMBODIMENT: 'Embodiment of Ancestors', CELEBRATOR: 'Moonhoof Celebrator'})


def emote(e, tgt='self', tp=()):
    return A(5, [e], tgt, tp, note=f'Emote {e}')


def no_interact():
    return A(83, [NPCFLAGS], 'self', note='Not interactible')


def interact():
    return A(82, [NPCFLAGS], 'self', note='Interactible again')


# ---------------------------------------------------------------- Moro'gai K'la: "Answers from Father" (41915)
for g_, b_ in enumerate((6285003, 6285004, 6285005, 6285006, 6285007, 6285008, 6285009)):
    S.btext(MORO, g_, b_)
S.row(MORO, 0, 62, [MORO, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(MORO, 0, 62, [MORO, 0], A(80, [MORO * 100 + 1, 0, 0], 'self', note='Answers from Father (action list)'))
S.actionlist(MORO * 100 + 1, [
    (0, no_interact()),
    (0, S.talk(0)), (0, emote(TALK)),
    (0, S.summon(ARLIA, 6776.02, -6146.79, 68.92, 0.61, kind=3, duration=110000)),
    (6000, S.talk(1)), (0, emote(TALK)),
    (15000, S.talk(2)), (0, emote(TALK)),
    (15000, S.talk(3)), (0, emote(TALK)),
    (18000, S.talk(4)), (0, emote(TALK)),
    (15000, S.talk(5)), (0, emote(TALK)),
    (33000, S.talk(6)),
    (3000, A(33, [60083], 'invoker', note="Quest Credit 60083 (Confronted Moro'gai K'la)")),
    (0, interact())], "Moro'gai K'la - Answers from Father")
S.on(MORO, 'reset', interact())

# ---------------------------------------------------------------- Riftmaster Ral'pekta: "An Ill Omen" (41912)
for g_, (b_, chat_) in enumerate(((4292003, 'say'), (4292004, 'emote'), (4292005, 'say'), (4292006, 'emote'), (4292007, 'say'), (4292008, 'say'))):
    S.btext(RIFT, g_, b_, chat_)
S.row(RIFT, 0, 62, [RIFT, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(RIFT, 0, 62, [RIFT, 0], A(80, [RIFT * 100 + 1, 0, 0], 'self', note='An Ill Omen (action list)'))
S.actionlist(RIFT * 100 + 1, [
    (0, no_interact()),
    (0, S.talk(0)), (0, emote(TALK)),
    (14000, S.talk(1)),
    (6000, S.talk(2)), (0, emote(TALK)),
    (10000, S.talk(3)),
    (0, A(11, [23017, 0], 'self', note='Cast 23017 Arcane Channeling')),
    (7000, A(28, [23017], 'self', note='Stops channeling')),
    (0, S.talk(4)),
    (0, A(12, [CRYSTAL, 1, 120000, 1], 'pos', xyz=(6749.66, -6160.73, 32.46, 2.70), note=f'Summon {CRYSTAL} (attacks the player)')),
    (3000, S.talk(5)),
    (0, interact())], "Riftmaster Ral'pekta - An Ill Omen")
S.on(RIFT, 'reset', interact())

# ---------------------------------------------------------------- Farmer Denphar: "Farm Raiders" (41946)
for g_, b_ in enumerate((6292202, 6292203, 6292204, 6292205)):
    S.btext(DENPHAR, g_, b_)
SPOTS = ((6515.68, -6431.71, 29.64, 0.90), (6511.61, -6427.59, 29.78, 0.75), (6516.87, -6426.47, 29.30, 0.86))


def raider(entry, spot):
    return A(12, [entry, 1, 180000, 1], 'pos', xyz=SPOTS[spot], note=f'Summon {entry} (attacks the player)')


S.row(DENPHAR, 0, 19, [41946], A(80, [DENPHAR * 100 + 1, 0, 0], 'self', note='Farm Raiders (action list)'))
S.actionlist(DENPHAR * 100 + 1, [
    (0, no_interact()), (0, S.talk(0)),
    (0, raider(RAIDER, 0)), (0, raider(RAIDER, 1)),
    (60000, raider(RAIDER, 2)), (0, raider(RAIDER, 1)), (0, raider(RAIDER, 0)), (0, S.talk(1)),
    (60000, S.talk(2)), (0, raider(RAIDER, 0)), (0, raider(RAIDER, 1)), (0, raider(GHINTARU, 2)),
    (180000, interact())], 'Farmer Denphar - Farm Raiders')
S.on(DENPHAR, 'data', S.talk(3), emote(CHEER), interact(), ep=(1, 1))
# the build turned Turtle's EventAI 6308901 (Denphar's victory line, said by Denphar) into a line Ghin'taru says himself
S.extra_sql.append(f"DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid`={GHINTARU} AND `id` < 100;\n"
                   f"DELETE FROM `creature_text` WHERE `CreatureID`={GHINTARU} AND `GroupID` >= 50;")
S.on(GHINTARU, 'death',A(45, [1, 1], 'closest_creature', [DENPHAR, 150, 0], note='Tells Denphar the raid is over'),
     A(15, [41946], 'player_range', [0, 60], note='Farm Raiders done for players within 60 yd'))

# ---------------------------------------------------------------- Elder Starstrider: "The Moonhoof Celebration" (42085)
S.btext(STARSTRIDER, 0, 2593100, 'yell')
S.btext(STARSTRIDER, 1, 2593101, 'emote')
for g_, b_ in enumerate((2593102, 2593103, 2593104)):
    S.btext(STARSTRIDER, 2 + g_, b_)
for g_, b_ in enumerate((2593105, 2593106, 2593107, 2593108, 2593109, 2593110, 2593111, 2593112, 2593113, 2593114)):
    S.btext(EMBODIMENT, g_, b_, 'emote' if b_ == 2593107 else 'say')
DANCERS = ('creature_range', [CELEBRATOR, 0, 70])
S.row(STARSTRIDER, 0, 19, [42085], A(80, [STARSTRIDER * 100 + 1, 0, 0], 'self', note='The Moonhoof Celebration (action list)'))
S.actionlist(STARSTRIDER * 100 + 1, [
    (0, no_interact()),
    (0, S.talk(0)),
    (4000, S.talk(1)), (0, emote(KNEEL)),
    (0, A(17, [STATE_DANCE], *DANCERS, note='The celebrators dance')),
    (6000, S.talk(2)),
    (6000, S.talk(3)),
    (0, S.summon(EMBODIMENT, 8327.3, -5299.6, 47.5, 5.89, kind=3, duration=95000)),
    (6000, S.talk(4)), (0, emote(CHEER)),
    (70000, A(17, [0], *DANCERS, note='The celebrators stop dancing')),
    (0, A(15, [42085], 'player_range', [0, 40], note='The Moonhoof Celebration done for players within 40 yd')),
    (0, interact())], 'Elder Starstrider - The Moonhoof Celebration')
S.on(STARSTRIDER, 'reset', interact())
S.on(EMBODIMENT, 'summoned', A(80, [EMBODIMENT * 100 + 1, 0, 0], 'self', note='Speaks (action list)'))
steps_ = []
for g_ in range(10):
    steps_.append((3000 if g_ == 0 else 7000, S.talk(g_)))
S.actionlist(EMBODIMENT * 100 + 1, steps_, 'Embodiment of Ancestors - Blessing')

# ---------------------------------------------------------------- Elder Moonhoof: "Facing the Elder" dialogue
# His Turtle id 29479 is a 3.3.5 creature (config creature_id_remap): here he is 5029479. The build follows a gossip
# chain only 5 menus deep; the credit (Turtle gossip script 2947926, dummy 60090) sits on the 12th page.
ELDER = 5029479
S.names[ELDER] = 'Elder Moonhoof'
S.row(ELDER, 0, 62, [2947913, 0], A(33, [60090], 'invoker', note='Quest Credit 60090 (Elder Moonhoof listened)'))

# ---------------------------------------------------------------- "The Missing Caravans" (41970) and "Bound in Stone" (42051)
# Turtle credits these in C++ (area triggers 5660/5661 with at_moonwhisper_missing_caravans; the Bundle of Beads'
# Turtle-only spell 37098), which is not in the Turtle source we have. Here Turtle's own credit dummies stand,
# invisible, at the spots and give their credit to a player who comes within range (out of combat):
# the caravans at Turtle's two area triggers and at the third wagon, off the road at the camp the quest text mentions
# (8498, -5857; unverified); the shrines at the middle of their elementals' spawns, only while the player carries the
# Bundle of Beads (Turtle: "use the Bundle of Beads at each shrine"; here being there with it is enough - unverified).
GBASE = 9520000 + 9990                              # top of this zone's creature guid range (slot 42)
TRIGGER_FLAGS = 0x2 | 0x2000000                     # not attackable, not selectable
POINTS = [(51691, 8293.25, -5914.31, 3.97, 20, None), (51692, 8366.79, -5804.49, 1.23, 20, None), (51693, 8498.0, -5857.0, 0.17, 25, None),
          (60357, 7203.0, -5841.0, 68.8, 30, 42345), (60358, 8435.0, -5159.0, 11.3, 30, 42345), (60359, 8847.0, -5510.0, -14.0, 30, 42345)]
cre_col = ctx['cre_id']
S.extra_sql.append("DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=22 AND `SourceEntry` IN (60357, 60358, 60359) AND `SourceId`=0;")
for k_, (e_, x_, y_, z_, r_, need_) in enumerate(POINTS):
    g_ = GBASE + k_
    S.names[e_] = q_name = ctx['q'](f"select name from {ctx['TW']}.creature_template where entry=%s", e_)[0]['name']
    S.extra_sql.append(f"UPDATE `creature_template` SET `unit_flags`=`unit_flags`|{TRIGGER_FLAGS}, `flags_extra`=`flags_extra`|128 WHERE `entry`={e_};\n"
                       f"DELETE FROM `creature` WHERE `guid`={g_};\n"
                       f"INSERT INTO `creature` (`guid`, `{cre_col}`, `map`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, "
                       f"`orientation`, `spawntimesecs`, `wander_distance`, `MovementType`, `Comment`) VALUES "
                       f"({g_}, {e_}, 1, 1, 1, 0, {x_}, {y_}, {z_}, 0, 300, 0, 0, 'turtle 087_moonwhisper_coast: {q_name} (quest credit spot, manual)');")
    ev_ = S.row(e_, 0, 10, [2, r_, 5000, 5000, 1], A(33, [e_], 'invoker', note=f'Quest Credit {e_}'))
    if need_:
        S.extra_sql.append(
            "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, "
            "`ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
            f"(22, {ev_ + 1}, {e_}, 0, 0, 2, 0, {ctx['item'](need_)}, 1, 0, 0, 0, 0, '', 'mod-turtle-content: {q_name} - carries the Bundle of Beads');")

# ---------------------------------------------------------------- spawns below the shipped ground
# Two Moonstrider Fledglings stand 1.3 and 3.0 yd under the ground of the shipped tiles (Turtle's own server map has no
# height there to compare): lifted onto it.
for tw_guid_, z_ in ((2593433, 15.98), (2593460, 12.33)):
    S.extra_sql.append(f"UPDATE `creature` SET `position_z`={z_} WHERE `guid`={ctx['cguid'](tw_guid_)};")

SQL = S.sql()
