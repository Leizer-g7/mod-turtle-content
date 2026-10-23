# Changed in the Dun Morogh + Frostmane Hollow build (2026-10-10, third delivery of the day)

Compared with the Tanaris + Zul'Farrak delivery made earlier the same day (patch md5 d2c7e6ac46061c41573f316adb2fce11). Everything that is not listed here is byte-identical to that delivery. In the SQL folder, files whose only change was the build-date line were kept as delivered, so the database updater doesn't run them again.

## Overlap with Max's patch-z

Nothing here is a patch-z file. patch-z loads after patch-y, so anything patch-z also has will keep showing Max's copy:

- `Textures\Minimap\md5translate.trs`: changed. It has 10 new lines (Azeroth 30_41, 31_41, 32_40, 32_41, 33_40, 33_41, 34_41, 35_41, 35_43, 36_43) and 2 changed ones (34_40, 35_40). If patch-z ships its own trs, merge these lines into it.
- `DBFilesClient\AreaTable.dbc`, `AreaTrigger.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, `LoadingScreens.dbc`, `Map.dbc`, `MapDifficulty.dbc`, `WorldMapArea.dbc`: changed. They gain the new areas (Frostmane Hollow, Rugford's Mountain Rest, Ironforge Airfields), the Frostmane Hollow map, its two area triggers, loading screen and dungeon row, object models and items. patch-z did not ship these tables as of the last handoff (its table is WorldMapOverlay.dbc, which is not changed here).
- ADT tiles: Azeroth 30_41, 31_40, 31_41, 32_40, 32_41, 33_40, 33_41, 34_40, 34_41, 35_40, 35_41, 35_43, 36_43, and the nine FrostmaneCaverns tiles. If patch-z has its own copy of any of them, that copy hides this one.

## Client patch (patch-y.mpq)

272,256,329 bytes (was 259,468,661).

- Added ADT tiles and WDT (21):
  - `World\Maps\Azeroth\Azeroth_30_41.adt`, `Azeroth_31_40.adt`, `Azeroth_31_41.adt`, `Azeroth_32_40.adt`, `Azeroth_32_41.adt`, `Azeroth_33_40.adt`, `Azeroth_33_41.adt`, `Azeroth_34_41.adt`, `Azeroth_35_41.adt`, `Azeroth_35_43.adt`, `Azeroth_36_43.adt`
  - `World\Maps\FrostmaneCaverns\FrostmaneCaverns.wdt` and `FrostmaneCaverns_37_45.adt`, `_37_46`, `_37_47`, `_38_45`, `_38_46`, `_38_47`, `_39_45`, `_39_46`, `_39_47`
- Changed ADT tiles (2): `World\Maps\Azeroth\Azeroth_34_40.adt`, `World\Maps\Azeroth\Azeroth_35_40.adt` (earlier zones' tiles, now with Dun Morogh's chunks too).
- Added minimap images (10): `Textures\Minimap\Azeroth\map30_41.blp`, `map31_41.blp`, `map32_40.blp`, `map32_41.blp`, `map33_40.blp`, `map33_41.blp`, `map34_41.blp`, `map35_41.blp`, `map35_43.blp`, `map36_43.blp`. Changed (2): `map34_40.blp`, `map35_40.blp`.
- Added buildings (WMO root + group files, 50):
  - `WORLD\WMO\DUNGEON\TT_NEWTINKERTOWN\TINKERTOWN.WMO` + groups `_000` to `_020` (the Gnomeregan Reclamation Facility)
  - `world\wmo\dungeon\AZ_FrostmaneCaverns\frostmanecave.wmo` + groups `_000` to `_006` (the Frostmane Hollow entrance cave in Dun Morogh)
  - `world\wmo\dungeon\AZ_FrostmaneCaverns\FrostmaneRetreat.wmo` + groups `_000` to `_018` (the dungeon)
- Added textures (35): `Interface\Glues\LoadingScreens\LoadScreenFrostmane.blp`; 4 under `dungeons\textures\draktharon\`; 17 under `dungeons\textures\rock\` (the `jlo_mcaves_*` set and the `stormpeaks cave variant` set); 13 under `world\environment\doodad\tanaris\textures\froz\`.
- Changed tables (9): `DBFilesClient\AreaTable.dbc`, `AreaTrigger.dbc`, `GameObjectDisplayInfo.dbc`, `Item.dbc`, `LoadingScreens.dbc`, `Map.dbc`, `MapDifficulty.dbc`, `WorldMapArea.dbc`, and `Textures\Minimap\md5translate.trs`.
- Removed: none.

## Server map tiles (server-data/maps)

- Added (20):
  - Dun Morogh (map 0): `0004031.map`, `0004032.map`, `0004033.map`, `0004130.map`, `0004131.map`, `0004132.map`, `0004133.map`, `0004134.map`, `0004135.map`, `0004335.map`, `0004336.map`.
  - Frostmane Hollow (map 822): `8224537.map`, `8224538.map`, `8224539.map`, `8224637.map`, `8224638.map`, `8224639.map`, `8224737.map`, `8224738.map`, `8224739.map`.
- Changed (2): `0004034.map`, `0004035.map`.
- `install_server_data.bat` rebuilds vmaps and mmaps for map 0 and map 822, so the new caves and the Reclamation Facility get collision.

## SQL (data/sql/db-world, sql_rollback)

- New: `mod_turtle_030_dun_morogh.sql`, `mod_turtle_031_frostmane_hollow.sql` (+ their undo files).
- Changed: `mod_turtle_000_common.sql` (+ undo; items and reference loot of the two zones).
- Changed: `mod_turtle_006_gilneas.sql` (+ undo). It picks up 'The Dawnstone Coupler' (40860), whose NPC (Technician Voltgear) Dun Morogh now spawns.
- Changed: `mod_turtle_022_badlands.sql` (+ undo). It picks up Senator Ryedol's three Badlands quests (40652-40654), now that Dun Morogh spawns him in Ironforge.
- Changed: `mod_turtle_012_wetlands.sql`. Two quests filed under area 4020 now use 6102, the id the module gives Turtle's Ironforge Airfields.
- Changed: `mod_turtle_013_dragonmaw_retreat.sql`, `mod_turtle_019_windhorn_canyon.sql`. The bosses' aggro, 50 % and death lines are now included: the converter reads Turtle's `script_texts` for them.
- 3.3.5 rows the new files change, all restored by their undo files:
  - Prospector Gehn (1255) gets a menu (Gol'Bolar Ore for 'Mastering the Formula II').
  - Spell 10260 Reconstruct may also target Hailar the Frigid (an extra conditions row).
  - Ice Claw Bear (1196) follows the Frostmane Tamer that summoned it.
  - Three 3.3.5 spawns raised onto the new ground: creature 2276, Copper Veins 205235 and 205392.
  - Turtle's quest drops added to Rockjaw troggs, Old Icebeard and Frostmane Seers.
  - Frostmane Hollow overwrites four unused 3.3.5 test templates (19, 67, 82, 108) with Turtle's creatures of the same ids; its undo file puts the stock rows back.

## Converter

- `build.py`:
  - `creature_id_takeover` and `spawn_boxes`.
  - EventAI talk lines read Turtle's `script_texts` when the id is negative.
  - `dungeon_access_template` ids continue below 250 once 250-255 are used.
- `config.json`:
  - The zones 074 and 075.
  - `area_id_remap` 4020 -> 6102.
  - `creature_id_takeover` (19, 67, 82, 108).
  - Spell stand-ins 33397 -> 12255, 33398 -> 3237, 33399 dropped (the manual script summons the bear).
- `lib/smartgen.py`: the `invoker_party` target.
- New `zones/074_dun_morogh.json`, `zones/075_frostmane_hollow.json`, `manual/074_dun_morogh.py`, `manual/075_frostmane_hollow.py`.
- Docs: `ADDING_A_ZONE.md`, `ZONES.md`, `zones/050_gilneas.md`, `zones/057_dragonmaw_retreat.md`, `zones/063_windhorn_canyon.md`, `zones/066_badlands.md`, new `zones/074_dun_morogh.md` and `zones/075_frostmane_hollow.md`, and this file.
- Reports: `050_gilneas.json`, `057_dragonmaw_retreat.json`, `063_windhorn_canyon.json`, `066_badlands.json`, `common.json`, new `074_dun_morogh.json` and `075_frostmane_hollow.json`.
- Also changed: `client/client_tables.json`, `server-data/tiles.json`, `server-data/required_assets.txt`. `install_server_data.py` is not changed.
