/*
 * mod-turtle-content - Dragonmaw Retreat (map 816) boss scripts.
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/dragonmaw_retreat
 * (boss_bogpaw_truthsay.cpp, boss_gowlfang.cpp, boss_halgan_redbrand.cpp,
 * boss_searistrasz.cpp, boss_zuluhed_the_whacked.cpp,
 * instance_dragonmaw_retreat.cpp). Timers, targets and texts follow the
 * Turtle scripts line for line.
 *
 * The other Dragonmaw bosses (Cavernweb Broodmother, Web Master Torkon,
 * Slagfist Destroyer, Overlord Blackheart, Garlok Flamekeeper, Elder
 * Hollowblood) have no Turtle C++ AI and keep their converted SmartAI.
 *
 * Turtle-only spells (ids 52042-52046 and 52249 are other spells in 3.3.5)
 * are rebuilt from 3.3.5 carrier spells with Turtle's values (read from the
 * Turtle server Spell.dbc).
 */

#include "turtle_boss_common.h"
#include "InstanceScript.h"
#include "Map.h"
#include "MapInstanced.h"
#include "ScriptMgr.h"
#include "AllMapScript.h"
#include "UnitScript.h"
#include <mutex>
#include <set>
#include <unordered_map>

using namespace TurtleBoss;

namespace
{
    constexpr uint32 MAP_DRAGONMAW_RETREAT = 816;

    enum DragonmawCreatures
    {
        NPC_ZULUHED_THE_WHACKED      = 62037,
        NPC_BOGPAW_TRUTHSAY          = 62056,
        NPC_GOWLFANG                 = 62057,
        NPC_HALGAN_REDBRAND          = 62069,
        NPC_SEARISTRASZ              = 62072,
        NPC_DRAGONMAW_ENCHANTER      = 62453,
    };

    constexpr uint32 MAX_DRAGONMAW_ENCHANTERS = 6;

    enum DragonmawSpells
    {
        // Same spell, same data in both cores
        SPELL_ENTANGLING_ROOTS       = 22415,
        SPELL_LIGHTNING_CLOUD        = 19513,
        SPELL_HEALING_WAVE           = 10395,
        SPELL_INTIMIDATING_ROAR      = 8715,   // "Terrifying Howl" in both DBCs
        SPELL_CURSE_OF_AGONY         = 11711,
        SPELL_PSYCHIC_SCREAM         = 22884,
        SPELL_FIREBALL               = 8401,
        SPELL_FLAME_BREATH           = 16396,
        SPELL_WING_FLAP              = 12882,

        // Same id, different damage carrier: Turtle 17311 ticks 42/sec as a
        // plain periodic; 3.3.5 17311 ticks through 58381 with its effect 2 value (36).
        SPELL_MIND_FLAY              = 17311,

        // Carriers for Turtle-only spells
        SPELL_C_SOUL_DOMINATION      = 15859,  // Turtle 52042: charm up to lvl 63, +100% attack time, 6 sec (Turtle casts in 3 sec, carrier in 2)
        SPELL_C_WITHERING_VISUAL     = 8734,   // Turtle 52044 visual 1124 (same attributes, dummy aura)
        SPELL_C_WITHERING_STUN       = 15660,  // Turtle 52044: self stun 6 sec
        SPELL_C_DEBILITATED_STATS    = 12530,  // Turtle 52045: all stats -25, 2 min, magic
        SPELL_C_DEBILITATED_SCALE    = 8066,   // Turtle 52045: scale -25% (and Turtle's visual 831)
        SPELL_C_EMPOWERED_SOUL       = 70371,  // Turtle 52046: +65% attack speed, +100% scale, 20 sec, enrage, visual 870
        SPELL_C_EMPOWERED_SLOW       = 31086,  // Turtle 52046: -40% movement speed
        SPELL_C_ENCHANTING_FLAMES    = 62733,  // Turtle 52249: -95% damage taken, permanent
        SPELL_C_ENCHANTING_VISUAL    = 16003,  // Turtle 52249 visual 46 (Immolate flames)
    };

    // Turtle values for the carriers above.
    constexpr int32 SOUL_DOMINATION_MAX_LEVEL   = 63;
    constexpr int32 SOUL_DOMINATION_DURATION    = 6000;
    constexpr int32 WITHERING_SOUL_DURATION     = 6000;
    constexpr int32 DEBILITATED_SOUL_DURATION   = 120000;
    constexpr float DEBILITATED_SOUL_RADIUS     = 200.0f;
    constexpr int32 DEBILITATED_SOUL_STATS      = -25;
    constexpr int32 DEBILITATED_SOUL_SCALE      = -25;
    constexpr int32 EMPOWERED_SOUL_DURATION     = 20000;
    constexpr int32 EMPOWERED_SOUL_HASTE        = 65;
    constexpr int32 EMPOWERED_SOUL_SCALE        = 100;
    constexpr int32 EMPOWERED_SOUL_SLOW         = -40;
    constexpr int32 ENCHANTING_FLAMES_REDUCTION = -95;
    constexpr float MIND_FLAY_TICK              = 42.0f;
    constexpr uint32 SOUL_SEQUENCE_DELAY        = 6500;

    // ------------------------------------------------------------------
    // instance_dragonmaw_retreat: dead Dragonmaw Enchanters per instance.
    // ------------------------------------------------------------------
    std::mutex s_enchanterLock;
    std::unordered_map<uint32, std::set<ObjectGuid>> s_deadEnchanters;
    std::unordered_map<uint32, ObjectGuid> s_searistrasz;   // OnCreatureCreate(NPC_SEARISTRASZ)

    void SetSearistraszGuid(Creature* searistrasz)
    {
        std::lock_guard<std::mutex> guard(s_enchanterLock);
        s_searistrasz[searistrasz->GetMap()->GetInstanceId()] = searistrasz->GetGUID();
    }

    ObjectGuid SearistraszGuid(Map const* map)
    {
        std::lock_guard<std::mutex> guard(s_enchanterLock);
        auto itr = s_searistrasz.find(map->GetInstanceId());
        return itr == s_searistrasz.end() ? ObjectGuid::Empty : itr->second;
    }

    uint32 DeadEnchanters(Map const* map)
    {
        std::lock_guard<std::mutex> guard(s_enchanterLock);
        auto itr = s_deadEnchanters.find(map->GetInstanceId());
        return itr == s_deadEnchanters.end() ? 0 : uint32(itr->second.size());
    }

    uint32 MarkEnchanterDead(Creature* enchanter)
    {
        std::lock_guard<std::mutex> guard(s_enchanterLock);
        std::set<ObjectGuid>& dead = s_deadEnchanters[enchanter->GetMap()->GetInstanceId()];
        dead.insert(enchanter->GetGUID());
        return uint32(dead.size());
    }

    void ApplyEnchantingFlames(Creature* searistrasz)
    {
        if (!searistrasz->HasAura(SPELL_C_ENCHANTING_FLAMES))
            if (Aura* aura = searistrasz->AddAura(SPELL_C_ENCHANTING_FLAMES, searistrasz))
                TuneAura(aura, -1, ENCHANTING_FLAMES_REDUCTION);
        if (!searistrasz->HasAura(SPELL_C_ENCHANTING_VISUAL))
            searistrasz->AddAura(SPELL_C_ENCHANTING_VISUAL, searistrasz);
    }

    void RemoveEnchantingFlames(Creature* searistrasz)
    {
        searistrasz->RemoveAurasDueToSpell(SPELL_C_ENCHANTING_FLAMES);
        searistrasz->RemoveAurasDueToSpell(SPELL_C_ENCHANTING_VISUAL);
    }

    // Bogpaw and Zuluhed are warrior-class (no mana) in the converted
    // creature_template; Turtle's creatures cast Healing Wave and Soul
    // Domination anyway, so those two skip the power cost.
    struct DragonmawBossAI : public TurtleBossAI
    {
        explicit DragonmawBossAI(Creature* c) : TurtleBossAI(c) { }

        // vmangos SelectAttackingTarget(RANDOM, 0, spell, IN_LOS | NO_TOTEM), else the victim.
        Unit* RandomOrVictim(uint32 spellId, bool playerOnly = false, bool meleeOnly = false)
        {
            if (Unit* target = RandomTarget(spellId, !meleeOnly, playerOnly, meleeOnly))
                return target;
            return me->GetVictim();
        }
    };

    // ------------------------------------------------------------------
    // Bogpaw Truthsay
    // ------------------------------------------------------------------
    struct boss_bogpaw_truthsayAI : public DragonmawBossAI
    {
        explicit boss_bogpaw_truthsayAI(Creature* c) : DragonmawBossAI(c) { }

        uint32 _entanglingRootsTimer = 0;
        uint32 _lightningCloudTimer = 0;
        uint32 _healingWaveTimer = 0;

        void Reset() override
        {
            _entanglingRootsTimer = urand(5 * IN_MILLISECONDS, 7 * IN_MILLISECONDS);
            _lightningCloudTimer = urand(2 * IN_MILLISECONDS, 4 * IN_MILLISECONDS);
            _healingWaveTimer = urand(6 * IN_MILLISECONDS, 8 * IN_MILLISECONDS);
        }

        Unit* SelectHealingTarget()
        {
            Unit* target = nullptr;

            if (Creature* gowlfang = me->FindNearestCreature(NPC_GOWLFANG, 80.0f, true))
                if (gowlfang->GetHealthPct() <= 50.0f)
                    target = gowlfang;

            if (me->GetHealthPct() <= 50.0f && (!target || me->GetHealthPct() < target->GetHealthPct()))
                target = me;

            return target;
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (_healingWaveTimer < diff)
            {
                if (Unit* target = SelectHealingTarget())
                {
                    if (TryCastNoCost(target, SPELL_HEALING_WAVE))
                        _healingWaveTimer = urand(8 * IN_MILLISECONDS, 11 * IN_MILLISECONDS);
                }
                else
                    _healingWaveTimer = urand(2 * IN_MILLISECONDS, 3 * IN_MILLISECONDS);
            }
            else
                _healingWaveTimer -= diff;

            if (_lightningCloudTimer < diff)
            {
                if (Unit* target = RandomOrVictim(SPELL_LIGHTNING_CLOUD))
                    if (TryCast(target, SPELL_LIGHTNING_CLOUD))
                        _lightningCloudTimer = urand(18 * IN_MILLISECONDS, 24 * IN_MILLISECONDS);
            }
            else
                _lightningCloudTimer -= diff;

            if (_entanglingRootsTimer < diff)
            {
                if (Unit* target = RandomOrVictim(SPELL_ENTANGLING_ROOTS))
                    if (TryCast(target, SPELL_ENTANGLING_ROOTS))
                        _entanglingRootsTimer = urand(12 * IN_MILLISECONDS, 15 * IN_MILLISECONDS);
            }
            else
                _entanglingRootsTimer -= diff;

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Gowlfang
    // ------------------------------------------------------------------
    struct boss_gowlfangAI : public DragonmawBossAI
    {
        explicit boss_gowlfangAI(Creature* c) : DragonmawBossAI(c) { }

        bool _usedIntimidatingRoar = false;

        void Reset() override { _usedIntimidatingRoar = false; }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "Who messes with Mosshide? We gnolls are strongest!"); }
        void JustDied(Unit* /*killer*/) override { Yell(me, "Mosshide is mine! No-no one else..."); }

        void UpdateAI(uint32 /*diff*/) override
        {
            if (!UpdateVictim())
                return;

            if (!_usedIntimidatingRoar && me->GetHealthPct() <= 50.0f)
            {
                if (TryCast(me, SPELL_INTIMIDATING_ROAR))
                {
                    _usedIntimidatingRoar = true;
                    Yell(me, "No one defeats Gowlfang, I am leader!");
                    DoResetThreatList();
                }
            }

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Halgan Redbrand
    // ------------------------------------------------------------------
    struct boss_halgan_redbrandAI : public DragonmawBossAI
    {
        explicit boss_halgan_redbrandAI(Creature* c) : DragonmawBossAI(c) { }

        uint32 _curseOfAgonyTimer = 0;
        uint32 _mindFlayTimer = 0;
        bool _usedPsychicScream = false;

        void Reset() override
        {
            _curseOfAgonyTimer = urand(2 * IN_MILLISECONDS, 4 * IN_MILLISECONDS);
            _mindFlayTimer = urand(5 * IN_MILLISECONDS, 7 * IN_MILLISECONDS);
            _usedPsychicScream = false;
        }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "These halls are a sacred place, you can go no further."); }
        void JustDied(Unit* /*killer*/) override { Yell(me, "To the great... Beyond."); }

        bool CastMindFlay(Unit* target)
        {
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT2, BasePointsFor(me, SPELL_MIND_FLAY, EFFECT_2, MIND_FLAY_TICK));
            return TryCastCustom(target, SPELL_MIND_FLAY, values);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!_usedPsychicScream && me->GetHealthPct() <= 50.0f)
            {
                if (TryCast(me->GetVictim(), SPELL_PSYCHIC_SCREAM))
                {
                    _usedPsychicScream = true;
                    Yell(me, "I shall not falter.");
                }
            }

            if (_curseOfAgonyTimer < diff)
            {
                if (Unit* target = RandomOrVictim(SPELL_CURSE_OF_AGONY))
                    if (TryCast(target, SPELL_CURSE_OF_AGONY))
                        _curseOfAgonyTimer = urand(14 * IN_MILLISECONDS, 18 * IN_MILLISECONDS);
            }
            else
                _curseOfAgonyTimer -= diff;

            if (_mindFlayTimer < diff)
            {
                if (Unit* target = RandomOrVictim(SPELL_MIND_FLAY))
                    if (CastMindFlay(target))
                        _mindFlayTimer = urand(10 * IN_MILLISECONDS, 14 * IN_MILLISECONDS);
            }
            else
                _mindFlayTimer -= diff;

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Searistrasz
    // ------------------------------------------------------------------
    struct boss_searistraszAI : public DragonmawBossAI
    {
        explicit boss_searistraszAI(Creature* c) : DragonmawBossAI(c) { SetSearistraszGuid(c); }

        uint32 _fireballTimer = 0;
        uint32 _flameBreathTimer = 0;
        uint32 _wingFlapTimer = 0;
        bool _usedHalfHealthLine = false;

        void Reset() override
        {
            _fireballTimer = urand(5 * IN_MILLISECONDS, 7 * IN_MILLISECONDS);
            _flameBreathTimer = urand(2 * IN_MILLISECONDS, 4 * IN_MILLISECONDS);
            _wingFlapTimer = urand(500, 1500);
            _usedHalfHealthLine = false;

            if (DeadEnchanters(me->GetMap()) < MAX_DRAGONMAW_ENCHANTERS)
                ApplyEnchantingFlames(me);
            else
                RemoveEnchantingFlames(me);
        }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "This sanctum is mine... Begone from this place."); }
        void JustDied(Unit* /*killer*/) override { Yell(me, "I am... Free, once again."); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (!_usedHalfHealthLine && me->GetHealthPct() <= 50.0f)
            {
                _usedHalfHealthLine = true;
                Yell(me, "Bathe in fire, and fury.");
            }

            if (_wingFlapTimer < diff)
            {
                if (TryCast(RandomOrVictim(SPELL_WING_FLAP, false, true), SPELL_WING_FLAP))
                    _wingFlapTimer = urand(15 * IN_MILLISECONDS, 18 * IN_MILLISECONDS);
            }
            else
                _wingFlapTimer -= diff;

            if (_flameBreathTimer < diff)
            {
                if (TryCast(me->GetVictim(), SPELL_FLAME_BREATH))
                    _flameBreathTimer = urand(28 * IN_MILLISECONDS, 36 * IN_MILLISECONDS);
            }
            else
                _flameBreathTimer -= diff;

            if (_fireballTimer < diff)
            {
                if (TryCast(RandomOrVictim(SPELL_FIREBALL), SPELL_FIREBALL))
                    _fireballTimer = urand(18 * IN_MILLISECONDS, 23 * IN_MILLISECONDS);
            }
            else
                _fireballTimer -= diff;

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Zuluhed the Whacked
    // ------------------------------------------------------------------
    struct boss_zuluhed_the_whackedAI : public DragonmawBossAI
    {
        explicit boss_zuluhed_the_whackedAI(Creature* c) : DragonmawBossAI(c) { }

        uint32 _soulDominationTimer = 0;
        uint32 _soulSequenceTimer = 0;
        bool _soulSequenceStarted = false;
        bool _soulSequenceFinished = false;

        void Reset() override
        {
            _soulDominationTimer = urand(6 * IN_MILLISECONDS, 8 * IN_MILLISECONDS);
            _soulSequenceTimer = 0;
            _soulSequenceStarted = false;
            _soulSequenceFinished = false;
        }

        void JustEngagedWith(Unit* /*who*/) override { Yell(me, "The Dragonmaw Clan shall live forever!"); }
        void JustDied(Unit* /*killer*/) override { Yell(me, "The Dragonmaw will never be destroyed... Another will take my place, whelps!"); }

        // Soul Domination lasts 6 sec in Turtle (carrier: 5 sec).
        void SpellHitTarget(Unit* target, SpellInfo const* spell) override
        {
            if (target && spell && spell->Id == SPELL_C_SOUL_DOMINATION)
                TuneAura(target->GetAura(SPELL_C_SOUL_DOMINATION, me->GetGUID()), SOUL_DOMINATION_DURATION);
        }

        bool CastSoulDomination(Unit* target)
        {
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_SOUL_DOMINATION, EFFECT_0, float(SOUL_DOMINATION_MAX_LEVEL)));
            if (!target || me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            return me->CastCustomSpell(SPELL_C_SOUL_DOMINATION, values, target, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST) == SPELL_CAST_OK;
        }

        // Turtle 52044: the boss stuns itself for 6 sec (Blackfathom channel visual).
        bool CastWitheringSoul()
        {
            if (me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            TuneAura(me->AddAura(SPELL_C_WITHERING_VISUAL, me), WITHERING_SOUL_DURATION);
            TuneAura(me->AddAura(SPELL_C_WITHERING_STUN, me), WITHERING_SOUL_DURATION);
            return true;
        }

        // Turtle 52045: every enemy within 200 yd, all stats -25 and 25% smaller for 2 min.
        bool CastDebilitatedSoul()
        {
            if (me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            std::vector<Unit*> targets;
            EnemiesNear(me, *me, DEBILITATED_SOUL_RADIUS, targets);
            for (Unit* target : targets)
            {
                TuneAura(me->AddAura(SPELL_C_DEBILITATED_STATS, target), DEBILITATED_SOUL_DURATION, DEBILITATED_SOUL_STATS);
                TuneAura(me->AddAura(SPELL_C_DEBILITATED_SCALE, target), DEBILITATED_SOUL_DURATION, 0, 0, DEBILITATED_SOUL_SCALE);
            }
            return true;
        }

        // Turtle 52046: +65% attack speed, twice the size, -40% movement speed, 20 sec.
        void CastEmpoweredSoul()
        {
            TuneAura(me->AddAura(SPELL_C_EMPOWERED_SOUL, me), EMPOWERED_SOUL_DURATION, EMPOWERED_SOUL_HASTE, 0, EMPOWERED_SOUL_SCALE);
            TuneAura(me->AddAura(SPELL_C_EMPOWERED_SLOW, me), EMPOWERED_SOUL_DURATION, EMPOWERED_SOUL_SLOW);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;

            if (_soulDominationTimer < diff)
            {
                if (CastSoulDomination(RandomOrVictim(SPELL_C_SOUL_DOMINATION, true)))
                {
                    Yell(me, "You are under MY command!");
                    _soulDominationTimer = urand(14 * IN_MILLISECONDS, 18 * IN_MILLISECONDS);
                }
            }
            else
                _soulDominationTimer -= diff;

            if (!_soulSequenceStarted && me->GetHealthPct() <= 50.0f)
            {
                if (CastWitheringSoul())
                {
                    _soulSequenceStarted = true;
                    _soulSequenceTimer = SOUL_SEQUENCE_DELAY;
                    Yell(me, "Your power is mine!");
                }
            }

            if (_soulSequenceStarted && !_soulSequenceFinished)
            {
                if (_soulSequenceTimer < diff)
                {
                    if (CastDebilitatedSoul())
                    {
                        CastEmpoweredSoul();
                        _soulSequenceFinished = true;
                    }
                }
                else
                    _soulSequenceTimer -= diff;
            }

            DoMeleeAttackIfReady();
        }
    };

    // instance_dragonmaw_retreat::OnCreatureDeath for the Enchanters.
    class dragonmaw_enchanter_death : public UnitScript
    {
    public:
        dragonmaw_enchanter_death() : UnitScript("mod_turtle_dragonmaw_enchanter_death", true, { UNITHOOK_ON_UNIT_DEATH }) { }

        void OnUnitDeath(Unit* unit, Unit* /*killer*/) override
        {
            Creature* enchanter = unit ? unit->ToCreature() : nullptr;
            if (!enchanter || enchanter->GetEntry() != NPC_DRAGONMAW_ENCHANTER || enchanter->GetMapId() != MAP_DRAGONMAW_RETREAT)
                return;

            if (MarkEnchanterDead(enchanter) < MAX_DRAGONMAW_ENCHANTERS)
                return;

            // Turtle: yell only if the flames were still up, then remove them.
            Creature* searistrasz = enchanter->GetMap()->GetCreature(SearistraszGuid(enchanter->GetMap()));
            if (!searistrasz || !searistrasz->IsAlive())
                return;

            if (searistrasz->HasAura(SPELL_C_ENCHANTING_FLAMES))
                Yell(searistrasz, "The enchanted flame has left! Who dares mess with my power?!");
            RemoveEnchantingFlames(searistrasz);
        }
    };

    // Forget an instance's Enchanter count when the instance is unloaded.
    class dragonmaw_instance_cleanup : public AllMapScript
    {
    public:
        dragonmaw_instance_cleanup() : AllMapScript("mod_turtle_dragonmaw_instance_cleanup", { ALLMAPHOOK_ON_DESTROY_INSTANCE }) { }

        void OnDestroyInstance(MapInstanced* /*mapInstanced*/, Map* map) override
        {
            if (!map || map->GetId() != MAP_DRAGONMAW_RETREAT)
                return;
            std::lock_guard<std::mutex> guard(s_enchanterLock);
            s_deadEnchanters.erase(map->GetInstanceId());
            s_searistrasz.erase(map->GetInstanceId());
        }
    };

    template <class AI>
    CreatureAI* MakeDragonmaw(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_dragonmaw_retreat()
{
    RegisterAI(NPC_BOGPAW_TRUTHSAY,     &MakeDragonmaw<boss_bogpaw_truthsayAI>);
    RegisterAI(NPC_GOWLFANG,            &MakeDragonmaw<boss_gowlfangAI>);
    RegisterAI(NPC_HALGAN_REDBRAND,     &MakeDragonmaw<boss_halgan_redbrandAI>);
    RegisterAI(NPC_SEARISTRASZ,         &MakeDragonmaw<boss_searistraszAI>);
    RegisterAI(NPC_ZULUHED_THE_WHACKED, &MakeDragonmaw<boss_zuluhed_the_whackedAI>);

    new dragonmaw_enchanter_death();
    new dragonmaw_instance_cleanup();
}
