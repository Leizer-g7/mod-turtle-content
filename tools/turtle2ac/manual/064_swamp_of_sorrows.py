"""Swamp of Sorrows - Turtle's quest flavour (src/scripts/miscellaneous/random_scripts_1.cpp) re-expressed as SmartAI.

- "Noboru the Cudgel" (40030): when Magtoor (3.3.5) rewards the quest, the four Draenei Exiles around Sanv K'la's camp thank
  the player one after another (QuestRewarded_npc_magtoor). Magtoor keeps his own 3.3.5 SmartAI rows (ids < 100) and action lists
  (177600-177603; ours is 177650).
- Quest items Turtle added to the loot of 3.3.5 creatures (see STOCK_DROPS).
Run by build.py with `S` and `ctx`.
"""
A = S.raw
q = ctx['q']
MAGTOOR = 1776
EXILES = ((60421, 67022), (60422, 67023), (60423, 67024), (60424, 67025))
S.names.update({MAGTOOR: 'Magtoor', 60421: 'Draenei Exile', 60422: 'Draenei Exile', 60423: 'Draenei Exile', 60424: 'Draenei Exile'})

S.mark_stock(MAGTOOR)
for who_, say_ in EXILES:
    S.btext(who_, 0, say_)
steps = []
for n_, (who_, _) in enumerate(EXILES):
    # Turtle: 1 s after the reward, then every 2 s; each exile within 40 yd of the player says its line
    steps.append((1000 if n_ == 0 else 2000, A(1, [0, 0, 0], 'closest_creature', [who_, 40, 0], note=f'Draenei Exile {who_} - Say Line 0')))
    steps.append((0, A(5, [1], 'closest_creature', [who_, 40, 0], note=f'Draenei Exile {who_} - Emote Talk')))
S.on(MAGTOOR, 'reward_quest', A(80, [MAGTOOR * 100 + 50, 0, 0], 'self', note='The exiles give thanks (action list)'), ep=[40030])
S.actionlist(MAGTOOR * 100 + 50, steps, 'Magtoor')

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Noboru the Cudgel (his cudgel),
#      young crocolisks (leather), Tangled Horrors and the Marsh murlocs (Draenic Communication), Swamp Jaguars (Food Improvision),
#      Deathstrike Tarantulas (venom), the green dragonflight (The Magic of Dragons), Kazkaz the Unholy in the Sunken Temple (Tablet of Zef'ek)
STOCK_DROPS = S.stock_quest_drops([60130, 60133, 60134, 60135, 60170, 60280, 60281, 61798])

# ---- a 3.3.5 ore node (one pooled spot: a silver, gold or iron vein) on the mountainside behind Sorrowguard Keep, where Turtle
#      lowered the ground 11.8 yd (stock-spawn ground check): put back on the ground (Turtle has no node there)
for g_ in (208321, 208349, 208377):
    z_ = q(f"select position_z z from {ctx['AC']}.gameobject where guid=%s", g_)[0]['z']
    S.stock_spawn('gameobject', g_, position_z=round(z_ - 11.787, 3))

SQL = S.sql()
