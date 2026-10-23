# Changed in the Eastern Plaguelands build (2026-10-11, second delivery of the day)

Compared with the Teldrassil + Darnassus delivery made earlier the same day (patch md5 a494231ee2046a7463727666c4ca7a74). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`: changed (the new subzone Forlorn Summit, object models, items). patch-z did not ship these tables as of the last handoff.
- ADT tiles: Azeroth 36_26, 36_27, 37_26, 37_27 (new). If patch-z has its own copy of any of them, that copy hides this one.
- `Textures\Minimap\md5translate.trs`: not changed (Turtle changed fewer than 128 chunks per tile, so the 3.3.5 minimap images are kept).

## Client patch (patch-y.mpq)

284,251,629 bytes (was 280,643,378).

- Added ADT tiles (4): `World\Maps\Azeroth\Azeroth_36_26.adt`, `Azeroth_36_27.adt`, `Azeroth_37_26.adt`, `Azeroth_37_27.adt`.
- Changed tables (3): `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`.
- No new buildings, textures or minimap images (Forlorn Summit's buildings and the spider cave are 3.3.5 models). Removed: none.

## Server map tiles (server-data/maps)

- Added (4), Azeroth: `0002636.map`, `0002637.map`, `0002736.map`, `0002737.map`.
- Changed: none. (`0003228.map` came out of the build with 8 different bytes, a map_extractor leftover; the delivered copy was kept. See ADDING_A_ZONE.md.)
- `install_server_data.bat` rebuilds vmaps and mmaps for Eastern Kingdoms (map 0).

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_036_eastern_plaguelands.sql` (+ its undo file).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zone's items.
- 3.3.5 rows the new file changes, all restored by its undo file:
  - Turtle's quest drop (the brains for 'It's All in Their Brains', 80710) added to four 3.3.5 Plaguelands creatures' loot.
  - Turtle quests started or ended by 3.3.5 NPCs (quest-relation rows only, no NPC row changed): Lord Maxwell Tyrosus, Leonid Barthalomew the Revered, Quartermaster Miranda Breechlock (Light's Hope), Brother Crowley (Stormwind), Gunther Arcanus (Undercity).

## Converter

- `build.py`: `merge_region.exclude_chunks` (chunks never taken from Turtle).
- `config.json`: the zone 080.
- New `zones/080_eastern_plaguelands.json`, `manual/080_eastern_plaguelands.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/080_eastern_plaguelands.md`, and this file.
- Reports: `common.json`, new `080_eastern_plaguelands.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
