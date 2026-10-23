/*
 * mod-turtle-content - Zul'Farrak additions from Turtle WoW.
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/zulfarrak/farraki_arena.cpp:
 * the Farraki Arena. Champion Razjal the Quick's "I challenge you to combat."
 * starts it; 5 s later his intro line, 8 s later Kath'zen the Brutal attacks the
 * challenger's group, Juthza the Cunning when Kath'zen dies or 30 s later, and
 * Razjal himself when both are dead or 30 s after Juthza. At 50% Razjal goes to
 * the middle of the arena, channels, is immune to damage and crowd control,
 * and 10 Sandfury Scorpids come from the four gates (never the same gate twice
 * in a row, one every 2 s after 5 s); then he fights on. At 10% he casts
 * Hellfire (no mana cost). If any of the three resets (a wipe), the whole arena
 * resets: scorpids gone, the dead respawned, the challenge offered again.
 * These AIs replace the module's SmartAI version of the arena.
 *
 * Zel'jeb the Ancient: Turtle 52695 Curse of Years at 50% (6 s cast; every
 * enemy within 20 yd takes 250 Nature damage and loses 250 mana every 5 s and
 * has -40 to all stats for 1 min) -> 6 s carrier cast 46627 (no effect), then
 * 11442 Withered Touch set to 500 damage / 500 mana every 10 s and 13524 Curse
 * of Stalvan set to -40 all stats, both 1 min. The converter's stand-in
 * (18267 Curse of Weakness) is removed by mod_turtle_908_zulfarrak.sql.
 */

#include "turtle_boss_common.h"
#include "Group.h"
#include "ScriptMgr.h"
#include "ScriptedGossip.h"
#include "SmartAI.h"

using namespace TurtleBoss;

namespace
{
    enum ZulFarrakArena
    {
        NPC_ZELJEB              = 62495,
        NPC_KATHZEN             = 62496,
        NPC_JUTHZA              = 62497,
        NPC_RAZJAL              = 62498,
        NPC_SANDFURY_SCORPID    = 62499,

        MENU_RAZJAL             = 62498,

        SPELL_ENRAGE            = 15716,
        SPELL_NATURE_CHANNELING = 13236,
        SPELL_HELLFIRE          = 11684,

        FACTION_HOSTILE         = 14,

        // creature_text groups (module rows, Turtle broadcast texts)
        TEXT_FIGHTER_AGGRO      = 0,      // Kath'zen 6249601, Juthza 6249701
        TEXT_RAZJAL_INTRO       = 0,      // 6249803
        TEXT_RAZJAL_AGGRO       = 1,      // 6249804
        TEXT_RAZJAL_SANDS       = 2,      // 6249805
        TEXT_RAZJAL_FINAL       = 3,      // 6249806

        ACTION_KATHZEN_DIED     = 1,
        ACTION_JUTHZA_DIED      = 2,
        ACTION_ARENA_RESET      = 3,
    };

    enum ArenaPhase { PHASE_IDLE, PHASE_INTRO, PHASE_KATHZEN, PHASE_JUTHZA, PHASE_RAZJAL, PHASE_SCORPIDS };

    constexpr float ARENA_RANGE = 150.0f;
    Position const RazjalChannelPosition = { 1512.2099609375f, 1016.0499877929688f, 11.678000450134277f, 2.899270534515381f };
    Position const ScorpidSpawnPositions[4] =
    {
        { 1498.650024f, 1030.937012f, 11.6f,    0.0f },
        { 1534.144043f, 1030.718018f, 11.826f,  0.0f },
        { 1536.583008f, 1005.965027f, 11.6277f, 0.0f },
        { 1499.567017f,  998.440002f, 11.756f,  0.0f },
    };

    uint32 const RazjalImmunityMechanics[] =
    {
        MECHANIC_CHARM, MECHANIC_DISORIENTED, MECHANIC_DISARM, MECHANIC_FEAR, MECHANIC_ROOT, MECHANIC_SILENCE,
        MECHANIC_SLEEP, MECHANIC_SNARE, MECHANIC_STUN, MECHANIC_FREEZE, MECHANIC_KNOCKOUT, MECHANIC_POLYMORPH,
        MECHANIC_BANISH, MECHANIC_SHACKLE, MECHANIC_TURN, MECHANIC_HORROR, MECHANIC_DAZE, MECHANIC_SAPPED,
    };

    void ApplyRazjalIntermissionImmunity(Creature* creature, bool apply)
    {
        creature->ApplySpellImmune(0, IMMUNITY_DAMAGE, SPELL_SCHOOL_MASK_ALL, apply);
        creature->ApplySpellImmune(0, IMMUNITY_DISPEL, DISPEL_MAGIC, apply);
        creature->ApplySpellImmune(0, IMMUNITY_DISPEL, DISPEL_CURSE, apply);
        creature->ApplySpellImmune(0, IMMUNITY_DISPEL, DISPEL_DISEASE, apply);
        creature->ApplySpellImmune(0, IMMUNITY_DISPEL, DISPEL_POISON, apply);
        for (uint32 mechanic : RazjalImmunityMechanics)
            creature->ApplySpellImmune(0, IMMUNITY_MECHANIC, mechanic, apply);
    }

    // vmangos creature_spells: one spell of the list, first after rand(initial), then rand(repeat).
    struct ListSpell
    {
        uint32 spellId, initialMin, initialMax, repeatMin, repeatMax;
        uint32 timer = 0;
    };

    struct ArenaFighterBase : public ScriptedAI
    {
        explicit ArenaFighterBase(Creature* c) : ScriptedAI(c) { }

        std::vector<ListSpell> _list;

        void StartList()
        {
            for (ListSpell& s : _list)
                s.timer = urand(s.initialMin, s.initialMax);
        }

        void UpdateList(uint32 diff)
        {
            for (ListSpell& s : _list)
            {
                if (s.timer > diff)
                {
                    s.timer -= diff;
                    continue;
                }
                if (me->HasUnitState(UNIT_STATE_CASTING))
                    continue;
                if (me->CastSpell(me->GetVictim(), s.spellId, false) == SPELL_CAST_OK)
                    s.timer = urand(s.repeatMin, s.repeatMax);
            }
        }

        void JustEngagedWith(Unit* /*who*/) override { StartList(); }

        Creature* Razjal() const { return me->FindNearestCreature(NPC_RAZJAL, ARENA_RANGE, true); }

        void Notify(uint32 action)
        {
            if (Creature* razjal = Razjal())
                if (razjal->IsAIEnabled && razjal->AI())
                    razjal->AI()->DoAction(int32(action));
        }
    };

    // ------------------------------------------------------------------
    // Kath'zen the Brutal / Juthza the Cunning
    // ------------------------------------------------------------------
    struct npc_arena_fighterAI : public ArenaFighterBase
    {
        npc_arena_fighterAI(Creature* c, bool kathzen) : ArenaFighterBase(c), _kathzen(kathzen)
        {
            if (kathzen)
                _list = { { 21553, 0, 3000, 20000, 25000 }, { 16095, 0, 3000, 15000, 20000 } };
            else
                _list = { { 6533, 2000, 4000, 10000, 15000 }, { 12540, 5000, 8000, 15000, 20000 }, { 15656, 5000, 8000, 10000, 15000 } };
        }

        bool _kathzen;
        bool _enraged = false;

        void Reset() override
        {
            _enraged = false;
            me->RestoreFaction();
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            Notify(ACTION_ARENA_RESET);
            ScriptedAI::EnterEvadeMode(why);
        }

        void JustDied(Unit* /*killer*/) override { Notify(_kathzen ? ACTION_KATHZEN_DIED : ACTION_JUTHZA_DIED); }

        void UpdateAI(uint32 diff) override
        {
            if (!UpdateVictim())
                return;
            UpdateList(diff);
            if (_kathzen && !_enraged && me->GetHealthPct() <= 50.0f && !me->HasUnitState(UNIT_STATE_CASTING))
                if (me->CastSpell(me, SPELL_ENRAGE, false) == SPELL_CAST_OK)
                    _enraged = true;
            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Champion Razjal the Quick
    // ------------------------------------------------------------------
    struct npc_champion_razjalAI : public ArenaFighterBase
    {
        explicit npc_champion_razjalAI(Creature* c) : ArenaFighterBase(c)
        {
            _originalNpcFlags = me->GetNpcFlags();
            _list = { { 22886, 0, 0, 20000, 25000 } };
        }

        NPCFlags _originalNpcFlags;
        ObjectGuid _starter;
        ArenaPhase _phase = PHASE_IDLE;
        uint32 _introTimer = 0;
        uint32 _nextPhaseTimer = 0;
        uint32 _scorpidStartTimer = 0;
        uint32 _scorpidSpawnTimer = 0;
        uint8 _scorpidsSpawned = 0;
        uint8 _lastScorpidSpawn = 255;
        bool _sandsStarted = false;
        bool _finalStarted = false;
        bool _resetting = false;
        GuidVector _scorpids;

        void Reset() override
        {
            DespawnScorpids();
            _starter.Clear();
            _phase = PHASE_IDLE;
            _introTimer = 0;
            _nextPhaseTimer = 0;
            _scorpidStartTimer = 0;
            _scorpidSpawnTimer = 0;
            _scorpidsSpawned = 0;
            _lastScorpidSpawn = 255;
            _sandsStarted = false;
            _finalStarted = false;
            _resetting = false;
            ApplyRazjalIntermissionImmunity(me, false);
            me->RemoveAurasDueToSpell(SPELL_NATURE_CHANNELING);
            me->SetReactState(REACT_AGGRESSIVE);
            me->RestoreFaction();
            me->ReplaceAllNpcFlags(_originalNpcFlags);
        }

        // The challenge (Turtle gossip script 6249801 -> npc_champion_razjal_the_quick).
        void sGossipSelect(Player* player, uint32 menuId, uint32 /*gossipListId*/) override
        {
            CloseGossipMenuFor(player);
            if (menuId != MENU_RAZJAL || _phase != PHASE_IDLE)
                return;
            _starter = player->GetGUID();
            me->RemoveNpcFlag(UNIT_NPC_FLAG_GOSSIP);
            _phase = PHASE_INTRO;
            _introTimer = 5 * IN_MILLISECONDS;
        }

        Player* Starter() const { return _starter ? ObjectAccessor::GetPlayer(*me, _starter) : nullptr; }
        Creature* Arena(uint32 entry, bool alive = true) const { return me->FindNearestCreature(entry, ARENA_RANGE, alive); }

        void AddThreatToParty(Creature* creature, Player* player)
        {
            if (!creature || !player)
                return;
            if (Group* group = player->GetGroup())
            {
                for (GroupReference* ref = group->GetFirstMember(); ref; ref = ref->next())
                    if (Player* member = ref->GetSource())
                        if (member->IsAlive() && member->GetMap() == creature->GetMap())
                            creature->GetThreatMgr().AddThreat(member, 1.0f);
            }
            else
                creature->GetThreatMgr().AddThreat(player, 1.0f);
        }

        void Engage(Creature* creature, Player* player, uint32 text)
        {
            if (!creature || !creature->IsAlive() || !player)
                return;
            creature->SetFaction(FACTION_HOSTILE);
            AddThreatToParty(creature, player);
            creature->AI()->AttackStart(player);
            creature->AI()->Talk(text);
        }

        bool FightersDead() const { return !Arena(NPC_KATHZEN) && !Arena(NPC_JUTHZA); }

        void StartKathzen()
        {
            _phase = PHASE_KATHZEN;
            _nextPhaseTimer = 30 * IN_MILLISECONDS;
            Engage(Arena(NPC_KATHZEN), Starter(), TEXT_FIGHTER_AGGRO);
        }

        void StartJuthza()
        {
            if (_phase >= PHASE_JUTHZA)
                return;
            _phase = PHASE_JUTHZA;
            _nextPhaseTimer = 30 * IN_MILLISECONDS;
            Engage(Arena(NPC_JUTHZA), Starter(), TEXT_FIGHTER_AGGRO);
        }

        void StartRazjal()
        {
            if (_phase >= PHASE_RAZJAL)
                return;
            _phase = PHASE_RAZJAL;
            Engage(me, Starter(), TEXT_RAZJAL_AGGRO);
        }

        void StartSands()
        {
            _sandsStarted = true;
            _phase = PHASE_SCORPIDS;
            _scorpidStartTimer = 5 * IN_MILLISECONDS;
            _scorpidSpawnTimer = 0;
            _scorpidsSpawned = 0;
            _lastScorpidSpawn = 255;

            ApplyRazjalIntermissionImmunity(me, true);
            me->SetReactState(REACT_PASSIVE);
            me->NearTeleportTo(RazjalChannelPosition.GetPositionX(), RazjalChannelPosition.GetPositionY(),
                RazjalChannelPosition.GetPositionZ(), RazjalChannelPosition.GetOrientation());
            me->SetFacingTo(RazjalChannelPosition.GetOrientation());
            me->AttackStop();
            me->StopMoving();
            me->GetMotionMaster()->Clear(false);
            me->GetMotionMaster()->MoveIdle();
            me->CastSpell(me, SPELL_NATURE_CHANNELING, true);
            Talk(TEXT_RAZJAL_SANDS);
        }

        void EndSands()
        {
            me->InterruptNonMeleeSpells(false, SPELL_NATURE_CHANNELING);
            me->RemoveAurasDueToSpell(SPELL_NATURE_CHANNELING);
            ApplyRazjalIntermissionImmunity(me, false);
            me->SetReactState(REACT_AGGRESSIVE);
            _phase = PHASE_RAZJAL;
            if (Player* player = Starter())
            {
                AddThreatToParty(me, player);
                AttackStart(player);
            }
        }

        void SpawnScorpid()
        {
            uint8 index = _lastScorpidSpawn < 4 ? urand(0, 2) : urand(0, 3);
            if (_lastScorpidSpawn < 4 && index >= _lastScorpidSpawn)
                ++index;

            if (Creature* scorpid = me->SummonCreature(NPC_SANDFURY_SCORPID, ScorpidSpawnPositions[index], TEMPSUMMON_TIMED_OR_DEAD_DESPAWN, 2 * MINUTE * IN_MILLISECONDS))
            {
                _scorpids.push_back(scorpid->GetGUID());
                scorpid->SetFaction(FACTION_HOSTILE);
                if (Player* player = Starter())
                {
                    AddThreatToParty(scorpid, player);
                    scorpid->AI()->AttackStart(player);
                }
            }

            _lastScorpidSpawn = index;
            if (++_scorpidsSpawned == 10)
                EndSands();
        }

        void DespawnScorpids()
        {
            for (ObjectGuid const& guid : _scorpids)
                if (Creature* scorpid = ObjectAccessor::GetCreature(*me, guid))
                    scorpid->DespawnOrUnsummon();
            _scorpids.clear();
        }

        void ResetFighter(uint32 entry)
        {
            if (Creature* fighter = me->FindNearestCreature(entry, ARENA_RANGE, false))
            {
                if (!fighter->IsAlive())
                    fighter->Respawn(true);
                fighter->RestoreFaction();
                if (fighter->IsInCombat())
                    fighter->AI()->EnterEvadeMode();
            }
        }

        void ResetArena()
        {
            if (_resetting)
                return;
            _resetting = true;
            DespawnScorpids();
            ApplyRazjalIntermissionImmunity(me, false);
            me->RemoveAurasDueToSpell(SPELL_NATURE_CHANNELING);
            ResetFighter(NPC_KATHZEN);
            ResetFighter(NPC_JUTHZA);
            if (me->IsInCombat())
                ScriptedAI::EnterEvadeMode(EVADE_REASON_OTHER);
            Reset();
        }

        void DoAction(int32 action) override
        {
            switch (action)
            {
                case ACTION_KATHZEN_DIED:
                    if (_phase == PHASE_KATHZEN)
                        StartJuthza();
                    else if (_phase == PHASE_JUTHZA && FightersDead())
                        StartRazjal();
                    break;
                case ACTION_JUTHZA_DIED:
                    if (_phase == PHASE_JUTHZA && FightersDead())
                        StartRazjal();
                    break;
                case ACTION_ARENA_RESET:
                    if (_phase != PHASE_IDLE)
                        ResetArena();
                    break;
                default:
                    break;
            }
        }

        void AttackStart(Unit* who) override
        {
            if (_phase != PHASE_SCORPIDS)
                ScriptedAI::AttackStart(who);
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            if (_phase != PHASE_IDLE)
            {
                ResetArena();
                return;
            }
            ScriptedAI::EnterEvadeMode(why);
        }

        void JustDied(Unit* /*killer*/) override
        {
            ApplyRazjalIntermissionImmunity(me, false);
            DespawnScorpids();
        }

        void UpdateAI(uint32 diff) override
        {
            switch (_phase)
            {
                case PHASE_IDLE:
                    if (!UpdateVictim())
                        return;
                    UpdateList(diff);
                    DoMeleeAttackIfReady();
                    return;
                case PHASE_INTRO:
                    if (_introTimer <= diff)
                    {
                        Talk(TEXT_RAZJAL_INTRO);
                        _introTimer = 8 * IN_MILLISECONDS;
                        _phase = PHASE_KATHZEN;
                    }
                    else
                        _introTimer -= diff;
                    return;
                case PHASE_KATHZEN:
                    if (_introTimer)
                    {
                        if (_introTimer <= diff)
                        {
                            _introTimer = 0;
                            StartKathzen();
                        }
                        else
                            _introTimer -= diff;
                        return;
                    }
                    if (_nextPhaseTimer <= diff)
                        StartJuthza();
                    else
                        _nextPhaseTimer -= diff;
                    return;
                case PHASE_JUTHZA:
                    if (FightersDead() || _nextPhaseTimer <= diff)
                        StartRazjal();
                    else
                        _nextPhaseTimer -= diff;
                    return;
                case PHASE_SCORPIDS:
                    if (_scorpidStartTimer)
                    {
                        if (_scorpidStartTimer <= diff)
                            _scorpidStartTimer = 0;
                        else
                        {
                            _scorpidStartTimer -= diff;
                            return;
                        }
                    }
                    if (_scorpidsSpawned < 10)
                    {
                        if (_scorpidSpawnTimer <= diff)
                        {
                            SpawnScorpid();
                            _scorpidSpawnTimer = 2 * IN_MILLISECONDS;
                        }
                        else
                            _scorpidSpawnTimer -= diff;
                    }
                    else
                        EndSands();
                    return;
                case PHASE_RAZJAL:
                    break;
            }

            if (!_sandsStarted && me->GetHealthPct() <= 50.0f)
            {
                StartSands();
                return;
            }

            if (_finalStarted && me->IsNonMeleeSpellCast(false))
                return;

            if (!_finalStarted && me->GetHealthPct() <= 10.0f)
            {
                _finalStarted = true;
                Talk(TEXT_RAZJAL_FINAL);
                me->InterruptNonMeleeSpells(false);
                me->CastSpell(me, SPELL_HELLFIRE, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST);
                return;
            }

            if (!UpdateVictim())
                return;
            UpdateList(diff);
            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Zel'jeb the Ancient: SmartAI (spells, lines) + Curse of Years at 50%.
    // ------------------------------------------------------------------
    struct npc_zeljeb_the_ancientAI : public SmartAI
    {
        explicit npc_zeljeb_the_ancientAI(Creature* c) : SmartAI(c) { }

        enum
        {
            SPELL_C_CURSE_CAST   = 46627,   // 6 s cast, no effect
            SPELL_C_CURSE_DOT    = 11442,   // damage + mana drain every 10 s
            SPELL_C_CURSE_STATS  = 13524,   // all stats down
        };
        static constexpr int32 CURSE_DURATION = 60000;
        static constexpr int32 CURSE_TICK     = 500;    // Turtle: 250 every 5 s
        static constexpr int32 CURSE_STATS    = -40;
        static constexpr float CURSE_RADIUS   = 20.0f;

        bool _cursed = false;

        void JustEngagedWith(Unit* who) override
        {
            _cursed = false;
            SmartAI::JustEngagedWith(who);
        }

        void OnSpellCast(SpellInfo const* spell) override
        {
            SmartAI::OnSpellCast(spell);
            if (!spell || spell->Id != SPELL_C_CURSE_CAST)
                return;
            std::vector<Unit*> targets;
            EnemiesNear(me, *me, CURSE_RADIUS, targets);
            for (Unit* target : targets)
            {
                TuneAura(me->AddAura(SPELL_C_CURSE_DOT, target), CURSE_DURATION, CURSE_TICK, CURSE_TICK);
                TuneAura(me->AddAura(SPELL_C_CURSE_STATS, target), CURSE_DURATION, CURSE_STATS);
            }
        }

        void UpdateAI(uint32 diff) override
        {
            if (!_cursed && me->IsInCombat() && me->GetHealthPct() <= 50.0f && !me->HasUnitState(UNIT_STATE_CASTING))
                if (me->CastSpell(me, SPELL_C_CURSE_CAST, false) == SPELL_CAST_OK)
                    _cursed = true;
            SmartAI::UpdateAI(diff);
        }
    };

    CreatureAI* MakeKathzen(Creature* c) { return new npc_arena_fighterAI(c, true); }
    CreatureAI* MakeJuthza(Creature* c) { return new npc_arena_fighterAI(c, false); }
    CreatureAI* MakeRazjal(Creature* c) { return new npc_champion_razjalAI(c); }
    CreatureAI* MakeZeljeb(Creature* c) { return new npc_zeljeb_the_ancientAI(c); }
}

void AddSC_turtle_zulfarrak()
{
    RegisterAI(NPC_KATHZEN, &MakeKathzen);
    RegisterAI(NPC_JUTHZA,  &MakeJuthza);
    RegisterAI(NPC_RAZJAL,  &MakeRazjal);
    RegisterAI(NPC_ZELJEB,  &MakeZeljeb);
}
