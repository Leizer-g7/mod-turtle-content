-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Crescent Grove fixes (Max + Claude, 2026-10-11)
-- Source: tortoise-wow-main/src/scripts/dungeons/crescent_grove/instance_crescent_grove.cpp and the
-- Turtle world DB.
--  - Aggro and death yells of the 4 bosses (Turtle instance script). Turtle also plays its own voice
--    files (sounds 30252-30273); those are not in the 3.3.5 client, so the yells are text only.
--  - 92112 Raging Infernal: Turtle casts 8269 ("Enrage", +50% damage, +60% attack speed, bigger).
--    8269 is the same spell in 3.3.5 (named Frenzy); the converter had used 8599.
-- Idempotent: deletes its own rows first.

DELETE FROM `creature_text` WHERE `CreatureID` IN (92107, 92109, 92110, 92111) AND `GroupID` IN (91, 92);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (92107, 92109, 92110, 92111) AND `id` IN (100, 101);
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` = 92111 AND `AIName` = '';

INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(92107, 91, 0, 'I am the leader of the tribes, me! The Groveweald shall destroy everyone that gets in the way!', 14, 0, 100, 0, 0, 0, 0, 0, 'Grovetender Engryss - aggro (Turtle instance_crescent_grove)'),
(92107, 92, 0, 'I.. I can see clearly now.. The madness... It''s... Over...', 14, 0, 100, 0, 0, 0, 0, 0, 'Grovetender Engryss - death (Turtle instance_crescent_grove)'),
(92109, 91, 0, 'What? Who..Who are you? They wouldn''t send you! Ancients, to my side!', 14, 0, 100, 0, 0, 0, 0, 0, 'Keeper Ranathos - aggro (Turtle instance_crescent_grove)'),
(92109, 92, 0, 'We must.. Stop.. The shadow...', 14, 0, 100, 0, 0, 0, 0, 0, 'Keeper Ranathos - death (Turtle instance_crescent_grove)'),
(92111, 91, 0, 'We will serve at the Master''s will!', 14, 0, 100, 0, 0, 0, 0, 0, 'Fenektis the Deceiver - aggro (Turtle instance_crescent_grove)'),
(92111, 92, 0, 'You think.. This.... Is the end?', 14, 0, 100, 0, 0, 0, 0, 0, 'Fenektis the Deceiver - death (Turtle instance_crescent_grove)'),
(92110, 91, 0, 'Do you think you can withstand the might of the Burning Legion?', 14, 0, 100, 0, 0, 0, 0, 0, 'Master Raxxieth - aggro (Turtle instance_crescent_grove)'),
(92110, 92, 0, 'My death.. Means little in the grand scheme, mortals... Drink down your victory... It will mean nothing... In the end...', 14, 0, 100, 0, 0, 0, 0, 0, 'Master Raxxieth - death (Turtle instance_crescent_grove)');

INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`,
    `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`,
    `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`,
    `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(92107, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 91, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grovetender Engryss - On Aggro - Yell (Turtle instance_crescent_grove)'),
(92107, 0, 101, 0, 6, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 92, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grovetender Engryss - On Death - Yell (Turtle instance_crescent_grove)'),
(92109, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 91, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Ranathos - On Aggro - Yell (Turtle instance_crescent_grove)'),
(92109, 0, 101, 0, 6, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 92, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Keeper Ranathos - On Death - Yell (Turtle instance_crescent_grove)'),
(92111, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 91, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Fenektis the Deceiver - On Aggro - Yell (Turtle instance_crescent_grove)'),
(92111, 0, 101, 0, 6, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 92, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Fenektis the Deceiver - On Death - Yell (Turtle instance_crescent_grove)'),
(92110, 0, 100, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 91, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Master Raxxieth - On Aggro - Yell (Turtle instance_crescent_grove)'),
(92110, 0, 101, 0, 6, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 92, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Master Raxxieth - On Death - Yell (Turtle instance_crescent_grove)');

UPDATE `smart_scripts` SET `action_param1` = 8269,
    `comment` = 'Raging Infernal - In Combat - Cast 8269 Enrage (Turtle spell list 201063)'
    WHERE `source_type` = 0 AND `entryorguid` = 92112 AND `id` = 0 AND `action_type` = 11 AND `action_param1` = 8599;
