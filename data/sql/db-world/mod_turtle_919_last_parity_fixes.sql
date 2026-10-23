-- mod-turtle-content: last parity fixes from the 2026-10-12 recheck against Penqle's core (tortoise-wow, latest 2026-10-11).
-- 1. Quest 41011 "The Upper Binding I": Turtle's Dragonkin Charge drops from Solakar Flamewreath (Upper Blackrock Spire;
--    AzerothCore summons him in the Father Flame event, so the 915 check, which looked at spawned creatures only, missed him).
--    Drops only for players on the quest (QuestRequired).
-- 2. Stormwrought Ruins secret portcullis: Turtle opens it only when all 4 Chamber Levers were pulled
--    (instance_stormwrought_ruins.cpp). The 003 rows counted every pull, so one lever pulled 4 times opened it.
--    Each lever now counts once (until the instance resets).
-- 3. World rares with Turtle C++ AI (tortoise-wow scripts/events/boss_rares.cpp) that fought with melee only here:
--    Tarangos (Azshara): Freeze 16350 every 60 s (first 15-60 s), Rend 17153 every 45 s (first 10-45 s).
--    Grug'thok the Seer (Feralas): Lightning Bolt 15207 every 10 s, Lightning Shield 10432 every 30 s,
--    Healing Stream Totem 10463 every 60 s.  Kin'Tozo (Stranglethorn): Enrage 12686 every 45 s, Sunder Armor 11596
--    every 20 s, and below 20% health Turtle's 28131 Enrage (3.3.5 "Frenzy") -> 8599 Enrage, as the converter does.
--    Ids 200+ (no collision with a zone rebuild).
SET NAMES utf8mb4;

DELETE FROM `creature_loot_template` WHERE `Entry` = 10264 AND `Item` = 61693;
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(10264, 61693, 0, 100, 1, 1, 0, 1, 1, 'Solakar Flamewreath - Dragonkin Charge (Turtle quest drop, quest 41011)');

UPDATE `smart_scripts` SET `event_flags` = `event_flags` | 1
WHERE `source_type` = 1 AND `entryorguid` IN (-9120020, -9120021, -9120022, -9120023) AND `id` = 100;

DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (49001, 49005, 80269) AND `id` BETWEEN 200 AND 299;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(49001, 0, 200, 0, 0, 0, 100, 0, 15000, 60000, 60000, 60000, 0, 0, 11, 16350, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Tarangos - In Combat - Cast Freeze (Turtle boss_rares.cpp)'),
(49001, 0, 201, 0, 0, 0, 100, 0, 10000, 45000, 45000, 45000, 0, 0, 11, 17153, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Tarangos - In Combat - Cast Rend (Turtle boss_rares.cpp)'),
(49005, 0, 200, 0, 0, 0, 100, 0, 2000, 10000, 10000, 10000, 0, 0, 11, 15207, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Grug''thok the Seer - In Combat - Cast Lightning Bolt (Turtle boss_rares.cpp)'),
(49005, 0, 201, 0, 0, 0, 100, 0, 10000, 30000, 30000, 30000, 0, 0, 11, 10432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grug''thok the Seer - In Combat - Cast Lightning Shield (Turtle boss_rares.cpp)'),
(49005, 0, 202, 0, 0, 0, 100, 0, 30000, 60000, 60000, 60000, 0, 0, 11, 10463, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grug''thok the Seer - In Combat - Cast Healing Stream Totem (Turtle boss_rares.cpp)'),
(80269, 0, 200, 0, 0, 0, 100, 0, 20000, 45000, 45000, 45000, 0, 0, 11, 12686, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Kin''Tozo - In Combat - Cast Enrage (Turtle boss_rares.cpp)'),
(80269, 0, 201, 0, 0, 0, 100, 0, 10000, 20000, 20000, 20000, 0, 0, 11, 11596, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Kin''Tozo - In Combat - Cast Sunder Armor (Turtle boss_rares.cpp)'),
(80269, 0, 202, 0, 2, 0, 100, 1, 0, 20, 0, 0, 0, 0, 11, 8599, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Kin''Tozo - Below 20% HP - Enrage (Turtle 28131 -> 8599)');
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (49001, 49005, 80269) AND `ScriptName` = '';
