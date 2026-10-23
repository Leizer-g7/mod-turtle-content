-- mod-turtle-content: two quests of the friend's Moonwhisper Coast build that could not be done (2026-10-12).
-- 41969 Raiments of Ritual: Ember Worg Fur drops (quest only) from Burning Steppes' Ember Worgs, Turtle's chances.
-- 42063 Delivery from Talendris: its giver Sentinel Velaya (Ashenvale, Turtle's spot) was missing.
SET NAMES utf8mb4;

DELETE FROM `creature_loot_template` WHERE `Entry` = 9690 AND `Item` = 1042250;
DELETE FROM `creature_loot_template` WHERE `Entry` = 9694 AND `Item` = 1042250;
DELETE FROM `creature_loot_template` WHERE `Entry` = 9697 AND `Item` = 1042250;
DELETE FROM `creature_template` WHERE `entry` = 63160;
DELETE FROM `creature_template_model` WHERE `CreatureID` = 63160;
DELETE FROM `creature_template_movement` WHERE `CreatureId` = 63160;
DELETE FROM `creature` WHERE `guid` BETWEEN 9990301 AND 9990399;
DELETE FROM `creature_queststarter` WHERE `quest` = 42063;

INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(9690, 1042250, 0, 24.0, 1, 1, 0, 1, 1, 'Ember Worg - Ember Worg Fur (Turtle quest drop, quest 41969)'),
(9694, 1042250, 0, 24.0, 1, 1, 0, 1, 1, 'Slavering Ember Worg - Ember Worg Fur (Turtle quest drop, quest 41969)'),
(9697, 1042250, 0, 48.0, 1, 1, 0, 1, 1, 'Giant Ember Worg - Ember Worg Fur (Turtle quest drop, quest 41969)');

INSERT INTO `creature_template` (`entry`, `name`, `subname`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RegenHealth`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(63160, 'Sentinel Velaya', NULL, 0, 50, 50, 0, 80, 2, 1.0, 1.42857, 18.0, 0, 0, 1.336, 2000, 2000, 1, 0, 2048, 0, 0, 7, 0, 0, 0, 0, '', 0, 1.515, 1, 1.011, 1, 1, 0, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(63160, 0, 2306, 1, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`) VALUES
(63160, 1, 1, 0, 0, 0, 0);

INSERT INTO `creature` (`guid`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `Comment`, `id`) VALUES
(9990301, 1, 0, 0, 1, 1, 0, 2694.0, -3888.46, 109.015, 1.28374, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 'turtle new-zone quest fix: Sentinel Velaya, Ashenvale (tw guid 2596626)', 63160);

INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(63160, 42063);

