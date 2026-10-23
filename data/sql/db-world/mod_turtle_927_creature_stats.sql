-- mod-turtle-content 927: creature stat fixes found while testing Hateforge Quarry on the cloud test server (Claude, 2026-10-13).
-- Safe to run again: each row only changes while it still has the old values. Rollback: old values are in each line's comment.
--
-- A) Turtle's dmg_min/dmg_max are already the final melee damage, but the port also multiplied by Turtle's
--    dmg_multiplier. Checked against stock bosses Turtle shares with AzerothCore (General Angerforge: Turtle
--    729-967 with multiplier 6.5, stock AzerothCore 578-766), so the multiplier must not be applied again.
--    Example: Har'gesh Doomcaller hit for about 6700-8900 instead of Turtle's 997-1363.
UPDATE `creature_template` SET `DamageModifier`=9.995 WHERE `entry`=49002 AND ABS(`DamageModifier`-19.991)<0.01; -- Blademaster Kargron (was 19.991, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=3.41 WHERE `entry`=50002 AND ABS(`DamageModifier`-6.82)<0.01; -- Professor Malkovich (was 6.82, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=3.41 WHERE `entry`=50004 AND ABS(`DamageModifier`-6.82)<0.01; -- Professor Papucho (was 6.82, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=4.064 WHERE `entry`=50006 AND ABS(`DamageModifier`-8.129)<0.01; -- Suspicious Defias Footpad (was 8.129, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=2.116 WHERE `entry`=50007 AND ABS(`DamageModifier`-4.232)<0.01; -- Suspicious Dark Iron Dwarf (was 4.232, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=4.064 WHERE `entry`=50008 AND ABS(`DamageModifier`-8.129)<0.01; -- Suspicious Southsea Pirate (was 8.129, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=1.849 WHERE `entry`=50011 AND ABS(`DamageModifier`-3.698)<0.01; -- Suspicious Syndicate Highwayman (was 3.698, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=6.272 WHERE `entry`=50523 AND ABS(`DamageModifier`-11.916)<0.01; -- Race Spectator (was 11.916, Turtle multiplier 1.9)
UPDATE `creature_template` SET `DamageModifier`=6.272 WHERE `entry`=50524 AND ABS(`DamageModifier`-11.916)<0.01; -- Race Spectator (was 11.916, Turtle multiplier 1.9)
UPDATE `creature_template` SET `DamageModifier`=6.272 WHERE `entry`=50525 AND ABS(`DamageModifier`-11.916)<0.01; -- Race Spectator (was 11.916, Turtle multiplier 1.9)
UPDATE `creature_template` SET `DamageModifier`=6.272 WHERE `entry`=50526 AND ABS(`DamageModifier`-11.916)<0.01; -- Race Spectator (was 11.916, Turtle multiplier 1.9)
UPDATE `creature_template` SET `DamageModifier`=21.077 WHERE `entry`=60596 AND ABS(`DamageModifier`-42.154)<0.01; -- Runic Construct (was 42.154, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=11.292 WHERE `entry`=60737 AND ABS(`DamageModifier`-73.398)<0.01; -- Har'gesh Doomcaller (was 73.398, Turtle multiplier 6.5)
UPDATE `creature_template` SET `DamageModifier`=10.98 WHERE `entry`=61352 AND ABS(`DamageModifier`-21.961)<0.01; -- Enduring Doomguard (was 21.961, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=9.56 WHERE `entry`=61356 AND ABS(`DamageModifier`-19.12)<0.01; -- Shadeflayer Berserker (was 19.12, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=9.861 WHERE `entry`=61423 AND ABS(`DamageModifier`-19.721)<0.01; -- Marshal Magnus Greystone (was 19.721, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=11.434 WHERE `entry`=61533 AND ABS(`DamageModifier`-22.867)<0.01; -- Shadeflayer Goliath (was 22.867, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=13.825 WHERE `entry`=61556 AND ABS(`DamageModifier`-27.65)<0.01; -- Larannikus (was 27.65, Turtle multiplier 2.0)
UPDATE `creature_template` SET `DamageModifier`=12.225 WHERE `entry`=80852 AND ABS(`DamageModifier`-41.566)<0.01; -- Tham'Grarr (was 41.566, Turtle multiplier 3.4)

-- B) Turtle gives these creatures mana while their class is warrior or rogue. In AzerothCore those classes
--    have no mana, so every spell with a mana cost fails (seen: Hateforge Cleric never cast Immolate or
--    Greater Heal). Only creatures that cast spells (SmartAI or C++) are changed. Class becomes paladin (2) with health, armor and melee damage rescaled so they stay the
--    same, and mana set to Turtle's value.
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=11.574, `ManaModifier`=4.573, `ArmorModifier`=0.933, `DamageModifier`=2.71 WHERE `entry`=49005 AND `unit_class`=1; -- Grug'thok the Seer (Turtle mana 7500; was class 1, HP 9.259, Armor 0.932, Dmg 2.53)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=1.745, `ManaModifier`=0.443, `ArmorModifier`=0.844, `DamageModifier`=1.6 WHERE `entry`=60713 AND `unit_class`=1; -- Peculiar Broodling (Turtle mana 800; was class 1, HP 1.396, Armor 0.843, Dmg 1.489)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=9.773, `ManaModifier`=0.468, `ArmorModifier`=0.792, `DamageModifier`=3.929 WHERE `entry`=60715 AND `unit_class`=1; -- 'Broody' (Turtle mana 900; was class 1, HP 7.819, Armor 0.795, Dmg 3.658)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=3.472, `ManaModifier`=1.127, `ArmorModifier`=0.74, `DamageModifier`=3.989 WHERE `entry`=60718 AND `unit_class`=1; -- Hateforge Cleric (Turtle mana 2100; was class 1, HP 2.778, Armor 0.74, Dmg 3.713)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=5.213, `ManaModifier`=5.049, `ArmorModifier`=0.855, `DamageModifier`=3.084 WHERE `entry`=62056 AND `unit_class`=1; -- Bogpaw Truthsay (Turtle mana 3499; was class 1, HP 4.525, Armor 0.854, Dmg 2.869)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=14.285, `ManaModifier`=15.497, `ArmorModifier`=0.734, `DamageModifier`=6.449 WHERE `entry`=62673 AND `unit_class`=1; -- Mergothid (Turtle mana 19883; was class 1, HP 11.492, Armor 0.734, Dmg 6.003)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=3.699, `ManaModifier`=8.719, `ArmorModifier`=2.162, `DamageModifier`=5.002 WHERE `entry`=62742 AND `unit_class`=1; -- Enraged Sea Elemental (Turtle mana 9303; was class 1, HP 3.059, Armor 2.162, Dmg 4.653)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=3.494, `ManaModifier`=2.716, `ArmorModifier`=0.731, `DamageModifier`=3.923 WHERE `entry`=62770 AND `unit_class`=1; -- Blackwind Earthkeeper (Turtle mana 1988; was class 1, HP 3.014, Armor 0.731, Dmg 3.65)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=4.545, `ManaModifier`=1.07, `ArmorModifier`=0.905, `DamageModifier`=7.367 WHERE `entry`=62774 AND `unit_class`=1; -- Deathtotem Bonespeaker (Turtle mana 809; was class 1, HP 3.9, Armor 0.904, Dmg 6.896)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=17.298, `ManaModifier`=3.29, `ArmorModifier`=1.142, `DamageModifier`=7.106 WHERE `entry`=62778 AND `unit_class`=1; -- Ahgk'tos the Pure (Turtle mana 2033; was class 1, HP 15.172, Armor 1.142, Dmg 6.608)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=17.273, `ManaModifier`=8.061, `ArmorModifier`=1.762, `DamageModifier`=6.617 WHERE `entry`=62780 AND `unit_class`=1; -- Bonespeaker Narlgom (Turtle mana 5901; was class 1, HP 14.898, Armor 1.762, Dmg 6.156)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=46.914, `ManaModifier`=3.04, `ArmorModifier`=1.004, `DamageModifier`=9.667 WHERE `entry`=62832 AND `unit_class`=1; -- Avranagos (Turtle mana 7400; was class 1, HP 37.537, Armor 1.003, Dmg 9.001)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=9.498, `ManaModifier`=2.93, `ArmorModifier`=1.013, `DamageModifier`=3.747 WHERE `entry`=63068 AND `unit_class`=1; -- Arch Druid Mothshroud (Turtle mana 6940; was class 1, HP 7.599, Armor 1.012, Dmg 3.488)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=3.62, `ManaModifier`=1.852, `ArmorModifier`=0.901, `DamageModifier`=4.318 WHERE `entry`=63139 AND `unit_class`=1; -- Frostmane Pathfinder (Turtle mana 489; was class 1, HP 3.355, Armor 0.901, Dmg 4.012)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=13.609, `ManaModifier`=3.249, `ArmorModifier`=0.943, `DamageModifier`=13.021 WHERE `entry`=80851 AND `unit_class`=1; -- Volkan Cruelblade (Turtle mana 8343; was class 1, HP 10.889, Armor 0.942, Dmg 12.113)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=12.546, `ManaModifier`=4.378, `ArmorModifier`=0.96, `DamageModifier`=7.495 WHERE `entry`=92111 AND `unit_class`=1; -- Fenektis the Deceiver (Turtle mana 5000; was class 1, HP 10.264, Armor 0.959, Dmg 6.973)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=1.614, `ManaModifier`=2.139, `ArmorModifier`=0.642, `DamageModifier`=2.445 WHERE `entry`=92113 AND `unit_class`=1; -- Grove Sprite Corruptor (Turtle mana 2000; was class 1, HP 1.356, Armor 0.641, Dmg 2.273)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=4.924, `ManaModifier`=0.348, `ArmorModifier`=0.807, `DamageModifier`=9.062 WHERE `entry`=92117 AND `unit_class`=1; -- Deranged Ancient (Turtle mana 350; was class 1, HP 4.094, Armor 0.806, Dmg 8.429)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=5.391, `ManaModifier`=8.434, `ArmorModifier`=1.456, `DamageModifier`=5.561 WHERE `entry`=92120 AND `unit_class`=1; -- Roaming Felguard (Turtle mana 8999; was class 1, HP 4.459, Armor 1.456, Dmg 5.173)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=4.738, `ManaModifier`=6.231, `ArmorModifier`=1.491, `DamageModifier`=5.508 WHERE `entry`=92123 AND `unit_class`=1; -- Blacktalon Trickster (Turtle mana 6000; was class 1, HP 3.961, Armor 1.491, Dmg 5.122)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=3.893, `ManaModifier`=0.328, `ArmorModifier`=0.787, `DamageModifier`=8.66 WHERE `entry`=92127 AND `unit_class`=1; -- Twisted Ancient (Turtle mana 350; was class 1, HP 3.22, Armor 0.787, Dmg 8.055)
UPDATE `creature_template` SET `unit_class`=2, `HealthModifier`=9.572, `ManaModifier`=0.779, `ArmorModifier`=1.014, `DamageModifier`=7.045 WHERE `entry`=92133 AND `unit_class`=1; -- Inuvias Brightlance (Turtle mana 1000; was class 1, HP 7.7, Armor 1.013, Dmg 6.557)
