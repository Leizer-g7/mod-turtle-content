-- mod-turtle-content: Turtle's keyed doors, gates and chests (2026-10-12, approved by Max: proper key locks).
-- The converter left these 5 objects out because their locks are new rows of Turtle's Lock.dbc. 3.3.5 uses ids 1652-1657 for
-- other locks, so Turtle 1652/1653/1655/1656/1657 are added as 1861-1865: here for the server (lock_dbc), and in the client
-- patch (patch-z.mpq, DBFilesClient\Lock.dbc) so the client knows which key opens them.
--   2020156 Crawford Family Chest (Northwind, Winery Key or lockpicking 140)
--   2020163 Blackrock Coffer (Northwind, Blackrock Coffer Key or lockpicking 140; Throkk's Command for 'Covering All Possibilities')
--   2020232 Lower Reserve Gate (Dragonmaw Retreat, Lower Reserve Key or lockpicking 160)
--   2020233 Stormwrought Castle Gate (Balor / Stormwrought Ruins, Key to Stormwrought Castle or lockpicking 185)
--   2010842 Magically Sealed Door (Lapidis Isle, Lapidis Tower Key)
SET NAMES utf8mb4;

DELETE FROM `lock_dbc` WHERE `ID` IN (1861,1862,1863,1864,1865);
DELETE FROM `gameobject_template` WHERE `entry` IN (2020156,2020163,2020232,2020233,2010842);
DELETE FROM `gameobject_template_addon` WHERE `entry` IN (2020156,2020163,2020232,2020233,2010842);
DELETE FROM `gameobject_loot_template` WHERE `Entry` IN (2020163,5000102);
DELETE FROM `gameobject` WHERE `guid` BETWEEN 9990101 AND 9990199;

INSERT INTO `lock_dbc` (`ID`, `Type_1`, `Type_2`, `Type_3`, `Type_4`, `Type_5`, `Type_6`, `Type_7`, `Type_8`, `Index_1`, `Index_2`, `Index_3`, `Index_4`, `Index_5`, `Index_6`, `Index_7`, `Index_8`, `Skill_1`, `Skill_2`, `Skill_3`, `Skill_4`, `Skill_5`, `Skill_6`, `Skill_7`, `Skill_8`, `Action_1`, `Action_2`, `Action_3`, `Action_4`, `Action_5`, `Action_6`, `Action_7`, `Action_8`) VALUES
(1861, 1, 2, 2, 0, 0, 0, 0, 0, 1041676, 1, 16, 0, 0, 0, 0, 0, 0, 140, 140, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0),
(1862, 1, 2, 2, 2, 2, 0, 0, 0, 1041692, 1, 10, 11, 16, 0, 0, 0, 0, 140, 0, 0, 140, 0, 0, 0, 1, 1, 0, 2, 1, 0, 0, 0),
(1863, 1, 2, 2, 2, 2, 0, 0, 0, 1041876, 1, 10, 11, 16, 0, 0, 0, 0, 160, 0, 0, 160, 0, 0, 0, 1, 1, 0, 2, 1, 0, 0, 0),
(1864, 1, 2, 2, 2, 2, 0, 0, 0, 1041913, 1, 10, 11, 16, 0, 0, 0, 0, 185, 0, 0, 185, 0, 0, 0, 1, 1, 0, 2, 1, 0, 0, 0),
(1865, 1, 0, 0, 0, 0, 0, 0, 0, 60302, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`, `Data0`, `Data1`, `Data2`, `Data3`, `Data4`, `Data5`, `Data6`, `Data7`, `Data8`, `Data9`, `Data10`, `Data11`, `Data12`, `Data13`, `Data14`, `Data15`, `Data16`, `Data17`, `Data18`, `Data19`, `Data20`, `Data21`, `Data22`, `Data23`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES
(2020156, 3, 41, 'Crawford Family Chest', '', '', '', 1.0, 1861, 5000102, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2020163, 3, 4192, 'Blackrock Coffer', '', '', '', 1.0, 1862, 2020163, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2020232, 0, 3614, 'Lower Reserve Gate', '', '', '', 1.15, 0, 1863, 196608, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2020233, 0, 3614, 'Stormwrought Castle Gate', '', '', '', 0.8, 0, 1864, 196608, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0),
(2010842, 0, 415, 'Magically Sealed Door', '', '', '', 2.45983, 0, 1865, 196608, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', 0);

INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`, `mingold`, `maxgold`, `artkit0`, `artkit1`, `artkit2`, `artkit3`) VALUES
(2020156, 0, 2, 0, 0, 0, 0, 0, 0),
(2020163, 0, 6, 0, 0, 0, 0, 0, 0),
(2020232, 0, 34, 0, 0, 0, 0, 0, 0),
(2020233, 0, 34, 0, 0, 0, 0, 0, 0),
(2010842, 0, 32, 0, 0, 0, 0, 0, 0);

INSERT INTO `gameobject_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES
(5000102, 422, 0, 16.67, 0, 1, 1, 1, 1, 'Dwarven Mild'),
(5000102, 929, 0, 25.0, 0, 1, 0, 1, 1, 'Healing Potion'),
(5000102, 1205, 0, 16.67, 0, 1, 1, 1, 1, 'Melon Juice'),
(5000102, 1206, 0, 0.5, 0, 1, 0, 1, 1, 'Moss Agate'),
(5000102, 1705, 0, 0.5, 0, 1, 0, 1, 1, 'Lesser Moonstone'),
(5000102, 3770, 0, 16.67, 0, 1, 1, 1, 1, 'Mutton Chop'),
(5000102, 4538, 0, 16.67, 0, 1, 1, 1, 1, 'Snapvine Watermelon'),
(5000102, 4542, 0, 16.67, 0, 1, 1, 1, 1, 'Moist Cornbread'),
(5000102, 4606, 0, 16.67, 0, 1, 1, 1, 1, 'Spongy Morel'),
(2020163, 1041691, 0, 100.0, 1, 1, 0, 1, 1, 'Throkk\'s Command');

INSERT INTO `gameobject` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `position_x`, `position_y`, `position_z`, `orientation`, `rotation0`, `rotation1`, `rotation2`, `rotation3`, `spawntimesecs`, `animprogress`, `state`, `ScriptName`, `VerifiedBuild`, `Comment`) VALUES
(9990101, 2020156, 0, 0, 0, 1, 1, -7678.98, 402.149, 70.8198, 5.44041, 0.0, 0.0, 0.409027, -0.912522, 300, 100, 1, '', 0, 'turtle key locks: Crawford Family Chest (tw guid 5022290)'),
(9990102, 2020163, 0, 0, 0, 1, 1, -7022.99, 494.857, 146.038, 0.693281, 0.0, 0.0, 0.33974, 0.940519, 300, 100, 1, '', 0, 'turtle key locks: Blackrock Coffer (tw guid 5022904)'),
(9990103, 2020232, 816, 0, 0, 1, 1, -6120.16, -4403.58, 300.978, 3.1925, 0.0, 0.0, 0.999676, -0.025451, 300, 100, 1, '', 0, 'turtle key locks: Lower Reserve Gate (tw guid 5025418)'),
(9990104, 2020233, 818, 0, 0, 1, 1, -6068.09, -4098.55, 218.912, 4.73473, 0.0, 0.0, 0.699164, -0.714961, 300, 100, 1, '', 0, 'turtle key locks: Stormwrought Castle Gate (tw guid 5025419)'),
(9990105, 2020233, 0, 0, 0, 1, 1, -9320.9, 2989.49, 118.896, 3.27495, 0.0, 0.0, 0.997778, -0.066629, 300, 100, 1, '', 0, 'turtle key locks: Stormwrought Castle Gate (tw guid 5025440)'),
(9990106, 2020233, 818, 0, 0, 1, 1, -6386.89, -3829.02, 218.569, 3.14043, 0.0, 0.0, 1.0, 0.000581, 300, 100, 1, '', 0, 'turtle key locks: Stormwrought Castle Gate (tw guid 5026069)'),
(9990107, 2010842, 0, 0, 0, 1, 1, -11688.6, 3193.14, 51.6003, 2.5954, 0.0, 0.0, 0.962941, 0.269713, 0, 100, 1, '', 0, 'turtle key locks: Magically Sealed Door (tw guid 5000020)');
