"""Felwood - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without this the quest cannot be finished):
- By Any Means Necessary V (40401): when it is accepted, Niremius Darkwind channels for 25 s, speaks twice and the quest
  completes (QuestAccept_npc_niremius: Turtle calls CompleteQuest; here the quest's own objective, credit 60370).
Flavour: his apology when "By Any Means Necessary III" (40399) is rewarded (QuestRewarded_npc_niremius).
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS).
Run by build.py with `S` and `ctx`.
"""
A = S.raw
NIREMIUS = 60710
NOT_SELECTABLE = 0x2000000
S.names.update({NIREMIUS: 'Niremius Darkwind'})
q = ctx['q']

S.btext(NIREMIUS, 0, 66424)
S.btext(NIREMIUS, 1, 66718)
S.btext(NIREMIUS, 2, 66719)
# ---- By Any Means Necessary III rewarded: the apology (1 s later)
S.on(NIREMIUS, 'reward_quest', A(80, [NIREMIUS * 100 + 1, 0, 0], 'self', note='Apology (action list)'), ep=[40399])
S.actionlist(NIREMIUS * 100 + 1, [(1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk'))], 'Niremius Darkwind')
# ---- By Any Means Necessary V accepted: the ritual (Turtle casts 17447 on himself, unselectable for 26 s)
ritual = [(0, A(18, [NOT_SELECTABLE], 'self', note='Not selectable'))]
cast_ = S.cast(17447, 'self')
if cast_:
    ritual.append((0, cast_))
ritual += [(10000, S.talk(1)),
           (15000, A(5, [2], 'self', note='Emote Bow')), (0, S.talk(2)),
           (0, A(33, [60370], 'invoker', note='Quest Credit 60370')),
           (1000, A(19, [NOT_SELECTABLE], 'self', note='Selectable again'))]
S.on(NIREMIUS, 'accepted_quest', A(80, [NIREMIUS * 100 + 2, 0, 0], 'self', note='The ritual (action list)'), ep=[40401])
S.actionlist(NIREMIUS * 100 + 2, ritual, 'Niremius Darkwind')

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): the Jaedenar satyrs
#      (By Any Means Necessary I), Hazzas in the Sunken Temple (IV), the Felwood oozes (Tainted Ooze Samples, No Questions
#      Asked), the Irontree treants (Unhallowed Branches), the Ironbeak owls (Morrow in Felwood)
STOCK_DROPS = S.stock_quest_drops([60532, 60535, 61084, 61761, 61766])

# ---- a 3.3.5 herb spot (one pooled Mountain Silversage) on the hill Turtle lowered by 3.8 yd at Talonbranch Glade's new camp
#      (stock-spawn ground check): put back on the ground
for g_ in (211228,):
    z_ = q(f"select position_z z from {ctx['AC']}.gameobject where guid=%s", g_)[0]['z']
    S.stock_spawn('gameobject', g_, position_z=round(z_ - 3.8, 3))

SQL = S.sql()
