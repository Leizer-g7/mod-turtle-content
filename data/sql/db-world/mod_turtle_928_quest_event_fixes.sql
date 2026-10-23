-- mod-turtle-content 928: quest event fix found on the cloud test server (Claude, 2026-10-13).
--
-- Farm Raiders (41946), Farmer Denphar (62922): accepting the quest starts a raid action list that ends
-- with a 180 s wait before Denphar is "interactible again". Killing the leader Ghin'taru ends the raid
-- early (Denphar thanks you and is interactible again), but that long action list keeps running, and
-- AzerothCore will not start a new one while it runs. So the next player who accepts the quest within
-- those minutes gets no raiders and can never finish it. When the raid ends, Denphar now replaces the
-- old action list with an empty one, so the next raid can start straight away.
DELETE FROM `smart_scripts` WHERE `entryorguid`=62922 AND `source_type`=0 AND `id`=104;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(62922, 0, 104, 0, 38, 0, 100, 0, 1, 1, 0, 0, 0, 0, 80, 6292202, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Farmer Denphar - Raid over - Stop the raid action list');
DELETE FROM `smart_scripts` WHERE `entryorguid`=6292202 AND `source_type`=9;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(6292202, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 82, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Farmer Denphar - Raid over - Interactible');
