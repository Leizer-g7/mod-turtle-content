-- mod-turtle-content 926: coexistence fixes found by comparing stock AzerothCore with the module installed.
--
-- 1) Lorekeeper Lydros (14368, Dire Maul) gives "A Dull and Flat Elven Blade" (18513) for the Quel'Serrar
--    chain when the player picks "Maybe... What do I do now?" on stock gossip menu 60045.
--    mod_turtle_012_wetlands put a Turtle text (52119) on menu 60045 and the stock option was deleted,
--    so the chain stopped at "Eh?" and the blade could not be obtained. No Turtle NPC uses menu 60045.
DELETE FROM `gossip_menu` WHERE `MenuID`=60045 AND `TextID`=52119;
DELETE FROM `gossip_menu` WHERE `MenuID`=60045 AND `TextID`=60045;
INSERT INTO `gossip_menu` (`MenuID`, `TextID`) VALUES (60045, 60045);
DELETE FROM `gossip_menu_option` WHERE `MenuID`=60045 AND `OptionID`=0;
INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, `OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) VALUES
(60045, 0, 0, 'Maybe... What do I do now?', 0, 1, 3, 0, 0, 0, 0, NULL, 0, 0);

-- 2) Three stock herb/ore nodes the module raised above the 3.3.5 ground (checked with .gps on the test server).
UPDATE `gameobject` SET `position_z`=406.9 WHERE `guid`=205235;
UPDATE `gameobject` SET `position_z`=428.1 WHERE `guid`=205392;
UPDATE `gameobject` SET `position_z`=33.5 WHERE `guid`=214229;
