-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Zul'Farrak fixes (Max + Claude, 2026-10-11)
--  62495 Zel'jeb the Ancient: Turtle casts 52695 Curse of Years at 50% (a 6 s area curse). The converter's
--        stand-in, 18267 Curse of Weakness (instant, one target, -2 damage), is removed: the curse is in
--        src/bosses/boss_zulfarrak.cpp. The 50% line and boss emote rows stay.
-- The Farraki Arena (62496-62498) now runs on the C++ port of Turtle's farraki_arena.cpp; the module's
-- SmartAI rows for it stay in the database (used only with TurtleContent.BossScripts = 0).
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 62495 AND `id` = 6 AND `action_type` = 11 AND `action_param1` = 18267;
