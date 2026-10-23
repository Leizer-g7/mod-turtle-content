-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Stormwind Vault pieces the converter left out (Max + Claude, 2026-10-11)
-- Source: Turtle world DB + tortoise-wow-main/src/scripts/dungeons/stormwind_vaults.
-- Used by src/bosses/boss_stormwind_vault.cpp.
--  93106 Hungry Vault Rat: the rat trap's 15 rats. Level 60, 1850 HP, 3271 armor, 365-403 damage,
--        display 1141, faction 16.
--  60612 Frigid Guardian: Arc'tiras summons 2 at 60%. Level 61 elite, 9067 HP, 3521 armor,
--        1514-1562 damage, display 18641, 5-7 gold. Turtle spell list 180016: Frost Shock (12548) on a
--        random enemy, first after 2 s, then every 11-12 s.
--  60597 Maddened Vault Guard: Turtle instance script, 30% chance of one of 3 lines on aggro.
--  Gameobject 2010867 Vault Armory Equipment: chest Arc'tiras leaves behind. Turtle's loot is kept for
--        the 2 items the module has (Crest of Valor x3, Fashion Coin 80%); the other 9 Turtle items
--        (40003, 41406, 41700, 60420, 60426, 60429, 60430, 60501, 60505, 60506, 83570) are not in the
--        module's item tables.
-- Modifiers are Turtle's values over AzerothCore's level 60/61 warrior base stats.
-- Idempotent: deletes its own rows first.

DELETE FROM `creature_template` WHERE `entry` IN (93106, 60612);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (93106, 60612);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (93106, 60612);
DELETE FROM `creature_template_addon` WHERE `entry` IN (93106, 60612);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 60612;
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 60597 AND `id` = 100;
DELETE FROM `creature_text` WHERE `CreatureID` = 60597 AND `GroupID` = 90;

DROP TEMPORARY TABLE IF EXISTS `tmp_turtle_ct`;
CREATE TEMPORARY TABLE `tmp_turtle_ct` SELECT * FROM `creature_template` WHERE `entry` = 60597;
UPDATE `tmp_turtle_ct` SET `entry` = 93106, `name` = 'Hungry Vault Rat', `subname` = NULL,
    `minlevel` = 60, `maxlevel` = 60, `rank` = 0, `type` = 8, `unit_class` = 1, `faction` = 16, `npcflag` = 0,
    `speed_walk` = 1, `speed_run` = 1.14286, `BaseAttackTime` = 2000, `unit_flags` = 0,
    `HealthModifier` = 0.606, `ManaModifier` = 1, `ArmorModifier` = 0.872, `DamageModifier` = 3.468,
    `AIName` = '', `ScriptName` = '', `gossip_menu_id` = 0, `lootid` = 0, `skinloot` = 0, `pickpocketloot` = 0,
    `mingold` = 0, `maxgold` = 0;
INSERT INTO `creature_template` SELECT * FROM `tmp_turtle_ct`;
UPDATE `tmp_turtle_ct` SET `entry` = 60612, `name` = 'Frigid Guardian', `minlevel` = 61, `maxlevel` = 61,
    `rank` = 1, `type` = 4, `HealthModifier` = 2.884, `ArmorModifier` = 0.870, `DamageModifier` = 12.80,
    `AIName` = 'SmartAI', `mingold` = 517, `maxgold` = 680;
INSERT INTO `creature_template` SELECT * FROM `tmp_turtle_ct`;
DROP TEMPORARY TABLE `tmp_turtle_ct`;

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(93106, 0, 1141, 1, 1, 0),
(60612, 0, 18641, 1, 1, 0);

INSERT INTO `creature_template_movement` SELECT 93106, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`
    FROM `creature_template_movement` WHERE `CreatureId` = 60597;
INSERT INTO `creature_template_movement` SELECT 60612, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`
    FROM `creature_template_movement` WHERE `CreatureId` = 60597;

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`,
    `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`,
    `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`,
    `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(60612, 0, 0, 0, 0, 0, 100, 0, 2000, 2000, 11000, 12000, 0, 0, 11, 12548, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0,
    'Frigid Guardian - In Combat - Cast Frost Shock on a random enemy (Turtle spell list 180016)'),
(60597, 0, 100, 0, 4, 0, 30, 0, 0, 0, 0, 0, 0, 0, 1, 90, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    'Maddened Vault Guard - On Aggro - Say random line (30%, Turtle instance_stormwind_vault)');

INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(60597, 90, 0, 'Do you hear them?! In the walls... They''re always watching!', 12, 0, 100, 0, 0, 0, 0, 0, 'Maddened Vault Guard - aggro'),
(60597, 90, 1, 'What even are you?! The watchers sent you, you''re going to rip us apart!', 12, 0, 100, 0, 0, 0, 0, 0, 'Maddened Vault Guard - aggro'),
(60597, 90, 2, 'There is no leaving, not for any of us, they block our escape...', 12, 0, 100, 0, 0, 0, 0, 0, 'Maddened Vault Guard - aggro');

DELETE FROM `gameobject_template` WHERE `entry` = 2010867;
DELETE FROM `gameobject_template_addon` WHERE `entry` = 2010867;
DELETE FROM `gameobject_loot_template` WHERE `Entry` = 2010867;
INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`,
    `Data0`, `Data1`, `Data2`, `Data3`, `Data15`, `AIName`, `ScriptName`) VALUES
(2010867, 3, 259, 'Vault Armory Equipment', '', '', '', 1, 57, 2010867, 0, 1, 1, '', '');
INSERT INTO `gameobject_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(2010867, 1041985, 0, 100, 1, 1, 0, 3, 3, 'Turtle 41985 x3 (quest)'),
(2010867, 1051217, 0, 80, 0, 1, 2, 1, 1, 'Turtle 51217');
