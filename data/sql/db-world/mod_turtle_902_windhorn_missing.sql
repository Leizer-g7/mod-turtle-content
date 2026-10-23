-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Windhorn Canyon creatures the converter left out (Max + Claude, 2026-10-11)
-- Source: Turtle world DB (tortoise-wow-main sql/base + database_updates).
--  61410 Spirit of Champion Rotag: Narlgom's 50% summon (Turtle 42004). Turtle gives it the same
--        stats as Champion Rotag (62785), so it copies Rotag's row; Turtle display 21393 has no
--        3.3.5 equivalent -> Rotag's display with Turtle's Ghost Visual (22650). Attackable
--        (Turtle unit_flags 32768). Turtle EventAI: "I have returned..." on spawn.
--  62866 Storm Residue: the Storm Guardian splits into 3 on death. Copies Storm Guardian (62865)
--        scaled to Turtle's values (498 HP, 404 armor, 26-32 damage, scale 0.7, normal rank,
--        no spell list, no loot).
-- Idempotent: deletes its own rows first.

DELETE FROM `creature_template` WHERE `entry` IN (61410, 62866);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (61410, 62866);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (61410, 62866);
DELETE FROM `creature_template_addon` WHERE `entry` IN (61410, 62866);
DELETE FROM `creature_text` WHERE `CreatureID` = 61410;
DELETE FROM `smart_scripts` WHERE `entryorguid` = 61410 AND `source_type` = 0;

DROP TEMPORARY TABLE IF EXISTS `tmp_turtle_ct`;
CREATE TEMPORARY TABLE `tmp_turtle_ct` SELECT * FROM `creature_template` WHERE `entry` IN (62785, 62865);
UPDATE `tmp_turtle_ct` SET `entry` = 61410, `name` = 'Spirit of Champion Rotag', `unit_flags` = 32768,
    `AIName` = 'SmartAI', `ScriptName` = '', `lootid` = 0, `skinloot` = 0, `pickpocketloot` = 0
    WHERE `entry` = 62785;
UPDATE `tmp_turtle_ct` SET `entry` = 62866, `name` = 'Storm Residue', `rank` = 0,
    `HealthModifier` = 0.5838, `DamageModifier` = 0.6955, `ArmorModifier` = 0.3637,
    `AIName` = '', `ScriptName` = '', `lootid` = 0, `skinloot` = 0, `pickpocketloot` = 0,
    `mingold` = 0, `maxgold` = 0
    WHERE `entry` = 62865;
INSERT INTO `creature_template` SELECT * FROM `tmp_turtle_ct`;
DROP TEMPORARY TABLE `tmp_turtle_ct`;

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(61410, 0, 3783, 1.4, 1, 0),
(62866, 0, 5490, 0.7, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`) VALUES
(61410, 1, 1, 0, 0, 0, 0, NULL),
(62866, 1, 1, 0, 0, 0, 0, NULL);

INSERT INTO `creature_template_addon` (`entry`, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras`) VALUES
(61410, 0, 0, 0, 0, 0, 0, '22650');

INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(61410, 0, 0, 'I have returned...', 14, 0, 100, 0, 0, 0, 0, 0, 'Spirit of Champion Rotag - spawn (Turtle -1999940)');

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(61410, 0, 0, 0, 54, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Spirit of Champion Rotag - Just Summoned - Yell Line 0');
