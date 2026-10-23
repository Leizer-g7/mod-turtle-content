-- mod-turtle-content 933: Turtle dungeon doors / levers spawn in their DB state again (Claude, 2026-10-14).
-- Cause: AzerothCore only applies `gameobject`.`state` to doors/buttons of a dungeon when the map has an InstanceScript.
-- Our Turtle dungeons have none, so these objects spawned OPEN (state 0) and without collision.
-- Fix: on spawn, SmartAI puts each one back to its DB state (1 = closed), like Penqle (vmangos uses the DB state).
-- Objects: Dragonmaw Retreat Reserve Gate + Lower Reserve Gate (816), Stormwrought Castle Gates + secret portcullis
-- + 4 Chamber Levers (818). The Stormwind Vault door is already handled in C++.
-- Part 2 (found while testing): the 4 Turtle keys had no use-spell (Turtle uses its own spells 58047-58050, which are
-- "Summon Mason" in 3.3.5, so the friend set 0) -> the client could not open the gates/chests once they are closed.
-- They now use the stock "Opening" spell 3366 (like the Winery Key). Charges as in Penqle: chest keys are used up (-1),
-- gate keys stay. Tested on the test server: Lower Reserve Gate and Stormwrought Castle Gate open with their key.
-- Approved by Max 2026-10-14. Safe to run again.

UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI' WHERE `entry` IN (2020251,2020232,2020233) AND `AIName`='';

DELETE FROM `smart_scripts` WHERE `source_type`=1 AND `entryorguid` IN (2020251,2020232,2020233) AND `id`=0;
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(2020251,1,0,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Dragonmaw Retreat Reserve Gate - On Spawn - Set Closed (DB state)'),
(2020232,1,0,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Lower Reserve Gate - On Spawn - Set Closed (DB state)'),
(2020233,1,0,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Stormwrought Castle Gate - On Spawn - Set Closed (DB state)');

DELETE FROM `smart_scripts` WHERE `source_type`=1 AND `entryorguid` IN (-9120018,-9120020,-9120021,-9120022,-9120023) AND `id` IN (101,102); -- 102 = old draft row, removed
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(-9120018,1,101,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Secret Portcullis - On Spawn - Set Closed (DB state)'),
(-9120020,1,101,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Chamber Lever - On Spawn - Set Ready (DB state)'),
(-9120021,1,101,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Chamber Lever - On Spawn - Set Ready (DB state)'),
(-9120022,1,101,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Chamber Lever - On Spawn - Set Ready (DB state)'),
(-9120023,1,101,0,63,0,100,0,0,0,0,0,0,0,118,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Chamber Lever - On Spawn - Set Ready (DB state)');

UPDATE `item_template` SET `spellid_1`=3366, `spelltrigger_1`=0, `spellcharges_1`=0  WHERE `entry` IN (1041876,1041913);  -- Lower Reserve Key, Key to Stormwrought Castle
UPDATE `item_template` SET `spellid_1`=3366, `spelltrigger_1`=0, `spellcharges_1`=-1 WHERE `entry` IN (1041692,1041905);  -- Blackrock Coffer Key, Kwabit's Chest Key
