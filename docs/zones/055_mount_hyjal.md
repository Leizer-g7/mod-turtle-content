# Mount Hyjal

File: `data/sql/db-world/mod_turtle_011_mount_hyjal.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 12
- conditions: 2
- creature: 748
- creature_addon: 52
- creature_equip_template: 24
- creature_loot_template: 5832
- creature_questender: 64
- creature_queststarter: 64
- creature_template: 91
- creature_template_addon: 4
- creature_template_model: 101
- creature_template_movement: 91
- creature_template_resistance: 22
- gameobject: 481
- gameobject_loot_template: 2
- gameobject_template: 16
- gameobject_template_addon: 4
- gossip_menu: 43
- gossip_menu_option: 10
- npc_text: 43
- npc_vendor: 99
- pickpocketing_loot_template: 4
- pool_gameobject: 223
- pool_pool: 60
- pool_template: 62
- quest_offer_reward: 66
- quest_request_items: 66
- quest_template: 66
- quest_template_addon: 66
- skinning_loot_template: 4
- smart_scripts: 68
- waypoint_data: 385

## Client tiles (23)

- 24 reshaped chunks next to the zone taken (keep their 3.3.5 area); 30 reshaped chunks away from the zone left as 3.3.5
- 153 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 12 edge points aligned (largest step 0.08 yd)
- Kalimdor_34_21: merged - 60 of 256 chunks from Turtle (1 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_34_22: merged - 222 of 256 chunks from Turtle
- Kalimdor_34_23: merged - 65 of 256 chunks from Turtle
- Kalimdor_35_21: merged - 256 of 256 chunks from Turtle
- Kalimdor_35_22: merged - 256 of 256 chunks from Turtle
- Kalimdor_35_23: merged - 213 of 256 chunks from Turtle
- Kalimdor_36_21: merged - 256 of 256 chunks from Turtle
- Kalimdor_36_22: merged - 256 of 256 chunks from Turtle
- Kalimdor_36_23: merged - 256 of 256 chunks from Turtle
- Kalimdor_37_21: merged - 256 of 256 chunks from Turtle
- Kalimdor_37_22: merged - 256 of 256 chunks from Turtle
- Kalimdor_37_23: merged - 256 of 256 chunks from Turtle
- Kalimdor_37_24: merged - 57 of 256 chunks from Turtle
- Kalimdor_38_21: merged - 256 of 256 chunks from Turtle
- Kalimdor_38_22: merged - 256 of 256 chunks from Turtle
- Kalimdor_38_23: merged - 237 of 256 chunks from Turtle (5 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_38_24: merged - 13 of 256 chunks from Turtle (10 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_39_21: merged - 190 of 256 chunks from Turtle
- Kalimdor_39_22: merged - 182 of 256 chunks from Turtle
- Kalimdor_39_23: merged - 65 of 256 chunks from Turtle (8 of them reshaped ground that keeps its 3.3.5 area)

## Client assets (1)

- 14 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (13)

- 5212 Bleakhollow Crater (subzone of 616, map 1, exploration bit 3750, level 60)
- 5213 Nordrassil Glade (subzone of 616, map 1, exploration bit 3751, level 60)
- 5214 Nordanaar (subzone of 616, map 1, exploration bit 3752, level 60)
- 5215 Barkskin Plateau (subzone of 616, map 1, exploration bit 3753, level 60)
- 5216 Barkskin Village (subzone of 616, map 1, exploration bit 3754, level 60)
- 5217 Circle of Power (subzone of 616, map 1, exploration bit 3755, level 60)
- 5218 The Ruins of Telennas (subzone of 616, map 1, exploration bit 3756, level 60)
- 5219 Zul'Hatha (subzone of 616, map 1, exploration bit 3757, level 60)
- 5220 Darkhollow Pass (subzone of 616, map 1, exploration bit 3758, level 60)
- 5221 The Emerald Gateway (subzone of 616, map 1, exploration bit 3759, level 60)
- 5222 Darkroot Cave (subzone of 616, map 1, exploration bit 3760, level 60)
- 5223: Turtle gives map 0, its zone 616 is on map 1 - map 1 used
- 5223 Barkskin Hold (subzone of 616, map 1, exploration bit 3761, level 60)

## Existing templates (2)

- 140 creature spawns of 5 templates 3.3.5 already has (AzerothCore's template is used)
- 232 object spawns of 13 templates 3.3.5 already has (herbs, ore, chests ...)

## Zone quests elsewhere (1)

- quest 41092: given and turned in outside the zone ([60710] / [60710])

## Cpp script (5)

- 61326 Ralathius: Turtle C++ script 'npc_ralathius' (see manual/055_mount_hyjal.sql)
- 61497 Loremaster Taerlon: Turtle C++ script 'npc_loremaster_taerlon' (see manual/055_mount_hyjal.sql)
- 61512 Arch Druid Dreamwind: Turtle C++ script 'npc_arch_druid_dreamwind' (see manual/055_mount_hyjal.sql)
- 61561 Buthok Cloudhorn: Turtle C++ script 'npc_buthok_cloudhorn' (see manual/055_mount_hyjal.sql)
- 61988 Dissipating Spectre: Turtle C++ script 'npc_dissipating_spectre' (see manual/055_mount_hyjal.sql)

## Trainer (21)

- 61332 Misthoof Stag: Turtle trainer rows but no trainer flag - not a trainer
- 61333 Misthoof Sprinter: Turtle trainer rows but no trainer flag - not a trainer
- 61334 Repulsing Ooze: Turtle trainer rows but no trainer flag - not a trainer
- 61335 Verdant Ooze: Turtle trainer rows but no trainer flag - not a trainer
- 61336 Greathorn Owl: Turtle trainer rows but no trainer flag - not a trainer
- 61337 Greathorn Hunter: Turtle trainer rows but no trainer flag - not a trainer
- 61339 Vilemusk Felsworn: Turtle trainer rows but no trainer flag - not a trainer
- 61340 Vilemusk Shadowstalker: Turtle trainer rows but no trainer flag - not a trainer
- 61341 Vilemusk Hellcaller: Turtle trainer rows but no trainer flag - not a trainer
- 61343 Barkskin Pathfinder: Turtle trainer rows but no trainer flag - not a trainer
- 61344 Barkskin Avenger: Turtle trainer rows but no trainer flag - not a trainer
- 61345 Barkskin Gardener: Turtle trainer rows but no trainer flag - not a trainer
- 61346 Barkskin Den Watcher: Turtle trainer rows but no trainer flag - not a trainer
- 61347 Barkskin Windtalker: Turtle trainer rows but no trainer flag - not a trainer
- 61349 Relentless Infernal: Turtle trainer rows but no trainer flag - not a trainer
- 61350 Relentless Temptress: Turtle trainer rows but no trainer flag - not a trainer
- 61354 Mana Stalker: Turtle trainer rows but no trainer flag - not a trainer
- 61367 Shadeflayer Troll: Turtle trainer rows but no trainer flag - not a trainer
- 61561 Buthok Cloudhorn: Turtle trainer rows but no trainer flag - not a trainer
- 61562 Farana Leafblade: Turtle trainer rows but no trainer flag - not a trainer
- 61563 Arayna Softwind: Turtle trainer rows but no trainer flag - not a trainer

## Spell sub (3)

- Vilemusk Felsworn: spell 10876 Mana Burn -> stand-in 25779 Mana Burn
- Mana Stalker: spell 10876 Mana Burn -> stand-in 25779 Mana Burn
- Azurebeak: spell 24579 Screech -> stand-in 31273 Screech

## Display stand in (26)

- 61342 Barkskin Ursa: Turtle display 18733 -> stand-in 145
- 61343 Barkskin Pathfinder: Turtle display 18745 -> stand-in 145
- 61344 Barkskin Avenger: Turtle display 18744 -> stand-in 145
- 61347 Barkskin Windtalker: Turtle display 18734 -> stand-in 145
- 61356 Shadeflayer Berserker: Turtle display 20287 -> stand-in 4623
- 61356 Shadeflayer Berserker: Turtle display 20288 -> stand-in 14983
- 61357 Shadeflayer Shadowhunter: Turtle display 20289 -> stand-in 4078
- 61357 Shadeflayer Shadowhunter: Turtle display 20290 -> stand-in 9721
- 61358 Shadeflayer Shaman: Turtle display 20291 -> stand-in 6540
- 61358 Shadeflayer Shaman: Turtle display 20292 -> stand-in 6420
- 61359 Shadeflayer Trapper: Turtle display 20293 -> stand-in 4475
- 61359 Shadeflayer Trapper: Turtle display 20294 -> stand-in 11191
- 61360 Warlord Hanzento: Turtle display 20297 -> stand-in 4634
- 61361 Speaker Gan'hota: Turtle display 20298 -> stand-in 9729
- 61367 Shadeflayer Troll: Turtle display 20295 -> stand-in 4771
- 61367 Shadeflayer Troll: Turtle display 20296 -> stand-in 4223
- 61505 Talona Gladeheart: Turtle display 20257 -> stand-in 19881
- 61521 Danthar Oakmantle: Turtle display 20253 -> stand-in 11326
- 61523 Naytha Grovelight: Turtle display 20260 -> stand-in 19881
- 61527 Nordanaar Guardian: Turtle display 20355 -> stand-in 12924
- 61527 Nordanaar Guardian: Turtle display 20356 -> stand-in 2064
- 61545 Ysera: Turtle display 7806 -> stand-in 19260
- 61577 Annesastrasza: Turtle display 20428 -> stand-in 20723
- 61578 Shadowhunter Trak'nal: Turtle display 20429 -> stand-in 11245
- 61579 Melanastrasza: Turtle display 20439 -> stand-in 28080
- 61988 Dissipating Spectre: Turtle display 20611 -> stand-in 1917

## Eventai (1)

- 61356 Shadeflayer Berserker: spell 8269 Enrage -> stand-in 8599 Enrage

## Gossip (3)

- menu 41396 option 1: runs Turtle gossip script 41396 (commands [0, 4, 10, 15, 61, 69]; not ported)
- menu 41483 option 0: Turtle condition 164 and script 342 not ported - option left out
- menu 47035 option 0: Turtle gossip script 47035 -> SmartAI Quest credit 60044

## Loot (2)

- 61510: lootid 61510 has no rows in Turtle's creature_loot_template - cleared
- 61511: lootid 61511 has no rows in Turtle's creature_loot_template - cleared

## Go display added (9)

- 2002655 World GENERIC DARKIRONDWARF PASSIVE DOODADS StretchedSkins B: new display row
- 2003734 World GENERIC NIGHTELF PASSIVE DOODADS TaxiFlags TaxiFlagNig: new display row
- 2005520 World KALIMDOR KALIDAR PASSIVEDOODADS KalidarHarpyNest Kalid: new display row
- 2005521 World KALIMDOR KALIDAR PASSIVEDOODADS KalidarHarpyNest Kalid: new display row
- 2005543 World KALIMDOR MAURADON PASSIVEDOODADS BRIDGEBRAZIERS Bridge: new display row
- 2010386 World GENERIC NIGHTELF PASSIVE DOODADS HippogryphRoost Hippo: new display row
- 2020036 Runestone of Nordrassil: new display row
- 2020299 Star Wood Tree: new display row
- 2020300 Dead Wood Tree: new display row

## Turtle only lock (2)

- 2020299 Star Wood Tree: lock 1664 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020300 Dead Wood Tree: lock 1663 is a Turtle-only lock type (e.g. Survival gathering) - left out

## Pools (1)

- 62 spawn pools (223 objects, 0 creatures)

## Area triggers (1)

- Turtle trigger 1705 Hyjal - Nordanaar Inn (rest area) -> 5913

## Graveyards (2)

- Turtle graveyard 147 Hyjal -> 1911
- Turtle graveyard 148 Hyjal, Nordanaar -> 1912

## Flight paths (5)

- node 434 Nordanaar, Hyjal (Turtle 99)
- path 2014: 52 -> 434, 43 points, cost 1020
- path 2015: 53 -> 434, 43 points, cost 1020
- path 2016: 434 -> 53, 43 points, cost 1020
- path 2017: 434 -> 52, 43 points, cost 1020

## Wmo areas (1)

- 23 WMOAreaTable rows (room names) for WMO ids [6004, 6005]

## World map (1)

- WorldMapArea 2009 'Hyjal' + 10 subzone overlays, 57 map images
