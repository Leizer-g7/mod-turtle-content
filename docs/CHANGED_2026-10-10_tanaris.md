# Changed in the Tanaris + Zul'Farrak build (2026-10-10, second delivery of the day)

Compared with the delivery made earlier the same day (Max's converter fixes). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `Textures\Minimap\md5translate.trs`: changed. It has 12 new lines: 9 Kalimdor tiles and 3 TanarisInstance tiles. If patch-z ships its own trs, merge these lines into it.
- `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`: changed. They gain the new subzones (Sandmoon Village, Slickwick Oil Rig), object models and items. patch-z did not ship these tables as of the last handoff.
- ADT tiles: Kalimdor 35_49, 35_50, 36_49, 36_50, 39_44, 40_43, 40_44, 40_45 and 41_45, and the four TanarisInstance tiles. If patch-z has its own copy of any of them, that copy hides this one.

## Client patch (patch-y.mpq)

- Added ADT tiles (13): `World\Maps\Kalimdor\Kalimdor_35_49.adt`, `World\Maps\Kalimdor\Kalimdor_35_50.adt`, `World\Maps\Kalimdor\Kalimdor_36_49.adt`, `World\Maps\Kalimdor\Kalimdor_36_50.adt`, `World\Maps\Kalimdor\Kalimdor_39_44.adt`, `World\Maps\Kalimdor\Kalimdor_40_43.adt`, `World\Maps\Kalimdor\Kalimdor_40_44.adt`, `World\Maps\Kalimdor\Kalimdor_40_45.adt`, `World\Maps\Kalimdor\Kalimdor_41_45.adt`, `World\Maps\TanarisInstance\TanarisInstance_29_28.adt`, `World\Maps\TanarisInstance\TanarisInstance_29_29.adt`, `World\Maps\TanarisInstance\TanarisInstance_30_28.adt`, `World\Maps\TanarisInstance\TanarisInstance_30_29.adt`
- Added minimap images (12): `Textures\Minimap\Kalimdor\map35_49.blp`, `Textures\Minimap\Kalimdor\map35_50.blp`, `Textures\Minimap\Kalimdor\map36_49.blp`, `Textures\Minimap\Kalimdor\map36_50.blp`, `Textures\Minimap\Kalimdor\map39_44.blp`, `Textures\Minimap\Kalimdor\map40_43.blp`, `Textures\Minimap\Kalimdor\map40_44.blp`, `Textures\Minimap\Kalimdor\map40_45.blp`, `Textures\Minimap\Kalimdor\map41_45.blp`, `Textures\Minimap\TanarisInstance\map29_28.blp`, `Textures\Minimap\TanarisInstance\map29_29.blp`, `Textures\Minimap\TanarisInstance\map30_29.blp`
- Added buildings (WMO root + group files, 20): `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTB\GOBLINHUTVARIANTB.WMO`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTB\GOBLINHUTVARIANTB_000.wmo`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTB\GOBLINHUTVARIANTB_001.wmo`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTG\GOBLINHUTVARIANTG.WMO`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTG\GOBLINHUTVARIANTG_000.wmo`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTG\GOBLINHUTVARIANTG_001.wmo`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTH\GOBLINHUTVARIANTH.WMO`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTH\GOBLINHUTVARIANTH_000.wmo`, `WORLD\WMO\KALIMDOR\GOBLINHOUSES\GOBLINHOUSEVARIANTH\GOBLINHUTVARIANTH_001.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins16.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins16_000.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_000.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_001.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_002.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_003.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_004.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_005.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_006.wmo`, `world\kalimdor\buildings\tanarisruins\tanarisruins17_007.wmo`
- Changed (4): `DBFilesClient\AreaTable.dbc`, `DBFilesClient\GameObjectDisplayInfo.dbc`, `DBFilesClient\Item.dbc`, `Textures\Minimap\md5translate.trs`
- Removed: none.

## Server map tiles (server-data/maps)

- Added (13): `0014340.map`, `0014439.map`, `0014440.map`, `0014540.map`, `0014541.map`, `0014935.map`, `0014936.map`, `0015035.map`, `0015036.map`, `2092829.map`, `2092830.map`, `2092929.map`, `2092930.map`.
  - The `001...` files are Kalimdor (Tanaris).
  - The `209...` files are Zul'Farrak (TanarisInstance 29_28, 30_28, 29_29, 30_29).
  - `install_server_data.bat` rebuilds vmaps for both maps, plus mmaps for Kalimdor and map 209.
- Changed or removed: none.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_028_tanaris.sql`, `mod_turtle_029_zulfarrak.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo; items and reference loot of the two zones).
- Changed: `mod_turtle_010_tel_abim.sql`. Gelwig Darkbrow keeps Turtle's height, now that Tanaris ships Turtle's lower ground at Steamwheedle Port.
- Changed: `mod_turtle_014_stranglethorn_vale.sql` (+ undo). Baron Revilgaz gets the 'VIP Invites' beach-party option.
- 3.3.5 rows the new files change, all restored by their undo files:
  - Vol'jin, Gazlowe and Baron Revilgaz gossip.
  - One Rabid Blisterpaw at Land's End raised onto the new ground.
  - In Zul'Farrak: 7 Sandfury trolls removed from the arena floor; Sandarr Dunereaver moved to Turtle's spot; 4 creatures raised onto the new ground.
  - Turtle's quest drops added to 3.3.5 Tanaris creatures.

## Converter

- `build.py`:
  - `lock_substitutions`.
  - `tw_asset_path`: finds Turtle files extracted in lower case.
  - Zones without a world-map rectangle (`all_spawns`).
  - `merge_region.take_hole_changes` and `ship_replaced_wmo_tiles`.
- `config.json`:
  - The zones 072 and 073.
  - `lock_substitutions` (1654 -> 43).
  - Spell stand-ins 57097 -> 15618 and 52695 -> 18267.
- `lib/smartgen.py`: `stock_spawn_remove` also takes a plain addon row.
- New `zones/072_tanaris.json`, `zones/073_zulfarrak.json`, `manual/072_tanaris.py`, `manual/073_zulfarrak.py`.
- Changed: `manual/054_tel_abim.py`, `manual/058_stranglethorn_vale.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, `zones/054_tel_abim.md`, new `zones/072_tanaris.md` and `zones/073_zulfarrak.md`.
- Reports: `054_tel_abim.json`, `common.json`, new `072_tanaris.json` and `073_zulfarrak.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
