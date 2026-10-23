-- mod-turtle-content: fixes from merging the friend's 2026-10-12 build (Teldrassil .. Wailing Caverns) into Max's module.
-- Meaty Strider Leg (Moonwhisper Coast) kept Turtle's bag family number 10 (cooking meat), which 3.3.5 reads as a bit mask
-- (ammo pouch + leatherworking bag). 3.3.5 has no meat bag, so it gets none. The converter has the mapping again (tools\turtle2ac\build.py).
UPDATE `item_template` SET `BagFamily` = 0 WHERE `entry` = 1042010 AND `BagFamily` = 10;
