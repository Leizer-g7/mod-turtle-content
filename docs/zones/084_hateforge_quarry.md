# Hateforge Quarry

File: `data/sql/db-world/mod_turtle_040_hateforge_quarry.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 2
- creature: 346
- creature_addon: 161
- creature_equip_template: 12
- creature_loot_template: 1474
- creature_template: 17
- creature_template_model: 27
- creature_template_movement: 17
- creature_template_resistance: 7
- gameobject: 44
- gameobject_loot_template: 2
- gameobject_template: 8
- gameobject_template_addon: 3
- smart_scripts: 12
- waypoint_data: 377

## Client tiles (9)

- Hateforge_37_46: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 196 object ids moved
- Hateforge_38_46: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 2 object ids moved
- Hateforge_39_46: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Hateforge_37_47: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 50 object ids moved
- Hateforge_38_47: 0 empty-liquid offsets fixed, 17 duplicated water layers collapsed, 17 legacy liquid blocks dropped, 570 object ids moved
- Hateforge_39_47: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 1 object ids moved
- Hateforge_37_48: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 0 object ids moved
- Hateforge_38_48: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 0 object ids moved
- Hateforge_39_48: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 0 legacy liquid blocks dropped, 0 object ids moved

## Client assets (1)

- 1 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (2)

- 5098 Hateforge Quarry (zone, map 808, exploration bit 3825, level 50)
- 5103 Hateforge Quarry (zone, map 808, exploration bit 3824, level 50)

## Existing templates (2)

- 1 creature spawns of 1 templates 3.3.5 already has (AzerothCore's template is used)
- 14 object spawns of 5 templates 3.3.5 already has (herbs, ore, chests ...)

## Display stand in (23)

- 60717 Hateforge Chemist: Turtle display 18836 -> stand-in 7916
- 60717 Hateforge Chemist: Turtle display 18837 -> stand-in 4042
- 60718 Hateforge Cleric: Turtle display 18838 -> stand-in 1568
- 60718 Hateforge Cleric: Turtle display 18839 -> stand-in 25023
- 60719 Hateforge Craftsman: Turtle display 18840 -> stand-in 7766
- 60719 Hateforge Craftsman: Turtle display 18841 -> stand-in 5529
- 60720 Hateforge Engineer: Turtle display 18842 -> stand-in 8593
- 60721 Hateforge Miner: Turtle display 18843 -> stand-in 1893
- 60721 Hateforge Miner: Turtle display 18844 -> stand-in 8729
- 60722 Hateforge Overseer: Turtle display 18845 -> stand-in 9816
- 60722 Hateforge Overseer: Turtle display 18846 -> stand-in 8820
- 60723 Hateforge Taskmaster: Turtle display 18847 -> stand-in 4969
- 60723 Hateforge Taskmaster: Turtle display 18848 -> stand-in 7794
- 60724 Hateforge Warden: Turtle display 18849 -> stand-in 5752
- 60725 Twilight Fireblade: Turtle display 18851 -> stand-in 10331
- 60725 Twilight Fireblade: Turtle display 18852 -> stand-in 9633
- 60725 Twilight Fireblade: Turtle display 18853 -> stand-in 12989
- 60726 Twilight Shadowcaller: Turtle display 18854 -> stand-in 7609
- 60726 Twilight Shadowcaller: Turtle display 18855 -> stand-in 20948
- 60726 Twilight Shadowcaller: Turtle display 18856 -> stand-in 11734
- 60735 High Foreman Bargul Blackhammer: Turtle display 18850 -> stand-in 3054
- 60736 Engineer Figgles: Turtle display 18832 -> stand-in 6710
- 60737 Har'gesh Doomcaller: Turtle display 18833 -> stand-in 2870

## Cpp script (7)

- 60718 Hateforge Cleric: Turtle C++ script 'mob_hateforge_cleric' (see manual/084_hateforge_quarry.sql)
- 60723 Hateforge Taskmaster: Turtle C++ script 'mob_hateforge_taskmaster' (see manual/084_hateforge_quarry.sql)
- 60725 Twilight Fireblade: Turtle C++ script 'mob_twilight_fireblade' (see manual/084_hateforge_quarry.sql)
- 60734 Hatereaver Annihilator: Turtle C++ script 'boss_hatereaver_annhilator' (see manual/084_hateforge_quarry.sql)
- 60735 High Foreman Bargul Blackhammer: Turtle C++ script 'boss_bargul_blackhammer' (see manual/084_hateforge_quarry.sql)
- 60736 Engineer Figgles: Turtle C++ script 'boss_engineer_figgles' (see manual/084_hateforge_quarry.sql)
- 60737 Har'gesh Doomcaller: Turtle C++ script 'boss_hargesh_doomcaller' (see manual/084_hateforge_quarry.sql)

## Spell sub (3)

- Hateforge Engineer: spell 56523 Decoy Dragonling -> stand-in 12749 Mithril Mechanical Dragonling
- Hateforge Overseer: spell 56520 Hateforge Aura -> stand-in 41106 Battle Aura
- Twilight Shadowcaller: spell 56519 Twilight Shadow -> stand-in 17228 Shadow Bolt Volley

## Area triggers (2)

- Turtle trigger 5009 Hateforge Quarry - Entrance -> 5931
- Turtle trigger 5013 Hateforge Quarry - Exit -> 5932

## World map (1)

- WorldMapArea 2015 'HateforgeQuarry' + 0 subzone overlays, 12 map images
