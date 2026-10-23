# Westfall

File: `data/sql/db-world/mod_turtle_041_westfall.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 1
- creature: 23
- creature_equip_template: 7
- creature_loot_template: 102
- creature_questender: 31
- creature_queststarter: 28
- creature_template: 11
- creature_template_addon: 1
- creature_template_model: 11
- creature_template_movement: 11
- creature_template_resistance: 5
- creature_text: 3
- gameobject: 9
- gameobject_loot_template: 7
- gameobject_queststarter: 2
- gameobject_template: 9
- gameobject_template_addon: 8
- gossip_menu: 3
- npc_text: 3
- npc_vendor: 1
- quest_offer_reward: 31
- quest_request_items: 30
- quest_template: 31
- quest_template_addon: 31
- smart_scripts: 5

## Client tiles (17)

- Azeroth_26_49: merged on top of an earlier zone's tile
- Azeroth_26_50: merged on top of an earlier zone's tile
- Azeroth_26_52: merged on top of an earlier zone's tile
- Azeroth_26_53: merged on top of an earlier zone's tile
- Azeroth_27_49: merged on top of an earlier zone's tile
- Azeroth_27_52: merged on top of an earlier zone's tile
- Azeroth_27_53: merged on top of an earlier zone's tile
- Azeroth_28_51: chunk 70 taken for Turtle's westfallhouse_smallstraw.wmo
- 0 reshaped chunks next to the zone taken (keep their 3.3.5 area); 0 reshaped chunks away from the zone left as 3.3.5
- 0 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 76 edge points aligned (largest step 0.47 yd)
- 51 edge points at the rim matched to the 3.3.5 tiles next to it
- Azeroth_26_52: merged - 2 of 256 chunks from Turtle
- Azeroth_27_50: merged - 5 of 256 chunks from Turtle
- Azeroth_27_52: merged - 2 of 256 chunks from Turtle
- Azeroth_27_53: merged - 29 of 256 chunks from Turtle
- Azeroth_28_51: merged - 28 of 256 chunks from Turtle

## Client assets (1)

- 19 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (1)

- 5102 Gartside Plot (subzone of 40, map 0, exploration bit 3826, level 10)

## Seasonal spawns (2)

- 21 creature spawns that Turtle shows only during seasonal events left out
- 45 object spawns that Turtle shows only during seasonal events left out

## Zone quests elsewhere (21)

- quest 40470: given and turned in outside the zone ([8934] / [8934])
- quest 40471: given and turned in outside the zone ([8934] / [8934])
- quest 40472: given and turned in outside the zone ([8934] / [5518])
- quest 40473: given and turned in outside the zone ([5518] / [8934])
- quest 40480: given and turned in outside the zone ([8934] / [3091])
- quest 40481: given and turned in outside the zone ([3091] / [3091])
- quest 40482: given and turned in outside the zone ([3091] / [3091])
- quest 40594: given and turned in outside the zone ([234] / [1646])
- quest 40595: given and turned in outside the zone ([1646] / [1212])
- quest 40596: given and turned in outside the zone ([1212] / [952])
- quest 40597: given and turned in outside the zone ([952] / [952])
- quest 40598: given and turned in outside the zone ([952] / [234])
- quest 40599: given and turned in outside the zone ([234] / [60879])
- quest 40600: given and turned in outside the zone ([60879] / [60879])
- quest 40601: given and turned in outside the zone ([60879] / [234])
- quest 40602: given and turned in outside the zone ([234] / [234])
- quest 40603: given and turned in outside the zone ([234] / [952])
- quest 41390: given and turned in outside the zone ([6946] / [7024])
- quest 41391: given and turned in outside the zone ([7024] / [6946])
- quest 40593: extra quest, given and turned in outside the zone or by an object (['object 2010927'] / [234])
- quest 40395: extra quest, given and turned in outside the zone or by an object (['object 2010884'] / [392])

## Display stand in (3)

- 60854 Farad Wrightsow: Turtle display 18913 -> stand-in 3286
- 60858 Maltimor Gartside: Turtle display 18917 -> stand-in 2039
- 62064 Blitzy Pouchcutter: Turtle display 11675 -> stand-in 15917

## Cpp script (2)

- 60854 Farad Wrightsow: Turtle C++ script 'npc_farad_wrightsow' (see manual/085_westfall.sql)
- 60858 Maltimor Gartside: Turtle C++ script 'npc_maltimor_gartside' (see manual/085_westfall.sql)

## Quest giver flag (1)

- quest-giver flag added to 3.3.5 NPCs [3091, 8934] (Franklin Hamar, Christopher Hewen)
