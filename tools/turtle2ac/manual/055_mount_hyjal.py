"""Mount Hyjal - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp and the Into the Dream gossip
script 41396 / generic script 4139602 in Turtle's database) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "The Horn of Binding" (40876): Loremaster Taerlon lends the Bracing of Nature.
- "The Runestone Ritual" (40985): Buthok Cloudhorn's ritual, then the credit.
- "Shadowed Spectre" (41339): the Dissipating Spectre's two-step gossip gives the credit.
- "Into the Dream IV" (40960): Itharius (3.3.5 NPC, Swamp of Sorrows) hands over the four items when it is accepted.
- "Into the Dream V" (40961): Ralathius's ritual - three Nightmare Apparitions to kill, then Ysera, Ursoc and Goldrinn
  appear and talk, then the credit (all players near Ralathius get it, as on Turtle where the event credited the group).
- Turtle's quest drops on 3.3.5 creatures (Moontouched Amulet, Slumberer's Shard, Binding Fragment, Overloaded Arcane Prism,
  the Rods of 'Ere and 'Lex, Arcane Essence, Head of Alzzin the Wildshaper, Imbued Sludge).
Travel: the Runestones of Nordrassil and Cenarius carry players who finished "The Runestone Scepter" (40990) to each other.
Flavour: Ralathius's Ysera scene when "Into the Dream VI" (40962) is handed in, Arch Druid Dreamwind's line for "Lord Xanvarak".
Gossip menus are the module's own (Turtle text id + 9,000,000), except Ralathius's (the build's menu 41396, option 1).
Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
RALATHIUS, TAERLON, DREAMWIND, BUTHOK, SPECTRE, ITHARIUS = 61326, 61497, 61512, 61561, 61988, 5353
APPARITION, YSERA, URSOC, GOLDRINN = 61544, 61545, 61546, 61547
S.names.update({RALATHIUS: 'Ralathius', TAERLON: 'Loremaster Taerlon', DREAMWIND: 'Arch Druid Dreamwind', BUTHOK: 'Buthok Cloudhorn',
                SPECTRE: 'Dissipating Spectre', ITHARIUS: 'Itharius', APPARITION: 'Nightmare Apparition', YSERA: 'Ysera',
                URSOC: 'Ursoc', GOLDRINN: 'Goldrinn'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these"""
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def by(entry, group, rng=40):
    """another creature nearby says one of its lines"""
    return A(1, [group, 0, 0], 'closest_creature', tp=[entry, rng, 0], note=f'{S.names[entry]}: Say Line {group}')


# ---- Loremaster Taerlon: The Horn of Binding (40876) - he lends the Bracing of Nature
S.btext(TAERLON, 0, 66627)
T0 = OFF + 61497
S.gossip(T0, npc_text(61497), [(0, 66626, 0, 0, [(47, 40876, IN_PROGRESS, 0), (2, 61415, 1, 1)])])
S.row(TAERLON, 0, 62, [T0, 0], A(56, [61415, 1], 'invoker', note='Give the Bracing of Nature'))
S.row(TAERLON, 0, 62, [T0, 0], S.talk(0))
S.row(TAERLON, 0, 62, [T0, 0], A(5, [1], 'self', note='Emote Talk'))
S.row(TAERLON, 0, 62, [T0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={T0}, `npcflag`=`npcflag`|1 WHERE `entry`={TAERLON};")

# ---- Buthok Cloudhorn: The Runestone Ritual (40985)
S.btext(BUTHOK, 0, 66612)
S.on(BUTHOK, 'accepted_quest', A(80, [BUTHOK * 100 + 1, 0, 0], 'self', note='Ritual (action list)'), ep=[40985])
S.actionlist(BUTHOK * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.cast(13236, 'self')),
    (3000, S.talk(0)),
    (6500, A(5, [273], 'self', note='Emote Yes')), (0, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (500, A(33, [60048], 'invoker', note='Quest Credit 60048')),
    (0, A(92, [], 'self', note='Stop casting'))], 'Buthok Cloudhorn')

# ---- Dissipating Spectre: Shadowed Spectre (41339) - inspect it, resist, credit
D1, D2 = OFF + 61988, OFF + 30221
S.gossip(D2, npc_text(30221), [(0, 30222, 0, 0, [(47, 41339, IN_PROGRESS, 0)])])
S.gossip(D1, npc_text(61988), [(0, 30220, 0, D2, [(47, 41339, IN_PROGRESS, 0)])])
S.row(SPECTRE, 0, 62, [D2, 0], A(33, [60054], 'invoker', note='Quest Credit 60054'))
S.row(SPECTRE, 0, 62, [D2, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={D1}, `npcflag`=`npcflag`|1 WHERE `entry`={SPECTRE};")

# ---- Arch Druid Dreamwind: Lord Xanvarak (41020) handed in
S.btext(DREAMWIND, 0, 66617)
S.on(DREAMWIND, 'reward_quest', S.talk(0), A(5, [1], 'self', note='Emote Talk'), ep=[41020])

# ---- Itharius (3.3.5 NPC): Into the Dream IV (40960) accepted - the four items
S.mark_stock(ITHARIUS)
for it in (61557, 61558, 61559, 61560):
    S.on(ITHARIUS, 'accepted_quest', A(56, [it, 1], 'invoker', note=f'Give item {it}'), ep=[40960])

# ---- Ralathius: Into the Dream VI (40962) handed in - Ysera appears
S.btext(RALATHIUS, 0, 66608)
S.btext(YSERA, 0, 66609)
S.btext(YSERA, 1, 66610)
S.on(RALATHIUS, 'reward_quest', A(80, [RALATHIUS * 100 + 1, 0, 0], 'self', note='Ysera scene (action list)'), ep=[40962])
S.actionlist(RALATHIUS * 100 + 1, [
    (0, S.cast(23017, 'self')),                                   # Arcane Channeling
    (3000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (2000, A(12, [YSERA, 1, 9000, 0], 'pos', xyz=(5527.01, -3700.22, 1595.52, 0.28), note='Summon Ysera (9 s)')),
    (1000, by(YSERA, 0)),
    (3000, by(YSERA, 1)),
    (3000, S.cast(24171, 'self'))], 'Ralathius')

# ---- Ralathius: Into the Dream V (40961) - "I'm ready. Start the ritual." (the build's menu 41396, option 1)
for g, b in enumerate((65014, 65015, 65016, 65017, 65019, 65021, 65029), start=1):
    S.btext(RALATHIUS, g, b)
S.btext(RALATHIUS, 8, 65030, chat='emote')
for g, b in enumerate((65018, 65020, 65022, 65023, 65024, 65025, 65026, 65028), start=2):
    S.btext(YSERA, g, b)
S.btext(URSOC, 0, 65027)
S.row(RALATHIUS, 0, 62, [41396, 1], A(72, [], 'invoker', note='Close Gossip'))
S.row(RALATHIUS, 0, 62, [41396, 1], A(80, [RALATHIUS * 100 + 2, 0, 0], 'self', note='Ritual (action list)'))
S.actionlist(RALATHIUS * 100 + 2, [
    (0, A(83, [3], 'self', note='Remove gossip + quest giver flags')),
    (0, A(63, [1, 0, 1], 'self', note='Reset apparition counter')),
    (0, S.cast(23017, 'self')),                                   # Arcane Channeling (Turtle's 45665 is not in 3.3.5)
    (3000, S.talk(1)),
    (5000, S.talk(2)),
    (5000, S.talk(3)),
    (5000, A(12, [APPARITION, 1, 120000, 0], 'pos', xyz=(5518.0, -3703.0, 1595.0, 0), note='Summon Nightmare Apparition')),
    (0, A(12, [APPARITION, 1, 120000, 0], 'pos', xyz=(5528.0, -3712.0, 1597.0, 0), note='Summon Nightmare Apparition')),
    (0, A(12, [APPARITION, 1, 120000, 0], 'pos', xyz=(5517.0, -3691.0, 1595.0, 0), note='Summon Nightmare Apparition')),
    # if the apparitions are not all killed, the flags come back after two minutes
    (122000, A(82, [3], 'self', note='Gossip + quest giver flags back (ritual not finished)')),
    (0, A(92, [], 'self', note='Stop casting'))], 'Ralathius')
# each apparition counts its death on Ralathius; at three, the Dream opens
S.on(APPARITION, 'death', A(63, [1, 1, 0], 'closest_creature', tp=[RALATHIUS, 100, 0], note='Count on Ralathius'))
S.on(RALATHIUS, 'counter', A(80, [RALATHIUS * 100 + 3, 0, 0], 'self', note='The Dream opens (action list)'), ep=[1, 3, 0, 0])
S.actionlist(RALATHIUS * 100 + 3, [
    (0, A(63, [1, 0, 1], 'self', note='Reset apparition counter')),
    (0, S.talk(4)),
    (3000, A(12, [URSOC, 1, 54000, 0], 'pos', xyz=(5529.0, -3694.0, 1596.0, 0), note='Summon Ursoc')),
    (0, A(12, [YSERA, 1, 54000, 0], 'pos', xyz=(5528.0, -3701.0, 1596.0, 0), note='Summon Ysera')),
    (0, A(12, [GOLDRINN, 1, 54000, 0], 'pos', xyz=(5533.0, -3704.0, 1597.0, 0), note='Summon Goldrinn')),
    (1000, by(YSERA, 2)),
    (5000, S.talk(5)),
    (5000, by(YSERA, 3)),
    (5000, S.talk(6)),
    (5000, by(YSERA, 4)),
    (5000, by(YSERA, 5)),
    (5000, by(YSERA, 6)),
    (5000, by(YSERA, 7)),
    (5000, by(YSERA, 8)),
    (5000, by(URSOC, 0)),
    (5000, by(YSERA, 9)),
    (5000, S.talk(7)),
    (1000, A(92, [], 'self', note='Stop casting')), (0, S.talk(8)),
    (1000, A(33, [60045], 'player_range', tp=[0, 40, 0], note='Quest Credit 60045 (players near Ralathius)')),
    (1000, A(82, [3], 'self', note='Gossip + quest giver flags back'))], 'Ralathius')

# ---- Runestones of Nordrassil and Cenarius: travel between them after The Runestone Scepter (40990)
R0 = OFF + 30127
S.gossip(R0, npc_text(30127), [(0, 66816, 0, 0, [(8, 40990, 0, 0)])])
for go, dest in ((2020036, (4474.1542, -3153.9086, 1033.9987, 3.3363)),        # Nordrassil -> Nordrassil's foot
                 (2020037, (5372.1660, -3696.9299, 1594.3531, 1.4211))):       # Cenarius -> Nordanaar
    S.names[go] = 'Runestone of Nordrassil' if go == 2020036 else 'Runestone of Cenarius'
    S.row(go, 1, 62, [R0, 0], A(62, [1], 'invoker', xyz=dest, note='Teleport'))
    S.row(go, 1, 62, [R0, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.extra_sql.append(f"UPDATE `gameobject_template` SET `Data3`={R0} WHERE `entry`={go};")

# ---- Turtle's quest drops on 3.3.5 creatures (the rollback removes exactly these rows)
#      Moontouched Amulet (Moontouched Owlbeasts, Winterspring), Slumberer's Shard (Weaver, Sunken Temple), Binding Fragment
#      (Cliff Breakers/Thunderers, Azshara), Overloaded Arcane Prism (Arcane Torrents, Winterspring), Rod of 'Ere / 'Lex (Legashi
#      and Jadefire satyrs), Arcane Essence (Eldreth spirits, Dire Maul - a normal drop on Turtle), Head of Alzzin the Wildshaper
#      (Dire Maul), Imbued Sludge (Living Decay / Rotting Sludge, Eastern Plaguelands)
STOCK_DROPS = S.stock_quest_drops([61414, 61557, 61558, 61559, 61640, 61641, 61673, 61702, 61715])

SQL = S.sql()
