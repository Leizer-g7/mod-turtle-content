"""Darnassus - Turtle's quest drops on 3.3.5 creatures.

- "Further Studies" (40369, Nessa Shadowsong in Rut'theran Village): Crustacean Carcasses from the Tide Crawlers and Young
  Reef Crawlers of Darkshore (quest-only loot rows; the rollback removes them).
Run by build.py with `S` and `ctx`.
"""
STOCK_DROPS = S.stock_quest_drops([60516])

SQL = S.sql()
