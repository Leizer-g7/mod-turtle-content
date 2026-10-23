-- mod-turtle-content: the Scarlet Crusade chain (2026-10-12), ported from the Turtle WoW world DB and C++ (random_scripts_1.cpp).
-- Alliance: Crier Goodman -> Mathias Shaw -> Lakeshire -> the Wetlands caravan -> Thandol Span -> Menethil interrogation
--           -> Brother Crowley -> Mavel Brightwood at Tyr's Hand (80700-80711, 80730).
-- Horde:    the Seekers -> Varimathras -> Brill/Sepulcher/Tarren Mill -> Deathguard Maverick's trap -> Zinge -> Gunther
--           -> Sylvanas -> Mavel Brightwood (80720-80729).
-- Turtle's C++ scenes are SmartAI here (no compile needed). Final reward: Scarlet Crusade Insignia, the key of Turtle's
-- Scarlet Citadel raid (not ported). Left out: the Dirt Mound / Archmage Alphus Wordwill fight (Turtle never spawns the mound;
-- the locket comes from the lockbox behind Ambermill's town hall, as on Turtle).
-- Changes to 3.3.5 NPCs: Foreman Oslow, Dorin Songblade, Magistrate Solomon and Kixxle get Turtle's menus + gossip flag;
-- Executors Zygand and Hadrec get a small menu + gossip flag; Stoutfist and Darthalia get one extra option (id 50);
-- SmartAI on Oslow, Dorin, Solomon, Kixxle, Stoutfist, Crowley, Zygand, Hadrec, Varimathras (rows id >= 100, texts group >= 100).
-- Varimathras and the three Seekers are spawned in Undercity only if this world DB has no spawn of them.
SET NAMES utf8mb4;

-- cleanup (makes the file safe to apply again)
DELETE FROM `quest_template` WHERE `ID` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `quest_template_addon` WHERE `ID` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `quest_offer_reward` WHERE `ID` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `quest_request_items` WHERE `ID` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `creature_queststarter` WHERE `quest` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `creature_questender` WHERE `quest` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `gameobject_queststarter` WHERE `quest` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `gameobject_questender` WHERE `quest` IN (80700,80701,80702,80730,80703,80704,80705,80706,80707,80708,80709,80710,80711,80720,80721,80722,80723,80724,80725,80726,80727,80728,80729);
DELETE FROM `item_template` WHERE `entry` IN (53000,53001,53003,53004,53005,53010,53011,53012,53013,53014);
DELETE FROM `item_dbc` WHERE `ID` IN (53000,53001,53003,53004,53005,53010,53011,53012,53013,53014);
DELETE FROM `creature_template` WHERE `entry` IN (50665,50666,50667,50668,50669,50670,50671,50675,50684,50685,50686,50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (50665,50666,50667,50668,50669,50670,50671,50675,50684,50685,50686,50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `creature_template_movement` WHERE `CreatureId` IN (50665,50666,50667,50668,50669,50670,50671,50675,50684,50685,50686,50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `creature_equip_template` WHERE `CreatureID` IN (50665,50666,50667,50668,50669,50670,50671,50675,50684,50685,50686,50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `creature_text` WHERE `CreatureID` IN (50665,50666,50667,50668,50669,50670,50671,50675,50684,50685,50686,50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `creature_text` WHERE `CreatureID` IN (2104,12336,1515,1952,2215,2425) AND `GroupID` >= 100;
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (50673,50674,50676,50677,50680,50681,50682,51567,90974);
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (341,956,344,8305,2104,12336,1515,1952,2215,2425) AND `id` >= 100;
DELETE FROM `smart_scripts` WHERE `source_type` = 9 AND `entryorguid` IN (9097400,1233600,5156700);
DELETE FROM `creature` WHERE `guid` BETWEEN 9990001 AND 9990099;
DELETE FROM `gameobject` WHERE `guid` BETWEEN 9990001 AND 9990099;
DELETE FROM `gameobject_template` WHERE `entry` = 1000177;
DELETE FROM `gameobject_template_addon` WHERE `entry` = 1000177;
DELETE FROM `gameobject_loot_template` WHERE `Entry` = 1000177;
DELETE FROM `creature_loot_template` WHERE `Entry` IN (50673, 50680, 50681, 50682);
DELETE FROM `creature_loot_template` WHERE `Item` IN (53004, 53014);
DELETE FROM `gossip_menu` WHERE `MenuID` IN (41333,41334,41335,41336,41337,41338,41343,41344,41345,41346,51683,51684,51690,9080001,9080002,9080003,9080004,9080005,9080011,9080012,9080013,9080014,9080015,9080016,9080030,9080031);
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (41333,41335,41337,41343,41344,41345,51683,51684,51690,9080001,9080002,9080003,9080004,9080005,9080011,9080012,9080013,9080014,9080015,9080016,9080030,9080031);
DELETE FROM `gossip_menu_option` WHERE `MenuID` IN (11499, 11886) AND `OptionID` = 50;
DELETE FROM `npc_text` WHERE `ID` IN (41333,41334,41335,41336,41337,41338,41343,41344,41345,41346,51683,51684,51685,51690,51691);
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` IN (14, 15) AND `SourceGroup` IN (41333,41334,41335,41336,41337,41338,41343,41344,41345,41346,51683,51684,51690,9080001,9080002,9080003,9080004,9080005,9080011,9080012,9080013,9080014,9080015,9080016,9080030,9080031);
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 15 AND `SourceGroup` IN (11499, 11886) AND `SourceEntry` = 50;
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 22 AND `SourceEntry` IN (90974, 51567);

-- quests
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `QuestInfoID`, `SuggestedGroupNum`, `RewardNextQuest`, `RewardXPDifficulty`, `RewardMoney`, `RewardDisplaySpell`, `RewardSpell`, `StartItem`, `Flags`, `TimeAllowed`, `AllowableRaces`, `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `RewardItem1`, `RewardAmount1`, `ItemDrop1`, `ItemDropQuantity1`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`, `RequiredItemId1`, `RequiredItemCount1`, `ObjectiveText1`, `RewardItem2`, `RewardAmount2`, `ItemDrop2`, `ItemDropQuantity2`, `RequiredNpcOrGo2`, `RequiredNpcOrGoCount2`, `RequiredItemId2`, `RequiredItemCount2`, `ObjectiveText2`, `RewardItem3`, `RewardAmount3`, `ItemDrop3`, `ItemDropQuantity3`, `RequiredNpcOrGo3`, `RequiredNpcOrGoCount3`, `RequiredItemId3`, `RequiredItemCount3`, `ObjectiveText3`, `RewardItem4`, `RewardAmount4`, `ItemDrop4`, `ItemDropQuantity4`, `RequiredNpcOrGo4`, `RequiredNpcOrGoCount4`, `RequiredItemId4`, `RequiredItemCount4`, `ObjectiveText4`, `RewardChoiceItemID1`, `RewardChoiceItemQuantity1`, `RewardChoiceItemID2`, `RewardChoiceItemQuantity2`, `RewardChoiceItemID3`, `RewardChoiceItemQuantity3`, `RewardChoiceItemID4`, `RewardChoiceItemQuantity4`, `RewardChoiceItemID5`, `RewardChoiceItemQuantity5`, `RewardChoiceItemID6`, `RewardChoiceItemQuantity6`) VALUES
(80700, 2, 60, 58, 1519, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1101, 'A Particular Letter', 'Accept suspicious letter to ease Goodman\'s mind.', 'I\'ve been looking for you all around the city! Although I am more of an announcer than a mailman I was instructed to give this letter to you by well… I am not sure who he was.$B$BThe figure\'s face was covered and his voice didn\'t seem familiar at all. He said you will understand when you read it.$B$BI am not one to pry, $N, but be more careful, I wouldn\'t let the guards know I associate myself with those kinds of people.', '', '', 53000, 1, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80701, 2, 60, 58, 1519, 0, 0, 0, 0, 0, 0, 0, 53001, 0, 0, 1101, 'The Elusive SI:7', 'Report to the SI:7 and present the ring to Mathias Shaw.', 'Burn this after you\'ve read it.$B$B$N,$B$BI dearly hope this letter finds you in good health, I wish I could\'ve delivered the message in person but you must understand that we like to keep secrecy at hand.$B$BI am not sure if you\'re aware of what our organisation does, or who we entirely are, but we have discovered valuable information and we might need your help.$B$BIn the envelope you will find a ring, keep it at hand while you come visit us, it will be the sign you\'ve accepted our mission and that the letter was burnt.$B$BUntil we meet,\nMathias Shaw.', '', '', 0, 0, 0, 0, 0, 0, 53001, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80702, 2, 60, 60, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Young and Foolish', 'Interrogate the people of Lakeshire and find out the truth. Report back to Mathias Shaw.', 'My agents have reported that a Scarlet caravan has started moving through various towns.$B$BFrom what we know they have already gone to Lakeshire, Darkshire, Menethil and Southshore.$B$BMy only assumption is that whoever took over the Crusade after the events that transpired the Scarlet Monastery, Hearthglen and Stratholme has realised they\'ve been running short on men.$B$BI want you to go and speak to the people of Lakeshire. The locals should have at least seen something.', '', '', 0, 0, 0, 0, 50665, 1, 0, 0, 'Speak to Foreman Oslow', 0, 0, 0, 0, 50666, 1, 0, 0, 'Speak to Dorin Songblade', 0, 0, 0, 0, 50667, 1, 0, 0, 'Speak to Magistrate Solomon', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80730, 2, 60, 60, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Caravan Meets Caravan', 'Follow the Caravan\'s route and look for clues.', 'The SI:7 have means of communication that reach us quite fast and believe it or not they are very reliable.$B$BSparing you any further details you should know that a dwarven caravan that was meant to reach Aerie Peak never made it out of the Wetlands.$B$BThe caravan lays in ruins and you can only find the mutilated husks of what used to be dwarves.$B$BOur agents already poked around the zone but failed to find anything, they are currently trying to localize these newly recruited Scarlet zealots.$B$BI\'m not very sure how much of a detective you believe yourself to be, but I ask you to take a second look, maybe they missed something.$B$BIf you find the recruits, keep in mind that we aren\'t sure what manner of persuasion the Scarlets used to brainwash them, spare as many as you can and take them to Menethil.', '', '', 0, 0, 0, 0, 50684, 1, 0, 0, 'Find the first clue', 0, 0, 0, 0, 50685, 1, 0, 0, 'Find the second clue', 0, 0, 0, 0, 50686, 1, 0, 0, 'Find the third clue', 0, 0, 0, 0, 50669, 1, 0, 0, 'Ask Kixxle if he saw anything', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80703, 2, 60, 60, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Thandol Span', 'Bring Vladeus Springriver back to Menethil Harbor and report back to Captain Stoutfist.', 'Yeah bub that\'s all I know, now I don\'t say I deserve any kind of compensation for the information but it will highly be appreciated.$B$B<Kixxle holds open his palm but you refuse to pay.>$B$BFine then, go on and follow the road to that bridge, Thandol Span or whatever, I hope those Scarlets get you for being such a prick!', '', '', 0, 0, 53002, 1, 50670, 1, 53002, 1, 'Defeat Scarlet Recruits', 0, 0, 0, 0, 50671, 1, 0, 0, 'Bring Vladeus Springriver back to Menethil Harbor', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80704, 2, 60, 60, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Are You True to Your Nature?', 'Decide what to do with Vladeus.', 'We\'ve been trying to no avail to interrogate the young lad you brought back, $N. He simply wouldn\'t talk, me and the other guards tried to persuade him as best as we could.$B$BConsidering you were there to put an end to their masquerade, I\'d assume you\'d have a better chance to draw some information out of him.$B$BCredits given where credits are due, you did a great job putting piece to piece together and finding them.$B$BTake whatever approach you\'d like, just see it done.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80705, 2, 60, 60, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'The Means of Persuading', 'Use your persuasion skills to interrogate Vladeus.', 'During your many adventures through Azeroth you have faced several perils and foes, unlike the man present before you.$B$BYou are more than sure he\'s not a wicked sort and chose to approach this lightly, staying true to your nature.$B$BWith a table full of choices you pick the best means of persuasion and are ready to begin.', '', '', 0, 0, 0, 0, 50675, 1, 0, 0, 'Obtain information from Vladeus', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80706, 2, 60, 60, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Seeking Justice or Vengeance?', 'Find out everything by any means necessary.', 'You\'ve met many foes on your several adventures through Azeroth, for the first time something in you clicked.$B$BHow many more scum do you have to beat, maim and kill so that this twisted world gets its damnable peace?$B$BThe Scarlet Crusade has been a personal thorn in your sides as well, maybe it\'s time to deliver some sort of justice or is it vengeance?$B$BWith a table full of tools that will aid you to obtain what you need, you are ready to embrace your demons.', '', '', 0, 0, 0, 0, 50675, 1, 0, 0, 'Obtain information from Vladeus', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80707, 2, 60, 60, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'The Price Of Information', 'Report to Captain Stoutfist.', 'You\'ve extracted all the information you could get from Vladeus. Deciding you\'re done with him you let him rest and think about your next actions.$B$BIt seems news of Whitemane\'s death and the demonic influence over Stratholme reached the ears of Lady Abbendis, the last true leader of the Scarlet Crusade.$B$BWith one of her henchmen tricking young men and women to join their cause and force them into staying she\'s trying to regain some numbers.$B$BYou decide to report this to Stoutfist and ask for his opinion.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80708, 2, 60, 60, 1519, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1101, 'Scarlet Aid', 'Travel to the Cathedral’s District of Stormwind and speak with Brother Crowley.', 'My boys made preparation for the prisoner to reach Stormwind. His fate will be decided there since he’s part of their jurisdiction.$B$BYou were of great help and I am sure you want to poke around this thing even further. I might have a lead for you, not sure how much it will help though.$B$BUnder the Cathedral District’s Chapel there’s a priest in red robes. The intel I got from Shaw’s men says that his name is Brother Crowley and was sent by the Scarlet Crusade inside the city as an ambassador of sorts.$B$BHis mission was to recruit the willing to fight in the name of the Light or whatever stupid lie these Scarlets are telling to themselves.$B$BIn any case, Crowley hasn’t been that active. We are not sure if he’s the one to recruit these blokes but it’s worth a try.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80709, 2, 60, 60, 139, 0, 0, 80710, 0, 0, 0, 0, 53003, 0, 0, 1101, 'Donning the Red Flag', 'Travel to Tyr’s Hand and report to Mavel Brightwood.', 'Abbendis must be stopped and you will be one of the thorns in her side and how better should you do it if not from the inside?$B$BWhile I hold no skill in the arts of the Arcane, a dear friend of mine who, just like me, would love to see her fall has provided me in the past with a few scrolls that could change one’s appearance.$B$BI am more than happy to offer you one if you were to tell nobody of it. Let’s just say the scrolls were for something more meaningful, yet desperate times call for desperate measures.$B$BUse this when close to Tyr’s Hand, claim to be one of the disciples of the caravan you destroyed and claim your team was slain by the ogres of Arathi.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80710, 2, 60, 60, 139, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'It’s All in Their Brains', 'Hunt undead all over the Plaguelands and gather their brains.', 'Ready for your first assignment?$B$BYour armor looks shabby and your blade dull but if you’re not able to pull up your own weight you’re not worth the trouble of the Light.$B$BTravel the Plaguelands, slay any undead in your path and bring me their brains. Their brains are essential for something the High General has planned, simply do your job and ask no questions.$B$BGo you fool, the Light waits for nobody, go on and claim your glorious purpose.', '', '', 0, 0, 53004, 30, 0, 0, 53004, 30, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80711, 2, 60, 60, 139, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Supplies We Need', 'Travel the world and bring back the supplies you were asked to.', 'Your next errand is to simply collect a few things here and there, nothing special.$B$BYou will find these while fighting Elementals and plants in some of the actual dangerous zones of the world, but I am more than sure you will succeed if you truly are chosen by the Light.$B$BBring me Savage Fronds and Core of the Elements, fifty of each, it will be a great help in what we wish to achieve.$B$BWhen and if you return you will officially be a member and I will give you a map as to where to find the entrance for the secret training spot.$B$BMay the Light bless your poor soul. If you return we will embrace you as a sibling, if you do not we will not mourn for you even for a second.', '', '', 53005, 1, 0, 0, 0, 0, 22529, 50, '', 0, 0, 0, 0, 0, 0, 22527, 50, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80720, 2, 60, 58, 1497, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 690, 'A Dreadful Summon', 'Report to Varimathras in Undercity.', '$N, is it?$B$BLord Varimathras tasked me to seek you out at once.$B$BI believe you know where to find him — he stands by the Dark Lady, forever bound to linger in her shadow.$B$BAnd now it is his shadow that looms over you; I would not try his patience.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80721, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'Grim News', 'Travel to Brill, the Sepulcher and Tarren Mill. Speak to High Executor Darthalia, Executor Zygand and High Executor Hadrec. Report back to Varimathras.', 'Word has come to me of strange occurrences on the frontlines.$B$BSome of our Queen\'s finest servants have gone missing. Too many, too swiftly and with conspicuous precision to be mere ill luck in warfare.$B$BMy Deathstalkers are preoccupied with far direr tasks, hence I would have you travel to Brill, the Sepulcher and Tarren Mill to collect the accounts of the local executors in their stead.$B$BReturn to me, and if I am pleased, I might just reward you.', '', '', 0, 0, 0, 0, 50665, 1, 0, 0, 'Speak to Executor Zygand', 0, 0, 0, 0, 50666, 1, 0, 0, 'Speak to High Executor Hadrec', 0, 0, 0, 0, 50667, 1, 0, 0, 'Speak to High Executor Darthalia', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80722, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'To Catch a Rat...', 'Find Deathguard Maverick and set a trap for the Scarlet Crusade. Report back to Varimathras.', 'If we truly want to unravel the truth of this ploy, we will have to spur the Scarlets to play their cards into our hands.$B$BFor this purpose, I have pressed a Deathguard into your service. His name is Maverin, or Moverish — human names are a blight to my tongue.$B$BYou will find him in the graveyard near the path to the Monastery in the north. Have him play the bait, he is not a valuable asset, then slay the Scarlets and seize whatever you can find of this curious new weapon in their arsenal.$B$BDo not disappoint me.', '', '', 0, 0, 53010, 1, 50668, 1, 53010, 1, 'Speak to Deathguard Maverick', 0, 0, 0, 0, 50681, 2, 0, 0, 'Defeat Scarlets Guards', 0, 0, 0, 0, 50670, 1, 0, 0, 'Inspect Maverick\'s condition', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80723, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 53010, 0, 0, 690, 'Trusted Apothecary', 'Take the vial to the Apothecarium and speak to Varimathras’ trusted apothecary.', 'So this potion is the crux of the Scarlet schemes. Dull, crude and yet irritatingly potent.$B$BI myself do not dabble in the low craft of alchemy. Fortunately, our Queen\'s Royal Apothecaries favor the art of pondering alembics and grinding grass.$B$BVenture to the Apothecarium, find Apothecary Zwinker and show her what you have found. She is a creature of mine.$B$BGo, be quick and be discreet.', '', '', 0, 0, 0, 0, 0, 0, 53010, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80724, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 53010, 0, 0, 690, 'Consulting an Expert', 'Find Gunther Arcanus in Tirisfal Glades.', 'I did perform a few precursory tests on the substance you have with you. All I have been able to discern is that the potion contains Peacebloom and Ghost Hair.$B$BBut that cannot answer for the catatonic state it forces upon undead.$B$BIt is my hypothesis that this concoction has been tampered with some manner of higher spellcraft, and that is beyond my abilities to solve.$B$BThere is only one who can give us the answers we need. He dwells at the centre of Brightwater Lake, east of Brill.$B$BApproach him with great reverence and measure your words accordingly.', '', '', 0, 0, 0, 0, 0, 0, 53010, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80725, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 53011, 0, 0, 690, 'In Gunther’s Favor', 'Travel behind Ambermill and dig for Gunther’s locket.', 'I sometimes long for Dalaran and of the days I once lived as no more than a mere student of the arcane arts.$B$BWhen the Scourge shackled me to their dominion, my old memories were the only tether that kept me from losing myself utterly.$B$BI do not intend to burden you with my life\'s story, $N, but I already know what this vial is and how it was made, yet I need you to do me a favor before I tell you. Think of it as an equivalent exchange.$B$BGo to the decadent town of Ambermill: Behind its town hall I buried a locket and sealed it with magic.$B$BI will give you a scroll that will erase its warding spell, retrieve the locket, and return it to me. Then we shall talk.', '', '', 0, 0, 53012, 1, 0, 0, 53012, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80726, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'Soul and Alchemy', 'Return to Varimathras in Undercity.', 'The potion brewed by the Scarlets that you retrieved is known as the Draught of Dormant Death, or Mortudiant as we scholars prefer.$B$BIt was first conceived during the Second War, in Dalaran, to aid in countering the unhallowed might of Gul\'dan\'s death knights.$B$BIt can only be concocted with a specific alchemical implement commonly used in transmutation known as the Philosopher\'s Stone. Which, unfortunately, I neither possess nor know how to emulate.$B$BFor now, you should return to your masters in the Undercity with what you\'ve learned. I will keep the potion and see whether I can learn anything else.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80727, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 53013, 0, 0, 690, 'Dark Temper for a Dark Lady', 'Report to Sylvanas.', 'I have prepared a report of our findings to be delivered to the Dark Lady.$B$BShe will little like what she shall read, and it would be a shame if her wrath were to be your end.$B$BSo kneel before her, appease her, serve her as loyally as you served me...but do not forget to whom you belong.', '', '', 0, 0, 0, 0, 0, 0, 53013, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80728, 2, 60, 60, 1497, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 690, 'The Future Looks Grim', 'Travel to Tyr\'s Hand in the Eastern Plaguelands, obtain a Scarlet Initiate Uniform, then return to Gunther Arcanus on the isle of Brightwater Lake.', 'I know all of the draught that clouds the minds of my warriors, your collusion with my dreadlord and the deathguard you\'ve squandered at his behest.$B$BBut perhaps you have grown fond of Varimathras. Would you like to be one of his playthings? One word and I will make sure you are his. Forever.$B$BNo? You yet value your soul? Pity.$B$BThen you will do as I say and go to Tyr\'s Hand, in the Eastern Plaguelands. Fetch a Scarlet uniform from those zealous fools and bring it to Gunther. He will know the rest.$B$BGo now, begone from my sight.', '', '', 0, 0, 53014, 1, 0, 0, 53014, 1, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(80729, 2, 60, 60, 1497, 0, 0, 80710, 0, 0, 0, 0, 53003, 0, 0, 690, 'A Different Shade of Red', 'Travel to Tyr’s Hand and report to Mavel Brightwood.', 'As you may have divined, we contrive to infiltrate you into the ranks of the Scarlet Crusade.$B$BUpon the uniform you\'ve brought me I placed an illusion charm, as well as a few greater cloaking wards to keep the enchantment from easy detection.$B$BAll that is left is for you to introduce yourself as a novice to the recruiters in Tyr\'s Hand.$B$BOne such recruiter should be Mavel Brightwood.$B$BI wish you luck, $N. Have your wits about you and find out what you can of their meddlesome alchemists.', '', '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `quest_template_addon` (`ID`, `MaxLevel`, `AllowableClasses`, `SourceSpellID`, `PrevQuestID`, `NextQuestID`, `ExclusiveGroup`, `ProvidedItemCount`, `SpecialFlags`) VALUES
(80700, 0, 0, 0, 0, 0, 0, 0, 0),
(80701, 0, 0, 0, 80700, 0, 0, 1, 0),
(80702, 0, 0, 0, 80701, 0, 0, 0, 0),
(80730, 0, 0, 0, 80702, 0, 0, 0, 0),
(80703, 0, 0, 0, 80730, 0, 0, 0, 0),
(80704, 0, 0, 0, 80703, 0, 0, 0, 0),
(80705, 0, 0, 0, 80704, 80707, 80705, 0, 0),
(80706, 0, 0, 0, 80704, 80707, 80705, 0, 0),
(80707, 0, 0, 0, 80705, 0, 0, 0, 0),
(80708, 0, 0, 0, 80707, 0, 0, 0, 0),
(80709, 0, 0, 0, 80708, 80710, 80709, 1, 0),
(80710, 0, 0, 0, 80709, 0, 0, 0, 0),
(80711, 0, 0, 0, 80710, 0, 0, 0, 0),
(80720, 0, 0, 0, 0, 0, 0, 0, 0),
(80721, 0, 0, 0, 80720, 0, 0, 0, 0),
(80722, 0, 0, 0, 80721, 0, 0, 0, 0),
(80723, 0, 0, 0, 80722, 0, 0, 1, 0),
(80724, 0, 0, 0, 80723, 0, 0, 1, 0),
(80725, 0, 0, 0, 80724, 0, 0, 1, 0),
(80726, 0, 0, 0, 80725, 0, 0, 0, 0),
(80727, 0, 0, 0, 80726, 0, 0, 1, 0),
(80728, 0, 0, 0, 80727, 0, 0, 0, 0),
(80729, 0, 0, 0, 80728, 80710, 80709, 1, 0);

INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `Emote2`, `Emote3`, `Emote4`, `EmoteDelay1`, `EmoteDelay2`, `EmoteDelay3`, `EmoteDelay4`, `RewardText`, `VerifiedBuild`) VALUES
(80700, 0, 0, 0, 0, 0, 0, 0, 0, 'Here\'s the letter, I hope I won\'t have to do this again.', 0),
(80701, 0, 0, 0, 0, 0, 0, 0, 0, 'Ah, my ring.$B$BIt seems you\'ve made it, apologies for the secrecy but we must be careful, even our walls have ears that do not belong to the organisation.', 0),
(80702, 0, 0, 0, 0, 0, 0, 0, 0, 'So we were right, this would\'ve been valuable information if we didn\'t already receive another report.$B$BSorry about that, $N. I will be needing your help once more.', 0),
(80730, 0, 0, 0, 0, 0, 0, 0, 0, 'Listen here pal, I am trying to make a living, so you either buy something or scram!$B$BOf course unless you got something else to talk about but make it quick!', 0),
(80703, 0, 0, 0, 0, 0, 0, 0, 0, 'So this is all you could salvage from the idiots that willingly murdered our caravan, eh?$B$BI’ll take him to the dungeon, good job.', 0),
(80704, 0, 0, 0, 0, 0, 0, 0, 0, 'You are at an impasse, not sure how to proceed. Given the circumstances you must make the best out of what you have.$B$BWhile contemplating the matter you take a wide look around the room, noticing that Stoutfist and the other guards left some means of approach to you. It\'s time for you to decide how to approach the interrogation of the prisoner.$B$BThe coffee mug on the table tells you it\'d be best to persuade him. The iron maiden next to him gives you other ideas.', 0),
(80705, 0, 0, 0, 0, 0, 0, 0, 0, 'Reaching for the quill and ink, you note the information you extracted from Vladeus thus finalizing the report.', 0),
(80706, 0, 0, 0, 0, 0, 0, 0, 0, 'Reaching for the quill and ink, you note the information you extracted from Vladeus thus finalizing the report.', 0),
(80707, 0, 0, 0, 0, 0, 0, 0, 0, 'It seems you got what you needed then, we will send the prisoner back to Stormwind so they decide his fate.$B$BWhatever you did to obtain this information, I won\'t judge it, I just hope you are content with your own choices.', 0),
(80708, 0, 0, 0, 0, 0, 0, 0, 0, 'Bold accusation, $R, I almost feel offended.$B$BI fear it was not me, things would’ve been simpler. I assume you got a name from your prisoner. Tell me what happened.', 0),
(80709, 0, 0, 0, 0, 0, 0, 0, 0, 'We’ve been expecting at least a handful of new recruits, not just one.$B$BExplain yourself immediately.', 0),
(80710, 0, 0, 0, 0, 0, 0, 0, 0, 'Perfect condition, if anything this rotten could be called something other than disgusting.$B$BBlasted Scourge, I hope the High General is right.$B$BNow onto your next task, recruit.', 0),
(80711, 0, 0, 0, 0, 0, 0, 0, 0, 'Welcome back, brother and may the Light bless us both in the days to come.$B$BHere’s your insignia and here’s the map for the entrance, the High General will be very pleased to have you.$B$BFor the Scarlet Crusade, for the Light and for Lordaeron!', 0),
(80720, 0, 0, 0, 0, 0, 0, 0, 0, 'Ah, $N, here to do my bidding. I expect you to be quicker if you deem yourself worthy of remaining in my service.', 0),
(80721, 0, 0, 0, 0, 0, 0, 0, 0, 'The fanatics of the Scarlet Crusade are behind this?$B$BHere I thought such cunning to be bereaved of their agitable little brains.', 0),
(80722, 0, 0, 0, 0, 0, 0, 0, 0, 'I can smell the sweet stench of man-blood on you, $N. Good, very good.$B$BAs for Deathguard Mavonius there, the Undertakers and Apothecaries can tend to him, and I expect that to be the last of your concerns.', 0),
(80723, 0, 0, 0, 0, 0, 0, 0, 0, 'My name is Zinge, $C.$B$BShow me what you\'ve brought and I shall help you as I can, if such is my lord\'s command.', 0),
(80724, 0, 0, 0, 0, 0, 0, 0, 0, 'If your tale and the effects of this potion are true, you were right to come to me.$B$BThis is a weapon that should never lay in the hands of the Scarlet Crusade. As for what it is, you will have to indulge me momentarily.', 0),
(80725, 0, 0, 0, 0, 0, 0, 0, 0, 'You had to battle a mage for it?$B$BI presume he failed to speak his name as you slew him, but that ought to be no concern of ours.$B$BYou fulfilled your end of the bargain, $N, and it is now my turn to repay the debt.', 0),
(80726, 0, 0, 0, 0, 0, 0, 0, 0, 'Bah, draughts, potions and stones. Could there be anything more tedious?$B$BAt least that so-called \'lich\' made himself useful. As did you.$B$BYou have pleased me once more.', 0),
(80727, 0, 0, 0, 0, 0, 0, 0, 0, 'Do you think me a fool, $N? Did you think I would be unaware of what occurs within my own realm, within my own throne room?$B$B<Sylvanas shreds the report with her hands.>', 0),
(80728, 0, 0, 0, 0, 0, 0, 0, 0, 'That will suffice. Lay it here for a moment. It will not take me long.', 0),
(80729, 0, 0, 0, 0, 0, 0, 0, 0, 'Ah, another recruit, what took you so long to get here?', 0);

INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`, `VerifiedBuild`) VALUES
(80700, 0, 0, 'Just take it off my hands before the guards think we\'re doing something shady.', 0),
(80701, 0, 0, 'How can I help you, stranger?', 0),
(80702, 0, 0, 'How is your task going?', 0),
(80730, 0, 0, 'Now do you want to buy something or just bother me?', 0),
(80703, 0, 0, 'The Scarlet Crusade must be put to an end.', 0),
(80704, 0, 0, 'The figure in front of you is displeased at your sight and is practically tearing you apart in their mind.', 0),
(80705, 0, 0, 'The report seems incomplete, other than some basic information of the prisoner there\'s really nothing useful there.', 0),
(80706, 0, 0, 'The report seems incomplete, other than some basic information of the prisoner there\'s really nothing useful there.', 0),
(80707, 0, 0, '<You are welcomed with nothing but a silent stare.>', 0),
(80708, 0, 0, 'How can I assist?', 0),
(80709, 0, 0, 'Speak quickly or move along.', 0),
(80710, 0, 0, 'Don’t worry yourself with details, do as you were told.', 0),
(80711, 0, 0, 'It’s a simple task, kill and collect, what more do you want?', 0),
(80720, 0, 0, 'Kneel all you like, mortal. I do so enjoy a good groveling.', 0),
(80721, 0, 0, 'I will empty your veins if you dare dawdle before me for one more fruitless instant.', 0),
(80722, 0, 0, 'You return already.$B$BHow is Meverius? Not too tarnished, I hope?', 0),
(80723, 0, 0, 'Zwinker...Yes, I can see that Lord Varimathras sent you.', 0),
(80724, 0, 0, 'Another visitor.', 0),
(80725, 0, 0, 'Were you successful?', 0),
(80726, 0, 0, 'My loyal $R returns.$B$BGo on, speak.', 0),
(80727, 0, 0, '<Sylvanas takes the report you give her. She does not open it.>', 0),
(80728, 0, 0, 'Yes, the Banshee Queen forewarned me of your arrival. Do you have the uniform at hand?$B$BIt might make amends for the unfortunate feelings I hear you roused in her.', 0),
(80729, 0, 0, 'Speak quickly or move along.', 0);

INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(2198, 80700),
(332, 80702),
(8305, 80703),
(2104, 80704),
(2104, 80708),
(12336, 80709),
(50677, 80710),
(50677, 80711),
(14402, 80720),
(14403, 80720),
(14404, 80720),
(2425, 80721),
(2425, 80722),
(2425, 80723),
(5204, 80724),
(1497, 80725),
(1497, 80726),
(2425, 80727),
(10181, 80728),
(1497, 80729),
(332, 80730);

INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(2198, 80700),
(332, 80701),
(332, 80702),
(2104, 80703),
(2104, 80707),
(12336, 80708),
(50677, 80709),
(50677, 80710),
(50677, 80711),
(2425, 80720),
(2425, 80721),
(2425, 80722),
(5204, 80723),
(1497, 80724),
(1497, 80725),
(2425, 80726),
(10181, 80727),
(1497, 80728),
(50677, 80729),
(8305, 80730);

INSERT INTO `gameobject_queststarter` (`id`, `quest`) VALUES
(1000172, 80705),
(1000173, 80706),
(1000171, 80707);

INSERT INTO `gameobject_questender` (`id`, `quest`) VALUES
(1000171, 80704),
(1000171, 80705),
(1000171, 80706);

-- items
INSERT INTO `item_template` (`entry`, `class`, `subclass`, `SoundOverrideSubclass`, `name`, `displayid`, `Quality`, `Flags`, `FlagsExtra`, `BuyCount`, `BuyPrice`, `SellPrice`, `InventoryType`, `AllowableClass`, `AllowableRace`, `ItemLevel`, `RequiredLevel`, `maxcount`, `stackable`, `delay`, `bonding`, `description`, `PageText`, `startquest`, `Material`, `sheath`, `BagFamily`, `RequiredDisenchantSkill`, `VerifiedBuild`, `spellid_1`, `spelltrigger_1`, `spellcharges_1`, `spellcooldown_1`, `spellcategory_1`, `spellcategorycooldown_1`, `spellid_2`, `spelltrigger_2`, `spellcharges_2`, `spellcooldown_2`, `spellcategory_2`, `spellcategorycooldown_2`, `spellid_3`, `spelltrigger_3`, `spellcharges_3`, `spellcooldown_3`, `spellcategory_3`, `spellcategorycooldown_3`, `spellid_4`, `spelltrigger_4`, `spellcharges_4`, `spellcooldown_4`, `spellcategory_4`, `spellcategorycooldown_4`, `spellid_5`, `spelltrigger_5`, `spellcharges_5`, `spellcooldown_5`, `spellcategory_5`, `spellcategorycooldown_5`) VALUES
(53000, 0, 0, -1, 'Sealed Letter', 3048, 1, 2048, 0, 1, 0, 0, 0, -1, -1, 1, 60, 1, 1, 0, 4, 'The seal bears no crest.', 0, 80701, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53001, 12, 0, -1, 'Mathias Shaw\'s Ring', 23728, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53003, 12, 0, -1, 'Tome of Disguise: Scarlet Crusade', 634, 1, 0, 0, 1, 0, 0, 0, -1, -1, 45, 60, 0, 1, 0, 1, '', 0, 0, 0, 1, 0, -1, 0, 19690, 0, -10, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53004, 12, 0, -1, 'Undead\'s Rotten Brain', 10923, 1, 0, 0, 1, 0, 0, 0, -1, -1, 1, 0, 0, 30, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53005, 13, 0, -1, 'Scarlet Crusade Insignia', 31604, 3, 64, 0, 1, 0, 0, 0, -1, -1, 60, 0, 1, 1, 0, 1, 'This insignia marks the bearer as a fully fledged member of the Scarlet Crusade.', 0, 0, 0, 0, 256, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53010, 12, 0, -1, 'Vial of Mysterious Concoction', 33451, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53011, 12, 0, -1, 'Gunther\'s Scroll', 1301, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53012, 12, 0, -1, 'Gunther\'s Locket', 34510, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53013, 12, 0, -1, 'Varimathras\'s Report', 1301, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1),
(53014, 12, 0, -1, 'Scarlet Initiate Uniform', 16612, 1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 0, 4, '', 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1);

INSERT INTO `item_dbc` (`ID`, `ClassID`, `SubclassID`, `Sound_Override_Subclassid`, `Material`, `DisplayInfoID`, `InventoryType`, `SheatheType`) VALUES
(53000, 0, 0, -1, 0, 3048, 0, 0),
(53001, 12, 0, -1, 0, 23728, 0, 1),
(53003, 12, 0, -1, 0, 634, 0, 1),
(53004, 12, 0, -1, 0, 10923, 0, 1),
(53005, 13, 0, -1, 0, 31604, 0, 0),
(53010, 12, 0, -1, 0, 33451, 0, 1),
(53011, 12, 0, -1, 0, 1301, 0, 1),
(53012, 12, 0, -1, 0, 34510, 0, 1),
(53013, 12, 0, -1, 0, 1301, 0, 1),
(53014, 12, 0, -1, 0, 16612, 0, 1);

-- creatures
INSERT INTO `creature_template` (`entry`, `name`, `subname`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RegenHealth`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(50665, 'Quest 80702 & 80720 Custom Trigger 1', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50666, 'Quest 80702 & 80720 Custom Trigger 2', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50667, 'Quest 80702 & 80720 Custom Trigger 3', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50668, 'Quest 80703 & 80722 Custom Trigger 1', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50669, 'Quest 80703 Custom Trigger 2', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50670, 'Quest 80703 & 80722 Custom Trigger 3', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50671, 'Quest 80703 Custom Trigger 3', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50675, 'Quest 80705 & 80706 Custom Trigger 3', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50684, 'Find the first clue', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50685, 'Find the second clue', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50686, 'Find the third clue', NULL, 0, 1, 1, 0, 35, 0, 1.0, 1.14286, 20.0, 0, 0, 1.0, 2000, 2000, 1, 0, 2048, 0, 0, 0, 0, 0, 0, 0, '', 0, 1.0, 1.0, 1.0, 1, 1, 0, '', 0),
(50673, 'Scarlet Recruit', NULL, 0, 60, 60, 0, 89, 0, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 50673, 59, 296, 'SmartAI', 0, 0.735, 0.957, 0.75, 1, 1, 0, '', 0),
(50674, 'Vladeus Springriver', NULL, 51683, 60, 60, 0, 89, 1, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 0, 59, 296, 'SmartAI', 0, 1.186, 0.957, 0.75, 1, 1, 0, '', 0),
(50676, 'Vladeus Springriver', NULL, 51684, 60, 60, 0, 35, 1, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 0, 59, 296, 'SmartAI', 0, 1.186, 0.957, 0.75, 1, 1, 0, '', 0),
(50677, 'Mavel Brightwood', NULL, 0, 60, 60, 0, 67, 3, 1.1, 1.14286, 20.0, 2, 0, 7.938, 1158, 2000, 2, 32832, 2048, 0, 0, 7, 0, 0, 2035, 2141, 'SmartAI', 0, 2.834, 1.741, 0.756, 1, 1, 0, '', 0),
(50680, 'Scarlet Magician', NULL, 0, 60, 60, 0, 7, 0, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 50680, 59, 296, 'SmartAI', 0, 0.735, 0.957, 0.75, 1, 1, 0, '', 0),
(50681, 'Scarlet Guard', NULL, 0, 60, 60, 0, 89, 0, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 50681, 59, 296, 'SmartAI', 0, 0.735, 0.957, 0.75, 1, 1, 0, '', 0),
(50682, 'Scarlet Alchemist', NULL, 0, 60, 60, 0, 7, 0, 1.0, 0.857143, 20.0, 0, 0, 1.823, 2000, 2000, 2, 0, 2048, 0, 0, 7, 0, 50682, 59, 296, 'SmartAI', 0, 3.213, 0.957, 0.75, 1, 1, 0, '', 0),
(51567, 'Deathguard Maverick', NULL, 51690, 30, 30, 0, 68, 1, 1.08, 1.14286, 20.0, 0, 0, 1.444, 1710, 1881, 1, 0, 2048, 0, 0, 7, 0, 0, 0, 0, 'SmartAI', 0, 2.2, 1.0, 1.018, 1, 1, 0, '', 0),
(90974, 'Thandol Span Attack Trigger', NULL, 0, 63, 63, 0, 35, 0, 0.91, 1.14286, 20.0, 3, 0, 0.217, 2000, 2200, 1, 33554434, 2048, 0, 8, 8, 5242886, 0, 0, 0, 'SmartAI', 0, 3.002, 1.0, 0.402, 1, 1, 130, '', 0);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(50665, 0, 328, 1.0, 1, 0),
(50666, 0, 328, 1.0, 1, 0),
(50667, 0, 328, 1.0, 1, 0),
(50668, 0, 328, 1.0, 1, 0),
(50669, 0, 328, 1.0, 1, 0),
(50670, 0, 328, 1.0, 1, 0),
(50671, 0, 328, 1.0, 1, 0),
(50675, 0, 328, 1.0, 1, 0),
(50684, 0, 328, 1.0, 1, 0),
(50685, 0, 328, 1.0, 1, 0),
(50686, 0, 328, 1.0, 1, 0),
(50673, 0, 2467, 1.0, 1, 0),
(50673, 1, 2471, 1.0, 1, 0),
(50673, 2, 2468, 1.0, 1, 0),
(50673, 3, 2483, 1.0, 1, 0),
(50674, 0, 2565, 1.0, 1, 0),
(50676, 0, 2565, 1.0, 1, 0),
(50677, 0, 10518, 1.0, 1, 0),
(50680, 0, 2512, 1.0, 1, 0),
(50681, 0, 2462, 1.0, 1, 0),
(50682, 0, 2525, 1.0, 1, 0),
(51567, 0, 2852, 1.0, 1, 0),
(90974, 0, 10045, 1.0, 1, 0);

INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`) VALUES
(50665, 1, 1, 0, 0, 0, 0),
(50666, 1, 1, 0, 0, 0, 0),
(50667, 1, 1, 0, 0, 0, 0),
(50668, 1, 1, 0, 0, 0, 0),
(50669, 1, 1, 0, 0, 0, 0),
(50670, 1, 1, 0, 0, 0, 0),
(50671, 1, 1, 0, 0, 0, 0),
(50675, 1, 1, 0, 0, 0, 0),
(50684, 1, 1, 0, 0, 0, 0),
(50685, 1, 1, 0, 0, 0, 0),
(50686, 1, 1, 0, 0, 0, 0),
(50673, 1, 1, 0, 0, 0, 0),
(50674, 1, 1, 0, 0, 0, 0),
(50676, 1, 1, 0, 0, 0, 0),
(50677, 1, 1, 0, 0, 0, 0),
(50680, 1, 1, 0, 0, 0, 0),
(50681, 1, 1, 0, 0, 0, 0),
(50682, 1, 1, 0, 0, 0, 0),
(51567, 1, 1, 0, 0, 0, 0),
(90974, 1, 0, 0, 0, 0, 0);

INSERT INTO `creature_equip_template` (`CreatureID`, `ID`, `ItemID1`, `ItemID2`, `ItemID3`, `VerifiedBuild`) VALUES
(50673, 1, 2813, 0, 0, 0),
(50674, 1, 2813, 0, 0, 0),
(50677, 1, 13050, 0, 0, 0),
(50680, 1, 2813, 0, 0, 0),
(50681, 1, 2813, 0, 0, 0),
(50682, 1, 2813, 0, 0, 0),
(51567, 1, 2557, 0, 2552, 0);

-- spawns
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) VALUES
(9990001, 50676, 0, 0, 0, 1, 1, 0, -3736.28, -809.162, 4.32525, 1.10049, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Vladeus Springriver, Menethil prison (tw guid 2571576)'),
(9990003, 51567, 0, 0, 0, 1, 1, 1, 2580.17, -549.507, 87.4045, 5.31687, 300, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Deathguard Maverick, Scarlet Monastery graveyard (tw guid 2569342)'),
(9990004, 90974, 0, 0, 0, 1, 1, 0, -2459.73, -2503.06, 78.507, 3.11, 60, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Thandol Span Attack Trigger (tw guid 328148)');

-- Mavel Brightwood (Tyr's Hand): only if no other module file spawns her (the 2026-10-12 Eastern Plaguelands build 036 does)
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) SELECT 9990002, 50677, 0, 0, 0, 1, 1, 1, 1682.32, -5333.22, 74.2273, 1.24345, 600, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Mavel Brightwood, Tyr\'s Hand (tw guid 2571577)' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `creature` WHERE `id` = 50677);

-- Varimathras and the Seekers: only where this world DB does not spawn them already
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) SELECT 9990005, 2425, 0, 0, 0, 1, 1, 0, 1292.0, 333.0, -60.0, 4.62, 86400, 0.0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Varimathras, Royal Quarter (moved beside Bragor Bloodfist, who uses this spot in 3.3.5) (tw guid 31901)' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `creature` WHERE `id` = 2425);
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) SELECT 9990006, 14402, 0, 0, 0, 1, 1, 0, 1583.51, 256.231, -62.1131, 2.35463, 900, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Seeker Cromwell, Undercity (tw guid 32073)' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `creature` WHERE `id` = 14402);
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) SELECT 9990007, 14403, 0, 0, 0, 1, 1, 0, 1609.25, 223.458, -61.9034, 5.80899, 900, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Seeker Nahr, Undercity (tw guid 32074)' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `creature` WHERE `id` = 14403);
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) SELECT 9990008, 14404, 0, 0, 0, 1, 1, 0, 1617.09, 218.687, -59.2467, 2.52553, 900, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'turtle scarlet chain: Seeker Thompson, Undercity (tw guid 32072)' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `creature` WHERE `id` = 14404);

-- Gunther's Lockbox (only players on "In Gunther's Favor" can open it)
INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`, `Data0`, `Data1`, `Data3`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES
(1000177, 3, 10, 'Gunther\'s Lockbox', '', '', '', 0.7, 43, 1000177, 1, '', '', 0);

INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`, `mingold`, `maxgold`) VALUES
(1000177, 0, 4, 0, 0);

INSERT INTO `gameobject` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `position_x`, `position_y`, `position_z`, `orientation`, `rotation0`, `rotation1`, `rotation2`, `rotation3`, `spawntimesecs`, `animprogress`, `state`, `ScriptName`, `VerifiedBuild`, `Comment`) VALUES
(9990009, 1000177, 0, 0, 0, 1, 1, -129.932, 748.791, 61.2702, 2.55272, 0.0, 0.0, 0.956966, 0.290201, 30, 100, 1, '', 0, 'turtle scarlet chain: Gunther\'s Lockbox, behind Ambermill\'s town hall (tw guid 5003782)');

-- loot
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(50673, 53002, 0, 100, 1, 1, 0, 1, 1, 'Scarlet Recruit\'s Insignia Ring'),
(50680, 16882, 0, 5, 0, 1, 0, 1, 1, 'Battered Junkbox'),
(50681, 16882, 0, 5, 0, 1, 0, 1, 1, 'Battered Junkbox'),
(50682, 16882, 0, 5, 0, 1, 0, 1, 1, 'Battered Junkbox');

-- Turtle's quest drops on 3.3.5 creatures (Eastern Plaguelands undead, Tyr's Hand Scarlets)
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(8530, 53004, 0, 90.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(8531, 53004, 0, 80.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(8532, 53004, 0, 80.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(8544, 53004, 0, 90.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(10946, 53004, 0, 90.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(16141, 53004, 0, 90.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(16380, 53004, 0, 80.0, 1, 1, 0, 1, 1, 'Undead\'s Rotten Brain'),
(9447, 53014, 0, 30.0, 1, 1, 0, 1, 1, 'Scarlet Initiate Uniform'),
(9449, 53014, 0, 30.0, 1, 1, 0, 1, 1, 'Scarlet Initiate Uniform'),
(9452, 53014, 0, 30.0, 1, 1, 0, 1, 1, 'Scarlet Initiate Uniform');

INSERT INTO `gameobject_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(1000177, 53012, 0, 100, 1, 1, 0, 1, 1, 'Gunther\'s Locket');

-- gossip
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`, `VerifiedBuild`) VALUES
(41333, 'I don\'t have much time for idle talk, $N.  I\'ve got to get this bridge rebuilt before the rains come.  I\'ve finished every project on-time and under budget and I\'m not about to start slipping now.', NULL, 0, 0, 1, 0),
(41334, 'Yes. A caravan with men and women dressed in scarlet passed through here. Many of our young ones followed them.', NULL, 0, 0, 1, 0),
(41335, 'I am really busy crafting this armor, so make it quick!', NULL, 0, 0, 1, 0),
(41336, 'Aye, our young ones left with them. Can you blame them? Look at this place.', NULL, 0, 0, 1, 0),
(41337, 'Who is this $c who goes before the Court of Lakeshire in the Kingdom of Stormwind?  State your business within this township, $R.  The orc threat to the Kingdom is far too great to squander time in idle conversation.', NULL, 0, 0, 1, 0),
(41338, 'It\'s regrettable that our children left with those foolish zealots of the crusade in the middle of the night! Please, don\'t harm them. Send them back home to us.', NULL, 0, 0, 1, 0),
(41343, 'Greetings, potential customer! I\'ve got many rare herbs for sale. Take a look.', NULL, 0, 0, 1, 0),
(41344, 'Yea boss, I sure did. I\'m a merchant, you know. If I got it, I sell it.', NULL, 0, 0, 1, 0),
(41345, 'They went North I guess, following in the footsteps of that dwarven caravan. One of them said they\'d wait by the bridge for an ambush or something. He didn\'t look like the sharpest tool in the shed, you get me?', NULL, 0, 0, 1, 0),
(41346, 'You\'re joking, right? There were like at least five of them!', NULL, 0, 0, 1, 0),
(51683, 'I am taking responsibility for what I have done, don\'t worry, I will follow you and behave.', NULL, 0, 0, 1, 0),
(51684, 'What are they going to do to me? I am sorry for all I have done, I really am.\n\nI regret all of it, and given the chance I will surely make amends.', NULL, 0, 0, 1, 0),
(51685, 'Please, don\'t kill me, please!\n\nI don\'t know anything else, please! I just want to go home.', NULL, 0, 0, 1, 0),
(51690, 'Are you the one Lord Varimathras spoke about, for the important mission?', NULL, 0, 0, 1, 0),
(51691, 'Maverick seems to be in a deep slumber nothing would be able to wake him up.', NULL, 0, 0, 1, 0);

INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES
(41333, 41333),
(41334, 41334),
(41335, 41335),
(41336, 41336),
(41337, 41337),
(41338, 41338),
(41343, 41343),
(41344, 41344),
(41345, 41345),
(41346, 41346),
(51683, 51683),
(51684, 51684),
(51684, 51685),
(9080001, 51684),
(9080002, 51684),
(9080003, 51684),
(9080004, 51684),
(9080005, 51684),
(9080011, 51685),
(9080012, 51685),
(9080013, 51685),
(9080014, 51685),
(9080015, 51685),
(9080016, 51685),
(9080030, 68),
(9080031, 68),
(51690, 51690),
(51690, 51691);

INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(41333, 0, 0, 'Anything strange happen recently?', 0, 1, 1, 41334, 0, 0, 0, '', 0, 0),
(41335, 0, 1, 'I want to browse your goods.', 3370, 3, 128, 0, 0, 0, 0, '', 0, 0),
(41335, 1, 0, 'Anything strange happen recently?', 0, 1, 1, 41336, 0, 0, 0, '', 0, 0),
(41337, 0, 0, 'Anything strange happen recently?', 0, 1, 1, 41338, 0, 0, 0, '', 0, 0),
(41343, 0, 1, 'I want to browse your goods.', 3370, 3, 128, 0, 0, 0, 0, '', 0, 0),
(41343, 1, 0, 'Were you the one to sell an oil canister to a group of men dressed in scarlet?', 0, 1, 1, 41344, 0, 0, 0, '', 0, 0),
(41344, 0, 0, 'Where did they go?', 0, 1, 1, 41345, 0, 0, 0, '', 0, 0),
(41345, 0, 0, 'Why didn\'t you stop them?', 0, 1, 1, 41346, 0, 0, 0, '', 0, 0),
(51683, 0, 0, 'I\'m taking you to the local law enforcement.', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(11499, 50, 7, 'This guy here is the only survivor of those who attacked the caravan that was ment to reach Aerie Peak, he yielded and I have spared his life.', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(51684, 0, 0, 'Vladeus Springriver, from Lakeshire, is it?', 0, 1, 1, 9080001, 0, 0, 0, '', 0, 0),
(9080001, 0, 0, 'Offer water to Vladeus.', 0, 1, 1, 9080002, 0, 0, 0, '', 0, 0),
(9080002, 0, 0, 'Please Vladeus, make this easier for both of us. You look like a decent man, the people of Lakeshire wanted me to bring all of you back.', 0, 1, 1, 9080003, 0, 0, 0, '', 0, 0),
(9080003, 0, 0, 'There is nothing to fear with me at your side, the Alliance will protect your family. The Scarlet Crusade already failed so many times.', 0, 1, 1, 9080004, 0, 0, 0, '', 0, 0),
(9080004, 0, 0, 'I do, take my word for it. Who recruited you and why?', 0, 1, 1, 9080005, 0, 0, 0, '', 0, 0),
(9080005, 0, 0, 'Abbendis?', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(51684, 1, 10, 'You smash your right fist into his sides.', 0, 1, 1, 9080011, 0, 0, 0, '', 0, 0),
(9080011, 0, 0, 'Silence mongrel, you will start talking before I do more than that.', 0, 1, 1, 9080012, 0, 0, 0, '', 0, 0),
(9080012, 0, 0, 'Last time I visited the Monastery I remember your people using this tool.\n\n<You grab a hot poker and place it one Vladeus\' neck.>\n\nNow talk!', 0, 1, 1, 9080013, 0, 0, 0, '', 0, 0),
(9080013, 0, 0, 'Your COMPANIONS murdered innocents.\n\n<You reach for the prongs.>', 0, 1, 1, 9080014, 0, 0, 0, '', 0, 0),
(9080014, 0, 0, 'He\'s not the one holding your life in his hands at this very moment.\n\n<You push the prongs close to his face.>', 0, 1, 1, 9080015, 0, 0, 0, '', 0, 0),
(9080015, 0, 0, 'Abbendis?', 0, 1, 1, 9080016, 0, 0, 0, '', 0, 0),
(9080016, 0, 0, 'Kick him in his knee.', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(9080030, 0, 0, 'You\'re missing a few guards.', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(9080031, 0, 0, 'Rumors say you\'ve lost a couple of men, is that true?', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(11886, 50, 0, 'Two other encampments have lost a few of their guards, did this also happen here?', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(51690, 0, 0, 'Are you ready, Maverick?', 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(51690, 1, 0, 'Inspect Maverick\'s condition.', 0, 1, 1, 0, 0, 0, 0, '', 0, 0);

-- 3.3.5 NPCs that get a menu, the gossip flag or SmartAI
UPDATE `creature_template` SET `gossip_menu_id` = 41333, `npcflag` = `npcflag` | 1 WHERE `entry` = 341;
UPDATE `creature_template` SET `gossip_menu_id` = 41335, `npcflag` = `npcflag` | 1 WHERE `entry` = 956;
UPDATE `creature_template` SET `gossip_menu_id` = 41337, `npcflag` = `npcflag` | 1 WHERE `entry` = 344;
UPDATE `creature_template` SET `gossip_menu_id` = 41343, `npcflag` = `npcflag` | 1 WHERE `entry` = 8305;
UPDATE `creature_template` SET `gossip_menu_id` = 9080030, `npcflag` = `npcflag` | 1 WHERE `entry` = 1515;
UPDATE `creature_template` SET `gossip_menu_id` = 9080031, `npcflag` = `npcflag` | 1 WHERE `entry` = 1952;
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (341,956,344,8305,2104,12336,1515,1952,2215,2425) AND `AIName` = '' AND `ScriptName` = '';

INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
(15, 41333, 0, 0, 0, 47, 0, 80702, 10, 0, 0, 0, 0, '', 'Young and Foolish taken'),
(15, 41335, 1, 0, 0, 47, 0, 80702, 10, 0, 0, 0, 0, '', 'Young and Foolish taken'),
(15, 41337, 0, 0, 0, 47, 0, 80702, 10, 0, 0, 0, 0, '', 'Young and Foolish taken'),
(15, 41343, 1, 0, 0, 2, 0, 53002, 1, 0, 0, 0, 0, '', 'has Scarlet Recruit\'s Insignia Ring'),
(15, 51683, 0, 0, 0, 47, 0, 80703, 8, 0, 0, 0, 0, '', 'Thandol Span in progress'),
(15, 51683, 0, 0, 0, 48, 0, 80703, 0, 1, 0, 0, 0, '', 'Vladeus defeated'),
(15, 51683, 0, 0, 0, 48, 0, 80703, 1, 1, 1, 0, 0, '', 'not brought back yet'),
(15, 11499, 50, 0, 0, 47, 0, 80703, 8, 0, 0, 0, 0, '', 'Thandol Span in progress'),
(15, 11499, 50, 0, 0, 48, 0, 80703, 1, 1, 1, 0, 0, '', 'not brought back yet'),
(15, 11499, 50, 0, 0, 29, 0, 50674, 30, 0, 0, 0, 0, '', 'Vladeus followed the player here'),
(14, 51684, 51685, 0, 0, 47, 0, 80706, 8, 0, 0, 0, 0, '', 'violent text for Seeking Justice or Vengeance?'),
(15, 51684, 0, 0, 0, 47, 0, 80705, 8, 0, 0, 0, 0, '', 'The Means of Persuading'),
(15, 51684, 0, 0, 0, 48, 0, 80705, 0, 1, 1, 0, 0, '', 'not interrogated yet'),
(15, 51684, 1, 0, 0, 47, 0, 80706, 8, 0, 0, 0, 0, '', 'Seeking Justice or Vengeance?'),
(15, 51684, 1, 0, 0, 48, 0, 80706, 0, 1, 1, 0, 0, '', 'not interrogated yet'),
(15, 9080030, 0, 0, 0, 47, 0, 80721, 8, 0, 0, 0, 0, '', 'Grim News'),
(15, 9080030, 0, 0, 0, 48, 0, 80721, 0, 1, 1, 0, 0, '', 'not asked yet'),
(15, 9080031, 0, 0, 0, 47, 0, 80721, 8, 0, 0, 0, 0, '', 'Grim News'),
(15, 9080031, 0, 0, 0, 48, 0, 80721, 1, 1, 1, 0, 0, '', 'not asked yet'),
(15, 11886, 50, 0, 0, 47, 0, 80721, 8, 0, 0, 0, 0, '', 'Grim News'),
(15, 11886, 50, 0, 0, 48, 0, 80721, 2, 1, 1, 0, 0, '', 'not asked yet'),
(14, 51690, 51691, 0, 0, 48, 0, 80722, 1, 2, 0, 0, 0, '', 'both Scarlet Guards defeated'),
(15, 51690, 0, 0, 0, 47, 0, 80722, 8, 0, 0, 0, 0, '', 'To Catch a Rat...'),
(15, 51690, 0, 0, 0, 48, 0, 80722, 0, 1, 1, 0, 0, '', 'trap not set yet'),
(15, 51690, 1, 0, 0, 47, 0, 80722, 8, 0, 0, 0, 0, '', 'To Catch a Rat...'),
(15, 51690, 1, 0, 0, 48, 0, 80722, 1, 2, 0, 0, 0, '', 'both Scarlet Guards defeated'),
(15, 51690, 1, 0, 0, 48, 0, 80722, 2, 1, 1, 0, 0, '', 'not inspected yet'),
(22, 1, 90974, 0, 0, 47, 0, 80703, 8, 0, 0, 0, 0, '', 'Thandol Span in progress'),
(22, 1, 90974, 0, 0, 48, 0, 80703, 0, 1, 1, 0, 0, '', 'Vladeus not defeated yet'),
(22, 1, 90974, 0, 0, 29, 1, 50674, 40, 0, 1, 0, 0, '', 'no Vladeus around yet'),
(22, 22, 51567, 0, 0, 29, 1, 2425, 30, 0, 1, 0, 0, '', 'Varimathras not here yet'),
(22, 23, 51567, 0, 0, 2, 0, 53010, 1, 0, 1, 0, 0, '', 'player has no vial yet (event 22)');

-- texts
INSERT INTO `creature_text` (`CreatureID`, `GroupID`, `ID`, `Text`, `Type`, `Language`, `Probability`, `Emote`, `Duration`, `Sound`, `BroadcastTextId`, `TextRange`, `comment`) VALUES
(50674, 0, 0, 'Stop, I give up! Spare me, I will submit to imprisonment.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66177'),
(50674, 1, 0, 'For the Scarlet Crusade!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66178'),
(50674, 2, 0, 'I understand.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66179'),
(2104, 100, 0, 'Great find. My boys and I will put him up in chains. Go get yourself an ale while we handle this.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66180'),
(50676, 0, 0, 'Vladeus remains silent while slightly nodding his head, the nod is followed by a cough. You assume his throat was parched after being in chains for so long.', 16, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66948'),
(50676, 1, 0, 'Thank you, you\'re the one that captured me, right? I am grateful you spared my life but there\'s nothing I can tell you.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66950'),
(50676, 2, 0, 'A bit late for that don\'t you think? Since you took the life of the rest, I have nothing to tell you, the man in the red hood would return home and ki... I have said too much.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66952'),
(50676, 3, 0, 'Perhaps you are right. I didn\'t really want it to end this way, we were promised a better life, we... I... I didn\'t expect they\'d make me kill innocents, you have to believe me!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66954'),
(50676, 4, 0, 'I didn\'t see his face clearly, he was wearing a red hood and was simply laughing every few minutes. Looking back, it was the stupidest choice I have ever made. As to why they recruited us, I am not really sure. He said we would be taken to a hidden place of the Crusade to be trained, he was complaining that their number was low and since the death of two of their leaders they became broken. I think he mentioned a name, Aventis or Adentis?', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66956'),
(50676, 5, 0, 'Yes, that\'s the one! Please I don\'t know anything else, I wish to return home.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66958'),
(50676, 6, 0, 'Ugh, bastard! What was that for?', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66960'),
(50676, 7, 0, 'Vladeus grits his teeth.', 16, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66961'),
(50676, 8, 0, 'I won\'t te... tell you anything!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66963'),
(50676, 9, 0, 'Vladeus short speech is followed by a cough. You assume he must be thirsty after being chained for so long.', 16, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66964'),
(50676, 10, 0, 'I will say nothing to the one that murdered my companions!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66966'),
(50676, 11, 0, 'Stop! Please stop, I will talk. I didn\'t want it to end up this way, I swear! The Red Hooded man said if we don\'t comply he\'d kill my family, please, you have to understand!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66968'),
(50676, 12, 0, 'He... he said we were going to be taken to a hidden place to train. They were lacking numbers an- and since two of their leaders were dead they weren\'t doing very well. He also mentioned a name, Aventis or Adentis?', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66970'),
(50676, 13, 0, 'Yes, please, please. I don\'t know anything else.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66972'),
(50676, 14, 0, 'Vladeus is utterly terrified.', 16, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66973'),
(50676, 15, 0, 'Vladeus squeals in pain, so harshly it\'d be heard outside.', 16, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66975'),
(12336, 100, 0, 'Brigitte Abbendis is the daughter of the former High General Abbendis and utterly hates the undead, which is not a surprise when it comes to the Scarlet Crusade, I know.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66976'),
(12336, 101, 0, 'The issue is she\'d go to any length and I mean any to achieve this purpose, given what you told me and the fate of the other leaders she probably broke and went insane by now.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66977'),
(12336, 102, 0, 'Last I heard she was in Tyr\'s Hand, but if there\'s a secret training place or whatever that prisoner called it the only one to know about it would be her, an information passed down from the Ashbringer to her father and from her father to her.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66978'),
(12336, 103, 0, 'I am telling you, the Scarlet Crusade is indeed broken and we have seen better days but Abbendis will not stop at anything to take on the undead, be they Scourge or not.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66979'),
(1515, 100, 0, 'I don\'t know how you obtained that information but yes, some Scarlet Remnants attacked one of my Deathguard patrols, some never made it back and the others are in a deep sleep. Before falling into this weird slumber one of the guards said they were heading for the Monastery.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66941'),
(1952, 100, 0, 'A small force of the Scarlet Crusade has reached far enough into the forest to attack one of the patrols, we found only one lying about who had this strange ichor drooling out of his mouth. One of the other Deathguards touched it and soon fell into a deep slumber, one whose relative may be Death itself.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66942'),
(2215, 100, 0, 'Right on point, yes, our short numbers grew even shorter, we found no trail of their corpses yet we have found their weapons covered in mud yet no blood. It seems they didn\'t put up a fight.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66943'),
(51567, 0, 0, 'Let\'s bring demise upon these foolish zealots!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66982'),
(51567, 1, 0, 'A trap! It\'s a trap!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66983'),
(51567, 2, 0, 'I feel... weird.', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66984'),
(2425, 100, 0, 'He really is just unconscious, how strange...', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66985'),
(50680, 0, 0, 'For the Scarlet Crusade!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66181'),
(50682, 0, 0, 'For the Scarlet Crusade!', 12, 0, 100, 0, 0, 0, 0, 0, 'Turtle broadcast text 66181');

-- SmartAI
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
(341, 0, 100, 0, 62, 0, 100, 0, 41333, 0, 0, 0, 0, 0, 33, 50665, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Foreman Oslow - Gossip - Credit Young and Foolish'),
(956, 0, 100, 0, 62, 0, 100, 0, 41335, 1, 0, 0, 0, 0, 33, 50666, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Dorin Songblade - Gossip - Credit Young and Foolish'),
(344, 0, 100, 0, 62, 0, 100, 0, 41337, 0, 0, 0, 0, 0, 33, 50667, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Magistrate Solomon - Gossip - Credit Young and Foolish'),
(8305, 0, 100, 0, 62, 0, 100, 0, 41345, 0, 0, 0, 0, 0, 33, 50669, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Kixxle - Gossip - Credit Caravan Meets Caravan'),
(8305, 0, 101, 0, 2, 0, 100, 1, 0, 15, 0, 0, 0, 0, 25, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Kixxle - At 15% HP - Flee (Turtle EventAI)'),
(90974, 0, 0, 0, 10, 0, 100, 0, 2, 15, 60000, 60000, 1, 0, 80, 9097400, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Thandol Span Attack Trigger - Player with Thandol Span in LoS - Start ambush'),
(9097400, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 50673, 1, 60000, 1, 0, 0, 8, 0, 0, 0, 0, -2456.98, -2512.89, 78.508, 2.13, 'Thandol Span - Summon Scarlet Recruit 1'),
(9097400, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 50673, 1, 60000, 1, 0, 0, 8, 0, 0, 0, 0, -2457.73, -2493.79, 78.508, 4.19, 'Thandol Span - Summon Scarlet Recruit 2'),
(9097400, 9, 2, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 12, 50673, 1, 60000, 1, 0, 0, 8, 0, 0, 0, 0, -2456.98, -2512.89, 78.508, 2.13, 'Thandol Span - Summon Scarlet Recruit 3'),
(9097400, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 50673, 1, 60000, 1, 0, 0, 8, 0, 0, 0, 0, -2457.73, -2493.79, 78.508, 4.19, 'Thandol Span - Summon Scarlet Recruit 4'),
(9097400, 9, 4, 0, 0, 0, 100, 0, 15000, 15000, 0, 0, 0, 0, 12, 50674, 1, 3600000, 1, 0, 0, 8, 0, 0, 0, 0, -2457.73, -2493.79, 78.508, 4.19, 'Thandol Span - Summon Vladeus Springriver'),
(50673, 0, 0, 0, 0, 0, 100, 0, 4000, 6000, 7000, 9000, 0, 0, 11, 17149, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Recruit - In Combat - Cast 17149 (Turtle spell list 123520)'),
(50673, 0, 1, 0, 0, 0, 100, 0, 8000, 11000, 15000, 19000, 0, 0, 11, 13005, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Recruit - In Combat - Cast 13005 (Turtle spell list 123520)'),
(50673, 0, 2, 0, 54, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 21, 40, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Recruit - On Summoned - Attack closest player'),
(50674, 0, 0, 0, 0, 0, 100, 0, 4000, 6000, 7000, 9000, 0, 0, 11, 17149, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - In Combat - Cast 17149 (Turtle spell list 123520)'),
(50674, 0, 1, 0, 0, 0, 100, 0, 8000, 11000, 15000, 19000, 0, 0, 11, 13005, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - In Combat - Cast 13005 (Turtle spell list 123520)'),
(50674, 0, 2, 0, 25, 0, 100, 0, 0, 0, 0, 0, 0, 0, 42, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - On Spawn - Cannot drop below 10%'),
(50674, 0, 3, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - On Aggro - Say'),
(50674, 0, 4, 0, 54, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 21, 40, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - On Summoned - Attack closest player'),
(50674, 0, 5, 6, 2, 0, 100, 1, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - At 10% HP - Say (gives up)'),
(50674, 0, 6, 7, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50670, 0, 0, 0, 0, 0, 24, 0, 1, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - At 10% HP - Credit players on his threat list'),
(50674, 0, 7, 8, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 35, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - At 10% HP - Friendly'),
(50674, 0, 8, 9, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - At 10% HP - Stop combat'),
(50674, 0, 9, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - At 10% HP - Passive'),
(50674, 0, 10, 11, 62, 0, 100, 0, 51683, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip - Say'),
(50674, 0, 11, 12, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 29, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip - Follow the player'),
(50674, 0, 12, 13, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 59, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip - Run'),
(50674, 0, 13, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip - Close'),
(2104, 0, 100, 101, 62, 0, 100, 0, 11499, 50, 0, 0, 0, 0, 33, 50671, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Captain Stoutfist - Gossip - Credit Thandol Span'),
(2104, 0, 101, 102, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Captain Stoutfist - Gossip - Say'),
(2104, 0, 102, 103, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 41, 2000, 0, 0, 0, 0, 0, 19, 50674, 30, 0, 0, 0, 0, 0, 0, 'Captain Stoutfist - Gossip - Vladeus is taken away'),
(2104, 0, 103, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Captain Stoutfist - Gossip - Close'),
(50676, 0, 0, 0, 62, 0, 100, 0, 51684, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 51684/0 (quest 80705) - Emote'),
(50676, 0, 1, 0, 62, 0, 100, 0, 9080001, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080001/0 (quest 80705) - Say'),
(50676, 0, 2, 3, 62, 0, 100, 0, 9080002, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080002/0 (quest 80705) - Cry'),
(50676, 0, 3, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080002/0 (quest 80705) - Say'),
(50676, 0, 4, 0, 62, 0, 100, 0, 9080003, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080003/0 (quest 80705) - Say'),
(50676, 0, 5, 0, 62, 0, 100, 0, 9080004, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080004/0 (quest 80705) - Say'),
(50676, 0, 6, 7, 62, 0, 100, 0, 9080005, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080005/0 (quest 80705) - Cry'),
(50676, 0, 7, 8, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080005/0 (quest 80705) - Say'),
(50676, 0, 8, 9, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50675, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080005/0 (quest 80705) - Credit interrogation'),
(50676, 0, 9, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080005/0 (quest 80705) - Close'),
(50676, 0, 10, 11, 62, 0, 100, 0, 51684, 1, 0, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 51684/1 (quest 80706) - Say'),
(50676, 0, 11, 12, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 51684/1 (quest 80706) - Emote'),
(50676, 0, 12, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 51684/1 (quest 80706) - Cry'),
(50676, 0, 13, 14, 62, 0, 100, 0, 9080011, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080011/0 (quest 80706) - Say'),
(50676, 0, 14, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 9, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080011/0 (quest 80706) - Emote'),
(50676, 0, 15, 16, 62, 0, 100, 0, 9080012, 0, 0, 0, 0, 0, 1, 10, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080012/0 (quest 80706) - Say'),
(50676, 0, 16, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080012/0 (quest 80706) - Cry'),
(50676, 0, 17, 18, 62, 0, 100, 0, 9080013, 0, 0, 0, 0, 0, 1, 11, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080013/0 (quest 80706) - Say'),
(50676, 0, 18, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 20, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080013/0 (quest 80706) - Beg'),
(50676, 0, 19, 0, 62, 0, 100, 0, 9080014, 0, 0, 0, 0, 0, 1, 12, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080014/0 (quest 80706) - Say'),
(50676, 0, 20, 21, 62, 0, 100, 0, 9080015, 0, 0, 0, 0, 0, 1, 13, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080015/0 (quest 80706) - Say'),
(50676, 0, 21, 22, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 14, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080015/0 (quest 80706) - Emote'),
(50676, 0, 22, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080015/0 (quest 80706) - Cry'),
(50676, 0, 23, 24, 62, 0, 100, 0, 9080016, 0, 0, 0, 0, 0, 1, 15, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080016/0 (quest 80706) - Emote'),
(50676, 0, 24, 25, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080016/0 (quest 80706) - Cry'),
(50676, 0, 25, 26, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50675, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080016/0 (quest 80706) - Credit interrogation'),
(50676, 0, 26, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Vladeus Springriver - Gossip 9080016/0 (quest 80706) - Close'),
(50677, 0, 0, 0, 0, 0, 100, 0, 3000, 5000, 15000, 20000, 0, 0, 11, 9128, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Mavel Brightwood - In Combat - Cast 9128 (Turtle spell list 108280)'),
(50677, 0, 1, 0, 0, 0, 100, 0, 10000, 13000, 20000, 30000, 0, 0, 11, 13730, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Mavel Brightwood - In Combat - Cast 13730 (Turtle spell list 108280)'),
(50677, 0, 2, 0, 0, 0, 100, 0, 5000, 7000, 6000, 9000, 0, 0, 11, 17143, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Mavel Brightwood - In Combat - Cast 17143 (Turtle spell list 108280)'),
(12336, 0, 100, 0, 20, 0, 100, 0, 80708, 0, 0, 0, 0, 0, 80, 1233600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - On Scarlet Aid Rewarded - Tell about Abbendis'),
(1233600, 9, 0, 0, 0, 0, 100, 0, 2000, 2000, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - Abbendis line 1'),
(1233600, 9, 1, 0, 0, 0, 100, 0, 8000, 8000, 0, 0, 0, 0, 1, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - Abbendis line 2'),
(1233600, 9, 2, 0, 0, 0, 100, 0, 8000, 8000, 0, 0, 0, 0, 1, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - Abbendis line 3'),
(1233600, 9, 3, 0, 0, 0, 100, 0, 10000, 10000, 0, 0, 0, 0, 1, 103, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - Abbendis line 4'),
(1233600, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Brother Crowley - Question emote'),
(1515, 0, 100, 101, 62, 0, 100, 0, 9080030, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Executor Zygand - Gossip - Say'),
(1515, 0, 101, 102, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50665, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Executor Zygand - Gossip - Credit Grim News'),
(1515, 0, 102, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Executor Zygand - Gossip - Close'),
(1952, 0, 100, 101, 62, 0, 100, 0, 9080031, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Hadrec - Gossip - Say'),
(1952, 0, 101, 102, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50666, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Hadrec - Gossip - Credit Grim News'),
(1952, 0, 102, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Hadrec - Gossip - Close'),
(2215, 0, 100, 101, 62, 0, 100, 0, 11886, 50, 0, 0, 0, 0, 5, 25, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Darthalia - Gossip - Point'),
(2215, 0, 101, 102, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Darthalia - Gossip - Say'),
(2215, 0, 102, 103, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50667, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Darthalia - Gossip - Credit Grim News'),
(2215, 0, 103, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'High Executor Darthalia - Gossip - Close'),
(51567, 0, 0, 0, 0, 0, 100, 0, 0, 0, 2000, 4000, 0, 0, 11, 6660, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - In Combat - Cast 6660 (Turtle spell list 130760)'),
(51567, 0, 10, 11, 62, 0, 100, 0, 51690, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Gossip - Say'),
(51567, 0, 11, 12, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 50668, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Gossip - Credit'),
(51567, 0, 12, 13, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Gossip - Close'),
(51567, 0, 13, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 80, 5156700, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Gossip - Start the trap'),
(5156700, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 91, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Stand up'),
(5156700, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 28, 25148, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Remove sleep visual'),
(5156700, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 18, 33554944, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Not selectable, immune to NPCs'),
(5156700, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Walk'),
(5156700, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 69, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 2545.8, -651.11, 78.8, 0, 'Maverick - Walk to the trap spot'),
(5156700, 9, 5, 0, 0, 0, 100, 0, 40000, 40000, 0, 0, 0, 0, 12, 50680, 2, 60000, 0, 0, 0, 8, 0, 0, 0, 0, 2552.95, -650.62, 80.09, 3.2, 'Maverick - Summon Scarlet Magician'),
(5156700, 9, 6, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 50, 2005011, 100, 0, 1, 0, 0, 8, 0, 0, 0, 0, 2545.8, -651.11, 78.8, 0, 'Maverick - Summon rune'),
(5156700, 9, 7, 0, 0, 0, 100, 0, 1000, 1000, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Say (trap)'),
(5156700, 9, 8, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 50680, 2, 60000, 0, 0, 0, 8, 0, 0, 0, 0, 2544.84, -658.78, 79.53, 1.5, 'Maverick - Summon Scarlet Magician'),
(5156700, 9, 9, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Say (weird)'),
(5156700, 9, 10, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 25148, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Sleep visual'),
(5156700, 9, 11, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 90, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Fall asleep'),
(5156700, 9, 12, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 12, 50682, 2, 120000, 0, 0, 0, 8, 0, 0, 0, 0, 2558.14, -663.63, 88.68, 2.19, 'Maverick - Summon Scarlet Alchemist'),
(5156700, 9, 13, 0, 0, 0, 100, 0, 9000, 9000, 0, 0, 0, 0, 12, 50681, 2, 60000, 0, 0, 0, 8, 0, 0, 0, 0, 2544.84, -658.78, 79.53, 1.5, 'Maverick - Summon Scarlet Guard'),
(5156700, 9, 14, 0, 0, 0, 100, 0, 1000, 1000, 0, 0, 0, 0, 12, 50681, 2, 60000, 0, 0, 0, 8, 0, 0, 0, 0, 2546.42, -643.44, 80.2, 4.6, 'Maverick - Summon Scarlet Guard'),
(5156700, 9, 15, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 33554432, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Selectable again (to be inspected)'),
(5156700, 9, 16, 0, 0, 0, 100, 0, 180000, 180000, 0, 0, 0, 0, 91, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Wake up after 3 minutes'),
(5156700, 9, 17, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 28, 25148, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Remove sleep visual'),
(5156700, 9, 18, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 19, 512, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Normal flags'),
(5156700, 9, 19, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Maverick - Walk back to his post'),
(51567, 0, 20, 0, 62, 0, 100, 0, 51690, 1, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Inspect - Close'),
(51567, 0, 21, 0, 62, 0, 100, 0, 51690, 1, 0, 0, 0, 0, 12, 2425, 3, 180000, 0, 0, 0, 8, 0, 0, 0, 0, 2552.95, -650.62, 80.09, 3.2, 'Deathguard Maverick - Inspect - Varimathras arrives'),
(51567, 0, 22, 23, 62, 0, 100, 0, 51690, 1, 0, 0, 0, 0, 33, 50670, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Inspect - Credit'),
(51567, 0, 23, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 56, 53010, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Deathguard Maverick - Inspect - Vial of Mysterious Concoction'),
(2425, 0, 100, 0, 54, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Varimathras - On Summoned (To Catch a Rat...) - Say'),
(50680, 0, 0, 0, 0, 0, 100, 0, 4000, 6000, 7000, 9000, 0, 0, 11, 17149, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Magician - In Combat - Cast 17149 (Turtle spell list 123520)'),
(50680, 0, 1, 0, 0, 0, 100, 0, 8000, 11000, 15000, 19000, 0, 0, 11, 13005, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Magician - In Combat - Cast 13005 (Turtle spell list 123520)'),
(50680, 0, 2, 0, 25, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 23017, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Magician - On Spawn - Channel'),
(50680, 0, 3, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Magician - On Aggro - Say'),
(50682, 0, 0, 0, 0, 0, 100, 0, 4000, 6000, 7000, 9000, 0, 0, 11, 17149, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Alchemist - In Combat - Cast 17149 (Turtle spell list 123520)'),
(50682, 0, 1, 0, 0, 0, 100, 0, 8000, 11000, 15000, 19000, 0, 0, 11, 13005, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Alchemist - In Combat - Cast 13005 (Turtle spell list 123520)'),
(50682, 0, 2, 0, 25, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 13540, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Alchemist - On Spawn - Channel'),
(50682, 0, 3, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Alchemist - On Aggro - Say'),
(50681, 0, 0, 0, 0, 0, 100, 0, 4000, 6000, 7000, 9000, 0, 0, 11, 17149, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Guard - In Combat - Cast 17149 (Turtle spell list 123520)'),
(50681, 0, 1, 0, 0, 0, 100, 0, 8000, 11000, 15000, 19000, 0, 0, 11, 13005, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'Scarlet Guard - In Combat - Cast 13005 (Turtle spell list 123520)');
