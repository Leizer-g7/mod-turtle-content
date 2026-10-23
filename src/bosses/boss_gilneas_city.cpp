/*
 * mod-turtle-content - Gilneas City (map 815) boss scripts.
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/gilneas_city
 * (boss_celia.cpp, boss_lord_mortimer.cpp, instance_gilneas_city.cpp).
 * The other Gilneas City bosses (Matthias Holtz, Judge Sutherland,
 * Dustivan Blackcowl, Marshal Magnus Greystone) have no Turtle C++ AI and
 * keep their converted SmartAI.
 *
 * Celia and Mortimer keep Turtle's per-form countdown timers on purpose:
 * each timer only runs while the boss is in the matching form.
 */

#include "turtle_boss_common.h"
#include "GameObject.h"
#include "Random.h"

using namespace TurtleBoss;

namespace
{
    enum GilneasCityCreatures
    {
        NPC_GENN_GREYMANE            = 61418,
        NPC_CELIA_HARLOW             = 61263,
        NPC_LORD_MORTIMER            = 61264,
        NPC_GREYMANE_KNIGHT          = 61365,
        NPC_GREYMANE_NOBLE           = 61390,
    };

    enum GilneasCityObjects
    {
        GO_HARLOW_FAMILY_CHEST       = 2020027,
    };

    enum GilneasCityDisplays
    {
        MODEL_DRAGONKIN_CELIA        = 8249,
        MODEL_DRAGONKIN_MORTIMER     = 143,
    };

    enum GilneasCitySpells
    {
        SPELL_BLAST_WAVE_NO_KNOCK    = 20229,  // Turtle 13021 (no knockback in 1.12): 462-544 fire, -50% speed 6 sec
        SPELL_IMMOLATE               = 25309,
        SPELL_SHADOW_WORD_PAIN       = 2767,   // Turtle 61/tick (3.3.5 55) -> bp0 overridden
        SPELL_CORRUPTION             = 11671,
        SPELL_C_HOLY_STRIKE          = 21889,  // Turtle 2495 (not in 3.3.5): 35% weapon damage + 71-77 holy
        SPELL_CONSECRATION           = 20924,  // Turtle 54/tick (3.3.5 56) -> bp0 overridden

        SPELL_DRAIN_LIFE             = 17620,
        SPELL_MORTAL_STRIKE          = 21551,
        SPELL_GENN_CURSE_OF_AGONY         = 11711,
        SPELL_GENN_FEAR              = 22678,
        SPELL_STRIKE                 = 18368,
        SPELL_HAMMER_OF_JUSTICE      = 853,
        SPELL_MIND_BLAST             = 10945,
        SPELL_MIND_FLAY              = 17312,
    };

    constexpr uint32 TIMER_BLAST_WAVE = 25 * IN_MILLISECONDS;

    // Shared by Celia and Mortimer: dragonkin form below 50% with Blast Wave.
    struct HarlowAI : public TurtleBossAI
    {
        HarlowAI(Creature* c, uint32 dragonkinModel) : TurtleBossAI(c), _dragonkinModel(dragonkinModel) { }

        uint32 _dragonkinModel;
        uint32 _blastWaveTimer = TIMER_BLAST_WAVE;

        void ResetForm()
        {
            _blastWaveTimer = TIMER_BLAST_WAVE;
            me->SetDisplayId(me->GetNativeDisplayId());
        }

        // Returns true while in dragonkin form (and runs its Blast Wave timer).
        bool UpdateDragonkin(uint32 diff)
        {
            if (!me->HealthBelowPct(50))
                return false;

            if (me->GetDisplayId() != _dragonkinModel)
                me->SetDisplayId(_dragonkinModel);

            if (_blastWaveTimer <= diff)
            {
                // Turtle picks a random target first; Blast Wave itself hits around the boss.
                // Turtle 13021 rolls 462-544 (avg 503); the carrier rolls bp..bp+112.
                if (SelectTarget(SelectTargetMethod::Random, 0))
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, 447);
                    values.AddSpellMod(SPELLVALUE_AURA_DURATION, 6000);
                    if (TryCastCustom(me, SPELL_BLAST_WAVE_NO_KNOCK, values))
                        _blastWaveTimer = TIMER_BLAST_WAVE;
                }
            }
            else
                _blastWaveTimer -= diff;

            return true;
        }
    };

    // ------------------------------------------------------------------
    // Regent-Lady Celia Harlow
    // ------------------------------------------------------------------
    struct boss_celiaAI : public HarlowAI
    {
        explicit boss_celiaAI(Creature* c) : HarlowAI(c, MODEL_DRAGONKIN_CELIA) { }

        uint32 _immolateTimer = 0;
        uint32 _shadowWordPainTimer = 0;
        uint32 _corruptionTimer = 0;

        void Reset() override
        {
            _immolateTimer = 8 * IN_MILLISECONDS;
            _shadowWordPainTimer = 11 * IN_MILLISECONDS;
            _corruptionTimer = 6 * IN_MILLISECONDS;
            ResetForm();
        }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "Mortimer, it would appear we have someone here to interrupt our plans!"); }
        void JustDied(Unit* /*killer*/) override
        {
            Yell(me, "All of our progress, our influence... What a pointless end...");

            // Turtle instance_gilneas_city::OnCreatureDeath: DoRespawnGameObject(Harlow
            // Family Chest, HOUR) - respawns the chest if it is not spawned.
            std::list<GameObject*> chests;
            me->GetGameObjectListWithEntryInGrid(chests, GO_HARLOW_FAMILY_CHEST, 100.0f);
            for (GameObject* chest : chests)
                if (chest && !chest->isSpawned())
                    chest->SetRespawnTime(HOUR);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!UpdateDragonkin(diff))
            {
                if (_immolateTimer <= diff)
                {
                    if (TryCast(SelectTarget(SelectTargetMethod::Random, 0), SPELL_IMMOLATE))
                        _immolateTimer = 8 * IN_MILLISECONDS;
                }
                else
                    _immolateTimer -= diff;

                if (_shadowWordPainTimer <= diff)
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, 61);
                    if (TryCastCustom(SelectTarget(SelectTargetMethod::Random, 0), SPELL_SHADOW_WORD_PAIN, values))
                        _shadowWordPainTimer = 11 * IN_MILLISECONDS;
                }
                else
                    _shadowWordPainTimer -= diff;

                if (_corruptionTimer <= diff)
                {
                    if (TryCast(SelectTarget(SelectTargetMethod::Random, 0), SPELL_CORRUPTION))
                        _corruptionTimer = 6 * IN_MILLISECONDS;
                }
                else
                    _corruptionTimer -= diff;
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Regent-Lord Mortimer Harlow
    // ------------------------------------------------------------------
    struct boss_lord_mortimerAI : public HarlowAI
    {
        explicit boss_lord_mortimerAI(Creature* c) : HarlowAI(c, MODEL_DRAGONKIN_MORTIMER) { }

        uint32 _holyStrikeTimer = 0;
        uint32 _consecrationTimer = 0;

        void Reset() override
        {
            _holyStrikeTimer = 9 * IN_MILLISECONDS;
            _consecrationTimer = 12 * IN_MILLISECONDS;
            ResetForm();
        }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "You will not take what is mine!"); }
        void JustDied(Unit* /*killer*/) override { Yell(me, "Father..."); }

        bool HolyStrike(Unit* target)
        {
            // Turtle 2495 has a 5 yd range; a random pick out of range retries next update.
            if (!target || !me->IsWithinMeleeRange(target))
                return false;
            int32 weapon = int32(me->CalculateDamage(BASE_ATTACK, false, true));
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT0, int32(CalculatePct(weapon, 35)) + irand(71, 77));
            return TryCastCustom(target, SPELL_C_HOLY_STRIKE, values);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!UpdateDragonkin(diff))
            {
                if (_holyStrikeTimer <= diff)
                {
                    if (HolyStrike(SelectTarget(SelectTargetMethod::Random, 0)))
                        _holyStrikeTimer = 9 * IN_MILLISECONDS;
                }
                else
                    _holyStrikeTimer -= diff;

                if (_consecrationTimer <= diff)
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, 54);
                    if (TryCastCustom(SelectTarget(SelectTargetMethod::Random, 0), SPELL_CONSECRATION, values))
                        _consecrationTimer = 12 * IN_MILLISECONDS;
                }
                else
                    _consecrationTimer -= diff;
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Genn Greymane
    // ------------------------------------------------------------------
    enum GennEvents { EVENT_GENN_DRAIN_LIFE = 1, EVENT_GENN_MORTAL_STRIKE, EVENT_GENN_CURSE_OF_AGONY };

    struct npc_genn_greymaneAI : public TurtleBossAI
    {
        explicit npc_genn_greymaneAI(Creature* c) : TurtleBossAI(c) { }

        bool _halfHealthDone = false;

        void Reset() override
        {
            _halfHealthDone = false;
            events.Reset();
            events.ScheduleEvent(EVENT_GENN_DRAIN_LIFE, 4s);
            events.ScheduleEvent(EVENT_GENN_MORTAL_STRIKE, 2s);
            events.ScheduleEvent(EVENT_GENN_CURSE_OF_AGONY, 1s);
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            Yell(me, "My family has held power in Gilneas for countless generations. You will not change fate.");
        }

        void JustDied(Unit* /*killer*/) override
        {
            Yell(me, "It... it was pointless after all... This cannot be the way I fall...");
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_GENN_DRAIN_LIFE:
                        if (TryCast(me->GetVictim(), SPELL_DRAIN_LIFE))
                            events.ScheduleEvent(EVENT_GENN_DRAIN_LIFE, 20s, 25s);
                        else
                            events.ScheduleEvent(EVENT_GENN_DRAIN_LIFE, 100ms);
                        break;
                    case EVENT_GENN_MORTAL_STRIKE:
                        if (TryCastNoCost(me->GetVictim(), SPELL_MORTAL_STRIKE))  // 300 rage cost, Genn has none
                            events.ScheduleEvent(EVENT_GENN_MORTAL_STRIKE, 17s, 20s);
                        else
                            events.ScheduleEvent(EVENT_GENN_MORTAL_STRIKE, 100ms);
                        break;
                    case EVENT_GENN_CURSE_OF_AGONY:
                        if (TryCast(SelectTarget(SelectTargetMethod::Random, 0, 0.0f, true), SPELL_GENN_CURSE_OF_AGONY))
                            events.ScheduleEvent(EVENT_GENN_CURSE_OF_AGONY, 10s, 15s);
                        else
                            events.ScheduleEvent(EVENT_GENN_CURSE_OF_AGONY, 100ms);
                        break;
                    default:
                        break;
                }
            }

            // Turtle: once below 50%, a yell and one Fear on a random player.
            if (!_halfHealthDone && me->GetHealthPct() < 50.0f)
            {
                _halfHealthDone = true;
                Say(me, "Our nation stands strong! I did what was neccesary.");   // broadcast text 81055 is a say
                TryCast(SelectTarget(SelectTargetMethod::Random, 0, 0.0f, true), SPELL_GENN_FEAR);
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Greymane Knight
    // ------------------------------------------------------------------
    enum KnightEvents { EVENT_KNIGHT_STRIKE = 1, EVENT_KNIGHT_HAMMER_OF_JUSTICE };

    struct npc_greymane_knightAI : public TurtleBossAI
    {
        explicit npc_greymane_knightAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_KNIGHT_HAMMER_OF_JUSTICE, 12s, 20s);
            events.ScheduleEvent(EVENT_KNIGHT_STRIKE, 1s);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_KNIGHT_STRIKE:
                        if (TryCast(me->GetVictim(), SPELL_STRIKE))
                            events.ScheduleEvent(EVENT_KNIGHT_STRIKE, 10s);
                        else
                            events.ScheduleEvent(EVENT_KNIGHT_STRIKE, 100ms);
                        break;
                    case EVENT_KNIGHT_HAMMER_OF_JUSTICE:
                        if (TryCast(SelectTarget(SelectTargetMethod::MaxThreat, 0, 0.0f, true), SPELL_HAMMER_OF_JUSTICE))
                            events.ScheduleEvent(EVENT_KNIGHT_HAMMER_OF_JUSTICE, 12s, 20s);
                        else
                            events.ScheduleEvent(EVENT_KNIGHT_HAMMER_OF_JUSTICE, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Greymane Noble
    // ------------------------------------------------------------------
    enum NobleEvents { EVENT_NOBLE_MIND_BLAST = 1, EVENT_NOBLE_MIND_FLAY };

    struct npc_greymane_nobleAI : public TurtleBossAI
    {
        explicit npc_greymane_nobleAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_NOBLE_MIND_FLAY, 10s, 18s);
            events.ScheduleEvent(EVENT_NOBLE_MIND_BLAST, 2s);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_NOBLE_MIND_BLAST:
                        if (TryCast(me->GetVictim(), SPELL_MIND_BLAST))
                            events.ScheduleEvent(EVENT_NOBLE_MIND_BLAST, 9s);
                        else
                            events.ScheduleEvent(EVENT_NOBLE_MIND_BLAST, 100ms);
                        break;
                    case EVENT_NOBLE_MIND_FLAY:
                        if (TryCast(SelectTarget(SelectTargetMethod::Random, 0, 0.0f, true), SPELL_MIND_FLAY))
                            events.ScheduleEvent(EVENT_NOBLE_MIND_FLAY, 10s, 18s);
                        else
                            events.ScheduleEvent(EVENT_NOBLE_MIND_FLAY, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    template <class AI>
    CreatureAI* MakeGilneas(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_gilneas_city()
{
    RegisterAI(NPC_CELIA_HARLOW,    &MakeGilneas<boss_celiaAI>);
    RegisterAI(NPC_LORD_MORTIMER,   &MakeGilneas<boss_lord_mortimerAI>);
    RegisterAI(NPC_GENN_GREYMANE,   &MakeGilneas<npc_genn_greymaneAI>);
    RegisterAI(NPC_GREYMANE_KNIGHT, &MakeGilneas<npc_greymane_knightAI>);
    RegisterAI(NPC_GREYMANE_NOBLE,  &MakeGilneas<npc_greymane_nobleAI>);
}
