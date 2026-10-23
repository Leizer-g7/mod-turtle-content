-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: smart_scripts rows that AzerothCore skipped at startup (Errors.log, 2026-10-11).
-- Action 33 (quest credit) does not use param2; a value there makes the core drop the whole row,
-- so these three Lapidis Isle scenes never gave their quest credit.
UPDATE `smart_scripts` SET `action_param2` = 0
WHERE `source_type` = 9 AND `action_type` = 33
  AND `entryorguid` IN (124201, 254301, 9293601);   -- Karl Boran 60325, Ansirem 60327, Samual Boran 60326

-- Ighal'for 62671: action 80 param3 (allow override) only accepts 0 or 1; 2 made the core drop the row.
UPDATE `smart_scripts` SET `action_param3` = 0
WHERE `entryorguid` = 62671 AND `source_type` = 0 AND `id` = 107 AND `action_type` = 80;
