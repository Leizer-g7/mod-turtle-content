# Changed in the Tirisfal Glades + Undercity build (2026-10-11, third delivery of the day)

Compared with the Eastern Plaguelands delivery made earlier the same day (patch md5 a31eafd2be606d8e9c9b48cd3bedf4e0). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`: changed (the 15 new Tirisfal subzones, object models, items). patch-z did not ship these tables as of the last handoff.
- ADT tiles: Azeroth 26_27, 26_28, 27_27, 27_28, 27_29, 28_27, 28_28, 28_29, 33_26, 33_27 (new). If patch-z has its own copy of any of them, that copy hides this one.
- `Textures\Minimap\md5translate.trs`: not changed (the 3.3.5 minimap images are kept; the new west coast shows 3.3.5's sea on the minimap).

## Client patch (patch-y.mpq)

290,939,550 bytes (was 284,251,629).

- Added ADT tiles (10): `World\Maps\Azeroth\Azeroth_26_27.adt`, `Azeroth_26_28.adt`, `Azeroth_27_27.adt`, `Azeroth_27_28.adt`, `Azeroth_27_29.adt`, `Azeroth_28_27.adt`, `Azeroth_28_28.adt`, `Azeroth_28_29.adt`, `Azeroth_33_26.adt`, `Azeroth_33_27.adt`.
- Changed tables (3): `DBFilesClient\AreaTable.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`.
- No new buildings, textures or minimap images (Turtle's farms, towers, caves and the second Scarlet building are 3.3.5 models). Removed: none.

## Server map tiles (server-data/maps)

- Added (10), Azeroth: `0002633.map`, `0002726.map`, `0002727.map`, `0002728.map`, `0002733.map`, `0002826.map`, `0002827.map`, `0002828.map`, `0002927.map`, `0002928.map`.
- Changed: none. (`0002736.map`, an Eastern Plaguelands tile, came out with a few different liquid bytes - the map_extractor leftover - and the delivered copy was kept.)
- `install_server_data.bat` rebuilds vmaps and mmaps for Eastern Kingdoms (map 0).

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_037_tirisfal_glades.sql`, `mod_turtle_038_undercity.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zones' items.
- 3.3.5 rows the new files change, all restored by their undo files:
  - Turtle's quest drops: Human Blood on Tirisfal Farmers / Farmhands ('Virulence'), Fine Free-Range Alterac Yeti Hide on Giant Yetis ('Fair Trade' Is Not Legally Defined in Azeroth).
  - Eight 3.3.5 creatures (murlocs, wild turkeys) and three objects (Silverleaf, Peacebloom, a Copper Vein) at the Whispering Shore moved onto Turtle's new ground.
  - Turtle quests started or ended by 3.3.5 NPCs (quest-relation rows only).

## Converter

- `build.py`: `exclude_boxes`, z ranges in `spawn_boxes`, `faction_keep_335`.
- `config.json`: the zones 081 and 082; `faction_keep_335` [709].
- New `zones/081_tirisfal_glades.json`, `zones/082_undercity.json`, `manual/081_tirisfal_glades.py`, `manual/082_undercity.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/081_tirisfal_glades.md` and `zones/082_undercity.md`, and this file.
- Reports: `common.json`, new `081_tirisfal_glades.json` and `082_undercity.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
- Extract tools (outside the module, `TWoW Data\turtle_extract`, already on the PC): `mpqread.py` and `turtle_extract.py` (empty files in Turtle's patches); the originals are kept as `.bak`.
