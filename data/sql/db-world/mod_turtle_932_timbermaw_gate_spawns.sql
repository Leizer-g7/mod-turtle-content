-- mod-turtle-content 932: Timbermaw tunnel (fix #6) - 3 stock furbolgs at the Azshara gate back on the ground (Claude, 2026-10-14).
-- Turtle's terrain (Kalimdor_41_24) is ~4 yd higher than stock 3.3.5 here, so these 3.3.5 spawns were under the ground.
-- Approved by Max 2026-10-14. Only position_z of these 3 rows changes. Ground heights read from the server (.gps) after fix #6. Safe to run again.
UPDATE `creature` SET `position_z`=122.3 WHERE `guid`=35249;
UPDATE `creature` SET `position_z`=121.8 WHERE `guid`=35257;
UPDATE `creature` SET `position_z`=122.9 WHERE `guid`=35277;
