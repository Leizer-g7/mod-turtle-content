"""Gillijim's Isle - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "The Maul'ogg Crisis I" (40264): Lord Cruk'Zogg answers Haz'gorg's message - credit.
- "The Maul'ogg Crisis VIII" (40271): Insom'ni's ritual hands over the potion; IX (40272): Lord Cruk'Zogg drinks it.
- "The Maul'ogg Crisis VI" (40269): Turtle's Gorilla Ligament drop on the Un'Goro gorillas (3.3.5 creatures).
- Insom'ni's Lapidis Isle quests, 'Moonshine' Marty's recipe (Southsea Reserve) and the Crate in High Elven Wrecks
  (Krilana's Magnificent Quest): the quests themselves are built by 053_lapidis_isle.
Flavour: Blazno Blastpipe when "The Blazno Touch" (40190) is handed in; Captain Saltbeard's line when pulled.
Left out with their quests (see the zone file): Garfield Sparkblast (the Bloodsail chain).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
GO_NO_SELECT = 0x10
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
CRUKZOGG, BLAZNO, SALTBEARD = 92180, 92191, 92144
S.names.update({CRUKZOGG: "Lord Cruk'Zogg", BLAZNO: 'Blazno Blastpipe', SALTBEARD: 'Captain Saltbeard'})

# ---- Lord Cruk'Zogg: The Maul'ogg Crisis I (40264) and IX (40272)
S.btext(CRUKZOGG, 0, 66683)
S.btext(CRUKZOGG, 1, 67027)
S.btext(CRUKZOGG, 2, 66385)
S.btext(CRUKZOGG, 3, 66475)
POTION = 60345
C0 = OFF + 92180
S.gossip(C0, 92180, [(0, 66681, 0, 0, [(47, 40264, IN_PROGRESS, 0)]),
                     (1, 66682, 0, 0, [(47, 40272, IN_PROGRESS, 0), (2, POTION, 1, 0)])])
for o in (0, 1):
    S.row(CRUKZOGG, 0, 62, [C0, o], A(72, [], 'invoker', note='Close Gossip'))
S.row(CRUKZOGG, 0, 62, [C0, 0], A(80, [CRUKZOGG * 100 + 1, 0, 0], 'self', note='Answer (action list)'))
S.row(CRUKZOGG, 0, 62, [C0, 1], A(57, [POTION, 1], 'invoker', note='Take the potion'))
S.row(CRUKZOGG, 0, 62, [C0, 1], A(80, [CRUKZOGG * 100 + 2, 0, 0], 'self', note='Potion (action list)'))
S.actionlist(CRUKZOGG * 100 + 2, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, A(5, [7], 'self', note='Emote Eat (drinks)')),
    (3000, S.talk(2)), (0, A(5, [1], 'self', note='Emote Talk')),
    (8000, S.talk(3)), (0, A(5, [1], 'self', note='Emote Talk')),
    (2000, A(33, [60339], 'invoker', note='Quest Credit 60339')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], "Lord Cruk'Zogg")
S.actionlist(CRUKZOGG * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, S.talk(0)), (0, A(5, [11], 'self', note='Emote Laugh')),
    (3000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(33, [60337], 'invoker', note='Quest Credit 60337')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], "Lord Cruk'Zogg")
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={C0}, `npcflag`=`npcflag`|1 WHERE `entry`={CRUKZOGG};")

# ---- Blazno Blastpipe: The Blazno Touch (40190) handed in
S.btext(BLAZNO, 0, 66665)
S.btext(BLAZNO, 1, 66666)
S.on(BLAZNO, 'reward_quest', A(80, [BLAZNO * 100 + 1, 0, 0], 'self', note='Experiment (action list)'), ep=[40190])
S.actionlist(BLAZNO * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (11000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], 'Blazno Blastpipe')

# ---- Captain Saltbeard: his line when pulled
S.btext(SALTBEARD, 0, 66400)
S.on(SALTBEARD, 'aggro', S.talk(0))

# ---- Insom'ni (Kazon Island): his Lapidis Isle quests (built by 053_lapidis_isle)
#   "The Hermit" (40210): his tale, then the credit. "The Tower of Lapidis IX" (40171): he attunes the key (item 60244).
#   "Uncovering Evil" (40214): on accepting (or "We must banish this evil together." if it failed), he walks to the centre of
#   Kazon Island and calls up Fearoth (60499), the dark presence to slay.
INSOMNI, FEAROTH = 60446, 60499
S.names.update({INSOMNI: "Insom'ni", 2010878: 'Crate in High Elven Wrecks'})
for g, b in enumerate((66405, 66406, 66407, 66672, 66409, 66410, 66411)):
    S.btext(INSOMNI, g, b)
S.ltext(INSOMNI, 7, 'Come, $n. It is time to banish this evil.', 'say')
I0 = OFF + 60446
S.gossip(I0, 60446, [(0, 66670, 0, 0, [(47, 40210, IN_PROGRESS, 0)]),
                     (1, 66671, 0, 0, [(47, 40214, IN_PROGRESS, 0)])])
for o in (0, 1):
    S.row(INSOMNI, 0, 62, [I0, o], A(72, [], 'invoker', note='Close Gossip'))
S.row(INSOMNI, 0, 62, [I0, 0], A(80, [INSOMNI * 100 + 1, 0, 0], 'self', note='The tale (action list)'))
S.row(INSOMNI, 0, 62, [I0, 1], A(80, [INSOMNI * 100 + 3, 0, 0], 'self', note='Banish the evil (action list)'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={I0}, `npcflag`=`npcflag`|1 WHERE `entry`={INSOMNI};")
S.actionlist(INSOMNI * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (20000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (20000, S.talk(2)), (0, A(5, [1], 'self', note='Emote Talk')),
    (15000, A(33, [60334], 'invoker', note='Quest Credit 60334')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], "Insom'ni")
S.on(INSOMNI, 'accepted_quest', A(80, [INSOMNI * 100 + 2, 0, 0], 'self', note='Attune the key (action list)'), ep=[40171])
S.actionlist(INSOMNI * 100 + 2, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.cast(13236, 'self')),
    (18000, A(5, [273], 'self', note='Emote Yes')),
    (2000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(56, [60244, 1], 'invoker', note='Give the attuned key')),
    (0, S.talk(3)), (0, A(5, [1], 'self', note='Emote Talk'))], "Insom'ni")
S.on(INSOMNI, 'accepted_quest', A(80, [INSOMNI * 100 + 3, 0, 0], 'self', note='Banish the evil (action list)'), ep=[40214])
#   "The Maul'ogg Crisis VIII" (40271): the same ritual, then the potion of strength (60345)
S.btext(INSOMNI, 8, 66673)
S.on(INSOMNI, 'accepted_quest', A(80, [INSOMNI * 100 + 4, 0, 0], 'self', note='The potion (action list)'), ep=[40271])
S.actionlist(INSOMNI * 100 + 4, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.cast(13236, 'self')),
    (18000, A(5, [273], 'self', note='Emote Yes')),
    (2000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(56, [60345, 1], 'invoker', note='Give the potion')),
    (0, S.talk(8)), (0, A(5, [1], 'self', note='Emote Talk'))], "Insom'ni")
S.actionlist(INSOMNI * 100 + 3, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (1000, A(59, [0], 'self', note='Walk')),
    (0, A(69, [0, 0, 0], 'pos', xyz=(-12864.27, 2809.63, -6.85, 0), note='Move')),
    (0, A(1, [7, 0, 0], 'invoker', note='Say Line 7')),
    (38000, S.talk(4)), (0, A(5, [1], 'self', note='Emote Talk')),
    (3000, A(69, [0, 0, 0], 'pos', xyz=(-12865.99, 2821.96, -0.82, 0), note='Move')),
    (5000, S.talk(5)), (0, A(5, [1], 'self', note='Emote Talk')),
    (1000, A(69, [0, 0, 0], 'pos', xyz=(-12864.54, 2908.59, 10.24, 0), note='Move')),
    (30000, S.talk(6)), (0, A(5, [1], 'self', note='Emote Talk')),
    (4000, S.cast(13236, 'self')),
    (10000, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(12, [FEAROTH, 6, 0], 'pos', xyz=(-12853.94, 2915.04, 10.81, 3.83), note='Summon Fearoth (despawns as a corpse)'))], "Insom'ni")

# ---- Crate in High Elven Wrecks: Krilana's Magnificent Quest (40370, Lapidis Isle) - the Mournful Apparition appears
MOURNFUL, CRATE = 60658, 2010878
K0 = OFF + 30017
S.gossip(K0, 30017, [(0, 66716, 0, 0, [(47, 40370, IN_PROGRESS, 0), (2, 60517, 1, 1)])])
S.row(CRATE, 1, 62, [K0, 0], A(12, [MOURNFUL, 3, 120000], 'self', note='Summon the Mournful Apparition'))
S.row(CRATE, 1, 62, [K0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(CRATE, 1, 62, [K0, 0], A(105, [GO_NO_SELECT], 'self', note='Not usable while it is out'))
S.row(CRATE, 1, 62, [K0, 0], A(80, [CRATE * 100 + 1, 0, 0], 'self', note='Usable again later'))
S.actionlist(CRATE * 100 + 1, [(120000, A(106, [GO_NO_SELECT], 'self', note='Usable again'))], 'Crate in High Elven Wrecks')
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data3`={K0}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={CRATE};")

# ---- 'Moonshine' Marty: the Southsea Reserve recipe (40148, a Lapidis Isle quest) - vendor menu + the threat
MARTY = 92137
S.names[MARTY] = "'Moonshine' Marty"
S.btext(MARTY, 0, 66653)
MM = OFF + 92137
S.gossip(MM, 92137, [(0, 66651, 1, 0, [], (3, 128)),
                     (1, 66652, 0, 0, [(47, 40148, IN_PROGRESS, 0), (2, 60217, 1, 1)])])
S.row(MARTY, 0, 62, [MM, 1], A(56, [60217, 1], 'invoker', note='Give the recipe'))
S.row(MARTY, 0, 62, [MM, 1], A(1, [0, 0, 0], 'invoker', note='Say Line 0'))
S.row(MARTY, 0, 62, [MM, 1], A(5, [1], 'self', note='Emote Talk'))
S.row(MARTY, 0, 62, [MM, 1], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={MM}, `npcflag`=`npcflag`|1 WHERE `entry`={MARTY};")

# ---- The Maul'ogg Crisis VI (40269): Gorilla Ligament, Turtle's drop on the Un'Goro gorillas (3.3.5 creatures)
STOCK_DROPS = S.stock_quest_drops([60343])

SQL = S.sql()
