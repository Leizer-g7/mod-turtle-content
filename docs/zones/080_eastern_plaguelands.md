# Eastern Plaguelands

File: `data/sql/db-world/mod_turtle_036_eastern_plaguelands.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 1
- creature: 171
- creature_addon: 34
- creature_equip_template: 8
- creature_loot_template: 1211
- creature_onkill_reputation: 2
- creature_questender: 10
- creature_queststarter: 9
- creature_template: 22
- creature_template_addon: 1
- creature_template_model: 25
- creature_template_movement: 22
- creature_template_resistance: 2
- gameobject: 314
- gameobject_loot_template: 1
- gameobject_template: 64
- gameobject_template_addon: 2
- gossip_menu: 3
- npc_text: 3
- npc_vendor: 10
- pickpocketing_loot_template: 3
- quest_offer_reward: 9
- quest_request_items: 9
- quest_template: 9
- quest_template_addon: 9
- smart_scripts: 17
- waypoint_data: 103

## Client tiles (18)

- Azeroth_36_26: chunk 223 taken for Turtle's duskwood_magetower.wmo
- Azeroth_36_27: chunk 15 taken for Turtle's duskwoodabandoned_human_farm.wmo
- Azeroth_36_27: chunk 31 taken for Turtle's duskwoodfarmhouseburnt.wmo
- Azeroth_37_26: chunk 231 taken for Turtle's guardtower_damaged.wmo
- Azeroth_37_26: chunk 242 taken for Turtle's duskwoodabandoned_human_farm.wmo
- Azeroth_37_27: chunk 17 taken for Turtle's duskwoodabandoned_humantwostory.wmo
- Azeroth_37_27: chunk 18 taken for Turtle's duskwoodabandoned_blacksmith.wmo
- Azeroth_37_27: chunk 48 taken for Turtle's ruinedkeep.wmo
- Azeroth_37_27: chunk 70 taken for Turtle's md_spidermine_nokobolds.wmo
- Azeroth_37_27: chunk 97 taken for Turtle's duskwoodabandoned_lumbermill.wmo
- 0 reshaped chunks next to the zone taken (keep their 3.3.5 area); 0 reshaped chunks away from the zone left as 3.3.5
- 110 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 33 edge points aligned (largest step 0.42 yd)
- 36 edge points at the rim matched to the 3.3.5 tiles next to it
- Azeroth_36_26: merged - 15 of 256 chunks from Turtle
- Azeroth_36_27: merged - 23 of 256 chunks from Turtle
- Azeroth_37_26: merged - 58 of 256 chunks from Turtle
- Azeroth_37_27: merged - 109 of 256 chunks from Turtle

## Client assets (1)

- 0 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (1)

- 5547 Forlorn Summit (subzone of 139, map 0, exploration bit 3806, level 57)

## Spawned elsewhere (1)

- Canos Clearwood (tw guid 2577971): already spawned by 055_mount_hyjal (its extra_spawns)

## Seasonal spawns (2)

- 13 creature spawns that Turtle shows only during seasonal events left out
- 85 object spawns that Turtle shows only during seasonal events left out

## Zone quests elsewhere (2)

- quest 40221: given and turned in outside the zone ([11536] / [11536])
- quest 41200: given and turned in outside the zone ([11034] / [11034])

## Object id taken (1)

- 186425 Torche en sorbier: 3.3.5 uses this id for 'Witchbane Torch' - not spawned

## Display stand in (10)

- 49008 Crusader Larsarius: Turtle display 18749 -> stand-in 2042
- 60533 First Mate Dorrul: Turtle display 18701 -> stand-in 1282
- 61572 Tanner Brightbelt: Turtle display 18662 -> stand-in 2910
- 61763 Dean LeGuin: Turtle display 20538 -> stand-in 11124
- 61764 High Widow Arania: Turtle display 20540 -> stand-in 4462
- 61765 Gunther: Turtle display 20539 -> stand-in 4283
- 61766 Overzealous Student: Turtle display 20542 -> stand-in 17884
- 61766 Overzealous Student: Turtle display 20543 -> stand-in 17681
- 61766 Overzealous Student: Turtle display 20544 -> stand-in 27848
- 61886 Miriam Lenheim: Turtle display 20541 -> stand-in 3828

## Cpp script (1)

- 49008 Crusader Larsarius: Turtle C++ script 'boss_crusader_larsarius' (see manual/080_eastern_plaguelands.sql)

## Go type changed (4)

- 1000009 Alliance Tower: type 14 (static WMO) -> 5 (generic)
- 2000193 World wmo Azeroth Buildings Duskwood_Stable Duskwood_Stable.: type 14 (static WMO) -> 5 (generic)
- 2007407 World wmo Azeroth Buildings Chapel DuskwoodChapel.wmo: type 14 (static WMO) -> 5 (generic)
- 2007426 World wmo Azeroth Buildings Duskwood_human_farm Duskwood_hum: type 14 (static WMO) -> 5 (generic)

## Go display added (27)

- 2001786 World AZEROTH DUSKWOOD PASSIVEDOODADS tombs TombStone08.mdx: new display row
- 2002258 World AZEROTH WESTFALL PASSIVEDOODADS TreeStumps WestFallTre: new display row
- 2002874 World GENERIC DWARF PASSIVE DOODADS TABLES DwarvenTableAvera: new display row
- 2003379 World GENERIC HUMAN PASSIVE DOODADS Lanterns GeneralLantern0: new display row
- 2003908 World GENERIC ORC PASSIVE DOODADS Saddles WyvernSaddle.mdx: new display row
- 2004241 World GENERIC PASSIVEDOODADS LIGHTS Chandelier01.mdx: new display row
- 2004337 World GENERIC PASSIVEDOODADS ParticleEmitters BubblesB.mdx: new display row
- 2004786 World GENERIC UNDEAD PASSIVE DOODADS STONEFENCE UndeadStoneW: new display row
- 2006548 World LORDAERON PLAGUELAND PASSIVEDOODADS TREES PlaguelandTr: new display row
- 2006551 World LORDAERON PLAGUELAND PASSIVEDOODADS TREES PlaguelandTr: new display row
- 2006554 World LORDAERON PLAGUELAND PASSIVEDOODADS TreeBarrier TreeBa: new display row
- 2006556 World LORDAERON PLAGUELAND PASSIVEDOODADS plants PlaguelandF: new display row
- 2006572 World LORDAERON SCHOLOMANCE PASSIVEDOODADS BOOKSHELVES Schol: new display row
- 2006574 World LORDAERON SCHOLOMANCE PASSIVEDOODADS BOOKSHELVES Schol: new display row
- 2006578 World LORDAERON SCHOLOMANCE PASSIVEDOODADS CANDLES FloorCand: new display row
- 2006587 World LORDAERON SCHOLOMANCE PASSIVEDOODADS CANDLES Scholme_C: new display row
- 2006589 World LORDAERON SCHOLOMANCE PASSIVEDOODADS CANDLES Scholme_C: new display row
- 2006603 World LORDAERON SCHOLOMANCE PASSIVEDOODADS OperationTables C: new display row
- 2006669 World LORDAERON SilverPine PassiveDoodads Boardwalks SilverP: new display row
- 2006694 World LORDAERON TIRISFALGLADE PASSIVEDOODADS GRAVES BrillCof: new display row
- 2006703 World LORDAERON TIRISFALGLADE PASSIVEDOODADS Outposts Tirisf: new display row
- 2006704 World LORDAERON TIRISFALGLADE PASSIVEDOODADS Outposts Tirisf: new display row
- 2006705 World LORDAERON TIRISFALGLADE PASSIVEDOODADS Outposts Tirisf: new display row
- 2006706 World LORDAERON TIRISFALGLADE PASSIVEDOODADS Outposts Tirisf: new display row
- 2006707 World LORDAERON TIRISFALGLADE PASSIVEDOODADS Outposts Tirisf: new display row
- 2008630 World EXPANSION01 DOODADS GENERIC BLOODELF Candles BE_Candle: new display row
- 2010384 World Generic Human Passive Doodads STORMWIND AllianceMapTab: new display row

## Go no model (1)

- 3000208 Thalassian Mailbox: Turtle-only model with no stand-in (add one to go_model_substitutions)

## Quest chain (2)

- quest 80709: PrevQuestID 80708 is not in this build - link removed
- quest 80729: PrevQuestID 80728 is not in this build - link removed

## Objects waiting for the client patch (2)

- 944 Place centrale de DarrowShire - `missing`
- 3000208 Thalassian Mailbox - `World\Generic\PassiveDoodads\PostBoxes\PostBoxHigh1Elf.mdx`
