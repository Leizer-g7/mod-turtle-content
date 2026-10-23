-- mod_turtle_925_post_merge_errors.sql (2026-10-13)
-- Clears the module lines the friend's 2026-10-12 merge added to Errors.log.
-- Tested on the cloud test server (same core, modules and data as Max's PC): applies twice cleanly,
-- and Errors.log keeps only stock 3.3.5 lines plus the two lines Max chose to keep (pools 9114001-25, quest 41315).

-- 1) 44 gameobjects (Tirisfal, Undercity, EPL, Burning Steppes...) were spawned with an all-zero rotation
--    quaternion. Build it from their orientation so the server stops falling back (same look in game).
UPDATE `gameobject` SET `rotation0` = 0, `rotation1` = 0, `rotation2` = SIN(`orientation` / 2), `rotation3` = COS(`orientation` / 2)
WHERE `guid` IN (9460012,9460018,9460036,9460063,9460100,9460177,9460188,9460191,9460260,9460261,9460291,9460297,9460301,9460328,9460329,9460330,9460331,9460339,9460422,9460423,9460424,9460473,9460525,9460548,9460563,9460655,9460656,9460657,9460691,9460701,9460702,9460703,9460704,9460718,9460764,9460765,9460766,9460770,9460777,9460834,9460836,9460844,9460847,9460849)
  AND `rotation0` = 0 AND `rotation1` = 0 AND `rotation2` = 0 AND `rotation3` = 0;

-- 2) Quest givers with a greeting menu but no gossip flag: the greeting text was never shown.
--    Bounty Hunter Knox 91749, Apothecary Villa 91750, Grock 91973.
UPDATE `creature_template` SET `npcflag` = `npcflag` | 1 WHERE `entry` IN (91749, 91750, 91973);
--    Karfang Grunt 60767 (Burning Steppes): Turtle's wind rider gossip ("I need a ride") has no 3.3.5 equivalent here
--    (the flight is a Turtle script). Unlink the unused menu instead of showing a dead option.
UPDATE `creature_template` SET `gossip_menu_id` = 0 WHERE `entry` = 60767 AND `npcflag` = 0;

-- 3) Young Brown Fox 80254 / Young Mist Fox 80258: Turtle fox family 36 does not exist in 3.3.5 (same fix 911 made for 80252).
UPDATE `creature_template` SET `family` = 0 WHERE `entry` IN (80254, 80258) AND `family` = 36;

-- 4) SmartAI rows the server skipped (so the scripts did nothing):
--    Vladeus Springriver: unused target_param2 on the threat-list credit.
UPDATE `smart_scripts` SET `target_param2` = 0 WHERE `entryorguid` = 50674 AND `source_type` = 0 AND `id` = 6;
--    Deathguard Maverick: timed action list "trap" had its timer type in the override slot.
UPDATE `smart_scripts` SET `action_param2` = 2, `action_param3` = 0 WHERE `entryorguid` = 51567 AND `source_type` = 0 AND `id` = 13;
--    Lucid Dream Stalker / Protector: repeat max was 0 -> cast every 60 s as Turtle does.
UPDATE `smart_scripts` SET `event_param4` = 60000 WHERE `entryorguid` IN (63065, 63066) AND `source_type` = 0 AND `id` = 0 AND `event_type` = 0;
--    Ancient Dirt Mound (Tel'Abim, from 915): attackInvoker must be 0/1, the value 2 made the whole row skipped,
--    so the Vengeful Spirit never appeared.
UPDATE `smart_scripts` SET `action_param4` = 1 WHERE `entryorguid` = 2010977 AND `source_type` = 1 AND `id` = 0;
--    Farm Raiders 41946 and The Moonhoof Celebration 42085 are completed by a script event, so they need the
--    exploration/event flag, otherwise the credit row is skipped and the quests can never be finished.
UPDATE `quest_template_addon` SET `SpecialFlags` = `SpecialFlags` | 2 WHERE `ID` IN (41946, 42085);

-- 5) Shadowforge Prowler 80207 (924): Turtle has no AI events for it, so plain melee AI.
UPDATE `creature_template` SET `AIName` = '' WHERE `entry` = 80207 AND `AIName` = 'SmartAI'
  AND NOT EXISTS (SELECT 1 FROM `smart_scripts` WHERE `entryorguid` = 80207 AND `source_type` = 0);

-- 6) Mavel Brightwood 50677: 913 rewrote her template without Turtle's loot / pickpocket tables (2000102 / 988008),
--    which left both tables unused. Turtle has them on her, so put them back.
UPDATE `creature_template` SET `lootid` = 2000102, `pickpocketloot` = 988008 WHERE `entry` = 50677;

-- 7) 'Fair Trade' Is Not Legally Defined in Azeroth 41272: Turtle zone 5130 does not exist in 3.3.5.
--    Its giver Coco Gucci stands in Undercity (1497).
UPDATE `quest_template` SET `QuestSortID` = 1497 WHERE `ID` = 41272 AND `QuestSortID` = 5130;
