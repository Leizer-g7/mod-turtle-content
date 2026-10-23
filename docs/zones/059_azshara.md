# Azshara

File: `data/sql/db-world/mod_turtle_015_azshara.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 2
- conditions: 1
- creature: 48
- creature_addon: 2
- creature_equip_template: 23
- creature_loot_template: 1035
- creature_questender: 61
- creature_queststarter: 61
- creature_template: 50
- creature_template_model: 50
- creature_template_movement: 50
- creature_template_resistance: 6
- gameobject: 348
- gameobject_loot_template: 11
- gameobject_template: 85
- gameobject_template_addon: 16
- gossip_menu: 39
- gossip_menu_option: 6
- npc_text: 39
- npc_vendor: 81
- pickpocketing_loot_template: 7
- pool_gameobject: 25
- pool_pool: 25
- pool_template: 26
- quest_offer_reward: 61
- quest_request_items: 61
- quest_template: 61
- quest_template_addon: 61
- skinning_loot_template: 2
- smart_scripts: 8

## Client tiles (5)

- 0 reshaped chunks next to the zone taken (keep their 3.3.5 area); 1302 reshaped chunks away from the zone left as 3.3.5
- 0 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 24 edge points aligned (largest step 0.48 yd)
- Kalimdor_42_27: merged - 11 of 256 chunks from Turtle
- Kalimdor_43_22: merged - 27 of 256 chunks from Turtle

## Client assets (1)

- 2 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (2)

- 5073 Flaxwhisker Front (subzone of 16, map 1, exploration bit 3769, level 53)
- 5074 Bloodfist Point (subzone of 16, map 1, exploration bit 3770, level 51)

## Seasonal spawns (2)

- 10 creature spawns that Turtle shows only during seasonal events left out
- 70 object spawns that Turtle shows only during seasonal events left out

## Zone quests elsewhere (6)

- quest 40064: given and turned in outside the zone ([8678] / [8678])
- quest 40062: given and turned in outside the zone ([12957] / [12957])
- quest 40063: given and turned in outside the zone ([8678] / [8678])
- quest 41313: given and turned in outside the zone ([8379] / [8379])
- quest 41314: given and turned in outside the zone ([8379] / [8379])
- quest 41315: given and turned in outside the zone ([8379] / [8379])

## Object id taken (1)

- 186425 Torche en sorbier: 3.3.5 uses this id for 'Witchbane Torch' - not spawned

## Cpp script (9)

- 49001 Tarangos: Turtle C++ script 'boss_tarangos' (see manual/059_azshara.sql)
- 61979 Tharessa: Turtle C++ script 'npc_tharessa' (see manual/059_azshara.sql)
- 91283 Lieutenant Azsalus: Turtle C++ script 'generic_spell_ai' (see manual/059_azshara.sql)
- 91350 Magus Bromley: Turtle C++ script 'npc_magus_bromley' (see manual/059_azshara.sql)
- 91722 Keeper Iselus: Turtle C++ script 'npc_iselus' (see manual/059_azshara.sql)
- 91770 Fendo Wobblefizz: Turtle C++ script 'npc_wendo_wobblefizz' (see manual/059_azshara.sql)
- 91775 Analyzor 53G: Turtle C++ script 'analyzor_53' (see manual/059_azshara.sql)
- 92196 Katokar Bladewind: Turtle C++ script 'npc_katokar_bladewind' (see manual/059_azshara.sql)
- 92197 Yharg'osh: Turtle C++ script 'npc_yhargosh' (see manual/059_azshara.sql)

## Display stand in (9)

- 60432 Tide Lord Naszharr: Turtle display 11258 -> stand-in 4036
- 60433 Laszan: Turtle display 11265 -> stand-in 4036
- 60509 Najhaz the Raider: Turtle display 11255 -> stand-in 4036
- 61979 Tharessa: Turtle display 14421 -> stand-in 2220
- 91777 Myrmidon Sasz: Turtle display 11255 -> stand-in 4036
- 91779 Hashaz: Turtle display 11255 -> stand-in 4036
- 91782 Akh Z'ador: Turtle display 18575 -> stand-in 152
- 92024 Dag'grak Bloodfist: Turtle display 18690 -> stand-in 1311
- 92217 Ticas Quirkfuzz: Turtle display 12669 -> stand-in 9819

## Gossip (9)

- menu 12855: text 8254 has Turtle condition 507 (not ported - always shown)
- menu 12855: text 8283 has Turtle condition 508 (not ported - always shown)
- menu 12855: text 8289 has Turtle condition 520 (not ported - always shown)
- menu 12855: text 8291 has Turtle condition 524 (not ported - always shown)
- menu 12855: text 8296 has Turtle condition 518 (not ported - always shown)
- menu 12855 option 0: Turtle condition 440 not ported - option always shown
- menu 12855 option 1: Turtle condition 523 and script 1285501 not ported - option left out
- menu 60077 option 0: Turtle condition 41321 not ported - option always shown
- menu 30191 option 0: Turtle gossip script 30191 -> SmartAI Quest 41320 complete (event)

## Quest scripts (1)

- 40247 Staff of Eldara: Turtle start/complete script 40247/0 (not ported)

## Go display added (30)

- 2002250 World AZEROTH WESTFALL PASSIVEDOODADS RugRacks RugRack01.mdx: new display row
- 2002773 World GENERIC DWARF PASSIVE DOODADS ExcavationBarrierPlank E: new display row
- 2002801 World GENERIC DWARF PASSIVE DOODADS LANTERNS DwarvenHangingL: new display row
- 2002935 World GENERIC GNOME PASSIVE DOODADS FURNITURE GnomeBed01.mdx: new display row
- 2002942 World GENERIC GNOME PASSIVE DOODADS FURNITURE GnomeChair03.m: new display row
- 2002945 World GENERIC GNOME PASSIVE DOODADS FURNITURE GnomeTable03.m: new display row
- 2002973 World GENERIC GNOME PASSIVE DOODADS LIGHTS GnomeMaintenanceL: new display row
- 2002984 World GENERIC GNOME PASSIVE DOODADS Parts GnomeScrew09.mdx: new display row
- 2002992 World GENERIC GNOME PASSIVE DOODADS Pipes GnomePipe04.mdx: new display row
- 2003224 World GENERIC HUMAN PASSIVE DOODADS CRATES CrateGrainLid.mdx: new display row
- 2003225 World GENERIC HUMAN PASSIVE DOODADS CRATES CrateGrainOpen.md: new display row
- 2003646 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin01.md: new display row
- 2003649 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin04.md: new display row
- 2003651 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin06.md: new display row
- 2003652 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin07.md: new display row
- 2003653 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin08.md: new display row
- 2003654 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin09.md: new display row
- 2003655 World GENERIC NIGHTELF PASSIVE DOODADS RUINS AZRElfRuin10.md: new display row
- 2003854 World GENERIC ORC PASSIVE DOODADS FeedingTroughs FeedTroph01: new display row
- 2004147 World GENERIC PASSIVEDOODADS DEATHSKELETONS GnomeMaleDeathSk: new display row
- 2005979 World KALIMDOR WAILINGCAVERNS PASSIVEDOODADS Baskets wc_bask: new display row
- 2005995 World KALIMDOR WAILINGCAVERNS PASSIVEDOODADS FANGDRUIDS WC_S: new display row
- 2006607 World LORDAERON SCHOLOMANCE PASSIVEDOODADS Tapestries Scholm: new display row
- 2007865 World wmo Kalimdor Buildings ClassicalElfRuins AZRClassicalE: new display row
- 2007868 World wmo Kalimdor Buildings ClassicalElfRuins AZRClassicalE: new display row
- 2008211 World wmo Outland DraeniBuildings draeniHutHooded01.wmo: new display row
- 2010849 Way-Stone of Eldarath: new display row
- 2010850 Way-Stone of Dorath: new display row
- 2020299 Star Wood Tree: new display row
- 2020300 Dead Wood Tree: new display row

## Go type changed (4)

- 2007865 World wmo Kalimdor Buildings ClassicalElfRuins AZRClassicalE: type 14 (static WMO) -> 5 (generic)
- 2007868 World wmo Kalimdor Buildings ClassicalElfRuins AZRClassicalE: type 14 (static WMO) -> 5 (generic)
- 2007914 World wmo Kalimdor Buildings NightElfMoonWell DSNightElfMoon: type 14 (static WMO) -> 5 (generic)
- 2008211 World wmo Outland DraeniBuildings draeniHutHooded01.wmo: type 14 (static WMO) -> 5 (generic)

## Turtle only lock (2)

- 2020299 Star Wood Tree: lock 1664 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020300 Dead Wood Tree: lock 1663 is a Turtle-only lock type (e.g. Survival gathering) - left out

## Go no model (1)

- 3000304 Sherpa_Bedroll_2: Turtle-only model with no stand-in (add one to go_model_substitutions)

## Pools (1)

- 26 spawn pools (25 objects, 0 creatures)

## Objects waiting for the client patch (1)

- 3000304 Sherpa_Bedroll_2 - `world\EXPANSION04\DOODADS\Sherpa\Sherpa_Bedroll_02.mdx`
