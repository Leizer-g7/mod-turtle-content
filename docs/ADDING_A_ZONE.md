# Adding a zone

The converter is `tools/turtle2ac/build.py`. It reads three things:
- the Turtle world DB (`tw_world`), loaded from the Tortoise-WoW repo: `sql/create_databases.sql` (only the `tw_world` part), every file in `sql/base`, then every `sql/database_updates/world` file in name order
- a **pristine** `acore_world`, without this module applied, so collisions are detected correctly. It must come from the **server's own world DB** (a dump of it with this module rolled back), not from upstream AzerothCore: the server's core (Grimfeather `b4bbae96`) names columns differently (`creature.id`, not `id1`), and its other modules add rows (mod-individual-progression adds MapDifficulty rows right after the stock ids). Every INSERT is checked against this DB's column list, and the build stops on an unknown column.
- the 3.3.5 client tables, from `client335_extract.py` run on the **players' client** (the HD client with its letter patches), not a backup copy. Each table the patch ships is that client's winning copy plus the module's rows.
- the Turtle and AzerothCore server data: `dbc/` and `maps/`

It writes `data/sql/db-world/`, `sql_rollback/`, `client/` and `docs/`.

## Steps

1. **Create a zone file** at `tools/turtle2ac/zones/<zone_id>_<slug>.json`. Copy `045_arathi_highlands.json` and change these fields:
   - `name`, `zone_id` (AreaTable ID of the zone) and `map`
   - `slot`: next free number. It fixes the zone's GUID block and file number. Never reuse a slot.
   - `terrain`: `turtle` when Turtle changed the zone's map tiles and you convert them; `stock` otherwise.
   - `terrain_tiles`: the `X_Y` of every `Azeroth_X_Y.adt` (or Kalimdor) tile Turtle edited.
     Tile names are `Azeroth_<x>_<y>` with **x = 32 - worldY / 533.33 and y = 32 - worldX / 533.33** (world X runs north). Swapping them sends the extractor to the wrong part of the map (it happened once with Gilneas). Get them with the extractor (`turtle_extract.py`); the tiles must be in its `assets` folder.
   - `area_bits`: one exploration bit per new Turtle subzone. Use the next free number after the last zone's, and never change one later. The build stops if a bit is taken, and suggests one if it's missing.
   - `exclude_creatures` / `exclude_gameobjects`: Turtle-only systems such as events, player-housing objects, or companions.
   - `hold_until_terrain_patch`: Turtle subzones whose terrain was rebuilt.
   - `force_display`: creature entry -> 3.3.5 display id, for Turtle-made models with no 3.3.5 file, and for a display the automatic match misses although 3.3.5 has it (Corrosis in Hateforge Quarry: display 5497, Viscous Fallout's).
   - `exclude_quests`: quests that depend on Turtle server code that can't be ported.
   - For **new land** (an area 3.3.5 does not have at all, like Balor), see `046_balor.json`:
     - `spawn_existing_templates: true` also spawns the creatures/objects 3.3.5 already has (herbs, ore, critters, spirit healer), with their spawn pools.
     - `ship_assets: true` ships the Turtle buildings (WMO) and textures the tiles use, plus their minimap images. Turtle models (.m2) are never shipped (1.12 format); `config.json` -> `m2_substitutions` rewrites them to a 3.3.5 model.
     - Tiles the 3.3.5 client lacks are added to its continent WDT automatically.
     - `area_templates`: the 3.3.5 zone whose flags a new zone copies (Balor uses Duskwood).
     - `world_map`, `taxi_nodes`, `graveyards`, `lights`, `wmo_area_ids`: world map + subzone overlays, flight masters and paths, graveyards, sky/fog, and room/building names, all from Turtle's DBCs.
   - For **land Turtle shares with live 3.3.5 content** (Northwind against Stormwind City, the harbor, Dun Morogh and Searing Gorge), see `048_northwind.json`:
     - `merge_region` (`x`, `y` tile ranges, `height_tolerance`): each tile in the range is the 3.3.5 tile with Turtle's chunks merged in. A chunk is taken from Turtle when Turtle marks it as this zone, or when Turtle's ground there differs by more than `height_tolerance` yards (those chunks keep their 3.3.5 area id). Shared edges are then aligned. Objects are kept by where they stand; a 3.3.5 building is only removed when its whole footprint is on Turtle chunks.
     - The 3.3.5 tiles come from `client335_extract.py` (`config.json` → `client335`); archives in `client335_skip_archives` (the HD patches) are not used as the base.
     - `"reshaped": "connected"` takes Turtle's reshaped ground only where it touches the zone (Grim Reaches); the default `"all"` takes every reshaped chunk in the region (Northwind).
     - Turtle land on deep 3.3.5 open sea (Gillijim's Isle): every Turtle chunk differs from the 3.3.5 sea floor (about -516), so `"connected"` would run on into neighbouring Turtle zones. Use `"reshaped": "sea"`: the zone's chunks plus the Turtle sea bed reached from it through chunks under water in both tiles (`sea_below`, default -2), never in a zone listed in `reshaped_skip_zones` (a Turtle zone not ported yet), only on the tiles in `sea_take` and never next to a tile outside the merge. Pad `x`/`y` by one tile so the margin tiles are seam partners.
     - `ocean_base`: a stock open-sea tile (e.g. `World\\Maps\\Azeroth\\Azeroth_25_56.adt`) used, moved, where 3.3.5 has no tile at all; such a tile is shipped only if it gets Turtle chunks, is added to the client WDT, and its other edges take the heights of the 3.3.5 tiles next to it (HD patches fill some world-edge tiles with flat ground at 0).
     - `"stitch_onto": "donor"`: at the seams the 3.3.5 side moves onto Turtle's ground (default `"base"` moves Turtle's edge onto 3.3.5, which pulled the island's edge 500 yards down where it met unported Lapidis Isle). Only where no 3.3.5 spawn or object stands on the region; a 3.3.5 tile whose floor was raised is shipped.
     - `"heal_turtle_seams": true`: where two of Turtle's own tiles do not meet (up to 5 yards at some borders), both edges get the average.
     - `"take_unnamed_land": true`: Turtle chunks whose area id is not in Turtle's AreaTable (small islets) are taken with the sea bed.
     - Zones sharing tiles (Gillijim's Isle and Lapidis Isle): a tile an earlier zone of the build already ships is the base of the next zone's merge, so both zones' chunks stay; the minimap image follows the total of Turtle chunks.
   - `spawns_in_whole_region`: look for the zone's spawns over the whole merge region, not only Turtle's world-map rectangle (opt-in: it would add 13 NPCs and 125 objects to Northwind, not checked yet).
   - `extra_spawns` / `extra_gameobject_spawns` (Turtle guids): quest NPCs and objects outside the zone. Each keeps its own map (a bug put Kalimdor extra spawns on map 0 until 2026-10-07).
   - `extra_quests`: a quest of the zone's chains that Turtle files under another zone (Tel'Abim: "Operation Help Jabbey", a Blackrock Depths step between two Tel'Abim quests). Its giver and turn-in must exist in 3.3.5 or in the build, or the build stops.
   - Kalimdor zones (`"map": 1`, Tel'Abim) work like Azeroth ones: `client335_extract.py` pulls the Kalimdor tiles and `Kalimdor.wdt`, the island options apply unchanged, and `ocean_base` is a Kalimdor open-sea tile. A spawn on a 3.3.5 tile outside the merge region keeps Turtle's height; check it against the server's `.map` tiles (Gelwig Darkbrow stood 1.2 yards under the 3.3.5 ground of Steamwheedle Port and is raised in `manual/054_tel_abim.py`).
   - Trainers: a creature is a trainer only when Turtle gives it the trainer flag (16). Turtle keeps `npc_trainer` rows on hunter NPCs, their pets and tamable beasts; before 2026-10-07 those became trainers here (Sneel Fizzwack, Dark Ranger Anya, Ragnaz, Misthoof Stags ...).
   - Gossip options that only run a Turtle script the build cannot port, behind a Turtle condition it cannot port (the Hallow's End "Trick or Treat!" on innkeepers), are left out instead of showing all year and doing nothing.
   - A subzone is put on its zone's map (Turtle's Barkskin Hold row says map 0).
   - `S.stock_quest_drops`: a row is quest-only only where Turtle's chance is negative (Arcane Essence drops normally on Turtle).
   - SmartAI targets: `player_range` (17, params min, max distance) gives a credit to everyone near after a scripted event (Ralathius's ritual).
   - For **a 3.3.5 zone Turtle reworked** (the Wetlands), see `056_wetlands.json`: the 3.3.5 zone, its spawns and quests stay; Turtle's additions are merged in.
     - `merge_region.own: "changed"`: only the zone's chunks that Turtle reshaped or gave a new subzone are taken (the default `"all"` takes every chunk Turtle marks as the zone). `own_exclude_areas`: the zone's areas that are not its own ground (the Wetlands' sea areas, which Turtle reshaped for Grim Reaches).
     - `reshaped: "connected"` with `connect_depth`: Turtle's reshaped ground at most that many chunks around the taken chunks (the Wetlands needs 8 for Turtle's Dun Morogh slopes under Dun Agrath; with 2 the seams stepped up to 28 yd). `reshaped: "none"` takes nothing outside the zone. The zone report lists every seam step over 5 yd with its world position.
     - `drop_removed_wmos`: a 3.3.5 building whose origin is in a taken chunk and that Turtle's tile no longer has (Turtle replaced 3.3.5's Grim Batol entrance with its own) is removed even if it reaches 3.3.5 chunks.
     - `spawn_existing_in_subzones` (Turtle area ids): Turtle's spawns of 3.3.5 templates (critters, guards, furniture) only inside Turtle's new subzones, never within 5 yd of a 3.3.5 spawn of the same template; `spawn_existing_skip`: 3.3.5 NPCs Turtle moved there (they stay where 3.3.5 has them).
     - `config.json` → `area_id_remap`: Turtle area ids that 3.3.5 uses for another area (Turtle reused Northrend ids: Hawk's Vigil 4018, Dun Agrath 4019) get a new id in the shipped tiles, AreaTable, quest sort, WMOAreaTable and world-map overlays. `area_bits` keep the Turtle id as key.
     - `S.stock_spawn(table, guid, position_z=...)`: moves a 3.3.5 spawn (with rollback) where Turtle changed its ground; find them with the ground check (3.3.5 spawns on the changed tiles).
     - `S.stock_spawn_remove(table, guid)`: deletes a 3.3.5 spawn Turtle removed because it built something there (three Skymane Gorillas inside Bloodsail Retreat); the rollback re-inserts the whole row. It refuses spawns with addon, pool, event, formation, linked-respawn or SmartAI rows.
     - `zone_from_335_tiles: true` (Stranglethorn): where Turtle did not change a tile (it was not extracted), the zone and subzone of a spawn come from the 3.3.5 tile's chunk areas; Turtle's server maps miss the north of Stranglethorn.
     - `reshaped_skip_zones` also works with `"reshaped": "connected"` (Azshara): the flood never enters ground Turtle gave to those zones (Moonwhisper Coast, a Turtle zone not ported; Hyjal, already merged; Winterspring). Leave out a reworked area whose new ground belongs to another zone's content with `own_exclude_areas` (Azshara's Timbermaw Hold / Ursolan, reshaped by up to 72 yd for Winterspring's furbolg village and the Timbermaw Hold raid).
     - A gossip menu a Turtle C++ script sends can have no npc_text row in Turtle's DB (the client shows its generic greeting): give `npc_text(id, default)` a short line (the Way-Stones of Eldarath).
     - A Turtle custom exploration trigger object (`custom_exploration_trigger`, credit to players within 30 yd) becomes a SmartGameObjectAI row: update-OOC every 2.5 s, kill credit to `player_range` 0-30 (Lake Mennar).
     - `S.stock_gossip_option(menu, option_id, text, icon, conds)`: adds an option (ids 50+) to a 3.3.5 gossip menu, with conditions; the rollback deletes it (Baron Revilgaz's "Making a Statement").
     - Reputation that Turtle sets in C++ (`SetReputation`) cannot be set by SmartAI: give it as a quest reward (`RewardFactionID`/`RewardFactionOverride` = value x 100, in the manual script). Bloodsail Buccaneers start at -6500 for every race and have no spillover, so +6500 lands a fresh character exactly on Neutral; Booty Bay passes half of any change to Gadgetzan, Everlook and Ratchet (Faction.dbc parent 169).
   - Spawns Turtle shows only during a seasonal event (`game_event_creature` / `game_event_gameobject` with event > 0: Hallow's End, Midsummer, Winter Veil ...) are left out: the module has no event linking, so they would stand there all year.
   - A Turtle gossip menu with the id and text of a 3.3.5 menu, whose unconditioned options are all in 3.3.5's menu (the innkeeper menu 342), uses 3.3.5's menu instead of a copy.
   - Flight paths: a Turtle path is kept only when its other end is ported or is the same 3.3.5 node (same id and position); Turtle node 93 (Ironforge Airfields) is a different node in 3.3.5.
   - `extra_quests` may be started or ended by an object on the zone's map (a tablet in a dungeon).
   - Items whose names start with `item_name_prefixes` ("Plans: ", "Design: ": Turtle-only recipes) are left out, except quest items (class 12) such as "Plans: Dark Iron Desecrator".
   - Manual scripts can touch 3.3.5 creatures with rollback: `S.stock_template(entry, col=value)` (old values restored), `S.mark_stock(entry)` (texts must use groups 100+; a stock AI other than SmartAI stops the build), `S.stock_quest_drops([items])` (Turtle's drops of those quest items on 3.3.5 creatures, as quest-only group-0 rows).
     - `zone_from_adt: true` decides which spawns belong to the zone from the area ids in Turtle's map chunks rather than Turtle's server maps, which disagree with its own terrain near moved borders.
     - Tiles that end up mostly 3.3.5 keep the 3.3.5 minimap image.
   - For a **new instance map**, see `047_stormwrought_ruins.json`: `map`, `map_dir`, `all_spawns`, `ship_wdt` and the `instance` block (Map / MapDifficulty / LoadingScreens rows, area triggers with new ids, entrance graveyard, `instance_template`, `dungeon_access_template`).
     - An **unused 3.3.5 map Turtle made a dungeon** (Stormwind Vault, map 35 StormwindPrison, WMO-only): `instance.existing_map: true` replaces 3.3.5's Map row (and reuses its MapDifficulty row) instead of adding one; the rollback's DELETE of the `map_dbc` row brings the stock row back. No `ship_wdt`, no tiles: the zone's `area_bits` still make its AreaTable row. A `loading_screen` 3.3.5 already ships (`LoadScreenDungeon.blp`) reuses its stock LoadingScreens row. `ship_assets: false` when nothing but the world-map art is Turtle's (the art comes with `world_map`).
   - Class trainers (`trainer_type` 0) teach 3.3.5's own list for their class (`creature_default_trainer` to the most used stock list); Turtle's class lists stop at the vanilla ranks. Profession and pet trainers keep the converted list.
   - `merge_region.take_new_wmos` (Thousand Needles): with `own: changed`, a chunk of the zone holding the origin of a building Turtle added (a WMO the 3.3.5 tile does not have there) is taken even if its ground did not change (huts on flat ground). `take_wmo_names` (list of WMO file names, lower case) takes such a chunk whatever its area: Windhorn Canyon's entrance cave `moocave.wmo` has its origin in a Dustwallow Marsh chunk. Check the cave-mouth holes (MCNK holes) are in the taken chunks.
   - Turtle reworks that cross a zone border (Thousand Needles' Shimmering Flats tip raised for northern Tanaris): leave that area out with `own_exclude_areas` rather than take half of it (a 72-yd step).
   - Staging the extract from the PC: a file more than 7 folders below `TWoW Data` cannot be staged; the extractor also writes those under `assets\_deep\` with `#` for each `\` (the build reads them there). Fetch the tiles first, build, then fetch what the build names as "referenced but not in the extract folder".
   - `scripted_taxi_paths` (Stormwind's Steelwing): a Turtle taxi path that only a gossip script starts. The build adds a start node of its own (no flight master and no path into it, so flight-master routes never use it; `at` puts it on the NPC: the core starts a scripted flight only within 10 yd of its start node) and the path to a node already ported (`to`, Turtle id). The manual script starts it with `A(52, [ctx['taxi_path'](turtle_path_id)], 'invoker')`.
   - Stock creatures' action lists (Swamp of Sorrows' Magtoor): 3.3.5 numbers its own lists entry×100+n as well; pick an id it does not use (`S.actionlist` stops the build on a 3.3.5 list id - the forward SQL would delete the stock list).
   - Gossip: an option whose Turtle condition is about a quest the zone leaves out is left out with its script (the core drops a condition on a missing quest and would show the option to everyone). Gossip scripts that complete an event quest (command 7) become SmartAI action 15. The build keeps only the repeatable bit of a quest's SpecialFlags: when the event that completes a no-objective quest is ported, set its "exploration or event" bit (2) in the manual script (`059_azshara.py`, "Learn Of My Past"), or the quest completes on accept.
   - Spawn height check: Turtle spawns far below the terrain may be inside a 3.3.5 cave WMO (the Swamp's Boulderclaw tunnelers, in the cave of 3.3.5's Nethergarde miners): compare with the WMO's MODF bounds, and with the 3.3.5 spawns already in that cave - a cave reached from the next zone usually belongs to that zone's rework.
   - Factions (*auto*, `FMAP` / `FTMAP` in build.py): Turtle's reputations whose id 3.3.5 gives to another faction get new ids (`faction_base`), reputations 3.3.5 knows only as plain factions keep their id and get a reputation index (`reputation_index_base`, below 128), and Turtle faction templates that would behave differently under their 3.3.5 id get new templates (`faction_template_base`). All go to the client patch and to `faction_dbc` / `factiontemplate_dbc`; quest rewards, kill reputation, item requirements and NPC templates use the new ids. Read `reports/common.json` "factions" after a build.
   - `merge_region.reshaped_take_areas` (Stonetalon): areas whose reshaped chunks are taken although their zone is in `reshaped_skip_zones` (the Veiled Sea Turtle raised into Stonetalon's new coast: skipped, it left a 500-yd underwater cliff). `match_stock_edges`: taken chunks at the rim of the region take the edge heights of the 3.3.5 tiles Turtle did not change (a 0.9-yd crack at the Barrens).
   - `merge_region.own_exclude_chunks` (Badlands, list of `"X_Y:chunk"`): single chunks of the zone left as 3.3.5 when taking them makes a step against a neighbour that cannot be taken (Badlands 36_43 chunk 197 next to Rugford's: a 43.8-yd step; taking the neighbour's area made it 101 yd).
   - `merge_region.exclude_chunks` (Eastern Plaguelands, list of `"X_Y:chunk"`): chunks never taken from Turtle, neither as the zone's own ground nor as reshaped ground next to it (`own_exclude_chunks` only removes them from the zone's own ground, so `reshaped: connected` takes them back). Used for a rim Turtle raised to meet a Turtle zone that is not ported (the Plaguewood's north rim under the Thalassian Highlands: 20-70 yd steps; left 3.3.5, the seams are 0.4 yd).
   - `merge_region.include_chunks` (Burning Steppes, list of `"X_Y:chunk"`): chunks always taken from Turtle as reshaped ground (they keep the area of the tile below). Used where an earlier zone already took a Turtle chunk and stitched its edge onto 3.3.5, and the new zone now takes the Turtle chunk next to it: without it the shared edge stays at the 3.3.5 height, a dip between two Turtle chunks (Badlands' four chunks on Azeroth_37_45 under Karfang Hold: 4.8 yd; re-taken, the largest step is 2.0 yd).
   - `merge_region.seam_report_yd` (default 5): seam steps above this are listed in the zone report with their world position. Set it lower (2) to find a remaining step.
   - `ship_wmos` (the Deadmines, list of WMO root paths): Turtle buildings shipped whole (root + all parts + their textures) although no shipped tile places them - a dungeon that is one building (a WMO-only map) Turtle extended. Compare the parts first: stage `Acore Data\vmaps\<name>.wmo.vmo` and match each Turtle part's group id (MOGP +56) and box with the vmo's groups (`GMOD`, then per group 24-byte box, flags, group id, VERT/TRIM/MBIH/LIQU chunks). The Deadmines: 3.3.5's 44 parts unchanged except two widened doorways + 5 new parts (the lab). Its mmaps are not rebuilt by install_server_data.py (no terrain tiles): run `server-data\rebuild_mmaps_map.bat` (default map 36) after it.
     The Wailing Caverns (088): 3.3.5's 23 parts contain every 3.3.5 collision vertex (except the openings) + 3 new parts (group ids 22027-22029); `rebuild_mmaps_wailing_caverns.bat` (map 43). A better test than boxes: every 3.3.5 vmo vertex (`VERT`, WMO-local = world (-x, -y) on a WMO-only map) should be among the Turtle part's `MOVT` vertices, and every 3.3.5 spawn should still be as close to Turtle's geometry as to 3.3.5's. Spawns in the new parts: Turtle spawns closer to the new parts' vertices than to any 3.3.5 vertex - their 3.3.5 templates go into `extra_spawns` / `extra_gameobject_spawns` (both take spawns of 3.3.5 templates), Turtle-only templates come with `all_spawns`.
   - `wmo_area_groups` (with `wmo_area_ids`): only these WMO group ids get WMOAreaTable rows (a 3.3.5 building's new rooms; 3.3.5 names its own rooms).
   - `extra_quests` also takes quests an object of the zone's map starts or ends (Westfall: the Abandoned Footlocker's 'The Old Church of Westfall' and the Guide to a Sailor's Stomach's 'Food for Sailing Thoughts?'); quests filed under the zone are only picked up when NPCs give and end them.
   - Server tiles: AzerothCore's `map_extractor` keeps liquid heights from the tile it extracted before, so adding tiles can change a few bytes at the end of an unrelated tile's liquid map (Azeroth 28_32 in the Eastern Plaguelands build). Such a tile is put back to the delivered copy before staging; its client ADT is unchanged.
   - Extractor (`TWoW Data\turtle_extract`): Turtle's patches hold a few empty files; `mpqread.py` reads them as empty and `turtle_extract.py` lists any file it cannot read as missing instead of stopping (the first Tirisfal run stopped there, before writing manifest.json).
   - Stock-spawn ground check on reworked zones lists many 3.3.5 spawns inside WMOs (Angor Fortress, Uldaman's entrance) whose terrain far above changed: check each against the MODF bounds of the WMOs on the tile before moving anything; only outdoor spawns need the height fix, and a spawn Turtle deleted (absent from Turtle's DB by guid) is removed with `S.stock_spawn_remove`.
   - Turtle's zeppelin masters stand by transport routes 3.3.5 does not have (Orgrimmar - Kargath): leave them out with the route.
   - A zone's `extra_spawns` / `extra_gameobject_spawns` belong to it: a later zone whose area holds them leaves them out (Feralas: Larodar Wildwhisper came with Gilneas, Fazgel Mechaflame and Lyvdia Dawnbird with Stranglethorn) - the report lists them under `spawned_elsewhere`.
   - Quest reward spells go through the same spell check as everything else (Turtle's 45519 Feral Spirit is 'zzOLD Defiance' in 3.3.5's server spell table): `quest_spell` notes.
   - A long ridge Turtle raised across the zone border (south of Chimaera Roost Vale) needs a deeper `connect_depth` (12) so it is taken whole; a partial take leaves 15-40 yd steps.
   - Quest mobs inside a 3.3.5 dungeon (Razorfen Kraul's Bramblehides) can be brought along as `extra_spawns` when the dungeon's layout is unchanged (check that 3.3.5 creatures stand nearby).
   - When a zone is ported whose NPC an earlier zone brought along (Felwood's Niremius Darkwind and Zafan, spawned by Hyjal), move the NPC to its home zone: drop it from the earlier zone's `extra_spawns`. A template whose SmartAI the later zone writes must belong to that zone's file - the earlier file's `DELETE FROM smart_scripts/creature_text` for its templates would wipe the rows whenever it is re-applied.
   - Two Turtle objects may share one loot id (Stonetalon's "Trash"): the build writes each loot id once (a duplicate key stopped the whole zone file at apply time - check `apply.sh` output for ERROR, not only check.py).
   - Turtle assets: the build reads its own copy of the extract folder. After an extract, a Turtle file the build names as "referenced but not in the extract folder" may only be missing from that copy (Davenburg's town hall and its textures, the Vault's world-map art were): bring it over from the PC before assuming the extract missed it.
   - Turtle gossip menus that replace a 3.3.5 NPC's menu (Ashenvale's "Words of Wisdom": Turtle gave the four hippogryph masters menus 59012-59015 = taxi option + a quest option): keep the 3.3.5 menu and add the quest option with `S.stock_gossip_option`. When two 3.3.5 NPCs share that menu (Teloren and Baritanas, menu 6944), add the option once; each NPC's own SmartAI "gossip select" row gives its credit, and `SMART_ACTION_SEND_GOSSIP_MENU` (98, menu + npc_text id) shows its own answer page. A stock NPC with no menu (Daelyshia) gets the shared one through `S.stock_template(gossip_menu_id=...)`.
   - qcheck's "item ... no source" can point at a Turtle object in a 3.3.5 dungeon (Ashenvale's Moonshrine Blooms in Blackfathom Deeps): add those spawns to `extra_gameobject_spawns` (any map).
   - Turtle's client-side tables are rebuilt from the user's current 3.3.5 client archives (`client335`). When the user's archive set changes (Ashenvale: patch-u disabled, patch-enUS-q/u gone), the build may ask for a table from another archive: fetch it from the extract, and tell the user to run CHECK_CLIENT.
   - **Max's rule for 3.3.5 zones Turtle changed (2026-10-09, Dustwallow):** where Turtle's version of a place would break or overlap 3.3.5 content, 3.3.5 stays and Turtle's part is left out; where nothing collides, both are kept. Check every Turtle camp/NPC against 3.3.5's spawns (Dustwallow: `dw/prox.py`, module creature spawns within 4 yd of a 3.3.5 one). A whole camp on the spot of a 3.3.5 camp (Deserter's Hideout on Direhorn Post, Blackhorn Village on the Grimtotem camp) goes out with its quests (`own_exclude_areas` keeps the ground and areas 3.3.5's); a single NPC Turtle put on the exact spot of a 3.3.5 NPC is moved beside it in the manual script.
   - `exclude_gameobject_boxes` [[x0, x1, y0, y1], ...]: Turtle objects inside a place 3.3.5 already has in its own form (Mudsprocket's 95 Turtle decorations). Turtle's copies of 3.3.5 NPCs are excluded by entry and their quests handed to the 3.3.5 NPC with `quest_npc_substitutions`; such quests are now picked up by the zone (the substitution counts as the giver/turn-in being present).
   - `extra_spawns` may list a Turtle spawn of a 3.3.5 template (Falgran Hastil): it is spawned as asked. When the 3.3.5 template's own SmartAI would misbehave on a permanent spawn (Falgran's walks away and despawns: 3.3.5 only summons him), give the spawn guid scripts in the manual (`S.row(-ctx['cguid'](tw_guid), ...)`): AzerothCore then runs those instead of the template's.
   - Long Turtle C++ dialogue scenes (`AddLambdaEventAtOffset` timelines): parse them into (ms, speaker, kind, value) lists (`dw/scenes.py`) and play them as one action list of the owner; the other speaker talks through `closest_creature` targets (talk with useTalkTarget 0 makes the target speak). One timed action list runs per creature at a time: put any start-up steps (unselectable, channel spell) into the same list.
   - Quest objectives on **objects** (negative `RequiredNpcOrGo`, Tanaris' Slickwick control panels) can't be credited by SmartAI: action 33 credits creatures only. Two options:
     - Make the object a goober (type 10) with the quest in `Data1`. This works when one quest uses it and needs nothing else (Stranglethorn's rum keg).
     - Otherwise, the manual script gives the quests credit creatures of the module's own (`creature_template` 9100001+, never spawned, with an invisible model row) and sets `ObjectiveText` to the object's name. Give each object its own gossip menu, so its option can check its own objective (condition 48, value 0 = not done yet).
   - `config.json` → `lock_substitutions`: a Turtle lock that needs a Turtle key item (Kwabit's Chest, lock 1654) has no 3.3.5 Lock.dbc equivalent, so the object would be left out. A plain 3.3.5 lock (43) keeps it, and the manual script makes the loot need the key (a condition on `gameobject_loot_template`, source type 4).
   - Turtle camps that Turtle itself later buried under new ground (Tanaris' Conquistadores beach camp, 2-9 yd under the raised Slickwick shore) are left out with `exclude_gameobject_boxes`. To find them, check every module spawn's z against the built `server-data/maps` (more than 1 yd under the ground), not only the 3.3.5 spawns.
   - **A 3.3.5 dungeon Turtle added to** (Zul'Farrak, `073_zulfarrak.json`): `map` and `map_dir` as for an instance, plus a `merge_region` over its tiles with `own: changed` and `reshaped: none`.
     - The 3.3.5 tiles come from `client335_extract.py` (add the map to `ALL_REGIONS`, and its WDT).
     - Turtle extracts some maps in lower case (`world\maps\tanarisinstance\`); `tw_asset_path` finds them.
     - A vanilla dungeon has no WorldMapArea row, so set `all_spawns`: every Turtle spawn of a non-3.3.5 template on the map is the zone's.
     - `merge_region.take_hole_changes`: a chunk where Turtle only cut terrain holes (a cave mouth into a new WMO) counts as changed.
     - The new WMOs' origin chunks are taken through `take_new_wmos`.
   - Spawns far under the ground are often inside a building, not buried (Dun Morogh: Ironforge's interior NPCs 200-340 yd under the mountain, the Reclamation Facility in tinkertown.wmo). Check them against the WMO placements (MODF extents) of the shipped tiles before leaving anything out (MWID/MWMO give the names, MODF the extents: world X = 17066.67 - extent z, world Y = 17066.67 - extent x).
   - `config.json` → `creature_id_takeover` {id: 3.3.5 name}: Turtle gave real creatures ids that 3.3.5 uses for test templates nothing spawns (Frostmane Hollow's 67, 82, 108 ...). The zone that spawns them writes Turtle's template over them; the build checks the 3.3.5 name and that nothing spawns or references them, and the zone's rollback puts the stock rows back. A Turtle id that a *used* 3.3.5 creature has (Turtle's Tamed Ice Claw Bear 33027 is Jessica Sellers in 3.3.5) can't be taken over: use a 3.3.5 stand-in in the manual script.
   - `spawn_boxes` [[x0, x1, y0, y1], ...]: spawns inside these boxes on the zone's map belong to the zone, whatever area their chunk carries (Dun Morogh's Reclamation mobs stand on chunks Turtle files under The Great Sea).
   - `spawn_boxes` may carry a z range as 5th and 6th values, and `exclude_boxes` [[x0, x1, y0, y1, z0, z1], ...] leaves spawns inside out (creatures and objects). Used for a capital under another zone's ground: Undercity's spawns stand on Tirisfal's chunks (Ruins of Lordaeron), so 081_tirisfal_glades leaves the city's box (z below 10) out and 082_undercity takes it with `spawn_boxes`.
   - `faction_keep_335` (config.json, list of Turtle faction ids): 3.3.5's Faction row stays as it is even where Turtle gave that faction a reputation (Battleground Neutral 709 for Tirisfal's Scarlet camp; without it the build adds a hidden reputation and changes Faction.dbc).
   - EventAI talk lines with negative ids come from Turtle's `script_texts` (their `type` decides say / yell); the build reads them there when `broadcast_text` has no row.
   - `dungeon_access_template.id` is a TINYINT: the module used 250-255 for its first six dungeons, then counts down from 249 (asserted free).
   - Turtle often *replaces* a 3.3.5 NPC on the spot (Ironforge: Gelwin Brasspipe on Mekkatorque's spot, the Airfield Engineers on the Gnome Engineers'), because Turtle moved the 3.3.5 NPC elsewhere. 3.3.5 keeps its NPC there, so the Turtle one goes when it only stands in (no quests), and moves 2-3 yd aside when it has quests (Masey Wirefuse beside Klockmort Spannerspan).
   - A capital that is its own 3.3.5 zone (Thunder Bluff, 1638) gets its own small zone file with `terrain: stock` and `zone_from_335_tiles`, next to the zone around it (Mulgore). Ironforge is different: its ground is Dun Morogh's, so its NPCs come with Dun Morogh.
   - Turtle mounts all use one Turtle-only spell (46499), so a Turtle mount item would have no use. `config.json` → `mount_spell_by_item` {item: 3.3.5 mount spell} makes the item teach the closest 3.3.5 mount (Learning 55884 + the mount spell, trigger 6, riding 150 for epic mounts), like the stock mount items.
   - Class quests for race/class pairs 3.3.5 does not have (Turtle's tauren priests) and chains whose reward is a new Turtle spell (The Way of Spiritwalking -> Spiritwalking 47262) are left out (`exclude_quests`).
   - Staging new Turtle tiles inside an earlier zone's `merge_region` changes that zone's object unique ids (the allocator sees the new tiles), even when it takes no new chunk: its shipped tiles differ in MDDF/MODF ids only. List them as changed.
2. **Add the zone** to `zones` in `config.json`. Order matters: when two zones share an NPC or quest, the first zone listed owns it.
3. **Make the map tiles available.**
   - The build reports any missing `.map` tiles, from both the TWoW and the AzerothCore data folders.
   - For `terrain: turtle` it also needs:
     - Turtle's `.adt` files, from `turtle_extract.py`
     - a Linux build of AzerothCore's `map_extractor` (`config.json` → `map_extractor`)
4. **Run** `python3 build.py`.
5. **Test** by applying everything in `data/sql/db-world/` to a copy of the world DB (twice, strict SQL mode), then running `python3 check.py <copy>`. It must say `all references resolve`. Then run every `sql_rollback/` file on the copy and compare all table checksums with the pristine DB: nothing may differ.
6. **Read** `docs/zones/<slug>.md`, which lists:
   - NPCs on stand-in appearances
   - spawns moved to stock ground
   - held-back content
   - EventAI and C++ scripts that still need converting
7. **Hand-written scripts** go in `tools/turtle2ac/manual/<slug>.py` (SmartAI written as Python with `lib/smartgen.py`; see `047_stormwrought_ruins.py`, which ports the 12 Stormwrought bosses and the secret door) or `tools/turtle2ac/manual/<slug>.sql`. In both, Turtle spawn GUIDs are translated: `ctx['cguid'](tw_guid)` / `ctx['gguid'](tw_guid)` in Python, `{cguid:N}` / `{gguid:N}` in SQL. For SQL:
   - Put each one in a `-- @block requires=<creature ids>` … `-- @end` block, so it's only included when those NPCs are part of the build.
   - Use `smart_scripts` ids from 100 up.
   - Number timed action lists as creature entry × 100 + n.

## What is converted automatically

- **Terrain (`terrain: turtle`):**
  - Turtle's tiles are cleaned for 3.3.5 and packed into `client/patch-y.mpq`.
  - The tiles are converted to server `.map` files in `server-data/maps/`.
  - New subzones get `AreaTable` rows, both in the client patch and in `areatable_dbc`.
- **Object models:** objects whose model has no 3.3.5 display row get one, in the client patch and in `gameobjectdisplayinfo_dbc`.
  - Models that only exist in Turtle's client need a stand-in in `config.json` → `go_model_substitutions`.
  - Objects with Turtle-only locks, such as Survival gathering nodes, are left out.

- **Creatures:** stats become AzerothCore modifiers.
- **Display IDs:** displays are checked against your server DBCs. Custom humanoid looks get the closest same race/sex stand-in.
- **Placement:** equipment, spawns, waypoints, `creature_addon`.
- **NPC services:**
  - Gossip menus, `npc_text` and options, on NPCs and on quest-giver objects. Turtle conditions on texts and options (quest taken / rewarded / not taken, and AND/OR of those) become `conditions` rows.
  - Gossip scripts: quest credit (command 8), summon at a position (10, with Turtle's one-at-a-time limit as a condition) and give item (17) become SmartAI "gossip select" rows, also on sub-menus (they run on the NPC/object that owns the first menu). Text lines in those scripts are dropped and delays ignored (both reported).
  - Vendors, including Turtle vendor templates.
  - Trainers. Turtle's "teach" spells are converted to the learned spells.
- **Loot:**
  - Creature, gameobject and reference loot. Turtle-only items are dropped: Jewelcrafting, gems, companions. An item a ported quest gives or asks for is always kept.
  - On-kill reputation.
- **Quests:**
  - Quests with their texts, rewards and reputation.
  - XP mapped to the equivalent 3.3.5 tier.
  - Race masks get Blood Elf / Draenei added.
  - Starter and ender relations.
- **Combat spells:** creature spell lists become SmartAI.
- **Items:**
  - Everything referenced above becomes an `item_template` row, plus the matching `item_dbc` rows and client `Item.dbc` rows.
  - Item spells that don't exist in 3.3.5 are replaced (`config.json` → `item_spell_replacements`).

- **Items:** a Turtle item id only counts as the 3.3.5 item when the names are close (much closer when the item class differs). If a 3.3.5 item has Turtle's exact name under another id, that item is used. Otherwise the item is ported as `item_remap_base` + Turtle id (see the README).
- **Quests filed under the zone** (quest log category) whose giver and turn-in both live elsewhere are added when those NPCs exist in 3.3.5 (same name) or in the build; `extra_spawns` adds Turtle NPCs outside the zone (e.g. in Ironforge) that quests need.
- **Quest chains:** prerequisite / next-quest links to quests that aren't in the build are removed (printed by the build and listed under `quest_chain` in the zone report). Quests started by an item that drops in the zone are added when their turn-in NPC exists.
- **Spells:** a Turtle spell id only counts as present in 3.3.5 when the 3.3.5 spell has the same name (Turtle reused many ids that are other spells in 3.3.5). Others use `config.json` → `spell_substitutions` or are dropped; every case is in the zone report.
- **EventAI:** `creature_ai_events` become SmartAI: casts, talk (Turtle broadcast texts become `creature_text` groups 50 and up) and flee; other script commands are reported.
- **Text:** Turtle database text that was double-encoded on its way into MySQL (`â€”` for `—`) is repaired when it's read.
- **Creatures whose Turtle id 3.3.5 uses for another creature** (Elder Moonhoof 29479 = Shoveltusk Forager): with
  `spawn_existing_templates` the 3.3.5 creature would stand in Turtle's spot. Find them by comparing the names of the
  zone's spawns with 3.3.5's (the zone SQL comment holds Turtle's name). An unused 3.3.5 test template can be taken over
  (`config.json` → `creature_id_takeover`); a spawned one goes into `creature_id_remap` (id → the 3.3.5 name, checked):
  the build treats the Turtle creature as new and writes it as `creature_remap_base` (5,000,000) + its Turtle id in the
  template, spawns, quest relations, SmartAI, texts and conditions. Zone settings and reports keep the Turtle id;
  manual scripts use the new id.
- **Objects that 3.3.5 already has under the same id** (even when renamed, e.g. "Alliance Mailbox" / "Mailbox") use the 3.3.5 template; an id 3.3.5 uses for a different object is never overwritten (listed as `object_id_taken`).
- **Terrain passes over every shipped tile** (after all zones; Max's fixes of 2026-10-09, `config.json` → `tile_fixes`, `ground_effects`):
  - `remove_placements` drops a doodad/WMO by uniqueId (the Stormwind harbor hangar 2544788 on Azeroth_29_47 / 30_47),
    `texture_substitutions` swaps terrain textures (Gilneas' neon-green duskwood grass), `never_ship` keeps files with stock names out of the patch.
    `never_ship` also takes WMO roots (their groups go with them): buildings Turtle copied from TBC/Wrath that the 3.3.5 client
    has at the same path (the guard towers, Zul'Aman troll huts, Dragonblight barracks, the Shadowmoon slag pit). Turtle's
    manifest only says "not in vanilla"; to check a building, stage `Acore Data\vmaps\<name>.wmo.vmo` (stock vmaps): if it
    exists with the same group count (`GMOD` + 4), the 3.3.5 client has it.
  - Sea floor: a sea chunk more than 30 yd below Turtle's own server height (TWoW Data `maps`, where Turtle has water
    over it) takes Turtle's server heights: no stock −516 pits next to the islands. Its edges meet the unchanged chunks;
    the MH2O depth is 1.72 per yard of water, "deep" only below −60.
  - Dark water: the "deep" mark (AzerothCore's extractor turns it into dark water = Fatigue) stays only on cells whose ground
    is below −60. The server flag is per chunk, so a chunk is dark when any of its cells is.
  - Grass: Turtle's ground-effect rows (30000+) are filled in the client's own `GroundEffectTexture.dbc` (written in the
    client's row order); untagged dirt layers in Gilneas and Balor get rows 30029/30031/30032; cells under water or whose
    most visible texture is a road or sand get the no-clutter bit (new-zone chunks only).
  - Minimap: every tile with new-zone ground gets `Textures\Minimap\<Dir>\mapX_Y.blp` and a trs line naming it after
    itself, in its directory's block (a `dir: Giln` block is added). Mixed tiles are composed per chunk (new-zone and water
    chunks from Turtle, stock dry land from the stock image) and written as BLP2 DXT1 with mipmaps.
  - World-map continent art and `.zmp` hover areas are not built: Max keeps them in his patch-z.
- **Client tables** are always built from the copy your client actually loads (`config.json` → `client_dbc`, extracted by `client335_extract.py`), so other patches in your client aren't undone.

## Not automatic yet (reported per zone)

- Turtle C++ scripts (rewrite as SmartAI in `manual/`, or C++ in `src/zones/`)
- Turtle gossip scripts other than quest credit, summon and give-item (those three are converted to SmartAI), quest start/complete scripts, and EventAI script commands other than casts
- Creature models that only exist in Turtle's client (they get the closest 3.3.5 look)
- Turtle-only locks (e.g. keys for Turtle doors): those objects are left out
- After building a `turtle` zone, players need the new `client/patch-y.mpq`, and the server needs `server-data/install_server_data.bat` run once.

## Pre-ship checklist

Everything here broke the live server or client once (see the history at the end). The items marked *auto* stop
the build or fail `check.py`; the rest are checked by hand before delivering.

**SQL**
- *auto* Every INSERT's columns exist in the target world DB (`lib/sqlw.py`: `creature.id1` is written as `id` on
  the Grimfeather core). A missing column makes the DB updater abort and the worldserver not start.
- *auto* Server `*_dbc` ids and client-table ids come from reserved bases in `config.json` → `ids`
  (`map_difficulty_base`, `loading_screen_base`, `light_base` …), never "stock max + 1": other modules and HD
  patches add their rows right after the stock ids.
- *auto* (`check.py`, compared with the pristine DB so only new problems show) what the worldserver logs at startup:
  quest givers/enders without the quest-giver flag, missing creature/skinning/pickpocket loot tables, missing book
  pages (items, text objects, goobers, next pages), trainer spells that are talents, fishing holes with
  min opens > max opens (a worldserver **assert** - it shuts down), spawn masks for difficulties the map lacks.
- Reused 3.3.5 templates (`spawn_existing_templates`) that 3.3.5 itself never spawns can hold junk; the build
  fixes fishing-hole ranges automatically, other types need a look if the core uses them in a random range.
- Instance blocks: `graveyard` is `{map, x, y, z, o}` (a list once had the orientation read as z: graveyard 130 yd
  underground), the loading-screen BLP is shipped (*auto*), `min_level` is what the server owner wants.

**Client patch** (*auto*, before `patch-y.mpq` is written)
- Every ADT passes the client's own MCNK walk: sub-chunks in order from +128, an MCLQ only where the header points.
  A leftover MCLQ block crashed the client (#132 at 0x007C3A42) on entering Stormwind.
- WMO groups: Turtle roots set MOHD flag 0x4, with `groupLiquid = 15` in every group, which 3.3.5 reads as WMO
  Magma filling the whole group: lava inside every Turtle building, on the client and (vmaps) on the server.
  Groups without MLIQ get 0, groups with MLIQ the matching WMO water/ocean/magma/slime type. After a WMO change the
  server data must be reinstalled (`install_server_data.bat`) so the vmaps lose the lava too.
- Flight master node ids must stay below 448 (the 3.3.5 client's known-nodes mask): 441-447 are used, the build then
  takes 437 down to 406 (free in both the client and server TaxiNodes).
- DBC row order: AreaTrigger (by map, then id), MapDifficulty (map, difficulty), TaxiPathNode (path, index) and
  WMOAreaTable (WMO, name set, group) keep the stock order (`lib/dbcw.py` ORDER). AreaTrigger sorted by id made the
  client ignore **every** area trigger: no instance portal worked anywhere. A table whose stock rows are in some other
  order stops the build.
- Client load order: `Data\patch-<x>` beats `Data\enUS\patch-enUS-<x>` (tested); `patch-z` beats `patch-y`.
  The build takes each table from the winning archive of the client335 extract (`archive_rank`) and writes
  `client/client_tables.json`; `client/CHECK_CLIENT.bat` compares a player's client with it and reports an archive
  that overrides the patch or a table copy the build did not see.

**Server collision and pathing** (`server-data/install_server_data.py`)
- vmap4_extractor ranks the enUS locale patches above `Data\patch-*`. The extraction client therefore gets patch-y
  twice, as `patch-99.MPQ` and `enUS\patch-enUS-99.MPQ`; with the first alone the stock Map.dbc hid map 818 and it
  got no vmaps (bosses fell through the floor, could not chase, vanished on evade). Check with `.gps`: `VMap: 1`.

**World map** (made by hand on the server PC in `patch-z.mpq`; not yet produced by the converter)
- A new zone in WorldMapArea.dbc shows in the zone list, but the continent hover/click comes from
  `Interface\WorldMap\Azeroth.zmp` (128x128 AreaTable ids): the zone must be painted there too.
- New land drawn on the continent (Balor) means editing `Interface\WorldMap\Azeroth\Azeroth<n>.blp` tiles. Keep the
  stock BLP format (DXT1, same header); rewrite only the changed blocks (tile 10 has a 1-bit see-through strip).
- A zone Turtle redrew (Arathi) needs Turtle's zone art and its WorldMapOverlay rows (moved and new overlays).
- While patch-z ships its own WorldMapOverlay.dbc it overrides patch-y's: overlays added by a new build stay hidden
  until patch-z is rebuilt or folded into the converter.

**In game, after installing**
- Walk into a new dungeon portal and a stock one (the Stockade) with `.debug areatriggers` on.
- Zone into each new area; enter Stormwind/the city next to the change (merged tiles); `.gps` must show `VMap: 1  MMap: 1`.
- Pull each boss (`.cheat god on`): it must chase and walk home without falling.
- Hover and click each new zone on the continent map.
- Read `Server\Errors.log` for: spawn mask, first page, loot "does not exist", quest flag, "is a talent".

**Extract (cloud side)**
- Files nested more than 7 folders below a connected folder cannot be fetched; `turtle_extract.py` also writes them flattened to `assets\_deep\` (`\` -> `#`), and `lib/assets.py` reads those copies.
- Quest givers or enders outside the zone (other cities): add their Turtle spawn GUIDs to `extra_spawns`, then exclude the quests they bring along that belong to their own zone (`exclude_quests`).

**Debugging that worked**
- Worldserver crash: `Server\Crashes\*.txt` has the call stack and locals (grid x/y, rotation) -> find the spawn.
- Client crash: the client's `Errors\*.txt`; the code bytes at EIP name the parser (`cmp eax,'MCNR'` = MCNK walk).
- Portals: `.debug areatriggers` prints only after the server's radius check. To see whether the client sends
  anything, set `Logger.network=5,Server` and grep `CMSG_AREATRIGGER`; `.go trigger <id>` tests the server side.
- Patch conflicts: list each letter MPQ's `DBFilesClient\*` and intersect with patch-y's (`CHECK_CLIENT.bat`).
