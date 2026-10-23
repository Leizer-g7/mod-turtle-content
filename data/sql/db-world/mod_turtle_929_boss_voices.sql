-- mod-turtle-content 929: Turtle WoW boss voice-overs (Claude, 2026-10-13).
-- Turtle plays a recorded voice line with these boss texts (script_texts / broadcast_text sound,
-- and PlayDirectSound in instance_gilneas_city / instance_crescent_grove). The sound files and the
-- client SoundEntries rows ship in client\patch-z.mpq; this file adds the same rows on the server
-- (so creature_text accepts the Sound ids) and sets Sound on the matching texts.
-- Safe to run again. Rollback: DELETE FROM soundentries_dbc WHERE ID IN (...below...); UPDATE creature_text SET Sound=0 for the rows below.

DELETE FROM `soundentries_dbc` WHERE `ID` IN (30252,30253,30256,30258,30268,30270,30271,30273,60348,60349,60350,60351,60352,60353,60354,60355,60356,60360,60361,60362,60382,60383,60384,60385,60386,60387,60388,60389,60390,60391,60392,60399,60400,60492,60493,60494,60495,60496,60497,60498,60499,60500,60501,60502,60503,60504,60505,60506,60507,60512,60513,60514,60515,60516,60517,60518,60519,60520,60521,60522,60523,60524,60525,60526,60527,60528,60529,60586,60587,60588,60589,60590,60591,60592,60593,60594,60595,60596,60597,60598,60599,60600,60601,60602,60603,60605,60606,60607,60608,60609,60610,60621,60622,60623,60634,60635,60636,60663,60664,60665,60666,60667,60668,60669,60670,60671,60673,60674,60675,60676,60677,60678,60679,60680,60681,60706,60707,60708,60709,60710,60711);
INSERT INTO `soundentries_dbc` (`ID`,`SoundType`,`Name`,`File_1`,`File_2`,`File_3`,`File_4`,`File_5`,`File_6`,`File_7`,`File_8`,`File_9`,`File_10`,`Freq_1`,`Freq_2`,`Freq_3`,`Freq_4`,`Freq_5`,`Freq_6`,`Freq_7`,`Freq_8`,`Freq_9`,`Freq_10`,`DirectoryBase`,`Volumefloat`,`Flags`,`MinDistance`,`DistanceCutoff`,`EAXDef`,`SoundEntriesAdvancedID`) VALUES
(30252,17,'Satyrboss_Aggro','Satyrboss_1.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30253,17,'Satyrboss_Death','Satyrboss_2.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30256,17,'Keeperboss_Aggro','Keeperboss_01.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30258,17,'Keeperboss_Death','Keeperboss_03.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30268,17,'Furbolgboss_Aggro','FurbolgBoss_Aggro.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30270,17,'FurbolgBoss_Dead','FurbolgBoss_Dead.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30271,17,'DemonBoss_Aggro','DemonBoss_Aggro.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(30273,17,'DemonBoss_DeathLine','DemonBoss_DeathLine.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60348,17,'BlackhammerAggro','Aggro.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60349,17,'BlackhammerShout1','Shout1.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60350,17,'BlackhammerShout2','Shout2.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60351,17,'BlackhammerShout3','Shout3.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60352,17,'BlackhammerDeath','BDeath.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60353,17,'Figgles1','Figgles1.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60354,17,'Figgles2','Figgles2.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60355,17,'Hatereaver1','Hatereaver1.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60356,17,'Hatereaver2','Hatereaver2.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60360,17,'Doomcaller1','Doomcaller1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60361,17,'Doomcaller2','Doomcaller2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60362,17,'DoomcallerVoidHungers','DoomcallerVoidHungers.wav','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,0,8.0,45.0,0,0),
(60382,10,'Sutherland1','Sutherland1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60383,10,'Sutherland2','Sutherland2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60384,10,'Holtz1','Holtz1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60385,10,'Holtz2','Holtz2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60386,10,'Greystone1','Greystone1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60387,10,'Greystone2','Greystone2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60388,10,'Greymane1','Greymane1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60389,10,'Greymane2','Greymane2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60390,10,'Greymane3','Greymane3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60391,10,'Blackcowl1','Blackcowl1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60392,10,'Blackcowl2.mp3','Blackcowl2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60399,10,'Celia1','Celia1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60400,10,'Celia2','Celia2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60492,10,'Garlok_aggro','GarlokFlamekeeper1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60493,10,'Garlok_half','GarlokFlamekeeper2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60494,10,'Garlok_death','GarlokFlamekeeper3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60495,10,'Redbrand_aggro','Redbrand1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60496,10,'Redbrand_half','Redbrand2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60497,10,'Redbrand_death','Redbrand3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60498,10,'Sear_aggro','Searistraz1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60499,10,'Sear_half','Searistraz2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60500,10,'Sear_death','Searistraz3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60501,10,'Slag_Aggro','Slagfistdestroyer1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60502,10,'Slag_half','Slagfistdestroyer2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60503,10,'Slag_death','Slagfistdestroyer3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60504,10,'Zulu_aggro','Zuluhed1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60505,10,'Zulu_drain','Zuluhed2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60506,10,'Zulu_mindcontrol','Zuluhed3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60507,10,'Zulu_death','Zuluhed4.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60512,10,'Zeljeb_aggro','Zeljeb1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60513,10,'Zeljeb_half','Zeljeb2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60514,10,'Zeljeb_death','Zeljeb3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60515,10,'Kathzen_aggro','Kathzen.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60516,10,'Juthza_aggro','Juthza.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60517,10,'Razjal_aggro','Razjal1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60518,10,'Razjal_hellfire','Razjal2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60519,10,'Razjal_sand','Razjalsand.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60520,10,'Torkon_aggro','Torkon1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60521,10,'Torkon_half','Torkon2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60522,10,'Torkon_death','Torkon3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60523,10,'Blackheart_aggro','Blackheart1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60524,10,'Blackheart_half','Blackheart2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60525,10,'Blackheart_death','Blackheart3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60526,10,'Sear_enchant','SearistrazEnchantment.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60527,10,'Gowlfang_aggro','Gowlfang1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60528,10,'Gowlfang_half','Gowlfang2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60529,10,'Gowlfang_death','Gowlfang3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60586,10,'DukeBalor_Aggro','Balor1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60587,10,'DukeBalor_Death','Balor2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60588,10,'Stormsong_Aggro','Stormsong1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60589,10,'Stormsong_Death','Stormsong2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60590,10,'Dagar_Aggro','Dagar1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60591,10,'Dagar_Death','Dagar2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60592,10,'Hollowblood_Aggro','Hollowblood1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60593,10,'Hollowblood_Cast','Hollowblood2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60594,10,'Hollowblood_Death','Hollowblood3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60595,10,'Oronok_Aggro','Oronok1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60596,10,'Oronok_Death','Oronok2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60597,10,'Tidebane_Aggro','Tidebane1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60598,10,'Tidebane_Cast','Tidebane3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60599,10,'Tidebane_Death','Tidebane2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60600,10,'Ighal_Pull','Ighal_Pull.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60601,10,'Ighal_Pull2','Ighal_Pull2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60602,10,'Ighal_Summon','Ighal_Summon.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60603,10,'Ighal_Mergothid','Ighal_Mergothid.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60605,10,'Halthas_Aggro','Halthas1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60606,10,'Halthas_Cast','Halthas2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60607,10,'Halthas_Death','Halthas3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60608,10,'Drazare_Aggro','Drazare1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60609,10,'Drazare_Half','Drazare2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60610,10,'Drazare_Death','Drazare3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60621,10,'Mergothid_Summon','Mergothid_Summon.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60622,10,'Mergothid_Aggro','Mergothid_Aggro.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60623,10,'Mergothid_Death','Mergothid_Death.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60634,10,'Librarian_Aggro','LibrarianAggro.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60635,10,'Librarian_Waves','Librarian_Waves.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60636,10,'Librarian_Death','Librarian_Death.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60663,10,'Pathun_Aggro','Pathun1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60664,10,'Pathun_Half','Pathun2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60665,10,'Pathun_Death','Pathun3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60666,10,'Walgan_Aggro','Walgan1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60667,10,'Walgan_Half','Walgan2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60668,10,'Walgan_Death','Walgan3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60669,10,'Prophet_Aggro','Prophetstorm1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60670,10,'Prophet_Half','Prophetstorm2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60671,10,'Prophet_Death','Prophetstorm3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60673,10,'Shalk_Aggro','Shalk1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60674,10,'Shalk_Half','Shalk2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60675,10,'Shalk_Death','Shalk3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60676,10,'Vortalus_Aggro','Vortalus1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60677,10,'Vortalus_Half','Vortalus2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60678,10,'Vortalus_Death','Vortalus3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60679,10,'Narlgom_Aggro','Narlgom1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60680,10,'Narlgom_Half','Narlgom2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60681,10,'Narlgom_Death','Narlgom3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60706,10,'Hailar_pull','Hailar1.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60707,10,'Hailar_50%','Hailar2.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60708,10,'Hailar_Death','Hailar3.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60709,10,'Oboka','HandlerOboka.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60710,10,'Ubukaz','BattlemasterUbukaz.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0),
(60711,10,'Kanza','Kanza.mp3','','','','','','','','','',1,1,1,1,1,1,1,1,1,1,'Sound\\Interface\\VA',1.0,32,0.0,300.0,0,0);

-- creature_text rows that Turtle voices (same text as Turtle's line)
UPDATE `creature_text` SET `Sound`=60667 WHERE `CreatureID`=1840 AND `GroupID`=6 AND `ID`=0 AND `Sound`=0; -- Enough!
UPDATE `creature_text` SET `Sound`=60667 WHERE `CreatureID`=28996 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Enough!
UPDATE `creature_text` SET `Sound`=60667 WHERE `CreatureID`=30396 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- ENOUGH!
UPDATE `creature_text` SET `Sound`=60400 WHERE `CreatureID`=61263 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Mortimer, it would appear we have someone here to interrupt our plans!
UPDATE `creature_text` SET `Sound`=60399 WHERE `CreatureID`=61263 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- All of our progress, our influence... What a pointless end...
UPDATE `creature_text` SET `Sound`=60388 WHERE `CreatureID`=61418 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- My family has held power in Gilneas for countless generations. You wil
UPDATE `creature_text` SET `Sound`=60390 WHERE `CreatureID`=61418 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- It... it was pointless after all... This cannot be the way I fall...
UPDATE `creature_text` SET `Sound`=60389 WHERE `CreatureID`=61418 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Our nation stands strong! I did what was neccesary.
UPDATE `creature_text` SET `Sound`=60384 WHERE `CreatureID`=61419 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- This district is currently on lockdown!
UPDATE `creature_text` SET `Sound`=60385 WHERE `CreatureID`=61419 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Foolish interloper, you do not belong here...
UPDATE `creature_text` SET `Sound`=60382 WHERE `CreatureID`=61421 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Order must be maintained!
UPDATE `creature_text` SET `Sound`=60383 WHERE `CreatureID`=61421 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- I will not let Gilneas fall to madness, not while I...
UPDATE `creature_text` SET `Sound`=60391 WHERE `CreatureID`=61422 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- I hunt from the shadows, these streets have been cleared by my hand!
UPDATE `creature_text` SET `Sound`=60392 WHERE `CreatureID`=61422 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- This was not meant to be...
UPDATE `creature_text` SET `Sound`=60386 WHERE `CreatureID`=61423 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- I have served as Marshal throughout all of the orcish incursions. You 
UPDATE `creature_text` SET `Sound`=60387 WHERE `CreatureID`=61423 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- The brave defenders of this city... will not let you put it to ruin, o
UPDATE `creature_text` SET `Sound`=60592 WHERE `CreatureID`=62038 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- The destiny of our clan is set in stone, you can not change fate.
UPDATE `creature_text` SET `Sound`=60593 WHERE `CreatureID`=62038 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- Behold, the power of the elements!
UPDATE `creature_text` SET `Sound`=60594 WHERE `CreatureID`=62038 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- My legacy...
UPDATE `creature_text` SET `Sound`=60520 WHERE `CreatureID`=62067 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- You won't interrupt my plans...
UPDATE `creature_text` SET `Sound`=60521 WHERE `CreatureID`=62067 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- The brood will live on, my work will not end here!
UPDATE `creature_text` SET `Sound`=60522 WHERE `CreatureID`=62067 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- Pointless...
UPDATE `creature_text` SET `Sound`=60501 WHERE `CreatureID`=62068 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- Unidentified intruder detected.
UPDATE `creature_text` SET `Sound`=60502 WHERE `CreatureID`=62068 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- Execute destruction measure 13.
UPDATE `creature_text` SET `Sound`=60503 WHERE `CreatureID`=62068 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- Protocal failure...
UPDATE `creature_text` SET `Sound`=60523 WHERE `CreatureID`=62070 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- More Slaves? How fortunate for you to deliver yourself to me!
UPDATE `creature_text` SET `Sound`=60524 WHERE `CreatureID`=62070 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- Get into order, maggots!
UPDATE `creature_text` SET `Sound`=60525 WHERE `CreatureID`=62070 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- Overlord Blackheart begins to laugh maniacally.
UPDATE `creature_text` SET `Sound`=60492 WHERE `CreatureID`=62071 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- I have been tasked to keep our sacred flame, do not test me!
UPDATE `creature_text` SET `Sound`=60493 WHERE `CreatureID`=62071 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- You have no place here!
UPDATE `creature_text` SET `Sound`=60494 WHERE `CreatureID`=62071 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- My duty... Is failed...
UPDATE `creature_text` SET `Sound`=60512 WHERE `CreatureID`=62495 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- These halls be sacred, you shall be banished from them.
UPDATE `creature_text` SET `Sound`=60513 WHERE `CreatureID`=62495 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- I shall live forever!
UPDATE `creature_text` SET `Sound`=60514 WHERE `CreatureID`=62495 AND `GroupID`=53 AND `ID`=0 AND `Sound`=0; -- No! Once more I return to sand...
UPDATE `creature_text` SET `Sound`=60515 WHERE `CreatureID`=62496 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- I shall crush your bones..
UPDATE `creature_text` SET `Sound`=60516 WHERE `CreatureID`=62497 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- I be elusive... You cannot escape me!
UPDATE `creature_text` SET `Sound`=60517 WHERE `CreatureID`=62498 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- I am Razjal, champion of Zul'Farrak, who you be mon?
UPDATE `creature_text` SET `Sound`=60519 WHERE `CreatureID`=62498 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Be consumed by the sand!
UPDATE `creature_text` SET `Sound`=60518 WHERE `CreatureID`=62498 AND `GroupID`=3 AND `ID`=0 AND `Sound`=0; -- I am the only champion, not you, not anyone!
UPDATE `creature_text` SET `Sound`=60590 WHERE `CreatureID`=62547 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- More meat to devour!
UPDATE `creature_text` SET `Sound`=60591 WHERE `CreatureID`=62547 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- The hunger... never ends...
UPDATE `creature_text` SET `Sound`=60595 WHERE `CreatureID`=62548 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Let me tear your heart asunder!
UPDATE `creature_text` SET `Sound`=60596 WHERE `CreatureID`=62548 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Gul'dan...! Your legacy...
UPDATE `creature_text` SET `Sound`=60586 WHERE `CreatureID`=62549 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Yet again do the forces of darkness seek to lay claim to my throne. St
UPDATE `creature_text` SET `Sound`=60587 WHERE `CreatureID`=62549 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Olivert... Philmore... Old friends...
UPDATE `creature_text` SET `Sound`=60597 WHERE `CreatureID`=62550 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Step forth. Accept the cold embrace of death and drown in its bleaknes
UPDATE `creature_text` SET `Sound`=60599 WHERE `CreatureID`=62550 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- The waves... they beckon me...
UPDATE `creature_text` SET `Sound`=60598 WHERE `CreatureID`=62550 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Darkness shall come, and consume you all!
UPDATE `creature_text` SET `Sound`=60588 WHERE `CreatureID`=62551 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- The dark sea will swallow your souls!
UPDATE `creature_text` SET `Sound`=60589 WHERE `CreatureID`=62551 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- You know so little, whelps...
UPDATE `creature_text` SET `Sound`=60634 WHERE `CreatureID`=62552 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- I must kindly ask you to leave, the archives are not ready for public 
UPDATE `creature_text` SET `Sound`=60636 WHERE `CreatureID`=62552 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- These pages were mine to organize... Such great effort, gone to waste!
UPDATE `creature_text` SET `Sound`=60635 WHERE `CreatureID`=62552 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Behold, my signature attack! The great waves of Balor shall destroy yo
UPDATE `creature_text` SET `Sound`=60605 WHERE `CreatureID`=62652 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- You shall be brought under heel intruder...
UPDATE `creature_text` SET `Sound`=60607 WHERE `CreatureID`=62652 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- This cannot be! I was going to change the world!
UPDATE `creature_text` SET `Sound`=60606 WHERE `CreatureID`=62652 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- My will is unbreakable, you shall bend your knee.
UPDATE `creature_text` SET `Sound`=60608 WHERE `CreatureID`=62665 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- New toys, let's hope you will not break so easily...
UPDATE `creature_text` SET `Sound`=60610 WHERE `CreatureID`=62665 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Impossible... You... vile...
UPDATE `creature_text` SET `Sound`=60609 WHERE `CreatureID`=62665 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Share your darkest secrets with me!
UPDATE `creature_text` SET `Sound`=60600 WHERE `CreatureID`=62671 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- My master prepared me for this moment. Those ignorant to his truth wil
UPDATE `creature_text` SET `Sound`=60601 WHERE `CreatureID`=62671 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Your intrusion ends here!
UPDATE `creature_text` SET `Sound`=60602 WHERE `CreatureID`=62671 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Enough! The Bloodstone is ready; savor the last fleeting moments of yo
UPDATE `creature_text` SET `Sound`=60603 WHERE `CreatureID`=62671 AND `GroupID`=3 AND `ID`=0 AND `Sound`=0; -- Great Mergothid, lay your eyes upon this feast of souls!
UPDATE `creature_text` SET `Sound`=60621 WHERE `CreatureID`=62673 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Too soon, incessant weakling. Your pathetic soul will be the compensat
UPDATE `creature_text` SET `Sound`=60622 WHERE `CreatureID`=62673 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- More souls to feast upon!
UPDATE `creature_text` SET `Sound`=60623 WHERE `CreatureID`=62673 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- The nether, calls yet again!
UPDATE `creature_text` SET `Sound`=60663 WHERE `CreatureID`=62779 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- This canyon will make for excellent hunting!
UPDATE `creature_text` SET `Sound`=60664 WHERE `CreatureID`=62779 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- You shall be crushed!
UPDATE `creature_text` SET `Sound`=60665 WHERE `CreatureID`=62779 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- I travel to the great beyond...
UPDATE `creature_text` SET `Sound`=60669 WHERE `CreatureID`=62781 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- Our destiny has been foretold!
UPDATE `creature_text` SET `Sound`=60670 WHERE `CreatureID`=62781 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- I have seen the future, and it is your death!
UPDATE `creature_text` SET `Sound`=60671 WHERE `CreatureID`=62781 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- My sight, has left me!
UPDATE `creature_text` SET `Sound`=60676 WHERE `CreatureID`=62783 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- Behold the howling wind!
UPDATE `creature_text` SET `Sound`=60677 WHERE `CreatureID`=62783 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- We seek unity...
UPDATE `creature_text` SET `Sound`=60678 WHERE `CreatureID`=62783 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- Disperse...
UPDATE `creature_text` SET `Sound`=60666 WHERE `CreatureID`=62784 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- Be destroyed by my hands!
UPDATE `creature_text` SET `Sound`=60667 WHERE `CreatureID`=62784 AND `GroupID`=51 AND `ID`=0 AND `Sound`=0; -- Enough!
UPDATE `creature_text` SET `Sound`=60668 WHERE `CreatureID`=62784 AND `GroupID`=52 AND `ID`=0 AND `Sound`=0; -- This cannot... be...
UPDATE `creature_text` SET `Sound`=60711 WHERE `CreatureID`=63129 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- I have seen da future, and you aint in it!
UPDATE `creature_text` SET `Sound`=60706 WHERE `CreatureID`=63130 AND `GroupID`=0 AND `ID`=0 AND `Sound`=0; -- Embrace the cold...
UPDATE `creature_text` SET `Sound`=60707 WHERE `CreatureID`=63130 AND `GroupID`=1 AND `ID`=0 AND `Sound`=0; -- Let the chill overcome...
UPDATE `creature_text` SET `Sound`=60708 WHERE `CreatureID`=63130 AND `GroupID`=2 AND `ID`=0 AND `Sound`=0; -- Destruction...
UPDATE `creature_text` SET `Sound`=60710 WHERE `CreatureID`=63131 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- The Frostmane be da strongest, be da fiercest! Dis be our home, you th
UPDATE `creature_text` SET `Sound`=60709 WHERE `CreatureID`=63132 AND `GroupID`=50 AND `ID`=0 AND `Sound`=0; -- Tan'sha, kill them all!
UPDATE `creature_text` SET `Sound`=30268 WHERE `CreatureID`=92107 AND `GroupID`=91 AND `ID`=0 AND `Sound`=0; -- I am the leader of the tribes, me! The Groveweald shall destroy everyo
UPDATE `creature_text` SET `Sound`=30270 WHERE `CreatureID`=92107 AND `GroupID`=92 AND `ID`=0 AND `Sound`=0; -- I.. I can see clearly now.. The madness... It's... Over...
UPDATE `creature_text` SET `Sound`=30256 WHERE `CreatureID`=92109 AND `GroupID`=91 AND `ID`=0 AND `Sound`=0; -- What? Who..Who are you? They wouldn't send you! Ancients, to my side!
UPDATE `creature_text` SET `Sound`=30258 WHERE `CreatureID`=92109 AND `GroupID`=92 AND `ID`=0 AND `Sound`=0; -- We must.. Stop.. The shadow...
UPDATE `creature_text` SET `Sound`=30271 WHERE `CreatureID`=92110 AND `GroupID`=91 AND `ID`=0 AND `Sound`=0; -- Do you think you can withstand the might of the Burning Legion?
UPDATE `creature_text` SET `Sound`=30273 WHERE `CreatureID`=92110 AND `GroupID`=92 AND `ID`=0 AND `Sound`=0; -- My death.. Means little in the grand scheme, mortals... Drink down you
UPDATE `creature_text` SET `Sound`=30252 WHERE `CreatureID`=92111 AND `GroupID`=91 AND `ID`=0 AND `Sound`=0; -- We will serve at the Master's will!
UPDATE `creature_text` SET `Sound`=30253 WHERE `CreatureID`=92111 AND `GroupID`=92 AND `ID`=0 AND `Sound`=0; -- You think.. This.... Is the end?
