-- mod-turtle-content: Hateforge Quarry + two world rares, from Penqle's tortoise-wow core (2026-10-12, approved by Max).
-- 1. Faceless Terror 60738: Har'gesh Doomcaller's adds. The boss scripts are C++ (src/bosses/boss_hateforge_quarry.cpp);
--    the converter builds only creatures that have a spawn, so this summoned one had no template.
-- 2. Crusader Larsarius (Eastern Plaguelands) and Blademaster Kargron (Burning Steppes): their Turtle abilities
--    (events/boss_rares.cpp), as SmartAI like the rares in 919. Rows use ids 200+.
SET NAMES utf8mb4;

DELETE FROM `creature_template` WHERE `entry` = 60738;
DELETE FROM `creature_template_model` WHERE `CreatureID` = 60738;
DELETE FROM `creature_template_movement` WHERE `CreatureId` = 60738;
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (49002, 49008) AND `id` BETWEEN 200 AND 299;

INSERT INTO `creature_template` (`entry`, `name`, `subname`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RegenHealth`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(60738, 'Faceless Terror', NULL, 0, 53, 53, 0, 54, 0, 1.0, 1.14286, 20.0, 1, 0, 8.174, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 4.454, 1, 0.777, 1, 1, 0, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(60738, 0, 27932, 0.8, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`) VALUES
(60738, 1, 1, 0, 0, 0, 0);

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(49002, 0, 200, 0, 0, 0, 100, 0, 5000, 30000, 30000, 30000, 0, 0, 11, 21919, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Blademaster Kargron - In Combat - Cast Thrash (Turtle boss_rares)'),
(49002, 0, 201, 0, 2, 0, 100, 1, 0, 20, 0, 0, 0, 0, 11, 5256, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Blademaster Kargron - Below 20% HP - Cast Parry (Turtle boss_rares)'),
(49002, 0, 202, 0, 2, 0, 100, 1, 0, 20, 0, 0, 0, 0, 11, 28131, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Blademaster Kargron - Below 20% HP - Cast Enrage (Turtle boss_rares)'),
(49008, 0, 200, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 10293, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Crusader Larsarius - On Aggro - Cast Devotion Aura (Turtle boss_rares)'),
(49008, 0, 201, 0, 0, 0, 100, 0, 8000, 20000, 20000, 20000, 0, 0, 11, 17284, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Crusader Larsarius - In Combat - Cast Holy Strike (Turtle boss_rares)'),
(49008, 0, 202, 0, 0, 0, 100, 0, 10000, 30000, 30000, 30000, 0, 0, 11, 10308, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Crusader Larsarius - In Combat - Cast Hammer of Justice (Turtle boss_rares)'),
(49008, 0, 203, 0, 0, 0, 100, 0, 20000, 40000, 40000, 40000, 0, 0, 11, 25292, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Crusader Larsarius - In Combat - Cast Holy Light (Turtle boss_rares)');

UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (49002, 49008) AND `ScriptName` = '';
