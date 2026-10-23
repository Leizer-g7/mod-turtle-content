# Changed in the Moonwhisper Coast build (2026-10-12)

Compared with the Westfall + Deadmines delivery (2026-10-12, patch md5 5e4b3df96a0fff1ae3246f786d098fe2). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- ADT tiles: the 65 new Kalimdor tiles below and `Kalimdor_43_22.adt` (changed). If patch-z has its own copy of any of them, that copy hides this one.
- `World\Maps\Kalimdor\Kalimdor.wdt` (changed: the new tiles are marked present).
- `Textures\Minimap\md5translate.trs` (changed) and the 50 new minimap images `Textures\Minimap\Kalimdor\mapX_Y.blp`. patch-z has minimap images and a trs of its own: merge.
- Changed tables (9): `DBFilesClient\AreaTable.dbc`, `FactionTemplate.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, `TaxiNodes.dbc`, `TaxiPath.dbc`, `TaxiPathNode.dbc`, `WorldMapArea.dbc`, `WorldMapOverlay.dbc`. patch-z did not ship these tables as of the last handoff.

## Client patch (patch-y.mpq)

335,108,706 bytes (was 302,436,970), md5 445a76fb63c02e40d11d7f5a5e686c67, **14 parts** (was 13).

- Added ADT tiles (65), `World\Maps\Kalimdor\Kalimdor_X_Y.adt` for X_Y = 38_13, 38_14, 38_15, 39_12, 39_13, 39_14, 39_15, 40_12, 40_13, 40_14, 40_15, 40_16, 41_12, 41_13, 41_14, 41_15, 41_16, 41_21, 41_22, 41_23, 42_12, 42_13, 42_14, 42_15, 42_16, 42_17, 42_18, 42_19, 42_20, 42_21, 42_22, 43_12, 43_13, 43_14, 43_15, 43_16, 43_17, 43_18, 43_19, 43_20, 43_21, 44_13, 44_14, 44_15, 44_16, 44_17, 44_18, 44_19, 44_20, 44_21, 45_13, 45_14, 45_15, 45_16, 45_17, 45_18, 45_19, 45_20, 46_13, 46_14, 46_15, 46_16, 46_17, 46_18, 46_19.
- Changed ADT tiles (1): `World\Maps\Kalimdor\Kalimdor_43_22.adt` (Azshara's tile; the coast's chunks and a wrecked ship added on top). Changed: `Kalimdor.wdt`.
- Added minimap images (50): `Textures\Minimap\Kalimdor\map38_14, 38_15, 39_13-39_15, 40_13-40_16, 41_13-41_16, 41_21-41_23, 42_13-42_22, 43_13-43_21, 44_13-44_21, 45_14, 45_15, 45_17-45_20 .blp`; changed `Textures\Minimap\md5translate.trs`.
- Added world map: `Interface\WorldMap\Moonwhisper\` (30 images: the zone map and its subzone overlays).
- Added buildings: `World\wmo\Kalimdor\Buildings\FurbolgCave\FurbolgCaveHyjal_01.wmo` + `_000` to `_003` (the Blackroot furbolg caves; Turtle's copy, 3.3.5 does not have it).
- Changed tables (9): see above.
- Removed: none.
- Zone music: Turtle's own Moonwhisper tracks are not shipped; the areas play 3.3.5 music (Darkshore, Ashenvale, Mulgore plains).

## Server map tiles (server-data/maps)

- Added (65), Kalimdor: `0011239`-`0011243`, `0011338`-`0011346`, `0011438`-`0011446`, `0011538`-`0011546`, `0011640`-`0011646`, `0011742`-`0011746`, `0011842`-`0011846`, `0011942`-`0011946`, `0012042`-`0012045`, `0012141`-`0012144`, `0012241`, `0012242`, `0012341` (`.map`).
- Changed (1): `0012243.map` (tile 43_22).
- 53 other Kalimdor tiles and `0002736.map` came out of the map extractor with a different liquid-flag byte only; the delivered copies were kept.
- `install_server_data.bat` rebuilds the vmaps (the furbolg caves) and the Kalimdor mmaps around the new tiles, as before.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_043_moonwhisper_coast.sql` (+ its undo file).
- Changed (+ undo files where noted):
  - `mod_turtle_000_common.sql` (+ undo): the zone's items.
  - `mod_turtle_007_gilneas_city.sql` (+ undo): **fix** - the two Lovely Pink Foxes in Gilneas City spawned as Battlemage Vyara (Turtle's fox id 22211 is a 3.3.5 creature). They are now their own creature (5022211, coyote look).
  - `mod_turtle_006_gilneas.sql`: Willow now casts Curse of the Elements (stand-in for Turtle's Curse of Shadow, which was dropped before).
  - `mod_turtle_032_mulgore.sql` (+ undo): "One Heir to Another" (42070), from Moonhoof the Younger to Baine Bloodhoof, now exists (its giver is in Moonwhisper Coast).
  - `mod_turtle_039_burning_steppes.sql` (+ undo): "Raiments of Ritual" (41969), filed under Burning Steppes but given in Moonwhisper Coast, now exists.
- 3.3.5 rows the new file changes, restored by its undo file: the quest-giver flag of Hulfnar Stonetotem (Thunder Bluff).

## Converter

- `build.py`: `creature_id_remap` (a Turtle creature whose id 3.3.5 uses for a spawned creature gets 5,000,000 + its id: Elder Moonhoof 29479, Lovely Pink Fox 22211).
- `check.py`: an item the build maps to a same-named 3.3.5 item (ITEM_ALIAS) is no longer reported as "a different 3.3.5 item".
- `config.json`: the zone 087; `creature_id_remap`, `ids.creature_remap_base`; spell stand-ins (Wrath, Starshards, Curse of Shadow, Fade, Summon Skeleton, Starfire, Mana Burn, Arcane Vulnerability, Pure Moonfire, Empowered Dust); zone music stand-ins for Turtle's music ids 510, 514, 570-572 and intro 630; the Owlbear rock object model -> 3.3.5's same model (display 6843).
- `zones/051_gilneas_city.json`: the Lovely Pink Fox's look.
- New `zones/087_moonwhisper_coast.json`, `manual/087_moonwhisper_coast.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, new `zones/087_moonwhisper_coast.md` and this file; zone docs/reports of Gilneas, Gilneas City, Mulgore and Burning Steppes, `common.json`, new `087_moonwhisper_coast.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
- Extract job on the PC (`TWoW Data\turtle_extract`): `extract_jobs.json`, `extract_jobs_moonwhisper.json`, `extra_paths_moonwhisper.txt`, `client335_extract.py` (Moonwhisper region), `run_extract_moonwhisper.bat`.
