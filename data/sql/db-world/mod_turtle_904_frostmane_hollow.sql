-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Frostmane Hollow fixes (Max + Claude, 2026-10-11)
-- Source: Turtle world DB (creature_spells, creature_ai_events) and
-- tortoise-wow-main/src/scripts/dungeons/frostmane_hollow. The C++ side is
-- src/bosses/zone_frostmane_hollow.cpp (ritualists, Cretin, Ice Elemental, Tamer).
--  63135 Ice Elemental: Turtle 33397 Frozen Mind (-16% attack and casting speed, 60 s, one
--        target). The converter used 12255 Curse of Tuten'kash (15 min area curse); the carrier
--        is now 7127 Wavering Will (single target, same auras), set to Turtle's values in C++.
--  63131 Battlemaster Ubukaz: Turtle casts 28131 Enrage at 25% (+25% damage, +40% attack
--        speed, 5 min). 28131 is the same spell in 3.3.5; the converter had used 8599.
-- Only rows still holding the converter's values are changed (re-running is harmless).

UPDATE `smart_scripts` SET `action_param1` = 7127,
    `comment` = 'Ice Elemental - In Combat - Cast 7127 (Turtle 33397 Frozen Mind carrier)'
    WHERE `source_type` = 0 AND `entryorguid` = 63135 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 12255;
UPDATE `smart_scripts` SET `action_param1` = 28131,
    `comment` = 'Battlemaster Ubukaz - Health 25% - Cast 28131 Enrage (Turtle EventAI 6313101)'
    WHERE `source_type` = 0 AND `entryorguid` = 63131 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 8599;
