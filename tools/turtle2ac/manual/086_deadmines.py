"""The Deadmines - Turtle's additions besides the spawns the build ports.
- "Captain Grayson's Revenge" (40396, Westfall): Cookie (3.3.5 boss) drops Grayson's Pendant (Turtle quest item, quest-only).
Jared Voss' lab, its mobs and the Masterpiece Harvester are ported by the build (Turtle EventAI -> SmartAI); the lab itself is
Turtle's extended Deadmines building (zones/086_deadmines.json ship_wmos).
Run by build.py with `S` and `ctx`.
"""
STOCK_DROPS = S.stock_quest_drops([60526])

SQL = S.sql()
