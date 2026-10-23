/*
 * mod-turtle-content - Turtle spell values for the converted Turtle creatures.
 *
 * Many spells keep their id from 1.12 to 3.3.5 but not their numbers: 3.3.5's
 * Sinister Strike 15667 adds 832-967 damage where Turtle's adds about 40,
 * Starfire 25298 hits for 692-817 instead of 495-584, Shadow Shock 16583 does
 * less than half of Turtle's damage, durations differ, and AzerothCore scales
 * creature spells with level differently from Turtle (vmangos).
 *
 * When a converted Turtle creature casts one of its own Turtle spells (the
 * pairs listed in turtle_spell_values_data.h, generated from the module's
 * SmartAI rows, Turtle's Spell.dbc and 3.3.5's Spell.dbc), the cast gets
 * Turtle's average values (base points, per-level bonus, Turtle's level
 * scaling) and Turtle's aura duration. 3.3.5 stand-ins for Turtle-only spells
 * are not touched, nor are casts whose values a script already set.
 *
 * TurtleContent.TurtleSpellValues = 0 turns it off.
 */

#include "turtle_boss_common.h"
#include "turtle_spell_values_data.h"
#include "Config.h"
#include "ScriptMgr.h"
#include "Spell.h"
#include <unordered_map>
#include <unordered_set>

using namespace TurtleBoss;

namespace
{
    bool s_enabled = true;
    std::unordered_map<uint32, TurtleSpellValues::Entry const*> s_spells;
    std::unordered_set<uint64> s_casters;

    void BuildTables()
    {
        if (!s_spells.empty())
            return;
        for (TurtleSpellValues::Entry const& e : TurtleSpellValues::Spells)
            s_spells[e.spellId] = &e;
        for (TurtleSpellValues::Caster const& c : TurtleSpellValues::Casters)
            s_casters.insert((uint64(c.creature) << 32) | c.spellId);
    }

    TurtleSpellValues::Entry const* Lookup(WorldObject const* caster, uint32 spellId)
    {
        if (!s_enabled || !caster)
            return nullptr;
        Creature const* creature = caster->ToCreature();
        if (!creature || creature->IsPet() || creature->IsControlledByPlayer())
            return nullptr;
        if (!s_casters.count((uint64(creature->GetEntry()) << 32) | spellId))
            return nullptr;
        auto itr = s_spells.find(spellId);
        return itr == s_spells.end() ? nullptr : itr->second;
    }

    // Turtle's average for one effect when `caster` casts it (vmangos CalculateSpellEffectValue + level scaling).
    float TurtleAverage(Unit const* caster, SpellInfo const* info, TurtleSpellValues::Entry const& e, TurtleSpellValues::Effect const& ef)
    {
        float bonus = 0.0f;
        if (ef.pointsPerLevel != 0.0f)
        {
            int32 level = int32(caster->GetLevel());
            if (e.maxLevel && level > int32(e.maxLevel))
                level = int32(e.maxLevel);
            else if (level < int32(e.baseLevel))
                level = int32(e.baseLevel);
            level -= int32(std::max(e.baseLevel, e.spellLevel));
            bonus = float(int32(level * ef.pointsPerLevel));
        }

        float roll = ef.dieSides == 0 ? 0.0f : (ef.dieSides == 1 ? 1.0f : (1.0f + float(ef.dieSides)) / 2.0f);
        float value = float(ef.basePoints) + bonus + roll;

        if (e.scales && e.spellLevel)
        {
            SpellEffectInfo const& eff = info->Effects[ef.index];
            bool excluded = eff.Effect == SPELL_EFFECT_WEAPON_PERCENT_DAMAGE || eff.Effect == SPELL_EFFECT_KNOCK_BACK
                || (eff.Effect == SPELL_EFFECT_APPLY_AURA && eff.ApplyAuraName == SPELL_AURA_MOD_DECREASE_SPEED);
            if (!excluded)
                value *= 0.25f * std::exp(float(caster->GetLevel()) * float(70 - int32(e.spellLevel)) / 1000.0f);
        }
        return value;
    }

    class turtle_spell_values_spells : public AllSpellScript
    {
    public:
        turtle_spell_values_spells() : AllSpellScript("mod_turtle_content_spell_values", { ALLSPELLHOOK_CAN_PREPARE, ALLSPELLHOOK_ON_CALC_MAX_DURATION }) { }

        bool CanPrepare(Spell* spell, SpellCastTargets const* /*targets*/, AuraEffect const* /*triggeredByAura*/) override
        {
            if (!spell)
                return true;
            SpellInfo const* info = spell->GetSpellInfo();
            Unit* caster = spell->GetCaster() ? spell->GetCaster()->ToUnit() : nullptr;
            TurtleSpellValues::Entry const* e = info ? Lookup(caster, info->Id) : nullptr;
            if (!e)
                return true;

            SpellValue const* current = spell->GetSpellValue();
            for (uint8 i = 0; i < e->effectCount && i < MAX_SPELL_EFFECTS; ++i)
            {
                TurtleSpellValues::Effect const& ef = e->effects[i];
                if (ef.index < 0 || ef.index >= MAX_SPELL_EFFECTS)
                    continue;
                // A script already chose this value (CastCustomSpell): keep it.
                if (current->EffectBasePoints[ef.index] != info->Effects[ef.index].BasePoints)
                    continue;
                spell->SetSpellValue(SpellValueMod(SPELLVALUE_BASE_POINT0 + ef.index),
                    BasePointsFor(caster, info->Id, ef.index, TurtleAverage(caster, info, *e, ef)));
            }
            return true;
        }

        void OnCalcMaxDuration(Aura const* aura, int32& maxDuration) override
        {
            if (!aura)
                return;
            TurtleSpellValues::Entry const* e = Lookup(aura->GetCaster(), aura->GetId());
            if (e && e->durationMs)
                maxDuration = e->durationMs;
        }
    };

    class turtle_spell_values_config : public WorldScript
    {
    public:
        turtle_spell_values_config() : WorldScript("mod_turtle_content_spell_values_config", { WORLDHOOK_ON_AFTER_CONFIG_LOAD }) { }

        void OnAfterConfigLoad(bool /*reload*/) override
        {
            BuildTables();
            s_enabled = sConfigMgr->GetOption<bool>("TurtleContent.TurtleSpellValues", true);
            LOG_INFO("module", ">> mod-turtle-content: Turtle spell values {} ({} spells, {} creature casts)",
                s_enabled ? "enabled" : "disabled", s_spells.size(), s_casters.size());
        }
    };
}

void AddSC_turtle_spell_values()
{
    new turtle_spell_values_spells();
    new turtle_spell_values_config();
}
