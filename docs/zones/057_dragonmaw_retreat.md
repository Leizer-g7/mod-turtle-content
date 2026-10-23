# Dragonmaw Retreat

File: `data/sql/db-world/mod_turtle_013_dragonmaw_retreat.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 2
- creature: 463
- creature_addon: 63
- creature_equip_template: 23
- creature_loot_template: 2403
- creature_questender: 6
- creature_queststarter: 5
- creature_template: 34
- creature_template_addon: 5
- creature_template_model: 34
- creature_template_movement: 34
- creature_template_resistance: 31
- creature_text: 15
- gameobject: 296
- gameobject_loot_template: 2
- gameobject_questender: 1
- gameobject_queststarter: 2
- gameobject_template: 18
- gameobject_template_addon: 4
- gossip_menu: 1
- npc_text: 1
- pickpocketing_loot_template: 6
- quest_offer_reward: 7
- quest_request_items: 7
- quest_template: 7
- quest_template_addon: 7
- smart_scripts: 62
- waypoint_data: 1079

## Client tiles (9)

- Dragonmaw_38_42: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_38_43: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_38_44: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_39_42: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_39_43: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_39_44: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_40_42: 0 empty-liquid offsets fixed, 24 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_40_43: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 1 object ids moved
- Dragonmaw_40_44: 0 empty-liquid offsets fixed, 9 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 1 object ids moved

## Client assets (1)

- 51 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (2)

- 5601 Dragonmaw Retreat (zone, map 816, exploration bit 3766, level 35)
- 5634 Zuluhed's Terrace (zone, map 816, exploration bit 3767, level 30)

## Existing templates (2)

- 75 creature spawns of 3 templates 3.3.5 already has (AzerothCore's template is used)
- 21 object spawns of 8 templates 3.3.5 already has (herbs, ore, chests ...)

## Zone quests elsewhere (6)

- quest 41749: given and turned in outside the zone ([8305] / [8305])
- quest 41753: given and turned in outside the zone ([2402] / [2402])
- quest 41756: given and turned in outside the zone ([2104] / [2104])
- quest 41757: given and turned in outside the zone ([2104] / [2104])
- quest 41754: extra quest, given and turned in outside the zone or by an object (['object 2020198'] / [8256])
- quest 41774: extra quest, given and turned in outside the zone or by an object (['object 2020220'] / ['object 2020220'])

## Display stand in (15)

- 61010 Torwyn Redbrand: Turtle display 18999 -> stand-in 15746
- 62036 Dragonmaw Bonespeaker: Turtle display 20664 -> stand-in 1392
- 62037 Zuluhed the Whacked: Turtle display 20665 -> stand-in 3857
- 62038 Elder Hollowblood: Turtle display 20666 -> stand-in 14413
- 62039 Dragonmaw Fireseeker: Turtle display 20667 -> stand-in 23932
- 62040 Dragonmaw Hatcher: Turtle display 20668 -> stand-in 3752
- 62045 Dragonmaw Soldier: Turtle display 20670 -> stand-in 1332
- 62046 Dragonmaw Tracker: Turtle display 20671 -> stand-in 1332
- 62047 Dragonmaw Wyrmguard: Turtle display 20672 -> stand-in 11866
- 62067 Web Master Torkon: Turtle display 20743 -> stand-in 6787
- 62069 Halgan Redbrand: Turtle display 18949 -> stand-in 3044
- 62071 Garlok Flamekeeper: Turtle display 20741 -> stand-in 4463
- 62263 Dragonmaw Marauder: Turtle display 20801 -> stand-in 1880
- 62264 Dragonmaw Sentry: Turtle display 20803 -> stand-in 4048
- 62453 Dragonmaw Enchanter: Turtle display 20798 -> stand-in 3743

## Cpp script (5)

- 62037 Zuluhed the Whacked: Turtle C++ script 'boss_zuluhed_the_whacked' (see manual/057_dragonmaw_retreat.sql)
- 62056 Bogpaw Truthsay: Turtle C++ script 'boss_bogpaw_truthsay' (see manual/057_dragonmaw_retreat.sql)
- 62057 Gowlfang: Turtle C++ script 'boss_gowlfang' (see manual/057_dragonmaw_retreat.sql)
- 62069 Halgan Redbrand: Turtle C++ script 'boss_halgan_redbrand' (see manual/057_dragonmaw_retreat.sql)
- 62072 Searistrasz: Turtle C++ script 'boss_searistrasz' (see manual/057_dragonmaw_retreat.sql)

## Spell sub (1)

- Dragonmaw Soldier: spell 15663 Cleave -> stand-in 15284 Cleave

## Eventai (1)

- 62263 Dragonmaw Marauder: spell 3019 Enrage -> stand-in 8599 Enrage

## Loot (3)

- 62041: lootid 62041 has no rows in Turtle's creature_loot_template - cleared
- 62055: lootid 62055 has no rows in Turtle's creature_loot_template - cleared
- 62056: lootid 62056 has no rows in Turtle's creature_loot_template - cleared

## Go display added (5)

- 2004238 World GENERIC PASSIVEDOODADS LIGHTS CandleOff01.mdx: new display row
- 2005357 World KALIMDOR DRAGONCAVE PASSIVEDOODADS BLACKDRAGONEGGS Bla: new display row
- 2006139 World KHAZMODAN BLACKROCK PASSIVEDOODADS DragonKinEggs Drago: new display row
- 2020277 Simple Wood Tree: new display row
- 2020280 Simple Wood Tree: new display row

## Turtle only lock (3)

- 2020232 Lower Reserve Gate: lock 1655 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020277 Simple Wood Tree: lock 1665 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020280 Simple Wood Tree: lock 1665 is a Turtle-only lock type (e.g. Survival gathering) - left out

## Area triggers (4)

- Turtle trigger 5343 Dragonmaw Retreat – Front Entrance -> 5914
- Turtle trigger 5346 Dragonmaw Retreat – Back Entrance -> 5915
- Turtle trigger 5344 Dragonmaw Retreat – Front Exit -> 5916
- Turtle trigger 5345 Dragonmaw Retreat – Back Exit -> 5917

## Wmo areas (1)

- 26 WMOAreaTable rows (room names) for WMO ids [7005]

## World map (1)

- WorldMapArea 2010 'DragonmawRetreat' + 0 subzone overlays, 12 map images

## Quest giver flag (1)

- quest-giver flag added to 3.3.5 NPCs [2402] (Shara Blazen)
