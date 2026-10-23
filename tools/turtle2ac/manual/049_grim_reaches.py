"""Grim Reaches - Turtle quest scripts the build does not convert by itself, re-expressed as SmartAI.

"The Ritual of Uth'okk" (41731): Turtle's quest start script. When a player accepts the quest, Far Seer Mothang
closes his services, channels for 18 seconds (with his two lines), flies into a rage, roars, gives the quest credit
(dummy NPC 60079) to the player who started it, laughs and opens his services again.

Run by build.py: `S` (lib.smartgen.Smart) and `ctx` are provided; the result is the module text SQL.
"""
MOTHANG, QUEST, CREDIT = 62432, 41731, 60079
A = S.raw
S.names[MOTHANG] = 'Far Seer Mothang'
S.btext(MOTHANG, 0, 6243202, 'emote')
S.btext(MOTHANG, 1, 6243203)
S.btext(MOTHANG, 2, 6243204)
NPC_FLAGS = 0x2 | 0x1                  # quest giver + gossip, removed for the duration (Turtle: flags 3)

S.on(MOTHANG, 'accepted_quest', A(80, [MOTHANG * 100 + 1, 0, 0], 'self', note='Ritual (action list)'), ep=[QUEST])
S.actionlist(MOTHANG * 100 + 1, [
    (0, A(83, [NPC_FLAGS], 'self', note='Remove quest giver / gossip flags')),
    (0, S.cast(13236, 'self')),                                              # Nature Channeling
    (0, S.talk(0)),                                                          # begins the ritual (emote)
    (8000, S.talk(1)),                                                       # power flowing
    (10000, A(28, [13236], 'self', note='Stop Nature Channeling')),
    (0, S.cast(51206, 'self', triggered=True)),                              # Enrage (3.3.5 stand-in)
    (0, A(5, [15], 'self', note='Emote Roar')),
    (1000, S.talk(2)),                                                       # ritual complete
    (0, A(33, [CREDIT], 'invoker', note=f'Quest Credit {CREDIT}')),
    (1000, A(5, [11], 'self', note='Emote Laugh')),
    (0, A(82, [NPC_FLAGS], 'self', note='Restore quest giver / gossip flags'))], 'Far Seer Mothang')

SQL = S.sql()
