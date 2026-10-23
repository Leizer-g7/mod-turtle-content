# The Deadmines

File: `data/sql/db-world/mod_turtle_042_deadmines.sql`  
Terrain mode: **stock**

## Counts

- creature: 16
- creature_addon: 6
- creature_equip_template: 3
- creature_loot_template: 21
- creature_questender: 2
- creature_queststarter: 2
- creature_template: 5
- creature_template_model: 6
- creature_template_movement: 5
- creature_template_resistance: 1
- creature_text: 4
- quest_offer_reward: 2
- quest_request_items: 2
- quest_template: 2
- quest_template_addon: 2
- smart_scripts: 9
- waypoint_data: 6

## Client assets (1)

- 50 Turtle files (buildings, textures) shipped in the client patch: World\wmo\Dungeon\AZ_Deadmines\AZ_Deadmines_B.wmo with its parts

## Model stand in (10)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\GENERIC\harvestgolemprop\Harvestgolembare.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\GENERIC\harvestgolemprop\Harvestgolemfull.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\GENERIC\harvestgolemprop\Harvestgolemnoback.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\GENERIC\harvestgolemprop\Harvestgolemnohead.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\GENERIC\harvestgolemprop\Harvestgolemonehand.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\GENERIC\harvestgolemprop\harvestgolemnoback.MDX -> Creature\GolemHarvest\GolemHarvest.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## Zone quests elsewhere (2)

- quest 40396: given and turned in outside the zone ([392] / [392])
- quest 41392: given and turned in outside the zone ([6946] / [6946])

## Display stand in (2)

- 61960 Defias Mixologist: Turtle display 20624 -> stand-in 29536
- 61961 Jared Voss: Turtle display 20628 -> stand-in 3984

## Eventai (4)

- 61961 Jared Voss: script command 16 (Jared Voss - Say on Aggro (sound)) not converted
- 61961 Jared Voss: script command 16 (Jared Voss - Say upon Death (sound)) not converted
- 61963 Masterpiece Harvester: script command 16 (Boss Masterpiece Harvester - Say on Aggro (sound)) not converted
- 61963 Masterpiece Harvester: script command 16 (Boss Masterpiece Harvester - Say upon Death (sound)) not converted

## Loot (3)

- 61959: lootid 61959 has no rows in Turtle's creature_loot_template - cleared
- 61960: lootid 61960 has no rows in Turtle's creature_loot_template - cleared
- 61963: lootid 61963 lost all its items (Turtle-only items left out) - cleared
