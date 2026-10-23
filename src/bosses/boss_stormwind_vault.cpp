/*
 * mod-turtle-content - Stormwind Vault (map 35, level 60 dungeon).
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/stormwind_vaults:
 *  - boss_black_bride.cpp, boss_volkan_cruelblade.cpp, boss_thamgrarr.cpp,
 *    boss_aszosh_grimflame.cpp, boss_damian_the_ripper.cpp, boss_arctiras.cpp
 *  - instance_stormwind_vaults.cpp: the Vault Door and the rat trap.
 *    (The Maddened Vault Guard aggro lines are SmartAI rows in
 *    mod_turtle_906_stormwind_vault.sql.)
 *  - boss_nazorna.cpp is not ported: Nazorna (80830) has no spawn on Turtle.
 *
 * The bosses keep Turtle's event queues (same timers, same "one event every
 * N ms" pacing, same retry after 400 ms) on AzerothCore's EventMap.
 *
 * Vault Door (4000509): Turtle opens it when Black Bride, Tham'Grarr, Aszosh,
 * Damian or Arc'tiras dies, closes it when Arc'tiras is pulled and opens it
 * again when he resets. (Turtle's instance script tests the creature entries
 * instead of the dead boss, so in practice the first of these bosses to die
 * opens the door: that live behaviour is what is ported.)
 *
 * Spells: all the same in both cores except
 *  - Damian's Backstab (Turtle 46320, custom damage) -> 72427 Backstab, same damage;
 *  - Damian's Gouge (11286): 75 damage on Turtle, 93 in 3.3.5 -> set to 75;
 *  - Tham'Grarr's Ice Block (Turtle 11958 = 27619 in 3.3.5).
 * Tham'Grarr and Aszosh get 50000 mana from Turtle's script, and Turtle's creatures
 * ignore rage/energy costs: Volkan, Tham'Grarr, Aszosh and Damian cast without power cost here.
 */

#include "turtle_boss_common.h"
#include "Chat.h"
#include "GameObject.h"
#include "GameObjectAI.h"
#include "Group.h"
#include "Map.h"
#include "ScriptMgr.h"
#include "WorldPacket.h"
#include <unordered_set>

using namespace TurtleBoss;

namespace
{
    constexpr uint32 MAP_STORMWIND_VAULT = 35;

    enum VaultCreatures
    {
        NPC_HUNGRY_VAULT_RAT    = 93106,
        NPC_BLACK_BRIDE         = 80850,
        NPC_VOLKAN_CRUELBLADE   = 80851,
        NPC_THAMGRARR           = 80852,
        NPC_ASZOSH_GRIMFLAME    = 80853,
        NPC_DAMIAN              = 80854,
        NPC_ARCTIRAS            = 93107,
        NPC_FRIGID_GUARDIAN     = 60612,
        NPC_RISEN_LACKEY        = 10482,
    };

    enum VaultObjects
    {
        GO_RAT_TRAP             = 3000273,
        GO_RAT_DOOR_ONE         = 3000275,
        GO_RAT_DOOR_TWO         = 3000276,
        GO_VAULT_DOOR           = 4000509,
        GO_OBSTRUCTION          = 2004982,   // Turtle spawn 5001265 (ice block in front of the armory)
        GO_OBSTRUCTION_DECOR    = 2010591,   // Turtle spawn 5001289
        GO_VAULT_ARMORY         = 2010867,
    };

    // ---- chat helpers (Turtle MonsterSendTextToZone / MonsterTextEmote / MonsterWhisper) ----
    void ZoneText(Creature* c, ChatMsg type, char const* text, char const* name = nullptr)
    {
        if (!c || !c->GetMap())
            return;
        WorldPacket data;
        ChatHandler::BuildChatPacket(data, type, LANG_UNIVERSAL, c->GetGUID(), ObjectGuid::Empty, text, 0, name ? name : c->GetName());
        c->GetMap()->SendToPlayers(&data);
    }

    void ZoneYell(Creature* c, char const* text, char const* name = nullptr) { ZoneText(c, CHAT_MSG_MONSTER_YELL, text, name); }
    void ZoneSay(Creature* c, char const* text, char const* name = nullptr) { ZoneText(c, CHAT_MSG_MONSTER_SAY, text, name); }
    void BossEmote(Creature* c, char const* text) { ZoneText(c, CHAT_MSG_RAID_BOSS_EMOTE, text); }

    void BossWhisper(Creature* c, Player* to, char const* text)
    {
        if (!c || !to)
            return;
        WorldPacket data;
        ChatHandler::BuildChatPacket(data, CHAT_MSG_RAID_BOSS_WHISPER, LANG_UNIVERSAL, c->GetGUID(), to->GetGUID(), text, 0, c->GetName(), to->GetName());
        to->SendDirectMessage(&data);
    }

    // Turtle ScriptedAI::GetRandomPlayerInRange: a living player of the map within range.
    Player* RandomPlayerInRange(Creature* me, float range, std::list<Player*> const* except = nullptr)
    {
        std::vector<Player*> players;
        for (auto const& itr : me->GetMap()->GetPlayers())
        {
            Player* p = itr.GetSource();
            if (!p || !p->IsAlive() || p->IsGameMaster() || !me->IsWithinDistInMap(p, range))
                continue;
            if (except && std::find(except->begin(), except->end(), p) != except->end())
                continue;
            players.push_back(p);
        }
        return players.empty() ? nullptr : Acore::Containers::SelectRandomContainerElement(players);
    }

    // Instances whose Vault Door a boss death has opened (the map has no
    // InstanceScript, so AzerothCore would not remember it).
    std::unordered_set<uint32>& OpenedVaults()
    {
        static std::unordered_set<uint32> opened;
        return opened;
    }

    void SetVaultDoor(Creature* me, bool open, bool bossKilled = false)
    {
        if (!me || me->GetMapId() != MAP_STORMWIND_VAULT)
            return;
        if (bossKilled)
            OpenedVaults().insert(me->GetInstanceId());
        if (GameObject* door = me->FindNearestGameObject(GO_VAULT_DOOR, 400.0f))
            door->SetGoState(open ? GO_STATE_ACTIVE : GO_STATE_READY);
    }

    // Base for the event-queue bosses: Turtle pops at most one event every
    // _minimumTicksBetweenEvents ms and melees on the other ticks.
    struct VaultBossAI : public TurtleBossAI
    {
        explicit VaultBossAI(Creature* c) : TurtleBossAI(c) { }

        EventMap _queue;
        uint32 _lastUpdateTick = 0;
        uint32 _lastEventProcessedAt = 0;
        uint32 _minimumTicksBetweenEvents = 0;

        void StartQueue(uint32 minimumTicks)
        {
            _lastUpdateTick = 0;
            _lastEventProcessedAt = 0;
            _minimumTicksBetweenEvents = minimumTicks;
            _queue.Reset();
        }

        uint32 PopEvent()
        {
            if (_lastUpdateTick - _lastEventProcessedAt < _minimumTicksBetweenEvents)
                return 0;
            uint32 e = _queue.ExecuteEvent();
            if (e)
                _lastEventProcessedAt = _lastUpdateTick;
            return e;
        }

        bool Casting() const { return me->IsNonMeleeSpellCast(false); }
        void Retry() { _queue.Repeat(400ms); }

        // Spells with a mana cost on bosses Turtle gives 50000 mana.
        void CastFree(Unit* target, uint32 spellId)
        {
            if (target)
                me->CastSpell(target, spellId, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST);
        }
    };

    // ------------------------------------------------------------------
    // Black Bride
    // ------------------------------------------------------------------
    struct boss_black_brideAI : public VaultBossAI
    {
        explicit boss_black_brideAI(Creature* c) : VaultBossAI(c) { }

        enum { SPELL_LICH_SLAP = 28873, SPELL_SCREAMS_OF_THE_PAST = 7074, SPELL_SHADOW_BOLT_VOLLEY = 17228 };
        enum { EVENT_LICH_SLAP = 1, EVENT_SCREAMS, EVENT_VOLLEY };

        void JustEngagedWith(Unit* /*who*/) override
        {
            StartQueue(2000);
            _queue.ScheduleEvent(EVENT_LICH_SLAP, 16s, 18s);
            _queue.ScheduleEvent(EVENT_SCREAMS, 6s);
            _queue.ScheduleEvent(EVENT_VOLLEY, 10s);
            ZoneYell(me, "Come and meet your end.");
        }

        void JustDied(Unit* /*killer*/) override
        {
            ZoneSay(me, "D-Damien, my.. my love.");
            SetVaultDoor(me, true, true);
        }

        void UpdateAI(uint32 diff) override
        {
            _lastUpdateTick += diff;
            if (!UpdateVictim())
                return;
            _queue.Update(diff);

            switch (PopEvent())
            {
                case EVENT_LICH_SLAP:
                    if (Casting()) { Retry(); break; }
                    DoCastVictim(SPELL_LICH_SLAP);
                    ZoneYell(me, "Your touch defiles me, I am only his!");
                    _queue.ScheduleEvent(EVENT_LICH_SLAP, 16s, 18s);
                    break;
                case EVENT_SCREAMS:
                    if (Casting()) { Retry(); break; }
                    DoCastVictim(SPELL_SCREAMS_OF_THE_PAST);
                    ZoneYell(me, "I would've done anything for your love.");
                    _queue.ScheduleEvent(EVENT_SCREAMS, 20s);
                    break;
                case EVENT_VOLLEY:
                    if (Casting()) { Retry(); break; }
                    DoCastVictim(SPELL_SHADOW_BOLT_VOLLEY);
                    ZoneYell(me, "Infidels!");
                    _queue.ScheduleEvent(EVENT_VOLLEY, 15s);
                    break;
                default:
                    DoMeleeAttackIfReady();
                    break;
            }
        }
    };

    // ------------------------------------------------------------------
    // Volkan Cruelblade
    // ------------------------------------------------------------------
    struct boss_volkan_cruelbladeAI : public VaultBossAI
    {
        explicit boss_volkan_cruelbladeAI(Creature* c) : VaultBossAI(c) { }

        enum { SPELL_BLINK_VISUAL = 7141, SPELL_BLOODLUST = 23951, SPELL_THUNDER_CLAP = 23931, SPELL_BLADESTORM = 9632 };
        enum { EVENT_BLINK = 1, EVENT_BLOODLUST, EVENT_THUNDER_CLAP, EVENT_BLADESTORM };

        uint8 _bloodlustPhase = 0;   // 70%, 40%, 10%, done
        bool _bladestorming = false;

        void JustEngagedWith(Unit* /*who*/) override
        {
            StartQueue(2000);
            _bloodlustPhase = 0;
            _bladestorming = false;
            _queue.ScheduleEvent(EVENT_BLINK, 10s);
            _queue.ScheduleEvent(EVENT_BLOODLUST, 400ms);
            _queue.ScheduleEvent(EVENT_THUNDER_CLAP, 15s, 40s);
            _queue.ScheduleEvent(EVENT_BLADESTORM, 400ms);
            ZoneYell(me, "I will be a prisoner no longer!");
        }

        void JustDied(Unit* /*killer*/) override { ZoneSay(me, "Lok'tar... *whimper* ...O-Ogar..."); }

        void Blink()
        {
            if (Casting())
                me->InterruptNonMeleeSpells(false);

            // Turtle: never the tank, unless he ran away during Bladestorm.
            std::list<Player*> except;
            if (Player* tank = me->GetVictim()->ToPlayer())
                if (!_bladestorming)
                    except.push_back(tank);

            Player* player = RandomPlayerInRange(me, 40.0f, &except);
            if (!player)
            {
                _queue.ScheduleEvent(EVENT_BLINK, 2s);
                return;
            }

            Position behind = player->GetNearPosition(2.5f, float(M_PI));
            DoCastAOE(SPELL_BLINK_VISUAL, true);
            ZoneYell(me, "Behind you!");
            me->NearTeleportTo(behind.GetPositionX(), behind.GetPositionY(), behind.GetPositionZ(), player->GetOrientation());
            DoResetThreatList();
            AttackStart(player);
            me->GetThreatMgr().AddThreat(player, 300.0f);
            _queue.ScheduleEvent(EVENT_BLINK, 30s);
        }

        void UpdateAI(uint32 diff) override
        {
            _lastUpdateTick += diff;
            if (!UpdateVictim())
                return;
            _queue.Update(diff);

            switch (PopEvent())
            {
                case EVENT_BLINK:
                    Blink();
                    break;
                case EVENT_BLOODLUST:
                {
                    static float const thresholds[3] = { 70.0f, 40.0f, 10.0f };
                    if (_bloodlustPhase >= 3 || me->GetHealthPct() > thresholds[_bloodlustPhase]) { Retry(); break; }
                    CastFree(me, SPELL_BLOODLUST);
                    static char const* const lines[3] = { "Feel the heat of the Burning Blade!", "I will see you fall! Trk'hsk!", "Lok'tar Ogar!" };
                    ZoneYell(me, lines[_bloodlustPhase]);
                    if (++_bloodlustPhase < 3)
                        _queue.ScheduleEvent(EVENT_BLOODLUST, 15s);
                    break;
                }
                case EVENT_THUNDER_CLAP:
                    CastFree(me, SPELL_THUNDER_CLAP);
                    _queue.ScheduleEvent(EVENT_THUNDER_CLAP, 90s, 120s);
                    break;
                case EVENT_BLADESTORM:
                    if (me->GetHealthPct() > 5.0f || Casting()) { Retry(); break; }
                    // Bladestorm until death: only Bladestorm from now on.
                    _queue.Reset();
                    _minimumTicksBetweenEvents = 0;
                    if (!_bladestorming)
                    {
                        ZoneYell(me, "Feel the wrath of the Cruelblade!");
                        _bladestorming = true;
                    }
                    CastFree(me, SPELL_BLADESTORM);
                    _queue.ScheduleEvent(EVENT_BLADESTORM, 400ms);
                    break;
                default:
                    DoMeleeAttackIfReady();
                    break;
            }
        }
    };

    // ------------------------------------------------------------------
    // Tham'Grarr (two heads: "Tham" and "Grarr" speak in turn)
    // ------------------------------------------------------------------
    struct boss_thamgrarrAI : public VaultBossAI
    {
        explicit boss_thamgrarrAI(Creature* c) : VaultBossAI(c) { }

        enum { SPELL_FIREBALL = 25306, SPELL_KNOCK_AWAY = 18670, SPELL_ICE_BLOCK = 27619, SPELL_RAIN_OF_FIRE = 19717 };
        enum { EVENT_RAIN_OF_FIRE = 1, EVENT_FIREBALL, EVENT_KNOCK_AWAY, EVENT_ICE_BLOCK };
        enum
        {
            TEXT_AGGRO_THAM = 1, TEXT_AGGRO_GRARR, TEXT_RAIN_THAM, TEXT_RAIN_GRARR,
            TEXT_KNOCK_THAM, TEXT_KNOCK_GRARR, TEXT_ICE_THAM, TEXT_ICE_GRARR
        };

        EventMap _text;
        uint32 _lastTextEventProcessedAt = 0;
        bool _iceBlockDone = false;

        void JustEngagedWith(Unit* /*who*/) override
        {
            StartQueue(4000);
            _iceBlockDone = false;
            _queue.ScheduleEvent(EVENT_RAIN_OF_FIRE, 6s);
            _queue.ScheduleEvent(EVENT_FIREBALL, 10s);
            _queue.ScheduleEvent(EVENT_KNOCK_AWAY, 12s, 14s);
            _queue.ScheduleEvent(EVENT_ICE_BLOCK, 400ms);

            _lastTextEventProcessedAt = 0;
            _text.Reset();
            Lines(TEXT_AGGRO_THAM, TEXT_AGGRO_GRARR);
        }

        void JustDied(Unit* /*killer*/) override { SetVaultDoor(me, true, true); }

        void Lines(uint32 tham, uint32 grarr)
        {
            _text.ScheduleEvent(tham, 0ms);
            _text.ScheduleEvent(grarr, 0ms);
        }

        void UpdateText(uint32 diff)
        {
            _text.Update(diff);
            if (_lastUpdateTick - _lastTextEventProcessedAt < 1250)
                return;
            uint32 e = _text.ExecuteEvent();
            if (!e)
                return;
            _lastTextEventProcessedAt = _lastUpdateTick;

            switch (e)
            {
                case TEXT_AGGRO_THAM:  ZoneSay(me, "Finally, something to amuse me.", "Tham"); break;
                case TEXT_AGGRO_GRARR: ZoneYell(me, "Kill them, kill them all!", "Grarr"); break;
                case TEXT_RAIN_THAM:   ZoneSay(me, "Death comes from above.", "Tham"); break;
                case TEXT_RAIN_GRARR:  ZoneYell(me, "Grarr sees puny people dance! Dance more for Grarr!", "Grarr"); break;
                case TEXT_KNOCK_THAM:  ZoneSay(me, "You're making me angry!", "Tham"); break;
                case TEXT_KNOCK_GRARR: ZoneYell(me, "Back, stay back!", "Grarr"); break;
                case TEXT_ICE_THAM:    ZoneYell(me, "I will not fail!", "Tham"); break;
                case TEXT_ICE_GRARR:   ZoneSay(me, "Grarr starting to feel cold...", "Grarr"); break;
                default: break;
            }
        }

        void UpdateAI(uint32 diff) override
        {
            _lastUpdateTick += diff;
            if (!UpdateVictim())
                return;
            _queue.Update(diff);

            switch (PopEvent())
            {
                case EVENT_RAIN_OF_FIRE:
                    if (Casting()) { Retry(); break; }
                    CastFree(me->GetVictim(), SPELL_RAIN_OF_FIRE);
                    Lines(TEXT_RAIN_THAM, TEXT_RAIN_GRARR);
                    _queue.ScheduleEvent(EVENT_RAIN_OF_FIRE, 18s, 20s);
                    break;
                case EVENT_FIREBALL:
                {
                    if (Casting()) { Retry(); break; }
                    Player* target = RandomPlayerInRange(me, 30.0f);
                    if (!target)
                    {
                        _queue.ScheduleEvent(EVENT_FIREBALL, 400ms);
                        break;
                    }
                    CastFree(target, SPELL_FIREBALL);
                    _queue.ScheduleEvent(EVENT_FIREBALL, 10s);
                    break;
                }
                case EVENT_KNOCK_AWAY:
                    if (Casting()) { Retry(); break; }
                    CastFree(me->GetVictim(), SPELL_KNOCK_AWAY);
                    Lines(TEXT_KNOCK_THAM, TEXT_KNOCK_GRARR);
                    _queue.ScheduleEvent(EVENT_KNOCK_AWAY, 12s, 14s);
                    break;
                case EVENT_ICE_BLOCK:
                    if (Casting() || _iceBlockDone || me->GetHealthPct() > 10.0f) { Retry(); break; }
                    CastFree(me, SPELL_ICE_BLOCK);
                    _iceBlockDone = true;
                    Lines(TEXT_ICE_THAM, TEXT_ICE_GRARR);
                    break;
                default:
                    DoMeleeAttackIfReady();
                    break;
            }

            UpdateText(diff);
        }
    };

    // ------------------------------------------------------------------
    // Aszosh Grimflame
    // ------------------------------------------------------------------
    struct boss_aszosh_grimflameAI : public VaultBossAI
    {
        explicit boss_aszosh_grimflameAI(Creature* c) : VaultBossAI(c) { }

        enum { SPELL_RISEN_LACKEY = 17618, SPELL_MIND_BLAST = 10947, SPELL_DRAIN_LIFE = 11700, SPELL_CORRUPTION = 18656 };
        enum { EVENT_RISEN_LACKEY = 1, EVENT_MIND_BLAST, EVENT_DRAIN_LIFE, EVENT_CORRUPTION };

        uint8 _drainLifePhase = 0;    // 80%, 40%, 20%, done
        uint32 _lastMindBlastHealth = 0;

        void Reset() override
        {
            std::list<Creature*> lackeys;
            me->GetCreatureListWithEntryInGrid(lackeys, NPC_RISEN_LACKEY, 500.0f);
            for (Creature* lackey : lackeys)
                lackey->DespawnOrUnsummon();
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            StartQueue(0);
            _lastMindBlastHealth = me->GetHealth();
            _drainLifePhase = 0;
            _queue.ScheduleEvent(EVENT_CORRUPTION, 15s);
            _queue.ScheduleEvent(EVENT_DRAIN_LIFE, 400ms);
            _queue.ScheduleEvent(EVENT_MIND_BLAST, 400ms);
            _queue.ScheduleEvent(EVENT_RISEN_LACKEY, 400ms);
            ZoneYell(me, "I was amongst the first, and I will claim vengeance for Gul'dan!");
        }

        void JustDied(Unit* /*killer*/) override
        {
            ZoneSay(me, "Your will is not your... *cough* ...own...");
            SetVaultDoor(me, true, true);
        }

        bool LackeyAlive()
        {
            std::list<Creature*> lackeys;
            me->GetCreatureListWithEntryInGrid(lackeys, NPC_RISEN_LACKEY, 500.0f);
            for (Creature* lackey : lackeys)
                if (lackey->IsAlive())
                    return true;
            return false;
        }

        void UpdateAI(uint32 diff) override
        {
            _lastUpdateTick += diff;
            if (!UpdateVictim())
                return;
            _queue.Update(diff);

            switch (PopEvent())
            {
                case EVENT_CORRUPTION:
                {
                    if (Casting()) { Retry(); break; }
                    // Turtle GetNearestVictimInRange(0, 40): the closest enemy within 40 yd.
                    Unit* target = nullptr;
                    float best = 40.0f;
                    for (ThreatReference const* ref : me->GetThreatMgr().GetUnsortedThreatList())
                        if (Unit* u = ref->GetVictim())
                            if (u->IsAlive() && me->GetDistance(u) <= best)
                            {
                                best = me->GetDistance(u);
                                target = u;
                            }
                    if (!target)
                    {
                        _queue.ScheduleEvent(EVENT_CORRUPTION, 400ms);
                        break;
                    }
                    CastFree(target, SPELL_CORRUPTION);
                    if (urand(0, 1))
                        ZoneYell(me, "Feel your blood boil.");
                    _queue.ScheduleEvent(EVENT_CORRUPTION, 30s);
                    break;
                }
                case EVENT_DRAIN_LIFE:
                {
                    static float const thresholds[3] = { 80.0f, 40.0f, 20.0f };
                    if (Casting() || _drainLifePhase >= 3 || me->GetHealthPct() > thresholds[_drainLifePhase]) { Retry(); break; }
                    CastFree(me->GetVictim(), SPELL_DRAIN_LIFE);
                    static char const* const lines[3] = { "Your strength becomes my own!", "I will take everything you have!", "You will serve me soon!" };
                    ZoneYell(me, lines[_drainLifePhase]);
                    if (++_drainLifePhase < 3)
                        _queue.ScheduleEvent(EVENT_DRAIN_LIFE, 400ms);
                    break;
                }
                case EVENT_MIND_BLAST:
                {
                    // Every 5% of max health lost since the last Mind Blast.
                    float healthToLose = me->GetMaxHealth() * 0.05f;
                    if (Casting() || !(float(_lastMindBlastHealth) - healthToLose > float(me->GetHealth()))) { Retry(); break; }
                    CastFree(me->GetVictim(), SPELL_MIND_BLAST);
                    if (urand(0, 1))
                        ZoneYell(me, "Your own mind shall become your enemy.");
                    _lastMindBlastHealth = me->GetHealth();
                    _queue.ScheduleEvent(EVENT_MIND_BLAST, 400ms);
                    break;
                }
                case EVENT_RISEN_LACKEY:
                    if (Casting() || LackeyAlive()) { Retry(); break; }
                    CastFree(me, SPELL_RISEN_LACKEY);
                    if (urand(0, 1))
                        ZoneYell(me, "Rise bones of misery and serve your new master!");
                    _queue.ScheduleEvent(EVENT_RISEN_LACKEY, 400ms);
                    break;
                default:
                    DoMeleeAttackIfReady();
                    break;
            }
        }
    };

    // ------------------------------------------------------------------
    // Damian (the Ripper)
    // ------------------------------------------------------------------
    struct boss_damianAI : public VaultBossAI
    {
        explicit boss_damianAI(Creature* c) : VaultBossAI(c) { }

        enum
        {
            SPELL_BACKSTAB = 72427,           // Turtle 46320
            SPELL_DARK_MENDING = 16588,
            SPELL_GOUGE = 11286,
            SPELL_SINISTER_STRIKE = 11294,
            SPELL_VANISH = 24222,
        };
        enum { EVENT_DARK_MENDING = 1, EVENT_GOUGE, EVENT_SINISTER_STRIKE, EVENT_RIPPERS_MADNESS, EVENT_VANISH };
        static constexpr float GOUGE_DAMAGE = 75.0f;   // Turtle 11286
        static constexpr uint32 VANISH_DURATION = 3000;

        bool _darkMendingDone = false;
        bool _madnessDone = false;
        uint8 _vanishPhase = 0;       // 70%, 40%, 10%, done
        uint32 _vanishedAt = 0;

        void Reset() override
        {
            _vanishedAt = 0;
            me->SetVisible(true);
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            StartQueue(2000);
            _darkMendingDone = false;
            _madnessDone = false;
            _vanishPhase = 0;
            _vanishedAt = 0;
            _queue.ScheduleEvent(EVENT_VANISH, 400ms);
            _queue.ScheduleEvent(EVENT_GOUGE, 15s);
            _queue.ScheduleEvent(EVENT_SINISTER_STRIKE, 10s);
            _queue.ScheduleEvent(EVENT_DARK_MENDING, 400ms);
            _queue.ScheduleEvent(EVENT_RIPPERS_MADNESS, 400ms);
            ZoneYell(me, "What's this, victims fighting their way to me? How thrilling!");
        }

        void JustDied(Unit* /*killer*/) override
        {
            me->SetVisible(true);
            ZoneSay(me, "Rip, RIP, I will rip you apart!");
            SetVaultDoor(me, true, true);
        }

        bool UpdateVanish()
        {
            if (!_vanishedAt)
                return false;

            // Turtle delays the invisibility so players see the animation and the line.
            if (me->IsVisible() && _lastUpdateTick > _vanishedAt + 800)
            {
                me->SetVisible(false);
                return true;
            }
            if (_lastUpdateTick < _vanishedAt + VANISH_DURATION)
                return true;

            Player* player = RandomPlayerInRange(me, 80.0f);
            if (!player)
                return true;

            Position behind = player->GetNearPosition(2.5f, float(M_PI));
            me->NearTeleportTo(behind.GetPositionX(), behind.GetPositionY(), behind.GetPositionZ(), player->GetOrientation());
            DoResetThreatList();
            _vanishedAt = 0;
            me->SetVisible(true);
            AttackStart(player);
            me->GetThreatMgr().AddThreat(player, 300.0f);

            // Turtle: Backstab for all the target's health under 40%, half of it otherwise.
            uint32 damage = player->GetHealthPct() <= 40.0f ? player->GetHealth() : player->GetHealth() / 2;
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_BACKSTAB, EFFECT_0, float(damage)));
            me->CastCustomSpell(SPELL_BACKSTAB, values, player, TRIGGERED_FULL_MASK);
            if (player->GetHealthPct() <= 40.0f || !player->IsAlive())
                ZoneYell(me, "Another one bites the dust.");
            return false;
        }

        void UpdateAI(uint32 diff) override
        {
            _lastUpdateTick += diff;

            if (UpdateVanish())
                return;

            if (!UpdateVictim())
                return;
            _queue.Update(diff);

            switch (PopEvent())
            {
                case EVENT_DARK_MENDING:
                    if (Casting() || _darkMendingDone || me->GetHealthPct() > 5.0f) { Retry(); break; }
                    CastFree(me, SPELL_DARK_MENDING);
                    ZoneYell(me, "In pain I find salvation, and so shall you!");
                    _darkMendingDone = true;
                    break;
                case EVENT_GOUGE:
                {
                    if (Casting() || !me->IsWithinMeleeRange(me->GetVictim())) { Retry(); break; }
                    Player* target = RandomPlayerInRange(me, 4.5f);
                    if (!target || !target->HasInArc(float(M_PI), me))
                    {
                        Retry();
                        break;
                    }
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_GOUGE, EFFECT_0, GOUGE_DAMAGE));
                    me->CastCustomSpell(SPELL_GOUGE, values, target, TRIGGERED_FULL_MASK);
                    ZoneYell(me, "You should stay quiet for a while!");
                    _queue.ScheduleEvent(EVENT_GOUGE, 15s);
                    break;
                }
                case EVENT_SINISTER_STRIKE:
                    if (Casting() || me->GetDistance(me->GetVictim()) > 4.5f) { Retry(); break; }
                    CastFree(me->GetVictim(), SPELL_SINISTER_STRIKE);
                    ZoneYell(me, "My blade craves your blood!");
                    _queue.ScheduleEvent(EVENT_SINISTER_STRIKE, 10s);
                    break;
                case EVENT_RIPPERS_MADNESS:
                    if (Casting() || _madnessDone || me->GetHealthPct() > 1.0f) { Retry(); break; }
                    // Turtle "The Ripper's Madness": kills his target outright.
                    if (Unit* victim = me->GetVictim())
                    {
                        Unit::Kill(me, victim);
                        ZoneYell(me, "The Shadow demands justice!");
                        _madnessDone = true;
                    }
                    else
                        Retry();
                    break;
                case EVENT_VANISH:
                {
                    static float const thresholds[3] = { 70.0f, 40.0f, 10.0f };
                    if (Casting() || _vanishPhase >= 3 || me->GetHealthPct() > thresholds[_vanishPhase]) { Retry(); break; }
                    static char const* const lines[3] = { "The shadow's veil embraces me!", "Now you see me, now you don't!", "Think fast, where am I now?" };
                    ZoneYell(me, lines[_vanishPhase]);
                    ++_vanishPhase;
                    _queue.ScheduleEvent(EVENT_VANISH, 400ms);
                    DoCastSelf(SPELL_VANISH, true);
                    me->AttackStop();
                    me->StopMoving();
                    me->GetMotionMaster()->Clear();
                    _vanishedAt = std::max<uint32>(_lastUpdateTick, 1);
                    break;
                }
                default:
                    DoMeleeAttackIfReady();
                    break;
            }
        }
    };

    // ------------------------------------------------------------------
    // Arc'tiras (rooted crystal)
    // ------------------------------------------------------------------
    struct boss_arctirasAI : public TurtleBossAI
    {
        explicit boss_arctirasAI(Creature* c) : TurtleBossAI(c) { }

        enum { SPELL_FROSTBOLT = 17503, SPELL_CAUSE_INSANITY = 12888, SPELL_FROST_NOVA = 30094 };
        enum Stage { STAGE_WAIT_60, STAGE_WAIT_35, STAGE_REST };

        Stage _stage = STAGE_WAIT_60;
        uint32 _frostboltTimer = 3500;
        uint32 _insanityTimer = 16000;
        uint32 _novaTimer = 0;
        bool _nova = false;

        void Reset() override
        {
            summons.DespawnAll();
            _stage = STAGE_WAIT_60;
            _frostboltTimer = 3500;
            _insanityTimer = 16000;
            _nova = false;
            me->SetControlled(true, UNIT_STATE_ROOT);
            me->AddUnitState(UNIT_STATE_CANNOT_TURN);
        }

        void JustEngagedWith(Unit* who) override
        {
            SetVaultDoor(me, false);
            if (Player* player = who ? who->ToPlayer() : nullptr)
                if (Group* group = player->GetGroup())
                    for (GroupReference* itr = group->GetFirstMember(); itr; itr = itr->next())
                        if (Player* member = itr->GetSource())
                            BossWhisper(me, member, "They brought me here in greed, and now they have me locked in absolute terror. This prison will be your frozen tomb.");
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            TurtleBossAI::EnterEvadeMode(why);
            if (OpenedVaults().count(me->GetInstanceId()))
                SetVaultDoor(me, true);
        }

        void JustDied(Unit* /*killer*/) override
        {
            summons.DespawnAll();
            BossEmote(me, "You hear something shatter behind you!");

            // Turtle despawns spawns 5001265 / 5001289 (the ice in front of the armory).
            static Position const ice[2] = { { -46.1388f, 155.504f, -40.7707f, 0.0f }, { -46.3668f, 144.127f, -40.4507f, 0.0f } };
            static uint32 const iceEntry[2] = { GO_OBSTRUCTION, GO_OBSTRUCTION_DECOR };
            for (uint8 i = 0; i < 2; ++i)
            {
                std::list<GameObject*> gos;
                me->GetGameObjectListWithEntryInGrid(gos, iceEntry[i], 200.0f);
                for (GameObject* go : gos)
                    if (go->GetExactDist(&ice[i]) < 3.0f)
                    {
                        go->SetLootState(GO_JUST_DEACTIVATED);
                        go->DespawnOrUnsummon();
                    }
            }

            me->SummonGameObject(GO_VAULT_ARMORY, -46.262f, 179.477f, -40.0506f, 4.72486f, 0.0f, 0.0f, 0.702685f, -0.711501f, 86400);
            SetVaultDoor(me, true, true);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            // GenericSpellMob: triggered casts that ignore line of sight, no melee.
            if (_frostboltTimer <= diff)
            {
                me->CastSpell(me->GetVictim(), SPELL_FROSTBOLT, TRIGGERED_FULL_MASK);
                _frostboltTimer = 3500;
            }
            else
                _frostboltTimer -= diff;

            if (_insanityTimer <= diff)
            {
                if (Unit* target = SelectTarget(SelectTargetMethod::Random, 1))
                    me->CastSpell(target, SPELL_CAUSE_INSANITY, TRIGGERED_FULL_MASK);
                _insanityTimer = 16000;
            }
            else
                _insanityTimer -= diff;

            if (_nova)
            {
                if (_novaTimer <= diff)
                {
                    me->CastSpell(me, SPELL_FROST_NOVA, TRIGGERED_FULL_MASK);
                    _novaTimer = 6500;
                }
                else
                    _novaTimer -= diff;
            }

            float hp = me->GetHealthPct();
            if (_stage == STAGE_WAIT_60 && hp <= 60.0f)
            {
                BossEmote(me, "Arc'tiras vocalizes a chilling chime.");
                for (uint8 i = 0; i < 2; ++i)
                {
                    Position pos = me->GetRandomNearPosition(5.0f);
                    if (Creature* guardian = me->SummonCreature(NPC_FRIGID_GUARDIAN, pos, TEMPSUMMON_TIMED_DESPAWN_OUT_OF_COMBAT, 2000))
                        DoZoneInCombat(guardian);
                }
                _stage = STAGE_WAIT_35;
            }
            else if (_stage == STAGE_WAIT_35 && hp <= 35.0f)
            {
                BossEmote(me, "Arc'tiras is destabilizing!");
                _nova = true;
                _novaTimer = 6500;
                _stage = STAGE_REST;
            }
        }
    };

    // ------------------------------------------------------------------
    // Rat trap (gameobject 3000273): step on it and the doors close on 15 rats.
    // ------------------------------------------------------------------
    struct go_stormwind_vault_rat_trapAI : public GameObjectAI
    {
        explicit go_stormwind_vault_rat_trapAI(GameObject* go) : GameObjectAI(go) { }

        uint32 _step = 0;
        uint32 _timer = 300;

        void SetDoors(bool open)
        {
            for (uint32 entry : { uint32(GO_RAT_DOOR_ONE), uint32(GO_RAT_DOOR_TWO) })
                if (GameObject* door = me->FindNearestGameObject(entry, 20.0f))
                    door->SetGoState(open ? GO_STATE_ACTIVE : GO_STATE_READY);
        }

        Player* PlayerOnTrap() const
        {
            Player* found = nullptr;
            float best = 5.0f;
            for (auto const& itr : me->GetMap()->GetPlayers())
                if (Player* p = itr.GetSource())
                    if (p->IsAlive() && !p->IsGameMaster() && me->GetDistance(p) <= best)
                    {
                        best = me->GetDistance(p);
                        found = p;
                    }
            return found;
        }

        void UpdateAI(uint32 diff) override
        {
            if (_timer > diff)
            {
                _timer -= diff;
                return;
            }
            if (me->GetMapId() != MAP_STORMWIND_VAULT)
            {
                _timer = HOUR * IN_MILLISECONDS;
                return;
            }

            switch (_step)
            {
                case 0: // waiting for a player
                    if (Player* player = PlayerOnTrap())
                    {
                        player->SendPlayMusic(8740, true);
                        player->NearTeleportTo(me->GetPositionX(), me->GetPositionY(), me->GetPositionZ(), player->GetOrientation());
                        SetDoors(false);
                        _step = 1;
                        _timer = 1000;
                    }
                    else
                        _timer = 300;
                    break;
                case 1: // the rats
                    if (Player* player = PlayerOnTrap())
                        for (int i = 0; i < 15; ++i)
                            if (Creature* rat = me->SummonCreature(NPC_HUNGRY_VAULT_RAT,
                                    player->GetPositionX() + urand(1, 4), player->GetPositionY() + urand(1, 4), player->GetPositionZ(),
                                    player->GetOrientation(), TEMPSUMMON_TIMED_OR_CORPSE_DESPAWN, 350 * IN_MILLISECONDS))
                                rat->AI()->AttackStart(player);
                    _step = 2;
                    _timer = 1000;
                    break;
                case 2: // wait until the rats are dead or the player left
                {
                    bool ratLeft = false;
                    std::list<Creature*> rats;
                    me->GetCreatureListWithEntryInGrid(rats, NPC_HUNGRY_VAULT_RAT, 5.0f);
                    for (Creature* rat : rats)
                        if (rat->IsAlive())
                            ratLeft = true;
                    if (!PlayerOnTrap() || !ratLeft)
                    {
                        SetDoors(true);
                        _step = 0;
                        _timer = HOUR * IN_MILLISECONDS;
                    }
                    else
                        _timer = 1000;
                    break;
                }
                default:
                    break;
            }
        }
    };

    class mod_turtle_stormwind_vault_objects : public AllGameObjectScript
    {
    public:
        mod_turtle_stormwind_vault_objects() : AllGameObjectScript("mod_turtle_stormwind_vault_objects") { }

        // AzerothCore leaves dungeon doors of a map without InstanceScript in
        // state 0 (open) instead of their spawn state: the Vault Door spawns closed.
        void OnGameObjectAddWorld(GameObject* go) override
        {
            if (go && go->GetEntry() == GO_VAULT_DOOR && go->GetMapId() == MAP_STORMWIND_VAULT && !go->GetInstanceScript())
                go->SetGoState(OpenedVaults().count(go->GetInstanceId()) ? GO_STATE_ACTIVE : GO_STATE_READY);
        }

        GameObjectAI* GetGameObjectAI(GameObject* go) const override
        {
            if (go && go->GetEntry() == GO_RAT_TRAP)
                return new go_stormwind_vault_rat_trapAI(go);
            return nullptr;
        }
    };

    template <class AI>
    CreatureAI* MakeVault(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_stormwind_vault()
{
    RegisterAI(NPC_BLACK_BRIDE,       &MakeVault<boss_black_brideAI>);
    RegisterAI(NPC_VOLKAN_CRUELBLADE, &MakeVault<boss_volkan_cruelbladeAI>);
    RegisterAI(NPC_THAMGRARR,         &MakeVault<boss_thamgrarrAI>);
    RegisterAI(NPC_ASZOSH_GRIMFLAME,  &MakeVault<boss_aszosh_grimflameAI>);
    RegisterAI(NPC_DAMIAN,            &MakeVault<boss_damianAI>);
    RegisterAI(NPC_ARCTIRAS,          &MakeVault<boss_arctirasAI>);
    new mod_turtle_stormwind_vault_objects();
}
