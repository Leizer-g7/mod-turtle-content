"""Feralas - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- The Way of the Spiritwolf III-V (40532-40534), the Ancient Wolf Spirit by its waterfall (npc_ancient_spirit_wolf):
  III: pour the powder (gossip) -> credit 60378; IV: it tells its tale (two lines) -> credit 60379 after 28 s;
  V: it fights the player and yields at 10 % health -> credit 60380 for everyone it was fighting.
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
WOLF = 66004
S.names.update({WOLF: 'Ancient Wolf Spirit'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


# ---- The Way of the Spiritwolf III-V: the Ancient Wolf Spirit
S.btext(WOLF, 0, 66456)
S.btext(WOLF, 1, 66457)
M = OFF + WOLF
S.gossip(M, npc_text(WOLF), [(0, 66751, 0, 0, [(47, 40532, IN_PROGRESS, 0)]),
                             (1, 66752, 0, 0, [(47, 40533, IN_PROGRESS, 0)]),
                             (2, 66753, 0, 0, [(47, 40534, IN_PROGRESS, 0)])])
# III: the powder
S.row(WOLF, 0, 62, [M, 0], A(33, [60378], 'invoker', note='Quest Credit 60378'))
S.row(WOLF, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
# IV: the tale (one telling at a time: the gossip flag comes back at the end)
S.row(WOLF, 0, 62, [M, 1], A(72, [], 'invoker', note='Close Gossip'))
S.row(WOLF, 0, 62, [M, 1], A(80, [WOLF * 100 + 1, 0, 0], 'self', note='Tells its tale (action list)'))
S.actionlist(WOLF * 100 + 1, [
    (0, A(83, [1], 'self', note='Remove gossip flag while telling')),
    (3000, S.talk(0)),
    (15000, S.talk(1)),
    (10000, A(33, [60379], 'invoker', note='Quest Credit 60379')),
    (0, A(82, [1], 'self', note='Gossip flag back'))], 'Ancient Wolf Spirit')
# V: the challenge - hostile until it yields at 10 % health (Turtle: SetFactionTemporary(14, RESTORE_COMBAT_STOP), then
#    at < 10 % it stops fighting, turns friendly and credits every player on its threat list)
S.row(WOLF, 0, 62, [M, 2], A(72, [], 'invoker', note='Close Gossip'))
S.row(WOLF, 0, 62, [M, 2], A(42, [0, 10], 'self', note='Cannot drop below 10 % health'))
S.row(WOLF, 0, 62, [M, 2], A(5, [36], 'self', note='Emote Attack'))
S.row(WOLF, 0, 62, [M, 2], A(2, [14], 'self', note='Hostile (faction 14)'))
S.row(WOLF, 0, 62, [M, 2], A(49, [], 'invoker', note='Attack'))
S.on(WOLF, 'hp', A(33, [60380], 'threat_list', note='Quest Credit 60380 (everyone it fought)'),
     A(2, [0], 'self', note='Default faction again'), A(24, [], 'self', note='Stop fighting (evade)'), ep=(0, 10, 1000, 1000))
S.on(WOLF, 'evade', A(2, [0], 'self', note='Default faction again'))
S.on(WOLF, 'respawn', A(2, [0], 'self', note='Default faction again'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M}, `npcflag`=`npcflag`|1 WHERE `entry`={WOLF};")

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): the Longtooth wolves
#      (Spiritwolf II, Provisions for Thalanaar), the Frayfeather hippogryphs (Feeding the Younglings), Lord Vyletongue in
#      Maraudon (Harness of Chimaeran), the Galak Messenger and the Galak centaurs of Thousand Needles (Anashya's two quests)
STOCK_DROPS = S.stock_quest_drops([60768, 61741, 61747, 61748, 61749, 61750])

# ---- 3.3.5 spawns on ground Turtle reshaped (stock-spawn ground check): Turtle lowered Thalanaar's ground by the moonwell;
#      two 3.3.5 NPCs there (Kristy Grant, Rendow) are moved down with it. The moonwell objects stay where they are (Turtle's
#      own moonwell keeps its height; the 3.3.5 ones sit with it).
for guid_, drop_ in ((50057, 0.8), (50796, 1.2)):
    z_ = q(f"select position_z z from {ctx['AC']}.creature where guid=%s", guid_)[0]['z']
    S.stock_spawn('creature', guid_, position_z=round(z_ - drop_, 3))

SQL = S.sql()
