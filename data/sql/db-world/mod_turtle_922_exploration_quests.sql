-- mod-turtle-content: exploration quests whose Turtle area triggers do not exist in 3.3.5 (2026-10-12, approved by Max).
-- 'Tomb of Ancestors' (41802, Turtle trigger 700) and 'To Cure the Withered' (41848, Turtle trigger 5601) had lost their
-- exploration flag and finished on accept. An invisible marker at Turtle's trigger spot (same radius) now completes them.
SET NAMES utf8mb4;

DELETE FROM `creature_template` WHERE `entry` IN (9991001,9991002);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (9991001,9991002);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (9991001,9991002);
DELETE FROM `creature` WHERE `guid` BETWEEN 9990201 AND 9990299;

INSERT INTO `creature_template` (`entry`, `name`, `minlevel`, `maxlevel`, `faction`, `speed_walk`, `speed_run`, `unit_class`, `unit_flags`, `unit_flags2`, `AIName`, `HealthModifier`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(9991001, 'quest_41802_tomb_of_ancestors', 1, 1, 35, 1, 1.14286, 1, 33554434, 2048, 'SmartAI', 0.024, 128, '', 0),
(9991002, 'quest_41848_grim_batol_passage', 1, 1, 35, 1, 1.14286, 1, 33554434, 2048, 'SmartAI', 0.024, 128, '', 0);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(9991001, 0, 11686, 1, 1, 0),
(9991002, 0, 11686, 1, 1, 0);
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `action_type`, `action_param1`, `target_type`, `comment`) VALUES
(9991001, 0, 0, 0, 10, 0, 100, 0, 2, 10, 5000, 5000, 1, 15, 41802, 7, 'quest_41802_tomb_of_ancestors - Player in range - Explore quest 41802 (Turtle area trigger 700)'),
(9991002, 0, 0, 0, 10, 0, 100, 0, 2, 50, 5000, 5000, 1, 15, 41848, 7, 'quest_41848_grim_batol_passage - Player in range - Explore quest 41848 (Turtle area trigger 5601)');
INSERT INTO `creature` (`guid`, `id`, `map`, `spawnMask`, `phaseMask`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `curhealth`, `Comment`) VALUES
(9990201, 9991001, 0, 1, 1, -5705.570, -4760.070, 198.031, 0, 300, 1, 'turtle exploration marker: quest 41802 (Turtle area trigger 700)'),
(9990202, 9991002, 0, 1, 1, -4177.600, -4350.500, 221.300, 0, 300, 1, 'turtle exploration marker: quest 41848 (Turtle area trigger 5601)');

UPDATE `quest_template_addon` SET `SpecialFlags` = `SpecialFlags` | 2 WHERE `ID` IN (41802,41848);
