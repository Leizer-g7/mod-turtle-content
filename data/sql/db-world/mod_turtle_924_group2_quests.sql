-- mod-turtle-content: group 2 (2026-10-12, approved by Max): 14 Turtle quests in 3.3.5 zones that the converter did not build.
--   Duskwood:  70054 Grave Injustice, 70055 Defias of Duskwood, 70056 Report to Darkshire, 70057 A Simple Memory, 70058 Law & Ogre
--   Loch Modan: 70053 The Loch Menace, 41905 Dark Iron Aggression, 41906 No Mercy For The Wicked
--   Stormwind: 60108 Arugal's Folly, 60109 The Missing Sorcerer (ends at Sorcerer Ashcrombe, Shadowfang Keep)
--   Undercity: 60116 Paint the Roses Red (60117 points to it again)   Thunder Bluff: 41758 Tainted Brambleheart (Rotthorn, RFK)
--   80397 Sap Their Strength (Innkeeper Faralia)   80398 A Pounding Brain (Intact Pounder Mainframe, Crowd Pummeler 9-60)
-- Loch Modan: Turtle's Shadowforge camp southwest of Farstrider Lodge (18 Prowlers, a Fire Priest with the Dark Key, its props),
--   the 11 Stolen Crates of Penqle's 2026-10-08 update, and the Shadowforge Cage (Turtle's script credited another quest: here
--   the cage is a Dark Key goober that gives 41906's objective). 3.3.5's buzzards, boar and Lord Condar stay where they are.
--   Props left out: 1 x Dark Iron keg (no 3.3.5 display row); 1 x blood elf female skeleton (Turtle-only model); 2 x shrub (no 3.3.5 display row); 1 x trigger of the deprecated quest 80204; 36 x wooden spike palisade (no 3.3.5 display row).
-- 3.3.5 NPCs changed: Watcher Paige, Warg Deepwater, Sorcerer Ashcrombe get the quest-giver flag (his gossip is unchanged).
-- New items are also in the client patch (patch-z.mpq Item.dbc); lock 1866 (Dark Key) is in patch-z Lock.dbc.
-- Ids: creature/gameobject guids 9990401-9990499, reference loot 9990000-9991999.
SET NAMES utf8mb4;

-- cleanup (makes the file safe to apply again)
DELETE FROM `quest_template` WHERE `ID` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `quest_template_addon` WHERE `ID` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `quest_offer_reward` WHERE `ID` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `quest_request_items` WHERE `ID` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `creature_queststarter` WHERE `quest` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `creature_questender` WHERE `quest` IN (41758,41905,41906,60108,60109,60116,70053,70054,70055,70056,70057,70058,80397,80398);
DELETE FROM `item_template` WHERE `entry` IN (1041853,1042072,1050800,1051805,1051832,1051833,1051834,58089,58090,58091,70034,70035,70036,70037,70044,70045,70046,70047,70048,80216,81275);
DELETE FROM `item_dbc` WHERE `ID` IN (1041853,1042072,1050800,1051805,1051832,1051833,1051834,58089,58090,58091,70034,70035,70036,70037,70044,70045,70046,70047,70048,80216,81275);
DELETE FROM `creature_template` WHERE `entry` IN (62503,80205,80207);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (62503,80205,80207);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (62503,80205,80207);
DELETE FROM `creature_equip_template` WHERE `CreatureID` IN (62503,80205,80207);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (62503,80205,80207);
DELETE FROM `creature_loot_template` WHERE `Entry` IN (62503,80205,80207);
DELETE FROM `creature_loot_template` WHERE `Entry` IN (218, 6229) AND `Item` IN (70035, 81275);
DELETE FROM `reference_loot_template` WHERE `Entry` BETWEEN 9990000 AND 9991999;
DELETE FROM `creature` WHERE `guid` BETWEEN 9990401 AND 9990499;
DELETE FROM `gameobject` WHERE `guid` BETWEEN 9990401 AND 9990499;
DELETE FROM `gameobject_template` WHERE `entry` IN (2020263,3000203,2000115,2001978,2010406);
DELETE FROM `gameobject_template_addon` WHERE `entry` IN (2020263,3000203,2000115,2001978,2010406);
DELETE FROM `gameobject_loot_template` WHERE `Entry` = 2020263;
DELETE FROM `lock_dbc` WHERE `ID` = 1866;

-- quests
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `QuestInfoID`, `SuggestedGroupNum`, `RequiredFactionId1`, `RequiredFactionId2`, `RequiredFactionValue1`, `RequiredFactionValue2`, `RewardNextQuest`, `RewardXPDifficulty`, `RewardMoney`, `RewardMoneyDifficulty`, `RewardDisplaySpell`, `RewardSpell`, `RewardHonor`, `RewardKillHonor`, `StartItem`, `Flags`, `RequiredPlayerKills`, `RewardItem1`, `RewardAmount1`, `ItemDrop1`, `ItemDropQuantity1`, `RewardItem2`, `RewardAmount2`, `ItemDrop2`, `ItemDropQuantity2`, `RewardItem3`, `RewardAmount3`, `ItemDrop3`, `ItemDropQuantity3`, `RewardItem4`, `RewardAmount4`, `ItemDrop4`, `ItemDropQuantity4`, `RewardChoiceItemID1`, `RewardChoiceItemQuantity1`, `RewardChoiceItemID2`, `RewardChoiceItemQuantity2`, `RewardChoiceItemID3`, `RewardChoiceItemQuantity3`, `RewardChoiceItemID4`, `RewardChoiceItemQuantity4`, `RewardChoiceItemID5`, `RewardChoiceItemQuantity5`, `RewardChoiceItemID6`, `RewardChoiceItemQuantity6`, `POIContinent`, `POIx`, `POIy`, `POIPriority`, `RewardTitle`, `RewardTalents`, `RewardArenaPoints`, `RewardFactionID1`, `RewardFactionValue1`, `RewardFactionOverride1`, `RewardFactionID2`, `RewardFactionValue2`, `RewardFactionOverride2`, `RewardFactionID3`, `RewardFactionValue3`, `RewardFactionOverride3`, `RewardFactionID4`, `RewardFactionValue4`, `RewardFactionOverride4`, `RewardFactionID5`, `RewardFactionValue5`, `RewardFactionOverride5`, `TimeAllowed`, `AllowableRaces`, `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`, `RequiredNpcOrGo2`, `RequiredNpcOrGoCount2`, `RequiredNpcOrGo3`, `RequiredNpcOrGoCount3`, `RequiredNpcOrGo4`, `RequiredNpcOrGoCount4`, `RequiredItemId1`, `RequiredItemCount1`, `RequiredItemId2`, `RequiredItemCount2`, `RequiredItemId3`, `RequiredItemCount3`, `RequiredItemId4`, `RequiredItemCount4`, `RequiredItemId5`, `RequiredItemCount5`, `RequiredItemId6`, `RequiredItemCount6`, `Unknown0`, `ObjectiveText1`, `ObjectiveText2`, `ObjectiveText3`, `ObjectiveText4`, `VerifiedBuild`) VALUES
(41758, 2, 32, 25, 1717, 0, 0, 0, 0, 0, 0, 0, 6, 2500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1041853, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1041854, 1, 1041855, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 81, 0, 30000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'Tainted Brambleheart', 'Destroy the living embodiment of natural corruption within the depths of Razorfen Kraul, and bring the Tainted Brambleheart to Kym Wildmane in Thunderbluff.', 'The quilboar are a primitive and hostile race, their kind has been at odds with us for longer than I can remember. Wherever the quilboar go they are often weaving large and heavy brushes of thorn. It is this very magic itself that is twisting the natural order, and in turn bringing it closer to corruption. For some months I have been able to sense something strange, and foreign.$B$BI seek proof of this natural corruption, and I am certain it lays within the heart of Razorfen Kraul. Find the living embodiment of this gnarled natural magic, and destroy it. When this task is complete, return to me.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1041853, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41905, 2, 18, 12, 38, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1042072, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 269, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Dark Iron Aggression', 'Recover the robbed provisions from the Dark Iron and bring them to Kelt Thomasin at the Farstrider Lodge.', 'While most of the caravans already departed to Stormwind, and eventually to Alah\'thalas, there are still many refugees who either wish to aid us here in the Farstrider Lodge or are still preparing for their journey.$B$BI wish I could say the same about the Dark Iron that roam the surrounding mountain ranges. Their horrible actions during the High Elves\' arrival in Loch Modan still continue to this day. Just recently they raided the last convoy on its way to Ironforge, stealing valuable supplies from those needing them most. $n, I appeal to your good heart to return what has been stolen to their rightful owners.$B$BThe Dark Iron set up camp in the southwest, be wary of their insidious tricks. They cannot be trusted under any circumstance.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1042072, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(41906, 2, 18, 12, 38, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 929, 3, 3385, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 269, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'No Mercy For The Wicked', 'Free the abducted High Elven family from the Dark Iron camp.', 'They are no different than the wild beasts we hunt. The Dark Iron violate the peace of my people by refusing them to find a new home after everything they endured. Not only are they ambushing our caravans to Ironforge, but just recently they began abducting innocents.$B$B$n, will you assist us in rescuing these poor souls? I dare not think about what the dwarves intend to do with them, given that even a child is among the captives. Will they be put into slave labour in the deep mines of the Blackrock Mountain, like the mountaineers tell us? They will not survive it, should it come to pass.$B$BPlease, ensure they have their chance on a brighter future after the horrors of Menethil\'s crusade. Release them from their prison, I am certain one of the Dark Iron has the key for it on him.$B$BThey\'ve been taken to their camp in the southwest.', '', '', -3000203, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(60108, 2, 27, 22, 209, 81, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1051805, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 72, 0, 20000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Arugal\'s Folly', 'High Sorcerer Andromath has tasked you with the death of Archmage Arugal. Return to him when you\'re done.', 'Greetings, $C!$B$BWe\'ve been on the tail of Archmage Arugal for some time, since the end of the Third War actually. What did he do? When the Scourge came to Dalaran, we were devastated.$B$BSeeing our friends and family being turned undead really messed with his mind. He thought the solution was a summoning ritual, to summon something that could aid us and stop the Scourge\'s advance. Even though as his mentor I advised against his idea, my warnings fell on deaf ears.$B$BThe resulting monstrosities are the Worgen. Even though they killed the Scourge, they quickly turned on us, worsening the situation. After going mad with his failure, he adopted the worgen as his children and retreated to Shadowfang Keep.$B$BAfter what had transpired I moved to Stormwind to try to forget what happened. Although it pains my heart to say this, you must travel to Shadowfang Keep in southern Silverpine Forest and end his life.', '', '', 4275, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '0', '', '', 0),
(60109, 2, 24, 22, 209, 81, 0, 0, 0, 0, 0, 0, 5, 5000, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 72, 0, 25000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'The Missing Sorcerer', 'High Sorcerer Andromath wants you to travel to Shadowfang Keep in Silverpine Forest and find out what happened to Sorcerer Ashcrombe.', 'One of my esteemed colleagues set off to gather vital information about the plots that the nefarious archmage Arugal is hatching inside of Shadowfang Keep, but I have not gotten word from him since. I am concerned about the corrupting influence that place has on even the most powerful and capable mages, and I need to know the fate of Sorcerer Ashcrombe.$B$BTravel to Silverpine Forest and seek him out for me at the Keep. If the Light wills it, find out what he has learned.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(60116, 2, 29, 27, 796, 1, 0, 0, 0, 0, 0, 0, 6, 2500, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1051832, 1, 1051833, 1, 1051834, 1, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'Paint the Roses Red', 'Eliminate the Scarlet forces outside the Scarlet Monastery, then return to Deathguard Burgess in Brill.', 'It\'s about time someone with some skills showed up around here! It\'s one thing to send fresh bodies after the lower Scarlet ranks, but I need an experienced $C if we\'re going to bring down the zealots on their own grounds.$B$BHmm. I seem to recall you being quite the efficient killer. Let me see that you\'ve still got what it takes to serve. Thin the ranks outside the Monastery!', '', '', 4281, 5, 4280, 5, 4283, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70053, 2, 20, 18, 38, 0, 0, 0, 0, 0, 0, 0, 4, 1000, 0, 0, 0, 0, 0, 0, 8, 0, 70034, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 47, 0, 15000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'The Loch Menace', 'Slay Threshadons in Loch Modan and return to Warg Deepwater in Loch Modan.', 'Something\'s wrong with the threshadons, $N. They\'re out from hiding and are eating all the fish of the lake! They\'ve been harming our business for a while now, and soon there may be nothing left.$B$BThey are beautiful creatures... We\'ve shared the lake for generations, so it pains me that we must take such extreme actions against them. I\'ve come to accept that we must cull their numbers so we can keep our livelihoods.$B$BIt\'s only expected of me to ask an outsider to do what we cannot and are not willing to do.', '', '', 1224, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70054, 2, 25, 22, 10, 0, 0, 0, 0, 0, 0, 70055, 3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 70035, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Grave Injustice', 'Investigate the grave robbers\' activity at the cemetery.', 'These lands aren\'t what they used to be, $C. Monsters have taken what\'s left of it, both the living and the dead.$B$BThere have been reports of grave robbers in the cemetery at Raven Hill. A crime this vile and depraved cannot go unpunished.$B$BPlease, head west to the cemetery and investigate this matter. If you find any grave robbers, get rid of them.$B$BThe place was already desecrated by the Scourge. The living shouldn\'t disturb the dead even further.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 70035, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70055, 2, 27, 24, 10, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70036, 1, 70037, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Defias of Duskwood', 'Slay members of the Defias Brotherhood in Duskwood and return to Watcher Paige.', 'I can only think of one person with those initials and that would be Sven Yorgen. He used to own the Yorgen Farmstead. In all of the chaos the farmstead was lost to the Defias Brotherhood who slowly made their way from Westfall.$B$BI assume Sven has nothing to do with the grave robbers, but the Defias might. Seems to me it\'s only a coincidence. In any case, the Defias must be brought to an end. We have enough on our plate when it comes to enemies and culling some of their numbers will bring peace to those who have yet to given up on their home.$B$BTherefore I ask that you slay any Defias in your way. The Night Watch has seen their activity in Addle\'s Stead prior to your investigations, so perhaps it\'d be best to start there, $N.', '', '', 909, 15, 215, 5, 910, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70056, 2, 27, 26, 10, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 70044, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Report to Darkshire', 'Bring Watcher Paige\'s report to Commander Althea Ebonlocke in Darkshire.', 'You have done me and the people of Duskwood a great favour, one I would like you to report to my commander.$B$BI am more than sure she will like to hear of your success against the Defias, and she will probably have another job for you.$B$BTake this parchment to Commander Althea Ebonlocke. She is stationed in front of the town hall so she\'ll be hard to miss.$B$BOh, and, $N, thank you.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 70044, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70057, 2, 27, 26, 10, 0, 0, 0, 0, 0, 0, 0, 5, 1000, 0, 0, 0, 0, 0, 70035, 0, 0, 70045, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'A Simple Memory', 'Bring the shovel to Sven Yorgen.', 'I hear Sven has taken shelter in a camp northwest of the Raven Hill Cemetery. I fear he\'s filled with regrets and anger, both at himself and those who took everything from him.$B$BConsidering we\'ve found this shovel of his among the ruins of his lost home, I think it would be appropriate to see it returned to him.$B$BPlease, be careful when you return this to Sven. He may be relieved to see it, or he might just break it in half in anguish. Who knows.$B$BThank you again, for all you\'ve done.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 70035, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(70058, 2, 28, 26, 10, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70046, 1, 70047, 1, 70048, 1, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Law & Ogre', 'Kill Splinter Fist Ogres in the Vul\'Gol Ogre Mound.', 'You have proven your worth to Paige, and frankly we can always use more hands in the Night Watch.$B$BWhile our forces focus on the worgen and the Scourge we would like you to take a trip to the south to Vul\'Gol Ogre Mound and reduce the ogre population.$B$BThere are only a few details that we know about the mound, but what we do know is that we need to be rid of the ogres. They are a threat to our scouts and to the roads leading to Westfall and Stranglethorn.$B$BThere\'s a reward waiting for you when you return, of course.', '', '', 212, 4, 1251, 4, 891, 4, 892, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(80397, 2, 24, 20, 467, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 2459, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 69, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Sap Their Strength', 'Slay 10 Sap Beasts and 6 Corrosive Sap Beasts, then return to Innkeeper Faralia.', 'Welcome, $C. We don\'t see many adventurers up this way — and not without reason.$B$BThe greed of the Venture Company has tainted the land itself. Every ancient tree that they fell only adds to my troubles.$B$BThe powerful sap that once nourished the trees of this forest now congeals into those awful sap beasts. Their corrosive nature harms the delicate balance we\'ve fought to maintain here.$B$BWorse still, many have recently made their way to Stonetalon Peak itself! Their corrosive sap kills the herbs I need for cooking and simple potions.$B$B$C, venture forth and rid the Peak of these things. You\'ll find many just south of here, over the ridge that holds the old ruins. We\'ve little enough use for coin up here, but perhaps a few potions might serve as payment?', '', '', 4020, 10, 4021, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0),
(80398, 2, 30, 30, 721, 0, 0, 0, 0, 0, 0, 0, 4, 2500, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 81275, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 21, 0, 15000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'A Pounding Brain', 'Find Someone who can figure out what to do with the Mainframe.', 'You find out that the Pounder\'s Mainframe is surprisingly intact. This could be valuable!$B$BTake it to an expert of Gnomish Engineering who might be able to do something with it.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 81275, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0);

INSERT INTO `quest_template_addon` (`ID`, `MaxLevel`, `AllowableClasses`, `SourceSpellID`, `PrevQuestID`, `NextQuestID`, `ExclusiveGroup`, `BreadcrumbForQuestId`, `RewardMailTemplateID`, `RewardMailDelay`, `RequiredSkillID`, `RequiredSkillPoints`, `RequiredMinRepFaction`, `RequiredMaxRepFaction`, `RequiredMinRepValue`, `RequiredMaxRepValue`, `ProvidedItemCount`, `SpecialFlags`) VALUES
(41758, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(41905, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(41906, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(60108, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(60109, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(60116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(70053, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(70054, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(70055, 0, 0, 0, 70054, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(70056, 0, 0, 0, 70055, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
(70057, 0, 0, 0, 70055, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
(70058, 0, 0, 0, 70056, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80397, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80398, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `Emote2`, `Emote3`, `Emote4`, `EmoteDelay1`, `EmoteDelay2`, `EmoteDelay3`, `EmoteDelay4`, `RewardText`, `VerifiedBuild`) VALUES
(41758, 0, 0, 0, 0, 0, 0, 0, 0, 'I sense something deep within the heart of this creature... It yearned for release, to combat a darkness that lurked.$B$B<Kym Wildmane looks confused, and lets out a slight sigh.>$B$BPerhaps my original assessment was incorrect. It was not the primitive dark magic of the quilboar that awakened this natural being and sent it into madness. No, it was something much darker, and sinister... I have more questions that I must research further. You have done well, regardless of my pondering. Please, take this, as a thanks from myself.', 0),
(41905, 0, 0, 0, 0, 0, 0, 0, 0, 'You did it! I am relieved to see you safe and sound, as well. With these returned, the group may continue their journey to their new home once more.', 0),
(41906, 0, 0, 0, 0, 0, 0, 0, 0, '$N! You\'re here! As soon as I saw them return to the lodge, I knew you were successful, yet I still feared for your safety. You have my deepest gratitude. Not only did you risk your life for the innocent, but also braved dangers beyond what the usual adventurer faces.$B$BPlease, have one of these as a token of the good deeds you fulfilled this day.$N!', 0),
(60108, 0, 0, 0, 0, 0, 0, 0, 0, 'Thanks, hero, it had to be done. Take this, the last memory I have left of him.', 0),
(60109, 0, 0, 0, 0, 0, 0, 0, 0, 'High Sorcerer Andromath sent you?$B$BMy, how the time flies when you\'re watching insanity and horror unfold from every angle.$B$BI will have to return with my findings and reassure him that I have not fallen to the same madness as those who are trapped here.', 0),
(60116, 0, 0, 0, 0, 0, 0, 0, 0, 'Now our forces may enter the Monastery fresh for battle and with the advantage of surprise. Varimathras shall be pleased.', 0),
(70053, 0, 0, 0, 0, 0, 0, 0, 0, 'You\'re saying they were smaller in size? That\'d explain their hunger.$B$BHowever, what would make them leave their nest so early and why all of them?$B$B<Warg ponders the thought for a while and turns back to you.>$B$BHere\'s the payment as promised. I will investigate further.', 0),
(70054, 0, 0, 0, 0, 0, 0, 0, 0, 'Good work, $C. What\'s that shovel you\'ve got there? I think I recognize the initials.', 0),
(70055, 0, 0, 0, 0, 0, 0, 0, 0, 'While I am glad we reduced their number it never pleases me to take lives, directly or indirectly.', 0),
(70056, 0, 0, 0, 0, 0, 0, 0, 0, 'You have my gratitude for aiding Paige. She\'s been in that camp for a great deal of time.$B$BAlas, there\'s little we can do in the situation we\'re in.', 0),
(70057, 0, 0, 0, 0, 0, 0, 0, 0, 'What do you have there, $C?$B$BOh, where did you find this?$B$BThis was the shovel my father had given me back when we worked the farmstead years ago. It served me well, and reminds me of him.$B$BMemories of a better time.$B$B<Sven stares at the shovel and hands it back to you.>$B$BIt was a nice gesture of you to bring me this, $N, but I have no use for it anymore.$B$BDo with it what you will.', 0),
(70058, 0, 0, 0, 0, 0, 0, 0, 0, 'You\'d be a great asset to the Night Watch but I am more than certain you wouldn\'t bore yourself with guard duty. Here\'s a little reward for a job well done.', 0),
(80397, 0, 0, 0, 0, 0, 0, 0, 0, 'Thank you, $N! With the Venture Company\'s activities unchecked, this surely isn\'t the end of those sap beasts, but for now the forest is quiet and already healing. Here, take a few of my potions in thanks for your hard work. They should help you travel swiftly in this mountainous terrain.', 0),
(80398, 0, 0, 0, 0, 0, 0, 0, 0, 'Is that an actual intact Pounder Mainframe?! Where did you get this?$B$BThe possibilities with this are endless! Tell you what, if you allow me to copy the data from this mainframe then I will help you build a Pounder of your own!', 0);

INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`, `VerifiedBuild`) VALUES
(41758, 0, 0, 'The lair of Razorfen Kraul is a twisted mess of bramble and thorn. I advise you prepare for the journey to such a place.', 0),
(41905, 0, 0, 'The Bronzebeard\'s hatred towards the Dark Iron is something I couldn\'t understand beforehand. Yet witnessing their disregard for morality and life firsthand made me realize where that disdain stems from.', 0),
(41906, 0, 0, 'This fate was not what we promised them.', 0),
(60108, 0, 0, 'Did you do it? This can\'t wait no longer.', 0),
(60109, 0, 0, 'There is untold darkness that will forever linger inside of these walls.', 0),
(60116, 66, 0, 'Well?', 0),
(70053, 0, 0, 'Are you done already, $N?', 0),
(70054, 0, 0, 'A good deed during dark times, that\'s what you\'re about to do.', 0),
(70055, 0, 0, 'My trust rests with you, $N. Please, do not fail me.', 0),
(70056, 0, 0, 'Yes, $C?', 0),
(70057, 0, 0, 'What is it?', 0),
(70058, 0, 0, 'Back so soon?', 0),
(80397, 0, 0, 'Have you rid the mountaintop of those sap beasts? Rest here for a moment and recover your strength.', 0),
(80398, 0, 0, 'Hello there, $R, are you here for one of my inventions?', 0);

INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(3036, 41758),
(1155, 41905),
(1156, 41906),
(5694, 60108),
(5694, 60109),
(1652, 60116),
(1683, 70053),
(499, 70054),
(499, 70055),
(499, 70056),
(499, 70057),
(264, 70058),
(16458, 80397);

INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(3036, 41758),
(1155, 41905),
(1156, 41906),
(5694, 60108),
(3850, 60109),
(1652, 60116),
(1683, 70053),
(499, 70054),
(499, 70055),
(264, 70056),
(311, 70057),
(264, 70058),
(16458, 80397),
(7406, 80398);

-- Turtle: Ghostly Guidance (60117) leads to Paint the Roses Red (60116); the converter dropped the link because 60116 was missing
UPDATE `quest_template_addon` SET `NextQuestID` = 60116 WHERE `ID` = 60117 AND `NextQuestID` = 0;
UPDATE `creature_template` SET `npcflag` = `npcflag` | 2 WHERE `entry` IN (499,1683,3850);

-- items
INSERT INTO `item_template` (`entry`, `class`, `subclass`, `SoundOverrideSubclass`, `name`, `displayid`, `Quality`, `Flags`, `FlagsExtra`, `BuyCount`, `BuyPrice`, `SellPrice`, `InventoryType`, `AllowableClass`, `AllowableRace`, `ItemLevel`, `RequiredLevel`, `RequiredSkill`, `RequiredSkillRank`, `requiredspell`, `requiredhonorrank`, `RequiredCityRank`, `RequiredReputationFaction`, `RequiredReputationRank`, `maxcount`, `stackable`, `ContainerSlots`, `stat_type1`, `stat_value1`, `stat_type2`, `stat_value2`, `stat_type3`, `stat_value3`, `stat_type4`, `stat_value4`, `stat_type5`, `stat_value5`, `stat_type6`, `stat_value6`, `stat_type7`, `stat_value7`, `stat_type8`, `stat_value8`, `stat_type9`, `stat_value9`, `stat_type10`, `stat_value10`, `ScalingStatDistribution`, `ScalingStatValue`, `dmg_min1`, `dmg_max1`, `dmg_type1`, `dmg_min2`, `dmg_max2`, `dmg_type2`, `armor`, `holy_res`, `fire_res`, `nature_res`, `frost_res`, `shadow_res`, `arcane_res`, `delay`, `ammo_type`, `RangedModRange`, `spellid_1`, `spelltrigger_1`, `spellcharges_1`, `spellppmRate_1`, `spellcooldown_1`, `spellcategory_1`, `spellcategorycooldown_1`, `spellid_2`, `spelltrigger_2`, `spellcharges_2`, `spellppmRate_2`, `spellcooldown_2`, `spellcategory_2`, `spellcategorycooldown_2`, `spellid_3`, `spelltrigger_3`, `spellcharges_3`, `spellppmRate_3`, `spellcooldown_3`, `spellcategory_3`, `spellcategorycooldown_3`, `spellid_4`, `spelltrigger_4`, `spellcharges_4`, `spellppmRate_4`, `spellcooldown_4`, `spellcategory_4`, `spellcategorycooldown_4`, `spellid_5`, `spelltrigger_5`, `spellcharges_5`, `spellppmRate_5`, `spellcooldown_5`, `spellcategory_5`, `spellcategorycooldown_5`, `bonding`, `description`, `PageText`, `LanguageID`, `PageMaterial`, `startquest`, `lockid`, `Material`, `sheath`, `RandomProperty`, `RandomSuffix`, `block`, `itemset`, `MaxDurability`, `area`, `Map`, `BagFamily`, `TotemCategory`, `socketColor_1`, `socketContent_1`, `socketColor_2`, `socketContent_2`, `socketColor_3`, `socketContent_3`, `socketBonus`, `GemProperties`, `RequiredDisenchantSkill`, `ArmorDamageModifier`, `duration`, `ItemLimitCategory`, `HolidayId`, `ScriptName`, `DisenchantID`, `FoodType`, `minMoneyLoot`, `maxMoneyLoot`, `flagsCustom`, `VerifiedBuild`) VALUES
(1041853, 12, 0, -1, 'Tainted Brambleheart', 3320, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(1042072, 12, 0, -1, 'Refugee Supplies', 11448, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(1050800, 4, 2, -1, 'Bramblethorn Girdle', 12441, 3, 0, 0, 1, 10800, 2064, 6, -1, -1, 34, 29, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 7, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 9411, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(1051805, 4, 0, -1, 'Signet of Arugal', 28733, 3, 0, 0, 1, 7944, 1986, 11, -1, -1, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 3, 5, 3, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 42, 0, 0, 0, 0, 0),
(1051832, 2, 0, -1, 'Nathrezim Wedge', 28679, 3, 0, 0, 1, 12050, 3013, 21, -1, -1, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48.0, 66.0, 0, 3.0, 6.0, 5, 0, 0, 0, 0, 0, 0, 0, 2700, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'Darkness envelops the blade.', 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 43, 0, 0, 0, 0, 0),
(1051833, 2, 10, -1, 'Femur Staff', 20426, 3, 0, 0, 1, 12050, 3013, 17, -1, -1, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 3, 5, 4, 6, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 71.0, 107.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 3200, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'LEGendary quality.', 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 43, 0, 0, 0, 0, 0),
(1051834, 2, 5, -1, 'Scarlet Pillar', 18324, 3, 0, 0, 1, 12050, 3013, 17, -1, -1, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 78.0, 120.0, 0, 4.0, 6.0, 1, 0, 0, 0, 0, 0, 0, 0, 3800, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'A relic from the monastery.', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 43, 0, 0, 0, 0, 0),
(58089, 2, 19, -1, 'Thornlash Branch', 28159, 3, 0, 0, 1, 25925, 6481, 26, -1, -1, 34, 29, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35.0, 64.0, 3, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 1500, 0, 100.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'A gnarled, living branch that crackles with energy.', 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(58090, 4, 0, -1, 'Seed of Writhing Growth', 8232, 3, 0, 0, 1, 7682, 1920, 12, -1, -1, 34, 29, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(58091, 4, 8, -1, 'Idol of the Thorned Grove', 31150, 3, 0, 0, 1, 7822, 1955, 28, -1, -1, 34, 29, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(70034, 4, 0, -1, 'Threshadon Trophy', 1503, 2, 0, 0, 1, 1350, 1030, 12, -1, -1, 17, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 9137, 1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 1, 0, 0, 0, 0, 0),
(70035, 12, 0, -1, 'Rusty Shovel', 7495, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, 'The initials S.Y. are scribbled on the handle.', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(70036, 4, 1, -1, 'Tattered Defias Mask', 15308, 2, 0, 0, 1, 1675, 1425, 1, -1, -1, 30, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 5, 7, 3, 4, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 1, 0, 0, 0, 0, 0),
(70037, 4, 3, -1, 'Defias Enforcer Shoulderguards', 27893, 2, 0, 0, 1, 8180, 2045, 3, -1, -1, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 7, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 149, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 4, 0, 0, 0, 0, 0),
(70044, 12, 0, -1, 'Watcher Paige\'s Report', 811, 1, 0, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(70045, 2, 4, -1, 'Rusty Shovel', 7495, 2, 0, 0, 1, 18060, 4515, 21, -1, -1, 30, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30.0, 57.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 2800, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'Engraved on the handle are two letters, S.Y.', 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 23, 0, 0, 0, 0, 0),
(70046, 4, 0, -1, 'Silver Ring', 26001, 2, 0, 0, 1, 1250, 915, 11, -1, -1, 30, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 1, 6, 3, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, 'Made from pure silver.', 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 1, 0, 0, 0, 0, 0),
(70047, 2, 4, -1, 'Smoldering Brand', 12312, 2, 0, 0, 1, 11384, 2846, 13, -1, -1, 32, 0, 142, 75, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22.0, 38.0, 0, 2.0, 6.0, 2, 0, 0, 0, 0, 0, 0, 0, 1800, 0, 0.0, 7363, 1, 0, 0.0, 0, 99, 1000, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 25, 0, 0, 0, 0, 0),
(70048, 4, 1, -1, 'Surgeon\'s Gloves', 13655, 2, 64, 0, 1, 3636, 909, 10, -1, -1, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 4, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 7679, 1, 0, 0.0, 300000, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '', 4, 0, 0, 0, 0, 0),
(80216, 13, 0, -1, 'Dark Key', 16100, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 4, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0),
(81275, 12, 0, -1, 'Intact Pounder Mainframe', 20625, 2, 0, 0, 1, 0, 0, 0, -1, -1, 20, 30, 202, 125, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 1, '', 0, 0, 0, 80398, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0);

INSERT INTO `item_dbc` (`ID`, `ClassID`, `SubclassID`, `Sound_Override_Subclassid`, `Material`, `DisplayInfoID`, `InventoryType`, `SheatheType`) VALUES
(1041853, 12, 0, -1, 3, 3320, 0, 0),
(1042072, 12, 0, -1, 3, 11448, 0, 0),
(1050800, 4, 2, -1, 8, 12441, 6, 0),
(1051805, 4, 0, -1, 0, 28733, 11, 0),
(1051832, 2, 0, -1, 0, 28679, 21, 3),
(1051833, 2, 10, -1, 0, 20426, 17, 2),
(1051834, 2, 5, -1, 0, 18324, 17, 1),
(58089, 2, 19, -1, 1, 28159, 26, 0),
(58090, 4, 0, -1, 1, 8232, 12, 0),
(58091, 4, 8, -1, 1, 31150, 28, 0),
(70034, 4, 0, -1, 4, 1503, 12, 0),
(70035, 12, 0, -1, 0, 7495, 0, 0),
(70036, 4, 1, -1, 7, 15308, 1, 0),
(70037, 4, 3, -1, 1, 27893, 3, 1),
(70044, 12, 0, -1, 0, 811, 0, 1),
(70045, 2, 4, -1, 1, 7495, 21, 3),
(70046, 4, 0, -1, 4, 26001, 11, 0),
(70047, 2, 4, -1, 2, 12312, 13, 3),
(70048, 4, 1, -1, 7, 13655, 10, 0),
(80216, 13, 0, -1, 0, 16100, 0, 0),
(81275, 12, 0, -1, 0, 20625, 0, 1);

-- creatures
INSERT INTO `creature_template` (`entry`, `name`, `subname`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RegenHealth`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(62503, 'Rotthorn', NULL, 0, 32, 32, 0, 152, 0, 0.666668, 1.14286, 18.0, 1, 0, 5.365, 2000, 2000, 2, 32768, 2048, 0, 0, 4, 0, 62503, 0, 0, 'SmartAI', 0, 11.05, 5.155, 2.093, 1, 1, 0, '', 0),
(80205, 'Shadowforge Fire Priest', NULL, 0, 19, 19, 0, 16, 0, 1.0, 1.14286, 18.0, 0, 0, 1.523, 2000, 2000, 2, 32768, 2048, 0, 0, 7, 0, 80205, 23, 35, 'SmartAI', 0, 1.324, 1.075, 1.019, 1, 1, 0, '', 0),
(80207, 'Shadowforge Prowler', NULL, 0, 17, 18, 0, 16, 0, 1.0, 1.14286, 18.0, 0, 0, 1.561, 2000, 2000, 2, 32768, 2048, 0, 0, 7, 0, 80207, 20, 31, 'SmartAI', 0, 1.364, 1.256, 1.065, 1, 1, 0, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(62503, 0, 1086, 2.0, 1, 0),
(80205, 0, 6055, 1.0, 1, 0),
(80207, 0, 6053, 1.0, 1, 0),
(80207, 1, 6057, 1.0, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`) VALUES
(62503, 1, 1, 0, 0, 0, 0),
(80205, 1, 1, 0, 0, 0, 0),
(80207, 1, 1, 0, 0, 0, 0);

INSERT INTO `creature_equip_template` (`CreatureID`, `ID`, `ItemID1`, `ItemID2`, `ItemID3`, `VerifiedBuild`) VALUES
(80205, 1, 5303, 0, 0, 0),
(80207, 1, 5303, 0, 0, 0);

-- SmartAI (Turtle spell lists)
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(62503, 0, 0, 0, 0, 0, 100, 0, 0, 0, 31000, 34000, 0, 0, 11, 7102, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Rotthorn - In Combat - Cast Contagion of Rot (Turtle spell list 62503)'),
(62503, 0, 1, 0, 0, 0, 100, 0, 1000, 2000, 21000, 24000, 0, 0, 11, 8272, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Rotthorn - In Combat - Cast Mind Tremor (Turtle spell list 62503)'),
(62503, 0, 2, 0, 0, 0, 100, 0, 4000, 5000, 15000, 18000, 0, 0, 11, 25311, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Rotthorn - In Combat - Cast Corruption (Turtle spell list 62503)'),
(62503, 0, 3, 0, 0, 0, 100, 0, 6000, 7000, 15000, 18000, 0, 0, 11, 21748, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Rotthorn - In Combat - Cast Thorn Volley (Turtle spell list 62503)'),
(80205, 0, 0, 0, 0, 0, 100, 0, 8000, 12000, 22000, 29000, 0, 0, 11, 1094, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Shadowforge Fire Priest - In Combat - Cast Immolate (Turtle spell list 180298)');

-- spawns
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) VALUES
(9990401, 62503, 47, 0, 0, 1, 1, 0, 1974.23, 1830.85, 82.7131, 2.85652, 86400, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2589523'),
(9990402, 80205, 0, 0, 0, 1, 1, 1, -5895.02, -4156.89, 393.863, 0.754321, 30, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560449'),
(9990403, 80207, 0, 0, 0, 1, 1, 1, -5899.67, -4141.34, 394.02, 1.04095, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560448'),
(9990404, 80207, 0, 0, 0, 1, 1, 1, -5837.75, -4140.8, 385.966, 5.85627, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560450'),
(9990405, 80207, 0, 0, 0, 1, 1, 1, -5837.95, -4150.49, 386.359, 6.11387, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560451'),
(9990406, 80207, 0, 0, 0, 1, 1, 1, -5858.17, -4149.48, 390.453, 2.58194, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560452'),
(9990407, 80207, 0, 0, 0, 1, 1, 1, -5863.71, -4149.12, 390.49, 0.271296, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560453'),
(9990408, 80207, 0, 0, 0, 1, 1, 1, -5858.58, -4117.72, 390.527, 3.81894, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560454'),
(9990409, 80207, 0, 0, 0, 1, 1, 1, -5875.07, -4137.03, 387.592, 0.176265, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560455'),
(9990410, 80207, 0, 0, 0, 1, 1, 1, -5836.21, -4118.0, 387.997, 6.07382, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560456'),
(9990411, 80207, 0, 0, 0, 1, 1, 1, -5838.22, -4104.35, 388.137, 0.821865, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560457'),
(9990412, 80207, 0, 0, 0, 1, 1, 1, -5848.79, -4087.11, 385.683, 0.294865, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560458'),
(9990413, 80207, 0, 0, 0, 1, 1, 1, -5844.25, -4100.76, 389.734, 0.623947, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560459'),
(9990414, 80207, 0, 0, 0, 1, 1, 1, -5885.61, -4156.57, 391.991, 0.822648, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560460'),
(9990415, 80207, 0, 0, 0, 1, 1, 1, -5856.54, -4131.56, 387.394, 5.99842, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560461'),
(9990416, 80207, 0, 0, 0, 1, 1, 1, -5876.38, -4090.15, 389.003, 0.423666, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560462'),
(9990417, 80207, 0, 0, 0, 1, 1, 1, -5872.07, -4089.93, 389.264, 3.09481, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560463'),
(9990418, 80207, 0, 0, 0, 1, 1, 1, -5873.45, -4087.17, 389.108, 4.25955, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560464'),
(9990419, 80207, 0, 0, 0, 1, 1, 1, -5877.81, -4173.83, 405.132, 1.16452, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560466'),
(9990420, 80207, 0, 0, 0, 1, 1, 1, -5863.94, -4120.34, 390.42, 6.17534, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Turtle guid 2560467');

-- objects
INSERT INTO `lock_dbc` (`ID`, `Type_1`, `Type_2`, `Type_3`, `Type_4`, `Type_5`, `Type_6`, `Type_7`, `Type_8`, `Index_1`, `Index_2`, `Index_3`, `Index_4`, `Index_5`, `Index_6`, `Index_7`, `Index_8`, `Skill_1`, `Skill_2`, `Skill_3`, `Skill_4`, `Skill_5`, `Skill_6`, `Skill_7`, `Skill_8`, `Action_1`, `Action_2`, `Action_3`, `Action_4`, `Action_5`, `Action_6`, `Action_7`, `Action_8`) VALUES
(1866, 1, 0, 0, 0, 0, 0, 0, 0, 80216, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`, `Data0`, `Data1`, `Data2`, `Data3`, `Data4`, `Data5`, `Data6`, `Data7`, `Data8`, `Data9`, `Data10`, `Data11`, `Data12`, `Data13`, `Data14`, `Data15`, `Data16`, `Data17`, `Data18`, `Data19`, `Data20`, `Data21`, `Data22`, `Data23`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES
(2020263, 3, 113, 'Stolen Crate', '', '', '', 1.0, 43, 2020263, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(3000203, 10, 676, 'Shadowforge Cage', '', '', '', 1.0, 1866, 41906, 0, 25000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2000115, 5, 7867, 'World Azeroth Karazahn PassiveDoodads Tables KarazahnTableBig.mdx', '', '', '', 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2001978, 5, 7838, 'World AZEROTH KARAZAHN PASSIVEDOODADS Tables KarazahnTableSmall.mdx', '', '', '', 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2010406, 5, 9209, 'World GENERIC PASSIVEDOODADS DEATHSKELETONS BloodElfMaleDeathSkeleton.mdx', '', '', '', 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0);

INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`, `mingold`, `maxgold`, `artkit0`, `artkit1`, `artkit2`, `artkit3`) VALUES
(2020263, 0, 4, 0, 0, 0, 0, 0, 0),
(3000203, 0, 32, 0, 0, 0, 0, 0, 0),
(2000115, 0, 0, 0, 0, 0, 0, 0, 0),
(2001978, 0, 0, 0, 0, 0, 0, 0, 0),
(2010406, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `gameobject` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `position_x`, `position_y`, `position_z`, `orientation`, `rotation0`, `rotation1`, `rotation2`, `rotation3`, `spawntimesecs`, `animprogress`, `state`, `ScriptName`, `VerifiedBuild`, `Comment`) VALUES
(9990401, 88498, 0, 0, 0, 1, 1, -5899.61, -4157.4, 393.955, 0.908526, 0.0, 0.0, 0.4388, 0.898585, 25, 100, 1, '', 0, 'Turtle guid 4004526'),
(9990402, 148841, 0, 0, 0, 1, 1, -5871.34, -4136.21, 387.148, 4.86819, 0.0, 0.0, 0.649934, -0.75999, 25, 100, 1, '', 0, 'Turtle guid 4004537'),
(9990403, 175739, 0, 0, 0, 1, 1, -5876.45, -4134.96, 388.221, 5.91639, 0.0, 0.0, 0.182373, -0.983229, 25, 100, 1, '', 0, 'Turtle guid 4007913'),
(9990404, 2000115, 0, 0, 0, 1, 1, -5893.71, -4158.84, 393.258, 0.362019, 0.0, 0.0, 0.180023, 0.983662, 25, 100, 1, '', 0, 'Turtle guid 4004479'),
(9990405, 2001881, 0, 0, 0, 1, 1, -5894.12, -4159.63, 394.62, 1.09832, 0.0, 0.0, 0.521972, 0.852962, 25, 100, 1, '', 0, 'Turtle guid 4004552'),
(9990406, 2001881, 0, 0, 0, 1, 1, -5896.59, -4148.8, 394.395, 5.2036, 0.0, 0.0, 0.513957, -0.857816, 25, 100, 1, '', 0, 'Turtle guid 4004553'),
(9990407, 2001882, 0, 0, 0, 1, 1, -5858.6, -4147.3, 391.193, 3.41525, 0.0, 0.0, 0.990654, -0.136402, 25, 100, 1, '', 0, 'Turtle guid 4004550'),
(9990408, 2001882, 0, 0, 0, 1, 1, -5866.56, -4138.44, 388.605, 1.97012, 0.0, 0.0, 0.833304, 0.552815, 25, 100, 1, '', 0, 'Turtle guid 4004551'),
(9990409, 2001978, 0, 0, 0, 1, 1, -5860.52, -4120.5, 390.202, 3.38602, 0.0, 0.0, 0.992541, -0.12191, 25, 100, 1, '', 0, 'Turtle guid 4004554'),
(9990410, 2002392, 0, 0, 0, 1, 1, -5897.95, -4160.48, 393.392, 1.15447, 0.0, 0.0, 0.545708, 0.837975, 25, 100, 1, '', 0, 'Turtle guid 4004562'),
(9990411, 2002787, 0, 0, 0, 1, 1, -5896.4, -4149.46, 394.056, 0.385156, 0.0, 0.0, 0.19139, 0.981514, 25, 100, 1, '', 0, 'Turtle guid 4004475'),
(9990412, 2002787, 0, 0, 0, 1, 1, -5901.41, -4140.9, 393.13, 0.611162, 0.0, 0.0, 0.300847, 0.953672, 25, 100, 1, '', 0, 'Turtle guid 4004477'),
(9990413, 2002787, 0, 0, 0, 1, 1, -5861.21, -4118.83, 389.569, 4.98051, 0.0, 0.0, 0.60625, -0.795274, 25, 100, 1, '', 0, 'Turtle guid 4004478'),
(9990414, 2002787, 0, 0, 0, 1, 1, -5860.24, -4148.43, 390.564, 2.3084, 0.0, 0.0, 0.914471, 0.404651, 25, 100, 1, '', 0, 'Turtle guid 4004641'),
(9990415, 2003226, 0, 0, 0, 1, 1, -5861.56, -4150.07, 390.45, 1.94965, 0.0, 0.0, 0.827605, 0.561311, 25, 100, 1, '', 0, 'Turtle guid 4004544'),
(9990416, 2003227, 0, 0, 0, 1, 1, -5858.8, -4147.33, 390.55, 2.17654, 0.0, 0.0, 0.707546, -0.706667, 25, 100, 1, '', 0, 'Turtle guid 4004541'),
(9990417, 2003227, 0, 0, 0, 1, 1, -5859.48, -4146.6, 390.57, 2.15909, 0.0, 0.0, 0.881744, 0.471728, 25, 100, 1, '', 0, 'Turtle guid 4004543'),
(9990418, 2003227, 0, 0, 0, 1, 1, -5861.56, -4150.07, 391.247, 1.9322, 0.0, 0.0, 0.822675, 0.568511, 25, 100, 1, '', 0, 'Turtle guid 4004545'),
(9990419, 2003228, 0, 0, 0, 1, 1, -5866.58, -4138.46, 387.918, 3.20787, 0.0, 0.0, 0.999451, -0.033133, 25, 100, 1, '', 0, 'Turtle guid 4004546'),
(9990420, 2003228, 0, 0, 0, 1, 1, -5861.67, -4148.51, 390.568, 4.84411, 0.0, 0.0, 0.659036, -0.752111, 25, 100, 1, '', 0, 'Turtle guid 4004547'),
(9990421, 2003229, 0, 0, 0, 1, 1, -5859.75, -4150.58, 390.334, 2.14739, 0.0, 0.0, 0.878969, 0.476878, 25, 100, 1, '', 0, 'Turtle guid 4004640'),
(9990422, 2003304, 0, 0, 0, 1, 1, -5892.48, -4159.1, 394.621, 1.79692, 0.0, 0.0, 0.782367, 0.622818, 25, 100, 1, '', 0, 'Turtle guid 4004503'),
(9990423, 2003390, 0, 0, 0, 1, 1, -5893.75, -4158.55, 394.62, 1.91912, 0.0, 0.0, 0.81894, 0.57388, 25, 100, 1, '', 0, 'Turtle guid 4004492'),
(9990424, 2003390, 0, 0, 0, 1, 1, -5894.26, -4158.83, 394.62, 5.06508, 0.0, 0.0, 0.572091, -0.82019, 25, 100, 1, '', 0, 'Turtle guid 4004498'),
(9990425, 2003390, 0, 0, 0, 1, 1, -5866.72, -4137.49, 387.917, 3.17296, 0.0, 0.0, 0.999877, -0.015683, 25, 100, 1, '', 0, 'Turtle guid 4004548'),
(9990426, 2003390, 0, 0, 0, 1, 1, -5859.39, -4146.48, 391.219, 3.18221, 0.0, 0.0, 0.999794, -0.020309, 25, 100, 1, '', 0, 'Turtle guid 4004549'),
(9990427, 2003460, 0, 0, 0, 1, 1, -5859.82, -4120.4, 391.564, 1.44489, 0.0, 0.0, 0.66122, 0.750192, 25, 100, 1, '', 0, 'Turtle guid 4004555'),
(9990428, 2004247, 0, 0, 0, 1, 1, -5837.18, -4137.34, 386.149, 2.54331, 0.0, 0.0, 0.95559, 0.2947, 25, 100, 1, '', 0, 'Turtle guid 4004524'),
(9990429, 2004247, 0, 0, 0, 1, 1, -5839.06, -4140.02, 386.112, 5.90717, 0.0, 0.0, 0.186902, -0.982379, 25, 100, 1, '', 0, 'Turtle guid 4004525'),
(9990430, 2004247, 0, 0, 0, 1, 1, -5839.86, -4149.68, 386.499, 0.341838, 0.0, 0.0, 0.170088, 0.985429, 25, 100, 1, '', 0, 'Turtle guid 4004527'),
(9990431, 2004247, 0, 0, 0, 1, 1, -5840.55, -4146.27, 386.633, 3.09702, 0.0, 0.0, 0.999752, 0.022287, 25, 100, 1, '', 0, 'Turtle guid 4004528'),
(9990432, 2004247, 0, 0, 0, 1, 1, -5836.59, -4117.39, 388.115, 3.13942, 0.0, 0.0, 0.999999, 0.001085, 25, 100, 1, '', 0, 'Turtle guid 4004529'),
(9990433, 2004247, 0, 0, 0, 1, 1, -5847.9, -4090.69, 386.5, 3.64522, 0.0, 0.0, 0.968462, -0.24916, 25, 100, 1, '', 0, 'Turtle guid 4004530'),
(9990434, 2004247, 0, 0, 0, 1, 1, -5850.17, -4087.19, 385.865, 3.64522, 0.0, 0.0, 0.968462, -0.24916, 25, 100, 1, '', 0, 'Turtle guid 4004531'),
(9990435, 2004247, 0, 0, 0, 1, 1, -5836.19, -4122.01, 387.791, 3.23996, 0.0, 0.0, 0.998791, -0.049164, 25, 100, 1, '', 0, 'Turtle guid 4004534'),
(9990436, 2004247, 0, 0, 0, 1, 1, -5889.7, -4160.46, 393.564, 0.745701, 0.0, 0.0, 0.364271, 0.931293, 25, 100, 1, '', 0, 'Turtle guid 4004535'),
(9990437, 2004247, 0, 0, 0, 1, 1, -5905.41, -4133.6, 393.412, 0.545159, 0.0, 0.0, 0.269217, 0.96308, 25, 100, 1, '', 0, 'Turtle guid 4004536'),
(9990438, 2004247, 0, 0, 0, 1, 1, -5855.19, -4118.62, 390.468, 3.58724, 0.0, 0.0, 0.975277, -0.220986, 25, 100, 1, '', 0, 'Turtle guid 4004597'),
(9990439, 2004247, 0, 0, 0, 1, 1, -5861.48, -4154.32, 390.058, 2.56623, 0.0, 0.0, 0.958904, 0.283731, 25, 100, 1, '', 0, 'Turtle guid 4004598'),
(9990440, 2004247, 0, 0, 0, 1, 1, -5885.22, -4129.22, 388.812, 3.76868, 0.0, 0.0, 0.951247, -0.308429, 25, 100, 1, '', 0, 'Turtle guid 4004599'),
(9990441, 2004607, 0, 0, 0, 1, 1, -5874.13, -4133.16, 387.715, 5.41003, 0.0, 0.0, 0.422842, -0.906203, 25, 100, 1, '', 0, 'Turtle guid 4004538'),
(9990442, 2004607, 0, 0, 0, 1, 1, -5867.09, -4135.48, 387.411, 3.24722, 0.0, 0.0, 0.998606, -0.05279, 25, 100, 1, '', 0, 'Turtle guid 4004539'),
(9990443, 2004607, 0, 0, 0, 1, 1, -5872.65, -4140.52, 387.54, 1.20519, 0.0, 0.0, 0.566781, 0.823868, 25, 100, 1, '', 0, 'Turtle guid 4004540'),
(9990444, 2004894, 0, 0, 0, 1, 1, -5895.84, -4147.32, 394.54, 5.30939, 0.0, 0.0, 0.467888, -0.883788, 25, 100, 1, '', 0, 'Turtle guid 4004509'),
(9990445, 2004894, 0, 0, 0, 1, 1, -5895.27, -4148.18, 394.426, 5.30066, 0.0, 0.0, 0.471739, -0.881738, 25, 100, 1, '', 0, 'Turtle guid 4004515'),
(9990446, 2004894, 0, 0, 0, 1, 1, -5898.83, -4149.11, 394.262, 5.30066, 0.0, 0.0, 0.471739, -0.881738, 25, 100, 1, '', 0, 'Turtle guid 4004516'),
(9990447, 2004894, 0, 0, 0, 1, 1, -5898.28, -4149.94, 394.228, 5.30066, 0.0, 0.0, 0.471739, -0.881738, 25, 100, 1, '', 0, 'Turtle guid 4004519'),
(9990448, 2004894, 0, 0, 0, 1, 1, -5895.3, -4151.02, 394.249, 2.19192, 0.0, 0.0, 0.889368, 0.457192, 25, 100, 1, '', 0, 'Turtle guid 4004520'),
(9990449, 2004894, 0, 0, 0, 1, 1, -5894.74, -4151.89, 394.16, 2.14829, 0.0, 0.0, 0.879183, 0.476485, 25, 100, 1, '', 0, 'Turtle guid 4004521'),
(9990450, 2004916, 0, 0, 0, 1, 1, -5878.95, -4116.44, 387.758, 0.232011, 0.0, 0.0, 0.994072, -0.108725, 25, 100, 1, '', 0, 'Turtle guid 4004542'),
(9990451, 2010406, 0, 0, 0, 1, 1, -5878.58, -4115.82, 387.889, 1.31997, 0.0, 0.0, 0.613105, 0.790001, 25, 100, 1, '', 0, 'Turtle guid 4004595'),
(9990452, 2010442, 0, 0, 0, 1, 1, -5895.48, -4148.36, 394.432, 0.160132, 0.0, 0.0, 0.079981, 0.996796, 25, 100, 1, '', 0, 'Turtle guid 4004532'),
(9990453, 3000203, 0, 0, 0, 1, 1, -5887.87, -4132.6, 388.408, 5.15365, 0.0, 0.0, 0.63116, -0.775652, 0, 100, 1, '', 0, 'Turtle guid 4004593'),
(9990454, 2020263, 0, 0, 0, 1, 1, -5848.75, -4148.790039, 388.549011, 3.98463, 0, 0, 0.912469, -0.409147, 300, 100, 1, '', 0, 'Turtle guid 5027068 (2026-10-08)'),
(9990455, 2020263, 0, 0, 0, 1, 1, -5857.0, -4112.629883, 389.834991, 2.94791, 0, 0, 0.995315, 0.09669, 300, 100, 1, '', 0, 'Turtle guid 5027069 (2026-10-08)'),
(9990456, 2020263, 0, 0, 0, 1, 1, -5878.830078, -4113.819824, 388.22699, 3.4537, 0, 0, 0.987848, -0.155421, 300, 100, 1, '', 0, 'Turtle guid 5027070 (2026-10-08)'),
(9990457, 2020263, 0, 0, 0, 1, 1, -5887.830078, -4129.939941, 389.020996, 3.3304, 0, 0, 0.995547, -0.094264, 300, 100, 1, '', 0, 'Turtle guid 5027071 (2026-10-08)'),
(9990458, 2020263, 0, 0, 0, 1, 1, -5903.069824, -4137.509766, 393.644989, 4.86977, 0, 0, 0.649333, -0.760504, 300, 100, 1, '', 0, 'Turtle guid 5027072 (2026-10-08)'),
(9990459, 2020263, 0, 0, 0, 1, 1, -5897.589844, -4157.120117, 393.938995, 4.79124, 0, 0, 0.678686, -0.734428, 300, 100, 1, '', 0, 'Turtle guid 5027073 (2026-10-08)'),
(9990460, 2020263, 0, 0, 0, 1, 1, -5890.759766, -4157.259766, 393.412994, 5.16194, 0, 0, 0.531714, -0.846924, 300, 100, 1, '', 0, 'Turtle guid 5027074 (2026-10-08)'),
(9990461, 2020263, 0, 0, 0, 1, 1, -5872.439941, -4150.319824, 389.377991, 0.02858, 0, 0, 0.01429, 0.999898, 300, 100, 1, '', 0, 'Turtle guid 5027075 (2026-10-08)'),
(9990462, 2020263, 0, 0, 0, 1, 1, -5874.569824, -4142.040039, 387.608002, 6.01332, 0, 0, 0.134524, -0.99091, 300, 100, 1, '', 0, 'Turtle guid 5027076 (2026-10-08)'),
(9990463, 2020263, 0, 0, 0, 1, 1, -5873.939941, -4091.469971, 389.270996, 1.42738, 0, 0, 0.654628, 0.755951, 300, 100, 1, '', 0, 'Turtle guid 5027077 (2026-10-08)'),
(9990464, 2020263, 0, 0, 0, 1, 1, -5852.850098, -4088.48999, 386.744995, 5.68659, 0, 0, 0.293893, -0.955838, 300, 100, 1, '', 0, 'Turtle guid 5027078 (2026-10-08)');

-- loot
INSERT INTO `reference_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(9990227, 2981, 0, 0.008333, 0, 1, 1, 1, 1, 'Seer\'s Robe'),
(9990227, 2982, 0, 0.008333, 0, 1, 1, 1, 1, 'Seer\'s Pants'),
(9990227, 2985, 0, 0.008333, 0, 1, 1, 1, 1, 'Inscribed Leather Breastplate'),
(9990227, 2986, 0, 0.008333, 0, 1, 1, 1, 1, 'Inscribed Leather Pants'),
(9990227, 2989, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Tunic'),
(9990227, 2990, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Leggings'),
(9990227, 2991, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Boots'),
(9990227, 2992, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Gloves'),
(9990227, 3184, 0, 0.008333, 0, 1, 1, 1, 1, 'Hook Dagger'),
(9990227, 3193, 0, 0.008333, 0, 1, 1, 1, 1, 'Oak Mallet'),
(9990227, 3655, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Shield'),
(9990227, 4568, 0, 0.008333, 0, 1, 1, 1, 1, 'Grunt Axe'),
(9990227, 4576, 0, 0.008333, 0, 1, 1, 1, 1, 'Light Bow'),
(9990227, 4697, 0, 0.008333, 0, 1, 1, 1, 1, 'Burnished Girdle'),
(9990227, 5207, 0, 0.008333, 0, 1, 1, 1, 1, 'Opaque Wand'),
(9990227, 6561, 0, 0.008333, 0, 1, 1, 1, 1, 'Seer\'s Padded Armor'),
(9990227, 6562, 0, 0.008333, 0, 1, 1, 1, 1, 'Shimmering Boots'),
(9990227, 6563, 0, 0.008333, 0, 1, 1, 1, 1, 'Shimmering Bracers'),
(9990227, 6564, 0, 0.008333, 0, 1, 1, 1, 1, 'Shimmering Cloak'),
(9990227, 6575, 0, 0.008333, 0, 1, 1, 1, 1, 'Defender Cloak'),
(9990227, 6581, 0, 0.008333, 0, 1, 1, 1, 1, 'Scouting Belt'),
(9990227, 6583, 0, 0.008333, 0, 1, 1, 1, 1, 'Scouting Bracers'),
(9990227, 6585, 0, 0.008333, 0, 1, 1, 1, 1, 'Scouting Cloak'),
(9990227, 7608, 0, 0.008333, 0, 1, 1, 1, 1, 'Seer\'s Fine Stein'),
(9990227, 9768, 0, 0.008333, 0, 1, 1, 1, 1, 'Greenweave Bracers'),
(9990227, 9770, 0, 0.008333, 0, 1, 1, 1, 1, 'Greenweave Cloak'),
(9990227, 9776, 0, 0.008333, 0, 1, 1, 1, 1, 'Bandit Boots'),
(9990227, 9778, 0, 0.008333, 0, 1, 1, 1, 1, 'Bandit Buckler'),
(9990227, 9780, 0, 0.008333, 0, 1, 1, 1, 1, 'Bandit Gloves'),
(9990227, 9783, 0, 0.008333, 0, 1, 1, 1, 1, 'Raider\'s Chestpiece'),
(9990227, 11965, 0, 0.008333, 0, 1, 1, 1, 1, 'Quartz Ring'),
(9990227, 11981, 0, 0.008333, 0, 1, 1, 1, 1, 'Lead Band'),
(9990227, 12052, 0, 0.008333, 0, 1, 1, 1, 1, 'Ring of the Moon'),
(9990227, 12053, 0, 0.008333, 0, 1, 1, 1, 1, 'Volcanic Rock Ring'),
(9990227, 14120, 0, 0.008333, 0, 1, 1, 1, 1, 'Aboriginal Robe'),
(9990227, 14121, 0, 0.008333, 0, 1, 1, 1, 1, 'Aboriginal Vest'),
(9990227, 14124, 0, 0.008333, 0, 1, 1, 1, 1, 'Ritual Gloves'),
(9990227, 14125, 0, 0.008333, 0, 1, 1, 1, 1, 'Ritual Leggings'),
(9990227, 14129, 0, 0.008333, 0, 1, 1, 1, 1, 'Ritual Sandals'),
(9990227, 14164, 0, 0.008333, 0, 1, 1, 1, 1, 'Pagan Belt'),
(9990227, 14168, 0, 0.008333, 0, 1, 1, 1, 1, 'Buccaneer\'s Gloves'),
(9990227, 14173, 0, 0.008333, 0, 1, 1, 1, 1, 'Buccaneer\'s Cord'),
(9990227, 14565, 0, 0.008333, 0, 1, 1, 1, 1, 'Prospector\'s Woolies'),
(9990227, 14571, 0, 0.008333, 0, 1, 1, 1, 1, 'Bristlebark Cape'),
(9990227, 14729, 0, 0.008333, 0, 1, 1, 1, 1, 'War Paint Shield'),
(9990227, 14745, 0, 0.008333, 0, 1, 1, 1, 1, 'Hulking Cloak'),
(9990227, 15018, 0, 0.008333, 0, 1, 1, 1, 1, 'Lupine Vest'),
(9990227, 15110, 0, 0.008333, 0, 1, 1, 1, 1, 'Rigid Belt'),
(9990227, 15111, 0, 0.008333, 0, 1, 1, 1, 1, 'Rigid Moccasins'),
(9990227, 15112, 0, 0.008333, 0, 1, 1, 1, 1, 'Rigid Bracelets'),
(9990227, 15248, 0, 0.008333, 0, 1, 1, 1, 1, 'Gleaming Claymore'),
(9990227, 15312, 0, 0.008333, 0, 1, 1, 1, 1, 'Feral Leggings'),
(9990227, 15488, 0, 0.008333, 0, 1, 1, 1, 1, 'Bloodspattered Surcoat'),
(9990227, 15498, 0, 0.008333, 0, 1, 1, 1, 1, 'Outrunner\'s Slippers'),
(9990227, 15502, 0, 0.008333, 0, 1, 1, 1, 1, 'Outrunner\'s Gloves'),
(9990227, 15506, 0, 0.008333, 0, 1, 1, 1, 1, 'Grunt\'s Anklewraps'),
(9990227, 15509, 0, 0.008333, 0, 1, 1, 1, 1, 'Grunt\'s Handwraps'),
(9990227, 15510, 0, 0.008333, 0, 1, 1, 1, 1, 'Grunt\'s Belt'),
(9990227, 15893, 0, 0.008333, 0, 1, 1, 1, 1, 'Prospector\'s Buckler'),
(9990227, 15971, 0, 0.008333, 0, 1, 1, 1, 1, 'Aboriginal Rod'),
(9990235, 2078, 0, 0.008475, 0, 1, 2, 1, 1, 'Northern Shortsword'),
(9990235, 2984, 0, 0.008475, 0, 1, 2, 1, 1, 'Seer\'s Gloves'),
(9990235, 2987, 0, 0.008475, 0, 1, 2, 1, 1, 'Inscribed Leather Boots'),
(9990235, 2988, 0, 0.008475, 0, 1, 2, 1, 1, 'Inscribed Leather Gloves'),
(9990235, 3040, 0, 0.008475, 0, 1, 2, 1, 1, 'Hunter\'s Muzzle Loader'),
(9990235, 3195, 0, 0.008475, 0, 1, 2, 1, 1, 'Barbaric Battle Axe'),
(9990235, 3196, 0, 0.008475, 0, 1, 2, 1, 1, 'Edged Bastard Sword'),
(9990235, 3211, 0, 0.008475, 0, 1, 2, 1, 1, 'Burnished Bracers'),
(9990235, 3306, 0, 0.008475, 0, 1, 2, 1, 1, 'Brackwater Vest'),
(9990235, 3310, 0, 0.008475, 0, 1, 2, 1, 1, 'Barbaric Cloth Vest'),
(9990235, 3313, 0, 0.008475, 0, 1, 2, 1, 1, 'Ceremonial Leather Harness'),
(9990235, 4575, 0, 0.008475, 0, 1, 2, 1, 1, 'Medicine Staff'),
(9990235, 4695, 0, 0.008475, 0, 1, 2, 1, 1, 'Burnished Cloak'),
(9990235, 4699, 0, 0.008475, 0, 1, 2, 1, 1, 'Seer\'s Belt'),
(9990235, 6380, 0, 0.008475, 0, 1, 2, 1, 1, 'Inscribed Buckler'),
(9990235, 6531, 0, 0.008475, 0, 1, 2, 1, 1, 'Barbaric Cloth Robe'),
(9990235, 6536, 0, 0.008475, 0, 1, 2, 1, 1, 'Willow Vest'),
(9990235, 6538, 0, 0.008475, 0, 1, 2, 1, 1, 'Willow Robe'),
(9990235, 6540, 0, 0.008475, 0, 1, 2, 1, 1, 'Willow Pants'),
(9990235, 6545, 0, 0.008475, 0, 1, 2, 1, 1, 'Soldier\'s Armor'),
(9990235, 6552, 0, 0.008475, 0, 1, 2, 1, 1, 'Bard\'s Tunic'),
(9990235, 6553, 0, 0.008475, 0, 1, 2, 1, 1, 'Bard\'s Trousers'),
(9990235, 7554, 0, 0.008475, 0, 1, 2, 1, 1, 'Willow Branch'),
(9990235, 9775, 0, 0.008475, 0, 1, 2, 1, 1, 'Bandit Cinch'),
(9990235, 9777, 0, 0.008475, 0, 1, 2, 1, 1, 'Bandit Bracers'),
(9990235, 9779, 0, 0.008475, 0, 1, 2, 1, 1, 'Bandit Cloak'),
(9990235, 9784, 0, 0.008475, 0, 1, 2, 1, 1, 'Raider\'s Boots'),
(9990235, 9787, 0, 0.008475, 0, 1, 2, 1, 1, 'Raider\'s Gauntlets'),
(9990235, 9788, 0, 0.008475, 0, 1, 2, 1, 1, 'Raider\'s Belt'),
(9990235, 9789, 0, 0.008475, 0, 1, 2, 1, 1, 'Raider\'s Legguards'),
(9990235, 9790, 0, 0.008475, 0, 1, 2, 1, 1, 'Raider\'s Shield'),
(9990235, 14122, 0, 0.008475, 0, 1, 2, 1, 1, 'Ritual Bands'),
(9990235, 14131, 0, 0.008475, 0, 1, 2, 1, 1, 'Ritual Belt'),
(9990235, 14160, 0, 0.008475, 0, 1, 2, 1, 1, 'Pagan Bands'),
(9990235, 14161, 0, 0.008475, 0, 1, 2, 1, 1, 'Pagan Cape'),
(9990235, 14166, 0, 0.008475, 0, 1, 2, 1, 1, 'Buccaneer\'s Bracers'),
(9990235, 14167, 0, 0.008475, 0, 1, 2, 1, 1, 'Buccaneer\'s Cape'),
(9990235, 14174, 0, 0.008475, 0, 1, 2, 1, 1, 'Buccaneer\'s Boots'),
(9990235, 14364, 0, 0.008475, 0, 1, 2, 1, 1, 'Mystic\'s Slippers'),
(9990235, 14367, 0, 0.008475, 0, 1, 2, 1, 1, 'Mystic\'s Gloves'),
(9990235, 14370, 0, 0.008475, 0, 1, 2, 1, 1, 'Mystic\'s Woolies'),
(9990235, 14559, 0, 0.008475, 0, 1, 2, 1, 1, 'Prospector\'s Sash'),
(9990235, 14560, 0, 0.008475, 0, 1, 2, 1, 1, 'Prospector\'s Boots'),
(9990235, 14564, 0, 0.008475, 0, 1, 2, 1, 1, 'Prospector\'s Mitts'),
(9990235, 14726, 0, 0.008475, 0, 1, 2, 1, 1, 'War Paint Gloves'),
(9990235, 14727, 0, 0.008475, 0, 1, 2, 1, 1, 'War Paint Legguards'),
(9990235, 15017, 0, 0.008475, 0, 1, 2, 1, 1, 'Lupine Leggings'),
(9990235, 15114, 0, 0.008475, 0, 1, 2, 1, 1, 'Rigid Cape'),
(9990235, 15222, 0, 0.008475, 0, 1, 2, 1, 1, 'Barbed Club'),
(9990235, 15305, 0, 0.008475, 0, 1, 2, 1, 1, 'Feral Shoes'),
(9990235, 15307, 0, 0.008475, 0, 1, 2, 1, 1, 'Feral Buckler'),
(9990235, 15310, 0, 0.008475, 0, 1, 2, 1, 1, 'Feral Gloves'),
(9990235, 15493, 0, 0.008475, 0, 1, 2, 1, 1, 'Bloodspattered Loincloth'),
(9990235, 15494, 0, 0.008475, 0, 1, 2, 1, 1, 'Bloodspattered Shield'),
(9990235, 15497, 0, 0.008475, 0, 1, 2, 1, 1, 'Outrunner\'s Cord'),
(9990235, 15499, 0, 0.008475, 0, 1, 2, 1, 1, 'Outrunner\'s Cuffs'),
(9990235, 15507, 0, 0.008475, 0, 1, 2, 1, 1, 'Grunt\'s Bracers'),
(9990235, 15508, 0, 0.008475, 0, 1, 2, 1, 1, 'Grunt\'s Cape'),
(9990235, 15945, 0, 0.008475, 0, 1, 2, 1, 1, 'Runic Stave'),
(9991180, 2407, 0, 0.02, 0, 1, 0, 1, 1, 'Pattern: White Leather Jerkin'),
(9991180, 2409, 0, 0.02, 0, 1, 0, 1, 1, 'Pattern: Dark Leather Tunic'),
(9991180, 2452, 0, 0.02, 0, 1, 0, 1, 1, 'Swiftthistle'),
(9991180, 2657, 0, 0.02, 0, 1, 0, 1, 1, 'Red Leather Bag'),
(9991180, 4293, 0, 0.02, 0, 1, 0, 1, 1, 'Pattern: Hillman\'s Leather Vest'),
(9991180, 4408, 0, 0.02, 0, 1, 0, 1, 1, 'Schematic: Mechanical Squirrel'),
(9991180, 4409, 0, 0.02, 0, 1, 0, 1, 1, 'Schematic: Small Seaforium Charge'),
(9991180, 6347, 0, 0.02, 0, 1, 0, 1, 1, 'Formula: Enchant Bracer - Minor Strength'),
(9991180, 6716, 0, 0.02, 0, 1, 0, 1, 1, 'Schematic: EZ-Thro Dynamite');

INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(62503, 1041853, 0, 100.0, 1, 1, 0, 1, 1, 'Tainted Brambleheart'),
(62503, 1050800, 0, 25.0, 0, 1, 1, 1, 1, 'Bramblethorn Girdle'),
(62503, 58089, 0, 25.0, 0, 1, 1, 1, 1, 'Thornlash Branch'),
(62503, 58090, 0, 25.0, 0, 1, 1, 1, 1, 'Seed of Writhing Growth'),
(62503, 58091, 0, 25.0, 0, 1, 1, 1, 1, 'Idol of the Thorned Grove'),
(80205, 818, 0, 0.16, 0, 1, 0, 1, 1, 'Tigerseye'),
(80205, 856, 0, 0.75, 0, 1, 0, 1, 1, 'Blue Leather Bag'),
(80205, 858, 0, 1.0243, 0, 1, 0, 1, 1, 'Lesser Healing Potion'),
(80205, 954, 0, 0.46, 0, 1, 0, 1, 1, 'Scroll of Strength'),
(80205, 955, 0, 0.52, 0, 1, 0, 1, 1, 'Scroll of Intellect'),
(80205, 1179, 0, 1.7926, 0, 1, 0, 1, 1, 'Ice Cold Milk'),
(80205, 1180, 0, 0.58, 0, 1, 0, 1, 1, 'Scroll of Stamina'),
(80205, 1206, 0, 0.08, 0, 1, 0, 1, 1, 'Moss Agate'),
(80205, 1210, 0, 0.36, 0, 1, 0, 1, 1, 'Shadowgem'),
(80205, 2274, 0, 1.0, 0, 1, 0, 1, 1, 'Sapper\'s Gloves'),
(80205, 2450, 0, 0.06, 0, 1, 0, 1, 1, 'Briarthorn'),
(80205, 2455, 0, 0.5122, 0, 1, 0, 1, 1, 'Minor Mana Potion'),
(80205, 2589, 0, 18.822, 0, 1, 0, 1, 3, 'Linen Cloth'),
(80205, 2592, 0, 19.3342, 0, 1, 0, 1, 2, 'Wool Cloth'),
(80205, 2700, 0, 0.08, 0, 1, 0, 1, 1, 'Recipe: Succulent Pork Ribs'),
(80205, 2770, 0, 0.08, 0, 1, 0, 1, 1, 'Copper Ore'),
(80205, 2835, 0, 0.03, 0, 1, 0, 1, 1, 'Rough Stone'),
(80205, 3012, 0, 0.34, 0, 1, 0, 1, 1, 'Scroll of Agility'),
(80205, 4345, 0, 0.04, 0, 1, 0, 1, 1, 'Pattern: Red Woolen Boots'),
(80205, 4541, 0, 3.9693, 0, 1, 0, 1, 1, 'Freshly Baked Bread'),
(80205, 5574, 0, 0.04, 0, 1, 0, 1, 1, 'White Leather Bag'),
(80205, 6344, 0, 0.04, 0, 1, 0, 1, 1, 'Formula: Enchant Bracer - Minor Spirit'),
(80205, 6348, 0, 0.04, 0, 1, 0, 1, 1, 'Formula: Enchant Weapon - Minor Beastslayer'),
(80205, 6391, 0, 0.04, 0, 1, 0, 1, 1, 'Pattern: Stylish Green Shirt'),
(80205, 80216, 0, 100.0, 0, 1, 6, 1, 1, 'Dark Key'),
(80205, 81094, 0, 0.16, 0, 1, 5, 1, 1, 'Amber Topaz'),
(80205, 10000126, 10000126, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80205, 9990227, 9990227, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80205, 9990235, 9990235, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80205, 10000315, 10000315, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80205, 9991180, 9991180, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80207, 818, 0, 0.16, 0, 1, 0, 1, 1, 'Tigerseye'),
(80207, 856, 0, 0.75, 0, 1, 0, 1, 1, 'Blue Leather Bag'),
(80207, 858, 0, 1.0243, 0, 1, 0, 1, 1, 'Lesser Healing Potion'),
(80207, 954, 0, 0.46, 0, 1, 0, 1, 1, 'Scroll of Strength'),
(80207, 955, 0, 0.52, 0, 1, 0, 1, 1, 'Scroll of Intellect'),
(80207, 1179, 0, 1.7926, 0, 1, 0, 1, 1, 'Ice Cold Milk'),
(80207, 1180, 0, 0.58, 0, 1, 0, 1, 1, 'Scroll of Stamina'),
(80207, 1206, 0, 0.08, 0, 1, 0, 1, 1, 'Moss Agate'),
(80207, 1210, 0, 0.36, 0, 1, 0, 1, 1, 'Shadowgem'),
(80207, 2274, 0, 1.0, 0, 1, 0, 1, 1, 'Sapper\'s Gloves'),
(80207, 2450, 0, 0.06, 0, 1, 0, 1, 1, 'Briarthorn'),
(80207, 2455, 0, 0.5122, 0, 1, 0, 1, 1, 'Minor Mana Potion'),
(80207, 2589, 0, 18.822, 0, 1, 0, 1, 3, 'Linen Cloth'),
(80207, 2592, 0, 19.3342, 0, 1, 0, 1, 2, 'Wool Cloth'),
(80207, 2700, 0, 0.08, 0, 1, 0, 1, 1, 'Recipe: Succulent Pork Ribs'),
(80207, 2770, 0, 0.08, 0, 1, 0, 1, 1, 'Copper Ore'),
(80207, 2835, 0, 0.03, 0, 1, 0, 1, 1, 'Rough Stone'),
(80207, 3012, 0, 0.34, 0, 1, 0, 1, 1, 'Scroll of Agility'),
(80207, 4345, 0, 0.04, 0, 1, 0, 1, 1, 'Pattern: Red Woolen Boots'),
(80207, 4541, 0, 3.9693, 0, 1, 0, 1, 1, 'Freshly Baked Bread'),
(80207, 5574, 0, 0.04, 0, 1, 0, 1, 1, 'White Leather Bag'),
(80207, 6344, 0, 0.04, 0, 1, 0, 1, 1, 'Formula: Enchant Bracer - Minor Spirit'),
(80207, 6348, 0, 0.04, 0, 1, 0, 1, 1, 'Formula: Enchant Weapon - Minor Beastslayer'),
(80207, 6391, 0, 0.04, 0, 1, 0, 1, 1, 'Pattern: Stylish Green Shirt'),
(80207, 81094, 0, 0.16, 0, 1, 5, 1, 1, 'Amber Topaz'),
(80207, 10000126, 10000126, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80207, 9990227, 9990227, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80207, 9990235, 9990235, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80207, 10000315, 10000315, 100.0, 0, 1, 0, 1, 1, '(reference)'),
(80207, 9991180, 9991180, 100.0, 0, 1, 0, 1, 1, '(reference)');

-- Turtle's quest drops on 3.3.5 creatures (Grave Robber: Rusty Shovel; Crowd Pummeler 9-60: Intact Pounder Mainframe)
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(218, 70035, 0, 100, 1, 1, 0, 1, 1, 'Rusty Shovel'),
(6229, 81275, 0, 0.8, 0, 1, 0, 1, 1, 'Intact Pounder Mainframe');

INSERT INTO `gameobject_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(2020263, 1042072, 0, 100, 1, 1, 0, 1, 1, 'Refugee Supplies');

