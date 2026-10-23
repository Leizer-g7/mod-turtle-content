"""Frostmane Hollow - Turtle's C++ (src/scripts/dungeons/frostmane_hollow/boss_hailar_the_frigid.cpp) and one EventAI summon as SmartAI.

- Hailar the Frigid: "Embrace the cold..." on aggro, "Let the chill overcome..." at 50 %, "Destruction..." on death.
- The five Frostmane Ritualists (36519; Turtle only spawns this template around Hailar): passive, no melee, they never move
  or fight back, and keep channeling Turtle's Frostmane Ritual (41592: heals Hailar 150 per second each) on him.
  Stand-in: 3.3.5's Reconstruct (10260, the same channelled 150-per-second heal, used on Archaedas in Uldaman); a
  conditions row adds Hailar to its allowed targets (an "or" next to Archaedas; the rollback removes it). Its range is
  20 yd (the ritualists stand 12-15 yd from him) and it lasts 20 s: they start it again within 5 s.
- Frostmane Tamer: Turtle's Summon Ice Claw (33399, a guardian bear) does not exist in 3.3.5; the tamer summons 3.3.5's
  Ice Claw Bear (1196: same level, faction and model family as Turtle's Tamed Ice Claw Bear) on spawn and respawn, and the
  bear follows it (a 'just summoned' event on the 3.3.5 bear; the bears spawned in Dun Morogh are never summoned, so they
  do not change). The bear's corpse goes when it dies.
Run by build.py with `S` and `ctx`.
"""
A = S.raw
HAILAR, RITUALIST, TAMER, ICE_CLAW_BEAR = 63130, 36519, 82, 1196
RECONSTRUCT = 10260
S.names.update({HAILAR: 'Hailar the Frigid', RITUALIST: 'Frostmane Ritualist', TAMER: 'Frostmane Tamer', ICE_CLAW_BEAR: 'Ice Claw Bear'})

# ---- Hailar
for g_, t_ in enumerate((-1999992, -1999993, -1999994)):
    S.text(HAILAR, g_, t_)
S.on(HAILAR, 'aggro', S.talk(0))
S.on(HAILAR, 'hp', S.talk(1), ep=[0, 50, 0, 0], once=True)
S.on(HAILAR, 'death', S.talk(2))

# ---- the ritualists
for ev_ in ('created', 'reset', 'respawn'):
    S.on(RITUALIST, ev_, A(8, [0], 'self', note='Passive'), A(21, [0], 'self', note='No combat movement'),
         A(20, [0], 'self', note='No melee'))
chan = A(11, [RECONSTRUCT, 0], 'closest_creature', tp=[HAILAR, 100, 0], note=f'Cast {RECONSTRUCT} (Frostmane Ritual stand-in) on Hailar')
S.row(RITUALIST, 0, 1, [500, 500, 5000, 5000], chan)
S.row(RITUALIST, 0, 0, [500, 500, 5000, 5000], A(chan.t, chan.p, chan.tgt, chan.tp, note=chan.note))
S.extra_sql.append(
    f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=13 AND `SourceGroup`=1 AND `SourceEntry`={RECONSTRUCT} AND `ElseGroup`=1;\n"
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, "
    "`ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, "
    "`NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(13, 1, {RECONSTRUCT}, 0, 1, 31, 0, 3, {HAILAR}, 0, 0, 0, 0, '', 'mod-turtle-content: Frostmane Ritual stand-in, target Hailar');")

# ---- the tamers' bears
for ev_ in ('created', 'respawn'):
    S.on(TAMER, ev_, S.summon(ICE_CLAW_BEAR, kind=5, duration=0))
S.mark_stock(ICE_CLAW_BEAR)
S.on(ICE_CLAW_BEAR, 'summoned', A(29, [2, 90, 0, 0, 0], 'invoker', note='Follow the tamer'))

SQL = S.sql()
