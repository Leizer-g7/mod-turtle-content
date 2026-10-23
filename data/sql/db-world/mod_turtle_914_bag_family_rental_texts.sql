-- mod-turtle-content: bag types + rental mount texts (Max + Claude, 2026-10-12)
-- 1. Turtle stores the bag type as a number (9 = keys); 3.3.5 uses bit flags (256 = keyring).
--    The converter copied Turtle's number, so these items could not go on the keyring or in the right
--    profession bag. Same mapping as the converter now uses (tools/turtle2ac/build.py BAG_FAMILY).
UPDATE `item_template` SET `BagFamily` = 256  WHERE `BagFamily` = 9  AND `entry` IN (60302, 1041676, 1041876, 1041913); -- Lapidis Tower Key, Winery Key, Lower Reserve Key, Key to Stormwrought Castle -> keyring
UPDATE `item_template` SET `BagFamily` = 8    WHERE `BagFamily` = 12 AND `entry` = 1042215;  -- Hydra Leather -> leatherworking bags
UPDATE `item_template` SET `BagFamily` = 1024 WHERE `BagFamily` = 13 AND `entry` = 81094;    -- Amber Topaz -> mining bags
-- 2. Gossip texts of the rental wolves (90368) and skeletal horses (90369), used by src/bosses/zone_northwind.cpp.
--    Turtle npc_text / broadcast_text 90368, 90369. The NPCs themselves come with their zones.
DELETE FROM `npc_text` WHERE `ID` IN (90368, 90369);
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`) VALUES
(90368, 'The wolf scratches the ground looking for something. As you approach, it looks up. A new smell has caught its attention.', 'The wolf scratches the ground looking for something. As you approach, it looks up. A new smell has caught its attention.', 0, 0, 1),
(90369, 'The horse, despite being an undead creature, seems to be aware of your motion.', 'The horse, despite being an undead creature, seems to be aware of your motion.', 0, 0, 1);
