# Changed in the Wailing Caverns build (2026-10-12)

Compared with the Moonwhisper Coast delivery (2026-10-12, patch md5 445a76fb63c02e40d11d7f5a5e686c67). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- No ADT tiles, server map tiles or minimap images changed (the Wailing Caverns is one building, no terrain).
- Changed tables (2): `DBFilesClient\WMOAreaTable.dbc` (3 room names), `Item.dbc`. patch-z did not ship these tables as of the last handoff.
- The building's 27 files below: if patch-z has its own copy of any of them, that copy hides this one.

## Client patch (patch-y.mpq)

340,279,514 bytes (was 335,108,706), md5 a0d221a798f392fc638b0e257ef59347, **14 parts** (as before).

- **The Wailing Caverns building replaced**: `World\wmo\Dungeon\KL_Wailing\wailingcaverns_instance.wmo` + `_000` to `_025.wmo` (27 files). Turtle's copy is 3.3.5's (the same 23 parts with the same ids; every 3.3.5 collision point is in it, except a few in the Winding Chasm and one in a side passage where the openings to the new parts are) with 3 new parts: The Overgrowth (two parts, beyond the Winding Chasm) and Kolkar Falls (on the other side). It uses only textures and models the 3.3.5 client already has.
- Changed tables (2): `DBFilesClient\WMOAreaTable.dbc` (The Overgrowth x2, Kolkar Falls), `Item.dbc`.
- Not taken: Turtle's world-map images and loading screen of the dungeon (3.3.5's stay).
- Removed: none. Added ADT tiles / minimap images: none.

## Server map tiles (server-data/maps)

- Added: none. Changed: none. (54 tiles came out of the map extractor with only the liquid-flag byte changed again; the delivered copies were kept.)
- `install_server_data.bat` rebuilds all vmaps (the new parts are in them).
- **New `rebuild_mmaps_wailing_caverns.bat`**: rebuilds the pathing (mmaps) of the Wailing Caverns (map 43) after install_server_data, like `rebuild_mmaps_map.bat` does for the Deadmines (it runs `rebuild_mmaps_map.py 43`). Without it the new parts' mobs cannot chase or walk home.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_044_wailing_caverns.sql` (+ its undo file).
- Changed: `mod_turtle_000_common.sql` (+ undo): the dungeon's items.
- 3.3.5 rows the new file changes: none besides quest relations on 3.3.5 NPCs (Thundris Windweaver, Alanndarian Nightsong, Nalpak), deleted by its undo file.

## Converter

- `build.py`: `wmo_area_groups` (only some WMO group ids get room names); `extra_gameobject_spawns` now also spawns 3.3.5 objects (herbs) - no earlier zone listed any, their SQL is unchanged.
- `config.json`: the zone 088.
- New `zones/088_wailing_caverns.json`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/088_wailing_caverns.md` and this file. Reports: `common.json`, new `088_wailing_caverns.json`.
- Also changed: `client/client_tables.json`. `install_server_data.py` is not changed.
- Extract job on the PC (`TWoW Data\turtle_extract`): `extract_jobs.json`, `extract_jobs_wailingcaverns.json`, `extra_paths_wailingcaverns.txt`, `run_extract_wailingcaverns.bat` (`client335_extract.py` unchanged).
