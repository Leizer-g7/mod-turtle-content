-- 2026-10-12 (merge of the friend's Westfall..Wailing Caverns build): re-run on purpose. His changed 000/006/007/027/032 run again, and without this line they would undo the fixes in this file. Same content as before, safe to run twice.
-- mod-turtle-content: 20-30 zone NPC scripts (Max + Claude, 2026-10-11)
-- Northwind rental horses (White Stallion 51560, Palomino 51561): the horse's gossip text.
-- Turtle npc_text 90365 / broadcast_text 90365. The C++ in src/bosses/zone_northwind.cpp shows it.
DELETE FROM `npc_text` WHERE `ID` = 90365;
INSERT INTO `npc_text` (`ID`, `text0_0`, `text0_1`, `BroadcastTextID0`, `lang0`, `Probability0`) VALUES
(90365, '<The horse seems to like you.>', '<The horse seems to like you.>', 0, 0, 1);
