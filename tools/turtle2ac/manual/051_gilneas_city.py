"""Gilneas City (map 815) - Turtle's dungeon C++ re-expressed as SmartAI.

Source: tortoise-wow src/scripts/dungeons/gilneas_city/*.cpp
- Regent-Lady Celia Harlow and Regent-Lord Mortimer Harlow: caster / paladin spells; below 50% health they take
  their dragonkin form and only use Blast Wave.
- Genn Greymane: Drain Life, Mortal Strike, Curse of Agony; at 50% one line and a Fear.
- Greymane Knight / Greymane Noble: their two spells each.
- The instance script's yells when five bosses are pulled and when they die (Turtle plays custom voice files the
  3.3.5 client does not have: text only). Turtle's rain while inside is left out.
Timers are Turtle's (first cast, then repeat, in ms). Run by build.py with `S` and `ctx`.
"""
A = S.raw
CELIA, MORTIMER, GENN, KNIGHT, NOBLE = 61263, 61264, 61418, 61365, 61390
HOLTZ, SUTHERLAND, BLACKCOWL, GREYSTONE = 61419, 61421, 61422, 61423
S.names.update({CELIA: 'Regent-Lady Celia Harlow', MORTIMER: 'Regent-Lord Mortimer Harlow', GENN: 'Genn Greymane',
                KNIGHT: 'Greymane Knight', NOBLE: 'Greymane Noble', HOLTZ: 'Matthias Holtz', SUTHERLAND: 'Judge Sutherland',
                BLACKCOWL: 'Dustivan Blackcowl', GREYSTONE: 'Marshal Magnus Greystone'})
P1, P2 = 1, 2                         # event phase masks: 1 = normal form, 2 = dragonkin form


def two_forms(entry, dragon_model):
    """phase 1 from the pull; below 50% health: dragonkin model + phase 2; reset: own model back"""
    S.on(entry, 'aggro', A(22, [1], 'self', note='Set Phase 1'))
    S.on(entry, 'hp', A(3, [0, dragon_model], 'self', note='Dragonkin form'), A(22, [2], 'self', note='Set Phase 2'),
         ep=(0, 50, 0, 0), once=True)
    S.on(entry, 'evade', A(3, [0, 0], 'self', note='Own form back'), A(22, [0], 'self', note='Set Phase 0'))


def yells(entry, aggro, death):
    for g, t in ((0, aggro), (1, death)):
        if isinstance(t, str):
            S.ltext(entry, g, t)
        else:
            S.btext(entry, g, t, 'yell')
    S.on(entry, 'aggro', S.talk(0))
    S.on(entry, 'death', S.talk(1))


# Regent-Lady Celia Harlow
yells(CELIA, "Mortimer, it would appear we have someone here to interrupt our plans!", "All of our progress, our influence... What a pointless end...")
two_forms(CELIA, 8249)
S.ic(CELIA, 'random', 25309, (8000, 8000), (8000, 8000), phase=P1)       # Immolate
S.ic(CELIA, 'random', 2767, (11000, 11000), (11000, 11000), phase=P1)    # Shadow Word: Pain
S.ic(CELIA, 'random', 11671, (6000, 6000), (6000, 6000), phase=P1)       # Corruption
S.ic(CELIA, 'random', 13021, (25000, 25000), (25000, 25000), phase=P2)   # Blast Wave

# Regent-Lord Mortimer Harlow
yells(MORTIMER, 30138, 30139)
two_forms(MORTIMER, 143)
S.ic(MORTIMER, 'random', 2495, (9000, 9000), (9000, 9000), phase=P1)     # Holy Strike
S.ic(MORTIMER, 'self', 20924, (12000, 12000), (12000, 12000), phase=P1)  # Consecration
S.ic(MORTIMER, 'random', 13021, (25000, 25000), (25000, 25000), phase=P2)

# Genn Greymane
yells(GENN, "My family has held power in Gilneas for countless generations. You will not change fate.",
      "It... it was pointless after all... This cannot be the way I fall...")
S.btext(GENN, 2, 81055, 'yell')
S.ic(GENN, 'victim', 17620, (4000, 4000), (20000, 25000))                # Drain Life
S.ic(GENN, 'victim', 21551, (2000, 2000), (17000, 20000))                # Mortal Strike
S.ic(GENN, 'random', 11711, (1000, 1000), (10000, 15000))                # Curse of Agony
fear = S.cast(22678, 'random')
S.on(GENN, 'hp', S.talk(2), *([fear] if fear else []), ep=(0, 50, 0, 0), once=True)

# Greymane Knight / Noble
S.ic(KNIGHT, 'victim', 18368, (1000, 1000), (10000, 10000))              # Strike
S.ic(KNIGHT, 'victim', 853, (12000, 20000), (12000, 20000))              # Hammer of Justice
S.ic(NOBLE, 'victim', 10945, (2000, 2000), (9000, 9000))                 # Mind Blast
S.ic(NOBLE, 'random', 17312, (10000, 18000), (10000, 18000))             # Mind Flay

# the instance script's boss yells
yells(HOLTZ, "This district is currently on lockdown!", "Foolish interloper, you do not belong here...")
yells(SUTHERLAND, "Order must be maintained!", "I will not let Gilneas fall to madness, not while I...")
yells(BLACKCOWL, "I hunt from the shadows, these streets have been cleared by my hand!", "This was not meant to be...")
yells(GREYSTONE, "I have served as Marshal throughout all of the orcish incursions. You will not put an end to Gilneas.",
      "The brave defenders of this city... will not let you put it to ruin, outsider!")

SQL = S.sql()
