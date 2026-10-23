"""Dustwallow Marsh - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- The Vimes / Falgran chain: "The Shield's Owner" (40554) - the three privates at Sentry Point and North Point Tower answer and
  give credits 60385-60387; "The Meeting with the Enemy" (40558) and "The Second Meeting" (40564) - Falgran Hastil and Kagoro talk
  it over (187 s / 105 s) and give credits 60388 / 60390; "Ritual of Divination" (40562) - Magus Halister calls up Paval Reethe's
  spirit (79 s, credit 60389).
- Kagoro's chain: "Next Course of Action" (40718) and "Tedious Diplomacy Once More" (40721) - Kagoro and Falgran talk it over
  (175 s / 130 s) when the quest is accepted; credits 60011 / 60012.
- "Reports of Dustwallow" (40415): Captain Wallace Cross and Captain Harker hand over their reports.
- "The Good Snuff" (40411): Jabbey (3.3.5 NPC, Gadgetzan) hands over Groy's package. His menu also carries the Burning
  Steppes quest "To Purchase Secret Information" (40466): he hands over the item it needs (Turtle's npc_jabbey, one menu).
- "The Way Of The Witch Doctor IV" (40352): N'ribbi takes the serum (credit 60353).
Flavour: the toads cheer N'ribbi (40353), Gizzix Grimegurgle's words on "Exquisite Goblin Engineering" (40719).
Falgran Hastil is a 3.3.5 template that 3.3.5 only summons for a moment in Theramore (its SmartAI walks him away and despawns him):
the spawn this zone adds gets scripts of its own (guid rows), which replace that. "Preparation for Divination" (40561): the
Archmage Ansirem part is in manual/053_lapidis_isle.py (that file owns Ansirem's SmartAI).
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS); two NPCs Turtle placed on the exact spot of a 3.3.5 NPC are moved
beside it.
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
import math
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
NO_SELECT = 0x2000000
FALGRAN, KAGORO, HALISTER, PAVAL, NRIBBI, GIZZIX, JABBEY = 5088, 61056, 60731, 60953, 60631, 23570, 8139
CROSS, HARKER, TALMAND, SLEIGHTOR, VALNOR = 60729, 60730, 60949, 60950, 60951
TOADS = (60866, 60867, 60868)
S.names.update({FALGRAN: 'Falgran Hastil', KAGORO: 'Kagoro', HALISTER: 'Magus Halister', PAVAL: 'Paval Reethe', NRIBBI: "N'ribbi",
                GIZZIX: 'Gizzix Grimegurgle', JABBEY: 'Jabbey', CROSS: 'Captain Wallace Cross', HARKER: 'Captain Harker',
                TALMAND: 'Private Talmand', SLEIGHTOR: 'Private Sleightor', VALNOR: 'Private Valnor'})
q, TW, item, cguid = ctx['q'], ctx['TW'], ctx['item'], ctx['cguid']
FALGRAN_G = -cguid(2572947)          # the Falgran this zone spawns: guid scripts
S.names[FALGRAN_G] = 'Falgran Hastil (Quagmire)'
ANIM = {'TALK': 1, 'LAUGH': 11, 'SALUTE': 66, 'BOW': 2}
SCENES = {}
SCENES['falgran_40558'] = [
    (5000, 'F', 'say', 66478), (5000, 'F', 'anim', 'TALK'), (13000, 'K', 'say', 66479), (13000, 'K', 'anim', 'TALK'),
    (21000, 'F', 'say', 66480), (21000, 'F', 'anim', 'TALK'), (29000, 'K', 'say', 66481), (29000, 'K', 'anim', 'TALK'),
    (32000, 'K', 'emote', 66482), (37000, 'K', 'say', 66483), (37000, 'K', 'anim', 'TALK'), (47000, 'F', 'say', 66484),
    (47000, 'F', 'anim', 'TALK'), (55000, 'K', 'say', 66485), (55000, 'K', 'anim', 'TALK'), (63000, 'F', 'say', 66486),
    (63000, 'F', 'anim', 'TALK'), (68000, 'K', 'say', 66487), (68000, 'K', 'anim', 'TALK'), (73000, 'F', 'say', 66488),
    (73000, 'F', 'anim', 'TALK'), (78000, 'K', 'say', 66489), (78000, 'K', 'anim', 'TALK'), (81000, 'F', 'say', 66490),
    (81000, 'F', 'anim', 'TALK'), (85000, 'K', 'emote', 66491), (88000, 'F', 'say', 66492), (88000, 'F', 'anim', 'TALK'),
    (100000, 'K', 'say', 66493), (100000, 'K', 'anim', 'TALK'), (110000, 'F', 'say', 66494), (110000, 'F', 'anim', 'TALK'),
    (122000, 'K', 'say', 66495), (122000, 'K', 'anim', 'TALK'), (136000, 'F', 'say', 66496), (136000, 'F', 'anim', 'TALK'),
    (144000, 'K', 'say', 66497), (144000, 'K', 'anim', 'TALK'), (156000, 'F', 'say', 66498), (156000, 'F', 'anim', 'TALK'),
    (164000, 'K', 'say', 66499), (164000, 'K', 'anim', 'TALK'), (174000, 'F', 'say', 66500), (174000, 'F', 'anim', 'TALK'),
    (182000, 'K', 'say', 66501), (182000, 'K', 'anim', 'TALK'), (187000, 'player', 'credit', 60388),
]
SCENES['falgran_40564'] = [
    (5000, 'F', 'say', 66502), (5000, 'F', 'anim', 'TALK'), (8000, 'K', 'say', 66503), (8000, 'K', 'anim', 'TALK'),
    (10000, 'F', 'say', 66504), (10000, 'F', 'anim', 'TALK'), (20000, 'K', 'say', 66505), (20000, 'K', 'anim', 'TALK'),
    (27000, 'F', 'say', 66506), (27000, 'F', 'anim', 'TALK'), (35000, 'K', 'say', 66507), (35000, 'K', 'anim', 'TALK'),
    (41000, 'F', 'say', 66508), (41000, 'F', 'anim', 'TALK'), (54000, 'K', 'say', 66509), (54000, 'K', 'anim', 'TALK'),
    (57000, 'F', 'say', 66510), (57000, 'F', 'anim', 'TALK'), (65000, 'K', 'say', 66511), (65000, 'K', 'anim', 'TALK'),
    (72000, 'F', 'say', 66512), (72000, 'F', 'anim', 'TALK'), (80000, 'K', 'say', 66513), (80000, 'K', 'anim', 'TALK'),
    (88000, 'F', 'say', 66514), (88000, 'F', 'anim', 'TALK'), (98000, 'K', 'say', 66515), (98000, 'K', 'anim', 'TALK'),
    (104000, 'F', 'say', 66516), (104000, 'F', 'anim', 'TALK'), (105000, 'player', 'credit', 60390),
]
SCENES['kagoro_40718'] = [
    (1000, 'K', 'say', 66529), (1000, 'K', 'anim', 'TALK'), (10000, 'F', 'say', 66530), (10000, 'F', 'anim', 'TALK'),
    (18000, 'K', 'say', 66531), (18000, 'K', 'anim', 'TALK'), (21000, 'K', 'emote', 66532), (26000, 'K', 'say', 66533),
    (26000, 'K', 'anim', 'TALK'), (36000, 'F', 'say', 66534), (36000, 'F', 'anim', 'TALK'), (44000, 'K', 'say', 66535),
    (44000, 'K', 'anim', 'TALK'), (52000, 'F', 'say', 66536), (52000, 'F', 'anim', 'TALK'), (60000, 'K', 'say', 66537),
    (60000, 'K', 'anim', 'TALK'), (65000, 'F', 'say', 66538), (65000, 'F', 'anim', 'TALK'), (70000, 'K', 'say', 66539),
    (70000, 'K', 'anim', 'TALK'), (73000, 'F', 'say', 66540), (73000, 'F', 'anim', 'TALK'), (77000, 'K', 'emote', 66491),
    (80000, 'F', 'say', 66541), (80000, 'F', 'anim', 'TALK'), (92000, 'K', 'say', 66542), (92000, 'K', 'anim', 'TALK'),
    (102000, 'F', 'say', 66543), (102000, 'F', 'anim', 'TALK'), (114000, 'K', 'say', 66544), (114000, 'K', 'anim', 'TALK'),
    (128000, 'F', 'say', 66545), (128000, 'F', 'anim', 'TALK'), (136000, 'K', 'say', 66546), (136000, 'K', 'anim', 'TALK'),
    (144000, 'F', 'say', 66547), (144000, 'F', 'anim', 'TALK'), (152000, 'K', 'say', 66548), (152000, 'K', 'anim', 'TALK'),
    (162000, 'F', 'say', 66549), (162000, 'F', 'anim', 'TALK'), (170000, 'K', 'say', 67030), (170000, 'K', 'anim', 'TALK'),
    (175000, 'player', 'credit', 60011),
]
SCENES['kagoro_40721'] = [
    (1000, 'F', 'say', 66550), (1000, 'F', 'anim', 'TALK'), (14000, 'K', 'say', 66551), (14000, 'K', 'anim', 'TALK'),
    (24000, 'F', 'say', 66552), (24000, 'F', 'anim', 'TALK'), (34000, 'K', 'say', 66553), (34000, 'K', 'anim', 'TALK'),
    (42000, 'F', 'say', 66554), (42000, 'F', 'anim', 'TALK'), (57000, 'K', 'say', 66555), (57000, 'K', 'anim', 'TALK'),
    (62000, 'F', 'say', 66556), (62000, 'F', 'anim', 'TALK'), (72000, 'K', 'say', 66557), (72000, 'K', 'anim', 'TALK'),
    (82000, 'F', 'say', 66558), (82000, 'F', 'anim', 'TALK'), (92000, 'K', 'say', 66559), (92000, 'K', 'anim', 'TALK'),
    (100000, 'F', 'say', 66560), (100000, 'F', 'anim', 'TALK'), (113000, 'K', 'say', 66561), (113000, 'K', 'anim', 'TALK'),
    (116000, 'F', 'say', 66562), (116000, 'F', 'anim', 'TALK'), (128000, 'K', 'say', 66563), (128000, 'K', 'anim', 'TALK'),
    (130000, 'player', 'credit', 60012),
]
SCENES['halister_40562'] = [
    (3000, 'H', 'emote', 66619), (8000, 'H', 'cast', 1449), (8000, 'H', 'summon', [60953, -3750.76, -4438.47, 30.57, 3.08, 61000]), (11000, 'P', 'say', 66582),
    (11000, 'P', 'anim', 'TALK'), (19000, 'H', 'say', 66583), (19000, 'H', 'anim', 'TALK'), (29000, 'P', 'say', 66584),
    (29000, 'P', 'anim', 'TALK'), (39000, 'H', 'say', 66585), (39000, 'H', 'anim', 'TALK'), (45000, 'P', 'say', 66586),
    (45000, 'P', 'anim', 'TALK'), (61000, 'H', 'say', 66587), (61000, 'H', 'anim', 'TALK'), (66000, 'P', 'emote', 66588),
    (66000, 'P', 'anim', 'LAUGH'), (68000, 'P', 'say', 66589), (68000, 'P', 'emote', 66590), (68000, 'P', 'anim', 'TALK'),
    (70000, 'H', 'yell', 66591), (70000, 'H', 'anim', 'TALK'), (76000, 'H', 'emote', 66592), (78000, 'H', 'say', 66593),
    (78000, 'H', 'anim', 'TALK'), (79000, 'player', 'credit', 60389),
]


def npc_text(i, default=None):
    r_ = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)
    if not r_:
        return default
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", r_[0]['b'])[0]
    return r['male_text'] or r['female_text']


_groups = {}


def text_group(entry, bid, chat):
    """one creature_text group per (speaker, Turtle text); 3.3.5 templates use groups 100+"""
    k = (entry, bid, chat)
    if k not in _groups:
        n = sum(1 for k_ in _groups if k_[0] == entry)
        g = (100 if entry in (FALGRAN, GIZZIX, JABBEY) else 0) + n
        S.btext(entry, g, bid, chat)
        _groups[k] = g
    return _groups[k]


def scene(list_id, owner_entry, timeline, who, owner_name, end=(), start=()):
    """a Turtle C++ timeline as one action list run by its owner. who: speaker letter -> creature entry; the owner speaks itself,
    the others are made to speak / animate as the closest creature of their entry (40 yd)"""
    steps, t0 = list(start), 0
    for ms, w, kind, val in timeline:
        d = ms - t0
        t0 = ms
        ent = who.get(w)
        tgt = ('self', []) if ent == owner_entry else ('closest_creature', [ent, 40, 0])
        if kind in ('say', 'yell', 'emote'):
            g = text_group(ent, val, kind)
            act = A(1, [g, 0, 0], tgt[0], tp=tgt[1], note=f"{S.names.get(ent, ent)}: line {val}")
        elif kind == 'anim':
            act = A(5, [ANIM[val]], tgt[0], tp=tgt[1], note=f'Emote {val}')
        elif kind == 'credit':
            act = A(33, [val], 'invoker', note=f'Quest Credit {val}')
        elif kind == 'cast':
            act = S.cast(val, 'self')
        elif kind == 'summon':
            e_, x_, y_, z_, o_, dur_ = val
            act = S.summon(e_, x_, y_, z_, o_, 3, dur_)
        if act is not None:
            steps.append((d, act))
        else:
            t0 -= d
    S.actionlist(list_id, steps + list(end), owner_name)
    return list_id


# ---- Falgran Hastil (the Quagmire): "The Meeting with the Enemy" (40558) / "The Second Meeting" (40564) - his gossip starts the talk
#      with Kagoro; one meeting at a time (Turtle: a 187 s / 105 s controller): the gossip flag is off while they talk
S.mark_stock(FALGRAN)
FM = OFF + 50880
S.gossip(FM, npc_text(50880), [(0, 66774, 0, 0, [(47, 40558, IN_PROGRESS, 0)]), (1, 66774, 0, 0, [(47, 40564, IN_PROGRESS, 0)])])
S.stock_template(FALGRAN, gossip_menu_id=FM, npcflag=3)
for oid_, key_, lid_ in ((0, 'falgran_40558', 508850), (1, 'falgran_40564', 508851)):
    S.row(FALGRAN_G, 0, 62, [FM, oid_], A(72, [], 'invoker', note='Close Gossip'))
    S.row(FALGRAN_G, 0, 62, [FM, oid_], A(83, [1], 'self', note='No gossip while they talk'))
    S.row(FALGRAN_G, 0, 62, [FM, oid_], A(80, [lid_, 0, 0], 'self', note='The meeting (action list)'))
    scene(lid_, FALGRAN, SCENES[key_], {'F': FALGRAN, 'K': KAGORO}, 'Falgran Hastil',
          end=[(0, A(82, [1], 'self', note='Gossip again'))])
# a harmless row of its own keeps the stock "walk away and despawn" script off this spawn
S.row(FALGRAN_G, 0, 11, [], A(82, [1], 'self', note='Respawn: gossip flag'))

# ---- Kagoro: "Next Course of Action" (40718) / "Tedious Diplomacy Once More" (40721) - the talk starts when the quest is accepted
for q_, key_, lid_ in ((40718, 'kagoro_40718', KAGORO * 100 + 1), (40721, 'kagoro_40721', KAGORO * 100 + 2)):
    S.on(KAGORO, 'accepted_quest', A(83, [2], 'self', note='No quests while they talk'),
         A(80, [lid_, 0, 0], 'self', note='The talk (action list)'), ep=[q_])
    scene(lid_, KAGORO, SCENES[key_], {'K': KAGORO, 'F': FALGRAN}, 'Kagoro',
          end=[(0, A(82, [2], 'self', note='Quests again'))])
S.on(KAGORO, 'respawn', A(82, [2], 'self', note='Quest-giver flag'))

# ---- Magus Halister: "Ritual of Divination" (40562) - Paval Reethe's spirit answers (Turtle: unselectable, Arcane Channeling)
rit = [(0, A(18, [NO_SELECT], 'self', note='Not selectable'))]
c_ = S.cast(23017, 'self')
if c_:
    rit.append((0, c_))
S.on(HALISTER, 'accepted_quest', A(80, [HALISTER * 100 + 1, 0, 0], 'self', note='The ritual (action list)'), ep=[40562])
scene(HALISTER * 100 + 1, HALISTER, SCENES['halister_40562'], {'H': HALISTER, 'P': PAVAL}, 'Magus Halister', start=rit,
      end=[(0, A(19, [NO_SELECT], 'self', note='Selectable again')), (0, A(28, [0], 'self', note='Stop channeling'))])
S.on(HALISTER, 'respawn', A(19, [NO_SELECT], 'self', note='Selectable'))

# ---- "Reports of Dustwallow" (40415): the captains' reports
for who_, menu_, it_, line_ in ((CROSS, 60729, 60602, 66726), (HARKER, 60730, 60603, 66727)):
    M_ = OFF + menu_
    S.gossip(M_, npc_text(menu_), [(0, 66725, 0, 0, [(47, 40415, IN_PROGRESS, 0), (2, item(it_), 1, 1)])])
    S.btext(who_, 0, line_)
    S.row(who_, 0, 62, [M_, 0], A(56, [item(it_), 1], 'invoker', note='Give the report'))
    S.row(who_, 0, 62, [M_, 0], S.talk(0))
    S.row(who_, 0, 62, [M_, 0], A(5, [1], 'self', note='Emote Talk'))
    S.row(who_, 0, 62, [M_, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M_}, `npcflag`=`npcflag`|1 WHERE `entry`={who_};")

# ---- "The Shield's Owner" (40554): the three privates
PM = OFF + 60821
S.gossip(PM, 'Greetings, $c.', [(0, 66757, 0, 0, [(47, 40554, IN_PROGRESS, 0)])])
for who_, line_, cr_ in ((TALMAND, 66459, 60385), (SLEIGHTOR, 66460, 60386), (VALNOR, 66461, 60387)):
    S.btext(who_, 0, line_)
    S.row(who_, 0, 62, [PM, 0], S.talk(0))
    S.row(who_, 0, 62, [PM, 0], A(5, [1], 'self', note='Emote Talk'))
    S.row(who_, 0, 62, [PM, 0], A(33, [cr_], 'invoker', note=f'Quest Credit {cr_}'))
    S.row(who_, 0, 62, [PM, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={PM}, `npcflag`=`npcflag`|1 WHERE `entry`={who_};")

# ---- "The Good Snuff" (40411): Jabbey (3.3.5, Gadgetzan) - Turtle gives him a menu with his goods and Groy's package
S.mark_stock(JABBEY)
JM = OFF + 8139
S.gossip(JM, npc_text(8139, 'Greetings, $c.'), [(0, 66720, 1, 0, [], (3, 128)),
                                                 (1, 66721, 0, 0, [(47, 40411, IN_PROGRESS, 0), (2, item(60597), 1, 1)]),
                                                 (2, 66722, 0, 0, [(47, 40466, IN_PROGRESS, 0), (2, item(60670), 1, 1)])])
old_ = q(f"select npcflag from {ctx['AC']}.creature_template where entry=%s", JABBEY)[0]['npcflag']
S.stock_template(JABBEY, gossip_menu_id=JM, npcflag=old_ | 1)
g_ = text_group(JABBEY, 66723, 'say')
S.row(JABBEY, 0, 62, [JM, 1], A(56, [item(60597), 1], 'invoker', note="Give Groy's package"))
S.row(JABBEY, 0, 62, [JM, 1], S.talk(g_))
S.row(JABBEY, 0, 62, [JM, 1], A(5, [1], 'self', note='Emote Talk'))
S.row(JABBEY, 0, 62, [JM, 1], A(72, [], 'invoker', note='Close Gossip'))
# "To Purchase Secret Information" (40466, Burning Steppes - Orvak Sternrock's miners): Jabbey hands over the Arcane Golem Core Information Radgan Deepblaze sent for
g_ = text_group(JABBEY, 66724, 'say')
S.row(JABBEY, 0, 62, [JM, 2], A(56, [item(60670), 1], 'invoker', note='Give the Secret Information'))
S.row(JABBEY, 0, 62, [JM, 2], S.talk(g_))
S.row(JABBEY, 0, 62, [JM, 2], A(5, [1], 'self', note='Emote Talk'))
S.row(JABBEY, 0, 62, [JM, 2], A(72, [], 'invoker', note='Close Gossip'))

# ---- N'ribbi: "The Way Of The Witch Doctor IV" (40352) takes the serum; V (40353) rewarded: the toads cheer (the spell Turtle
#      teaches here is Turtle-only and left out)
NM = OFF + 60631
S.gossip(NM, npc_text(60631), [(0, 66703, 0, 0, [(47, 40352, IN_PROGRESS, 0), (2, item(60509), 1, 0)])])
S.row(NRIBBI, 0, 62, [NM, 0], A(33, [60353], 'invoker', note='Quest Credit 60353'))
S.row(NRIBBI, 0, 62, [NM, 0], A(57, [item(60509), 1], 'invoker', note='Take the serum'))
S.row(NRIBBI, 0, 62, [NM, 0], A(72, [], 'invoker', note='Close Gossip'))
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={NM}, `npcflag`=`npcflag`|1 WHERE `entry`={NRIBBI};")
S.on(NRIBBI, 'reward_quest', A(80, [NRIBBI * 100 + 1, 0, 0], 'self', note='The toads cheer (action list)'), ep=[40353])
scene(NRIBBI * 100 + 1, NRIBBI, [(1000, 'a', 'say', 66704), (3000, 'b', 'say', 66705), (4000, 'c', 'say', 66706),
                                 (5000, 'a', 'say', 66707), (7000, 'b', 'say', 66708)],
      {'N': NRIBBI, 'a': TOADS[0], 'b': TOADS[1], 'c': TOADS[2]}, "N'ribbi")

# ---- Gizzix Grimegurgle (3.3.5, Mudsprocket): "Exquisite Goblin Engineering" (40719) rewarded
S.mark_stock(GIZZIX)
S.on(GIZZIX, 'reward_quest', A(80, [2357050, 0, 0], 'self', note='His words (action list)'), ep=[40719])
scene(2357050, GIZZIX, [(0, 'G', 'say', 66564), (0, 'G', 'anim', 'TALK'), (4000, 'G', 'emote', 66565), (7000, 'G', 'say', 66566),
                        (7000, 'G', 'anim', 'TALK')], {'G': GIZZIX}, 'Gizzix Grimegurgle')

# ---- two NPCs Turtle placed on the very spot of a 3.3.5 NPC (Sergeant Terresa on Lieutenant Nath in Theramore, Private Valnor on
#      Ithania at North Point Tower): moved 2.5 yd to the side of that NPC
for tw_g, stock_ in ((2570880, 23949), (2572942, 17119)):
    s_ = q(f"select position_x x, position_y y, orientation o from {ctx['AC']}.creature where {ctx['cre_id']}=%s limit 1", stock_)[0]
    a_ = s_['o'] + math.pi / 2
    x_, y_ = round(s_['x'] + 2.5 * math.cos(a_), 2), round(s_['y'] + 2.5 * math.sin(a_), 2)
    S.extra_sql.append(f"UPDATE `creature` SET `position_x`={x_}, `position_y`={y_} WHERE `guid`={cguid(tw_g)};")

# ---- two 3.3.5 sea creatures (Muckshell crabs) stood in the bay Turtle raised into Westhaven Hollow: now 3-14 yd under its ground,
#      removed as on Turtle (stock-spawn ground check; the rollback puts them back)
for guid_ in (22596, 22656):
    S.stock_spawn_remove('creature', guid_)

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them): Bloodfen raptors (Need Claws),
#      Darkmist spiders (Balai's Experiment), the Burning Blade of Desolace (Mannoroc Demonic Sigil), Darkfang spiders (Juicy
#      Darkfang Legs!), Mirefin murlocs (The Mirefin Nuisance), Venture Co. in the Barrens (A Strangle Favor), the marsh oozes
#      (Preparation for Divination), Firemane whelps (Exquisite Goblin Engineering), Saltstone basilisks (Willing to Serve)
STOCK_DROPS = S.stock_quest_drops([60583, 60588, 60589, 60592, 60594, 60811, 60816, 60949, 60829])

SQL = S.sql()
