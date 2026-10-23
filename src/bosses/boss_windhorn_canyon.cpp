/*
 * mod-turtle-content - Windhorn Canyon (map 820) boss scripts.
 *
 * Ported from tortoise-wow-main/src/scripts/dungeons/windhorn_canyon
 * (boss_bonespeaker_narlgom.cpp, windhorn_canyon.cpp, windhorn_canyon.h).
 *
 * - Bonespeaker Narlgom and Champion Rotag: Turtle C++ AI (Narlgom has no
 *   spell list; Rotag is the dead champion Narlgom channels on).
 * - Chieftain Shalk Blackwind and the Storm Guardians: Turtle runs their
 *   spell lists plus a C++ script. Their converted SmartAI rows (the spell
 *   lists) are kept: the AIs below are SmartAI with Turtle's C++ on top.
 * - The other Windhorn bosses (Pathun Duskhide, Prophet Stormhoof,
 *   Ambassador Vortalus, Walgan Bloodcaller, Ahgk'tos the Pure, Grand Elder
 *   Skystrider) have no Turtle C++ AI and keep their converted SmartAI.
 *
 * Turtle-only spells (41121, 42004, 51187, 57747 are other spells in 3.3.5)
 * use 3.3.5 carriers with Turtle's values (Turtle server Spell.dbc).
 *
 * Trash and bosses whose Turtle spells the converter dropped (Turtle world DB
 * creature_spells / creature_ai_events; timers are Turtle's, in ms):
 *  - Blackwind Geologist: 36918 Molten Blast (2 s, 136-155 fire) -> 15095
 *    Molten Blast; 45526 "Earth Shield" (heals himself 85) -> 20167 heal.
 *  - Blackwind Earthkeeper: 36729 Summon Lesser Stone Elemental (3 s cast)
 *    and Deathtotem Shaman: 36731 Summon Scorpid Totem (3 s cast) -> 3 s
 *    carrier cast 44433 (visual 74, no effect), then the summon.
 *  - Prophet Stormhoof: 57748 Wail of Souls -> 17631 (same spell data).
 *  - Deathtotem Behemoth: 31771 Pulverize (160 to enemies within 8 yd) ->
 *    41059 Whirlwind set to 160, radius 8.
 *  - Blackwind Overseer: 36730 Blackwind Aura (+25% attack speed to allies)
 *    -> 41106 Battle Aura (same visual, same +25%).
 *  - Blackwind Bloodguard: 36732 Bloodguard Ritual at 50% (+50% damage,
 *    -65% speed, +54% size, 2 min) -> 40417 Rage set to those values.
 *  - Ambassador Vortalus: 36578 Engulfing Vortex at 50% (every enemy within
 *    30 yd takes 100 Nature every 3 s and has -10% chance to hit) -> 5570
 *    Insect Swarm on each enemy in range (67 every 2 s, -10% hit).
 */

#include "turtle_boss_common.h"
#include "Log.h"
#include "Map.h"
#include "SmartAI.h"

using namespace TurtleBoss;

namespace
{
    enum WindhornCreatures
    {
        NPC_BONESPEAKER_NARLGOM      = 62780,
        NPC_CHIEFTAIN_SHALK          = 62782,
        NPC_CHAMPION_ROTAG           = 62785,
        NPC_BLACKWIND_BLOODGUARD     = 62771,
        NPC_STORM_GUARDIAN           = 62865,
        NPC_STORM_RESIDUE            = 62866,  // added by mod_turtle_902_windhorn_missing.sql
        NPC_SPIRIT_OF_ROTAG          = 61410,  // Turtle 42004 summon; added by mod_turtle_902_windhorn_missing.sql
        NPC_BLACKWIND_GEOLOGIST      = 62765,
        NPC_BLACKWIND_OVERSEER       = 62766,
        NPC_BLACKWIND_EARTHKEEPER    = 62770,
        NPC_DEATHTOTEM_SHAMAN        = 62773,
        NPC_PROPHET_STORMHOOF        = 62781,
        NPC_AMBASSADOR_VORTALUS      = 62783,
        NPC_DEATHTOTEM_BEHEMOTH      = 62985,
        NPC_LESSER_STONE_ELEMENTAL   = 62969,  // added by mod_turtle_905_windhorn_summons.sql
        NPC_SCORPID_TOTEM            = 49019,  // added by mod_turtle_905_windhorn_summons.sql
    };

    enum WindhornSpells
    {
        // Same spell, same data in both cores
        SPELL_BONE_ARMOR             = 11445,
        SPELL_RAIN_OF_FIRE           = 16005,  // Turtle 57747: identical values (3.3.5 copy of the same spell)

        // Carriers for Turtle-only spells
        SPELL_C_ARCANE_CHANNELING    = 30662,  // Turtle 51187 Targeted Arcane Channeling: dummy channel, visual 277
        SPELL_C_SUMMON_ROTAG         = 8677,   // Turtle 42004 Summon Rotag: 5 sec cast, visual 74, not kickable
        SPELL_C_FLAME_OF_SHALK_CAST  = 11970,  // Turtle 41121: 2 sec kickable fire cast, visual 963 (radius set to 0: no hit)
        SPELL_C_FLAME_OF_SHALK_DOT   = 48733,  // Turtle 41121: 200 fire every 5 sec, 1 min, every enemy within 200 yd
        SPELL_C_FLAME_OF_SHALK_HEAL  = 56112,  // Turtle 41121: -50% healing taken, 1 min
        SPELL_C_MOLTEN_BLAST         = 15095,  // Turtle 36918
        SPELL_C_EARTH_SHIELD         = 20167,  // Turtle 45526 (a self heal)
        SPELL_C_SUMMON_CAST          = 44433,  // Turtle 36729 / 36731: 3 sec cast, visual 74, sends an unused event
        SPELL_WAIL_OF_SOULS          = 17631,  // Turtle 57748: same data
        SPELL_C_PULVERIZE            = 41059,  // Turtle 31771
        SPELL_C_BLACKWIND_AURA       = 41106,  // Turtle 36730
        SPELL_C_BLOODGUARD_RITUAL    = 40417,  // Turtle 36732
        SPELL_C_ENGULFING_VORTEX     = 5570,   // Turtle 36578, applied to each enemy in range
    };

    // Turtle creature_spells timers: first cast after rand(initial), then rand(repeat).
    struct TurtleSpellTimer
    {
        uint32 initialMin, initialMax, repeatMin, repeatMax;
        uint32 timer = 0;

        void Start() { timer = urand(initialMin, initialMax); }
        void Next() { timer = urand(repeatMin, repeatMax); }
        bool Ready(uint32 diff)
        {
            if (timer <= diff)
                return true;
            timer -= diff;
            return false;
        }
    };

    // Non-triggered cast (fails while casting, like vmangos DoCastSpellIfCan) with base points.
    bool CastWithValues(Creature* caster, Unit* target, uint32 spellId, CustomSpellValues const& values)
    {
        if (!caster || !target || caster->HasUnitState(UNIT_STATE_CASTING))
            return false;
        return caster->CastCustomSpell(spellId, values, target, TRIGGERED_NONE) == SPELL_CAST_OK;
    }

    // Same spell in both cores: cast it with Turtle's level scaling.
    bool CastTurtleScaled(Creature* caster, Unit* target, uint32 spellId)
    {
        if (!caster || !target || caster->HasUnitState(UNIT_STATE_CASTING))
            return false;
        SpellInfo const* info = sSpellMgr->GetSpellInfo(spellId);
        if (!info)
            return false;
        CustomSpellValues values;
        if (TurtleScaledValues(caster, info, values))
            return caster->CastCustomSpell(spellId, values, target, TRIGGERED_NONE) == SPELL_CAST_OK;
        return caster->CastSpell(target, spellId, false) == SPELL_CAST_OK;
    }

    constexpr float MOLTEN_BLAST_AVERAGE    = 145.5f;  // Turtle 36918: 135 + 1d20
    constexpr float EARTH_SHIELD_HEAL       = 85.0f;   // Turtle 45526: 84 + 1
    constexpr float PULVERIZE_DAMAGE        = 160.0f;  // Turtle 31771: 159 + 1
    constexpr int32 PULVERIZE_RADIUS_MOD    = 8000;    // 41059 hits 10 yd; Turtle 8 yd
    constexpr uint32 SUMMON_DURATION        = 3600000; // Turtle 36729 / 36731: 1 hour
    constexpr int32 BLOODGUARD_DURATION     = 120000;
    constexpr int32 BLOODGUARD_DAMAGE_PCT   = 50;
    constexpr int32 BLOODGUARD_SPEED_PCT    = -65;
    constexpr int32 BLOODGUARD_SCALE_PCT    = 54;
    constexpr float VORTEX_RADIUS           = 30.0f;
    constexpr int32 VORTEX_TICK_DAMAGE      = 67;      // 100 per 3 s on Turtle; 5570 ticks every 2 s
    constexpr int32 VORTEX_HIT_PCT          = -10;
    constexpr int32 VORTEX_REFRESH_MS       = 4000;

    constexpr int32 FLAME_OF_SHALK_DURATION = 60000;
    constexpr int32 FLAME_OF_SHALK_TICK     = 200;
    constexpr int32 FLAME_OF_SHALK_HEALING  = -50;
    constexpr float FLAME_OF_SHALK_RADIUS   = 200.0f;

    // Flame of Shalk was in Shalk's Turtle spell list, which the converter
    // dropped (Turtle-only spell). Its timers (initial / repeat, ms) come
    // from that list (Turtle world DB, creature_spells 62782).
    constexpr uint32 FLAME_OF_SHALK_INITIAL_MIN = 11000;  // Turtle creature_spells 62782, slot 2
    constexpr uint32 FLAME_OF_SHALK_INITIAL_MAX = 13000;
    constexpr uint32 FLAME_OF_SHALK_REPEAT_MIN  = 32000;
    constexpr uint32 FLAME_OF_SHALK_REPEAT_MAX  = 47000;

    Position const BloodguardSpawn = { -7546.968750f, -3762.458008f, 282.898224f, 5.498519f };

    // ------------------------------------------------------------------
    // Bonespeaker Narlgom
    // ------------------------------------------------------------------
    struct boss_bonespeaker_narlgomAI : public TurtleBossAI
    {
        explicit boss_bonespeaker_narlgomAI(Creature* c) : TurtleBossAI(c) { }

        bool _allowIdleChannel = true;
        bool _summonedRotag = false;
        uint32 _boneArmorTimer = 0;
        uint32 _rainOfFireTimer = 0;
        uint32 _idleChannelTimer = 0;

        void Reset() override
        {
            _boneArmorTimer = urand(0, 1 * IN_MILLISECONDS);
            _rainOfFireTimer = urand(1 * IN_MILLISECONDS, 2 * IN_MILLISECONDS);
            _idleChannelTimer = 1 * IN_MILLISECONDS;
            _summonedRotag = false;
        }

        void JustEngagedWith(Unit* /*who*/) override
        {
            _allowIdleChannel = false;
            StopIdleChannel();
            Yell(me, "My powers will lead us to victory!");
        }

        void JustDied(Unit* /*killer*/) override { Yell(me, "I do not fear death... I embrace it..."); }

        void JustReachedHome() override
        {
            _allowIdleChannel = true;
            _idleChannelTimer = 1 * IN_MILLISECONDS;
        }

        void JustRespawned() override
        {
            _allowIdleChannel = true;
            TurtleBossAI::JustRespawned();
        }

        // Turtle 42004 summons the spirit when the 5 sec cast completes.
        void OnSpellCast(SpellInfo const* spell) override
        {
            if (!spell || spell->Id != SPELL_C_SUMMON_ROTAG)
                return;

            if (!sObjectMgr->GetCreatureTemplate(NPC_SPIRIT_OF_ROTAG))
            {
                LOG_ERROR("module", "mod-turtle-content: Bonespeaker Narlgom: creature {} (Turtle Summon Rotag) is missing from the database", uint32(NPC_SPIRIT_OF_ROTAG));
                return;
            }

            Position pos = me->GetNearPosition(CONTACT_DISTANCE, float(M_PI) / 4.0f); // TARGET_LOCATION_CASTER_FRONT_LEFT
            if (Creature* spirit = me->SummonCreature(NPC_SPIRIT_OF_ROTAG, pos, TEMPSUMMON_CORPSE_DESPAWN))
                if (Unit* target = me->GetVictim())
                    spirit->AI()->AttackStart(target);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!me->IsInCombat())
            {
                UpdateIdleChannel(diff);
                return;
            }

            if (!UpdateVictim())
                return;

            if (!_summonedRotag && me->GetHealthPct() <= 50.0f)
            {
                // DoCastSpellIfCan(CF_INTERRUPT_PREVIOUS)
                me->InterruptNonMeleeSpells(false);
                if (TryCast(me, SPELL_C_SUMMON_ROTAG))
                {
                    _summonedRotag = true;
                    Yell(me, "The Windhorn were just a nuisance!");
                    return;
                }
            }

            if (_boneArmorTimer <= diff)
            {
                // CF_AURA_NOT_PRESENT
                if (!me->HasAura(SPELL_BONE_ARMOR) && TryCast(me, SPELL_BONE_ARMOR))
                {
                    _boneArmorTimer = urand(14 * IN_MILLISECONDS, 31 * IN_MILLISECONDS);
                    return;
                }
            }
            else
                _boneArmorTimer -= diff;

            if (_rainOfFireTimer <= diff)
            {
                if (TryCast(me->GetVictim(), SPELL_RAIN_OF_FIRE))
                {
                    _rainOfFireTimer = urand(17 * IN_MILLISECONDS, 22 * IN_MILLISECONDS);
                    return;
                }
            }
            else
                _rainOfFireTimer -= diff;

            DoMeleeAttackIfReady();
        }

        Creature* GetChampionRotag() const
        {
            return me->FindNearestCreature(NPC_CHAMPION_ROTAG, 100.0f, true);
        }

        void UpdateIdleChannel(uint32 diff)
        {
            if (!_allowIdleChannel || me->IsNonMeleeSpellCast(false))
                return;

            if (_idleChannelTimer > diff)
            {
                _idleChannelTimer -= diff;
                return;
            }

            if (Creature* rotag = GetChampionRotag())
            {
                // CF_FORCE_CAST
                if (me->CastSpell(rotag, SPELL_C_ARCANE_CHANNELING, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST) == SPELL_CAST_OK)
                {
                    rotag->SetStandState(UNIT_STAND_STATE_DEAD);
                    _idleChannelTimer = 5 * IN_MILLISECONDS;
                    return;
                }
            }

            _idleChannelTimer = 1 * IN_MILLISECONDS;
        }

        void StopIdleChannel()
        {
            me->InterruptNonMeleeSpells(false, SPELL_C_ARCANE_CHANNELING);

            if (Creature* rotag = GetChampionRotag())
            {
                rotag->RemoveAurasDueToSpell(SPELL_C_ARCANE_CHANNELING);
                rotag->CombatStop(true);
                rotag->SetStandState(UNIT_STAND_STATE_DEAD);
            }
        }
    };

    // ------------------------------------------------------------------
    // Champion Rotag: lies dead, never fights.
    // ------------------------------------------------------------------
    struct npc_champion_rotagAI : public ScriptedAI
    {
        explicit npc_champion_rotagAI(Creature* c) : ScriptedAI(c) { }

        void Reset() override
        {
            me->SetReactState(REACT_PASSIVE);
            me->SetStandState(UNIT_STAND_STATE_DEAD);
        }

        void MoveInLineOfSight(Unit* /*who*/) override { }
        void AttackStart(Unit* /*who*/) override { }
        void JustEngagedWith(Unit* /*who*/) override { me->SetStandState(UNIT_STAND_STATE_DEAD); }

        void UpdateAI(uint32 /*diff*/) override
        {
            if (me->IsInCombat())
                me->CombatStop(true);

            if (me->getStandState() != UNIT_STAND_STATE_DEAD)
                me->SetStandState(UNIT_STAND_STATE_DEAD);
        }
    };

    // ------------------------------------------------------------------
    // Chieftain Shalk Blackwind: SmartAI (Turtle spell list) + Turtle C++.
    // ------------------------------------------------------------------
    struct boss_chieftain_shalk_blackwindAI : public SmartAI
    {
        explicit boss_chieftain_shalk_blackwindAI(Creature* c) : SmartAI(c) { }

        bool _summonedBloodguard = false;
        bool _pollForFlameAura = false;
        uint32 _underwaterCheckTimer = 250;
        uint32 _flameOfShalkTimer = 0;

        static bool FlameOfShalkScheduled() { return FLAME_OF_SHALK_REPEAT_MAX != 0; }

        void ResetTurtleState()
        {
            _summonedBloodguard = false;
            _underwaterCheckTimer = 250;
            if (FlameOfShalkScheduled())
                _flameOfShalkTimer = urand(FLAME_OF_SHALK_INITIAL_MIN, FLAME_OF_SHALK_INITIAL_MAX);
        }

        void JustEngagedWith(Unit* who) override
        {
            ResetTurtleState();
            SmartAI::JustEngagedWith(who);
            Yell(me, "You challenge the chieftain of the Blackwind? So be it.");
        }

        void JustDied(Unit* killer) override
        {
            Yell(me, "My death means little... the Grimtotem shall not be defeated...");
            SmartAI::JustDied(killer);
        }

        // Turtle 41121: 2 sec cast, then every enemy within 200 yd burns (dive under water to put it out).
        bool CastFlameOfShalk()
        {
            if (me->HasUnitState(UNIT_STATE_CASTING))
                return false;
            CustomSpellValues values;
            values.AddSpellMod(SPELLVALUE_RADIUS_MOD, 0);
            return me->CastCustomSpell(SPELL_C_FLAME_OF_SHALK_CAST, values, me, TRIGGERED_IGNORE_POWER_AND_REAGENT_COST) == SPELL_CAST_OK;
        }

        void OnSpellCast(SpellInfo const* spell) override
        {
            if (!spell || spell->Id != SPELL_C_FLAME_OF_SHALK_CAST)
                return;

            std::vector<Unit*> targets;
            EnemiesNear(me, *me, FLAME_OF_SHALK_RADIUS, targets);
            for (Unit* target : targets)
            {
                TuneAura(me->AddAura(SPELL_C_FLAME_OF_SHALK_DOT, target), FLAME_OF_SHALK_DURATION, FLAME_OF_SHALK_TICK);
                TuneAura(me->AddAura(SPELL_C_FLAME_OF_SHALK_HEAL, target), FLAME_OF_SHALK_DURATION, FLAME_OF_SHALK_HEALING);
            }
        }

        static bool HasFlameOfShalk(Player* player)
        {
            return player->HasAura(SPELL_C_FLAME_OF_SHALK_DOT) || player->HasAura(SPELL_C_FLAME_OF_SHALK_HEAL);
        }

        void UpdateAI(uint32 diff) override
        {
            if (!_summonedBloodguard && me->IsInCombat() && me->GetHealthPct() <= 50.0f)
            {
                Yell(me, "The Grimtotem will endure!");

                if (Creature* guard = me->SummonCreature(NPC_BLACKWIND_BLOODGUARD, BloodguardSpawn, TEMPSUMMON_TIMED_OR_DEAD_DESPAWN, 300000))
                {
                    Yell(guard, "Chieftain I come to your aid!");
                    if (Unit* target = SelectTarget(SelectTargetMethod::Random, 0))
                        guard->AI()->AttackStart(target);
                }

                _summonedBloodguard = true;
            }

            if (FlameOfShalkScheduled() && me->IsInCombat() && me->GetVictim())
            {
                if (_flameOfShalkTimer <= diff)
                {
                    if (CastFlameOfShalk())
                        _flameOfShalkTimer = urand(FLAME_OF_SHALK_REPEAT_MIN, FLAME_OF_SHALK_REPEAT_MAX);
                }
                else
                    _flameOfShalkTimer -= diff;
            }

            if (me->IsInCombat())
                _pollForFlameAura = true;

            if (_pollForFlameAura && _underwaterCheckTimer <= diff)
            {
                _pollForFlameAura = false;

                for (auto const& itr : me->GetMap()->GetPlayers())
                {
                    Player* player = itr.GetSource();
                    if (!player || !HasFlameOfShalk(player))
                        continue;

                    if (player->IsUnderWater())
                    {
                        player->RemoveAurasDueToSpell(SPELL_C_FLAME_OF_SHALK_DOT, me->GetGUID());
                        player->RemoveAurasDueToSpell(SPELL_C_FLAME_OF_SHALK_HEAL, me->GetGUID());
                    }
                    else
                        _pollForFlameAura = true;
                }

                _underwaterCheckTimer = 500;
            }
            else if (_pollForFlameAura)
                _underwaterCheckTimer -= diff;

            SmartAI::UpdateAI(diff);
        }
    };

    // ------------------------------------------------------------------
    // Storm Guardian: SmartAI (Turtle spell list) + splits on death.
    // ------------------------------------------------------------------
    struct npc_windhorn_storm_guardianAI : public SmartAI
    {
        explicit npc_windhorn_storm_guardianAI(Creature* c) : SmartAI(c) { }

        void JustDied(Unit* killer) override
        {
            Unit* target = SelectTarget(SelectTargetMethod::Random, 0);
            if (!target && killer && killer->IsAlive())
                target = killer;

            SmartAI::JustDied(killer);

            if (!sObjectMgr->GetCreatureTemplate(NPC_STORM_RESIDUE))
            {
                LOG_ERROR("module", "mod-turtle-content: Storm Guardian: creature {} (Storm Residue) is missing from the database", uint32(NPC_STORM_RESIDUE));
                return;
            }

            static constexpr float offsets[3][2] =
            {
                {  1.50f,  0.00f },
                { -0.75f,  1.30f },
                { -0.75f, -1.30f },
            };

            for (auto const& offset : offsets)
            {
                if (Creature* residue = me->SummonCreature(NPC_STORM_RESIDUE,
                        me->GetPositionX() + offset[0], me->GetPositionY() + offset[1], me->GetPositionZ(), me->GetOrientation(),
                        TEMPSUMMON_TIMED_OR_DEAD_DESPAWN, 300000))
                    if (target)
                        residue->AI()->AttackStart(target);
            }
        }
    };

    // ------------------------------------------------------------------
    // Blackwind Geologist: SmartAI (Turtle spell list, 10412) + the 2 dropped spells.
    // ------------------------------------------------------------------
    struct npc_blackwind_geologistAI : public SmartAI
    {
        explicit npc_blackwind_geologistAI(Creature* c) : SmartAI(c) { }

        TurtleSpellTimer _moltenBlast { 1000, 3000, 7000, 20000 };
        TurtleSpellTimer _earthShield { 8000, 9000, 5000, 9000 };

        void JustEngagedWith(Unit* who) override
        {
            _moltenBlast.Start();
            _earthShield.Start();
            SmartAI::JustEngagedWith(who);
        }

        void UpdateAI(uint32 diff) override
        {
            if (me->IsInCombat() && me->GetVictim())
            {
                if (_moltenBlast.Ready(diff))
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_MOLTEN_BLAST, EFFECT_0, MOLTEN_BLAST_AVERAGE));
                    if (CastWithValues(me, me->GetVictim(), SPELL_C_MOLTEN_BLAST, values))
                        _moltenBlast.Next();
                }
                if (_earthShield.Ready(diff))
                {
                    CustomSpellValues values;
                    values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_EARTH_SHIELD, EFFECT_0, EARTH_SHIELD_HEAL));
                    if (CastWithValues(me, me, SPELL_C_EARTH_SHIELD, values))
                        _earthShield.Next();
                }
            }
            SmartAI::UpdateAI(diff);
        }
    };

    // ------------------------------------------------------------------
    // Blackwind Earthkeeper / Deathtotem Shaman: 3 sec cast, then a summon.
    // ------------------------------------------------------------------
    template <class Base>
    struct windhorn_summonerAI : public Base
    {
        windhorn_summonerAI(Creature* c, uint32 summonEntry, TurtleSpellTimer timer, bool guardian)
            : Base(c), _entry(summonEntry), _timer(timer), _guardian(guardian) { }

        uint32 _entry;
        TurtleSpellTimer _timer;
        bool _guardian;
        GuidList _guardians;

        void JustEngagedWith(Unit* who) override
        {
            _timer.Start();
            Base::JustEngagedWith(who);
        }

        void OnSpellCast(SpellInfo const* spell) override
        {
            Base::OnSpellCast(spell);
            if (!spell || spell->Id != SPELL_C_SUMMON_CAST)
                return;

            if (!sObjectMgr->GetCreatureTemplate(_entry))
            {
                LOG_ERROR("module", "mod-turtle-content: Windhorn summoner {}: creature {} is missing from the database", this->me->GetEntry(), _entry);
                return;
            }

            Position pos = this->me->GetNearPosition(2.0f, frand(0.0f, 2.0f * float(M_PI)));
            Creature* summon = this->me->SummonCreature(_entry, pos, TEMPSUMMON_TIMED_OR_DEAD_DESPAWN, SUMMON_DURATION);
            if (!summon)
                return;
            if (_guardian)
            {
                // Turtle summon guardian: follows its shaman and goes when he dies.
                _guardians.push_back(summon->GetGUID());
                summon->GetMotionMaster()->MoveFollow(this->me, PET_FOLLOW_DIST, frand(0.0f, 2.0f * float(M_PI)));
            }
            if (Unit* victim = this->me->GetVictim())
                summon->AI()->AttackStart(victim);
        }

        void JustDied(Unit* killer) override
        {
            for (ObjectGuid const& guid : _guardians)
                if (Creature* guardian = ObjectAccessor::GetCreature(*this->me, guid))
                    guardian->DespawnOrUnsummon();
            _guardians.clear();
            Base::JustDied(killer);
        }

        void UpdateAI(uint32 diff) override
        {
            if (this->me->IsInCombat() && this->me->GetVictim() && _timer.Ready(diff))
                if (!this->me->HasUnitState(UNIT_STATE_CASTING) && this->me->CastSpell(this->me, SPELL_C_SUMMON_CAST, false) == SPELL_CAST_OK)
                    _timer.Next();
            Base::UpdateAI(diff);
        }
    };

    struct npc_blackwind_earthkeeperAI : public windhorn_summonerAI<ScriptedAI>
    {
        explicit npc_blackwind_earthkeeperAI(Creature* c)
            : windhorn_summonerAI<ScriptedAI>(c, NPC_LESSER_STONE_ELEMENTAL, { 18000, 24000, 60000, 90000 }, false) { }
    };

    struct npc_deathtotem_shamanAI : public windhorn_summonerAI<SmartAI>
    {
        explicit npc_deathtotem_shamanAI(Creature* c)
            : windhorn_summonerAI<SmartAI>(c, NPC_SCORPID_TOTEM, { 20000, 25000, 14000, 24000 }, true) { }
    };

    // ------------------------------------------------------------------
    // Prophet Stormhoof: SmartAI (texts, Corruption, Curse of Agony) + Wail of Souls.
    // ------------------------------------------------------------------
    struct npc_prophet_stormhoofAI : public SmartAI
    {
        explicit npc_prophet_stormhoofAI(Creature* c) : SmartAI(c) { }

        TurtleSpellTimer _wail { 4000, 5000, 13000, 22000 };

        void JustEngagedWith(Unit* who) override
        {
            _wail.Start();
            SmartAI::JustEngagedWith(who);
        }

        void UpdateAI(uint32 diff) override
        {
            if (me->IsInCombat() && me->GetVictim() && _wail.Ready(diff))
                if (CastTurtleScaled(me, me->GetVictim(), SPELL_WAIL_OF_SOULS))
                    _wail.Next();
            SmartAI::UpdateAI(diff);
        }
    };

    // ------------------------------------------------------------------
    // Deathtotem Behemoth: SmartAI (Consuming Rage at 50%) + Pulverize.
    // ------------------------------------------------------------------
    struct npc_deathtotem_behemothAI : public SmartAI
    {
        explicit npc_deathtotem_behemothAI(Creature* c) : SmartAI(c) { }

        TurtleSpellTimer _pulverize { 4000, 21000, 15000, 22000 };

        void JustEngagedWith(Unit* who) override
        {
            _pulverize.Start();
            SmartAI::JustEngagedWith(who);
        }

        void UpdateAI(uint32 diff) override
        {
            if (me->IsInCombat() && me->GetVictim() && _pulverize.Ready(diff))
            {
                CustomSpellValues values;
                values.AddSpellMod(SPELLVALUE_BASE_POINT0, BasePointsFor(me, SPELL_C_PULVERIZE, EFFECT_0, PULVERIZE_DAMAGE));
                values.AddSpellMod(SPELLVALUE_RADIUS_MOD, PULVERIZE_RADIUS_MOD);
                if (CastWithValues(me, me, SPELL_C_PULVERIZE, values))
                    _pulverize.Next();
            }
            SmartAI::UpdateAI(diff);
        }
    };

    // ------------------------------------------------------------------
    // Blackwind Overseer: Blackwind Aura on spawn and after evading.
    // ------------------------------------------------------------------
    struct npc_blackwind_overseerAI : public ScriptedAI
    {
        explicit npc_blackwind_overseerAI(Creature* c) : ScriptedAI(c) { }

        uint32 _auraCheck = 1000;

        void UpdateAI(uint32 diff) override
        {
            if (!me->IsInCombat())
            {
                if (_auraCheck <= diff)
                {
                    _auraCheck = 1000;
                    if (!me->HasAura(SPELL_C_BLACKWIND_AURA) && !me->IsInEvadeMode())
                        me->CastSpell(me, SPELL_C_BLACKWIND_AURA, true);
                }
                else
                    _auraCheck -= diff;
                return;
            }

            if (!UpdateVictim())
                return;
            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Blackwind Bloodguard: Bloodguard Ritual at 50% health (once).
    // ------------------------------------------------------------------
    struct npc_blackwind_bloodguardAI : public ScriptedAI
    {
        explicit npc_blackwind_bloodguardAI(Creature* c) : ScriptedAI(c) { }

        bool _ritual = false;

        void Reset() override { _ritual = false; }

        void SpellHitTarget(Unit* target, SpellInfo const* spell) override
        {
            if (target == me && spell && spell->Id == SPELL_C_BLOODGUARD_RITUAL)
                TuneAura(me->GetAura(SPELL_C_BLOODGUARD_RITUAL, me->GetGUID()), BLOODGUARD_DURATION,
                    BLOODGUARD_DAMAGE_PCT, BLOODGUARD_SPEED_PCT, BLOODGUARD_SCALE_PCT);
        }

        void UpdateAI(uint32 /*diff*/) override
        {
            if (!UpdateVictim())
                return;

            if (!_ritual && me->GetHealthPct() <= 50.0f && !me->HasUnitState(UNIT_STATE_CASTING))
                if (me->CastSpell(me, SPELL_C_BLOODGUARD_RITUAL, false) == SPELL_CAST_OK)
                    _ritual = true;

            DoMeleeAttackIfReady();
        }
    };

    // ------------------------------------------------------------------
    // Ambassador Vortalus: SmartAI (texts, spells) + Engulfing Vortex at 50%.
    // ------------------------------------------------------------------
    struct npc_ambassador_vortalusAI : public SmartAI
    {
        explicit npc_ambassador_vortalusAI(Creature* c) : SmartAI(c) { }

        bool _vortex = false;
        uint32 _vortexTimer = 0;

        void StopVortex()
        {
            _vortex = false;
            for (auto const& itr : me->GetMap()->GetPlayers())
                if (Player* player = itr.GetSource())
                    player->RemoveAurasDueToSpell(SPELL_C_ENGULFING_VORTEX, me->GetGUID());
        }

        void JustEngagedWith(Unit* who) override
        {
            StopVortex();
            SmartAI::JustEngagedWith(who);
        }

        void JustDied(Unit* killer) override
        {
            StopVortex();
            SmartAI::JustDied(killer);
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            StopVortex();
            SmartAI::EnterEvadeMode(why);
        }

        void UpdateVortex(uint32 diff)
        {
            if (_vortexTimer > diff)
            {
                _vortexTimer -= diff;
                return;
            }
            _vortexTimer = 1000;

            std::vector<Unit*> targets;
            EnemiesNear(me, *me, VORTEX_RADIUS, targets, false);
            for (Unit* target : targets)
            {
                if (Aura* aura = target->GetAura(SPELL_C_ENGULFING_VORTEX, me->GetGUID()))
                    aura->SetDuration(VORTEX_REFRESH_MS);
                else
                    TuneAura(me->AddAura(SPELL_C_ENGULFING_VORTEX, target), VORTEX_REFRESH_MS, VORTEX_TICK_DAMAGE, VORTEX_HIT_PCT);
            }
        }

        void UpdateAI(uint32 diff) override
        {
            if (me->IsInCombat())
            {
                if (!_vortex && me->GetHealthPct() <= 50.0f)
                {
                    _vortex = true;
                    _vortexTimer = 0;
                }
                if (_vortex)
                    UpdateVortex(diff);
            }
            SmartAI::UpdateAI(diff);
        }
    };

    template <class AI>
    CreatureAI* MakeWindhorn(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_windhorn_canyon()
{
    RegisterAI(NPC_BONESPEAKER_NARLGOM, &MakeWindhorn<boss_bonespeaker_narlgomAI>);
    RegisterAI(NPC_CHAMPION_ROTAG,      &MakeWindhorn<npc_champion_rotagAI>);
    RegisterAI(NPC_CHIEFTAIN_SHALK,     &MakeWindhorn<boss_chieftain_shalk_blackwindAI>);
    RegisterAI(NPC_STORM_GUARDIAN,      &MakeWindhorn<npc_windhorn_storm_guardianAI>);
    RegisterAI(NPC_BLACKWIND_GEOLOGIST,   &MakeWindhorn<npc_blackwind_geologistAI>);
    RegisterAI(NPC_BLACKWIND_EARTHKEEPER, &MakeWindhorn<npc_blackwind_earthkeeperAI>);
    RegisterAI(NPC_DEATHTOTEM_SHAMAN,     &MakeWindhorn<npc_deathtotem_shamanAI>);
    RegisterAI(NPC_PROPHET_STORMHOOF,     &MakeWindhorn<npc_prophet_stormhoofAI>);
    RegisterAI(NPC_DEATHTOTEM_BEHEMOTH,   &MakeWindhorn<npc_deathtotem_behemothAI>);
    RegisterAI(NPC_BLACKWIND_OVERSEER,    &MakeWindhorn<npc_blackwind_overseerAI>);
    RegisterAI(NPC_BLACKWIND_BLOODGUARD,  &MakeWindhorn<npc_blackwind_bloodguardAI>);
    RegisterAI(NPC_AMBASSADOR_VORTALUS,   &MakeWindhorn<npc_ambassador_vortalusAI>);
}
