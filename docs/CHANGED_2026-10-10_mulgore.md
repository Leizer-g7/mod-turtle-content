# Changed in the Mulgore + Thunder Bluff build (2026-10-10, fourth delivery of the day)

Compared with the Dun Morogh + Frostmane Hollow delivery made earlier the same day (patch md5 9aa2c14dde50fe4d56ba72760dc6610e). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `Textures\Minimap\md5translate.trs`: changed. It has 3 new lines (Kalimdor 31_36, 31_37, 32_37) and 2 changed ones (Kalimdor 33_32, 34_32). If patch-z ships its own trs, merge these lines into it.
- `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`: changed (the new subzones Red Cloud Roost and Suntail Pass, object models, items). patch-z did not ship these tables as of the last handoff.
- ADT tiles: Kalimdor 30_36, 31_35, 31_36, 31_37, 32_37, 33_33, 34_33, 34_34 (new), 33_32, 34_32 (changed), and 32_30, 32_31, 33_30, 33_31, 34_31 (object ids only, see below). If patch-z has its own copy of any of them, that copy hides this one.

## Client patch (patch-y.mpq)

278,678,105 bytes (was 272,256,329).

- Added ADT tiles (8): `World\Maps\Kalimdor\Kalimdor_30_36.adt`, `Kalimdor_31_35.adt`, `Kalimdor_31_36.adt`, `Kalimdor_31_37.adt`, `Kalimdor_32_37.adt`, `Kalimdor_33_33.adt`, `Kalimdor_34_33.adt`, `Kalimdor_34_34.adt`.
- Changed ADT tiles (7):
  - `World\Maps\Kalimdor\Kalimdor_33_32.adt`, `Kalimdor_34_32.adt`: Stonetalon's tiles, now also with Suntail Pass and the reshaped Barrens slopes next to it.
  - `Kalimdor_32_30.adt`, `Kalimdor_32_31.adt`, `Kalimdor_33_30.adt`, `Kalimdor_33_31.adt`, `Kalimdor_34_31.adt`: Stonetalon's tiles with their object unique ids renumbered (the new Turtle tiles staged for Mulgore lie in Stonetalon's region too); ground, textures and objects are unchanged.
- Added minimap images (3): `Textures\Minimap\Kalimdor\map31_36.blp`, `map31_37.blp`, `map32_37.blp`. Changed (2): `map33_32.blp`, `map34_32.blp`.
- Changed tables (3): `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, and `Textures\Minimap\md5translate.trs`.
- No new buildings or textures: Turtle's huts at Red Cloud Roost and Suntail Pass are 3.3.5 models.
- Removed: none.

## Server map tiles (server-data/maps)

- Added (8), Kalimdor: `0013333.map`, `0013334.map`, `0013434.map`, `0013531.map`, `0013630.map`, `0013631.map`, `0013731.map`, `0013732.map`.
- Changed (2): `0013233.map`, `0013234.map`.
- `install_server_data.bat` rebuilds vmaps and mmaps for Kalimdor.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_032_mulgore.sql`, `mod_turtle_033_thunder_bluff.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zones' items, and the Turtle mount items now teach a 3.3.5 mount (they had no use before; see Converter).
- 3.3.5 rows the new files change, all restored by their undo files:
  - Four 3.3.5 creatures (Windfury harpies at Suntail Pass, an Ornery Plainstrider) and three Copper Veins raised onto the new ground.
  - Turtle's quest drops added to Prairie Stalkers, Windfury Harpies / Wind Witches and Razormane Scouts.

## Converter

- `build.py`: `mount_spell_by_item` (Turtle mount items teach a 3.3.5 mount).
- `config.json`: the zones 076 and 077; `mount_spell_by_item` for the 12 Turtle mount items in the build.
- New `zones/076_mulgore.json`, `zones/077_thunder_bluff.json`, `manual/076_mulgore.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, `zones/065_stonetalon_mountains.md`, new `zones/076_mulgore.md` and `zones/077_thunder_bluff.md`, and this file.
- Reports: `065_stonetalon_mountains.json`, `common.json`, new `076_mulgore.json` and `077_thunder_bluff.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
