"""Stormwrought Ruins - the bosses and the secret door, re-expressed as SmartAI.

Source: tortoise-wow src/scripts/dungeons/stormwrought_ruins/*.cpp (Turtle's C++ scripts).
Timers are Turtle's (first cast min/max, then repeat min/max, in ms). Turtle-only spells go through
config.json spell_substitutions (stand-ins); the build report lists every substitution.
Run by build.py: `S` (lib.smartgen.Smart) and `ctx` are provided; the result is the module text SQL.
"""
from lib.smartgen import EV
A = S.raw
NA = 0x2 | 0x2000000          # non attackable + not selectable

names = {62547: 'Dagar the Glutton', 62548: 'Oronok Torn-Heart', 62549: 'Duke Balor the IV', 62550: 'Deathlord Tidebane',
         62551: 'Chieftain Stormsong', 62552: 'Librarian Theodorus', 62652: 'Subjugator Halthas Shadecrest',
         62661: 'Eldermaw the Primordial', 62664: 'Mycellakos', 62665: 'Lady Drazare', 62671: "Ighal'for", 62672: 'Rifttorn Nether Imp',
         62673: 'Mergothid', 62674: 'Eldermaw Crocolisk', 62675: 'Growth of Mycellakos', 62742: 'Enraged Sea Elemental'}
S.names.update(names)


def aggro_death(entry, aggro, death):
    S.text(entry, 0, aggro)
    S.text(entry, 1, death)
    S.on(entry, 'aggro', S.talk(0))
    S.on(entry, 'death', S.talk(1))


# Dagar the Glutton
aggro_death(62547, -1999962, -1999963)
S.ic(62547, 'victim', 3393, (6000, 8000), (12000, 16000))                 # Consume Flesh

# Oronok Torn-Heart
aggro_death(62548, -1999969, -1999970)
S.ic(62548, 'victim', 10101, (8000, 12000), (16000, 22000))               # Knock Away
S.ic(62548, 'victim', 11433, (1000, 1000), (22000, 30000))                # Death and Decay
S.ic(62548, 'random', 11660, (5000, 8000), (7000, 10000))                 # Shadow Bolt

# Duke Balor the IV
aggro_death(62549, -1999964, -1999965)
S.ic(62549, 'victim', 47386, (5000, 5000), (25000, 30000))                # Mind Flay (Turtle id -> stand-in)
S.ic(62549, 'self', 13704, (15000, 20000), (15000, 20000))                # Psychic Scream
S.ic(62549, 'self', 7713, (10000, 15000), (10000, 15000))                 # Wailing Dead
S.ic(62549, 'victim', 22574, (7000, 10000), (16000, 22000))               # Dark Strike

# Deathlord Tidebane
S.text(62550, 0, -1999973)
S.text(62550, 1, -1999975)
S.text(62550, 2, -1999974)
S.on(62550, 'aggro', S.talk(0))
S.on(62550, 'death', S.talk(1))
S.ic(62550, 'random', 11990, (9000, 13000), (18000, 24000))               # Rain of Fire
S.ic(62550, 'random', 18270, (4000, 7000), (10000, 14000))                # Dark Plague
S.ic(62550, 'self', 17631, (16000, 22000), (22000, 30000), then=[S.talk(2)])   # Wail of Souls + line

# Chieftain Stormsong
aggro_death(62551, -1999971, -1999972)
S.ic(62551, 'victim', 20299, (5000, 8000), (11000, 15000))                # Forked Lightning
S.ic(62551, 'random', 16497, (25000, 30000), (25000, 30000))              # Stun Bomb
S.ic(62551, 'victim', 52422, (12000, 16000), (14000, 20000))              # Lightning Strike (stand-in)
S.on(62551, 'hp', A(14, [0, 100], 'self', note='Reset Threat (Turtle: at 50%)'), ep=(0, 50, 0, 0), once=True)

# Librarian Theodorus
S.text(62552, 0, -1999966)
S.text(62552, 1, -1999968)
S.text(62552, 2, -1999967)
S.on(62552, 'aggro', S.talk(0))
S.on(62552, 'death', S.talk(1))
S.ic(62552, 'victim', 10159, (1000, 1000), (15000, 22000))                # Cone of Cold
S.ic(62552, 'random', 8406, (4000, 6000), (6000, 9000))                   # Frostbolt
S.ic(62552, 'random', 30093, (10000, 14000), (16000, 22000))              # Blizzard
S.on(62552, 'hp', S.talk(2), S.summon(62742, kind=2, duration=120000), ep=(0, 50, 0, 0), once=True)   # Enraged Sea Elemental
S.on(62742, 'summoned', A(38, [0], 'self', note='Set In Combat With Zone'))

# Subjugator Halthas Shadecrest
S.text(62652, 0, -1999976)
S.text(62652, 1, -1999978)
S.text(62652, 2, -1999977)
S.on(62652, 'aggro', S.talk(0))
S.on(62652, 'death', S.talk(1))
S.ic(62652, 'victim', 15859, (12000, 16000), (26000, 34000), then=[S.talk(2)])   # Dominate Mind + line
S.ic(62652, 'victim', 11829, (0, 0), (12000, 16000))                      # Flamestrike
S.ic(62652, 'self', 27641, (18000, 24000), (24000, 32000))                # Fear

# Eldermaw the Primordial
S.ic(62661, 'random', 44041, (4000, 6000), (10000, 12000))                # Tail Slap (stand-in)
S.on(62661, 'hp', S.cast(44042, 'self', triggered=True), S.summon(62674, kind=2, duration=60000),
     S.summon(62674, kind=2, duration=60000), ep=(0, 50, 0, 0), once=True)   # Primordial Regeneration + 2 crocolisks
S.on(62674, 'summoned', A(38, [0], 'self', note='Set In Combat With Zone'))

# Mycellakos: every 15-20 s a Volatile Fungus appears at his feet and bursts 3 s later into gas + 2 Growths
S.actionlist(6266400, [
    (0, S.summon_go(300420, 4)),
    (3000, S.cast(44048, 'self', triggered=True)),
    (0, S.summon(62675, kind=2, duration=60000)),
    (0, S.summon(62675, kind=2, duration=60000)),
], 'Mycellakos - Volatile Fungus')
S.row(62664, 0, 0, [8000, 8000, 15000, 20000], A(80, [6266400, 0, 1], 'self', note='Volatile Fungus (action list)'))
S.ic(62664, 'self', 44050, (25000, 30000), (25000, 30000))                # Decaying Mold (stand-in)
S.on(62675, 'summoned', A(38, [0], 'self', note='Set In Combat With Zone'))
S.extra_sql.append("DELETE FROM `gameobject_template` WHERE `entry`=300420;\n"
                   "INSERT INTO `gameobject_template` (`entry`,`type`,`displayId`,`name`,`IconName`,`castBarCaption`,`unk1`,`size`,`AIName`,`ScriptName`,`VerifiedBuild`) "
                   "VALUES (300420, 5, 6432, 'Volatile Fungus', '', '', '', 1.5, '', '', 0);")

# Lady Drazare
S.text(62665, 0, -1999979)
S.text(62665, 1, -1999981)
S.text(62665, 2, -1999980)
S.on(62665, 'aggro', S.talk(0))
S.on(62665, 'death', S.talk(1))
seduce = S.cast(44051, 'random')
seduce.tp = [0, 1]                                                       # players only
S.row(62665, 0, 0, [19000, 20000, 39000, 58000], seduce)
S.row(62665, 0, 0, [19000, 20000, 39000, 58000], S.talk(2))
S.ic(62665, 'self', 44053, (12000, 24000), (12000, 24000))                # Drazare's Embrace (stand-in: shadow volley)

# Ighal'for (phase 1: fight, 2: channels at the Bloodstone and opens the rift, 3: fights again next to Mergothid)
ALTAR = (-5479.79, -3968.8, 259.671)
S.text(62671, 0, -1999982)
S.text(62671, 1, -1999983)
S.text(62671, 2, -1999984)
S.text(62671, 3, -1999985)
S.row(62671, 0, 10, [0, 80, 0, 0, 1], S.talk(0), flags=1)                 # sees a player: temple line (once)
S.on(62671, 'aggro', S.talk(1), A(22, [1], 'self', note='Set Phase 1'))
S.ic(62671, 'random', 6789, (12000, 12000), (22000, 22000), phase=1 | 4)   # Death Coil
S.ic(62671, 'random', 8423, (7000, 7000), (24000, 24000), phase=1 | 4)    # Flamestrike
S.ic(62671, 'random', 11712, (18000, 18000), (26000, 26000), phase=1 | 4)  # Curse of Agony
S.on(62671, 'hp', A(22, [2], 'self', note='Set Phase 2'), A(80, [6267100, 0, 2], 'self', note='Channel (action list)'),
     ep=(0, 25, 0, 0), phase=1, once=True)
imps = []
for dx, dy in ((1.5, 0.0), (-0.75, 1.3), (-0.75, -1.3)):
    imps.append((0, S.summon(62672, ALTAR[0] + dx, ALTAR[1] + dy, ALTAR[2], kind=2, duration=120000)))
S.actionlist(6267100, [
    (0, S.talk(2)),
    (0, A(18, [NA], 'self', note='Set Unit Flags (not attackable)')),
    (0, A(8, [0], 'self', note='Set Passive')),
    (0, A(21, [0], 'self', note='Stop Combat Movement')),
    (0, A(69, [0], 'pos', xyz=ctx['home'](62671), note='Move To Home')),
    (2000, S.cast(8734, 'self', triggered=True)),                         # Blackfathom Channeling at the Bloodstone
    (3000, None)] + [(0, a) for _, a in imps] +
    [(15000, None)] + [(0, a) for _, a in imps] +
    [(15000, None)] + [(0, a) for _, a in imps] +
    [(3000, S.talk(3)),
     (2000, S.summon(62673, *ALTAR, kind=7, duration=0)),
     (8000, A(28, [8734], 'self', note='Remove Channeling')),
     (0, A(19, [NA], 'self', note='Remove Unit Flags')),
     (0, A(8, [2], 'self', note='Set Aggressive')),
     (0, A(21, [1], 'self', note='Allow Combat Movement')),
     (0, A(22, [3], 'self', note='Set Phase 3')),
     (0, A(45, [1, 1], 'closest_creature', tp=[62673, 100, 0], note='Release Mergothid'))],
    "Ighal'for - Channel")
S.on(62671, 'evade', A(19, [NA], 'self', note='Remove Unit Flags'), A(8, [2], 'self', note='Set Aggressive'),
     A(21, [1], 'self', note='Allow Combat Movement'), A(41, [0], 'creature_range', tp=[62672, 0, 200], note='Despawn Imps'),
     A(41, [0], 'creature_range', tp=[62673, 0, 200], note='Despawn Mergothid'))
S.on(62671, 'death', A(41, [0], 'creature_range', tp=[62672, 0, 200], note='Despawn Imps'))
S.on(62672, 'summoned', A(38, [0], 'self', note='Set In Combat With Zone'))

# Mergothid
S.text(62673, 0, -1999986)
S.text(62673, 1, -1999987)
S.text(62673, 2, -1999988)
S.on(62673, 'summoned', A(18, [NA], 'self', note='Set Unit Flags (not attackable)'), A(8, [0], 'self', note='Set Passive'))
S.on(62673, 'data', S.talk(0), A(19, [NA], 'self', note='Remove Unit Flags'), A(8, [2], 'self', note='Set Aggressive'),
     A(38, [0], 'self', note='Set In Combat With Zone'), ep=(1, 1, 0, 0))
S.on(62673, 'hp', S.talk(1), ep=(0, 50, 0, 0), once=True)
S.on(62673, 'death', S.talk(2))

# Secret door: the 4 Chamber Levers each add 1 to the portcullis' counter; at 4 it opens
DOOR = ctx['gguid'](5025428)
S.names[-DOOR] = 'Secret Portcullis'
for tw_guid in (5025429, 5025430, 5025431, 5025432):
    g = ctx['gguid'](tw_guid)
    S.names[-g] = 'Chamber Lever'
    S.row(-g, 1, EV['hello'], [0], A(63, [1, 1, 0], 'go_guid', tp=[DOOR, 2006138], note='Add 1 to the portcullis counter'), flags=1)
S.row(-DOOR, 1, EV['counter'], [1, 4], A(9, [], 'self', note='Open'))
S.extra_sql.append(f"UPDATE `gameobject_template` SET `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry` IN (2020236, 2006138);")

SQL = S.sql()
