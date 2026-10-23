"""Badlands - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "The Land of Kings" (40713): the Gong of Corthan in the Temple of Corthan, struck with the Mallet of Zeth, calls up the echoes
  of King Corthan and two of his lords; they speak, and after 22 s the player gets credit 60009 (go_gong_of_corthan).
- "The Curse of Zetharia" (40714): the Forgotten Keeper tells the tale over six gossip pages; the last one gives credit 60010
  (npc_forgotten_keeper).
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
GO_NO_SELECT = 16
EMOTE_STATE_KNEEL = 68
GONG, KEEPER = 2010946, 60916
ECHO, CHIEFTAIN, WARLORD = 61066, 61067, 61068
S.names.update({GONG: 'Gong of Corthan', KEEPER: 'Forgotten Keeper', ECHO: 'Echo of Corthan',
                CHIEFTAIN: 'Forgotten Chieftain', WARLORD: 'Forgotten Warlord'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


# ---- "The Land of Kings" (40713): the Gong of Corthan
G = OFF + 30051
S.gossip(G, npc_text(30051), [(0, 66777, 0, 0, [(47, 40713, IN_PROGRESS, 0), (2, 60944, 1, 0)])])
for who_, x_, y_, z_, o_ in ((ECHO, -6381.10, -3024.88, 403.54, 1.60), (WARLORD, -6379.24, -3021.03, 403.46, 4.36),
                             (CHIEFTAIN, -6383.77, -3020.89, 403.37, 5.03)):
    S.row(GONG, 1, 62, [G, 0], S.summon(who_, x_, y_, z_, o_, 3, 22000))
S.row(GONG, 1, 62, [G, 0], A(72, [], 'invoker', note='Close Gossip'))
# Turtle: one calling at a time (a 24-s controller summon); here the gong is not usable while the echoes are out
S.row(GONG, 1, 62, [G, 0], A(105, [GO_NO_SELECT], 'self', note='Not usable while the echoes speak'))
S.row(GONG, 1, 62, [G, 0], A(80, [GONG * 100 + 1, 0, 0], 'self', note='Credit after the echoes (action list)'))
S.actionlist(GONG * 100 + 1, [(22000, A(33, [60009], 'invoker', note='Quest Credit 60009')),
                              (2000, A(106, [GO_NO_SELECT], 'self', note='Usable again'))], 'Gong of Corthan')
S.extra_sql.append(f"UPDATE `gameobject_template` SET `type`=2, `Data3`={G}, `AIName`='SmartGameObjectAI', `ScriptName`='' WHERE `entry`={GONG};")
# the echoes keep Turtle's timing from the moment they appear: the lords kneel after 1 s, Corthan speaks at 4 s,
# the warlord at 11 s, the chieftain at 12 s
S.btext(ECHO, 0, 66526)
S.btext(WARLORD, 0, 66527)
S.btext(CHIEFTAIN, 0, 66528)
S.on(ECHO, 'summoned', A(80, [ECHO * 100 + 1, 0, 0], 'self', note='Speaks (action list)'))
S.actionlist(ECHO * 100 + 1, [(4000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk'))], 'Echo of Corthan')
for who_, at_ in ((WARLORD, 11000), (CHIEFTAIN, 12000)):
    S.on(who_, 'summoned', A(80, [who_ * 100 + 1, 0, 0], 'self', note='Kneels, then speaks (action list)'))
    S.actionlist(who_ * 100 + 1, [(1000, A(17, [EMOTE_STATE_KNEEL], 'self', note='Emote state Kneel')),
                                  (at_ - 1000, S.talk(0)), (0, A(5, [1], 'self', note='Emote Talk'))], S.names[who_])

# ---- "The Curse of Zetharia" (40714): the Forgotten Keeper's tale, page by page
PAGES = [OFF + 60916] + [OFF + t for t in (30102, 30103, 30104, 30105, 30106, 30107)]
S.gossip(PAGES[0], npc_text(60916), [(0, 66778, 0, PAGES[1], [(47, 40714, IN_PROGRESS, 0)])])
for n_ in range(1, 6):
    S.gossip(PAGES[n_], npc_text(PAGES[n_] - OFF), [(0, 66779, 0, PAGES[n_ + 1], [])])
S.gossip(PAGES[6], npc_text(30107))
S.row(KEEPER, 0, 62, [PAGES[5], 0], A(33, [60010], 'invoker', note='Quest Credit 60010'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={PAGES[0]}, `npcflag`=`npcflag`|1 WHERE `entry`={KEEPER};")

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Angor Fortress (Shadowforge
#      dwarves), A Heart of Stone (Stone Golems), Pitch a Tent (the Badlands buzzards and coyotes), Re-assembler! (Stonevault ogres)
STOCK_DROPS = S.stock_quest_drops([60311, 60891, 70038, 59997])

# ---- 3.3.5 spawns on ground Turtle reshaped (stock-spawn ground check)
#      Turtle removed two: a Scalding Whelp where the Scalebane Ridge camp stands and an Enraged Rock Elemental where Noli and Brotalus camp
for guid_ in (6907, 7158):
    S.stock_spawn_remove('creature', guid_)
#      Turtle raised the slopes of Lethlor Ravine under three Scalding Whelps, and a Wild Steelbloom spot by the camp:
#      moved up by the rise (the Angor Fortress and Uldaman spawns the check also lists are indoors, under both grounds)
for table_, guid_, rise_ in (('creature', 6904, 5.9), ('creature', 6906, 10.3), ('creature', 6908, 3.5), ('gameobject', 205681, 0.9)):
    z_ = q(f"select position_z z from {ctx['AC']}.{table_} where guid=%s", guid_)[0]['z']
    S.stock_spawn(table_, guid_, position_z=round(z_ + rise_, 3))

SQL = S.sql()
