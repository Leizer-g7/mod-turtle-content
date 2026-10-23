-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: Turtle-only Errors.log fixes (2026-10-11), checked against Turtle data.
-- Not touched on purpose (Max's choice): missing Turtle items 60204/60205/70182 (waiting for item data),
-- Caravan Meets Caravan orphan scripts (quest line not ported yet), Azshara gemstone pools 9114001-9114025.

-- 1. Profession trainers that were marked as class trainers (they teach Blacksmithing, Engineering, Cooking,
--    Herbalism, Enchanting, Alchemy). Type 2 = profession trainer.
UPDATE `trainer` SET `Type` = 2 WHERE `Type` = 0 AND `Id` IN (61277, 61438, 62143, 62282, 62286, 62290, 62299);

-- 2. NPCs whose Turtle greeting should open: add the gossip flag.
UPDATE `creature_template` SET `npcflag` = `npcflag` | 1 WHERE `entry` IN (80450, 80451, 80460, 81023, 61132);
-- Applebough is quest giver + vendor: his menu needs the shop line or the shop can't be opened.
DELETE FROM `gossip_menu_option` WHERE `MenuID` = 59140 AND `OptionID` = 0;
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(59140, 0, 1, 'I want to browse your goods.', 3370, 3, 128, 0, 0, 0, 0, '', 0, 0);

-- NPCs that can't be talked to in Turtle either (3 quest triggers, Bael Hardul Mountaineer, Blackthorn Footpad,
-- Dinkle Togpipe, Skrak): unlink the unused menu. No change in game.
UPDATE `creature_template` SET `gossip_menu_id` = 0 WHERE `entry` IN (60301, 60312, 60313, 60988, 61378, 91774, 91780);

-- 3. Quest 41659 The Sal'Galaz Mines: empty first objective ("6 of nothing", same in Turtle data).
UPDATE `quest_template` SET `RequiredNpcOrGoCount1` = 0 WHERE `ID` = 41659 AND `RequiredNpcOrGo1` = 0;

-- 4. Shagu's Shisha 2010700: action 85 (self cast) does not work on objects; 134 = the player casts the puff.
UPDATE `smart_scripts` SET `action_type` = 134 WHERE `entryorguid` = 2010700 AND `source_type` = 1 AND `id` = 101 AND `action_type` = 85;

-- 5. Cleanup, no change in game (the core already did these at startup).
-- 80 object spawns with all-zero rotation: store the facing they already use.
UPDATE `gameobject` SET `rotation2` = SIN(`orientation` / 2), `rotation3` = COS(`orientation` / 2)
WHERE `rotation0` = 0 AND `rotation1` = 0 AND `rotation2` = 0 AND `rotation3` = 0
  AND `guid` IN (9160236,9210001,9210002,9210003,9210004,9210006,9210007,9210262,9210263,9210265,9210266,9210267,9210268,9210269,9210270,9210271,9210278,9210279,9210289,9210290,9210291,9210292,9210293,9210294,9210295,9210296,9210297,9210299,9210300,9210301,9230011,9230035,9230054,9230055,9230056,9230067,9230068,9230125,9230126,9230127,9230130,9230224,9240001,9240282,9240300,9240301,9240302,9240303,9240304,9240305,9240306,9240307,9240308,9240309,9240310,9240311,9240312,9240313,9290003,9290100,9290101,9290102,9320236,9340066,9340078,9340382,9340405,9340406,9340407,9340408,9340409,9340437,9370039,9370164,9370165,9410034,9410070,9410077,9410078,9410079);
UPDATE `creature_template` SET `unit_class` = 1 WHERE `entry` IN (9100001, 9100002, 9100003, 9100004) AND `unit_class` = 0;
UPDATE `creature_template` SET `family` = 0 WHERE `entry` = 80252 AND `family` = 36;   -- Turtle-only Fox family
UPDATE `creature_equip_template` SET `ItemID2` = 0 WHERE `CreatureID` IN (60935, 60936, 60937) AND `ItemID2` = 4130;
UPDATE `creature_equip_template` SET `ItemID1` = 0 WHERE `CreatureID` = 60949 AND `ItemID1` = 5085;
UPDATE `quest_template_addon` SET `SpecialFlags` = `SpecialFlags` | 1 WHERE `ID` = 40337;
