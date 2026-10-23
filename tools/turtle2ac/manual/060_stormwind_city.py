"""Stormwind City - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_1.cpp, _3.cpp, gossip scripts
41248 and 8016301, EventAI of Sailor Pardol) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "Controlling Sailors" (40660, Petty Officer Milldough in Davenburg): Sailor Hylreth and Sailor Brewen answer when asked
  (npc_q_controlling_sailors); Sailor Pardol picks a fight and yields at half health (gossip script 41248 + EventAI).
- "Apple a Day" (80315): Iluria Nightwhisper hands over the Healing Balm (npc_iluria); Applebough's words on accepting
  and handing in the quest (npc_applebough; his leaf colour change uses Turtle displays and is left out).
Flavour: Koli Steamheart's thanks for "Recovering Vault Shackles" (40426, npc_koli_steamheart).
Travel: Steelwing, Operative Simmons' gryphon at the harbor, flies to the SI:7 Outpost on Balor (gossip script 8016301,
Turtle taxi path 298; build.py ports the path through the zone's scripted_taxi_paths).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
HYLRETH, BREWEN, PARDOL, ILURIA, APPLEBOUGH, KOLI, STEELWING = 61013, 61015, 61016, 80900, 80460, 80451, 80163
S.names.update({HYLRETH: 'Sailor Hylreth', BREWEN: 'Sailor Brewen', PARDOL: 'Sailor Pardol', ILURIA: 'Iluria Nightwhisper',
                APPLEBOUGH: 'Applebough', KOLI: 'Koli Steamheart', STEELWING: 'Steelwing'})
q, TW, item = ctx['q'], ctx['TW'], ctx['item']


def npc_text(i, default=None):
    """the text of a Turtle npc_text row (its first broadcast text): the C++ gossip menus send these. Some menus the C++
    sends have no npc_text row in Turtle's DB (the client then shows its generic greeting): `default` is used there"""
    r_ = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)
    if not r_:
        assert default, f'npc_text {i} is not in the Turtle DB'
        return default
    b = r_[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def creature_gossip(entry, menu):
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={menu}, `npcflag`=`npcflag`|1 WHERE `entry`={entry};")


# ---- "Controlling Sailors" (40660): Hylreth and Brewen answer the player (credits 60395, 60396)
for who_, say_, credit_ in ((HYLRETH, 66467, 60395), (BREWEN, 66468, 60396)):
    S.btext(who_, 0, say_)
    M = OFF + who_
    S.gossip(M, npc_text(who_), [(0, 66768, 0, 0, [(47, 40660, IN_PROGRESS, 0)])])
    S.row(who_, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.row(who_, 0, 62, [M, 0], S.talk(0))
    S.row(who_, 0, 62, [M, 0], A(5, [1], 'self', note='Emote Talk'))
    S.row(who_, 0, 62, [M, 0], A(33, [credit_], 'invoker', note=f'Quest Credit {credit_}'))
    creature_gossip(who_, M)

# ---- Sailor Pardol: asked to behave he turns on the player (gossip script 41248) and yields at half health
#      (EventAI 6101601: its "I yield" line is the build's conversion, group 50; the credit and the evade are here)
S.btext(PARDOL, 0, 51697)
M = OFF + PARDOL
S.gossip(M, npc_text(61016, 'Greetings, $n.'), [(0, 66768, 0, 0, [(47, 40660, IN_PROGRESS, 0)])])
S.row(PARDOL, 0, 62, [M, 0], A(80, [PARDOL * 100 + 1, 0, 0], 'self', note='Picks a fight (action list)'))
S.actionlist(PARDOL * 100 + 1, [
    (0, A(72, [], 'invoker', note='Close Gossip')),
    (0, S.talk(0)),
    (0, A(5, [36], 'self', note='Emote Attack')),
    (0, A(2, [14], 'self', note='Hostile (faction 14)')),
    (0, A(49, [], 'invoker', note='Attack'))], 'Sailor Pardol')
S.row(PARDOL, 0, 2, [0, 50, 0, 0], A(33, [60397], 'victim', note='Quest Credit 60397'), flags=1)
S.row(PARDOL, 0, 2, [0, 50, 0, 0], A(2, [0], 'self', note='Default faction again'), flags=1)
S.row(PARDOL, 0, 2, [0, 50, 0, 0], A(24, [], 'self', note='Evade'), flags=1)
S.on(PARDOL, 'evade', A(2, [0], 'self', note='Default faction again'))
S.on(PARDOL, 'respawn', A(2, [0], 'self', note='Default faction again'))
creature_gossip(PARDOL, M)

# ---- "Apple a Day" (80315): Iluria Nightwhisper gives the Healing Balm
BALM = item(80865)
S.btext(ILURIA, 0, 66928)
M = OFF + ILURIA
S.gossip(M, npc_text(1, 'Greetings, $n.'), [(0, 66927, 0, 0, [(47, 80315, IN_PROGRESS, 0), (2, BALM, 1, 1)])])
S.row(ILURIA, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(ILURIA, 0, 62, [M, 0], A(56, [BALM, 1], 'invoker', note='Give Healing Balm'))
S.row(ILURIA, 0, 62, [M, 0], S.talk(0))
S.row(ILURIA, 0, 62, [M, 0], A(5, [1], 'self', note='Emote Talk'))
creature_gossip(ILURIA, M)

# ---- Applebough: his words on accepting and handing in "Apple a Day"
S.btext(APPLEBOUGH, 0, 66929)
S.btext(APPLEBOUGH, 1, 66931)
S.on(APPLEBOUGH, 'accepted_quest', S.talk(0), A(5, [18], 'self', note='Emote Cry'), ep=[80315])
S.on(APPLEBOUGH, 'reward_quest', S.talk(1), A(5, [4], 'self', note='Emote Cheer'), ep=[80315])

# ---- Koli Steamheart: thanks for "Recovering Vault Shackles" (40426)
S.btext(KOLI, 0, 66728)
S.on(KOLI, 'reward_quest', S.talk(0), A(5, [1], 'self', note='Emote Talk'), ep=[40426])

# ---- Steelwing: "Take me to Balor!" - the flight to the SI:7 Outpost (Turtle taxi path 298)
M = OFF + STEELWING
S.gossip(M, npc_text(8016301), [(0, 'Take me to Balor!', 0, 0, [])])
S.row(STEELWING, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(STEELWING, 0, 62, [M, 0], A(52, [ctx['taxi_path'](298)], 'invoker', note='Fly to the SI:7 Outpost, Balor'))
creature_gossip(STEELWING, M)

SQL = S.sql()
