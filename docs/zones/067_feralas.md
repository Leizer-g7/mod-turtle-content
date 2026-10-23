# Feralas

File: `data/sql/db-world/mod_turtle_023_feralas.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 2
- creature: 102
- creature_addon: 9
- creature_equip_template: 9
- creature_loot_template: 1248
- creature_questender: 19
- creature_queststarter: 19
- creature_template: 37
- creature_template_addon: 1
- creature_template_model: 40
- creature_template_movement: 37
- gameobject: 301
- gameobject_loot_template: 4
- gameobject_template: 57
- gameobject_template_addon: 5
- gossip_menu: 17
- gossip_menu_option: 13
- npc_text: 17
- npc_vendor: 75
- quest_offer_reward: 19
- quest_request_items: 19
- quest_template: 19
- quest_template_addon: 19
- skinning_loot_template: 4
- smart_scripts: 9
- waypoint_data: 82

## Client tiles (21)

- Kalimdor_32_39: chunk 172 taken for Turtle's md_mushroomcave02.wmo
- Kalimdor_32_41: chunk 230 taken for Turtle's dsnightelf2story.wmo
- Kalimdor_32_42: chunk 5 taken for Turtle's azrclassicalelfruin04.wmo
- Kalimdor_32_42: chunk 27 taken for Turtle's azrclassicalelfruin02.wmo
- Kalimdor_33_40: merged on top of an earlier zone's tile
- Kalimdor_33_40: chunk 70 taken for Turtle's nightelfsmallhouse.wmo
- Kalimdor_33_40: chunk 100 taken for Turtle's nightelfguardtower.wmo
- Kalimdor_33_40: chunk 118 taken for Turtle's nightelftent02_pvp.wmo
- 105 reshaped chunks next to the zone taken (keep their 3.3.5 area); 81 reshaped chunks away from the zone left as 3.3.5
- 184 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 96 edge points aligned (largest step 1.22 yd)
- 0 edge points at the rim matched to the 3.3.5 tiles next to it
- Kalimdor_31_40: merged - 13 of 256 chunks from Turtle
- Kalimdor_31_42: merged - 32 of 256 chunks from Turtle (29 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_32_39: merged - 79 of 256 chunks from Turtle
- Kalimdor_32_40: merged - 38 of 256 chunks from Turtle
- Kalimdor_32_41: merged - 227 of 256 chunks from Turtle
- Kalimdor_32_42: merged - 155 of 256 chunks from Turtle (44 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_33_40: merged - 24 of 256 chunks from Turtle
- Kalimdor_33_41: merged - 13 of 256 chunks from Turtle (13 of them reshaped ground that keeps its 3.3.5 area)
- Kalimdor_33_42: merged - 19 of 256 chunks from Turtle (19 of them reshaped ground that keeps its 3.3.5 area)

## Client assets (1)

- 0 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (2)

- 5210 Chimaera Roost Vale (subzone of 357, map 1, exploration bit 3791, level 42)
- 5556 Feralkin Cave (subzone of 357, map 1, exploration bit 3792, level 0)

## Spawned elsewhere (7)

- Larodar Wildwhisper (tw guid 2578251): already spawned by 050_gilneas (its extra_spawns)
- Fazgel Mechaflame (tw guid 2569415): already spawned by 058_stranglethorn_vale (its extra_spawns)
- Lyvdia Dawnbird (tw guid 5003651): already spawned by 058_stranglethorn_vale (its extra_gameobject_spawns)
- Highborne Golden Statue (tw guid 5003322): already spawned by 058_stranglethorn_vale (its extra_gameobject_spawns)
- Highborne Golden Statue (tw guid 5003323): already spawned by 058_stranglethorn_vale (its extra_gameobject_spawns)
- Highborne Golden Statue (tw guid 5003324): already spawned by 058_stranglethorn_vale (its extra_gameobject_spawns)
- Highborne Golden Statue (tw guid 5003325): already spawned by 058_stranglethorn_vale (its extra_gameobject_spawns)

## Seasonal spawns (2)

- 22 creature spawns that Turtle shows only during seasonal events left out
- 73 object spawns that Turtle shows only during seasonal events left out

## Zone quests elsewhere (2)

- quest 60020: given and turned in outside the zone ([7877] / [7877])
- quest 41043: given and turned in outside the zone ([61584] / [61584])

## Display stand in (10)

- 49005 Grug'thok the Seer: Turtle display 11556 -> stand-in 33
- 61296 Nyhm: Turtle display 2637 -> stand-in 2637
- 61586 Cenerron: Turtle display 20410 -> stand-in 320
- 61587 Bethelon Wildwhisper: Turtle display 20434 -> stand-in 2066
- 61588 Velos Sharpstrike: Turtle display 20433 -> stand-in 16343
- 61590 Lataro Swifthoof: Turtle display 20436 -> stand-in 15544
- 61596 Venomlash Chimaera: Turtle display 20414 -> stand-in 4269
- 61597 Dunebound Chimaera: Turtle display 20412 -> stand-in 4269
- 61598 Marat Grimtotem: Turtle display 10240 -> stand-in 10240
- 61599 Darksaber: Turtle display 20437 -> stand-in 9954

## Cpp script (2)

- 49005 Grug'thok the Seer: Turtle C++ script 'boss_grugthok_the_seer' (see manual/067_feralas.sql)
- 66004 Ancient Wolf Spirit: Turtle C++ script 'npc_ancient_spirit_wolf' (see manual/067_feralas.sql)

## Gossip (4)

- menu 2890 option 0: Turtle condition 164 and script 342 not ported - option left out
- menu 2890 option 3: Turtle condition 440 not ported - option always shown
- menu 5113: text 8317 has Turtle condition 3 (not ported - always shown)
- menu 5113: text 8319 has Turtle condition 2 (not ported - always shown)

## Quest spell (1)

- quest 40534 The Way of the Spiritwolf V: RewSpellCast spell 45519 Feral Spirit does not exist in 3.3.5 - dropped (add a stand-in to spell_substitutions)

## Go display added (29)

- 2002001 World AZEROTH REDRIDGE PASSIVEDOODADS DOCKPIECES RedRidgeDoc: new display row
- 2002110 World AZEROTH STRANGLETHORN PASSIVEDOODADS Trees Strangletho: new display row
- 2002218 World AZEROTH WESTFALL PASSIVEDOODADS Detail WestFallBerryBu: new display row
- 2002403 World DUNGEON SCARLETMONASTERY PASSIVEDOODADS STATUES statue: new display row
- 2002410 World DUNGEON SCARLETMONASTERY PASSIVEDOODADS STATUES statue: new display row
- 2002412 World DUNGEON SCARLETMONASTERY PASSIVEDOODADS STATUES statue: new display row
- 2002708 World GENERIC DWARF PASSIVE DOODADS Bookshelves BookshelfDwa: new display row
- 2002798 World GENERIC DWARF PASSIVE DOODADS Guns RifleDwarven.mdx: new display row
- 2002884 World GENERIC DWARF PASSIVE DOODADS TABLES DwarvenTableSimpl: new display row
- 2003086 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorLeatherShirtO: new display row
- 2003114 World GENERIC HUMAN PASSIVE DOODADS Artwork Painting12.mdx: new display row
- 2003419 World GENERIC HUMAN PASSIVE DOODADS PLANTERBOXES TirisfallWi: new display row
- 2003592 World GENERIC NIGHTELF PASSIVE DOODADS BOWLS NightelfBowl.md: new display row
- 2004227 World GENERIC PASSIVEDOODADS Hides HideStack01.mdx: new display row
- 2004586 World GENERIC TAUREN PASSIVE DOODADS BOWLS TaurenBowl03.mdx: new display row
- 2004591 World GENERIC TAUREN PASSIVE DOODADS BOWLS TaurenBowl08.mdx: new display row
- 2004697 World GENERIC TAUREN PASSIVE DOODADS TaurenCanoe Taurencanoe: new display row
- 2004712 World GENERIC TAUREN PASSIVE DOODADS TaurenWallScrolls Taure: new display row
- 2006265 World KHAZMODAN LOCHMODAN PASSIVEDOODADS Fences LochModanWoo: new display row
- 2006267 World KHAZMODAN LOCHMODAN PASSIVEDOODADS Fences LochModanWoo: new display row
- 2006268 World KHAZMODAN LOCHMODAN PASSIVEDOODADS Fences LochModanWoo: new display row
- 2007422 World wmo Azeroth Buildings Duskwood_MageTower Duskwood_Mage: new display row
- 2007929 World wmo Kalimdor Buildings OrcBlacksmith SwampOrcBlacksmit: new display row
- 2008046 World wmo Kalimdor CollidableDoodads Mulgore CentaurTents Ce: new display row
- 2008143 World wmo KhazModan Collidable Doodads LochModan ExcavationS: new display row
- 2008708 World EXPANSION01 DOODADS GENERIC BLOODELF RUGS BE_Rug_Mediu: new display row
- 2009326 World EXPANSION01 DOODADS SILVERMOON FLOWERS SilvermoonFlowe: new display row
- 2020299 Star Wood Tree: new display row
- 2020309 Shade Wood Tree: new display row

## Go type changed (5)

- 2007422 World wmo Azeroth Buildings Duskwood_MageTower Duskwood_Mage: type 14 (static WMO) -> 5 (generic)
- 2007929 World wmo Kalimdor Buildings OrcBlacksmith SwampOrcBlacksmit: type 14 (static WMO) -> 5 (generic)
- 2008046 World wmo Kalimdor CollidableDoodads Mulgore CentaurTents Ce: type 14 (static WMO) -> 5 (generic)
- 2008143 World wmo KhazModan Collidable Doodads LochModan ExcavationS: type 14 (static WMO) -> 5 (generic)
- 2010617 World wmo transports transport_zeppelin transport_zeppelin.w: type 14 (static WMO) -> 5 (generic)

## Turtle only lock (2)

- 2020299 Star Wood Tree: lock 1664 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020309 Shade Wood Tree: lock 1661 is a Turtle-only lock type (e.g. Survival gathering) - left out

## Go no model (2)

- 3000303 Sherpa_Bedroll_0: Turtle-only model with no stand-in (add one to go_model_substitutions)
- 3000304 Sherpa_Bedroll_2: Turtle-only model with no stand-in (add one to go_model_substitutions)

## Objects waiting for the client patch (2)

- 3000303 Sherpa_Bedroll_0 - `world\EXPANSION04\DOODADS\Sherpa\Sherpa_Bedroll_01.mdx`
- 3000304 Sherpa_Bedroll_2 - `world\EXPANSION04\DOODADS\Sherpa\Sherpa_Bedroll_02.mdx`
