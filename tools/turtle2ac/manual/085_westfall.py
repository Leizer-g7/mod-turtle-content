"""Westfall - Turtle's quest scripts (src/scripts/miscellaneous/random_scripts_3.cpp) as SmartAI.

The Harvest Golem Mystery (40470-40485, 40529):
- Maltimor Gartside: his lines when "V" (40474) is turned in; the Rewiring ritual of "VII" (40476): he summons a Harvest
  Reaper, it turns hostile for 20 s while he channels, then he calms it and the player gets the credit (Turtle's dummy
  60375, Burning Steppes'). Turtle gives no credit when the reaper died or the player died; here the credit comes at 31 s
  either way (unverified simplification). "Letter from Maltimor" (40529): with the letter he tells his story over four
  pages, takes the letter and gives the credit (dummy 60381).
- Franklin Hamar (Lakeshire, 3.3.5): reads the note aloud when "XIII" (40482) is turned in.
- Farad Wrightsow and Gazzirik (Duskwood shack, spawned by this zone): "XVI" (40485) - Farad's three-page talk ends with
  "<Attack.>": both turn hostile (their faction comes back when they reset).
The Old Church of Westfall (40593-40603):
- Brother Neals (Northshire, 3.3.5): "V" (40597) - his story over four pages gives the credit (dummy 60392).
- Gryan Stoutmantle (3.3.5): accepting "XI" (40603) hands over the Letter and the Westfall Church Key (Turtle drops the
  quest when the bags are full; here the items are just not given then).
Captain Grayson (3.3.5): "Captain Grayson's Revenge" (40396) turned in - Cookie's ghost appears, sighs, and Grayson says
farewell; afterwards Grayson has a "What was Cookie to you?" page.
3.3.5 spawns: the Defias Highwayman whose spot Carver Molsen takes in Turtle goes; a Peacebloom and a Copper Vein at
Gartside Plot are lifted onto the new ground (the rollback puts them back).
Turtle's quest drops on 3.3.5 creatures: Animation Runes on Westfall's harvest golems, Moonlight Silk on Duskwood spiders,
Greater Tarantula Venom on Greater Tarantulas.
Run by build.py with `S` and `ctx`.
"""
A, item, q, TW, AC = S.raw, ctx['item'], ctx['q'], ctx['TW'], ctx['AC']
OFF = 9000000
IN_PROGRESS, REWARDED = 8, 0
MALTIMOR, REAPER, FRANKLIN, FARAD, GAZZIRIK, NEALS, GRYAN, GRAYSON, COOKIE = 60858, 60871, 3091, 60854, 60859, 952, 234, 392, 60709
S.names.update({MALTIMOR: 'Maltimor Gartside', REAPER: 'Harvest Reaper', FRANKLIN: 'Franklin Hamar', FARAD: 'Farad Wrightsow',
                GAZZIRIK: 'Gazzirik', NEALS: 'Brother Neals', GRYAN: 'Gryan Stoutmantle', GRAYSON: 'Captain Grayson', COOKIE: 'Cookie'})
TALK, WAVE, CHEER, ATTACK1H, STATE_WORK = 1, 3, 4, 36, 173
NOT_SELECTABLE = 0x2000000


def npc_text(i, default=None):
    r_ = q(f"select BroadcastTextID0 b from {TW}.npc_text where ID=%s", i)
    if not r_:
        return default
    r = q(f"select male_text, female_text from {TW}.broadcast_text where entry=%s", r_[0]['b'])[0]
    return r['male_text'] or r['female_text']


def emote(e, tgt='self', tp=()):
    return A(5, [e], tgt, tp, note=f'Emote {e}')


def pages(texts, option_text):
    """Turtle's C++ story pages: menus OFF + text id, each with one option leading to the next. -> the last menu id"""
    ids = [OFF + t for t in texts]
    for k, m_ in enumerate(ids):
        nxt = ids[k + 1] if k + 1 < len(ids) else None
        S.gossip(m_, npc_text(texts[k]), [(0, option_text, 0, nxt, [])] if nxt else [])
    return ids


def stock_ai(entry, **extra):
    """a 3.3.5 NPC this script gives events to: SmartAI (and the extra columns), texts in groups 100+"""
    S.mark_stock(entry)
    old_ = q(f"select AIName, ScriptName, npcflag from {AC}.creature_template where entry=%s", entry)[0]
    assert not old_['ScriptName'], f'{entry} has a C++ script in 3.3.5'
    S.stock_template(entry, AIName='SmartAI', **extra)
    return old_


# ---------------------------------------------------------------- Maltimor Gartside
for g_, b_ in enumerate((66434, 66435, 66436, 66437, 66438)):
    S.btext(MALTIMOR, g_, b_)
S.btext(MALTIMOR, 5, 66739, 'emote')
# "V" (40474) turned in
S.row(MALTIMOR, 0, 20, [40474], A(80, [MALTIMOR * 100 + 1, 0, 0], 'self', note='Reads the blueprints (action list)'))
S.actionlist(MALTIMOR * 100 + 1, [(0, S.talk(5)), (0, S.talk(0)), (0, emote(TALK)),
                                  (5000, S.talk(1)), (0, emote(TALK)),
                                  (5000, S.talk(2)), (0, emote(TALK)),
                                  (5000, emote(CHEER))], 'Maltimor Gartside - Blueprints')
# "VII" (40476) accepted: the Rewiring ritual
S.row(MALTIMOR, 0, 19, [40476], A(80, [MALTIMOR * 100 + 2, 0, 0], 'self', note='Rewiring ritual (action list)'))
REAPER_AT = (-10279.18, 1920.43, 34.23, 3.99)
S.actionlist(MALTIMOR * 100 + 2, [
    (0, A(18, [NOT_SELECTABLE], 'self', note='Not selectable during the ritual')),
    (0, A(17, [STATE_WORK], 'self', note='Works on the golem')),
    (5000, A(17, [0], 'self', note='Stops working')),
    (0, S.summon(REAPER, *REAPER_AT, kind=2, duration=30000)),
    (4000, S.talk(3)), (0, emote(TALK)),
    (1000, A(11, [13540, 0], 'self', note='Cast 13540 Green Channeling')),
    (0, A(2, [14], 'closest_creature', [REAPER, 30, 0], note='The reaper turns hostile')),
    (0, emote(ATTACK1H, 'closest_creature', [REAPER, 30, 0])),
    (20000, A(11, [24171, 2], 'self', note='Cast 24171 Resurrection Impact Visual (the spell lands)')),
    (0, A(2, [35], 'closest_creature', [REAPER, 30, 0], note='The reaper is calm again')),
    (0, A(24, [], 'closest_creature', [REAPER, 30, 0], note='The reaper stops fighting')),
    (1000, S.talk(4)), (0, emote(TALK)),
    (0, A(19, [NOT_SELECTABLE], 'self', note='Selectable again')),
    (0, A(33, [60375], 'invoker', note="Quest Credit 60375 (the Rewiring)"))], 'Maltimor Gartside - Rewiring')
S.on(REAPER, 'summoned', A(8, [1], 'self', note='Defensive until the ritual turns it'))
# "Letter from Maltimor" (40529): the letter, four pages, credit
M_MALT = 41162                                      # his Turtle gossip menu (text 60858), built by the zone
malt_pages = pages((30066, 30067, 30068, 30069), 66741)
S.extra_sql.append(
    f"DELETE FROM `gossip_menu_option` WHERE `MenuID`={M_MALT} AND `OptionID`=0;\n"
    f"DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId`=15 AND `SourceGroup`={M_MALT};\n"
    "INSERT INTO `gossip_menu_option` (`MenuID`, `OptionID`, `OptionIcon`, `OptionText`, `OptionBroadcastTextID`, `OptionType`, "
    "`OptionNpcFlag`, `ActionMenuID`, `ActionPoiID`, `BoxCoded`, `BoxMoney`, `BoxText`, `BoxBroadcastTextID`, `VerifiedBuild`) "
    f"VALUES ({M_MALT}, 0, 0, '<Hand him the letter.>', 0, 1, 1, {malt_pages[0]}, 0, 0, 0, NULL, 0, 0);\n"
    "INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`, `ConditionTypeOrReference`, "
    "`ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`, `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES "
    f"(15, {M_MALT}, 0, 0, 0, 47, 0, 40529, {IN_PROGRESS}, 0, 0, 0, 0, '', 'mod-turtle-content: Maltimor - Letter from Maltimor in progress'),\n"
    f"(15, {M_MALT}, 0, 0, 0, 2, 0, {item(60767)}, 1, 0, 0, 0, 0, '', 'mod-turtle-content: Maltimor - carries the letter');")
S.row(MALTIMOR, 0, 62, [malt_pages[2], 0], A(57, [item(60767), 1], 'invoker', note='Takes the letter'))
S.row(MALTIMOR, 0, 62, [malt_pages[2], 0], A(33, [60381], 'invoker', note='Quest Credit 60381 (Letter from Maltimor)'))

# ---------------------------------------------------------------- Franklin Hamar (Lakeshire): "XIII" (40482)
stock_ai(FRANKLIN)
S.btext(FRANKLIN, 100, 66742, 'emote')
for g_, b_ in enumerate((66439, 66440, 66441, 66442, 66443)):
    S.btext(FRANKLIN, 101 + g_, b_)
S.row(FRANKLIN, 0, 20, [40482], A(80, [FRANKLIN * 100 + 1, 0, 0], 'self', note='Reads the note (action list)'))
steps_ = [(0, S.talk(100))]
for k_ in range(5):
    steps_ += [(0 if k_ == 0 else 8000, S.talk(101 + k_)), (0, emote(TALK))]
S.actionlist(FRANKLIN * 100 + 1, steps_, 'Franklin Hamar - The note')

# ---------------------------------------------------------------- Farad Wrightsow and Gazzirik: "XVI" (40485)
M_FARAD = OFF + FARAD
farad_pages = [OFF + 30024, OFF + 30025]
S.gossip(farad_pages[1], npc_text(30025), [(0, 66745, 0, 0, [])])
S.gossip(farad_pages[0], npc_text(30024), [(0, 66744, 0, farad_pages[1], [])])
S.gossip(M_FARAD, npc_text(FARAD, 'Greetings.'), [(0, 66743, 0, farad_pages[0], [(47, 40485, IN_PROGRESS, 0)])])
S.extra_sql.append(f"UPDATE `creature_template` SET `gossip_menu_id`={M_FARAD}, `npcflag`=`npcflag`|1 WHERE `entry`={FARAD};")
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(72, [], 'invoker', note='Close Gossip'))
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(2, [14], 'self', note='Turns hostile'))
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(2, [14], 'closest_creature', [GAZZIRIK, 75, 0], note='Gazzirik turns hostile'))
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(49, [], 'invoker', note='Attacks'))
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(5, [ATTACK1H], 'self', note='Emote attack'))
for who_ in (FARAD, GAZZIRIK):
    S.on(who_, 'reset', A(2, [0], 'self', note='Faction back'))
S.on(GAZZIRIK, 'data', A(49, [], 'closest_player', [75], note='Attacks the nearest player'), ep=(1, 1))
S.row(FARAD, 0, 62, [farad_pages[1], 0], A(45, [1, 1], 'closest_creature', [GAZZIRIK, 75, 0], note='Tells Gazzirik to attack'))

# ---------------------------------------------------------------- Brother Neals (Northshire): "The Old Church of Westfall V" (40597)
old_ = stock_ai(NEALS)
M_NEALS = OFF + NEALS
neals_pages = pages((30062, 30063, 30064, 30065), 66761)
S.gossip(M_NEALS, npc_text(NEALS, 'Greetings, $c.'), [(0, 66760, 0, neals_pages[0], [(47, 40597, IN_PROGRESS, 0)])])
S.stock_template(NEALS, gossip_menu_id=M_NEALS, npcflag=old_['npcflag'] | 1)
S.row(NEALS, 0, 62, [neals_pages[2], 0], A(33, [60392], 'invoker', note="Quest Credit 60392 (Brother Neals' story)"))

# ---------------------------------------------------------------- Gryan Stoutmantle: "The Old Church of Westfall XI" (40603)
S.mark_stock(GRYAN)
for it_, nm_ in ((60842, 'the Letter'), (60846, 'the Westfall Church Key')):
    S.row(GRYAN, 0, 19, [40603], A(56, [item(it_), 1], 'invoker', note=f'Give {nm_}'))

# ---------------------------------------------------------------- Captain Grayson: "Captain Grayson's Revenge" (40396)
old_ = stock_ai(GRAYSON)
S.btext(GRAYSON, 100, 66423)
S.btext(COOKIE, 0, 66421, 'emote')
S.btext(COOKIE, 1, 66422)
S.row(GRAYSON, 0, 20, [40396], S.summon(COOKIE, -11410.70, 1966.56, 10.60, 6.12, kind=3, duration=7500))
S.row(GRAYSON, 0, 20, [40396], A(80, [GRAYSON * 100 + 1, 0, 0], 'self', note='Farewell (action list)'))
S.actionlist(GRAYSON * 100 + 1, [(9000, S.talk(100)), (0, emote(WAVE))], 'Captain Grayson - Farewell')
S.on(COOKIE, 'summoned', A(80, [COOKIE * 100 + 1, 0, 0], 'self', note='Sighs (action list)'))
S.actionlist(COOKIE * 100 + 1, [(5000, S.talk(0)), (0, S.talk(1))], 'Cookie - Ghost')
M_GRAY = OFF + GRAYSON
S.gossip(OFF + 30019, npc_text(30019))
S.gossip(M_GRAY, npc_text(GRAYSON, 'Greetings.'), [(0, 66717, 0, OFF + 30019, [(8, 40396, 0, 0)])])
S.stock_template(GRAYSON, gossip_menu_id=M_GRAY, npcflag=old_['npcflag'] | 1)

# ---------------------------------------------------------------- 3.3.5 spawns where Turtle changed things
S.stock_spawn_remove('creature', 90395)            # Defias Highwayman: Turtle put Carver Molsen on his spot at the Dead Acre
S.stock_spawn('gameobject', 207130, position_z=34.5)   # Peacebloom at Gartside Plot, on the new ground
S.stock_spawn('gameobject', 207477, position_z=36.0)   # Copper Vein at Gartside Plot, on the new ground

# ---------------------------------------------------------------- Turtle's quest drops on 3.3.5 creatures
STOCK_DROPS = S.stock_quest_drops([60676, 60677, 60688, 60839])

SQL = S.sql()
