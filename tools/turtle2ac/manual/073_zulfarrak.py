"""Zul'Farrak - the Farraki Arena (Turtle C++ src/scripts/dungeons/zulfarrak/farraki_arena.cpp) as SmartAI.

Champion Razjal the Quick's "I challenge you to combat." starts it (one run at a time: his gossip flag is off meanwhile):
  +5 s  Razjal: "You challenge me? ..."             +8 s  Kath'zen the Brutal turns hostile and attacks the challenger
  Juthza the Cunning follows when Kath'zen dies or 30 s later; Razjal himself when both are dead or 30 s after Juthza.
  Kath'zen enrages (15716) at 50 %. Razjal at 50 %: back to the arena's middle, channels (13236), takes no damage
  (invincible at 50 %), and after 5 s calls ten Sandfury Scorpids, one every 2 s from the four gates (2-minute summons that
  attack the nearest player); then he fights on. At 10 %: "I am the only champion ..." and Hellfire (11684, cast as
  triggered: no mana cost, as Turtle's zero-cost copy).
  The whole arena resets when any of the three leaves combat (wipe): scorpids gone, the dead respawned, factions back,
  Razjal's gossip back.
Differences from Turtle (SmartAI cannot do these): Razjal's crowd-control immunities during the scorpid phase are not
copied; the scorpid gates follow a fixed order instead of a random one; the fighters attack the challenger and the rest of
the group joins through normal aggro (Turtle put the whole group on their threat lists).
Zel'jeb the Ancient and the Sandfury Ritualists need nothing here: their EventAI and spell lists are converted by the build.
Run by build.py with `S` and `ctx`.
"""
A = S.raw
RAZJAL, KATHZEN, JUTHZA, SCORPID = 62498, 62496, 62497, 62499
HOSTILE = 14
S.names.update({RAZJAL: 'Champion Razjal the Quick', KATHZEN: "Kath'zen the Brutal", JUTHZA: 'Juthza the Cunning',
                SCORPID: 'Sandfury Scorpid'})
MENU = 62498                         # Razjal's gossip menu (converted from Turtle); option 0 "I challenge you to combat."
P_INTRO, P_KATHZEN, P_JUTHZA, P_RAZJAL, P_SANDS = 1, 2, 3, 4, 5
M = lambda *ph: sum(1 << (p - 1) for p in ph)      # event phase mask
ALL = M(P_INTRO, P_KATHZEN, P_JUTHZA, P_RAZJAL, P_SANDS)
CHANNEL_POS = (1512.21, 1016.05, 11.678, 2.899)
GATES = [(1498.65, 1030.937, 11.6), (1534.144, 1030.718, 11.826), (1536.583, 1005.965, 11.6277), (1499.567, 998.44, 11.756)]
NEAR = 150                           # yd: the arena is about 60 yd across

for e_, g_, bid in ((KATHZEN, 0, 6249601), (JUTHZA, 0, 6249701), (RAZJAL, 0, 6249803), (RAZJAL, 1, 6249804),
                    (RAZJAL, 2, 6249805), (RAZJAL, 3, 6249806)):
    S.btext(e_, g_, bid, 'yell')


def to(entry, act):
    """the action aimed at the nearest living creature of `entry`"""
    act.tgt, act.tp = 'closest_creature', [entry, NEAR, 0]
    return act


# ---- the challenge (gossip) and the intro
for a_ in (A(72, [], 'invoker', note='Close Gossip'), A(64, [1], 'invoker', note='Remember the challenger'),
           A(83, [1], 'self', note='No gossip during the fight'), A(63, [1, 0, 1], 'self', note='Deaths counter = 0'),
           A(22, [P_INTRO], 'self', note='Phase: intro'), A(67, [1, 5000, 5000, 0, 0, 100], 'self', note='Intro in 5 s')):
    S.row(RAZJAL, 0, 62, [MENU, 0], a_)
S.row(RAZJAL, 0, 59, [1], S.talk(0), phase=M(P_INTRO))
S.row(RAZJAL, 0, 59, [1], A(67, [2, 8000, 8000, 0, 0, 100], 'self', note="Kath'zen in 8 s"), phase=M(P_INTRO))

# ---- Kath'zen
for a_ in (to(KATHZEN, A(100, [1], note="Pass the challenger to Kath'zen")), to(KATHZEN, A(45, [1, 1], note="Kath'zen: fight")),
           A(22, [P_KATHZEN], 'self', note="Phase: Kath'zen"), A(67, [3, 30000, 30000, 0, 0, 100], 'self', note='Juthza in 30 s')):
    S.row(RAZJAL, 0, 59, [2], a_, phase=M(P_INTRO))

# ---- Juthza: 30 s after Kath'zen, or when Kath'zen dies (a fighter's death sends data 1 = 1)
JU_LIST, RJ_LIST, SANDS_LIST, RESET_LIST = RAZJAL * 100 + 1, RAZJAL * 100 + 2, RAZJAL * 100 + 3, RAZJAL * 100 + 4
S.actionlist(JU_LIST, [(0, to(JUTHZA, A(100, [1], note='Pass the challenger to Juthza'))), (0, to(JUTHZA, A(45, [1, 1], note='Juthza: fight'))),
                       (0, A(22, [P_JUTHZA], 'self', note='Phase: Juthza')),
                       (0, A(67, [4, 30000, 30000, 0, 0, 100], 'self', note='Razjal in 30 s'))], S.names[RAZJAL])
S.row(RAZJAL, 0, 59, [3], A(80, [JU_LIST, 0, 0], 'self', note='Juthza (action list)'), phase=M(P_KATHZEN))
S.row(RAZJAL, 0, 38, [1, 1], A(80, [JU_LIST, 0, 0], 'self', note="Kath'zen died: Juthza (action list)"), phase=M(P_KATHZEN))
S.row(RAZJAL, 0, 38, [1, 1], A(63, [1, 1, 0], 'self', note='Deaths counter + 1'))

# ---- Razjal: both fighters dead (counter 2) or 30 s after Juthza
S.actionlist(RJ_LIST, [(0, A(22, [P_RAZJAL], 'self', note='Phase: Razjal')), (0, A(2, [HOSTILE], 'self', note='Faction hostile')),
                       (0, A(8, [2], 'self', note='Aggressive')), (0, S.talk(1)),
                       (0, A(49, [], 'stored', tp=[1], note='Attack the challenger'))], S.names[RAZJAL])
S.row(RAZJAL, 0, 59, [4], A(80, [RJ_LIST, 0, 0], 'self', note='Razjal fights (action list)'), phase=M(P_JUTHZA))
S.row(RAZJAL, 0, 77, [1, 2], A(80, [RJ_LIST, 0, 0], 'self', note='Both fighters dead: Razjal fights (action list)'), phase=M(P_JUTHZA))

# ---- 50 %: the sands
gate_order = [0, 2, 1, 3, 0, 2, 1, 3, 0, 2]
steps = [(0, A(22, [P_SANDS], 'self', note='Phase: sands')), (0, A(8, [0], 'self', note='Passive')),
         (0, A(42, [0, 50], 'self', note='Invincible at 50 %')),
         (0, A(62, [209], 'self', xyz=CHANNEL_POS, note="To the arena's middle")),
         (0, S.cast(13236, 'self', triggered=True)), (0, S.talk(2))]
for n_, g_ in enumerate(gate_order):
    steps.append((5000 if n_ == 0 else 2000, S.summon(SCORPID, *GATES[g_], 0.0, 1, 120000)))
steps += [(0, A(28, [13236], 'self', note='Stop channeling')), (0, A(42, [0, 0], 'self', note='Not invincible')),
          (0, A(8, [2], 'self', note='Aggressive')), (0, A(22, [P_RAZJAL], 'self', note='Phase: Razjal')),
          (0, A(49, [], 'stored', tp=[1], note='Attack the challenger'))]
S.actionlist(SANDS_LIST, steps, S.names[RAZJAL])
S.row(RAZJAL, 0, 2, [0, 50, 0, 0], A(80, [SANDS_LIST, 0, 0], 'self', note='The sands (action list)'), phase=M(P_RAZJAL), flags=1)

# ---- 10 %: Hellfire
S.row(RAZJAL, 0, 2, [0, 10, 0, 0], S.talk(3), phase=M(P_RAZJAL), flags=1)
S.row(RAZJAL, 0, 2, [0, 10, 0, 0], S.cast(11684, 'self', triggered=True), phase=M(P_RAZJAL), flags=1)

# ---- reset (Razjal leaves combat, or a fighter does: data 9 = 1)
S.actionlist(RESET_LIST, [(0, A(41, [0], 'creature_range', tp=[SCORPID, 0, NEAR], note='Scorpids gone')),
                          (0, A(70, [], 'creature_range', tp=[KATHZEN, 0, NEAR], note="Kath'zen back")),
                          (0, A(70, [], 'creature_range', tp=[JUTHZA, 0, NEAR], note='Juthza back')),
                          (0, A(28, [13236], 'self', note='Stop channeling')), (0, A(42, [0, 0], 'self', note='Not invincible')),
                          (0, A(2, [0], 'self', note='Faction restored')), (0, A(8, [2], 'self', note='Aggressive')),
                          (0, A(63, [1, 0, 1], 'self', note='Deaths counter = 0')), (0, A(82, [1], 'self', note='Gossip again')),
                          (0, A(22, [0], 'self', note='Phase: idle'))], S.names[RAZJAL])
S.row(RAZJAL, 0, 7, [], A(80, [RESET_LIST, 0, 0], 'self', note='Arena reset (action list)'), phase=ALL)
S.row(RAZJAL, 0, 38, [9, 1], A(80, [RESET_LIST, 0, 0], 'self', note='Arena reset (action list)'), phase=ALL)

# ---- the two fighters
for e_ in (KATHZEN, JUTHZA):
    S.on(e_, 'data', A(2, [HOSTILE], 'self', note='Faction hostile'), S.talk(0), A(49, [], 'stored', tp=[1], note='Attack the challenger'),
         ep=[1, 1])
    S.on(e_, 'death', to(RAZJAL, A(45, [1, 1], note='Tell Razjal')))
    S.on(e_, 'evade', A(2, [0], 'self', note='Faction restored'), to(RAZJAL, A(45, [9, 1], note='Arena reset')))
S.on(KATHZEN, 'hp', S.cast(15716, 'self'), ep=[0, 50, 0, 0], once=True)

# ---- the scorpids: hostile, straight at the nearest player
S.on(SCORPID, 'summoned', A(2, [HOSTILE], 'self', note='Faction hostile'), A(49, [], 'closest_player', tp=[NEAR], note='Attack the nearest player'))

# ---- 3.3.5 spawns where Turtle cut the arena into the hill (stock-spawn ground check against the shipped tiles), as Turtle has them:
#      the Sandfury trolls Turtle removed from the arena floor and the old hill (two of them would float 7-11 yd over the
#      new basin), Sandarr Dunereaver moved out of the arena to Turtle's spot, and four that stand 1-2 yd under the new
#      ground lifted onto it. The rollback puts every row back.
for guid_ in (81613, 81616, 81617, 81620, 81621, 81634, 81636):
    S.stock_spawn_remove('creature', guid_)
S.stock_spawn('creature', 205802, position_x=1661.51, position_y=900.463, position_z=8.911)
for guid_, z_ in ((81614, 10.9), (81618, 10.6), (81619, 10.6), (81624, 10.0)):
    S.stock_spawn('creature', guid_, position_z=z_)

SQL = S.sql()
