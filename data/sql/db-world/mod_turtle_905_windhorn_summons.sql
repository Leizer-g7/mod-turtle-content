-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Windhorn Canyon summons the converter left out (Max + Claude, 2026-10-11)
-- Source: Turtle world DB creature_template. Used by src/bosses/boss_windhorn_canyon.cpp.
--  62969 Lesser Stone Elemental: Blackwind Earthkeeper's summon (Turtle 36729). Level 28-29 elite,
--        2317 HP, 1605 armor, 153-198 damage, display 1108, faction 16, elemental.
--  49019 Scorpid Totem: Deathtotem Shaman's summon (Turtle 36731). Level 28-29, 2 HP, no armor,
--        11 damage, display 4588, faction 16. Follows the shaman; no spells on Turtle either.
-- Modifiers are Turtle's values over AzerothCore's level 28-29 warrior base stats.
-- Idempotent: deletes its own rows first.

DELETE FROM `creature_template` WHERE `entry` IN (62969, 49019);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (62969, 49019);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (62969, 49019);
DELETE FROM `creature_template_addon` WHERE `entry` IN (62969, 49019);

DROP TEMPORARY TABLE IF EXISTS `tmp_turtle_ct`;
CREATE TEMPORARY TABLE `tmp_turtle_ct` SELECT * FROM `creature_template` WHERE `entry` = 62770;
UPDATE `tmp_turtle_ct` SET `entry` = 62969, `name` = 'Lesser Stone Elemental', `subname` = NULL,
    `minlevel` = 28, `maxlevel` = 29, `rank` = 1, `type` = 4, `unit_class` = 1, `faction` = 16, `npcflag` = 0,
    `speed_walk` = 1, `speed_run` = 1.14286, `BaseAttackTime` = 2000, `unit_flags` = 0,
    `HealthModifier` = 2.636, `ManaModifier` = 1, `ArmorModifier` = 1.423, `DamageModifier` = 4.14,
    `AIName` = '', `ScriptName` = '', `gossip_menu_id` = 0, `lootid` = 0, `skinloot` = 0, `pickpocketloot` = 0,
    `mingold` = 0, `maxgold` = 0;
INSERT INTO `creature_template` SELECT * FROM `tmp_turtle_ct`;
UPDATE `tmp_turtle_ct` SET `entry` = 49019, `name` = 'Scorpid Totem', `rank` = 0, `type` = 10,
    `speed_walk` = 1, `speed_run` = 1, `HealthModifier` = 0.0023, `ArmorModifier` = 0, `DamageModifier` = 0.608;
INSERT INTO `creature_template` SELECT * FROM `tmp_turtle_ct`;
DROP TEMPORARY TABLE `tmp_turtle_ct`;

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(62969, 0, 1108, 1, 1, 0),
(49019, 0, 4588, 1, 1, 0);

INSERT INTO `creature_template_movement` SELECT 62969, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`
    FROM `creature_template_movement` WHERE `CreatureId` = 62770;
INSERT INTO `creature_template_movement` SELECT 49019, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`
    FROM `creature_template_movement` WHERE `CreatureId` = 62770;
