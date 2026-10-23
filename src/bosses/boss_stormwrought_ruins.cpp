/*
 * mod-turtle-content - Stormwrought Ruins (map 818) boss scripts.
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/stormwrought_ruins.
 * Timers, health triggers, targets and yells are Turtle's. Turtle-only spells
 * that the 3.3.5 client does not have are rebuilt from 3.3.5 spells with
 * Turtle's numbers (see the "carrier" notes next to each spell id).
 */

#include "turtle_boss_common.h"
#include "DynamicObject.h"
#include "GameObject.h"
#include "Random.h"
#include "ScriptMgr.h"
#include "TemporarySummon.h"
#include <cmath>

using namespace TurtleBoss;

namespace
{
    enum StormwroughtCreatures
    {
        NPC_IGHALFOR                 = 62671,
        NPC_NETHER_IMP               = 62672,
        NPC_MERGOTHID                = 62673,
        NPC_LADY_DRAZARE             = 62665,
        NPC_ELDERMAW                 = 62661,
        NPC_ELDERMAW_CROCOLISK       = 62674,
        NPC_MYCELLAKOS               = 62664,
        NPC_GROWTH_OF_MYCELLAKOS     = 62675,
        NPC_HALTHAS_SHADECREST       = 62652,
        NPC_DEATHLORD_TIDEBANE       = 62550,
        NPC_CHIEFTAIN_STORMSONG      = 62551,
        NPC_DUKE_BALOR_IV            = 62549,
        NPC_LIBRARIAN_THEODORUS      = 62552,
        NPC_THEODORUS_SEA_ELEMENTAL  = 62742,
        NPC_DAGAR_THE_GLUTTON        = 62547,
        NPC_ORONOK_TORN_HEART        = 62548,
    };

    enum StormwroughtObjects
    {
        GO_BLOODSTONE_ALTAR          = 223364, // Turtle "Nether Altar" (tw guid 5032815)
        GO_VOLATILE_FUNGUS           = 300420,
    };

    // Bloodstone altar position (Turtle spawn 5032815), used if the GO is not found.
    Position const AltarFallbackPos = { -5479.79f, -3968.8f, 259.671f, 3.11807f };

    enum StormwroughtSpells
    {
        // Spells that exist unchanged in 3.3.5
        SPELL_DEATH_COIL             = 6789,   // Turtle drains 287 (3.3.5 245) -> bp0 overridden
        SPELL_FLAMESTRIKE            = 8423,
        SPELL_CURSE_OF_AGONY         = 11712,
        SPELL_IGHALFOR_CHANNELING    = 8734,
        SPELL_DOMINATE_MIND          = 15859,
        SPELL_PSYCHIC_SCREAM         = 13704,
        SPELL_HALTHAS_FEAR           = 27641,
        SPELL_HALTHAS_FLAMESTRIKE    = 11829,
        SPELL_RAIN_OF_FIRE           = 11990,
        SPELL_DARK_PLAGUE            = 18270,
        SPELL_WAIL_OF_SOULS          = 17631,
        SPELL_FORKED_LIGHTNING       = 20299,
        SPELL_STUN_BOMB              = 16497,
        SPELL_DARK_STRIKE            = 22574,
        SPELL_WAILING_DEAD           = 7713,
        SPELL_CONSUME_FLESH          = 3393,
        SPELL_CONE_OF_COLD           = 10159,
        SPELL_FROSTBOLT              = 8406,
        SPELL_THEODORUS_BLIZZARD     = 30093,
        SPELL_DEATH_AND_DECAY        = 11433,
        SPELL_SHADOW_BOLT            = 11660,
        SPELL_KNOCK_AWAY             = 10101,
        SPELL_GHOST_VISUAL           = 22650,  // Turtle creature_template.auras for Duke Balor and Theodorus

        // Carriers for Turtle-only spells (3.3.5 spells whose values are overridden)
        SPELL_C_MIND_FLAY            = 16568,  // Turtle 47386: 700 shadow/sec for 3 sec, -80% speed
        SPELL_C_STRIKE_PHYSICAL      = 21140,  // Turtle 52422 Lightning Strike: 60% weapon damage (melee class) ...
        SPELL_C_STRIKE_NATURE        = 16614,  // ... + 20% weapon damage as nature (52421) on hit
        SPELL_C_TAIL_SLAP_DAMAGE     = 12723,  // Turtle 44041: 200-280 physical, no dodge/parry (+ knockback coded)
        SPELL_C_PRIMORDIAL_ARMOR     = 50994,  // Turtle 44042: +1000 armor, +25 all resistances, 10 sec
        SPELL_C_PRIMORDIAL_REGEN     = 4970,   // Turtle 44042: heal 750 every 2 sec for 10 sec
        SPELL_C_FUNGUS_BURST         = 3339,   // Turtle 44048 effect 1: 400-500 nature to enemies within 5 yd
        SPELL_C_FUNGUS_CLOUD         = 29047,  // Turtle 44048 effect 2: 5 yd ground cloud, 80-120 nature / 3 sec, 15 sec
        SPELL_C_DECAYING_MOLD        = 18289,  // Turtle 44050: disease, 2 x 75-125 over 14 sec, all within 20 yd
        SPELL_C_SEDUCTION            = 44415,  // Turtle 44051: 6 sec stun that damage does not break ...
        SPELL_C_SHADOW_HIT           = 32742,  // ... + 300-350 shadow when it runs out; also Drazare's Embrace explosion
        SPELL_C_EMBRACE_CURSE        = 13619,  // Turtle 44053: 8 sec curse (dummy)
    };

    // Turtle 44051 spell visual 2576 ("Seduction" kiss): its cast kit.
    constexpr uint32 SEDUCTION_CAST_KIT = 4829;

    // ------------------------------------------------------------------
    // Dagar the Glutton
    // ------------------------------------------------------------------
    enum DagarEvents { EVENT_DAGAR_CONSUME_FLESH = 1 };

    struct boss_dagar_the_gluttonAI : public TurtleBossAI
    {
        explicit boss_dagar_the_gluttonAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_DAGAR_CONSUME_FLESH, 6s, 8s);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "More meat to devour!"); }
        void JustDied(Unit* /*killer*/) override { Say(me, "The hunger... never ends..."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_DAGAR_CONSUME_FLESH:
                        if (TryCast(me->GetVictim(), SPELL_CONSUME_FLESH))
                            events.ScheduleEvent(EVENT_DAGAR_CONSUME_FLESH, 12s, 16s);
                        else
                            events.ScheduleEvent(EVENT_DAGAR_CONSUME_FLESH, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Oronok Torn-Heart
    // ------------------------------------------------------------------
    enum OronokEvents { EVENT_ORONOK_KNOCK_AWAY = 1, EVENT_ORONOK_DEATH_AND_DECAY, EVENT_ORONOK_SHADOW_BOLT };

    struct boss_oronok_torn_heartAI : public TurtleBossAI
    {
        explicit boss_oronok_torn_heartAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_ORONOK_KNOCK_AWAY, 8s, 12s);
            events.ScheduleEvent(EVENT_ORONOK_DEATH_AND_DECAY, 1s);
            events.ScheduleEvent(EVENT_ORONOK_SHADOW_BOLT, 5s, 8s);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "Let me tear your heart asunder!"); }
        void JustDied(Unit* /*killer*/) override { Say(me, "Gul'dan...! Your legacy..."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_ORONOK_KNOCK_AWAY:
                        if (TryCast(me->GetVictim(), SPELL_KNOCK_AWAY))
                            events.ScheduleEvent(EVENT_ORONOK_KNOCK_AWAY, 16s, 22s);
                        else
                            events.ScheduleEvent(EVENT_ORONOK_KNOCK_AWAY, 100ms);
                        break;
                    case EVENT_ORONOK_DEATH_AND_DECAY:
                        if (TryCast(me->GetVictim(), SPELL_DEATH_AND_DECAY))
                            events.ScheduleEvent(EVENT_ORONOK_DEATH_AND_DECAY, 22s, 30s);
                        else
                            events.ScheduleEvent(EVENT_ORONOK_DEATH_AND_DECAY, 100ms);
                        break;
                    case EVENT_ORONOK_SHADOW_BOLT:
                        if (TryCast(RandomTarget(SPELL_SHADOW_BOLT), SPELL_SHADOW_BOLT))
                            events.ScheduleEvent(EVENT_ORONOK_SHADOW_BOLT, 7s, 10s);
                        else
                            events.ScheduleEvent(EVENT_ORONOK_SHADOW_BOLT, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Duke Balor the IV
    // ------------------------------------------------------------------
    enum BalorEvents { EVENT_BALOR_MIND_FLAY = 1, EVENT_BALOR_PSYCHIC_SCREAM, EVENT_BALOR_WAILING_DEAD, EVENT_BALOR_DARK_STRIKE };

    constexpr int32 MIND_FLAY_TICK = 700;   // Turtle 47386

    struct boss_duke_balor_ivAI : public TurtleBossAI
    {
        explicit boss_duke_balor_ivAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_BALOR_MIND_FLAY, 5s);
            events.ScheduleEvent(EVENT_BALOR_PSYCHIC_SCREAM, 15s, 20s);
            events.ScheduleEvent(EVENT_BALOR_WAILING_DEAD, 10s, 15s);
            events.ScheduleEvent(EVENT_BALOR_DARK_STRIKE, 7s, 10s);

            if (!me->HasAura(SPELL_GHOST_VISUAL))
                me->AddAura(SPELL_GHOST_VISUAL, me);
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            Say(me, "Yet again do the forces of darkness seek to lay claim to my throne. Stormwrought will not fall into your hands, fiends!");
        }

        void JustDied(Unit* /*killer*/) override { Say(me, "Olivert... Philmore... Old friends..."); }

        // The carrier's level scaling moves in steps of ~1.7, so base points alone
        // land on 699 or 701: once the channel's aura is on the target, set it to 700.
        void SpellHitTarget(Unit* target, SpellInfo const* spell) override
        {
            if (!target || !spell || spell->Id != SPELL_C_MIND_FLAY)
                return;
            if (Aura* flay = target->GetAura(SPELL_C_MIND_FLAY, me->GetGUID()))
                if (AuraEffect* dot = flay->GetEffect(EFFECT_0))
                    if (dot->GetAuraType() == SPELL_AURA_PERIODIC_DAMAGE)
                        dot->ChangeAmount(MIND_FLAY_TICK);
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
                    case EVENT_BALOR_MIND_FLAY:
                    {
                        // Turtle 47386: 700 shadow damage every second for 3 sec, movement -80%.
                        // The carrier scales with creature level on this core, Turtle's spell did not:
                        // BasePointsFor() removes that so every tick is exactly 700.
                        CustomSpellValues values;
                        values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_MIND_FLAY, EFFECT_0, float(MIND_FLAY_TICK)));
                        values.AddSpellMod(SPELLVALUE_BASE_POINT1, -80);
                        if (TryCastCustom(me->GetVictim(), SPELL_C_MIND_FLAY, values))
                            events.ScheduleEvent(EVENT_BALOR_MIND_FLAY, 25s, 30s);
                        else
                            events.ScheduleEvent(EVENT_BALOR_MIND_FLAY, 100ms);
                        break;
                    }
                    case EVENT_BALOR_PSYCHIC_SCREAM:
                        if (TryCast(me, SPELL_PSYCHIC_SCREAM))
                            events.ScheduleEvent(EVENT_BALOR_PSYCHIC_SCREAM, 15s, 20s);
                        else
                            events.ScheduleEvent(EVENT_BALOR_PSYCHIC_SCREAM, 100ms);
                        break;
                    case EVENT_BALOR_WAILING_DEAD:
                        if (TryCast(me, SPELL_WAILING_DEAD))
                            events.ScheduleEvent(EVENT_BALOR_WAILING_DEAD, 10s, 15s);
                        else
                            events.ScheduleEvent(EVENT_BALOR_WAILING_DEAD, 100ms);
                        break;
                    case EVENT_BALOR_DARK_STRIKE:
                        if (TryCast(me->GetVictim(), SPELL_DARK_STRIKE))
                            events.ScheduleEvent(EVENT_BALOR_DARK_STRIKE, 16s, 22s);
                        else
                            events.ScheduleEvent(EVENT_BALOR_DARK_STRIKE, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Deathlord Tidebane
    // ------------------------------------------------------------------
    enum TidebaneEvents { EVENT_TIDEBANE_RAIN_OF_FIRE = 1, EVENT_TIDEBANE_DARK_PLAGUE, EVENT_TIDEBANE_WAIL_OF_SOULS };

    struct boss_deathlord_tidebaneAI : public TurtleBossAI
    {
        explicit boss_deathlord_tidebaneAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_TIDEBANE_RAIN_OF_FIRE, 9s, 13s);
            events.ScheduleEvent(EVENT_TIDEBANE_DARK_PLAGUE, 4s, 7s);
            events.ScheduleEvent(EVENT_TIDEBANE_WAIL_OF_SOULS, 16s, 22s);
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            Say(me, "Step forth. Accept the cold embrace of death and drown in its bleakness!");
        }

        void JustDied(Unit* /*killer*/) override { Say(me, "The waves... they beckon me..."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_TIDEBANE_RAIN_OF_FIRE:
                        if (TryCast(RandomTarget(SPELL_RAIN_OF_FIRE), SPELL_RAIN_OF_FIRE))
                            events.ScheduleEvent(EVENT_TIDEBANE_RAIN_OF_FIRE, 18s, 24s);
                        else
                            events.ScheduleEvent(EVENT_TIDEBANE_RAIN_OF_FIRE, 100ms);
                        break;
                    case EVENT_TIDEBANE_DARK_PLAGUE:
                        if (TryCast(RandomTarget(SPELL_DARK_PLAGUE), SPELL_DARK_PLAGUE))
                            events.ScheduleEvent(EVENT_TIDEBANE_DARK_PLAGUE, 10s, 14s);
                        else
                            events.ScheduleEvent(EVENT_TIDEBANE_DARK_PLAGUE, 100ms);
                        break;
                    case EVENT_TIDEBANE_WAIL_OF_SOULS:
                        if (TryCast(me, SPELL_WAIL_OF_SOULS))
                        {
                            Say(me, "Darkness shall come, and consume you all!");
                            events.ScheduleEvent(EVENT_TIDEBANE_WAIL_OF_SOULS, 22s, 30s);
                        }
                        else
                            events.ScheduleEvent(EVENT_TIDEBANE_WAIL_OF_SOULS, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Chieftain Stormsong
    // ------------------------------------------------------------------
    enum StormsongEvents { EVENT_STORMSONG_FORKED_LIGHTNING = 1, EVENT_STORMSONG_STUN_BOMB, EVENT_STORMSONG_LIGHTNING_STRIKE };

    struct boss_chieftain_stormsongAI : public TurtleBossAI
    {
        explicit boss_chieftain_stormsongAI(Creature* c) : TurtleBossAI(c) { }

        bool _didThreatReset = false;

        void Reset() override
        {
            _didThreatReset = false;
            events.Reset();
            events.ScheduleEvent(EVENT_STORMSONG_FORKED_LIGHTNING, 5s, 8s);
            events.ScheduleEvent(EVENT_STORMSONG_STUN_BOMB, 25s, 30s);
            events.ScheduleEvent(EVENT_STORMSONG_LIGHTNING_STRIKE, 12s, 16s);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "The dark sea will swallow your souls!"); }
        void JustDied(Unit* /*killer*/) override { Say(me, "You know so little, whelps..."); }

        int32 _strikeNatureDamage = 0;

        // Turtle 52422: 60% weapon damage, melee range, on the victim; on hit
        // 52421 adds 20% weapon damage as nature.
        bool LightningStrike()
        {
            Unit* victim = me->GetVictim();
            if (!victim || !me->IsWithinMeleeRange(victim))
                return false;
            uint32 weapon = me->CalculateDamage(BASE_ATTACK, false, true);
            _strikeNatureDamage = int32(std::lround(weapon * 0.20f));
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_STRIKE_PHYSICAL, EFFECT_0, weapon * 0.60f));
            return TryCastCustom(victim, SPELL_C_STRIKE_PHYSICAL, values);
        }

        void SpellHitTarget(Unit* target, SpellInfo const* spell) override
        {
            if (!target || !spell || spell->Id != SPELL_C_STRIKE_PHYSICAL || _strikeNatureDamage <= 0)
                return;
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_STRIKE_NATURE, EFFECT_0, float(_strikeNatureDamage)));
            me->CastCustomSpell(SPELL_C_STRIKE_NATURE, values, target, TRIGGERED_FULL_MASK);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            // Turtle: threat wipe once at 50% health.
            if (!_didThreatReset && me->GetHealthPct() <= 50.0f)
            {
                DoResetThreatList();
                _didThreatReset = true;
            }

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_STORMSONG_FORKED_LIGHTNING:
                        if (TryCast(me->GetVictim(), SPELL_FORKED_LIGHTNING))
                            events.ScheduleEvent(EVENT_STORMSONG_FORKED_LIGHTNING, 11s, 15s);
                        else
                            events.ScheduleEvent(EVENT_STORMSONG_FORKED_LIGHTNING, 100ms);
                        break;
                    case EVENT_STORMSONG_STUN_BOMB:
                        if (TryCast(RandomTarget(SPELL_STUN_BOMB), SPELL_STUN_BOMB))
                            events.ScheduleEvent(EVENT_STORMSONG_STUN_BOMB, 25s, 30s);
                        else
                            events.ScheduleEvent(EVENT_STORMSONG_STUN_BOMB, 100ms);
                        break;
                    case EVENT_STORMSONG_LIGHTNING_STRIKE:
                        if (LightningStrike())
                            events.ScheduleEvent(EVENT_STORMSONG_LIGHTNING_STRIKE, 14s, 20s);
                        else
                            events.ScheduleEvent(EVENT_STORMSONG_LIGHTNING_STRIKE, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Librarian Theodorus
    // ------------------------------------------------------------------
    enum TheodorusEvents { EVENT_THEODORUS_CONE_OF_COLD = 1, EVENT_THEODORUS_FROSTBOLT, EVENT_THEODORUS_BLIZZARD };

    struct boss_librarian_theodorusAI : public TurtleBossAI
    {
        explicit boss_librarian_theodorusAI(Creature* c) : TurtleBossAI(c) { }

        bool _summonedElemental = false;

        void Reset() override
        {
            _summonedElemental = false;
            summons.DespawnAll();   // no second elemental after a wipe
            events.Reset();
            events.ScheduleEvent(EVENT_THEODORUS_CONE_OF_COLD, 1s);
            events.ScheduleEvent(EVENT_THEODORUS_FROSTBOLT, 4s, 6s);
            events.ScheduleEvent(EVENT_THEODORUS_BLIZZARD, 10s, 14s);

            if (!me->HasAura(SPELL_GHOST_VISUAL))
                me->AddAura(SPELL_GHOST_VISUAL, me);
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            Yell(me, "I must kindly ask you to leave, the archives are not ready for public viewing!");
        }

        void JustDied(Unit* /*killer*/) override
        {
            Yell(me, "These pages were mine to organize... Such great effort, gone to waste!");
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            // Turtle 44100 "Summon Theodorus Elemental" at 50% (summon, 10 min duration).
            if (!_summonedElemental && me->GetHealthPct() <= 50.0f)
            {
                _summonedElemental = true;
                Position pos = me->GetNearPosition(3.0f, 0.0f);
                if (Creature* elemental = me->SummonCreature(NPC_THEODORUS_SEA_ELEMENTAL, pos, TEMPSUMMON_TIMED_OR_DEAD_DESPAWN, 10 * MINUTE * IN_MILLISECONDS))
                    elemental->SetInCombatWithZone();
                Yell(me, "Behold, my signature attack! The great waves of Balor shall destroy you, once and for all!");
            }

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_THEODORUS_CONE_OF_COLD:
                        if (TryCast(me->GetVictim(), SPELL_CONE_OF_COLD))
                            events.ScheduleEvent(EVENT_THEODORUS_CONE_OF_COLD, 15s, 22s);
                        else
                            events.ScheduleEvent(EVENT_THEODORUS_CONE_OF_COLD, 100ms);
                        break;
                    case EVENT_THEODORUS_FROSTBOLT:
                        if (TryCast(RandomTarget(SPELL_FROSTBOLT), SPELL_FROSTBOLT))
                            events.ScheduleEvent(EVENT_THEODORUS_FROSTBOLT, 6s, 9s);
                        else
                            events.ScheduleEvent(EVENT_THEODORUS_FROSTBOLT, 100ms);
                        break;
                    case EVENT_THEODORUS_BLIZZARD:
                        if (TryCast(RandomTarget(SPELL_THEODORUS_BLIZZARD), SPELL_THEODORUS_BLIZZARD))
                            events.ScheduleEvent(EVENT_THEODORUS_BLIZZARD, 16s, 22s);
                        else
                            events.ScheduleEvent(EVENT_THEODORUS_BLIZZARD, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Subjugator Halthas Shadecrest
    // ------------------------------------------------------------------
    enum HalthasEvents { EVENT_HALTHAS_DOMINATE_MIND = 1, EVENT_HALTHAS_FLAMESTRIKE, EVENT_HALTHAS_FEAR };

    struct boss_subjugator_halthas_shadecrestAI : public TurtleBossAI
    {
        explicit boss_subjugator_halthas_shadecrestAI(Creature* c) : TurtleBossAI(c) { }

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_HALTHAS_DOMINATE_MIND, 12s, 16s);
            events.ScheduleEvent(EVENT_HALTHAS_FLAMESTRIKE, 0ms);
            events.ScheduleEvent(EVENT_HALTHAS_FEAR, 18s, 24s);
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "You shall be brought under heel intruder..."); }
        void JustDied(Unit* /*killer*/) override { Say(me, "This cannot be! I was going to change the world!"); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_HALTHAS_DOMINATE_MIND:
                        if (TryCast(me->GetVictim(), SPELL_DOMINATE_MIND))
                        {
                            Say(me, "My will is unbreakable, you shall bend your knee.");
                            events.ScheduleEvent(EVENT_HALTHAS_DOMINATE_MIND, 26s, 34s);
                        }
                        else
                            events.ScheduleEvent(EVENT_HALTHAS_DOMINATE_MIND, 100ms);
                        break;
                    case EVENT_HALTHAS_FLAMESTRIKE:
                        if (TryCast(me->GetVictim(), SPELL_HALTHAS_FLAMESTRIKE))
                            events.ScheduleEvent(EVENT_HALTHAS_FLAMESTRIKE, 12s, 16s);
                        else
                            events.ScheduleEvent(EVENT_HALTHAS_FLAMESTRIKE, 100ms);
                        break;
                    case EVENT_HALTHAS_FEAR:
                        if (TryCast(me, SPELL_HALTHAS_FEAR))
                            events.ScheduleEvent(EVENT_HALTHAS_FEAR, 24s, 32s);
                        else
                            events.ScheduleEvent(EVENT_HALTHAS_FEAR, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Eldermaw the Primordial
    // ------------------------------------------------------------------
    enum EldermawEvents { EVENT_ELDERMAW_TAIL_SLAP = 1 };

    // Turtle 44041 knockback: EffectMiscValue 49 -> horizontal 4.9,
    // damage 500 -> vertical 50.0 (vmangos EffectKnockBack). Kept exact on request.
    constexpr float TAIL_SLAP_SPEED_XY = 4.9f;
    constexpr float TAIL_SLAP_SPEED_Z  = 50.0f;

    struct boss_eldermaw_the_primordialAI : public TurtleBossAI
    {
        explicit boss_eldermaw_the_primordialAI(Creature* c) : TurtleBossAI(c) { }

        bool _calledPrimordial = false;
        bool _primordialBuffUp = false;
        float _buffOrientation = 0.0f;
        std::vector<ObjectGuid> _guardians;

        void Reset() override
        {
            _calledPrimordial = false;
            RemovePrimordialRegeneration();
            DespawnGuardians();
            summons.DespawnAll();
            events.Reset();
            events.ScheduleEvent(EVENT_ELDERMAW_TAIL_SLAP, 4s, 6s);
        }

        void JustDied(Unit* /*killer*/) override
        {
            // Turtle: 44043's guardians die with their owner; the two
            // timed crocolisks from the script keep fighting.
            DespawnGuardians();
        }

        void SpellHitTarget(Unit* target, SpellInfo const* spell) override
        {
            // Knockback only when Tail Slap actually landed (Turtle: one spell).
            if (target && spell && spell->Id == SPELL_C_TAIL_SLAP_DAMAGE)
                target->KnockbackFrom(me->GetPositionX(), me->GetPositionY(), TAIL_SLAP_SPEED_XY, TAIL_SLAP_SPEED_Z);
        }

        void DespawnGuardians()
        {
            for (ObjectGuid const& guid : _guardians)
                if (Creature* croc = ObjectAccessor::GetCreature(*me, guid))
                    if (croc->IsAlive())
                        croc->DespawnOrUnsummon();
            _guardians.clear();
        }

        void RemovePrimordialRegeneration()
        {
            if (!_primordialBuffUp)
                return;
            _primordialBuffUp = false;
            me->RemoveAurasDueToSpell(SPELL_C_PRIMORDIAL_ARMOR, me->GetGUID());
            me->RemoveAurasDueToSpell(SPELL_C_PRIMORDIAL_REGEN, me->GetGUID());
        }

        void SummonCrocolisk(float x, float y, float z, TempSummonType type, uint32 despawnMs, bool guardian)
        {
            if (Creature* croc = me->SummonCreature(NPC_ELDERMAW_CROCOLISK, x, y, z, me->GetOrientation(), type, despawnMs))
            {
                croc->SetInCombatWithZone();
                if (guardian)
                    _guardians.push_back(croc->GetGUID());
            }
        }

        void CallOfThePrimordial()
        {
            // Turtle 44042 Primordial Regeneration: armor +1000, magic resistances +25,
            // 750 health every 2 sec, 10 sec. Turtle's aura breaks when Eldermaw casts,
            // moves, turns or swings (auraInterruptFlags 0x101C) - mirrored in UpdateAI.
            Aura* armor = me->AddAura(SPELL_C_PRIMORDIAL_ARMOR, me);
            TuneAura(armor, 10000, 1000, 25);
            Aura* regen = me->AddAura(SPELL_C_PRIMORDIAL_REGEN, me);
            TuneAura(regen, 10000, 750);
            _primordialBuffUp = armor || regen;
            _buffOrientation = me->GetOrientation();

            me->HandleEmoteCommand(EMOTE_ONESHOT_ROAR);

            // Turtle 44043 Call of the Primordial: two Eldermaw Crocolisk guardians
            // (value 2, permanent, they die with Eldermaw) ...
            for (uint8 i = 0; i < 2; ++i)
            {
                float angle = me->GetOrientation() + float(M_PI) * (0.5f + float(i));
                SummonCrocolisk(me->GetPositionX() + 3.0f * std::cos(angle), me->GetPositionY() + 3.0f * std::sin(angle),
                    me->GetPositionZ(), TEMPSUMMON_DEAD_DESPAWN, 0, true);
            }

            // ... plus the script's two crocolisks beside the boss, 60 sec, zone combat.
            for (uint8 i = 0; i < 2; ++i)
            {
                float angle = me->GetOrientation() + (i == 0 ? 1.0f : -1.0f);
                SummonCrocolisk(me->GetPositionX() + 2.0f * std::cos(angle), me->GetPositionY() + 2.0f * std::sin(angle),
                    me->GetPositionZ(), TEMPSUMMON_TIMED_OR_CORPSE_DESPAWN, 60000, false);
            }
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!_calledPrimordial && me->GetHealthPct() <= 50.0f)
            {
                _calledPrimordial = true;
                CallOfThePrimordial();
            }

            // Turtle 44042 interrupt flags: removed on move / turn / cast.
            if (_primordialBuffUp)
            {
                if (!me->HasAura(SPELL_C_PRIMORDIAL_ARMOR) && !me->HasAura(SPELL_C_PRIMORDIAL_REGEN))
                    _primordialBuffUp = false;
                else if (me->isMoving() || me->HasUnitState(UNIT_STATE_CASTING) || std::fabs(me->GetOrientation() - _buffOrientation) > 0.01f)
                    RemovePrimordialRegeneration();
            }

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_ELDERMAW_TAIL_SLAP:
                    {
                        // Random target in melee range, 200-280 physical + knockback; retry after 1 sec.
                        CustomSpellValues values;
                        values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_TAIL_SLAP_DAMAGE, EFFECT_0, float(urand(200, 280))));
                        if (TryCastCustom(RandomTarget(0, true, false, true), SPELL_C_TAIL_SLAP_DAMAGE, values))
                        {
                            RemovePrimordialRegeneration();     // Turtle: casting breaks it
                            events.ScheduleEvent(EVENT_ELDERMAW_TAIL_SLAP, 10s, 12s);
                        }
                        else
                            events.ScheduleEvent(EVENT_ELDERMAW_TAIL_SLAP, 1s);
                        break;
                    }
                    default:
                        break;
                }
            }

            // Turtle: a melee swing also breaks Primordial Regeneration.
            bool swingReady = _primordialBuffUp && me->isAttackReady(BASE_ATTACK) && me->GetVictim() && me->IsWithinMeleeRange(me->GetVictim());
            DoMeleeAttackIfReady();
            if (swingReady && !me->isAttackReady(BASE_ATTACK))
                RemovePrimordialRegeneration();
        }
    };

    // ------------------------------------------------------------------
    // Mycellakos
    // ------------------------------------------------------------------
    enum MycellakosEvents { EVENT_MYCELLAKOS_FUNGUS = 1, EVENT_MYCELLAKOS_DETONATE, EVENT_MYCELLAKOS_DECAYING_MOLD };

    struct boss_mycellakosAI : public TurtleBossAI
    {
        explicit boss_mycellakosAI(Creature* c) : TurtleBossAI(c) { }

        Position _fungusPos;

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_MYCELLAKOS_FUNGUS, 8s);
            events.ScheduleEvent(EVENT_MYCELLAKOS_DECAYING_MOLD, 25s, 30s);
            summons.DespawnAll();
        }

        void DetonateFungus()
        {
            // Turtle: two Growths of Mycellakos at the mushroom, 60 sec, zone combat.
            for (uint8 i = 0; i < 2; ++i)
            {
                float offset = (i == 0) ? 1.0f : -1.0f;
                if (Creature* growth = me->SummonCreature(NPC_GROWTH_OF_MYCELLAKOS, _fungusPos.GetPositionX() + offset, _fungusPos.GetPositionY(),
                    _fungusPos.GetPositionZ(), _fungusPos.GetOrientation(), TEMPSUMMON_TIMED_OR_CORPSE_DESPAWN, 60000))
                    growth->SetInCombatWithZone();
            }

            Creature* trigger = TriggerAt(_fungusPos, 5000);
            if (!trigger)
                return;

            // Turtle 44048 effect 1: 400-500 nature to every enemy within 5 yd of the mushroom.
            {
                CustomSpellValues values;
                values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(trigger, SPELL_C_FUNGUS_BURST, EFFECT_0, float(urand(400, 500))));
                values.AddSpellMod(SPELLVALUE_RADIUS_MOD, 5000);     // 10 yd * 0.5 = 5 yd
                trigger->CastCustomSpell(SPELL_C_FUNGUS_BURST, values, trigger, TRIGGERED_FULL_MASK, nullptr, nullptr, me->GetGUID());
            }

            // Turtle 44048 effect 2: a 5 yd poison cloud on the ground for 15 sec,
            // 80-120 nature every 3 sec to whoever stands in it. The carrier ticks
            // every 2 sec, so each tick is 2/3 of Turtle's (same damage per second).
            {
                CustomSpellValues values;
                values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(trigger, SPELL_C_FUNGUS_CLOUD, EFFECT_0, float(urand(80, 120)) * 2.0f / 3.0f));
                trigger->CastCustomSpell(SPELL_C_FUNGUS_CLOUD, values, trigger, TRIGGERED_FULL_MASK, nullptr, nullptr, me->GetGUID());
                // A world trigger's ground effect belongs to the original caster (Spell::EffectPersistentAA).
                if (DynamicObject* cloud = me->GetDynObject(SPELL_C_FUNGUS_CLOUD))
                    cloud->SetDuration(15000);
            }
        }

        void DecayingMold()
        {
            // Turtle 44050: disease on every enemy within 20 yd, 75-125 every 7 sec for 14 sec.
            // Carrier ticks every 3 sec: 4 ticks of half the roll = same total over the same 14 sec.
            std::vector<Unit*> enemies;
            EnemiesNear(me, me->GetPosition(), 20.0f, enemies);
            for (Unit* enemy : enemies)
            {
                if (!me->IsValidAttackTarget(enemy))
                    continue;
                if (Aura* mold = me->AddAura(SPELL_C_DECAYING_MOLD, enemy))
                    TuneAura(mold, 14000, int32(urand(75, 125) / 2));
            }
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
                    case EVENT_MYCELLAKOS_FUNGUS:
                        // Turtle: mushroom under the boss, explodes 3 sec later at that spot.
                        _fungusPos = me->GetPosition();
                        me->SummonGameObject(GO_VOLATILE_FUNGUS, _fungusPos.GetPositionX(), _fungusPos.GetPositionY(), _fungusPos.GetPositionZ(),
                            _fungusPos.GetOrientation(), 0.0f, 0.0f, 0.0f, 0.0f, 3);
                        events.ScheduleEvent(EVENT_MYCELLAKOS_DETONATE, 3s);
                        events.ScheduleEvent(EVENT_MYCELLAKOS_FUNGUS, 15s, 20s);
                        break;
                    case EVENT_MYCELLAKOS_DETONATE:
                        DetonateFungus();
                        break;
                    case EVENT_MYCELLAKOS_DECAYING_MOLD:
                        if (!me->HasUnitState(UNIT_STATE_CASTING))
                        {
                            DecayingMold();
                            events.ScheduleEvent(EVENT_MYCELLAKOS_DECAYING_MOLD, 25s, 30s);
                        }
                        else
                            events.ScheduleEvent(EVENT_MYCELLAKOS_DECAYING_MOLD, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Lady Drazare
    // ------------------------------------------------------------------
    enum DrazareEvents { EVENT_DRAZARE_DARK_SEDUCTION = 1, EVENT_DRAZARE_EMBRACE };

    // Damage from a spot near `center`, credited to Drazare when she is alive.
    void DrazareShadowHit(Creature* drazare, Unit* victim, Position const& spot, int32 damage)
    {
        if (!drazare || !victim)
            return;
        Creature* trigger = SpellTrigger(drazare, spot, 5000);
        if (!trigger)
            return;
        CustomSpellValues values;
        values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(trigger, SPELL_C_SHADOW_HIT, EFFECT_0, float(damage)));
        trigger->CastCustomSpell(SPELL_C_SHADOW_HIT, values, victim, TRIGGERED_FULL_MASK, nullptr, nullptr,
            drazare->IsAlive() ? drazare->GetGUID() : ObjectGuid::Empty);
    }

    // Turtle 44051 runs out (not dispelled/broken): 300-350 shadow to the victim.
    void DarkSeductionExpired(Creature* drazare, Unit* victim)
    {
        DrazareShadowHit(drazare, victim, victim->GetPosition(), int32(urand(300, 350)));
    }

    // Turtle 44052 (cast when 44053 expires): 100-150 shadow to every enemy within
    // 10 yd of the cursed player, including them, and a knockback (9.9 / 10.0).
    void DrazaresEmbraceExplosion(Creature* drazare, Unit* victim)
    {
        Position center = victim->GetPosition();
        std::vector<Unit*> enemies;
        EnemiesNear(drazare, center, 10.0f, enemies, false);
        bool victimListed = false;
        for (Unit* u : enemies)
            if (u == victim)
                victimListed = true;
        if (!victimListed && victim->IsAlive())
            enemies.push_back(victim);

        for (Unit* u : enemies)
        {
            DrazareShadowHit(drazare, u, center, int32(urand(100, 150)));
            u->KnockbackFrom(center.GetPositionX(), center.GetPositionY(), 9.9f, 10.0f);
        }
    }

    struct boss_lady_drazareAI : public TurtleBossAI
    {
        explicit boss_lady_drazareAI(Creature* c) : TurtleBossAI(c) { }

        std::vector<ObjectGuid> _debuffed;

        void Reset() override
        {
            events.Reset();
            events.ScheduleEvent(EVENT_DRAZARE_DARK_SEDUCTION, 19s, 20s);
            events.ScheduleEvent(EVENT_DRAZARE_EMBRACE, 12s, 24s);
            _debuffed.clear();
        }

        void JustEngagedWith(Unit* /*who*/) override { Say(me, "New toys, let's hope you will not break so easily..."); }

        // Turtle: her debuffs keep running after she dies (and still explode).
        void JustDied(Unit* /*killer*/) override { Say(me, "Impossible... You... vile..."); }

        void EnterEvadeMode(EvadeReason why) override
        {
            // Wipe: take her debuffs off quietly (removal by default does not explode).
            for (ObjectGuid const& guid : _debuffed)
                if (Unit* u = ObjectAccessor::GetUnit(*me, guid))
                {
                    u->RemoveAurasDueToSpell(SPELL_C_SEDUCTION, me->GetGUID());
                    u->RemoveAurasDueToSpell(SPELL_C_EMBRACE_CURSE, me->GetGUID());
                }
            _debuffed.clear();
            TurtleBossAI::EnterEvadeMode(why);
        }

        // Turtle 44051: random player within 30 yd, 6 sec stun that damage does not
        // break, 300-350 shadow when it runs out (see the aura-remove hook below).
        bool DarkSeduction()
        {
            Unit* target = RandomTarget(0, true, true);
            if (!target || me->GetDistance(target) > 30.0f)
                return false;
            Aura* aura = me->AddAura(SPELL_C_SEDUCTION, target);
            if (!aura)
                return false;
            TuneAura(aura, 6000);
            me->SendPlaySpellVisual(SEDUCTION_CAST_KIT);
            _debuffed.push_back(target->GetGUID());
            return true;
        }

        // Turtle 44053: random player within 30 yd, 8 sec curse; if it runs out
        // (not decursed), 44052 explodes around them (see the hook below).
        bool DrazaresEmbrace()
        {
            Unit* target = RandomTarget(0, true, true);
            if (!target || me->GetDistance(target) > 30.0f)
                return false;
            Aura* aura = me->AddAura(SPELL_C_EMBRACE_CURSE, target);
            if (!aura)
                return false;
            TuneAura(aura, 8000);
            _debuffed.push_back(target->GetGUID());
            return true;
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
                    case EVENT_DRAZARE_DARK_SEDUCTION:
                        if (!me->HasUnitState(UNIT_STATE_CASTING) && DarkSeduction())
                        {
                            Say(me, "Share your darkest secrets with me!");
                            events.ScheduleEvent(EVENT_DRAZARE_DARK_SEDUCTION, 39s, 58s);
                        }
                        else
                            events.ScheduleEvent(EVENT_DRAZARE_DARK_SEDUCTION, 100ms);
                        break;
                    case EVENT_DRAZARE_EMBRACE:
                        if (!me->HasUnitState(UNIT_STATE_CASTING) && DrazaresEmbrace())
                            events.ScheduleEvent(EVENT_DRAZARE_EMBRACE, 12s, 24s);
                        else
                            events.ScheduleEvent(EVENT_DRAZARE_EMBRACE, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // Turtle used an AuraScript (AURA_REMOVE_BY_EXPIRE) for these two debuffs.
    // Same here: only a natural expiry triggers the effect; a dispel, a death or
    // the boss evading does not. Filtered on Drazare as caster, so the carrier
    // spells behave normally everywhere else.
    class turtle_drazare_debuffs : public UnitScript
    {
    public:
        turtle_drazare_debuffs() : UnitScript("turtle_drazare_debuffs", true, { UNITHOOK_ON_AURA_REMOVE }) { }

        void OnAuraRemove(Unit* unit, AuraApplication* aurApp, AuraRemoveMode mode) override
        {
            if (mode != AURA_REMOVE_BY_EXPIRE || !unit || !aurApp)
                return;
            Aura const* aura = aurApp->GetBase();
            if (!aura)
                return;
            uint32 spellId = aura->GetId();
            if (spellId != SPELL_C_SEDUCTION && spellId != SPELL_C_EMBRACE_CURSE)
                return;
            ObjectGuid casterGuid = aura->GetCasterGUID();
            if (!casterGuid.IsCreature() || casterGuid.GetEntry() != NPC_LADY_DRAZARE)
                return;
            if (!unit->IsAlive() || !unit->IsInWorld())
                return;
            Creature* drazare = ObjectAccessor::GetCreature(*unit, casterGuid);
            if (!drazare)
                return;

            if (spellId == SPELL_C_SEDUCTION)
                DarkSeductionExpired(drazare, unit);
            else
                DrazaresEmbraceExplosion(drazare, unit);
        }
    };

    // 3.3.5 Death Coil heals its caster for 3x the damage (EffectValueMultiplier 3);
    // Turtle's healed Ighal'for for the damage dealt. ModifyHealReceived runs
    // before the heal is applied and logged, so the combat log shows the real value.
    class turtle_ighalfor_death_coil : public UnitScript
    {
    public:
        turtle_ighalfor_death_coil() : UnitScript("turtle_ighalfor_death_coil", true, { UNITHOOK_MODIFY_HEAL_RECEIVED }) { }

        void ModifyHealReceived(Unit* target, Unit* healer, uint32& heal, SpellInfo const* spellInfo) override
        {
            if (!spellInfo || spellInfo->Id != SPELL_DEATH_COIL || !target || !healer)
                return;
            if (target != healer || healer->GetEntry() != NPC_IGHALFOR || !healer->IsCreature())
                return;
            float multiplier = spellInfo->Effects[EFFECT_0].CalcValueMultiplier(healer);
            if (multiplier > 1.0f)
                heal = uint32(std::lround(float(heal) / multiplier));
        }
    };

    // ------------------------------------------------------------------
    // Ighal'for and Mergothid
    // ------------------------------------------------------------------
    enum IghalforEvents { EVENT_IGHALFOR_DEATH_COIL = 1, EVENT_IGHALFOR_FLAMESTRIKE, EVENT_IGHALFOR_CURSE_OF_AGONY };

    enum MergothidActions { ACTION_MERGOTHID_RELEASE = 1 };

    void SetAttackable(Creature* creature, bool attackable)
    {
        if (!creature)
            return;

        if (attackable)
        {
            creature->RemoveUnitFlag(UNIT_FLAG_NON_ATTACKABLE);
            creature->RemoveUnitFlag(UNIT_FLAG_NOT_SELECTABLE);
            creature->SetReactState(REACT_AGGRESSIVE);
        }
        else
        {
            creature->SetUnitFlag(UNIT_FLAG_NON_ATTACKABLE);
            creature->SetUnitFlag(UNIT_FLAG_NOT_SELECTABLE);
            creature->SetReactState(REACT_PASSIVE);
            creature->AttackStop();
            creature->ClearTarget();
        }
    }

    struct boss_ighalforAI : public TurtleBossAI
    {
        explicit boss_ighalforAI(Creature* c) : TurtleBossAI(c) { }

        ObjectGuid _mergothidGuid;
        bool _phaseTriggered = false;
        bool _channeling = false;
        bool _impsAt5 = false;
        bool _impsAt20 = false;
        bool _impsAt35 = false;
        bool _mergothidLine = false;
        bool _mergothidSummoned = false;
        bool _mergothidReleased = false;
        bool _templeLine = false;
        uint32 _channelTimer = 0;

        void Reset() override
        {
            StopChanneling();
            SetAttackable(me, true);
            DespawnEverything();

            _mergothidGuid.Clear();
            _phaseTriggered = false;
            _channeling = false;
            _impsAt5 = _impsAt20 = _impsAt35 = false;
            _mergothidLine = false;
            _mergothidSummoned = false;
            _mergothidReleased = false;
            _templeLine = false;
            _channelTimer = 0;

            events.Reset();
            events.ScheduleEvent(EVENT_IGHALFOR_DEATH_COIL, 12s);
            events.ScheduleEvent(EVENT_IGHALFOR_FLAMESTRIKE, 7s);
            events.ScheduleEvent(EVENT_IGHALFOR_CURSE_OF_AGONY, 18s);
        }

        bool InChannelPhase() const { return _phaseTriggered && !_mergothidReleased; }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "Your intrusion ends here!"); }

        void MoveInLineOfSight(Unit* who) override
        {
            if (!_templeLine && !me->IsInCombat() && who && who->IsPlayer() && !who->ToPlayer()->IsGameMaster()
                && who->IsWithinDistInMap(me, 80.0f) && who->IsWithinLOSInMap(me))
            {
                _templeLine = true;
                Yell(me, "My master prepared me for this moment. Those ignorant to his truth will perish by my hands.");
            }

            TurtleBossAI::MoveInLineOfSight(who);
        }

        void AttackStart(Unit* who) override
        {
            if (InChannelPhase())
                return;
            TurtleBossAI::AttackStart(who);
        }

        void DamageTaken(Unit* attacker, uint32& damage, DamageEffectType damagetype, SpellSchoolMask schoolMask) override
        {
            // Untouchable while channeling (lingering DoTs must not kill him mid-ritual).
            if (InChannelPhase())
                damage = 0;
            TurtleBossAI::DamageTaken(attacker, damage, damagetype, schoolMask);
        }

        void JustDied(Unit* /*killer*/) override
        {
            StopChanneling();
            // Turtle despawns only the imps; Mergothid fights on (he has his own loot).
            summons.DespawnEntry(NPC_NETHER_IMP);
            if (Creature* mergothid = GetMergothid())
                if (!_mergothidReleased && mergothid->IsAlive() && mergothid->AI())
                    mergothid->AI()->DoAction(ACTION_MERGOTHID_RELEASE);
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            StopChanneling();
            DespawnEverything();
            TurtleBossAI::EnterEvadeMode(why);
        }

        void DespawnEverything()
        {
            // Turtle left Mergothid behind after a wipe; despawn him too so the
            // next attempt starts clean.
            summons.DespawnAll();
            if (Creature* mergothid = GetMergothid())
                if (mergothid->IsAlive())
                    mergothid->DespawnOrUnsummon();
        }

        Creature* GetMergothid() const
        {
            if (_mergothidGuid.IsEmpty())
                return nullptr;
            return ObjectAccessor::GetCreature(*me, _mergothidGuid);
        }

        Position AltarPosition() const
        {
            if (GameObject* altar = me->FindNearestGameObject(GO_BLOODSTONE_ALTAR, 120.0f))
                return altar->GetPosition();
            return AltarFallbackPos;
        }

        void StartPhaseTransition()
        {
            _phaseTriggered = true;
            SetAttackable(me, false);
            Yell(me, "Enough! The Bloodstone is ready; savor the last fleeting moments of your life!");

            me->GetMotionMaster()->Clear();
            me->AttackStop();
            Position home = me->GetHomePosition();
            me->NearTeleportTo(home.GetPositionX(), home.GetPositionY(), home.GetPositionZ(), home.GetOrientation());

            _channeling = true;
            _channelTimer = 0;
            me->StopMoving();

            if (GameObject* altar = me->FindNearestGameObject(GO_BLOODSTONE_ALTAR, 120.0f))
                me->SetFacingToObject(altar);
            me->CastSpell(me, SPELL_IGHALFOR_CHANNELING, true);
        }

        void StopChanneling()
        {
            me->InterruptNonMeleeSpells(false);
            me->RemoveAurasDueToSpell(SPELL_IGHALFOR_CHANNELING);
            _channeling = false;
        }

        void SpawnImpWave()
        {
            Position altar = AltarPosition();
            static float const offsets[3][2] = { { 1.5f, 0.0f }, { -0.75f, 1.3f }, { -0.75f, -1.3f } };
            for (uint8 i = 0; i < 3; ++i)
            {
                if (Creature* imp = me->SummonCreature(NPC_NETHER_IMP, altar.GetPositionX() + offsets[i][0], altar.GetPositionY() + offsets[i][1],
                    altar.GetPositionZ(), altar.GetOrientation(), TEMPSUMMON_TIMED_OR_CORPSE_DESPAWN, 2 * MINUTE * IN_MILLISECONDS))
                    CopyThreatTo(imp);
            }
        }

        void SpawnMergothid()
        {
            Position altar = AltarPosition();
            if (Creature* mergothid = me->SummonCreature(NPC_MERGOTHID, altar, TEMPSUMMON_DEAD_DESPAWN))
            {
                SetAttackable(mergothid, false);
                _mergothidGuid = mergothid->GetGUID();
            }
        }

        void FinishChanneling()
        {
            _mergothidReleased = true;
            StopChanneling();
            SetAttackable(me, true);

            if (Unit* top = SelectTarget(SelectTargetMethod::MaxThreat, 0))
                AttackStart(top);

            if (Creature* mergothid = GetMergothid())
            {
                Yell(mergothid, "Too soon, incessant weakling. Your pathetic soul will be the compensation for your failure.");
                SetAttackable(mergothid, true);
                CopyThreatTo(mergothid);
            }
        }

        void UpdateChannel(uint32 diff)
        {
            _channelTimer += diff;

            if (!_impsAt5 && _channelTimer >= 5 * IN_MILLISECONDS)
            {
                _impsAt5 = true;
                SpawnImpWave();
            }
            if (!_impsAt20 && _channelTimer >= 20 * IN_MILLISECONDS)
            {
                _impsAt20 = true;
                SpawnImpWave();
            }
            if (!_impsAt35 && _channelTimer >= 35 * IN_MILLISECONDS)
            {
                _impsAt35 = true;
                SpawnImpWave();
            }
            if (!_mergothidLine && _channelTimer >= 38 * IN_MILLISECONDS)
            {
                _mergothidLine = true;
                Yell(me, "Great Mergothid, lay your eyes upon this feast of souls!");
            }
            if (!_mergothidSummoned && _channelTimer >= 40 * IN_MILLISECONDS)
            {
                _mergothidSummoned = true;
                SpawnMergothid();
            }
            if (!_mergothidReleased && _channelTimer >= 48 * IN_MILLISECONDS)
                FinishChanneling();
        }

        void UpdateAI(uint32 diff) override
        {
            if (_channeling && !_mergothidReleased)
            {
                // Passive while channeling: UpdateVictim keeps combat and evades on a wipe.
                if (!UpdateVictim())
                    return;
                UpdateChannel(diff);
                return;
            }

            if (!UpdateVictim())
                return;

            if (!_phaseTriggered && me->HealthBelowPct(25))
            {
                StartPhaseTransition();
                return;
            }

            if (_phaseTriggered && !_mergothidReleased)
                return;

            events.Update(diff);
            while (uint32 eventId = events.ExecuteEvent())
            {
                switch (eventId)
                {
                    case EVENT_IGHALFOR_DEATH_COIL:
                    {
                        CustomSpellValues values;
                        values.AddSpellMod(SPELLVALUE_BASE_POINT0, 287);   // Turtle value
                        if (TryCastCustom(RandomTarget(SPELL_DEATH_COIL), SPELL_DEATH_COIL, values))
                            events.ScheduleEvent(EVENT_IGHALFOR_DEATH_COIL, 22s);
                        else
                            events.ScheduleEvent(EVENT_IGHALFOR_DEATH_COIL, 100ms);
                        break;
                    }
                    case EVENT_IGHALFOR_FLAMESTRIKE:
                        if (TryCast(RandomTarget(SPELL_FLAMESTRIKE), SPELL_FLAMESTRIKE))
                            events.ScheduleEvent(EVENT_IGHALFOR_FLAMESTRIKE, 24s);
                        else
                            events.ScheduleEvent(EVENT_IGHALFOR_FLAMESTRIKE, 100ms);
                        break;
                    case EVENT_IGHALFOR_CURSE_OF_AGONY:
                        if (TryCast(RandomTarget(SPELL_CURSE_OF_AGONY), SPELL_CURSE_OF_AGONY))
                            events.ScheduleEvent(EVENT_IGHALFOR_CURSE_OF_AGONY, 26s);
                        else
                            events.ScheduleEvent(EVENT_IGHALFOR_CURSE_OF_AGONY, 100ms);
                        break;
                    default:
                        break;
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    struct boss_mergothidAI : public TurtleBossAI
    {
        explicit boss_mergothidAI(Creature* c) : TurtleBossAI(c) { }

        bool _moreSouls = false;

        void Reset() override { _moreSouls = false; }

        void DoAction(int32 action) override
        {
            // Safety release if Ighal'for dies before releasing him.
            if (action != ACTION_MERGOTHID_RELEASE)
                return;
            SetAttackable(me, true);
            me->SetInCombatWithZone();
        }

        void JustDied(Unit* /*killer*/) override { Yell(me, "The nether, calls yet again!"); }

        void UpdateAI(uint32 /*diff*/) override
        {
            if (!_moreSouls && me->HealthBelowPct(50))
            {
                _moreSouls = true;
                Yell(me, "More souls to feast upon!");
            }

            if (!UpdateVictim())
                return;

            DoMeleeAttackIfReady();
        }
    };

    template <class AI>
    CreatureAI* MakeStormwrought(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_stormwrought_ruins()
{
    RegisterAI(NPC_DAGAR_THE_GLUTTON,       &MakeStormwrought<boss_dagar_the_gluttonAI>);
    RegisterAI(NPC_ORONOK_TORN_HEART,       &MakeStormwrought<boss_oronok_torn_heartAI>);
    RegisterAI(NPC_DUKE_BALOR_IV,           &MakeStormwrought<boss_duke_balor_ivAI>);
    RegisterAI(NPC_DEATHLORD_TIDEBANE,      &MakeStormwrought<boss_deathlord_tidebaneAI>);
    RegisterAI(NPC_CHIEFTAIN_STORMSONG,     &MakeStormwrought<boss_chieftain_stormsongAI>);
    RegisterAI(NPC_LIBRARIAN_THEODORUS,     &MakeStormwrought<boss_librarian_theodorusAI>);
    RegisterAI(NPC_HALTHAS_SHADECREST,      &MakeStormwrought<boss_subjugator_halthas_shadecrestAI>);
    RegisterAI(NPC_ELDERMAW,                &MakeStormwrought<boss_eldermaw_the_primordialAI>);
    RegisterAI(NPC_MYCELLAKOS,              &MakeStormwrought<boss_mycellakosAI>);
    RegisterAI(NPC_LADY_DRAZARE,            &MakeStormwrought<boss_lady_drazareAI>);
    RegisterAI(NPC_IGHALFOR,                &MakeStormwrought<boss_ighalforAI>);
    RegisterAI(NPC_MERGOTHID,               &MakeStormwrought<boss_mergothidAI>);

    // Summoned adds: plain melee, the summoner puts them in combat.
    RegisterAI(NPC_NETHER_IMP,              &MakeStormwrought<TurtleAddAI>);
    RegisterAI(NPC_ELDERMAW_CROCOLISK,      &MakeStormwrought<TurtleAddAI>);
    RegisterAI(NPC_GROWTH_OF_MYCELLAKOS,    &MakeStormwrought<TurtleAddAI>);
    RegisterAI(NPC_THEODORUS_SEA_ELEMENTAL, &MakeStormwrought<TurtleAddAI>);

    new turtle_drazare_debuffs();
    new turtle_ighalfor_death_coil();
}
