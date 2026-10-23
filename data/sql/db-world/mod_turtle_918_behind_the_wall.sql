-- mod-turtle-content: Turtle quest 40841 "Behind The Wall" (2026-10-12, approved by Max). Therum Deepforge (Stormwind, 3.3.5 NPC,
-- gets the quest-giver flag) sends Alliance players into Gilneas City for the Dawnstone Plans (object 2020015, already in 007).
-- Rewards: Inlaid Plate Boots 61348 (3.3.5 plate-boots look with the same icon: Turtle's model has no 3.3.5 twin) or
-- Dwarven Battle Bludgeon 61349 (same look). The client learns both items from Item.dbc in patch-z.mpq.
SET NAMES utf8mb4;

DELETE FROM `item_template` WHERE `entry` IN (61348, 61349);
DELETE FROM `item_dbc` WHERE `ID` IN (61348, 61349);
DELETE FROM `quest_template` WHERE `ID` = 40841;
DELETE FROM `quest_template_addon` WHERE `ID` = 40841;
DELETE FROM `quest_offer_reward` WHERE `ID` = 40841;
DELETE FROM `quest_request_items` WHERE `ID` = 40841;
DELETE FROM `creature_queststarter` WHERE `quest` = 40841;
DELETE FROM `creature_questender` WHERE `quest` = 40841;

INSERT INTO `item_template` (`entry`, `class`, `subclass`, `SoundOverrideSubclass`, `name`, `displayid`, `Quality`, `Flags`, `FlagsExtra`, `BuyCount`, `BuyPrice`, `SellPrice`, `InventoryType`, `AllowableClass`, `AllowableRace`, `ItemLevel`, `RequiredLevel`, `RequiredSkill`, `RequiredSkillRank`, `requiredspell`, `requiredhonorrank`, `RequiredCityRank`, `RequiredReputationFaction`, `RequiredReputationRank`, `maxcount`, `stackable`, `ContainerSlots`, `stat_type1`, `stat_value1`, `stat_type2`, `stat_value2`, `stat_type3`, `stat_value3`, `stat_type4`, `stat_value4`, `stat_type5`, `stat_value5`, `stat_type6`, `stat_value6`, `stat_type7`, `stat_value7`, `stat_type8`, `stat_value8`, `stat_type9`, `stat_value9`, `stat_type10`, `stat_value10`, `ScalingStatDistribution`, `ScalingStatValue`, `dmg_min1`, `dmg_max1`, `dmg_type1`, `dmg_min2`, `dmg_max2`, `dmg_type2`, `armor`, `holy_res`, `fire_res`, `nature_res`, `frost_res`, `shadow_res`, `arcane_res`, `delay`, `ammo_type`, `RangedModRange`, `spellid_1`, `spelltrigger_1`, `spellcharges_1`, `spellppmRate_1`, `spellcooldown_1`, `spellcategory_1`, `spellcategorycooldown_1`, `spellid_2`, `spelltrigger_2`, `spellcharges_2`, `spellppmRate_2`, `spellcooldown_2`, `spellcategory_2`, `spellcategorycooldown_2`, `spellid_3`, `spelltrigger_3`, `spellcharges_3`, `spellppmRate_3`, `spellcooldown_3`, `spellcategory_3`, `spellcategorycooldown_3`, `spellid_4`, `spelltrigger_4`, `spellcharges_4`, `spellppmRate_4`, `spellcooldown_4`, `spellcategory_4`, `spellcategorycooldown_4`, `spellid_5`, `spelltrigger_5`, `spellcharges_5`, `spellppmRate_5`, `spellcooldown_5`, `spellcategory_5`, `spellcategorycooldown_5`, `bonding`, `description`, `PageText`, `LanguageID`, `PageMaterial`, `startquest`, `lockid`, `Material`, `sheath`, `RandomProperty`, `RandomSuffix`, `block`, `itemset`, `MaxDurability`, `area`, `Map`, `BagFamily`, `TotemCategory`, `socketColor_1`, `socketContent_1`, `socketColor_2`, `socketContent_2`, `socketColor_3`, `socketContent_3`, `socketBonus`, `GemProperties`, `RequiredDisenchantSkill`, `ArmorDamageModifier`, `duration`, `ItemLimitCategory`, `HolidayId`, `ScriptName`, `DisenchantID`, `FoodType`, `minMoneyLoot`, `maxMoneyLoot`, `flagsCustom`, `VerifiedBuild`) VALUES
(61348, 4, 4, -1, 'Inlaid Plate Boots', 18958, 2, 0, 0, 1, 24616, 6154, 8, -1, -1, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 6, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 388, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 13669, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 27, 0, 0, 0, 0, 0),
(61349, 2, 4, -1, 'Dwarven Battle Bludgeon', 19703, 2, 0, 0, 1, 75064, 18766, 21, -1, -1, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56.0, 91.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 2600, 0, 0.0, 17308, 2, 0, 1.0, 600000, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 27, 0, 0, 0, 0, 0);

INSERT INTO `item_dbc` (`ID`, `ClassID`, `SubclassID`, `Sound_Override_Subclassid`, `Material`, `DisplayInfoID`, `InventoryType`, `SheatheType`) VALUES
(61348, 4, 4, -1, 6, 18958, 8, 0),
(61349, 2, 4, -1, 1, 19703, 21, 3);

INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `QuestInfoID`, `SuggestedGroupNum`, `RewardXPDifficulty`, `RewardMoney`, `Flags`, `AllowableRaces`, `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `RequiredItemId1`, `RequiredItemCount1`, `ItemDrop1`, `ItemDropQuantity1`, `RewardChoiceItemID1`, `RewardChoiceItemQuantity1`, `RewardChoiceItemID2`, `RewardChoiceItemQuantity2`, `VerifiedBuild`, `ObjectiveText1`, `ObjectiveText2`, `ObjectiveText3`, `ObjectiveText4`) VALUES
(40841, 2, 41, 36, 5180, 81, 0, 6, 0, 8, 1101, 'Behind The Wall', 'Venture into Gilneas City and recover the Dawnstone Plans for Therum Deepforge in Stormwind.', 'Have you heard of the tidings from the north? The Greymane Wall lies open at last.$B$BI never thought I would see the day after hearing all the horrible things I did, and by the sounds of it, things don\'t bode well. Still, within Gilneas City one of my dearest friends used to work with a rare material called \'Dawnstone\' which could only be found within Gilneas itself.$B$BI have no doubt his patterns are still within his shop in the city, and I ask you to recover them for me. I would advise to bring some comrades in arms along with you; word has it that there is unrest, entailing worgen and civil war, so it certainly is not a safe place to venture alone.', '', '', 61347, 1, 61347, 1, 61348, 1, 61349, 1, 0, '', '', '', '');

INSERT INTO `quest_template_addon` (`ID`, `MaxLevel`, `AllowableClasses`, `ProvidedItemCount`, `SpecialFlags`) VALUES
(40841, 0, 0, 0, 0);

INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `Emote2`, `Emote3`, `Emote4`, `EmoteDelay1`, `EmoteDelay2`, `EmoteDelay3`, `EmoteDelay4`, `RewardText`, `VerifiedBuild`) VALUES
(40841, 0, 0, 0, 0, 0, 0, 0, 0, 'Are these it? I haven\'t had the opportunity to read these plans in quite some years.$B$BAdaman was an exceptionally talented blacksmith and I grieve deeply for his passing. I will make sure his findings are properly recorded here and in Ironforge, so that his name may earn the recognition he always deserved.$B$BThank you, $N. I have prepared something for you as well, as compensation for the immense trouble you put yourself through.', 0);

INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`, `VerifiedBuild`) VALUES
(40841, 0, 0, 'Have you had any luck with the plans?$B$BI know it is nothing easy I asked of you, but those plans were a man\'s life\'s work, it would be a tragedy if they were lost.', 0);

INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(5511, 40841);

INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(5511, 40841);

UPDATE `creature_template` SET `npcflag` = `npcflag` | 2 WHERE `entry` = 5511;
