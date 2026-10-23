# Changed in the Teldrassil + Darnassus build (2026-10-11)

Compared with the Mulgore + Thunder Bluff delivery (2026-10-10, patch md5 9f9e02169d118c4fe375ee96a1fa07a1). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`: changed (the new subzone Ursan Heights, object models, items). patch-z did not ship these tables as of the last handoff.
- ADT tiles: Kalimdor 27_14, 28_14 (new). If patch-z has its own copy of either, that copy hides this one.
- `Textures\Minimap\md5translate.trs`: not changed (Turtle changed fewer than 128 chunks per tile, so the 3.3.5 minimap images are kept).

## Client patch (patch-y.mpq)

280,643,378 bytes (was 278,678,105).

- Added ADT tiles (2): `World\Maps\Kalimdor\Kalimdor_27_14.adt`, `World\Maps\Kalimdor\Kalimdor_28_14.adt`.
- Changed tables (3): `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`.
- No new buildings, textures or minimap images. Removed: none.

## Server map tiles (server-data/maps)

- Added (2), Kalimdor: `0011427.map`, `0011428.map`.
- Changed: none.
- `install_server_data.bat` rebuilds vmaps and mmaps for Kalimdor.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_034_teldrassil.sql`, `mod_turtle_035_darnassus.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zones' items.
- 3.3.5 rows the new files change, all restored by their undo files:
  - Turtle's quest drop (Crustacean Carcass) added to Darkshore's Tide Crawlers and Young Reef Crawlers.
  - Shailiea (7295, Darnassus) gets the quest-giver flag ('A Secret Admirer' ends at her).

## Converter

- `config.json`: the zones 078 and 079.
- New `zones/078_teldrassil.json`, `zones/079_darnassus.json`, `manual/079_darnassus.py`.
- Docs: `ZONES.md`, new `zones/078_teldrassil.md` and `zones/079_darnassus.md`, and this file.
- Reports: `common.json`, new `078_teldrassil.json` and `079_darnassus.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `build.py` and `install_server_data.py` are not changed.
