"""Stonetalon Mountains - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) re-expressed as SmartAI.

Quest progress (without these the quests cannot be finished):
- "A Journey for Vengeance" (40691): Grumnir Battlebeard in Bael Hardul tells the story of his brother Darnir when asked
  (npc_grumnir_battlebeard: three lines, then credit 60399).
- "Conflicting Questions" (40698): Faldan Moonshatter by Astranaar (an extra spawn) tells Maloran Oakbranch's envoy what he
  knows of the corruption (npc_faldan_moonshatter: four lines, then credit 60008).
Flavour: the words of Farmer Segwar Ironback (40608), Harlek Vaultshield (40696), Maloran Oakbranch (40698) and Senior
Foreman Nazz Firecracker (40642) when they reward their quests.
Also: Turtle's quest drops on 3.3.5 creatures (STOCK_DROPS).
Gossip menus are the module's own (Turtle text id + 9,000,000). Run by build.py with `S` and `ctx`.
"""
A = S.raw
OFF = 9000000
IN_PROGRESS = 8                       # CONDITION_QUESTSTATE mask: incomplete
GRUMNIR, FALDAN, SEGWAR, HARLEK, MALORAN, NAZZ = 60993, 60471, 61001, 61006, 60998, 61024
S.names.update({GRUMNIR: 'Grumnir Battlebeard', FALDAN: 'Faldan Moonshatter', SEGWAR: 'Farmer Segwar Ironback',
                HARLEK: 'Harlek Vaultshield', MALORAN: 'Maloran Oakbranch', NAZZ: 'Senior Foreman Nazz Firecracker'})
q, TW = ctx['q'], ctx['TW']


def npc_text(i):
    b = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)[0]['b']
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", b)[0]
    return r['male_text'] or r['female_text']


def story(who, quest, option_text, lines, credit, credit_at):
    """a gossip option while `quest` is in progress: the NPC tells his story (lines at Turtle's offsets, ms), then the
    player gets the quest's kill credit. One telling at a time (Turtle: a 48-s controller summon); here the option is
    hidden while the NPC is busy (his gossip flag comes back at the end)."""
    for n_, (_, b_) in enumerate(lines):
        S.btext(who, n_, b_)
    M = OFF + who
    S.gossip(M, npc_text(who), [(0, option_text, 0, 0, [(47, quest, IN_PROGRESS, 0)])])
    S.row(who, 0, 62, [M, 0], A(72, [], 'invoker', note='Close Gossip'))
    S.row(who, 0, 62, [M, 0], A(80, [who * 100 + 1, 0, 0], 'self', note='Tells the story (action list)'))
    steps, t_ = [(0, A(83, [1], 'self', note='Remove gossip flag while telling'))], 0
    for n_, (at_, _) in enumerate(lines):
        steps.append((at_ - t_, S.talk(n_)))
        steps.append((0, A(5, [1], 'self', note='Emote Talk')))
        t_ = at_
    steps.append((credit_at - t_, A(33, [credit], 'invoker', note=f'Quest Credit {credit}')))
    steps.append((0, A(82, [1], 'self', note='Gossip flag back')))
    S.actionlist(who * 100 + 1, steps, S.names[who])
    S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M}, `npcflag`=`npcflag`|1 WHERE `entry`={who};")


# ---- "A Journey for Vengeance" (40691): Grumnir Battlebeard's brother
story(GRUMNIR, 40691, 66775, [(1000, 66517), (13000, 66518), (25000, 66519)], 60399, 33000)
# ---- "Conflicting Questions" (40698): Faldan Moonshatter on the corruption
story(FALDAN, 40698, 66776, [(1000, 66521), (13000, 66522), (27000, 66523), (35000, 66524)], 60008, 39000)

# ---- words on rewarding quests
for who_, quest_, say_, emote_ in ((SEGWAR, 40608, 66464, 1), (HARLEK, 40696, 66520, 4), (MALORAN, 40698, 66525, 1),
                                   (NAZZ, 40642, 66466, 3)):
    S.btext(who_, 10, say_)
    S.on(who_, 'reward_quest', S.talk(10), A(5, [emote_], 'self', note='Emote'), ep=[quest_])

# ---- Turtle's quest drops on 3.3.5 creatures (quest-only loot rows; the rollback removes them)
STOCK_DROPS = S.stock_quest_drops([60310, 60870, 60878, 60936, 60937, 80422])

# ---- 3.3.5 spawns whose ground Turtle raised (stock-spawn ground check): moved up by the rise, as Turtle has them
#      (a Venture Co. Logger by Bael Hardul's road, a Deepmoss Venomspitter and a Wild Steelbloom by Mirkfallon Lake)
for table_, guid_, rise_ in (('creature', 29856, 14.1), ('creature', 29995, 5.6), ('gameobject', 212682, 7.3)):
    z_ = q(f"select position_z z from {ctx['AC']}.{table_} where guid=%s", guid_)[0]['z']
    S.stock_spawn(table_, guid_, position_z=round(z_ + rise_, 3))

SQL = S.sql()
