-- mod-turtle-content: Turtle creature abilities the converter dropped (2026-10-12, approved by Max).
-- Willow 61514 is no longer here: mod_turtle_006_gilneas.sql (2026-10-12 build) casts the same curse; keeping both would cast it twice.
-- Rows use ids 200+ so a later zone rebuild (ids 0..n) never collides with them.
-- Not portable: the aggro voice lines of Darkmaster Haza'gi, Champion Raggazi and Chieftain Woh'zo (Turtle sounds 30265-30267
-- are Turtle-only client files; their aggro texts are already in). Brol'ok Mauler's Turtle spell list is empty.
SET NAMES utf8mb4;

DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (61502,62647,62779,80806) AND `id` BETWEEN 200 AND 299;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(61502, 0, 200, 0, 0, 0, 100, 0, 0, 0, 45000, 45000, 0, 0, 11, 11641, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Witch Doctor Tan\'zo - In Combat - Cast Hex (Turtle 45504 -> 3.3.5 NPC Hex 11641)'),
(62647, 0, 200, 0, 0, 0, 100, 0, 0, 0, 300000, 300000, 0, 0, 12, 62667, 4, 30000, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Shadow Council Summoner - In Combat - Summon Cackling Impling (Turtle 44045, no 3.3.5 spell: summoned directly)'),
(80806, 0, 200, 0, 0, 0, 100, 0, 6000, 6000, 33000, 41000, 0, 0, 11, 7761, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Risen Troll - In Combat - Cast Shared Bonds 7761 (Turtle spell list 18660)'),
(62779, 0, 200, 0, 2, 0, 100, 1, 0, 50, 0, 0, 0, 0, 14, 0, 100, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Pathun Duskhide - At 50% HP - Reset all threat (Turtle EventAI 6277901)');

UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (61502,62647,62779,80806) AND `ScriptName` = '';
