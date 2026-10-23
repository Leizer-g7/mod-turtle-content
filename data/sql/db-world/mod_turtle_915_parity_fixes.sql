-- mod-turtle-content: parity fixes vs Turtle's world DB for the zones already in the module (2026-10-12, approved by Max).
-- 1. 53 quest drops Turtle put on 3.3.5 creatures (the converter only copied loot of Turtle's own creatures):
--    quests 40014, 40016, 40017, 40024, 40036, 40063, 40292, 40359, 40453, 40942, 40970, 40993, 40995, 41012, 41013, 41033, 41710, 41728, 41740, 41804, 41851, 60155, 80380 could not be finished.
--    Rows drop only for players on the quest (QuestRequired); 3.3.5 loot is unchanged.
-- 2. Markel Smythe (Booty Bay): Turtle's option that hands over the Zeppelin Motor (Favor For Spare Parts, 41703).
-- 3. A Curious Leaf (40583): the Mulgore druid chain start (the leaf on the ground -> Gennia Runetotem); A Dryad in Mulgore needs it again.
-- 4. Black Sealed Chest (Northwind): opening it turns The Dark Knight hostile, as on Turtle.
-- 5. Ancient Dirt Mound (Tel'Abim, 'Azotha Gold'): each dig summons a Vengeful Spirit that attacks, as on Turtle.
-- 6. 3.3.5 models for 3 NPCs that were invisible (their Turtle models do not exist in 3.3.5).
-- 7. Hidden (disables): quests that cannot be finished in Turtle's own data either.
SET NAMES utf8mb4;

-- cleanup (safe to apply again)
DELETE FROM `creature_loot_template` WHERE `Entry` = 689 AND `Item` = 1041814;
DELETE FROM `creature_loot_template` WHERE `Entry` = 1097 AND `Item` = 2924;
DELETE FROM `creature_loot_template` WHERE `Entry` = 1550 AND `Item` = 61606;
DELETE FROM `creature_loot_template` WHERE `Entry` = 1551 AND `Item` = 61606;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2375 AND `Item` = 1529;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2376 AND `Item` = 1041774;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2377 AND `Item` = 1041774;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2544 AND `Item` = 81013;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2559 AND `Item` = 60119;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2560 AND `Item` = 60119;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2561 AND `Item` = 60119;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2562 AND `Item` = 60108;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2562 AND `Item` = 60658;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2564 AND `Item` = 60108;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2564 AND `Item` = 60658;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2565 AND `Item` = 60109;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2592 AND `Item` = 60125;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2649 AND `Item` = 61720;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2650 AND `Item` = 61720;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2651 AND `Item` = 61720;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2652 AND `Item` = 61720;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2725 AND `Item` = 1041811;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2739 AND `Item` = 1041949;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2740 AND `Item` = 1041949;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2742 AND `Item` = 1041906;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2742 AND `Item` = 1041949;
DELETE FROM `creature_loot_template` WHERE `Entry` = 2743 AND `Item` = 1041949;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4328 AND `Item` = 61485;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4329 AND `Item` = 61485;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4331 AND `Item` = 61485;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4334 AND `Item` = 61485;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4668 AND `Item` = 61655;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4676 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4677 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4679 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4680 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4681 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4684 AND `Item` = 1041813;
DELETE FROM `creature_loot_template` WHERE `Entry` = 4705 AND `Item` = 61655;
DELETE FROM `creature_loot_template` WHERE `Entry` = 6116 AND `Item` = 60404;
DELETE FROM `creature_loot_template` WHERE `Entry` = 6117 AND `Item` = 60404;
DELETE FROM `creature_loot_template` WHERE `Entry` = 6196 AND `Item` = 60137;
DELETE FROM `creature_loot_template` WHERE `Entry` = 6351 AND `Item` = 60159;
DELETE FROM `creature_loot_template` WHERE `Entry` = 6371 AND `Item` = 60159;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7358 AND `Item` = 61657;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7864 AND `Item` = 60404;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7885 AND `Item` = 60137;
DELETE FROM `creature_loot_template` WHERE `Entry` = 11480 AND `Item` = 61695;
DELETE FROM `creature_loot_template` WHERE `Entry` = 11484 AND `Item` = 61695;
DELETE FROM `creature_loot_template` WHERE `Entry` = 11746 AND `Item` = 61694;
DELETE FROM `creature_loot_template` WHERE `Entry` = 11747 AND `Item` = 61694;
DELETE FROM `creature_loot_template` WHERE `Entry` = 14399 AND `Item` = 61695;
DELETE FROM `creature_loot_template` WHERE `Entry` = 14400 AND `Item` = 61695;
DELETE FROM `npc_text` WHERE `ID` IN (249901, 249903);
DELETE FROM `gossip_menu` WHERE `MenuID` IN (249901, 249902);
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (249901, 249902);
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 15 AND `SourceGroup` = 249901;
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (2499, 62485) AND `id` >= 100;
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 61118;
DELETE FROM `smart_scripts` WHERE `source_type` = 1 AND `entryorguid` IN (2020170, 2010977);
DELETE FROM `quest_template` WHERE `ID` = 40583;
DELETE FROM `quest_template_addon` WHERE `ID` = 40583;
DELETE FROM `quest_offer_reward` WHERE `ID` = 40583;
DELETE FROM `quest_request_items` WHERE `ID` = 40583;
DELETE FROM `gameobject_queststarter` WHERE `quest` = 40583;
DELETE FROM `creature_questender` WHERE `quest` = 40583;
DELETE FROM `creature_template` WHERE `entry` = 61118;
DELETE FROM `creature_template_model` WHERE `CreatureID` = 61118;
DELETE FROM `creature_template_movement` WHERE `CreatureId` = 61118;
DELETE FROM `creature_equip_template` WHERE `CreatureID` = 61118;
DELETE FROM `creature_template_addon` WHERE `entry` = 62779;
DELETE FROM `disables` WHERE `sourceType` = 1 AND `entry` IN (41667);

-- 1. quest drops
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(689, 1041814, 0, 38.0, 1, 1, 0, 1, 1, 'Crystal Spine Basilisk - Crystal Spine Scale (Turtle quest drop, quest 41728)'),
(1097, 2924, 0, 72.0, 1, 1, 0, 1, 1, 'Venture Co. Mechanic - Crocolisk Meat (Turtle quest drop, quest 80380)'),
(1550, 61606, 0, 5.0, 1, 1, 0, 1, 1, 'Thrashtail Basilisk - Crystalvein Ore (Turtle quest drop, quest 40970)'),
(1551, 61606, 0, 5.0, 1, 1, 0, 1, 1, 'Ironjaw Basilisk - Crystalvein Ore (Turtle quest drop, quest 40970)'),
(2375, 1529, 0, 20.0, 1, 1, 0, 1, 1, 'Torn Fin Coastrunner - Jade (Turtle quest drop, quest 40359)'),
(2376, 1041774, 0, 30.0, 1, 1, 0, 1, 1, 'Torn Fin Oracle - Finnigan\'s Notebook (Turtle quest drop, quest 41710)'),
(2377, 1041774, 0, 30.0, 1, 1, 0, 1, 1, 'Torn Fin Tidehunter - Finnigan\'s Notebook (Turtle quest drop, quest 41710)'),
(2544, 81013, 0, 40.0, 1, 1, 0, 1, 1, 'Southern Sand Crawler - Southern Sand Crawler Leg (Turtle quest drop, quest 60155)'),
(2559, 60119, 0, 20.0, 1, 1, 0, 1, 1, 'Highland Strider - Arathi Raptor Hide (Turtle quest drop, quest 40017)'),
(2560, 60119, 0, 20.0, 1, 1, 0, 1, 1, 'Highland Thrasher - Arathi Raptor Hide (Turtle quest drop, quest 40017)'),
(2561, 60119, 0, 20.0, 1, 1, 0, 1, 1, 'Highland Fleshstalker - Arathi Raptor Hide (Turtle quest drop, quest 40017)'),
(2562, 60108, 0, 10.0, 1, 1, 0, 1, 1, 'Boulderfist Ogre - Gortog\'s Beads (Turtle quest drop, quest 40016)'),
(2562, 60658, 0, 90.0, 1, 1, 0, 1, 1, 'Boulderfist Ogre - Boulderfist Truncheon (Turtle quest drop, quest 40453)'),
(2564, 60108, 0, 12.0, 1, 1, 0, 1, 1, 'Boulderfist Enforcer - Gortog\'s Beads (Turtle quest drop, quest 40016)'),
(2564, 60658, 0, 100.0, 1, 1, 0, 1, 1, 'Boulderfist Enforcer - Boulderfist Truncheon (Turtle quest drop, quest 40453)'),
(2565, 60109, 0, 20.0, 1, 1, 0, 1, 1, 'Giant Plains Creeper - Greater Venom Sacs (Turtle quest drop, quest 40014)'),
(2592, 60125, 0, 40.0, 1, 1, 0, 1, 1, 'Rumbling Exile - Inner Binding Bracer (Turtle quest drop, quest 40024)'),
(2649, 61720, 0, 32.0, 1, 1, 0, 1, 1, 'Witherbark Scalper - Witherbark Blood (Turtle quest drop, quest 41033)'),
(2650, 61720, 0, 32.0, 1, 1, 0, 1, 1, 'Witherbark Zealot - Witherbark Blood (Turtle quest drop, quest 41033)'),
(2651, 61720, 0, 32.0, 1, 1, 0, 1, 1, 'Witherbark Hideskinner - Witherbark Blood (Turtle quest drop, quest 41033)'),
(2652, 61720, 0, 32.0, 1, 1, 0, 1, 1, 'Witherbark Venomblood - Witherbark Blood (Turtle quest drop, quest 41033)'),
(2725, 1041811, 0, 12.0, 1, 1, 0, 1, 1, 'Scalding Whelp - Ensorcelled Whelp Scale (Turtle quest drop, quest 41740)'),
(2739, 1041949, 0, 10.0, 1, 1, 0, 1, 1, 'Shadowforge Tunneler - Right Part of Gemstone of Naraz (Turtle quest drop, quest 41851)'),
(2740, 1041949, 0, 10.0, 1, 1, 0, 1, 1, 'Shadowforge Darkweaver - Right Part of Gemstone of Naraz (Turtle quest drop, quest 41851)'),
(2742, 1041906, 0, 10.0, 1, 1, 0, 1, 1, 'Shadowforge Chanter - Memorials of the Battle of Grim Batol (Turtle quest drop, quest 41804)'),
(2742, 1041949, 0, 10.0, 1, 1, 0, 1, 1, 'Shadowforge Chanter - Right Part of Gemstone of Naraz (Turtle quest drop, quest 41851)'),
(2743, 1041949, 0, 10.0, 1, 1, 0, 1, 1, 'Shadowforge Warrior - Right Part of Gemstone of Naraz (Turtle quest drop, quest 41851)'),
(4328, 61485, 0, 18.0, 1, 1, 0, 1, 1, 'Firemane Scalebane - Potent Draconic Jewel (Turtle quest drop, quest 40942)'),
(4329, 61485, 0, 18.0, 1, 1, 0, 1, 1, 'Firemane Scout - Potent Draconic Jewel (Turtle quest drop, quest 40942)'),
(4331, 61485, 0, 18.0, 1, 1, 0, 1, 1, 'Firemane Ash Tail - Potent Draconic Jewel (Turtle quest drop, quest 40942)'),
(4334, 61485, 0, 18.0, 1, 1, 0, 1, 1, 'Firemane Flamecaller - Potent Draconic Jewel (Turtle quest drop, quest 40942)'),
(4668, 61655, 0, 20.0, 1, 1, 0, 1, 1, 'Burning Blade Summoner - Eye of Xythos (Turtle quest drop, quest 40993)'),
(4676, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Lesser Infernal - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4677, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Doomwarder - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4679, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Nether Maiden - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4680, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Doomwarder Captain - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4681, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Mage Hunter - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4684, 1041813, 0, 32.0, 1, 1, 0, 1, 1, 'Nether Sorceress - Lingering Fel Energy (Turtle quest drop, quest 41728)'),
(4705, 61655, 0, 20.0, 1, 1, 0, 1, 1, 'Burning Blade Invoker - Eye of Xythos (Turtle quest drop, quest 40993)'),
(6116, 60404, 0, 80.0, 1, 1, 0, 1, 1, 'Highborne Apparition - Highborne Essence (Turtle quest drop, quest 40292)'),
(6117, 60404, 0, 80.0, 1, 1, 0, 1, 1, 'Highborne Lichling - Highborne Essence (Turtle quest drop, quest 40292)'),
(6196, 60137, 0, 100.0, 1, 1, 0, 1, 1, 'Spitelash Myrmidon - Myrmidon Signet (Turtle quest drop, quest 40036)'),
(6351, 60159, 0, 35.0, 1, 1, 0, 1, 1, 'Storm Bay Oracle - Sprugbolt (Turtle quest drop, quest 40063)'),
(6371, 60159, 0, 35.0, 1, 1, 0, 1, 1, 'Storm Bay Warrior - Sprugbolt (Turtle quest drop, quest 40063)'),
(7358, 61657, 0, 100.0, 1, 1, 0, 1, 1, 'Amnennar the Coldbringer - Obsidian Phylactery (Turtle quest drop, quest 40995)'),
(7864, 60404, 0, 80.0, 1, 1, 0, 1, 1, 'Lingering Highborne - Highborne Essence (Turtle quest drop, quest 40292)'),
(7885, 60137, 0, 100.0, 1, 1, 0, 1, 1, 'Spitelash Battlemaster - Myrmidon Signet (Turtle quest drop, quest 40036)'),
(11480, 61695, 0, 11.0, 1, 1, 0, 1, 1, 'Arcane Aberration - Supercharged Arcane Resonation (Turtle quest drop, quest 41013)'),
(11484, 61695, 0, 11.0, 1, 1, 0, 1, 1, 'Residual Monstrosity - Supercharged Arcane Resonation (Turtle quest drop, quest 41013)'),
(11746, 61694, 0, 21.0, 1, 1, 0, 1, 1, 'Desert Rumbler - Fragment of Earth (Turtle quest drop, quest 41012)'),
(11747, 61694, 0, 21.0, 1, 1, 0, 1, 1, 'Desert Rager - Fragment of Earth (Turtle quest drop, quest 41012)'),
(14399, 61695, 0, 40.0, 1, 1, 0, 1, 1, 'Arcane Torrent - Supercharged Arcane Resonation (Turtle quest drop, quest 41013)'),
(14400, 61695, 0, 11.0, 1, 1, 0, 1, 1, 'Arcane Feedback - Supercharged Arcane Resonation (Turtle quest drop, quest 41013)');

-- 2. Markel Smythe
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`, `VerifiedBuild`) VALUES
(249901, 'Where are these goblins?! One would think they\'d cherish their precious gold above all else.', NULL, 0, 0, 1, 0),
(249903, 'BALOR?! How did they even manage to fly over there? This is the first time I\'ve ever heard of any zeppelin routing over that accursed island. Completely dumbfoundere, that\'s what I am! They are lucky that I am in desparate need of their cargo. Here, take the motor and make sure they come back here in one piece - with their wares!', NULL, 0, 0, 1, 0);

INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES
(249901, 249901),
(249902, 249903);

INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(249901, 0, 0, 'Are you Markel Smythe? The goblins you are looking for have been stranded on the island of Balor. I\'m here to get a spare zeppelin motor from you.', 0, 1, 1, 249902, 0, 0, 0, '', 0, 0);

UPDATE `creature_template` SET `gossip_menu_id` = 249901, `npcflag` = `npcflag` | 1 WHERE `entry` = 2499;
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` = 2499 AND `AIName` = '' AND `ScriptName` = '';

-- 3. A Curious Leaf
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `QuestInfoID`, `SuggestedGroupNum`, `RewardNextQuest`, `RewardXPDifficulty`, `RewardMoney`, `StartItem`, `Flags`, `RewardFactionID1`, `RewardFactionValue1`, `RewardFactionOverride1`, `AllowableRaces`, `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `RequiredItemId1`, `RequiredItemCount1`, `VerifiedBuild`, `ObjectiveText1`, `ObjectiveText2`, `ObjectiveText3`, `ObjectiveText4`) VALUES
(40583, 2, 5, 1, 215, 0, 0, 40584, 3, 112, 60830, 0, 81, 0, 5000, 690, 'A Curious Leaf', 'Take the Mysterious Leaf to Gennia Runetotem at Bloodhoof Village in Mulgore.', 'You have found what appears to be a rich lively leaf on the ground. Touching the leaf gives you an odd sensation, there is also no sign of the leaf dessecating. Perhaps the Druid trainer in Bloodhoof Village would know more?', '', '', 60830, 1, 0, '', '', '', '');

INSERT INTO `quest_template_addon` (`ID`, `MaxLevel`, `AllowableClasses`, `PrevQuestID`, `NextQuestID`, `ExclusiveGroup`, `ProvidedItemCount`, `SpecialFlags`) VALUES
(40583, 0, 0, 0, 0, 0, 1, 0);

INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `Emote2`, `Emote3`, `Emote4`, `EmoteDelay1`, `EmoteDelay2`, `EmoteDelay3`, `EmoteDelay4`, `RewardText`, `VerifiedBuild`) VALUES
(40583, 0, 0, 0, 0, 0, 0, 0, 0, 'By the Spirits?! That is no ordinary leaf. I have only seen a leaf like this during my time as an apprentice in Moonglade. This may be very urgent $C, and I will need your help.', 0);

INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`, `VerifiedBuild`) VALUES
(40583, 0, 0, 'Greetings young $C, what can I do for you?', 0);

INSERT INTO `gameobject_queststarter` (`id`, `quest`) VALUES
(2010924, 40583);

INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(3064, 40583);

UPDATE `quest_template_addon` SET `PrevQuestID` = 40583 WHERE `ID` = 40584;

-- 4./5. chest and dirt mound events
UPDATE `gameobject_template` SET `AIName` = 'SmartGameObjectAI' WHERE `entry` IN (2020170, 2010977) AND `ScriptName` = '';
INSERT INTO `creature_template` (`entry`, `name`, `subname`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RegenHealth`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(61118, 'Vengeful Spirit', NULL, 0, 57, 57, 0, 16, 0, 1.0, 1.14286, 18.0, 0, 0, 1.943, 1500, 2000, 2, 4608, 2048, 0, 0, 6, 0, 0, 0, 0, 'SmartAI', 0, 2.026, 1.032, 0.998, 1, 1, 0, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(61118, 0, 21300, 1, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`) VALUES
(61118, 1, 0, 0, 0, 0, 0);

INSERT INTO `creature_equip_template` (`CreatureID`, `ID`, `ItemID1`, `ItemID2`, `ItemID3`, `VerifiedBuild`) VALUES
(61118, 1, 17743, 0, 0, 0);

-- 6. models
UPDATE `creature_template_model` SET `CreatureDisplayID` = 10626 WHERE `CreatureID` = 60599 AND `Idx` = 0; -- Soulless Husk -> Soulless Ghoul model (Turtle display 18000)
UPDATE `creature_template_model` SET `CreatureDisplayID` = 6835 WHERE `CreatureID` = 62779 AND `Idx` = 0; -- Pathun Duskhide -> Grimtotem tauren model, riding a kodo (Turtle display 21396, a mounted tauren)
UPDATE `creature_template_model` SET `CreatureDisplayID` = 11874 WHERE `CreatureID` = 62985 AND `Idx` = 0; -- Deathtotem Behemoth -> Grimtotem Brute model at his own 1.7 scale (Turtle display 21395)
INSERT INTO `creature_template_addon` (`entry`, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras`) VALUES
(62779, 0, 11641, 0, 1, 0, 0, NULL);

UPDATE `creature_addon` ca JOIN `creature` c ON c.`guid` = ca.`guid` SET ca.`mount` = 11641 WHERE c.`id` = 62779;

-- 7. hidden quests
INSERT INTO `disables` (`sourceType`, `entry`, `flags`, `params_0`, `params_1`, `comment`) VALUES
(1, 41667, 0, '', '', 'mod-turtle-content: In Need of Shoes: Chaddus Suncarrier (Alah\'Thalas), who gives the horse shoes, has no spawn in Turtle either');

-- conditions
INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
(15, 249901, 0, 0, 0, 47, 0, 41703, 8, 0, 0, 0, 0, '', 'Markel Smythe - Favor For Spare Parts in progress'),
(15, 249901, 0, 0, 0, 2, 0, 1041765, 1, 0, 1, 0, 0, '', 'Markel Smythe - player has no Zeppelin Motor yet');

-- SmartAI
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(2499, 0, 100, 0, 62, 0, 100, 0, 249901, 0, 0, 0, 0, 0, 56, 1041765, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Markel Smythe - Gossip - Give Zeppelin Motor (Favor For Spare Parts, Turtle gossip script 249902)'),
(2020170, 1, 0, 0, 64, 0, 100, 0, 1, 0, 0, 0, 0, 0, 45, 1, 1, 0, 0, 0, 0, 19, 62485, 30, 0, 0, 0, 0, 0, 0, 'Black Sealed Chest - On Use - The Dark Knight turns on the player (Turtle event script 2020170)'),
(62485, 0, 100, 101, 38, 0, 100, 0, 1, 1, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'The Dark Knight - Chest opened - Hostile'),
(62485, 0, 101, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 21, 30, 0, 0, 0, 0, 0, 0, 0, 'The Dark Knight - Chest opened - Attack'),
(62485, 0, 102, 0, 7, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'The Dark Knight - On Evade - Back to his own faction'),
(61118, 0, 0, 0, 0, 0, 100, 0, 0, 0, 15000, 15000, 0, 0, 11, 10148, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Vengeful Spirit - In Combat - Cast Fireball (Turtle spell list 180094)'),
(2010977, 1, 0, 0, 64, 0, 100, 0, 1, 0, 0, 0, 0, 0, 12, 61118, 1, 60000, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Ancient Dirt Mound - On Use - Summon Vengeful Spirit, attacks the player (Turtle event script 61118)');
