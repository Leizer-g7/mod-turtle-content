"""Tel'Abim - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "Gargantuan Information!" (40733): Leezza Fraxtoggle tells her tale, then the credit (Turtle dummy 60013).
- "The Missing Friend!" (40771): Nibu is told to go home (credit 60014).
- "Secrets of the Dark Iron Desecrator" (40761): Gelwig Darkbrow (Steamwheedle Port, Tanaris; a Turtle NPC added to
  this zone) hands over the plans.
- Turtle's quest drops on 3.3.5 creatures: Blighted Essence (Operation Help Jabbey 2), Molten Fragment (The Dark Iron
  Desecrator), Frostwoven Chillwind Horn (Chillwind Armor).
Flavour: Tazzo Gearfire grows the Gargantuan Banana when "The Final Test" (40737) is accepted, and his, Bixxle
Screwfuse's, Pumpworker Zalwan's, Wazlon Headiron's and Sneel Fizzwack's lines when quests are handed in.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
NO_SELECT = 0x2000000                 # UNIT_FLAG_NOT_SELECTABLE
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
TAZZO, BIXXLE, WAZLON, ZALWAN, SNEEL, LEEZZA, NIBU, GELWIG = 61100, 61101, 61108, 61111, 61113, 61116, 61157, 60955
S.names.update({TAZZO: 'Tazzo Gearfire', BIXXLE: 'Bixxle Screwfuse', WAZLON: 'Wazlon Headiron', ZALWAN: 'Pumpworker Zalwan',
                SNEEL: 'Sneel Fizzwack', LEEZZA: 'Leezza Fraxtoggle', NIBU: 'Nibu', GELWIG: 'Gelwig Darkbrow'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these"""
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def say_on_reward(npc, quest, group, text, emote=1):
    S.btext(npc, group, text)
    S.on(npc, 'reward_quest', S.talk(group), ep=[quest])
    if emote:
        S.on(npc, 'reward_quest', A(5, [emote], 'self', note='Emote Talk'), ep=[quest])


# ---- quest hand-in lines
say_on_reward(ZALWAN, 40726, 0, 66567)                       # The Backup Seal-Valve
say_on_reward(WAZLON, 40727, 0, 66568)                       # Derelict Supplies
say_on_reward(TAZZO, 40729, 0, 66574)                        # Collecting Specimens
say_on_reward(TAZZO, 40734, 1, 66578)                        # A Must Have Discovery
say_on_reward(BIXXLE, 40760, 0, 66594)                       # Operation Final Repairs
S.on(BIXXLE, 'reward_quest', A(5, [11], 'self', note='Emote Laugh'), ep=[40761])   # Secrets of the Dark Iron Desecrator
say_on_reward(BIXXLE, 40762, 1, 66595)                       # The Dark Iron Desecrator
say_on_reward(SNEEL, 40785, 0, 66596)                        # King Morogo Thunderfoot!

# ---- Tazzo Gearfire: Early Testing (40730) handed in - the banana bloats and collapses
S.btext(TAZZO, 2, 66575, chat='emote')
S.btext(TAZZO, 3, 66576, chat='emote')
S.btext(TAZZO, 4, 66577)
S.on(TAZZO, 'reward_quest', A(80, [TAZZO * 100 + 1, 0, 0], 'self', note='Early Testing (action list)'), ep=[40730])
S.actionlist(TAZZO * 100 + 1, [
    (0, S.talk(2)),
    (5000, S.talk(3)),
    (4000, S.talk(4)), (0, A(5, [1], 'self', note='Emote Talk'))], 'Tazzo Gearfire')

# ---- Tazzo Gearfire: The Final Test (40737) accepted - the Gargantuan Banana grows
S.btext(TAZZO, 5, 66569)
S.btext(TAZZO, 6, 66570, chat='emote')
S.btext(TAZZO, 7, 66571)
S.btext(TAZZO, 8, 66572, chat='emote')
S.btext(TAZZO, 9, 66573)
S.on(TAZZO, 'accepted_quest', A(80, [TAZZO * 100 + 2, 0, 0], 'self', note='The Final Test (action list)'), ep=[40737])
S.actionlist(TAZZO * 100 + 2, [
    (0, A(83, [3], 'self', note='Remove gossip + quest giver flags')),
    (0, S.cast(23017, 'self')),                                   # Arcane Channeling
    (3000, S.talk(5)),
    (7000, S.talk(6)),
    (3000, S.talk(7)),
    (5000, S.talk(8)),
    (3000, S.cast(1449, 'self')),                                 # Arcane Explosion (visual)
    (2000, S.talk(9)), (0, A(5, [4], 'self', note='Emote Cheer')),
    (0, A(82, [3], 'self', note='Gossip + quest giver flags back'))], 'Tazzo Gearfire')

# ---- Leezza Fraxtoggle: Gargantuan Information! (40733) - her tale, then the credit
S.btext(LEEZZA, 0, 66579)
S.btext(LEEZZA, 1, 66580)
S.btext(LEEZZA, 2, 66581)
L0 = OFF + 61116
S.gossip(L0, npc_text(61116), [(0, 66780, 0, 0, [(47, 40733, IN_PROGRESS, 0)])])
S.row(LEEZZA, 0, 62, [L0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(LEEZZA, 0, 62, [L0, 0], A(80, [LEEZZA * 100 + 1, 0, 0], 'self', note='Tale (action list)'))
S.actionlist(LEEZZA * 100 + 1, [
    (0, A(18, [NO_SELECT], 'self', note='Not selectable')),
    (0, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk')),
    (13000, S.talk(1)), (0, A(5, [1], 'self', note='Emote Talk')),
    (15000, S.talk(2)), (0, A(5, [1], 'self', note='Emote Talk')),
    (5000, A(33, [60013], 'invoker', note='Quest Credit 60013')),
    (0, A(19, [NO_SELECT], 'self', note='Selectable again'))], 'Leezza Fraxtoggle')
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={L0}, `npcflag`=`npcflag`|1 WHERE `entry`={LEEZZA};")

# ---- Nibu: The Missing Friend! (40771)
N0 = OFF + 61157
S.gossip(N0, npc_text(61157), [(0, 66782, 0, 0, [(47, 40771, IN_PROGRESS, 0)])])
S.row(NIBU, 0, 62, [N0, 0], A(33, [60014], 'invoker', note='Quest Credit 60014'))
S.row(NIBU, 0, 62, [N0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={N0}, `npcflag`=`npcflag`|1 WHERE `entry`={NIBU};")

# ---- Gelwig Darkbrow (Steamwheedle Port): Secrets of the Dark Iron Desecrator (40761) - the plans
S.btext(GELWIG, 0, 66164)
G0 = OFF + 60955
S.gossip(G0, npc_text(60955), [(0, 66781, 0, 0, [(47, 40761, IN_PROGRESS, 0), (2, 60998, 1, 1)]),
                     (1, 'I want to browse your goods.', 1, 0, [], (3, 128))])
S.row(GELWIG, 0, 62, [G0, 0], A(56, [60998, 1], 'invoker', note='Give the Dark Iron Desecrator plans'))
S.row(GELWIG, 0, 62, [G0, 0], S.talk(0))
S.row(GELWIG, 0, 62, [G0, 0], A(5, [1], 'self', note='Emote Talk'))
S.row(GELWIG, 0, 62, [G0, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={G0}, `npcflag`=`npcflag`|1 WHERE `entry`={GELWIG};")
# Turtle stands him at z 8.99 on its own, lower ground of Steamwheedle Port. Until 2026-10-10 that tile was not part of
# this module and he was raised to the 3.3.5 ground (10.19); Tanaris (072) now ships Turtle's ground there (the chunk of
# Turtle's new house), so he keeps Turtle's height.

# ---- Turtle's quest drop on 3.3.5 creatures (quest-only loot rows; the rollback removes them)
#      Blighted Essence (Blighted Horrors, Eastern Plaguelands) for Operation Help Jabbey 2, Molten Fragment (Molten
#      Destroyers, Molten Core) for The Dark Iron Desecrator, Frostwoven Chillwind Horn (Chillwind Chimaeras, Winterspring)
#      for Chillwind Armor
STOCK_DROPS = S.stock_quest_drops([60994, 61067, 61078])

SQL = S.sql()
