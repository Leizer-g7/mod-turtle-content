# Stranglethorn Vale

File: `data/sql/db-world/mod_turtle_014_stranglethorn_vale.sql`  
Terrain mode: **turtle**

## Counts

- areatable_dbc: 1
- creature: 43
- creature_addon: 2
- creature_default_trainer: 1
- creature_equip_template: 23
- creature_loot_template: 366
- creature_questender: 48
- creature_queststarter: 48
- creature_template: 47
- creature_template_addon: 1
- creature_template_model: 47
- creature_template_movement: 47
- creature_text: 1
- gameobject: 356
- gameobject_loot_template: 13
- gameobject_questender: 3
- gameobject_queststarter: 3
- gameobject_template: 75
- gameobject_template_addon: 17
- gossip_menu: 22
- npc_text: 22
- npc_vendor: 93
- quest_offer_reward: 51
- quest_request_items: 51
- quest_template: 51
- quest_template_addon: 51
- skinning_loot_template: 4
- smart_scripts: 4
- trainer: 1
- trainer_spell: 2
- waypoint_data: 1

## Client tiles (5)

- 0 reshaped chunks next to the zone taken (keep their 3.3.5 area); 0 reshaped chunks away from the zone left as 3.3.5
- 0 edge points where Turtle's own tiles do not meet: both sides set to the average
- seams between Turtle and 3.3.5 chunks: 14 edge points aligned (largest step 0.05 yd)
- Azeroth_32_59: merged - 16 of 256 chunks from Turtle
- Azeroth_33_59: merged - 10 of 256 chunks from Turtle

## Client assets (1)

- 0 Turtle files (buildings, textures) shipped in the client patch

## Model stand in (4)

- WORLD\AZEROTH\DUSKWOOD\BUILDINGS\GYPSYWAGON\GYPSYWAGON2.M2 -> World\Azeroth\Duskwood\Buildings\GypsyWagon\GypsyWagon.m2
- WORLD\KALIMDOR\BALOR\PASSIVEDOODADS\WATERFALLS\WaterfallRed.MDX -> World\Kalimdor\Mauradon\PassiveDoodads\Waterfalls\MaraudonCorruptedFalls03.m2
- World\Azeroth\balor\shield_crest_a_02balor.MDX -> World\Azeroth\Elwynn\PassiveDoodads\BattleGladeShield1\BattleGladeShield1.m2
- world\azeroth\Balor\BalorThrone.MDX -> World\Azeroth\Karazahn\PassiveDoodads\Throne\KarazahnThrone01.m2

## New areas (1)

- 5084 Bloodsail Retreat (subzone of 33, map 0, exploration bit 3768, level 48)

## Seasonal spawns (2)

- 31 creature spawns that Turtle shows only during seasonal events left out
- 264 object spawns that Turtle shows only during seasonal events left out

## Existing templates (2)

- 2 creature spawns of 2 templates 3.3.5 already has (AzerothCore's template is used)
- 8 object spawns of 2 templates 3.3.5 already has (herbs, ore, chests ...)

## Zone quests elsewhere (2)

- quest 60155: given and turned in outside the zone ([6807] / [6807])
- quest 40970: given and turned in outside the zone ([2498] / [2498])

## Cpp script (9)

- 51607 Morgan the Storm: Turtle C++ script 'npc_morgan_the_storm' (see manual/058_stranglethorn_vale.sql)
- 60450 Gold-Tooth Gary: Turtle C++ script 'npc_agne_gambler' (see manual/058_stranglethorn_vale.sql)
- 60453 Garfield Sparkblast: Turtle C++ script 'npc_garfield_sparkblast' (see manual/058_stranglethorn_vale.sql)
- 60459 Vil'do One-Tusk: Turtle C++ script 'npc_vildo_onetusk' (see manual/058_stranglethorn_vale.sql)
- 60496 Garfield Sparkblast: Turtle C++ script 'npc_garfield_sparkblast' (see manual/058_stranglethorn_vale.sql)
- 60643 Fazgel Mechaflame: Turtle C++ script 'npc_fazgel_mechaflame' (see manual/058_stranglethorn_vale.sql)
- 60644 Arcanist Sovatir: Turtle C++ script 'npc_sovatir' (see manual/058_stranglethorn_vale.sql)
- 80269 Kin'Tozo: Turtle C++ script 'boss_kintozo' (see manual/058_stranglethorn_vale.sql)
- 91282 Shalgrig Pipeshack: Turtle C++ script 'npc_shalgrig' (see manual/058_stranglethorn_vale.sql)

## Display stand in (16)

- 60447 Fishface Joe: Turtle display 18706 -> stand-in 10299
- 60448 Dirty Jacob: Turtle display 18703 -> stand-in 19308
- 60449 Sark Blacktooth: Turtle display 18717 -> stand-in 27853
- 60450 Gold-Tooth Gary: Turtle display 18708 -> stand-in 3259
- 60451 Jessie Sugar-Tongue: Turtle display 18710 -> stand-in 4462
- 60452 First Mate McCoy: Turtle display 18705 -> stand-in 9333
- 60453 Garfield Sparkblast: Turtle display 18707 -> stand-in 12669
- 60454 Old-Tide Sam: Turtle display 18713 -> stand-in 2464
- 60456 Belgrush Daggerfist: Turtle display 18701 -> stand-in 1282
- 60458 One-Ear Nellie: Turtle display 18714 -> stand-in 3347
- 60459 Vil'do One-Tusk: Turtle display 18722 -> stand-in 15502
- 60460 'Ale Saint' Grida: Turtle display 18709 -> stand-in 12549
- 60496 Garfield Sparkblast: Turtle display 18707 -> stand-in 12669
- 60642 Arcanist Sovatir: Turtle display 14420 -> stand-in 12044
- 60644 Arcanist Sovatir: Turtle display 14420 -> stand-in 12044
- 91281 Spanessa Fogwater: Turtle display 15300 -> stand-in 15300

## Go display added (33)

- 2001872 World AZEROTH ELWYNN PASSIVEDOODADS ELWYNNFENCES ElwynnFence: new display row
- 2002006 World AZEROTH REDRIDGE PASSIVEDOODADS Docks RedRidgeDocks01.: new display row
- 2002030 World AZEROTH STRANGLETHORN BUILDINGS CRASHZEPPELIN CrashZep: new display row
- 2002233 World AZEROTH WESTFALL PASSIVEDOODADS GrindStone GrindStone.: new display row
- 2002409 World DUNGEON SCARLETMONASTERY PASSIVEDOODADS STATUES statue: new display row
- 2002518 World EXPANSION01 DOODADS GENERIC Tradeskill JewelCrafting J: new display row
- 2002776 World GENERIC DWARF PASSIVE DOODADS ExcavationBarrierPlank E: new display row
- 2002796 World GENERIC DWARF PASSIVE DOODADS GUNRACKS GunRack02D.mdx: new display row
- 2002894 World GENERIC DWARF PASSIVE DOODADS TARGETS TargetAxe03.mdx: new display row
- 2002896 World GENERIC DWARF PASSIVE DOODADS TARGETS TargetHammer02.m: new display row
- 2003047 World GENERIC HUMAN PASSIVE DOODADS Anchors BootyAnchor.mdx: new display row
- 2003211 World GENERIC HUMAN PASSIVE DOODADS CLOTH ClothBoltBlue.mdx: new display row
- 2003259 World GENERIC HUMAN PASSIVE DOODADS Clothing BootsLeatherDar: new display row
- 2003260 World GENERIC HUMAN PASSIVE DOODADS Clothing ClothYarnBallRe: new display row
- 2003261 World GENERIC HUMAN PASSIVE DOODADS Clothing ClothYarnBallYe: new display row
- 2003271 World GENERIC HUMAN PASSIVE DOODADS Clothing HangingPantsGre: new display row
- 2003463 World GENERIC HUMAN PASSIVE DOODADS ShopCounter DuskwoodShop: new display row
- 2003787 World GENERIC OGRE PASSIVE DOODADS TORCHES OgreWallTorch.mdx: new display row
- 2003862 World GENERIC ORC PASSIVE DOODADS Hammocks Hammock02.mdx: new display row
- 2004392 World GENERIC PASSIVEDOODADS ShieldRacks RackShieldHorde01.m: new display row
- 2004505 World GENERIC PASSIVEDOODADS WeaponCrates WeaponCrateHordeAx: new display row
- 2005111 World KALIMDOR AZSHARA PASSIVEDOODADS Seashells AzsharaShell: new display row
- 2005112 World KALIMDOR AZSHARA PASSIVEDOODADS Seashells AzsharaShell: new display row
- 2005317 World KALIMDOR DIREMAUL PassiveDoodads GoldenHighElfStatue03: new display row
- 2006327 World KHAZMODAN ULDAMAN PASSIVEDOODADS Debris UldamanScrollD: new display row
- 2008678 World EXPANSION01 DOODADS GENERIC BLOODELF INSTRUMENTS BE_Ha: new display row
- 2008679 World EXPANSION01 DOODADS GENERIC BLOODELF INSTRUMENTS BE_Lu: new display row
- 2010377 World Generic HUMAN PASSIVE DOODADS Artwork Painting14.mdx: new display row
- 2010871 Lyvdia Dawnbird: new display row
- 2010872 Highborne Golden Statue: new display row
- 2020288 Shade Wood Tree: new display row
- 2020298 Tropical Wood Tree: new display row
- 3000305 Goblin_Oildrum_01: stand-in display 6904 (World\Generic\Human\Passive Doodads\OilDrums\oildrum01.mdx)

## Go type changed (1)

- 2008270 World wmo transports transport_ship transportship.wmo: type 14 (static WMO) -> 5 (generic)

## Go no model (3)

- 2010685 worldgenericpassivedoodadsthanksgivingg_thanksgivingtable_01: Turtle-only model with no stand-in (add one to go_model_substitutions)
- 3000303 Sherpa_Bedroll_0: Turtle-only model with no stand-in (add one to go_model_substitutions)
- 3000304 Sherpa_Bedroll_2: Turtle-only model with no stand-in (add one to go_model_substitutions)

## Turtle only lock (2)

- 2020288 Shade Wood Tree: lock 1661 is a Turtle-only lock type (e.g. Survival gathering) - left out
- 2020298 Tropical Wood Tree: lock 1662 is a Turtle-only lock type (e.g. Survival gathering) - left out

## Quest giver flag (1)

- quest-giver flag added to 3.3.5 NPCs [2663, 6807] (Narkk, Innkeeper Skindle)

## Objects waiting for the client patch (3)

- 2010685 worldgenericpassivedoodadsthanksgivingg_thanksgivingtable_01_collision - `World\Expansion03\Doodads\Steamwheedle\Steamwheedle_Banner_01.mdx`
- 3000303 Sherpa_Bedroll_0 - `world\EXPANSION04\DOODADS\Sherpa\Sherpa_Bedroll_01.mdx`
- 3000304 Sherpa_Bedroll_2 - `world\EXPANSION04\DOODADS\Sherpa\Sherpa_Bedroll_02.mdx`
