# Changed in the Westfall + Deadmines build (2026-10-12)

Compared with the Burning Steppes + Hateforge Quarry delivery (2026-10-11, patch md5 683a404750d9dece015ad623c6665772). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- ADT tiles: Azeroth 27_50 and 28_51 (new), 26_52, 27_52 and 27_53 (changed). If patch-z has its own copy of any of them, that copy hides this one.
- `Textures\Minimap\md5translate.trs` (changed) and minimap images `Textures\Minimap\Azeroth\map27_52.blp`, `map27_53.blp` (new). patch-z has minimap images and a trs of its own: merge.
- `DBFilesClient\AreaTable.dbc` (Gartside Plot), `Item.dbc`: changed. patch-z did not ship these tables as of the last handoff.

## Client patch (patch-y.mpq)

302,436,970 bytes (was 296,319,541), md5 5e4b3df96a0fff1ae3246f786d098fe2, **13 parts** (was 12).

- Added ADT tiles (2): `World\Maps\Azeroth\Azeroth_27_50.adt`, `Azeroth_28_51.adt`.
- Changed ADT tiles (3): `World\Maps\Azeroth\Azeroth_26_52.adt`, `Azeroth_27_52.adt`, `Azeroth_27_53.adt` (Lapidis Isle's tiles; Westfall's Longshore coast and sea chunks added on top).
- Added minimap images (2): `Textures\Minimap\Azeroth\map27_52.blp`, `map27_53.blp`; changed `Textures\Minimap\md5translate.trs`.
- Added buildings: `HumanHouse\WestfallHouse_SmallStraw.wmo` + `_000.wmo` (Maltimor Gartside's house; Turtle's own path) and its 16 textures under `World\Generic\Human\Buildings\Houses\`.
- **The Deadmines building replaced**: `World\wmo\Dungeon\AZ_Deadmines\AZ_Deadmines_B.wmo` + `_000` to `_048.wmo` (50 files). Turtle's copy is 3.3.5's (the same 44 parts with the same ids, including Wrath's two) with two doorways widened and 5 new parts: Jared Voss' alchemy lab east of the Goblin Foundry. The lab's harvest-golem props are a Turtle-made model; 3.3.5's Harvest Golem stands in.
- Changed tables (2): `DBFilesClient\AreaTable.dbc`, `Item.dbc`.
- Removed: none.

## Server map tiles (server-data/maps)

- Added (2), Azeroth: `0005027.map`, `0005128.map`.
- Changed (3): `0005226.map`, `0005227.map`, `0005327.map`. (`0002736.map`, the Eastern Plaguelands tile, came out with the map_extractor liquid noise again and the delivered copy was kept.)
- `install_server_data.bat` rebuilds all vmaps (the Deadmines' new rooms are in them) and the map 0 mmaps around the Turtle tiles.
- **New `rebuild_mmaps_map.bat` / `rebuild_mmaps_map.py`**: rebuilds the pathing (mmaps) of the Deadmines (map 36) after install_server_data. The installer only rebuilds mmaps of maps with Turtle terrain tiles, and the Deadmines is one building with no tiles: without this the lab's mobs cannot chase or walk home. It uses the install_server_data.py next to it (your fixed one) for the folders and tools, asks before changing anything and backs up the old map 36 mmaps (RESTORE.bat).

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_041_westfall.sql`, `mod_turtle_042_deadmines.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo): the zones' items.
- 3.3.5 rows the new files change, all restored by their undo files:
  - SmartAI and texts (groups 100+) for Franklin Hamar, Brother Neals, Captain Grayson and Gryan Stoutmantle; gossip menus (and the gossip flag) for Brother Neals and Captain Grayson.
  - Turtle's quest drops on 3.3.5 creatures: Animation Runes (Westfall harvest golems), Moonlight Silk (Duskwood spiders), Greater Tarantula Venom, Grayson's Pendant (Cookie, the Deadmines).
  - The Defias Highwayman whose spot Carver Molsen takes at the Dead Acre is removed; a Peacebloom and a Copper Vein at Gartside Plot are lifted onto the new ground.
  - Turtle quests started or ended by 3.3.5 NPCs (quest-relation rows; quest-giver flag for Franklin Hamar and Christopher Hewen).

## Converter

- `build.py`: `ship_wmos` (a Turtle building shipped whole, also on a zone without Turtle terrain).
- `config.json`: the zones 085 and 086; `m2_substitutions` for the harvest-golem props.
- New `zones/085_westfall.json`, `zones/086_deadmines.json`, `manual/085_westfall.py`, `manual/086_deadmines.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/085_westfall.md`, `zones/086_deadmines.md` and this file.
- Reports: `common.json`, new `085_westfall.json`, `086_deadmines.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
- Extract job on the PC (`TWoW Data\turtle_extract`): `extract_jobs.json`, `extract_jobs_westfall.json`, `extra_paths_westfall.txt`, `client335_extract.py` (Westfall region), `run_extract_westfall.bat`.
