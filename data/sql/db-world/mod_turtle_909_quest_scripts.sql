-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: quest NPC / object script audit against Turtle's C++ (Max + Claude, 2026-10-11)
-- Turtle's scripts compared: src/scripts/miscellaneous/random_scripts_1.cpp and random_scripts_3.cpp.
-- C++ side of this audit: src/bosses/zone_quest_scripts.cpp.

-- 52066 Barthos Thundercrank: Turtle HandleEmote(69) is the 'use standing' emote STATE (kept until
--   EMOTE_ONESHOT_NONE at 14 s), not a one-shot emote.
UPDATE `smart_scripts` SET `action_type` = 17, `comment` = 'Barthos Thundercrank - Emote State Use Standing' WHERE `source_type` = 9 AND `entryorguid` = 5206601 AND `id` = 1 AND `action_type` = 5;
UPDATE `smart_scripts` SET `action_type` = 17, `comment` = 'Barthos Thundercrank - Emote State None' WHERE `source_type` = 9 AND `entryorguid` = 5206601 AND `id` = 7 AND `action_type` = 5;

-- 60467 Arch Hydromancer Lapidis: the death line was said twice (EventAI row 3 and gossip-script row 101).
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 60467 AND `id` = 101;

-- 60949/60950/60951 Privates Talmand, Sleightor, Valnor: the converter gave them Sunchaser's menu 9060821
--   ("Present the meat.", quest 40536). Turtle: "Ask him about Tauren presence in Dustwallow Marsh." while
--   quest 40554 "The Shield's Owner" is in progress (same greeting text 60821).
DELETE FROM `gossip_menu` WHERE `MenuID` = 9060949;
INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES (9060949, 9060821);
DELETE FROM `gossip_menu_option` WHERE `MenuID` = 9060949;
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(9060949, 0, 0, 'Ask him about Tauren presence in Dustwallow Marsh.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 15 AND `SourceGroup` = 9060949;
INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
(15, 9060949, 0, 0, 0, 47, 0, 40554, 8, 0, 0, 0, 0, '', 'mod-turtle-content gossip option');
UPDATE `creature_template` SET `gossip_menu_id` = 9060949 WHERE `entry` IN (60949, 60950, 60951);
UPDATE `smart_scripts` SET `event_param1` = 9060949 WHERE `source_type` = 0 AND `entryorguid` IN (60949, 60950, 60951) AND `event_type` = 62 AND `event_param1` = 9060821;

-- 61143 Commander Starwind / 61147 Brolthan Ironglade: Turtle shows ONE option when quest 40801 OR 40807 is in
--   progress; the module had two identical options (one per quest). One option, two condition groups.
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (9061143, 9061147) AND `OptionID` = 1;
UPDATE `conditions` SET `SourceEntry` = 0, `ElseGroup` = 1 WHERE `SourceTypeOrReferenceId` = 15 AND `SourceGroup` IN (9061143, 9061147) AND `SourceEntry` = 1;

-- Endless channels: 13236 / 23017 last until something stops them. Turtle stops them with a second cast
--   (5906 / 1449) that the converter left out, so these NPCs kept channeling forever.

-- 60446 Insom'ni, quest 40171 (key) and 40271 (potion): channel stops at 18 s.

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6044602;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6044602, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Not selectable'),
(6044602, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 13236, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Cast 13236'),
(6044602, 9, 2, 0, 0, 0, 100, 0, 18000, 18000, 0, 0, 0, 0, 5, 273, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Emote Yes'),
(6044602, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Stop channeling'),
(6044602, 9, 4, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Selectable again'),
(6044602, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 56, 60244, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Give the attuned key'),
(6044602, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Say Line 3'),
(6044602, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Emote Talk');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6044604;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6044604, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Not selectable'),
(6044604, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 13236, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Cast 13236'),
(6044604, 9, 2, 0, 0, 0, 100, 0, 18000, 18000, 0, 0, 0, 0, 5, 273, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Emote Yes'),
(6044604, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Stop channeling'),
(6044604, 9, 4, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Selectable again'),
(6044604, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 56, 60345, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Give the potion'),
(6044604, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Say Line 8'),
(6044604, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Insom''ni - Emote Talk');

-- 91350 Magus Bromley, quest 40124: at 6 s the channel ends with the Arcane Explosion visual.

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 9135001;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(9135001, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Say Line 0'),
(9135001, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Cast 23017'),
(9135001, 9, 2, 0, 0, 0, 100, 0, 6000, 6000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Say Line 1'),
(9135001, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 274, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Emote No'),
(9135001, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Stop channeling'),
(9135001, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 1449, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Bromley - Cast 1449 (Arcane Explosion visual)');

-- Same for the other quest scenes whose channel Turtle ended with a visual cast (an instant cast does not
--   break a creature channel in AzerothCore): Ansirem 40166, Halister 40562, Tazzo 40737, Ralathius 40962,
--   Parnabus 41014, Iselus 40247.

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 254301;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(254301, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Not selectable'),
(254301, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Cast 23017'),
(254301, 9, 2, 0, 0, 0, 100, 0, 18000, 18000, 0, 0, 0, 0, 5, 273, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Emote Yes'),
(254301, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Stop channeling'),
(254301, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 1449, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Cast 1449'),
(254301, 9, 5, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Say Line 100'),
(254301, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Emote Talk'),
(254301, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 60327, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Quest Credit 60327'),
(254301, 9, 8, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Archmage Ansirem Runeweaver - Selectable again');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6073101;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6073101, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Not selectable'),
(6073101, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Cast 23017'),
(6073101, 9, 2, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66619'),
(6073101, 9, 3, 0, 0, 0, 100, 0, 5000, 5000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Stop channeling'),
(6073101, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 1449, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Cast 1449'),
(6073101, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 60953, 3, 61000, 0, 0, 0, 8, 0, 0, 0, 0, -3750.76, -4438.47, 30.57, 3.08, 'Magus Halister - Summon 60953'),
(6073101, 9, 6, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66582'),
(6073101, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 8, 0, 0, 0, 100, 0, 8000, 8000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66583'),
(6073101, 9, 9, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 10, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66584'),
(6073101, 9, 11, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 12, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66585'),
(6073101, 9, 13, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 14, 0, 0, 0, 100, 0, 6000, 6000, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66586'),
(6073101, 9, 15, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 16, 0, 0, 0, 100, 0, 16000, 16000, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66587'),
(6073101, 9, 17, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 18, 0, 0, 0, 100, 0, 5000, 5000, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66588'),
(6073101, 9, 19, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 11, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote LAUGH'),
(6073101, 9, 20, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66589'),
(6073101, 9, 21, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Paval Reethe: line 66590'),
(6073101, 9, 22, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 19, 60953, 40, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 23, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66591'),
(6073101, 9, 24, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 25, 0, 0, 0, 100, 0, 6000, 6000, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66592'),
(6073101, 9, 26, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Magus Halister: line 66593'),
(6073101, 9, 27, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Emote TALK'),
(6073101, 9, 28, 0, 0, 0, 100, 0, 1000, 1000, 0, 0, 0, 0, 33, 60389, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Quest Credit 60389'),
(6073101, 9, 29, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Selectable again'),
(6073101, 9, 30, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 28, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Magus Halister - Stop channeling');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6110002;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6110002, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 83, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Remove gossip + quest giver flags'),
(6110002, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Cast 23017'),
(6110002, 9, 2, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Say Line 5'),
(6110002, 9, 3, 0, 0, 0, 100, 0, 7000, 7000, 0, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Say Line 6'),
(6110002, 9, 4, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Say Line 7'),
(6110002, 9, 5, 0, 0, 0, 100, 0, 5000, 5000, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Say Line 8'),
(6110002, 9, 6, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Stop channeling'),
(6110002, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 1449, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Cast 1449'),
(6110002, 9, 8, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 9, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Say Line 9'),
(6110002, 9, 9, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Emote Cheer'),
(6110002, 9, 10, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 82, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Tazzo Gearfire - Gossip + quest giver flags back');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6132601;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6132601, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ralathius - Cast 23017'),
(6132601, 9, 1, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ralathius - Say Line 0'),
(6132601, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ralathius - Emote Talk'),
(6132601, 9, 3, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 12, 61545, 1, 9000, 0, 0, 0, 8, 0, 0, 0, 0, 5527.01, -3700.22, 1595.52, 0.28, 'Ralathius - Summon Ysera (9 s)'),
(6132601, 9, 4, 0, 0, 0, 100, 0, 1000, 1000, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 19, 61545, 40, 0, 0, 0, 0, 0, 0, 'Ralathius - Ysera: Say Line 0'),
(6132601, 9, 5, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 19, 61545, 40, 0, 0, 0, 0, 0, 0, 'Ralathius - Ysera: Say Line 1'),
(6132601, 9, 6, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ralathius - Stop channeling'),
(6132601, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 24171, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ralathius - Cast 24171');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 6157001;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6157001, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Not selectable'),
(6157001, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Cast 23017'),
(6157001, 9, 2, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Say Line 0'),
(6157001, 9, 3, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Stop channeling'),
(6157001, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 1449, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Cast 1449'),
(6157001, 9, 5, 0, 0, 0, 100, 0, 1500, 1500, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Say Line 1'),
(6157001, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Emote Talk'),
(6157001, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Selectable again'),
(6157001, 9, 8, 0, 0, 0, 100, 0, 500, 500, 0, 0, 0, 0, 33, 60049, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Parnabus - Quest Credit 60049');

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 9172202;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(9172202, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 83, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Remove npcflag questgiver'),
(9172202, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Cast 23017'),
(9172202, 9, 2, 0, 0, 0, 100, 0, 5000, 5000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Say Line 1'),
(9172202, 9, 3, 0, 0, 0, 100, 0, 15000, 15000, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Say Line 2'),
(9172202, 9, 4, 0, 0, 0, 100, 0, 13000, 13000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Stop channeling'),
(9172202, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 24171, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Cast 24171'),
(9172202, 9, 6, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Say Line 3'),
(9172202, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 60335, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Quest Credit 60335'),
(9172202, 9, 8, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 82, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Iselus - Add npcflag questgiver');

-- 91411 Speaker Ganz'ih, quest 40026: Lord Rog's channel stops at 12 s (Turtle casts 5906 then).

DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 9141100;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(9141100, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554944, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Set Unit Flags (not selectable, immune to NPC)'),
(9141100, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 86, 13236, 0, 19, 91289, 30, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Cast Nature Channeling on Speaker Ganz''ih'),
(9141100, 9, 2, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Say Line 0'),
(9141100, 9, 3, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Stop channeling'),
(9141100, 9, 4, 0, 0, 0, 100, 0, 8000, 8000, 0, 0, 0, 0, 84, 1, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Say Line 1'),
(9141100, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 60313, 0, 0, 0, 0, 0, 12, 1, 0, 0, 0, 0, 0, 0, 0, 'Purification - Quest Credit ''Lord Rog''s Favor'''),
(9141100, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554944, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Remove Unit Flags');

-- 2020036 Runestone of Nordrassil / 2020037 Runestone of Cenarius: teleport rows existed but AIName was empty.
UPDATE `gameobject_template` SET `AIName` = 'SmartGameObjectAI' WHERE `entry` IN (2020036, 2020037);

-- 2020099 Resonating Pedestal: Turtle refuses while the two monstrosities are up (15 s); lock the pedestal.
DELETE FROM `smart_scripts` WHERE `source_type` = 1 AND `entryorguid` = 2020099 AND `id` IN (103, 104);
DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 202009901;

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(2020099, 1, 103, 0, 62, 0, 100, 0, 11020099, 0, 0, 0, 0, 0, 105, 16, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Resonating Pedestal - Not usable while the monstrosities are up'),
(2020099, 1, 104, 0, 62, 0, 100, 0, 11020099, 0, 0, 0, 0, 0, 80, 202009901, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Resonating Pedestal - Usable again later (action list)');

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(202009901, 9, 0, 0, 0, 0, 100, 0, 15000, 15000, 0, 0, 0, 0, 106, 16, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Resonating Pedestal - Usable again');

-- 92143 Captain Blackeye: Turtle aggro line 66401 missing.
DELETE FROM `creature_text` WHERE `CreatureID` = 92143 AND `GroupID` = 0;
INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(92143, 0, 0, 'Who are you? You think you can take my ship without a fight?!', 12, 0, 100, 0, 0, 0, 0, 0, 'Captain Blackeye - Aggro (Turtle 66401)');
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 92143 AND `id` = 100;

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(92143, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Captain Blackeye - On Aggro - Say Line 0');

-- 2010933 Crystalline Resonation Crystal / 2010934 Crystalline Harmonization Crystal (Badlands): Turtle
--   go_resonation_crystal / go_harmonization_crystal, "Touch the Crystal." teleports to the other crystal.
DELETE FROM `npc_text` WHERE `ID` IN (92010933, 92010934);
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`) VALUES
(92010933, '<The Crystal hums ominously.>', '<The Crystal hums ominously.>', 0, 0, 1),
(92010934, '<The Crystal remains silent.>', '<The Crystal remains silent.>', 0, 0, 1);
DELETE FROM `gossip_menu` WHERE `MenuID` IN (92010933, 92010934);
INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES (92010933, 92010933), (92010934, 92010934);
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (92010933, 92010934);
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(92010933, 0, 0, 'Touch the Crystal.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0),
(92010934, 0, 0, 'Touch the Crystal.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);
UPDATE `gameobject_template` SET `AIName` = 'SmartGameObjectAI', `Data3` = 92010933 WHERE `entry` = 2010933;
UPDATE `gameobject_template` SET `AIName` = 'SmartGameObjectAI', `Data3` = 92010934 WHERE `entry` = 2010934;
DELETE FROM `smart_scripts` WHERE `source_type` = 1 AND `entryorguid` IN (2010933, 2010934);

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(2010933, 1, 100, 0, 62, 0, 100, 0, 92010933, 0, 0, 0, 0, 0, 62, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, -6598.6328, -3910.7919, 354.9179, 4.6873, 'Crystalline Resonation Crystal - Teleport to the Harmonization Crystal'),
(2010933, 1, 101, 0, 62, 0, 100, 0, 92010933, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Crystalline Resonation Crystal - Close Gossip'),
(2010934, 1, 100, 0, 62, 0, 100, 0, 92010934, 0, 0, 0, 0, 0, 62, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, -6881.5537, -3767.8178, 316.7491, 3.3884, 'Crystalline Harmonization Crystal - Teleport to the Resonation Crystal'),
(2010934, 1, 101, 0, 62, 0, 100, 0, 92010934, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Crystalline Harmonization Crystal - Close Gossip');

-- 60450 Gold-Tooth Gary (npc_agne_gambler): the rules text Turtle shows (npc_text 80602). Script: zone_quest_scripts.cpp.
DELETE FROM `npc_text` WHERE `ID` = 9080602;
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`) VALUES
(9080602, 'Heya, sweetie. Here to make a long time investement?$B$BMaybe you wanna gamble, little $c? Tell me how much and I''ll throw the dice. If the roll is above 50, I will double the bet. If it''s lower than 50, it''s gone forever.$B$BIf you win three times in a row using the same amount, the reward is tripled, but only if the 3rd roll is above 75. If it''s below 75 on the 3rd roll, your gold will be gone too.', NULL, 0, 0, 1);

-- 2547 Ironpatch (Bloodsail, Booty Bay docks): Turtle npc_ironpatch, quest 40355 "Sark's Grudge":
--   "Let me show what how in shape I am." -> "Arrrgh!" and he fights the player. Missing from the module.
--   (Turtle's own greeting text for him is a stray id, so the plain greeting text 68 is used.)
UPDATE `creature_template` SET `npcflag` = `npcflag` | 1, `gossip_menu_id` = 9002547 WHERE `entry` = 2547;
DELETE FROM `gossip_menu` WHERE `MenuID` = 9002547;
INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES (9002547, 68);
DELETE FROM `gossip_menu_option` WHERE `MenuID` = 9002547;
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(9002547, 0, 0, 'Let me show what how in shape I am.', 0, 1, 1, 0, 0, 0, 0, NULL, 0, 0);
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 15 AND `SourceGroup` = 9002547;
INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
(15, 9002547, 0, 0, 0, 47, 0, 40355, 8, 0, 0, 0, 0, '', 'mod-turtle-content gossip option');
DELETE FROM `creature_text` WHERE `CreatureID` = 2547 AND `GroupID` = 100;
INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(2547, 100, 0, 'Arrrgh!', 12, 0, 100, 0, 0, 0, 0, 0, 'Ironpatch - Sark''s Grudge (Turtle 66710)');
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 2547 AND `id` IN (100, 101, 102);
DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` = 254700;

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(2547, 0, 100, 0, 62, 0, 100, 0, 9002547, 0, 0, 0, 0, 0, 80, 254700, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Sark''s Grudge: turns on the player (action list)'),
(2547, 0, 101, 0, 7, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Default faction again'),
(2547, 0, 102, 0, 11, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Default faction again');

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(254700, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Close Gossip'),
(254700, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Say Arrrgh!'),
(254700, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 36, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Emote Attack'),
(254700, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Hostile (faction 14)'),
(254700, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Ironpatch - Attack');

-- Turtle rented_mount: the riding rams (4779 Brown, 4710 Gray) and kodos (12354 Brown, 12355 Gray) at the
--   stables can be hired for 50 copper (script: zone_northwind.cpp). They need the gossip flag and
--   Turtle's texts 90381 / 90382.
UPDATE `creature_template` SET `npcflag` = `npcflag` | 1 WHERE `entry` IN (4779, 4710, 12354, 12355);
DELETE FROM `npc_text` WHERE `ID` IN (90381, 90382);
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`) VALUES
(90381, 'The Ram, a creature as majestic as it is stubborn. It gazes at you.', 'The Ram, a creature as majestic as it is stubborn. It gazes at you.', 0, 0, 1),
(90382, 'The Kodo Beast is a peaceful creature. There isn''t much which is able to stop it once in motion.', 'The Kodo Beast is a peaceful creature. There isn''t much which is able to stop it once in motion.', 0, 0, 1);
