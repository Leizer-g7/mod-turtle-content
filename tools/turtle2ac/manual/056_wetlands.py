"""Wetlands - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp and _3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "Sleepwalking at Day" (40567): Bert Mano is asked about his wife's evidence (credit 60391).
- "Strange Bedfellows" (40571): the Felbound Pendant is shown to Bert Mano, who calls Hedania (she drops the quest item).
- "Oscilation Inhibited Disk!" (55211): Barthos Thundercrank builds the disk when the quest is accepted (credit 91301).
- "The Hawk's Vigil" (55225): Harlus Ashbuckle (Martin Corinth) is told he will be executed and attacks.
- Turtle's quest drops on 3.3.5 creatures: Lesser Felguards (Ashenvale), Leech/Cave Stalkers, Razormaws, the Wetlands oozes and Mottled
  Raptors/Screechers (40569, 40566, 40682, 55200, 55201).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
BERT, BARTHOS, HARLUS, HEDANIA = 52017, 52066, 52119, 60954
S.names.update({BERT: 'Bert Mano', BARTHOS: 'Barthos Thundercrank', HARLUS: 'Harlus Ashbuckle', HEDANIA: 'Hedania'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these"""
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


# ---- Bert Mano: Sleepwalking at Day (40567) and Strange Bedfellows (40571)
S.btext(BERT, 0, 66462)
B0, B1 = OFF + 52017, OFF + 30035
S.gossip(B1, npc_text(30035))
S.gossip(B0, npc_text(52017), [(0, 66758, 0, B1, [(47, 40567, IN_PROGRESS, 0)]),
                               (1, 66759, 0, 0, [(47, 40571, IN_PROGRESS, 0), (29, HEDANIA, 40, 1)])])
S.row(BERT, 0, 62, [B0, 0], A(33, [60391], 'invoker', note='Quest Credit 60391'))
S.row(BERT, 0, 62, [B0, 1], A(72, [], 'invoker', note='Close Gossip'))
S.row(BERT, 0, 62, [B0, 1], S.talk(0))
S.row(BERT, 0, 62, [B0, 1], A(5, [1], 'self', note='Emote Talk'))
S.row(BERT, 0, 62, [B0, 1], A(80, [BERT * 100 + 1, 0, 0], 'self', note='Hedania (action list)'))
S.actionlist(BERT * 100 + 1, [
    (3000, A(12, [HEDANIA, 4, 30000], 'self', note='Summon Hedania (despawns 30 s out of combat)'))], 'Bert Mano')
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={B0}, `npcflag`=`npcflag`|1 WHERE `entry`={BERT};")

# ---- Barthos Thundercrank: Oscilation Inhibited Disk! (55211) accepted - he builds it
S.btext(BARTHOS, 0, 66997)
S.btext(BARTHOS, 1, 66998)
S.btext(BARTHOS, 2, 66999)
S.on(BARTHOS, 'accepted_quest', A(80, [BARTHOS * 100 + 1, 0, 0], 'self', note='Building the disk (action list)'), ep=[55211])
S.actionlist(BARTHOS * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, A(5, [69], 'self', note='Emote Use Standing')),
    (0, S.talk(0)),
    (6000, S.talk(1)),
    (6000, S.talk(2)),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again')),
    (0, A(33, [91301], 'invoker', note='Quest Credit 91301')),
    (2000, A(5, [0], 'self', note='Emote None'))], 'Barthos Thundercrank')

# ---- Harlus Ashbuckle (Martin Corinth): The Hawk's Vigil (55225) - the sentence, then he attacks
S.btext(HARLUS, 0, 67014)
S.btext(HARLUS, 1, 67015)
S.btext(HARLUS, 2, 67016)
H0 = OFF + 52119
S.gossip(H0, npc_text(52119), [(0, 67013, 0, 0, [(47, 55225, IN_PROGRESS, 0)])])
S.row(HARLUS, 0, 62, [H0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(HARLUS, 0, 62, [H0, 0], A(80, [HARLUS * 100 + 1, 0, 0], 'self', note='The sentence (action list)'))
S.actionlist(HARLUS * 100 + 1, [
    (1000, S.talk(0)), (0, A(5, [11], 'self', note='Emote Laugh')),
    (4000, S.talk(1)), (0, A(5, [274], 'self', note='Emote No')),
    (4000, S.talk(2)), (0, A(5, [36], 'self', note='Emote Attack')),
    (0, A(2, [14], 'self', note='Hostile (faction 14)')),
    (0, A(49, [], 'invoker', note='Attack'))], 'Harlus Ashbuckle')
S.on(HARLUS, 'evade', A(2, [0], 'self', note='Default faction again'))
S.on(HARLUS, 'respawn', A(2, [0], 'self', note='Default faction again'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={H0}, `npcflag`=`npcflag`|1 WHERE `entry`={HARLUS};")

# ---- Turtle's quest drop on a 3.3.5 creature (quest-only loot rows; the rollback removes them)
#      Lesser Felguards (Ashenvale) for Sweet Dreams are Made of This; Leech and Cave Stalkers (Leech Stalker Venom) for Sleep Paralysis;
#      Highland and Elder Razormaws (Razormaw Talon) for Raptor Ridge; the Wetlands oozes (Sticky Ooze-Tar) for Preparations for Adventure!;
#      Mottled Raptors and Screechers (Mottled Talon) for Retaking The Roadways
STOCK_DROPS = S.stock_quest_drops([60823, 60822, 60924, 81400, 81401])

# ---- 3.3.5 spawns where Turtle reshaped the ground (moved by the height change found by the ground check: the
#      Bruiseweed herbs south of Grim Batol and near Dun Agrath, a Black Ooze, a Young Wetlands Crocolisk and a Mottled Raptor)
for table_, guid_, dz_ in (('gameobject', 204320, -24.6), ('gameobject', 204331, 17.0), ('creature', 10322, -2.9),
                           ('creature', 9650, -1.8), ('creature', 10931, -1.4)):
    z_ = q(f"select position_z z from {ctx['AC']}.{table_} where guid=%s", guid_)[0]['z']
    S.stock_spawn(table_, guid_, position_z=round(z_ + dz_, 3))

SQL = S.sql()
