/*
 * mod-turtle-content - Frostmane Hollow (map 822, level 13-16 dungeon).
 *
 * Ported from tortoise-wow-main:
 *  - src/scripts/dungeons/frostmane_hollow/boss_hailar_the_frigid.cpp
 *    (npc_frostmane_ritualist: the 5 ritualists around Hailar the Frigid
 *    stay passive and channel Frostmane Ritual on him, 150 health per second
 *    each, until they die). Hailar's own lines (aggro, 50%, death) are
 *    already in the module's SmartAI rows.
 *  - Turtle creature_spells / EventAI for the trash whose Turtle-only spells
 *    the converter replaced with 3.3.5 stand-ins that do something else.
 *
 * Turtle spells and their 3.3.5 carriers (same visual / same mechanics,
 * values set to Turtle's):
 *  - 41592 Frostmane Ritual (channel, 150 heal/s, no end) ->
 *      30662 Demonic Summon Channel for the beam (same visual, 277) +
 *      10260 Reconstruct for the heal (150 per second), refreshed while the
 *      ritualist lives and removed when it dies.
 *  - 33398 Icerot Decay (Frostmane Cretin: -11 Spirit, 15 min) ->
 *      3237 Curse of Thule (same 2 s cast, same Spirit aura), -11 for 15 min.
 *  - 33397 Frozen Mind (Ice Elemental: -16% attack speed, -16% casting
 *      speed for 60 s) -> 7127 Wavering Will, set to -16% / -16%, no slow.
 *  - 33399 Summon Ice Claw (Frostmane Tamer: a Tamed Ice Claw Bear that
 *      protects him) -> the module's summon of Ice Claw Bear 1196 (same
 *      level 7-8 bear); here it follows the tamer and joins his fights,
 *      and only one bear per tamer.
 */

#include "turtle_boss_common.h"
#include "ScriptMgr.h"
#include "SmartAI.h"

using namespace TurtleBoss;

namespace
{
    enum FrostmaneHollow
    {
        NPC_HAILAR_THE_FRIGID   = 63130,
        NPC_FROSTMANE_RITUALIST = 36519,
        NPC_FROSTMANE_CRETIN    = 67,
        NPC_ICE_ELEMENTAL       = 63135,
        NPC_FROSTMANE_TAMER     = 82,
        NPC_ICE_CLAW_BEAR       = 1196,

        SPELL_RITUAL_BEAM       = 30662,   // carrier visual for Turtle 41592 Frostmane Ritual
        SPELL_RITUAL_HEAL       = 10260,   // 150 health per second, 20 s, refreshed
        SPELL_ICEROT_DECAY      = 3237,    // carrier for Turtle 33398
        SPELL_FROZEN_MIND       = 7127,    // carrier for Turtle 33397

        ICEROT_SPIRIT           = -11,
        ICEROT_DURATION_MS      = 15 * MINUTE * IN_MILLISECONDS,
        FROZEN_MIND_PCT         = -16,
        FROZEN_MIND_DURATION_MS = 60 * IN_MILLISECONDS,
    };

    // ---- Frostmane Ritualist ------------------------------------------------
    struct npc_frostmane_ritualistAI : public ScriptedAI
    {
        explicit npc_frostmane_ritualistAI(Creature* creature) : ScriptedAI(creature) { }

        uint32 _timer = 500;

        void Reset() override
        {
            me->SetReactState(REACT_PASSIVE);
            _timer = 500;
        }

        // Turtle: the ritualists never fight, they only keep channeling.
        void MoveInLineOfSight(Unit* /*who*/) override { }
        void AttackStart(Unit* /*who*/) override { }

        Creature* Hailar() const { return me->FindNearestCreature(NPC_HAILAR_THE_FRIGID, 100.0f, true); }

        void UpdateAI(uint32 diff) override
        {
            if (_timer > diff)
            {
                _timer -= diff;
                return;
            }
            _timer = 1 * IN_MILLISECONDS;

            Creature* hailar = Hailar();
            if (!hailar)
            {
                me->InterruptNonMeleeSpells(false);
                return;
            }

            if (!me->GetCurrentSpell(CURRENT_CHANNELED_SPELL))
                me->CastSpell(hailar, SPELL_RITUAL_BEAM, true);

            // Keep the heal running (it lasts 20 s, refreshed every 5 s).
            Aura* heal = hailar->GetAura(SPELL_RITUAL_HEAL, me->GetGUID());
            if (!heal || heal->GetDuration() < 15 * IN_MILLISECONDS)
                me->CastSpell(hailar, SPELL_RITUAL_HEAL, true);
        }

        void StopRitual()
        {
            me->InterruptNonMeleeSpells(false);
            if (Creature* hailar = Hailar())
                hailar->RemoveAura(SPELL_RITUAL_HEAL, me->GetGUID());
        }

        void JustDied(Unit* /*killer*/) override { StopRitual(); }
    };

    // ---- Trash whose Turtle spell rides on a 3.3.5 carrier --------------------
    // The SmartAI rows keep Turtle's timers and targets; the carrier aura is
    // set to Turtle's values when it lands.
    struct npc_frostmane_cretinAI : public SmartAI
    {
        explicit npc_frostmane_cretinAI(Creature* creature) : SmartAI(creature) { }

        void SpellHitTarget(Unit* target, SpellInfo const* spellInfo) override
        {
            SmartAI::SpellHitTarget(target, spellInfo);
            if (target && spellInfo && spellInfo->Id == SPELL_ICEROT_DECAY)
                TuneAura(target->GetAura(SPELL_ICEROT_DECAY, me->GetGUID()), ICEROT_DURATION_MS, ICEROT_SPIRIT);
        }
    };

    struct npc_frostmane_ice_elementalAI : public SmartAI
    {
        explicit npc_frostmane_ice_elementalAI(Creature* creature) : SmartAI(creature) { }

        void SpellHitTarget(Unit* target, SpellInfo const* spellInfo) override
        {
            SmartAI::SpellHitTarget(target, spellInfo);
            if (target && spellInfo && spellInfo->Id == SPELL_FROZEN_MIND)
                TuneAura(target->GetAura(SPELL_FROZEN_MIND, me->GetGUID()), FROZEN_MIND_DURATION_MS,
                    FROZEN_MIND_PCT, 0, FROZEN_MIND_PCT);
        }
    };

    // ---- Frostmane Tamer ------------------------------------------------------
    struct npc_frostmane_tamerAI : public SmartAI
    {
        explicit npc_frostmane_tamerAI(Creature* creature) : SmartAI(creature) { }

        ObjectGuid _bear;

        Creature* Bear() const
        {
            Creature* bear = _bear ? ObjectAccessor::GetCreature(*me, _bear) : nullptr;
            return bear && bear->IsAlive() ? bear : nullptr;
        }

        void JustSummoned(Creature* summon) override
        {
            SmartAI::JustSummoned(summon);
            if (!summon || summon->GetEntry() != NPC_ICE_CLAW_BEAR)
                return;

            // One bear per tamer (the module summons it on spawn and on respawn).
            if (Bear() && Bear() != summon)
            {
                summon->DespawnOrUnsummon();
                return;
            }
            _bear = summon->GetGUID();
            summon->SetFaction(me->GetFaction());
            if (!me->IsInCombat())
                summon->GetMotionMaster()->MoveFollow(me, PET_FOLLOW_DIST, PET_FOLLOW_ANGLE);
        }

        void JustEngagedWith(Unit* who) override
        {
            SmartAI::JustEngagedWith(who);
            if (Creature* bear = Bear())
                if (!bear->IsInCombat() && bear->IsAIEnabled && bear->AI())
                    bear->AI()->AttackStart(who);
        }

        void JustReachedHome() override
        {
            SmartAI::JustReachedHome();
            if (Creature* bear = Bear())
                if (!bear->IsInCombat())
                    bear->GetMotionMaster()->MoveFollow(me, PET_FOLLOW_DIST, PET_FOLLOW_ANGLE);
        }
    };

    template <class AI>
    CreatureAI* MakeFrostmane(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_frostmane_hollow()
{
    RegisterAI(NPC_FROSTMANE_RITUALIST, &MakeFrostmane<npc_frostmane_ritualistAI>);
    RegisterAI(NPC_FROSTMANE_CRETIN,    &MakeFrostmane<npc_frostmane_cretinAI>);
    RegisterAI(NPC_ICE_ELEMENTAL,       &MakeFrostmane<npc_frostmane_ice_elementalAI>);
    RegisterAI(NPC_FROSTMANE_TAMER,     &MakeFrostmane<npc_frostmane_tamerAI>);
}
