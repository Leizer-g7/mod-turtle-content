"""Eastern Plaguelands - Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): the
Scourge brains for Mavel Brightwood's 'It's All in Their Brains' (80710) from Cannibal / Gibbering Ghouls, Diseased Flayers,
Gangled Golems, Ghoul Berserkers, Bone Witches and Horgus the Ravager.
Turtle has no C++ for the zone's new NPCs (Crusader Larsarius' 'boss_crusader_larsarius' is not in the source: a plain elite).
Run by build.py with `S` and `ctx`.
"""
STOCK_DROPS = S.stock_quest_drops([53004])
SQL = S.sql()
