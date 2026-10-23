# Changed in the Burning Steppes + Hateforge Quarry build (2026-10-11, fourth delivery of the day)

Compared with the Tirisfal Glades + Undercity delivery made earlier the same day (patch md5 97c1445dc15edce59ed91786d6b9d94e). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `World\Maps\Azeroth\Azeroth_37_45.adt` and `Textures\Minimap\Azeroth\map37_45.blp`: changed (Karfang Hold's north edge). If patch-z has its own copy of either, that copy hides this one.
- New ADT tiles: Azeroth 36_47, 37_46, 37_47, 38_46, 38_47, and the nine Hateforge tiles. If patch-z has its own copy of any Azeroth one, that copy hides this one.
- `DBFilesClient\WorldMapArea.dbc` (Hateforge Quarry's dungeon map), `AreaTable.dbc`, `AreaTrigger.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, `LoadingScreens.dbc`, `Map.dbc`, `MapDifficulty.dbc`: changed. patch-z did not ship these tables as of the last handoff (it ships WorldMapOverlay.dbc, which is not changed here).
- `Textures\Minimap\md5translate.trs`: not changed.

## Client patch (patch-y.mpq)

296,319,541 bytes (was 290,939,550), md5 683a404750d9dece015ad623c6665772, 12 parts.

- Added ADT tiles (5): `World\Maps\Azeroth\Azeroth_36_47.adt`, `Azeroth_37_46.adt`, `Azeroth_37_47.adt`, `Azeroth_38_46.adt`, `Azeroth_38_47.adt`.
- Added dungeon map (10): `World\Maps\Hateforge\Hateforge.wdt` and `Hateforge_37_46.adt`, `37_47`, `37_48`, `38_46`, `38_47`, `38_48`, `39_46`, `39_47`, `39_48`.
- Added art (13): `Interface\GLUES\LoadingScreens\LoadScreenHateforge.blp`, `Interface\WorldMap\HateforgeQuarry\HateforgeQuarry1.blp` to `HateforgeQuarry12.blp`.
- Changed tile: `World\Maps\Azeroth\Azeroth_37_45.adt`; changed minimap image: `Textures\Minimap\Azeroth\map37_45.blp`.
- Changed tables (8): `DBFilesClient\AreaTable.dbc`, `AreaTrigger.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, `LoadingScreens.dbc`, `Map.dbc`, `MapDifficulty.dbc`, `WorldMapArea.dbc`.
- Removed (29): Turtle's copies of buildings the 3.3.5 client already has at the same path, and the textures only they used. The client now uses its own files (same buildings; found in AzerothCore's stock vmaps with the same number of parts):
  - `WORLD\WMO\AZEROTH\BUILDINGS\GUARDTOWER\GUARDTOWER_DESTROYED.WMO` + `_000.wmo` (Tirisfal, Gilneas, Gilneas City).
  - `WORLD\WMO\LORDERON\BUILDINGS\ZULAMAN\FTROLL_HUTS\FORREST_TROLL_HUT2STORY.WMO` + `_000`, `_001`, `FORREST_TROLL_HUTSMALL01.WMO` + `_000` (Stonetalon), and 7 `DUNGEONS\TEXTURES\ZULAMAN\*` textures.
  - `WORLD\WMO\NORTHREND\BUILDINGS\HUMAN\DB_BARRACKS.WMO` + `_000` to `_012` (Gilneas) and `DUNGEONS\TEXTURES\ROOF\BM_KZN_SHINGLES01.BLP`.
  - Not added for the same reason: `GUARDTOWER_DAMAGED.WMO` (Eastern Plaguelands' Forlorn Summit; it was referenced but never shipped), `OL_DWARVEN_WATCHTOWER.WMO` and the Hateforge slag pit `SHADOWMOON_SLAGPIT01.WMO` (Burning Steppes / Hateforge Quarry).

## Server map tiles (server-data/maps)

- Added (5), Azeroth: `0004637.map`, `0004638.map`, `0004736.map`, `0004737.map`, `0004738.map`.
- Added (9), Hateforge Quarry (map 808): `8084637.map`, `8084638.map`, `8084639.map`, `8084737.map`, `8084738.map`, `8084739.map`, `8084837.map`, `8084838.map`, `8084839.map`.
- Changed (1): `0004537.map` (Azeroth_37_45). (`0002736.map`, an Eastern Plaguelands tile, came out with a few different liquid bytes again - the map_extractor leftover - and the delivered copy was kept.)
- `install_server_data.bat` rebuilds vmaps and mmaps for Eastern Kingdoms (map 0) and Hateforge Quarry (map 808).

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_039_burning_steppes.sql`, `mod_turtle_040_hateforge_quarry.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zones' items. `mod_turtle_027_dustwallow_marsh.sql`: Jabbey's (Gadgetzan) Turtle menu gets a third option for the Burning Steppes quest "To Purchase Secret Information" (40466); his undo file is not changed (it already removes his whole menu and texts).
- 3.3.5 rows the new files change, all restored by their undo files:
  - Turtle's quest drops on 3.3.5 creatures (10 items): Blackrock orcs, War Reavers, Thaurissan agents, Flamekin, Felguard Sentries, Deathlash / Venomtip Scorpids, War Master Voone, Golem Lord Argelmach.
  - Four 3.3.5 objects on Turtle's new ground: an ore pool point near Karfang Hold (3 rows) lifted 1.9 yd, a Mountain Silversage point lowered 3 yd.
  - Turtle quests started or ended by 3.3.5 NPCs (quest-relation rows only).

## Converter

- `build.py`: `merge_region.include_chunks`, `merge_region.seam_report_yd`.
- `lib/assets.py`: `never_ship` also covers buildings (WMO root and its parts).
- `config.json`: the zones 083 and 084; `spell_substitutions` 56519 -> 17228 (Shadow Bolt Volley), 56520 -> 41106 (Battle Aura), 56523 -> 12749 (Mithril Mechanical Dragonling); 7 buildings in `never_ship`.
- New `zones/083_burning_steppes.json`, `zones/084_hateforge_quarry.json`, `manual/083_burning_steppes.py`. Changed `manual/071_dustwallow_marsh.py` (Jabbey).
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/083_burning_steppes.md` and `zones/084_hateforge_quarry.md`; `zones/050_gilneas.md`, `051_gilneas_city.md`, `065_stonetalon_mountains.md`, `081_tirisfal_glades.md` (their count of shipped Turtle files); and this file.
- Reports: `common.json`, new `083_burning_steppes.json` and `084_hateforge_quarry.json`; `050_gilneas.json`, `051_gilneas_city.json`, `065_stonetalon_mountains.json`, `081_tirisfal_glades.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
