-- mod-turtle-content 940: part B, group 1 (2026-10-14, Max: 'go on fait 1'). Quests of the 'missing item or monster' list reachable in 3.3.5:
--   41306 It's All Ogre Now, 41307 They're Eating It!, 41308 Fishy Practices, 41309 Brittle Gnome More, 41346 A Mossy Mystery
--   Left out (checked one by one): 40130 Bael Modan dig site: crates underground; 40131 Bael Modan; 40133 Bael Modan; 40281 Shadowfang Keep Turtle object (dungeon additions: friend); 40282 after 40281; 40905 Emerald Sanctum raid; 40906 after 40905; 40963 Emerald Sanctum raid; 41038 Emerald Sanctum raid; 41118 Blood Ring arena tokens (Turtle system); 41119 idem; 41123 idem; 41129 idem; 41279 Turtle jewelcrafting; 41280 Turtle jewelcrafting; 41281 Turtle jewelcrafting; 41282 Turtle jewelcrafting; 41345 idol made by a Turtle-only spell; 41353 starts from a Lower Karazhan Halls drop (raid not in the module); 41552 Turtle jewelcrafting; 41775 item with no source even in Penqle; 41776 idem; 41777 idem; 41900 Sapta: rewards Turtle-only spells; 41901 Sapta; 41902 Sapta; 41903 Sapta; 41904 Sapta; 41941 no quest giver in Penqle; 41942 after 41941; 41984 items made by Turtle-only crafting spells; 42041 items made by Turtle-only survival spells; 80401 rewards Turtle Pounder mounts (Turtle mount collection); 80738 idem; 80739 idem
-- New creatures: 61913 Fanzy Sparkspring, 61977 Traxis. Guids 9988001-9988999, refs 9988000-9988999.
-- 3.3.5 rows touched: quest-giver flag on 8767 Sah'rhee; quest drops (QuestRequired) added to Boneflayer Ghoul, Frozen Soul, Skeletal Frostweaver, Skeletal Summoner, Splinterbone Captain, Splinterbone Centurion, Splinterbone Warrior, Steeljaw Snapper, Thorn Eater Ghoul; lootid set on none; Tel'Abim fishing loot (area 5121, Turtle table).
SET NAMES utf8mb4;

-- cleanup (safe to apply again)
DELETE FROM `quest_template` WHERE `ID` IN (41306,41307,41308,41309,41346);
DELETE FROM `quest_template_addon` WHERE `ID` IN (41306,41307,41308,41309,41346);
DELETE FROM `quest_offer_reward` WHERE `ID` IN (41306,41307,41308,41309,41346);
DELETE FROM `quest_request_items` WHERE `ID` IN (41306,41307,41308,41309,41346);
DELETE FROM `creature_queststarter` WHERE `quest` IN (41306,41307,41308,41309,41346);
DELETE FROM `creature_questender` WHERE `quest` IN (41306,41307,41308,41309,41346);
DELETE FROM `gameobject_queststarter` WHERE `quest` IN (41306,41307,41308,41309,41346);
DELETE FROM `gameobject_questender` WHERE `quest` IN (41306,41307,41308,41309,41346);
DELETE FROM `item_template` WHERE `entry` IN (56087,1041367,1041368,1041369);
DELETE FROM `item_dbc` WHERE `ID` IN (56087,1041367,1041368,1041369);
DELETE FROM `creature_template` WHERE `entry` IN (61913,61977);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (61913,61977);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (61913,61977);
DELETE FROM `creature_template_resistance` WHERE `CreatureID` IN (61913,61977);
DELETE FROM `creature_template_addon` WHERE `entry` IN (61913,61977);
DELETE FROM `creature_equip_template` WHERE `CreatureID` IN (61913,61977);
DELETE FROM `creature_text` WHERE `CreatureID` IN (61913,61977);
DELETE FROM `creature_loot_template` WHERE `Entry` IN (61913,61977);
DELETE FROM `npc_vendor` WHERE `entry` IN (61913,61977);
DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN (61913,61977);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (61913,61977);
DELETE FROM `gossip_menu_option` WHERE `MenuID` = 41608 AND `OptionID` = 0;
DELETE FROM `gossip_menu` WHERE `MenuID` IN (41608,41621);
DELETE FROM `npc_text` WHERE `ID` IN (61913,61977);
DELETE FROM `gameobject_template` WHERE `entry` IN (2020106);
DELETE FROM `gameobject_template_addon` WHERE `entry` IN (2020106);
DELETE FROM `reference_loot_template` WHERE `Entry` BETWEEN 9988000 AND 9988999;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7341 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7342 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7344 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7345 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7346 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7347 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7348 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 7352 AND `Item` = 1041367;
DELETE FROM `creature_loot_template` WHERE `Entry` = 14123 AND `Item` = 1041368;
DELETE FROM `creature_addon` WHERE `guid` BETWEEN 9988001 AND 9988999;
DELETE FROM `waypoint_data` WHERE `id` BETWEEN 99880010 AND 99889999;
DELETE FROM `creature` WHERE `guid` BETWEEN 9988001 AND 9988999;
DELETE FROM `gameobject` WHERE `guid` BETWEEN 9988001 AND 9988999;
DELETE FROM `fishing_loot_template` WHERE `Entry` = 5121;

-- Tel'Abim fishing
INSERT INTO `fishing_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(5121, 6358, 0, 9.6802, 0, 1, 1, 1, 1, 'Oily Blackmouth'),
(5121, 10096, 0, 0.1155, 0, 1, 1, 1, 1, 'Councillor\'s Cuffs'),
(5121, 13443, 0, 0.2889, 0, 1, 1, 1, 1, 'Superior Mana Potion'),
(5121, 13757, 0, 9.589, 0, 1, 1, 1, 1, 'Lightning Eel'),
(5121, 13758, 0, 5.4795, 0, 1, 1, 1, 1, 'Raw Redgill'),
(5121, 13759, 0, 12.3288, 0, 1, 1, 1, 1, 'Raw Nightfin Snapper'),
(5121, 13760, 0, 16.4384, 0, 1, 1, 1, 1, 'Raw Sunscale Salmon'),
(5121, 13889, 0, 0.05, 0, 1, 1, 1, 1, 'Raw Whitescale Salmon'),
(5121, 13890, 0, 14.3836, 0, 1, 1, 1, 1, 'Plated Armorfish'),
(5121, 13901, 0, 0.1733, 0, 1, 1, 1, 1, '15 Pound Salmon'),
(5121, 13903, 0, 0.1155, 0, 1, 1, 1, 1, '22 Pound Salmon'),
(5121, 56087, 0, 4.0, 0, 1, 1, 1, 1, 'Barnacle Covered Key');

-- quests
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `QuestInfoID`, `SuggestedGroupNum`, `RequiredFactionId1`, `RequiredFactionId2`, `RequiredFactionValue1`, `RequiredFactionValue2`, `RewardNextQuest`, `RewardXPDifficulty`, `RewardMoney`, `RewardMoneyDifficulty`, `RewardDisplaySpell`, `RewardSpell`, `RewardHonor`, `RewardKillHonor`, `StartItem`, `Flags`, `RequiredPlayerKills`, `RewardItem1`, `RewardAmount1`, `ItemDrop1`, `ItemDropQuantity1`, `RewardItem2`, `RewardAmount2`, `ItemDrop2`, `ItemDropQuantity2`, `RewardItem3`, `RewardAmount3`, `ItemDrop3`, `ItemDropQuantity3`, `RewardItem4`, `RewardAmount4`, `ItemDrop4`, `ItemDropQuantity4`, `RewardChoiceItemID1`, `RewardChoiceItemQuantity1`, `RewardChoiceItemID2`, `RewardChoiceItemQuantity2`, `RewardChoiceItemID3`, `RewardChoiceItemQuantity3`, `RewardChoiceItemID4`, `RewardChoiceItemQuantity4`, `RewardChoiceItemID5`, `RewardChoiceItemQuantity5`, `RewardChoiceItemID6`, `RewardChoiceItemQuantity6`, `POIContinent`, `POIx`, `POIy`, `POIPriority`, `RewardTitle`, `RewardTalents`, `RewardArenaPoints`, `RewardFactionID1`, `RewardFactionValue1`, `RewardFactionOverride1`, `RewardFactionID2`, `RewardFactionValue2`, `RewardFactionOverride2`, `RewardFactionID3`, `RewardFactionValue3`, `RewardFactionOverride3`, `RewardFactionID4`, `RewardFactionValue4`, `RewardFactionOverride4`, `RewardFactionID5`, `RewardFactionValue5`, `RewardFactionOverride5`, `TimeAllowed`, `AllowableRaces`, `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`, `RequiredNpcOrGo2`, `RequiredNpcOrGoCount2`, `RequiredNpcOrGo3`, `RequiredNpcOrGoCount3`, `RequiredNpcOrGo4`, `RequiredNpcOrGoCount4`, `RequiredItemId1`, `RequiredItemCount1`, `RequiredItemId2`, `RequiredItemCount2`, `RequiredItemId3`, `RequiredItemCount3`, `RequiredItemId4`, `RequiredItemCount4`, `RequiredItemId5`, `RequiredItemCount5`, `RequiredItemId6`, `RequiredItemCount6`, `Unknown0`, `ObjectiveText1`, `ObjectiveText2`, `ObjectiveText3`, `ObjectiveText4`, `VerifiedBuild`) VALUES
(41306, 2, 40, 36, 722, 0, 0, 0, 0, 0, 0, 41307, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'It\'s All Ogre Now', 'Search for Traxis\' lost bodyguard in the Razorfen Downs.', 'I am cursed with bad luck, I\'m telling you. You see, with all the pirates roaming around the trade routes nowadays, sending your cargo via ship is the same as directly handing it to those swashbucklers neatly tied with a bow on top. So clearly not an option. The other alternative I have is having it delivered by foot, equally risky, you\'ll surely know what I am talking about.$B$BEither way, I chose the latter option and because I really, REALLY, needed to deliver this cargo I looked for the most intimidating ogre here in Ratchet and paid him to accompany me on my way down to Steamwheedle Port. Too bad we were ambushed by undead zombie quilboar who took both the ogre and my precious cargo with them.$B$BI am getting desperate here. Can you retrieve my wares from the Razorfen Downs? I doubt they will be on my ogre guard anymore, but should he still be alive, he will know where they are.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41307, 2, 40, 36, 722, 0, 0, 0, 0, 0, 0, 41308, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1041367, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'They\'re Eating It!', 'Collect the missing cargo of Traxis and deliver it to his contractor in Steamwheedle Port in Tanaris.', 'Sah\'rhee is so sorry he failed. Sah\'rhee was not strong enough to protect little green friend and mean quilboar took me here. They want to eat me, but mother always said Sah\'rhee is too chubby, probably don\'t taste that good.$B$BIf you are looking for Traxis\' box, it is here, but all the stones fell out when they hit poor Sah\'rhee to walk faster. Now scary zombies and ghosts have all the sparkly gems! Sah\'rhee wants to go home, can you collect Traxis\' jewels and bring them to small gnome in Tanaris? Traxis\' said she is at the beach town waiting for the box!', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1041367, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41308, 2, 42, 36, 440, 0, 0, 0, 0, 0, 0, 41309, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1041368, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Fishy Practices', 'Bring eight Steeljaw Glands, a Greater Mystic Essence and a Crystal Vial to Fanzy\'s mysterious partner south of Steamwheedle Port.', 'Okay, scrap what I just said. I will definitely not order from him again. All these gemstones have brittle surfaces! How could this have happened? What did he do with them?$B$B<You explain to Fanzy how the jewels ended up in several undead stomachs and have been ruined by their bodily fluids.>$B$BUgh, you didn\'t have to explain it in such detail. Gross. Well, this is just perfect. Now I have extra work on my hands, and that\'s the last thing I can afford right now. But luckily you are here to help out. Oh, don\'t give me that look, I\'ll pay you instead of Traxis, it\'s in his best interest to not show his grimy mug here anytime soon.$B$BTo fix the gems we need something with a bit more oomph, your regular gemstone oil won\'t cut it here. Not far south of here is a small cove near the beach, you will find... let\'s say a business partner of mine there. Bring him the oily glands of the Steeljaw Snappers from the coast, a greater mystic essence and a crystal vial. Tell him I sent you.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1041368, 8, 11135, 1, 8925, 1, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41309, 2, 42, 36, 440, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1041369, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brittle Gnome More', 'Return with Zalashji\'s Gemstone Oil to Fanzy Sparkspring in Steamwheedle Port.', '<Zalashji squeezes the oily glands into the vial. Muttering unintelligible words under his raspy breath, he casts foreign magic, making the concoction glow in a vibrant light.>$B$BTake it, stranger. This oil should seal the cracks in the gems\' surfaces, while still allowing for accurate cuts. Now go, while I permit her to frequent me, I cannot say the same about you. I may be more hospitable than my brethren, but that does not mean my patience is endless.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1041369, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41346, 2, 58, 58, 5121, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'A Mossy Mystery', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 56087, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0);

INSERT INTO `quest_template_addon` (`ID`, `MaxLevel`, `AllowableClasses`, `SourceSpellID`, `PrevQuestID`, `NextQuestID`, `ExclusiveGroup`, `BreadcrumbForQuestId`, `RewardMailTemplateID`, `RewardMailDelay`, `RequiredSkillID`, `RequiredSkillPoints`, `RequiredMinRepFaction`, `RequiredMaxRepFaction`, `RequiredMinRepValue`, `RequiredMaxRepValue`, `ProvidedItemCount`, `SpecialFlags`) VALUES
(41306, 0, 0, 0, 0, 0, 0, 0, 0, 0, 755, 200, 0, 0, 0, 0, 0, 0),
(41307, 0, 0, 0, 41306, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(41308, 0, 0, 0, 41307, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(41309, 0, 0, 0, 41308, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
(41346, 0, 0, 0, 0, 0, 0, 0, 0, 0, 356, 300, 0, 0, 0, 0, 0, 1);

INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `Emote2`, `Emote3`, `Emote4`, `EmoteDelay1`, `EmoteDelay2`, `EmoteDelay3`, `EmoteDelay4`, `RewardText`, `VerifiedBuild`) VALUES
(41306, 0, 0, 0, 0, 0, 0, 0, 0, 'Are you here to help poor Sah\'rhee?', 0),
(41307, 0, 0, 0, 0, 0, 0, 0, 0, 'What is this? Traxis\' delivery? I\'ve been waiting ages for this! What\'s up with that goblin and his lackluster service? Either way, thank you for finishing his work. If he didn\'t have such exclusive contact, this would be the last time I\'m ordering anything from him.', 0),
(41308, 0, 0, 0, 0, 0, 0, 0, 0, 'I dare not call that tiny being a partner, but we share much valuable knowledge between us, so I tolerate her presence and requests. Tell me, what does she require today?', 0),
(41309, 0, 0, 0, 0, 0, 0, 0, 0, 'Oho, now that\'s the stuff. I can tell right away that we can salvage that mess of Traxis with this miracle mixture. Did you come along with Zalashji? He\'s a solitary... man? Snake? I don\'t know, but so far he didn\'t say no to a long and philosophical talk about the history and art of jewelcrafting. Who knows, maybe someday I will tell you how we two met!$B$BSince you helped me with preventing uncomfortable customer confrontations, let me reward you. Am I correct in assuming you\'re proficient in jewelcrafting as well? Don\'t be surprised, I\'m not a master in this craft for nothing. Let me share some of my knowledge for free, as just payment.', 0),
(41346, 0, 0, 0, 0, 0, 0, 0, 0, 'The chest opens and a wet odor escapes it. Inside you find some rusted trinkets - and a surprisingly immaculate piece of something broken. Picking it up, you feel a sense of danger coming from it. Harrowing.', 0);

INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`, `VerifiedBuild`) VALUES
(41307, 0, 0, '<The gnome doesn\'t seem to pay attentio to you.>', 0),
(41308, 0, 0, 'What is it you desire, landwalker?', 0),
(41309, 0, 0, 'Back so soon?', 0),
(41346, 0, 0, 'This old chest blends into the interior of the cave almost seamlessly. The letter ‘G\' is engraved atop the lock. Next to it, a tattered book, or rather what is left of it. Quickly glancing over it, you surmise this chest belonged to someone who lived here on the island. The last readable entry says something about getting some fish for today\'s meal.', 0);

INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(61977, 41306),
(8767, 41307),
(61913, 41308),
(8617, 41309);

INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(8767, 41306),
(61913, 41307),
(8617, 41308),
(61913, 41309);

INSERT INTO `gameobject_queststarter` (`id`, `quest`) VALUES
(2020106, 41346);

INSERT INTO `gameobject_questender` (`id`, `quest`) VALUES
(2020106, 41346);

UPDATE `creature_template` SET `npcflag` = `npcflag` | 2 WHERE `entry` IN (8767);

-- items
INSERT INTO `item_template` (`entry`, `class`, `subclass`, `SoundOverrideSubclass`, `name`, `displayid`, `Quality`, `Flags`, `FlagsExtra`, `BuyCount`, `BuyPrice`, `SellPrice`, `InventoryType`, `AllowableClass`, `AllowableRace`, `ItemLevel`, `RequiredLevel`, `RequiredSkill`, `RequiredSkillRank`, `requiredspell`, `requiredhonorrank`, `RequiredCityRank`, `RequiredReputationFaction`, `RequiredReputationRank`, `maxcount`, `stackable`, `ContainerSlots`, `stat_type1`, `stat_value1`, `stat_type2`, `stat_value2`, `stat_type3`, `stat_value3`, `stat_type4`, `stat_value4`, `stat_type5`, `stat_value5`, `stat_type6`, `stat_value6`, `stat_type7`, `stat_value7`, `stat_type8`, `stat_value8`, `stat_type9`, `stat_value9`, `stat_type10`, `stat_value10`, `ScalingStatDistribution`, `ScalingStatValue`, `dmg_min1`, `dmg_max1`, `dmg_type1`, `dmg_min2`, `dmg_max2`, `dmg_type2`, `armor`, `holy_res`, `fire_res`, `nature_res`, `frost_res`, `shadow_res`, `arcane_res`, `delay`, `ammo_type`, `RangedModRange`, `spellid_1`, `spelltrigger_1`, `spellcharges_1`, `spellppmRate_1`, `spellcooldown_1`, `spellcategory_1`, `spellcategorycooldown_1`, `spellid_2`, `spelltrigger_2`, `spellcharges_2`, `spellppmRate_2`, `spellcooldown_2`, `spellcategory_2`, `spellcategorycooldown_2`, `spellid_3`, `spelltrigger_3`, `spellcharges_3`, `spellppmRate_3`, `spellcooldown_3`, `spellcategory_3`, `spellcategorycooldown_3`, `spellid_4`, `spelltrigger_4`, `spellcharges_4`, `spellppmRate_4`, `spellcooldown_4`, `spellcategory_4`, `spellcategorycooldown_4`, `spellid_5`, `spelltrigger_5`, `spellcharges_5`, `spellppmRate_5`, `spellcooldown_5`, `spellcategory_5`, `spellcategorycooldown_5`, `bonding`, `description`, `PageText`, `LanguageID`, `PageMaterial`, `startquest`, `lockid`, `Material`, `sheath`, `RandomProperty`, `RandomSuffix`, `block`, `itemset`, `MaxDurability`, `area`, `Map`, `BagFamily`, `TotemCategory`, `socketColor_1`, `socketContent_1`, `socketColor_2`, `socketContent_2`, `socketColor_3`, `socketContent_3`, `socketBonus`, `GemProperties`, `RequiredDisenchantSkill`, `ArmorDamageModifier`, `duration`, `ItemLimitCategory`, `HolidayId`, `ScriptName`, `DisenchantID`, `FoodType`, `minMoneyLoot`, `maxMoneyLoot`, `flagsCustom`, `VerifiedBuild`) VALUES
(1041367, 12, 0, -1, 'Etched Gemstone', 1262, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, 'The surface is cracked and brittle.', 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(1041368, 12, 0, -1, 'Steeljaw Gland', 1438, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(1041369, 12, 0, -1, 'Zalashji\'s Gemstone Oil', 3663, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(56087, 15, 0, -1, 'Barnacle Covered Key', 9153, 3, 0, 0, 1, 1000, 1000, 0, -1, -1, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0);

INSERT INTO `item_dbc` (`ID`, `ClassID`, `SubclassID`, `Sound_Override_Subclassid`, `Material`, `DisplayInfoID`, `InventoryType`, `SheatheType`) VALUES
(1041367, 12, 0, -1, 4, 1262, 0, 0),
(1041368, 12, 0, -1, 3, 1438, 0, 0),
(1041369, 12, 0, -1, 3, 3663, 0, 0),
(56087, 15, 0, -1, 0, 9153, 0, 1);

-- creatures
INSERT INTO `creature_template` (`entry`, `difficulty_entry_1`, `difficulty_entry_2`, `difficulty_entry_3`, `KillCredit1`, `KillCredit2`, `name`, `subname`, `IconName`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `speed_swim`, `speed_flight`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `BaseVariance`, `RangeVariance`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `pickpocketloot`, `skinloot`, `PetSpellDataId`, `VehicleId`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HoverHeight`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RacialLeader`, `movementId`, `RegenHealth`, `CreatureImmunitiesId`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(61913, 0, 0, 0, 0, 0, 'Fanzy Sparkspring', 'Master Jewelcrafter', NULL, 41608, 57, 57, 0, 474, 19, 1.0, 1.14286, 1, 1, 20, 0, 0, 1.356, 2000, 2000, 1, 1, 1, 0, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1.621, 1, 0.998, 1, 0, 0, 1, 0, 0, '', 0),
(61977, 0, 0, 0, 0, 0, 'Traxis', NULL, NULL, 41621, 40, 40, 0, 35, 3, 1.0, 1.14286, 1, 1, 20, 0, 0, 1.344, 2000, 2000, 1, 1, 1, 0, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1.264, 1, 0.975, 1, 0, 0, 1, 0, 0, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(61913, 0, 7039, 1.0, 1, 0),
(61977, 0, 13969, 1.0, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`) VALUES
(61913, 1, 1, 0, 0, 0, 0, NULL),
(61977, 1, 1, 0, 0, 0, 0, NULL);

INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`, `em0_0`, `em0_1`, `em0_2`, `em0_3`, `em0_4`, `em0_5`, `text1_0`, `text1_1`, `BroadcastTextID1`, `lang1`, `Probability1`, `em1_0`, `em1_1`, `em1_2`, `em1_3`, `em1_4`, `em1_5`, `text2_0`, `text2_1`, `BroadcastTextID2`, `lang2`, `Probability2`, `em2_0`, `em2_1`, `em2_2`, `em2_3`, `em2_4`, `em2_5`, `text3_0`, `text3_1`, `BroadcastTextID3`, `lang3`, `Probability3`, `em3_0`, `em3_1`, `em3_2`, `em3_3`, `em3_4`, `em3_5`, `text4_0`, `text4_1`, `BroadcastTextID4`, `lang4`, `Probability4`, `em4_0`, `em4_1`, `em4_2`, `em4_3`, `em4_4`, `em4_5`, `text5_0`, `text5_1`, `BroadcastTextID5`, `lang5`, `Probability5`, `em5_0`, `em5_1`, `em5_2`, `em5_3`, `em5_4`, `em5_5`, `text6_0`, `text6_1`, `BroadcastTextID6`, `lang6`, `Probability6`, `em6_0`, `em6_1`, `em6_2`, `em6_3`, `em6_4`, `em6_5`, `text7_0`, `text7_1`, `BroadcastTextID7`, `lang7`, `Probability7`, `em7_0`, `em7_1`, `em7_2`, `em7_3`, `em7_4`, `em7_5`, `VerifiedBuild`) VALUES
(61913, 'The properties of gold seem to blend well with Star Ruby to create ornate jewelry with stunning appeal. A little tinkering with the shape and proportions could...$B$B<Fanzy is snapped back to reality.>$B$BHey, what are you doing here? Can\'t you see I\'m deep in study?$B$BOh, you\'re looking to learn advanced jewelcrafting? Well, you had better have a deep understanding of the vast and complex science of jewelcrafting before I even humor the thought of teaching you.', NULL, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(61977, 'I just can\'t catch a break.', NULL, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES
(41608, 61913),
(41621, 61977);

-- vendors and trainers
INSERT INTO `creature_default_trainer` (`CreatureId`, `TrainerId`) VALUES
(61913, 112);

-- SmartAI (Turtle spell lists + ported scripts)
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(41608, 0, 3, 'Train me.', 0, 5, 16, 0, 0, 0, 0, NULL, 0, 0);

-- spawns
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) VALUES
(9988001, 61913, 1, 0, 0, 1, 1, 0, -6908.71, -4852.65, 8.36977, 0.59453, 120, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle 939: Fanzy Sparkspring (tw guid 2582869)'),
(9988002, 61977, 1, 0, 0, 1, 1, 0, -980.036, -3635.91, 19.1743, 5.99098, 120, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle 939: Traxis (tw guid 2583254)');

-- objects
INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`, `Data0`, `Data1`, `Data2`, `Data3`, `Data4`, `Data5`, `Data6`, `Data7`, `Data8`, `Data9`, `Data10`, `Data11`, `Data12`, `Data13`, `Data14`, `Data15`, `Data16`, `Data17`, `Data18`, `Data19`, `Data20`, `Data21`, `Data22`, `Data23`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES
(2020106, 2, 5744, 'Mosscovered Chest', '', '', '', 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0);

INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`, `mingold`, `maxgold`, `artkit0`, `artkit1`, `artkit2`, `artkit3`) VALUES
(2020106, 0, 32, 0, 0, 0, 0, 0, 0);

INSERT INTO `gameobject` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `position_x`, `position_y`, `position_z`, `orientation`, `rotation0`, `rotation1`, `rotation2`, `rotation3`, `spawntimesecs`, `animprogress`, `state`, `ScriptName`, `VerifiedBuild`, `Comment`) VALUES
(9988001, 2020106, 1, 0, 0, 1, 1, -8405.63, -6884.02, 48.2447, 5.46592, 0.0, 0.0, 0.397354, -0.917666, 0, 100, 1, '', 0, 'turtle 939: Mosscovered Chest (tw guid 5019427) on wmo MD_MUSHROOMCAVE09.WMO (Kalimdor_44_47, patch-y): the chest is in the cave under Highvale Rise');

-- loot
-- Turtle's quest drops on creatures already in our world
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(7341, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Skeletal Frostweaver)'),
(7342, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Skeletal Summoner)'),
(7344, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Splinterbone Warrior)'),
(7345, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Splinterbone Captain)'),
(7346, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Splinterbone Centurion)'),
(7347, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Boneflayer Ghoul)'),
(7348, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Thorn Eater Ghoul)'),
(7352, 1041367, 0, 30.0, 1, 1, 0, 1, 1, 'Etched Gemstone (turtle 939, Frozen Soul)'),
(14123, 1041368, 0, 50.0, 1, 1, 0, 1, 1, 'Steeljaw Gland (turtle 939, Steeljaw Snapper)');

