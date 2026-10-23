-- mod-turtle-content 934: Thromrar Darkflame's Skardyn Darkshield + the Dragonfire Bomb, like Penqle (Claude, 2026-10-14).
-- Penqle: Thromrar (62725, Grim Reaches, quest 41809 "Smell of Dragonfire") spawns with Skardyn Darkshield (-100% damage
-- taken); the Dragonfire Bomb (41909) removes it (npc_thromrar_darkflame). Turtle's spells 52712/52713 do not exist in 3.3.5,
-- so stock spells are used instead (no client change):
--   shield = 62276 "Sheath of Lightning" (3.3.5: -100% damage taken, permanent, no proc, no core script)
--   bomb   = 74454 "Conflagration" (3.3.5: 1 s cast, fire projectile, dummy on an enemy, no core script, no condition)
-- Without the bomb Thromrar takes no damage, as in Penqle. Approved by Max 2026-10-14. Safe to run again.

DELETE FROM `creature_template_addon` WHERE `entry`=62725;
INSERT INTO `creature_template_addon` (`entry`,`path_id`,`mount`,`bytes1`,`bytes2`,`emote`,`visibilityDistanceType`,`auras`) VALUES
(62725,0,0,0,0,0,0,'62276');
-- the only spawn has its own creature_addon row (it overrides the template one): give it the shield too
UPDATE `creature_addon` SET `auras`='62276' WHERE `guid`=9141302;

DELETE FROM `smart_scripts` WHERE `entryorguid`=62725 AND `source_type`=0 AND `id`=100;
INSERT INTO `smart_scripts` (`entryorguid`,`source_type`,`id`,`link`,`event_type`,`event_phase_mask`,`event_chance`,`event_flags`,`event_param1`,`event_param2`,`event_param3`,`event_param4`,`event_param5`,`event_param6`,`action_type`,`action_param1`,`action_param2`,`action_param3`,`action_param4`,`action_param5`,`action_param6`,`target_type`,`target_param1`,`target_param2`,`target_param3`,`target_param4`,`target_x`,`target_y`,`target_z`,`target_o`,`comment`) VALUES
(62725,0,100,0,8,0,100,0,74454,0,0,0,0,0,28,62276,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'Thromrar Darkflame - On Spellhit Dragonfire Bomb - Remove Skardyn Darkshield');

UPDATE `item_template` SET `spellid_1`=74454, `spelltrigger_1`=0, `spellcharges_1`=0 WHERE `entry`=1041909;  -- Dragonfire Bomb
