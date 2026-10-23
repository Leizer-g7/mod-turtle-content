-- mod-turtle-content 931: remove the Turtle "Enough!" voice from 3 stock WotLK creatures (Claude, 2026-10-13).
-- SQL 929 matched Walgan's "Enough!" (sound 60667) by text and also gave it to these 3.3.5 creatures by mistake.
-- Approved by Max 2026-10-13. Only these 3 rows change; Walgan (62784) keeps his voice. Safe to run again.
UPDATE `creature_text` SET `Sound`=0 WHERE `Sound`=60667 AND `CreatureID` IN (1840,28996,30396);
