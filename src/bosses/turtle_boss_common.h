/*
 * mod-turtle-content - Turtle WoW content for AzerothCore.
 *
 * Shared helpers for the boss scripts ported from the Turtle WoW server
 * source (tortoise-wow-main/src/scripts/dungeons).
 *
 * The bosses are bound to their creature entries from C++ (see
 * turtle_boss_registry.cpp), so they do not depend on creature_template
 * ScriptName and keep working when the converter regenerates the SQL.
 * Setting TurtleContent.BossScripts = 0 falls back to the SmartAI rows.
 */

#ifndef MOD_TURTLE_CONTENT_BOSS_COMMON_H
#define MOD_TURTLE_CONTENT_BOSS_COMMON_H

#include "Creature.h"
#include "CreatureAI.h"
#include "Language.h"
#include "ObjectAccessor.h"
#include "ObjectMgr.h"
#include "Player.h"
#include "ScriptedCreature.h"
#include "SpellAuraEffects.h"
#include "SpellAuras.h"
#include "SpellInfo.h"
#include "SpellMgr.h"
#include "ThreatManager.h"
#include "turtle_voice_data.h"
#include <cmath>
#include <cstring>
#include <limits>
#include <list>
#include <vector>

namespace TurtleBoss
{
    // Factory used by the registry.
    typedef CreatureAI* (*AIFactory)(Creature*);
    void RegisterAI(uint32 entry, AIFactory factory);

    // Turtle script_texts type 0 = say, type 1 = yell. Turtle plays a recorded
    // voice line with many boss texts (script_texts.sound): the same sound ids
    // ship in client\patch-z.mpq (Sound\Interface\VA + SoundEntries.dbc), see
    // turtle_voice_data.h. A client without that patch just hears nothing.
    inline void PlayVoice(Creature* c, char const* text)
    {
        for (TurtleVoices::Line const& line : TurtleVoices::Lines)
            if (!std::strcmp(line.text, text))
            {
                c->PlayDirectSound(line.sound);
                return;
            }
    }
    inline void Say(Creature* c, char const* text)  { if (c) { PlayVoice(c, text); c->Say(text, LANG_UNIVERSAL); } }
    inline void Yell(Creature* c, char const* text) { if (c) { PlayVoice(c, text); c->Yell(text, LANG_UNIVERSAL); } }

    // ------------------------------------------------------------------
    // Spell value maths.
    //
    // AzerothCore (SpellEffectInfo::CalcValue at this commit) rolls
    //     (base + level bonus + rand(1..DieSides)) * creatureLevelFactor
    // where creatureLevelFactor = CBS(caster level) / CBS(spell level) for
    // SPELL_ATTR0_SCALES_WITH_CREATURE_LEVEL spells cast by creatures.
    // Turtle (vmangos) instead multiplied SPELL_ATTR_LEVEL_DAMAGE_CALCULATION
    // spells by 0.25 * exp(level * (70 - spellLevel) / 1000).
    // The helpers below mirror both so the ported numbers match Turtle.
    // ------------------------------------------------------------------

    // Same multiplier AzerothCore will apply to effect `effIndex` of `info` cast by `caster`.
    inline float AcCreatureLevelFactor(Unit const* caster, SpellInfo const* info, uint8 effIndex)
    {
        if (!caster || !info || effIndex >= MAX_SPELL_EFFECTS || !caster->IsCreature() || caster->IsControlledByPlayer())
            return 1.0f;

        SpellEffectInfo const& eff = info->Effects[effIndex];
        if (!info->SpellLevel || info->SpellLevel == caster->GetLevel() || eff.RealPointsPerLevel != 0.0f
            || !info->HasAttribute(SPELL_ATTR0_SCALES_WITH_CREATURE_LEVEL))
            return 1.0f;

        bool scales = false;
        switch (eff.Effect)
        {
            case SPELL_EFFECT_SCHOOL_DAMAGE:
            case SPELL_EFFECT_DUMMY:
            case SPELL_EFFECT_POWER_DRAIN:
            case SPELL_EFFECT_HEALTH_LEECH:
            case SPELL_EFFECT_HEAL:
            case SPELL_EFFECT_WEAPON_DAMAGE:
            case SPELL_EFFECT_POWER_BURN:
            case SPELL_EFFECT_SCRIPT_EFFECT:
            case SPELL_EFFECT_NORMALIZED_WEAPON_DMG:
            case SPELL_EFFECT_FORCE_CAST_WITH_VALUE:
            case SPELL_EFFECT_TRIGGER_SPELL_WITH_VALUE:
            case SPELL_EFFECT_TRIGGER_MISSILE_SPELL_WITH_VALUE:
                scales = true;
                break;
            default:
                break;
        }
        switch (eff.ApplyAuraName)
        {
            case SPELL_AURA_PERIODIC_DAMAGE:
            case SPELL_AURA_DUMMY:
            case SPELL_AURA_PERIODIC_HEAL:
            case SPELL_AURA_DAMAGE_SHIELD:
            case SPELL_AURA_PROC_TRIGGER_DAMAGE:
            case SPELL_AURA_PERIODIC_LEECH:
            case SPELL_AURA_PERIODIC_MANA_LEECH:
            case SPELL_AURA_SCHOOL_ABSORB:
            case SPELL_AURA_PERIODIC_TRIGGER_SPELL_WITH_VALUE:
                scales = true;
                break;
            default:
                break;
        }
        if (SpellInfo const* trig = sSpellMgr->GetSpellInfo(eff.TriggerSpell))
            if (trig->HasAttribute(SPELL_ATTR0_SCALES_WITH_CREATURE_LEVEL))
                scales = false;
        if (!scales)
            return 1.0f;

        CreatureTemplate const* cInfo = caster->ToCreature()->GetCreatureTemplate();
        CreatureBaseStats const* casterStats = sObjectMgr->GetCreatureBaseStats(caster->GetLevel(), caster->getClass());
        CreatureBaseStats const* spellStats = sObjectMgr->GetCreatureBaseStats(info->SpellLevel, caster->getClass());
        if (!cInfo || !casterStats || !spellStats || cInfo->expansion >= MAX_EXPANSIONS || spellStats->BaseDamage[cInfo->expansion] <= 0.0f)
            return 1.0f;
        return casterStats->BaseDamage[cInfo->expansion] / spellStats->BaseDamage[cInfo->expansion];
    }

    // Turtle's level multiplier for SPELL_ATTR_LEVEL_DAMAGE_CALCULATION spells (Object.cpp).
    inline float TurtleLevelFactor(Unit const* caster, SpellInfo const* info, uint8 effIndex)
    {
        if (!caster || !info || effIndex >= MAX_SPELL_EFFECTS || !info->SpellLevel
            || !info->HasAttribute(SPELL_ATTR0_SCALES_WITH_CREATURE_LEVEL))
            return 1.0f;
        SpellEffectInfo const& eff = info->Effects[effIndex];
        if (eff.Effect == SPELL_EFFECT_WEAPON_PERCENT_DAMAGE || eff.Effect == SPELL_EFFECT_KNOCK_BACK
            || (eff.Effect == SPELL_EFFECT_APPLY_AURA && eff.ApplyAuraName == SPELL_AURA_MOD_DECREASE_SPEED))
            return 1.0f;
        return 0.25f * std::exp(float(caster->GetLevel()) * float(70 - int32(info->SpellLevel)) / 1000.0f);
    }

    inline float AverageDieRoll(SpellEffectInfo const& eff)
    {
        int32 die = int32(eff.DieSides);
        if (die == 0)
            return 0.0f;
        if (die == 1)
            return 1.0f;
        return die > 0 ? (1.0f + float(die)) / 2.0f : (1.0f + float(die)) / 2.0f;
    }

    // Level bonus CalcValue adds before the roll (RealPointsPerLevel).
    inline float LevelBonus(Unit const* caster, SpellInfo const* info, uint8 effIndex)
    {
        SpellEffectInfo const& eff = info->Effects[effIndex];
        if (!caster || eff.RealPointsPerLevel == 0.0f)
            return 0.0f;
        int32 level = int32(caster->GetLevel());
        if (level > int32(info->MaxLevel) && info->MaxLevel > 0)
            level = int32(info->MaxLevel);
        else if (level < int32(info->BaseLevel))
            level = int32(info->BaseLevel);
        level -= int32(std::max(info->BaseLevel, info->SpellLevel));
        return float(int32(level * eff.RealPointsPerLevel));
    }

    // Value to pass as SPELLVALUE_BASE_POINTn so that AzerothCore's AVERAGE
    // result for this effect is `wantedAverage` when `caster` casts it.
    inline int32 BasePointsFor(Unit const* caster, uint32 spellId, uint8 effIndex, float wantedAverage)
    {
        SpellInfo const* info = sSpellMgr->GetSpellInfo(spellId);
        if (!info || effIndex >= MAX_SPELL_EFFECTS)
            return int32(std::lround(wantedAverage));
        SpellEffectInfo const& eff = info->Effects[effIndex];
        float factor = AcCreatureLevelFactor(caster, info, effIndex);
        float levelBonus = LevelBonus(caster, info, effIndex);
        // CalcValue truncates value * factor to int: on average that loses half a point.
        float truncation = std::fabs(factor - 1.0f) < 0.0001f ? 0.0f : 0.5f;
        float base = (wantedAverage + truncation) / factor - levelBonus - AverageDieRoll(eff);
        // CastCustomSpell feeds the value through CalcBaseValue (value - 1 when DieSides != 0).
        int32 bp = int32(std::lround(eff.DieSides != 0 ? base + 1.0f : base));

        // Fixed effects (no random part): pick the base points whose exact
        // AzerothCore result is the wanted value (or the closest to it).
        if (eff.DieSides == 0 || eff.DieSides == 1)
        {
            int32 wanted = int32(std::lround(wantedAverage));
            auto result = [&](int32 passed) -> int32
            {
                int32 points = (eff.DieSides != 0 ? passed - 1 : passed) + int32(levelBonus) + (eff.DieSides == 1 ? 1 : 0);
                return int32(float(points) * factor);
            };
            int32 best = bp;
            for (int32 candidate = bp - 3; candidate <= bp + 3; ++candidate)
                if (std::abs(result(candidate) - wanted) < std::abs(result(best) - wanted))
                    best = candidate;
            bp = best;
        }
        return bp;
    }

    // For spells that exist in both cores with the same data: override every
    // effect whose AzerothCore level scaling differs from Turtle's so the
    // average matches Turtle. Returns false when nothing needs overriding.
    inline bool TurtleScaledValues(Unit const* caster, SpellInfo const* info, CustomSpellValues& values)
    {
        bool any = false;
        for (uint8 i = 0; i < MAX_SPELL_EFFECTS; ++i)
        {
            SpellEffectInfo const& eff = info->Effects[i];
            if (!eff.Effect)
                continue;
            float ac = AcCreatureLevelFactor(caster, info, i);
            float turtle = TurtleLevelFactor(caster, info, i);
            if (std::fabs(ac - turtle) < 0.001f)
                continue;
            float unscaledAverage = float(eff.BasePoints) + LevelBonus(caster, info, i) + AverageDieRoll(eff);
            values.AddSpellMod(SpellValueMod(SPELLVALUE_BASE_POINT0 + i), BasePointsFor(caster, info->Id, i, unscaledAverage * turtle));
            any = true;
        }
        return any;
    }

    // Invisible caster at `pos` with the boss faction and level. World Invisible
    // Trigger (12999) is immune to players and NPCs in its template, which would
    // stop its area spells from picking anyone: those flags are dropped here.
    inline Creature* SpellTrigger(Creature* owner, Position const& pos, uint32 durationMs)
    {
        if (!owner)
            return nullptr;
        Creature* trigger = owner->SummonTrigger(pos.GetPositionX(), pos.GetPositionY(), pos.GetPositionZ(), pos.GetOrientation(), durationMs, true);
        if (trigger)
        {
            trigger->RemoveUnitFlag(UNIT_FLAG_IMMUNE_TO_PC);
            trigger->RemoveUnitFlag(UNIT_FLAG_IMMUNE_TO_NPC);
            trigger->SetReactState(REACT_PASSIVE);
        }
        return trigger;
    }

    // Base for every ported boss. Mirrors the helpers the Turtle scripts use
    // (DoCastSpellIfCan / SelectAttackingTarget) so the ported logic stays
    // line-for-line comparable with the original.
    struct TurtleBossAI : public ScriptedAI
    {
        explicit TurtleBossAI(Creature* creature) : ScriptedAI(creature), summons(creature) { }

        SummonList summons;

        void JustSummoned(Creature* summon) override { summons.Summon(summon); }
        void SummonedCreatureDespawn(Creature* summon) override { summons.Despawn(summon); }


        // vmangos DoCastSpellIfCan: a non-triggered cast fails while another
        // cast is in progress, and the caller keeps its timer so it retries.
        // Spells that both cores scale with creature level get Turtle's scaling.
        bool TryCast(Unit* target, uint32 spellId, bool triggered = false)
        {
            if (!target)
                return false;
            if (!triggered && me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            if (SpellInfo const* info = sSpellMgr->GetSpellInfo(spellId))
            {
                CustomSpellValues values;
                if (TurtleScaledValues(me, info, values))
                    return me->CastCustomSpell(spellId, values, target, triggered ? TRIGGERED_FULL_MASK : TRIGGERED_NONE) == SPELL_CAST_OK;
            }
            SpellCastResult res = me->CastSpell(target, spellId, triggered);
            return res == SPELL_CAST_OK;
        }

        // Warrior spells (rage cost) on a creature without rage: Turtle's
        // creatures cast them anyway, so the power cost is skipped.
        bool TryCastNoCost(Unit* target, uint32 spellId)
        {
            if (!target || me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            return me->CastSpell(target, spellId, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST) == SPELL_CAST_OK;
        }

        bool TryCastCustom(Unit* target, uint32 spellId, CustomSpellValues const& values, bool triggered = false)
        {
            if (!target)
                return false;
            if (!triggered && me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            return me->CastCustomSpell(spellId, values, target, triggered ? TRIGGERED_FULL_MASK : TRIGGERED_NONE) == SPELL_CAST_OK;
        }

        // vmangos SelectAttackingTarget(ATTACKING_TARGET_RANDOM, 0, spellId, flags)
        // spellId != 0 -> target must be inside the spell's max range.
        Unit* RandomTarget(uint32 spellId = 0, bool needLos = true, bool playerOnly = false, bool meleeOnly = false)
        {
            float maxRange = 0.0f;
            if (spellId)
                if (SpellInfo const* info = sSpellMgr->GetSpellInfo(spellId))
                    maxRange = info->GetMaxRange(false);

            Creature* self = me;
            return SelectTarget(SelectTargetMethod::Random, 0, [self, maxRange, needLos, playerOnly, meleeOnly](Unit* u) -> bool
            {
                if (!u || !u->IsAlive())
                    return false;
                if (u->IsTotem())
                    return false;
                if (playerOnly && !u->IsPlayer())
                    return false;
                if (needLos && !self->IsWithinLOSInMap(u))
                    return false;
                if (meleeOnly && !self->IsWithinMeleeRange(u))
                    return false;
                if (maxRange > 0.0f && !self->IsWithinCombatRange(u, maxRange))
                    return false;
                return true;
            });
        }

        // Copy our threat list onto another creature (Turtle ThreatCopier).
        void CopyThreatTo(Creature* target)
        {
            if (!target)
                return;

            for (ThreatReference const* ref : me->GetThreatMgr().GetSortedThreatList())
            {
                Unit* victim = ref->GetVictim();
                if (!victim || !victim->IsAlive())
                    continue;
                float threat = ref->GetThreat();
                if (threat <= 0.0f)
                    threat = 1.0f;
                target->GetThreatMgr().AddThreat(victim, threat, nullptr, true, true);
            }

            if (Unit* top = SelectTarget(SelectTargetMethod::MaxThreat, 0))
                if (target->IsAIEnabled && target->AI())
                    target->AI()->AttackStart(top);
        }

        // Spell damage that must come from a spot (e.g. around a player) rather
        // than from the boss: an invisible trigger with the boss faction casts
        // it there, credited to the boss.
        Creature* TriggerAt(Position const& pos, uint32 durationMs)
        {
            return SpellTrigger(me, pos, durationMs);
        }
    };

    // Living enemies of `source` within `radius` of `center` (Turtle area
    // spells hit every hostile unit: players and their pets). Uses the
    // source's threat list; if that is empty (e.g. the source died), falls
    // back to the players of the map.
    inline void EnemiesNear(Creature* source, Position const& center, float radius, std::vector<Unit*>& out, bool needLos = true)
    {
        out.clear();
        if (!source)
            return;

        auto accept = [&](Unit* u) -> bool
        {
            if (!u || !u->IsAlive() || !u->IsInWorld() || u->GetMapId() != source->GetMapId())
                return false;
            if (Player* p = u->ToPlayer())
                if (p->IsGameMaster())
                    return false;
            if (u->GetExactDist(&center) > radius)
                return false;
            if (needLos && !u->IsWithinLOS(center.GetPositionX(), center.GetPositionY(), center.GetPositionZ()))
                return false;
            return true;
        };

        for (ThreatReference const* ref : source->GetThreatMgr().GetUnsortedThreatList())
            if (Unit* u = ref->GetVictim())
                if (accept(u))
                    out.push_back(u);

        if (!out.empty() || !source->GetMap())
            return;

        for (auto const& itr : source->GetMap()->GetPlayers())
            if (Player* p = itr.GetSource())
                if (accept(p))
                    out.push_back(p);
    }

    // Plain melee add that simply fights (summons of the ported bosses).
    struct TurtleAddAI : public ScriptedAI
    {
        explicit TurtleAddAI(Creature* creature) : ScriptedAI(creature) { }

        void UpdateAI(uint32 /*diff*/) override
        {
            if (!UpdateVictim())
                return;
            DoMeleeAttackIfReady();
        }
    };

    // Set an aura's duration (<= 0 = leave as is) and the amount of its
    // effects (KEEP_AMOUNT = leave as is; negative amounts are allowed).
    constexpr int32 KEEP_AMOUNT = std::numeric_limits<int32>::min();

    inline void TuneAura(Aura* aura, int32 durationMs, int32 eff0 = KEEP_AMOUNT, int32 eff1 = KEEP_AMOUNT, int32 eff2 = KEEP_AMOUNT)
    {
        if (!aura)
            return;
        if (durationMs > 0)
        {
            aura->SetMaxDuration(durationMs);
            aura->SetDuration(durationMs);
        }
        int32 amounts[3] = { eff0, eff1, eff2 };
        for (uint8 i = 0; i < 3; ++i)
            if (amounts[i] != KEEP_AMOUNT)
                if (AuraEffect* eff = aura->GetEffect(i))
                    eff->ChangeAmount(amounts[i]);
    }
}

#endif
