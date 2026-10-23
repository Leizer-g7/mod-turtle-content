# Gilneas City

File: `data/sql/db-world/mod_turtle_007_gilneas_city.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 2
- creature: 340
- creature_addon: 123
- creature_equip_template: 10
- creature_loot_template: 834
- creature_template: 21
- creature_template_addon: 1
- creature_template_model: 28
- creature_template_movement: 21
- creature_template_resistance: 2
- creature_text: 19
- gameobject: 269
- gameobject_loot_template: 13
- gameobject_template: 106
- gameobject_template_addon: 9
- skinning_loot_template: 4
- smart_scripts: 40
- waypoint_data: 250

## Client tiles (16)

- Giln_25_32: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_25_33: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_25_34: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_25_35: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_26_32: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_26_33: 0 empty-liquid offsets fixed, 211 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 122 object ids moved
- Giln_26_34: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 236 object ids moved
- Giln_26_35: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 39 object ids moved
- Giln_27_32: 0 empty-liquid offsets fixed, 210 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_27_33: 0 empty-liquid offsets fixed, 146 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 55 object ids moved
- Giln_27_34: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 1533 object ids moved
- Giln_27_35: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 526 object ids moved
- Giln_28_32: 0 empty-liquid offsets fixed, 168 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 0 object ids moved
- Giln_28_33: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 501 object ids moved
- Giln_28_34: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 1099 object ids moved
- Giln_28_35: 0 empty-liquid offsets fixed, 0 duplicated water layers collapsed, 256 legacy liquid blocks dropped, 992 object ids moved

## Client assets (1)

- 106 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (2)

- 5208 Gilneas City (zone, map 815, exploration bit 3711, level 43)
- 5209 Greymane Tower (subzone of 5208, map 815, exploration bit 3712, level 46)

## Existing templates (2)

- 42 creature spawns of 1 templates 3.3.5 already has (AzerothCore's template is used)
- 3 object spawns of 2 templates 3.3.5 already has (herbs, ore, chests ...)

## Display stand in (21)

- 61263 Regent-Lady Celia Harlow: Turtle display 19140 -> stand-in 1446
- 61264 Regent-Lord Mortimer Harlow: Turtle display 19160 -> stand-in 2531
- 61364 Greymane Arbalest: Turtle display 20263 -> stand-in 2594
- 61364 Greymane Arbalest: Turtle display 20264 -> stand-in 3918
- 61365 Greymane Knight: Turtle display 20277 -> stand-in 10554
- 61365 Greymane Knight: Turtle display 20278 -> stand-in 10557
- 61388 Greymane Elite: Turtle display 20267 -> stand-in 4321
- 61388 Greymane Elite: Turtle display 20268 -> stand-in 25599
- 61389 Greymane Footman: Turtle display 20273 -> stand-in 3985
- 61389 Greymane Footman: Turtle display 20274 -> stand-in 2482
- 61390 Greymane Noble: Turtle display 20281 -> stand-in 3322
- 61390 Greymane Noble: Turtle display 20282 -> stand-in 27848
- 61391 Greymane Cleric: Turtle display 20265 -> stand-in 28364
- 61391 Greymane Cleric: Turtle display 20266 -> stand-in 11898
- 61417 Greymane Justicar: Turtle display 20313 -> stand-in 1499
- 61418 Genn Greymane: Turtle display 20311 -> stand-in 13450
- 61419 Matthias Holtz: Turtle display 20320 -> stand-in 2607
- 61421 Judge Sutherland: Turtle display 20334 -> stand-in 1292
- 61422 Dustivan Blackcowl: Turtle display 20309 -> stand-in 10536
- 61423 Marshal Magnus Greystone: Turtle display 20319 -> stand-in 1427
- 61604 Gilneas Stable Horse: Turtle display 20424 -> stand-in 8469

## Cpp script (5)

- 61263 Regent-Lady Celia Harlow: Turtle C++ script 'boss_celia' (see manual/051_gilneas_city.sql)
- 61264 Regent-Lord Mortimer Harlow: Turtle C++ script 'boss_lord_mortimer' (see manual/051_gilneas_city.sql)
- 61365 Greymane Knight: Turtle C++ script 'greymane_knight' (see manual/051_gilneas_city.sql)
- 61390 Greymane Noble: Turtle C++ script 'greymane_noble' (see manual/051_gilneas_city.sql)
- 61418 Genn Greymane: Turtle C++ script 'genn_greymane' (see manual/051_gilneas_city.sql)

## Spell sub (1)

- Darkpelt Rager: spell 9754 Swipe -> stand-in 31279 Swipe

## Eventai (1)

- 61424 Darkpelt Rager: spell 28131 Enrage -> stand-in 8599 Enrage

## Loot (1)

- 61604: lootid 61604 has no rows in Turtle's creature_loot_template - cleared

## Go display added (41)

- 2000712 SPELLS Creature_ScourgeRuneCircleCrystal.mdx: stand-in display 6679 (World\Goober\G_ScourgeRuneCircleCrystal.mdx)
- 2002394 World DUNGEON GoldshireInn InnChandelier InnChandelier.mdx: new display row
- 2002411 World DUNGEON SCARLETMONASTERY PASSIVEDOODADS STATUES statue: new display row
- 2002707 World GENERIC DWARF PASSIVE DOODADS Bookshelves BookshelfDwa: new display row
- 2002792 World GENERIC DWARF PASSIVE DOODADS GUNRACKS GunRack01D.mdx: new display row
- 2002875 World GENERIC DWARF PASSIVE DOODADS TABLES DwarvenTableLarge: new display row
- 2002885 World GENERIC DWARF PASSIVE DOODADS TABLES DwarvenTableSimpl: new display row
- 2003066 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorHelmGreen.mdx: new display row
- 2003070 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorHelmVisorBlue: new display row
- 2003075 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorLeatherHelmBl: new display row
- 2003078 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorLeatherHelmBr: new display row
- 2003087 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorLeatherShould: new display row
- 2003089 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorLeatherShould: new display row
- 2003099 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorMailHangingRe: new display row
- 2003100 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorShoulderBlue.: new display row
- 2003101 World GENERIC HUMAN PASSIVE DOODADS Armor ArmorShoulderGold.: new display row
- 2003109 World GENERIC HUMAN PASSIVE DOODADS Artwork Painting07.mdx: new display row
- 2003117 World GENERIC HUMAN PASSIVE DOODADS Artwork Painting15.mdx: new display row
- 2003266 World GENERIC HUMAN PASSIVE DOODADS Clothing HangingCloakBlu: new display row
- 2003347 World GENERIC HUMAN PASSIVE DOODADS GunShop GunShopMortar.md: new display row
- 2003355 World GENERIC HUMAN PASSIVE DOODADS GunShop GunTripod.mdx: new display row
- 2003401 World GENERIC HUMAN PASSIVE DOODADS Mops mop.mdx: new display row
- 2003430 World GENERIC HUMAN PASSIVE DOODADS RUGS KarazahnRugOrange.m: new display row
- 2003531 World GENERIC HUMAN PASSIVE DOODADS TortureDevices GeneralIr: new display row
- 2003532 World GENERIC HUMAN PASSIVE DOODADS TortureDevices GeneralRa: new display row
- 2004373 World GENERIC PASSIVEDOODADS SKELETONS ChainedSkeleton01.mdx: new display row
- 2004374 World GENERIC PASSIVEDOODADS SKELETONS ChainedSkeleton02.mdx: new display row
- 2004435 World GENERIC PASSIVEDOODADS Thanksgiving G_PilgrimHat.mdx: new display row
- 2004502 World GENERIC PASSIVEDOODADS WeaponCrates WeaponCrateAllianc: new display row
- 2004785 World GENERIC UNDEAD PASSIVE DOODADS STONEFENCE UndeadFenceP: new display row
- 2005544 World KALIMDOR MAURADON PASSIVEDOODADS BRIDGEBRAZIERS Bridge: new display row
- 2006206 World KHAZMODAN IRONFORGE PASSIVEDOODADS MUSEUMEXHIBITS Dwar: new display row
- 2006588 World LORDAERON SCHOLOMANCE PASSIVEDOODADS CANDLES Scholme_C: new display row
- 2010662 Nifty_StopWatch: new display row
- 2010682 WorldExpansion02DoodadsGenericInscriptionInscription_Quill_F: new display row
- 2020006 Shoemaker and Co.: new display row
- 2020007 The Luring Rod: new display row
- 2020008 Flappy Chicken: new display row
- 2020011 Orven Vintage Limited: new display row
- 2020012 Gilneas City Customs: new display row
- 2020056 Painting of Mia: new display row

## Area triggers (2)

- Turtle trigger 5014 Gilneas City - Entrance -> 5908
- Turtle trigger 5015 Gilneas City - Exit -> 5909

## Wmo areas (1)

- 9 WMOAreaTable rows (room names) for WMO ids [5196]

## World map (1)

- WorldMapArea 2005 'GilneasCity' + 0 subzone overlays, 12 map images

## Lights (1)

- Light 4016 (Turtle 546) params [3017, 3018, 3019, 3018, 4]

## Script spells (1)

- spell 2495 Holy Strike -> stand-in 13953 Holy Strike
