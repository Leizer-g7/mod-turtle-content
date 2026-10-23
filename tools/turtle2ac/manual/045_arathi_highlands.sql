-- ---------------------------------------------------------------------------
-- Hand-written scripts for Arathi Highlands
-- Re-expresses Turtle's C++ scripts (tortoise-wow random_scripts_1/3.cpp) as SmartAI.
-- Each '@block requires=' block is only emitted when those creatures are part of the build
-- (e.g. Wildtusk Village is held back until the terrain patch exists).
-- smart_scripts ids >= 100 are reserved for hand-written rows.
-- ---------------------------------------------------------------------------

-- @block requires=91289,91411,60313
-- Lord Rog / Speaker Ganz'ih (Wildtusk Village) - texts from Turtle broadcast_text 67019-67021
DELETE FROM `creature_text` WHERE `CreatureID` IN (91411, 91289);
INSERT INTO `creature_text` (`CreatureID`,`GroupID`,`ID`,`Text`,`Type`,`Language`,`Probability`,`Emote`,`Duration`,`Sound`,`BroadcastTextId`,`TextRange`,`comment`) VALUES
(91411, 0, 0, 'It would appear the bracers be having some sort of voodoo corruption tainting them, I can sense it from here.', 12, 0, 100, 1, 0, 0, 0, 0, 'Speaker Ganz\'ih - after Lord Rog\'s Exiles'),
(91289, 0, 0, 'The curse upon the bracers has been lifted, the weak magic of mortals cannot compete with the Elemental Plane.', 12, 0, 100, 0, 0, 0, 0, 0, 'Lord Rog - purification 1'),
(91289, 1, 0, 'I must thank you, your assistance has been instrumental.', 12, 0, 100, 0, 0, 0, 0, 0, 'Lord Rog - purification 2');
UPDATE `creature_template` SET `AIName`='SmartAI' WHERE `entry` IN (91411, 91289);
DELETE FROM `smart_scripts` WHERE (`source_type`=0 AND `entryorguid` IN (91411, 91289) AND `id` >= 100) OR (`source_type`=9 AND `entryorguid`=9141100);
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(91289, 0, 100, 0, 20, 0, 100, 0, 40024, 0, 0, 0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 19, 91411, 30, 0, 0, 0, 0, 0, 0, 'Lord Rog - On Quest \'Lord Rog\'s Exiles\' Rewarded - Speaker Ganz\'ih Say Line 0'),
(91411, 0, 100, 101, 19, 0, 100, 0, 40026, 0, 0, 0, 0, 0, 64, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Speaker Ganz\'ih - On Quest \'Lord Rog\'s Favor\' Accepted - Store Invoker'),
(91411, 0, 101, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 80, 9141100, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Speaker Ganz\'ih - Linked - Run Purification Script'),
(9141100, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554944, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Set Unit Flags (not selectable, immune to NPC)'),
(9141100, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 86, 13236, 0, 19, 91289, 30, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Cast Nature Channeling on Speaker Ganz\'ih'),
(9141100, 9, 2, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Say Line 0'),
(9141100, 9, 3, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 84, 1, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Say Line 1'),
(9141100, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 60313, 0, 0, 0, 0, 0, 12, 1, 0, 0, 0, 0, 0, 0, 0, 'Purification - Quest Credit \'Lord Rog\'s Favor\''),
(9141100, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554944, 0, 0, 0, 0, 0, 19, 91289, 30, 0, 0, 0, 0, 0, 0, 'Purification - Lord Rog - Remove Unit Flags');
-- @end

-- @block requires=91790
-- Speaker Gan'to (Ruins of Zul'Rasaz) - Turtle broadcast_text 66190
DELETE FROM `creature_text` WHERE `CreatureID`=91790;
INSERT INTO `creature_text` (`CreatureID`,`GroupID`,`ID`,`Text`,`Type`,`Language`,`Probability`,`Emote`,`Duration`,`Sound`,`BroadcastTextId`,`TextRange`,`comment`) VALUES
(91790, 0, 0, 'What, did that foolish Yin\'do send you? You shall perish!', 12, 0, 100, 0, 0, 0, 0, 0, 'Speaker Gan\'to - aggro');
UPDATE `creature_template` SET `AIName`='SmartAI' WHERE `entry`=91790;
DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid`=91790 AND `id` >= 100;
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(91790, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Speaker Gan\'to - On Aggro - Say Line 0');
-- @end

-- @block requires=60779
-- 'Chaser' (Livingstone Croft) - Turtle broadcast_text 66737
DELETE FROM `creature_text` WHERE `CreatureID`=60779;
INSERT INTO `creature_text` (`CreatureID`,`GroupID`,`ID`,`Text`,`Type`,`Language`,`Probability`,`Emote`,`Duration`,`Sound`,`BroadcastTextId`,`TextRange`,`comment`) VALUES
(60779, 0, 0, 'Initiating thank you protocols.... THANK YOU', 12, 0, 100, 0, 0, 0, 0, 0, '\'Chaser\' - quest rewarded');
UPDATE `creature_template` SET `AIName`='SmartAI' WHERE `entry`=60779;
DELETE FROM `smart_scripts` WHERE `source_type`=0 AND `entryorguid`=60779 AND `id` >= 100;
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(60779, 0, 100, 0, 20, 0, 100, 0, 40450, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '\'Chaser\' - On Quest \'Repowering Chaser\' Rewarded - Say Line 0');
-- @end
