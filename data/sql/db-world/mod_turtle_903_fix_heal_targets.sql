-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: healers healed their enemy (Max + Claude, 2026-10-11)
-- Turtle creature_spells castTarget 15 = "friendly injured" (targetParam1 = search radius,
-- targetParam2 = minimum % of health missing). The converter turned these heals into
-- "In Combat - cast on my victim", so the healer tried to heal the player (and failed).
-- Each row becomes SmartAI event 74 (friendly health %): same Turtle timers, the most
-- injured friend within the radius whose health is at or below 100 - targetParam2 %
-- (no radius in Turtle = the spell's range).
-- Only rows still holding the converter's values are changed (re-running is harmless).

UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 61345 AND `id` = 1 AND `action_type` = 11 AND `action_param1` = 25299 AND `event_type` = 0 AND `target_type` = 2; -- Rejuvenation
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 61391 AND `id` = 1 AND `action_type` = 11 AND `action_param1` = 10963 AND `event_type` = 0 AND `target_type` = 2; -- Greater Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 20, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62053 AND `id` = 1 AND `action_type` = 11 AND `action_param1` = 959 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 40, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62132 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 939 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 40, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62137 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 939 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62230 AND `id` = 1 AND `action_type` = 11 AND `action_param1` = 939 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62243 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 939 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 40, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62501 AND `id` = 2 AND `action_type` = 11 AND `action_param1` = 9840 AND `event_type` = 0 AND `target_type` = 2; -- Rejuvenation
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 20, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62650 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 9856 AND `event_type` = 0 AND `target_type` = 2; -- Regrowth
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 50, `event_param6` = 30, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 62768 AND `id` = 1 AND `action_type` = 11 AND `action_param1` = 10622 AND `event_type` = 0 AND `target_type` = 2; -- Chain Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 50, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 63132 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 8005 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 41, `event_param6` = 30, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 63136 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 913 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 91794 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 11642 AND `event_type` = 0 AND `target_type` = 2; -- Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 91811 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 11986 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 91856 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 11986 AND `event_type` = 0 AND `target_type` = 2; -- Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 91860 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 11642 AND `event_type` = 0 AND `target_type` = 2; -- Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92105 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 14900 AND `event_type` = 0 AND `target_type` = 2; -- Chain Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92106 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 14900 AND `event_type` = 0 AND `target_type` = 2; -- Chain Heal
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92107 AND `id` = 2 AND `action_type` = 11 AND `action_param1` = 9839 AND `event_type` = 0 AND `target_type` = 2; -- Rejuvenation
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 80, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92148 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 27606 AND `event_type` = 0 AND `target_type` = 2; -- Renew
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 80, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92154 AND `id` = 2 AND `action_type` = 11 AND `action_param1` = 10466 AND `event_type` = 0 AND `target_type` = 2; -- Lesser Healing Wave
UPDATE `smart_scripts` SET `event_type` = 74, `event_param5` = 99, `event_param6` = 40, `target_type` = 7
    WHERE `source_type` = 0 AND `entryorguid` = 92160 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 10467 AND `event_type` = 0 AND `target_type` = 2; -- Lesser Healing Wave
