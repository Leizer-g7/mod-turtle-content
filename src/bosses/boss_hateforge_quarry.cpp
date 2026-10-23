/*
 * mod-turtle-content - Hateforge Quarry (map 808) boss and trash scripts.
 *
 * Ported from Penqle's tortoise-wow core (commit 10393426, 2026-10-11),
 * src/scripts/dungeons/hateforge_quarry: boss_engineer_figgles.cpp,
 * boss_hatereaver_annhilator.cpp, boss_bargul_blackhammer.cpp,
 * boss_hargesh_doomcaller.cpp and hateforge_quarry_trash.cpp. Same timers and
 * the same "keep the timer and retry until the cast works" behaviour.
 *
 * - Engineer Figgles: Corrosive Poison once, 10 s into the fight.
 * - Hatereaver Annihilator: Knockback every 30 s, Cleave every 40 s, War Stomp every 45 s.
 * - High Foreman Bargul Blackhammer: Stunning Strike 25 s, Mortal Strike 35 s,
 *   Demoralizing Shout 40 s; out of combat a random shout 60 s after spawn/reset, then every 5 min.
 * - Har'gesh Doomcaller: Immolate 30 s, Shadow Bolt Volley (60 s, then 90 s), Shadow Bolt 10 s.
 *   At 60% he becomes immune, roots himself and channels; two Faceless Terrors come out and
 *   attack (Turtle's loop stops after the first player, so it is two adds, both at the first
 *   spawn point). When both are dead he fights again. He resets if pulled below z 135.
 *   A Faceless Terror left without a target resets Har'gesh (wipe check every 5 s).
 * - Hateforge Cleric: Immolate as an opener, Greater Heal on the most wounded ally within 40 yd
 *   every 8-10 s (Turtle's heal values).
 * - Hateforge Taskmaster: Hooked Net every 35 s (Turtle's 10 s duration) and, once per fight,
 *   Whipped Into Shape on an ally within 5 yd.
 * - Twilight Fireblade: Fire-Blessed Weapon once per fight.
 *
 * Turtle-only spells and their 3.3.5 stand-ins:
 *   29230 Immune All        -> damage + crowd-control immunity applied directly (as Razjal in Zul'Farrak)
 *   56522 Whipped Into Shape (+100 physical damage done, 10 s, ally) -> 4539 aura set to +100 / 10 s
 *   56524 Fire-Blessed Weapon (+50 fire damage per hit, 30 s, self)  -> 38793 Flameblade (+50, 30 s, self)
 * The bosses' lines are Turtle's script_texts -1999950..-1999961 (text only, the voices are
 * Turtle client files).
 */

#include "turtle_boss_common.h"
#include "CellImpl.h"
#include "Containers.h"
#include "GridNotifiers.h"
#include "GridNotifiersImpl.h"
#include "Map.h"
#include "Random.h"
#include "TemporarySummon.h"

using namespace TurtleBoss;

namespace
{
    enum HateforgeCreatures
    {
        NPC_HATEFORGE_CLERIC        = 60718,
        NPC_HATEFORGE_TASKMASTER    = 60723,
        NPC_TWILIGHT_FIREBLADE      = 60725,
        NPC_HATEREAVER_ANNIHILATOR  = 60734,
        NPC_BARGUL_BLACKHAMMER      = 60735,
        NPC_ENGINEER_FIGGLES        = 60736,
        NPC_HARGESH_DOOMCALLER      = 60737,
        NPC_FACELESS_TERROR         = 60738,
    };

    enum HateforgeSpells
    {
        SPELL_CORROSIVE_POISON      = 24111,
        SPELL_KNOCKBACK             = 28438,
        SPELL_CLEAVE                = 19983,
        SPELL_WAR_STOMP             = 11876,
        SPELL_STUNNING_STRIKE       = 5703,
        SPELL_MORTAL_STRIKE         = 27580,
        SPELL_DEMORALIZING_SHOUT    = 27579,
        SPELL_IMMOLATE              = 11668,
        SPELL_SHADOW_BOLT_VOLLEY    = 27646,
        SPELL_SHADOW_BOLT           = 12739,
        SPELL_SHADOW_CHANNELING     = 12380,
        SPELL_GREATER_HEAL          = 10965,
        SPELL_HOOKED_NET            = 13608,
        SPELL_WHIPPED_STAND_IN      = 4539,   // Turtle 56522 Whipped Into Shape
        SPELL_FIRE_BLESSED_STAND_IN = 38793,  // Turtle 56524 Fire-Blessed Weapon
    };

    // Turtle values where 3.3.5's spell of the same id differs.
    constexpr float GREATER_HEAL_TURTLE_AVERAGE = 1680.0f + (1.0f + 196.0f) / 2.0f;  // Turtle 10965: 1681-1876
    constexpr int32 HOOKED_NET_TURTLE_DURATION  = 10 * IN_MILLISECONDS;              // 3.3.5: 4 s
    constexpr int32 WHIPPED_DAMAGE              = 100;
    constexpr int32 WHIPPED_DURATION            = 10 * IN_MILLISECONDS;

    char const* const TEXT_BARGUL_OOC[3] =
    {
        "We must maintain our production! WORK HARDER!",
        "Shadowforge shall reward us all for our work here in the Quarry!",
        "I don't see enough of you busy out there, We don't have all month!",
    };

    Position const FacelessTerrorSpawn = { -8300.825195f, -3735.292725f, 138.12f, 6.020778f };
    constexpr float HARGESH_MIN_Z = 135.0f;

    uint32 const HargeshImmunityMechanics[] =
    {
        MECHANIC_CHARM, MECHANIC_DISORIENTED, MECHANIC_DISARM, MECHANIC_FEAR, MECHANIC_ROOT, MECHANIC_SILENCE,
        MECHANIC_SLEEP, MECHANIC_SNARE, MECHANIC_STUN, MECHANIC_FREEZE, MECHANIC_KNOCKOUT, MECHANIC_POLYMORPH,
        MECHANIC_BANISH, MECHANIC_SHACKLE, MECHANIC_TURN, MECHANIC_HORROR, MECHANIC_DAZE, MECHANIC_SAPPED,
        MECHANIC_INTERRUPT,
    };

    // Turtle 29230 Immune All.
    void ApplyImmuneAll(Creature* creature, bool apply)
    {
        creature->ApplySpellImmune(0, IMMUNITY_DAMAGE, SPELL_SCHOOL_MASK_ALL, apply);
        for (uint32 mechanic : HargeshImmunityMechanics)
            creature->ApplySpellImmune(0, IMMUNITY_MECHANIC, mechanic, apply);
    }

    // vmangos SelectRandomFriendlyTarget(nullptr, radius): a random friendly unit within radius (the caster counts).
    Unit* RandomFriendly(Creature* me, float radius)
    {
        std::list<Unit*> units;
        Acore::AnyFriendlyUnitInObjectRangeCheck check(me, me, radius);
        Acore::UnitListSearcher<Acore::AnyFriendlyUnitInObjectRangeCheck> searcher(me, units, check);
        Cell::VisitObjects(me, searcher, radius);
        units.push_back(me);
        units.remove_if([](Unit* u) { return !u || !u->IsAlive() || u->IsPlayer() || u->IsTotem(); });
        if (units.empty())
            return nullptr;
        return Acore::Containers::SelectRandomContainerElement(units);
    }

    // Shared: a timer that restarts only when the cast works (vmangos DoCastSpellIfCan == CAST_OK).
    struct RetryTimer
    {
        uint32 timer = 0;
        uint32 period = 0;

        void Set(uint32 first, uint32 repeat) { timer = first; period = repeat; }

        template <typename F>
        void Update(uint32 diff, F tryCast)
        {
            if (timer < diff)
            {
                if (tryCast())
                    timer = period;
            }
            else
                timer -= diff;
        }
    };

    // ------------------------------------------------------------------
    // Engineer Figgles
    // ------------------------------------------------------------------
    struct boss_engineer_figglesAI : public TurtleBossAI
    {
        explicit boss_engineer_figglesAI(Creature* c) : TurtleBossAI(c) { }

        bool _poisonDone = false;
        uint32 _poisonTimer = 0;

        void Reset() override
        {
            _poisonDone = false;
            _poisonTimer = 10 * IN_MILLISECONDS;
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            Say(me, "You foolish outsiders! You're not supposed to be here interrupting my great work. Broody, get them, destroy them!");
        }

        void JustDied(Unit* /*killer*/) override { Say(me, "I.. Was going to build an army... I would've never been stopped!"); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            // Turtle marks it done even when the cast fails: one try only.
            if (!_poisonDone)
            {
                if (_poisonTimer < diff)
                {
                    TryCast(me->GetVictim(), SPELL_CORROSIVE_POISON);
                    _poisonDone = true;
                }
                else
                    _poisonTimer -= diff;
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Hatereaver Annihilator
    // ------------------------------------------------------------------
    struct boss_hatereaver_annihilatorAI : public TurtleBossAI
    {
        explicit boss_hatereaver_annihilatorAI(Creature* c) : TurtleBossAI(c) { }

        RetryTimer _knockback, _cleave, _warStomp;

        void Reset() override
        {
            _knockback.Set(30 * IN_MILLISECONDS, 30 * IN_MILLISECONDS);
            _cleave.Set(40 * IN_MILLISECONDS, 40 * IN_MILLISECONDS);
            _warStomp.Set(45 * IN_MILLISECONDS, 45 * IN_MILLISECONDS);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "Unidentified intruders, defensive measures, engaged."); }
        void JustDied(Unit* /*killer*/) override { Say(me, "Activate emergency power... Emergency power activation failed... Commence... Shut... Do..wn..."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            _knockback.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_KNOCKBACK); });
            _cleave.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_CLEAVE); });
            _warStomp.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_WAR_STOMP); });

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // High Foreman Bargul Blackhammer
    // ------------------------------------------------------------------
    struct boss_bargul_blackhammerAI : public TurtleBossAI
    {
        explicit boss_bargul_blackhammerAI(Creature* c) : TurtleBossAI(c) { }

        RetryTimer _stunningStrike, _mortalStrike, _demoralizingShout;
        uint32 _oocShoutTimer = 0;

        void Reset() override
        {
            _stunningStrike.Set(25 * IN_MILLISECONDS, 25 * IN_MILLISECONDS);
            _mortalStrike.Set(35 * IN_MILLISECONDS, 35 * IN_MILLISECONDS);
            _demoralizingShout.Set(40 * IN_MILLISECONDS, 40 * IN_MILLISECONDS);
            _oocShoutTimer = 60 * IN_MILLISECONDS;
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "You think you contend with the High Foreman? Feel the fury of the Dark Iron!"); }
        void JustDied(Unit* /*killer*/) override { Say(me, "Curse you.. Damn you... The work, must go on."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
            {
                // Turtle: only out of combat, a random zone shout, then every 5 minutes.
                if (me->IsInCombat() || !me->IsAlive())
                    return;
                if (_oocShoutTimer < diff)
                {
                    Yell(me, TEXT_BARGUL_OOC[urand(0, 2)]);
                    _oocShoutTimer = 5 * MINUTE * IN_MILLISECONDS;
                }
                else
                    _oocShoutTimer -= diff;
                return;
            }

            _stunningStrike.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_STUNNING_STRIKE); });
            _mortalStrike.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_MORTAL_STRIKE); });
            _demoralizingShout.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_DEMORALIZING_SHOUT); });

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Har'gesh Doomcaller
    // ------------------------------------------------------------------
    struct boss_hargesh_doomcallerAI : public TurtleBossAI
    {
        explicit boss_hargesh_doomcallerAI(Creature* c) : TurtleBossAI(c) { }

        bool _phaseTwo = false;
        bool _addsDead = false;
        uint32 _checkAddsTimer = 0;
        RetryTimer _immolate, _volley, _shadowBolt;

        void Reset() override
        {
            _immolate.Set(30 * IN_MILLISECONDS, 30 * IN_MILLISECONDS);
            _volley.Set(60 * IN_MILLISECONDS, 90 * IN_MILLISECONDS);
            _shadowBolt.Set(10 * IN_MILLISECONDS, 10 * IN_MILLISECONDS);
            _checkAddsTimer = 500;
            _phaseTwo = false;
            _addsDead = false;
            EndChannel();
            summons.DespawnAll();
        }

        void EndChannel()
        {
            me->InterruptNonMeleeSpells(false, SPELL_SHADOW_CHANNELING);
            me->RemoveAurasDueToSpell(SPELL_SHADOW_CHANNELING);
            ApplyImmuneAll(me, false);
            me->SetControlled(false, UNIT_STATE_ROOT);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "So, you have been the ones that raised the alarms, you shall meet your demise within this cave..."); }

        void JustDied(Unit* /*killer*/) override
        {
            Say(me, "Stronger than I have anticipated... I have served my masters, till the end.");
            summons.DespawnAll();
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            EndChannel();
            summons.DespawnAll();
            TurtleBossAI::EnterEvadeMode(why);
        }

        void PhaseTwo()
        {
            ApplyImmuneAll(me, true);
            me->StopMoving();
            me->SetControlled(true, UNIT_STATE_ROOT);
            me->CastSpell(me, SPELL_SHADOW_CHANNELING, true);

            // Turtle loops over the map's players but returns after the first living, non-GM one.
            for (auto const& itr : me->GetMap()->GetPlayers())
            {
                Player* player = itr.GetSource();
                if (!player || !player->IsAlive() || player->IsGameMaster())
                    continue;

                for (uint8 i = 0; i < 2; ++i)
                    if (Creature* terror = me->SummonCreature(NPC_FACELESS_TERROR, FacelessTerrorSpawn, TEMPSUMMON_MANUAL_DESPAWN))
                        if (terror->AI())
                            terror->AI()->AttackStart(player);

                Say(me, "The Void hungers for more souls, let it consume you...");
                _phaseTwo = true;
                return;
            }
        }

        void CheckIfAddsAreDead(uint32 diff)
        {
            if (_checkAddsTimer >= diff)
            {
                _checkAddsTimer -= diff;
                return;
            }
            _checkAddsTimer = 500;

            if (summons.empty())
                return;

            for (ObjectGuid const& guid : summons)
            {
                Creature* terror = ObjectAccessor::GetCreature(*me, guid);
                if (terror && terror->IsAlive())
                    return;   // at least one still fights
            }

            EndChannel();
            if (Unit* victim = me->GetVictim())
                me->GetThreatMgr().AddThreat(victim, 10.0f);
            _addsDead = true;
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (me->GetPositionZ() < HARGESH_MIN_Z)
            {
                EnterEvadeMode(EVADE_REASON_OTHER);
                return;
            }

            if (!_phaseTwo || _addsDead)
            {
                _immolate.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_IMMOLATE); });
                _volley.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_SHADOW_BOLT_VOLLEY); });
                _shadowBolt.Update(diff, [this] { return TryCast(me->GetVictim(), SPELL_SHADOW_BOLT); });
            }

            if (!_phaseTwo && me->HealthBelowPct(60))
                PhaseTwo();

            if (_phaseTwo && !_addsDead)
                CheckIfAddsAreDead(diff);

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Faceless Terror (Har'gesh's adds)
    // ------------------------------------------------------------------
    struct npc_faceless_terrorAI : public ScriptedAI
    {
        explicit npc_faceless_terrorAI(Creature* c) : ScriptedAI(c) { }

        bool _calledEvade = false;
        uint32 _wipeCheckTimer = 0;

        void Reset() override
        {
            _calledEvade = false;
            _wipeCheckTimer = 5 * IN_MILLISECONDS;
            me->ApplySpellImmune(0, IMMUNITY_SCHOOL, SPELL_SCHOOL_MASK_SHADOW, true);  // Turtle school_immune_mask 32
        }

        // Turtle: a terror with nobody to fight tells Har'gesh to reset (the group wiped).
        void CheckForWipe(uint32 diff)
        {
            if (_wipeCheckTimer >= diff)
            {
                _wipeCheckTimer -= diff;
                return;
            }
            _wipeCheckTimer = 5 * IN_MILLISECONDS;

            for (auto const& itr : me->GetMap()->GetPlayers())
                if (Player* player = itr.GetSource())
                    if (Creature* hargesh = player->FindNearestCreature(NPC_HARGESH_DOOMCALLER, 250.0f))
                    {
                        if (hargesh->IsAIEnabled && hargesh->AI())
                            hargesh->AI()->EnterEvadeMode();
                        _calledEvade = true;
                        break;
                    }
        }

        void EnterEvadeMode(EvadeReason /*why*/) override
        {
            // Stays where it is until the wipe check has run (Turtle keeps the add up).
            me->CombatStop(true);
            me->GetThreatMgr().ClearAllThreat();
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
            {
                if (!_calledEvade)
                    CheckForWipe(diff);
                return;
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Hateforge Cleric
    // ------------------------------------------------------------------
    struct mob_hateforge_clericAI : public TurtleBossAI
    {
        explicit mob_hateforge_clericAI(Creature* c) : TurtleBossAI(c) { }

        bool _openerDone = false;
        uint32 _healTimer = 0;

        void Reset() override
        {
            _openerDone = false;
            _healTimer = 4 * IN_MILLISECONDS;
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            // Turtle's variable says Shadow Word: Pain, the cast is Immolate.
            if (!_openerDone && TryCast(me->GetVictim(), SPELL_IMMOLATE))
                _openerDone = true;

            if (_healTimer < diff)
            {
                if (Unit* ally = DoSelectLowestHpFriendly(40.0f))
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_GREATER_HEAL, EFFECT_0, GREATER_HEAL_TURTLE_AVERAGE));
                    if (TryCastCustom(ally, SPELL_GREATER_HEAL, values))
                        _healTimer = urand(8 * IN_MILLISECONDS, 10 * IN_MILLISECONDS);
                }
            }
            else
                _healTimer -= diff;

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Hateforge Taskmaster
    // ------------------------------------------------------------------
    struct mob_hateforge_taskmasterAI : public TurtleBossAI
    {
        explicit mob_hateforge_taskmasterAI(Creature* c) : TurtleBossAI(c) { }

        bool _whipDone = false;
        uint32 _whipTimer = 0;
        RetryTimer _net;

        void Reset() override
        {
            _whipDone = false;
            _whipTimer = 5 * IN_MILLISECONDS;
            _net.Set(1 * IN_MILLISECONDS, 35 * IN_MILLISECONDS);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!_whipDone)
            {
                if (_whipTimer < diff)
                {
                    if (Unit* ally = RandomFriendly(me, 5.0f))
                        if (!me->HasUnitState(UNIT_STATE_CASTING))
                        {
                            TuneAura(me->AddAura(SPELL_WHIPPED_STAND_IN, ally), WHIPPED_DURATION, WHIPPED_DAMAGE);
                            _whipDone = true;
                        }
                }
                else
                    _whipTimer -= diff;
            }

            _net.Update(diff, [this]
            {
                CustomSpellValues values;
                values.AddSpellMod(SPELLVALUE_AURA_DURATION, HOOKED_NET_TURTLE_DURATION);
                return TryCastCustom(me->GetVictim(), SPELL_HOOKED_NET, values);
            });

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Twilight Fireblade
    // ------------------------------------------------------------------
    struct mob_twilight_firebladeAI : public TurtleBossAI
    {
        explicit mob_twilight_firebladeAI(Creature* c) : TurtleBossAI(c) { }

        bool _buffDone = false;
        uint32 _buffTimer = 0;

        void Reset() override
        {
            _buffDone = false;
            _buffTimer = 1 * IN_MILLISECONDS;
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!_buffDone)
            {
                if (_buffTimer < diff)
                {
                    // Turtle aims it at a random ally within 10 yd, but the spell only targets its caster.
                    if (RandomFriendly(me, 10.0f) && TryCast(me, SPELL_FIRE_BLESSED_STAND_IN))
                        _buffDone = true;
                }
                else
                    _buffTimer -= diff;
            }

            DoMeleeAttackIfReady();
        }
    };

    CreatureAI* MakeFiggles(Creature* c)      { return new boss_engineer_figglesAI(c); }
    CreatureAI* MakeAnnihilator(Creature* c)  { return new boss_hatereaver_annihilatorAI(c); }
    CreatureAI* MakeBargul(Creature* c)       { return new boss_bargul_blackhammerAI(c); }
    CreatureAI* MakeHargesh(Creature* c)      { return new boss_hargesh_doomcallerAI(c); }
    CreatureAI* MakeFacelessTerror(Creature* c) { return new npc_faceless_terrorAI(c); }
    CreatureAI* MakeCleric(Creature* c)       { return new mob_hateforge_clericAI(c); }
    CreatureAI* MakeTaskmaster(Creature* c)   { return new mob_hateforge_taskmasterAI(c); }
    CreatureAI* MakeFireblade(Creature* c)    { return new mob_twilight_firebladeAI(c); }
}

void AddSC_turtle_hateforge_quarry()
{
    RegisterAI(NPC_ENGINEER_FIGGLES,       &MakeFiggles);
    RegisterAI(NPC_HATEREAVER_ANNIHILATOR, &MakeAnnihilator);
    RegisterAI(NPC_BARGUL_BLACKHAMMER,     &MakeBargul);
    RegisterAI(NPC_HARGESH_DOOMCALLER,     &MakeHargesh);
    RegisterAI(NPC_FACELESS_TERROR,        &MakeFacelessTerror);
    RegisterAI(NPC_HATEFORGE_CLERIC,       &MakeCleric);
    RegisterAI(NPC_HATEFORGE_TASKMASTER,   &MakeTaskmaster);
    RegisterAI(NPC_TWILIGHT_FIREBLADE,     &MakeFireblade);
}
