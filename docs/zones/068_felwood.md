# Felwood

File: `data/sql/db-world/mod_turtle_024_felwood.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 1
- creature: 37
- creature_addon: 10
- creature_equip_template: 3
- creature_loot_template: 224
- creature_questender: 19
- creature_queststarter: 18
- creature_template: 19
- creature_template_model: 20
- creature_template_movement: 19
- creature_template_resistance: 2
- gameobject: 107
- gameobject_loot_template: 5
- gameobject_template: 25
- gameobject_template_addon: 5
- gossip_menu: 5
- npc_text: 5
- npc_vendor: 39
- pickpocketing_loot_template: 7
- quest_offer_reward: 19
- quest_request_items: 19
- quest_template: 19
- quest_template_addon: 19
- smart_scripts: 10
- waypoint_data: 25

## Client tiles (21)

- Kalimdor_34_21: merged on top of an earlier zone's tile
- Kalimdor_34_22: merged on top of an earlier zone's tile
- Kalimdor_34_23: merged on top of an earlier zone's tile
- Kalimdor_35_20: chunk 69 taken for Turtle's nightelftent02_pvp.wmo
- Kalimdor_35_20: chunk 73 taken for Turtle's kalidardock01.wmo
- Kalimdor_35_20: chunk 87 taken for Turtle's nightelf2story.wmo
- Kalimdor_35_20: chunk 104 taken for Turtle's nightelfoutpost.wmo
- Kalimdor_35_20: chunk 105 taken for Turtle's nightelfmoonwell.wmo
- Kalimdor_35_21: merged on top of an earlier zone's tile
- Kalimdor_35_22: merged on top of an earlier zone's tile
- Kalimdor_35_23: merged on top of an earlier zone's tile
- Kalimdor_36_21: merged on top of an earlier zone's tile
- Kalimdor_36_22: merged on top of an earlier zone's tile
- Kalimdor_36_23: merged on top of an earlier zone's tile
- 0 reshaped chunks next to the zone taken (keep their 3.3.5 area); 0 reshaped chunks away from the zone left as 3.3.5
- 0 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 10 edge points aligned (largest step 0.33 yd)
- 0 edge points at the rim matched to the 3.3.5 tiles next to it
- Kalimdor_33_21: merged - 3 of 256 chunks from Turtle
- Kalimdor_34_21: merged - 12 of 256 chunks from Turtle
- Kalimdor_35_20: merged - 30 of 256 chunks from Turtle

## Client assets (1)

- 0 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (1)

- 5224 Shrine of the Betrayer (subzone of 361, map 1, exploration bit 3793, level 60)

## Spawned elsewhere (1)

- Pethax Blackhorn (tw guid 2567808): already spawned by 053_lapidis_isle (its extra_spawns)

## Seasonal spawns (1)

- 1 creature spawns that Turtle shows only during seasonal events left out

## Zone quests elsewhere (2)

- quest 40786: given and turned in outside the zone ([9465] / [9465])
- quest 41071: given and turned in outside the zone ([9465] / [9465])

## Display stand in (5)

- 60710 Niremius Darkwind: Turtle display 18648 -> stand-in 1542
- 61164 Faladar Starsplinter: Turtle display 18119 -> stand-in 1895
- 61592 Yohan Wildwalker: Turtle display 20401 -> stand-in 15399
- 61593 Marlonias Shademoon: Turtle display 20402 -> stand-in 5083
- 61613 Zafan: Turtle display 18363 -> stand-in 4449

## Cpp script (1)

- 60710 Niremius Darkwind: Turtle C++ script 'npc_niremius' (see manual/068_felwood.sql)

## Trainer (2)

- 61149 Taloras Gladewind: Turtle trainer rows but no trainer flag - not a trainer
- 61155 Shaewyn: Turtle trainer rows but no trainer flag - not a trainer

## Spell sub (1)

- Faladar Starsplinter: spell 8269 Enrage -> stand-in 8599 Enrage

## Go display added (10)

- 2003600 World GENERIC NIGHTELF PASSIVE DOODADS Beds elfbed02.mdx: new display row
- 2003611 World GENERIC NIGHTELF PASSIVE DOODADS GardenBenches GardenB: new display row
- 2003623 World GENERIC NIGHTELF PASSIVE DOODADS LAMPS KalidarStreetLa: new display row
- 2003625 World GENERIC NIGHTELF PASSIVE DOODADS Lanterns NightElfHang: new display row
- 2003631 World GENERIC NIGHTELF PASSIVE DOODADS MAGICALIMPLEMENTS NEM: new display row
- 2003634 World GENERIC NIGHTELF PASSIVE DOODADS MAGICALIMPLEMENTS NEM: new display row
- 2003635 World GENERIC NIGHTELF PASSIVE DOODADS MAGICALIMPLEMENTS NEM: new display row
- 2003641 World GENERIC NIGHTELF PASSIVE DOODADS Pottery ElvenPottery0: new display row
- 2020299 Star Wood Tree: new display row
- 2020300 Dead Wood Tree: new display row

## Go type changed (1)

- 2008025 World wmo Kalimdor CollidableDoodads Darkshore GiantSeaTurtl: type 14 (static WMO) -> 5 (generic)

## Turtle only lock (2)

- 2020299 Star Wood Tree: lock 1664 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020300 Dead Wood Tree: lock 1663 is a Turtle-only lock type (e.g. Survival gathering) - left out
