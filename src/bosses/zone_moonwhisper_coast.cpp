/*
 * mod-turtle-content - Moonwhisper Coast: "The Moonhoof Celebration" (42085).
 *
 * Ported from Penqle's tortoise-wow core (commit 10393426, 2026-10-11),
 * src/scripts/world/moonwhisper_coast.cpp, npc_elder_starstrider. It replaces
 * the converter's rebuilt version (which was a guess: the friend's Turtle
 * source did not have this script). With TurtleContent.BossScripts = 0 the
 * converter's SmartAI version runs again.
 *
 * On accepting the quest Elder Starstrider stops being interactive and calls
 * the tribe; eight Moonhoof Celebrators gather on the hill over 15 s (random
 * order and timing); he prepares, the Embodiment of Ancestors appears 8 s
 * later, he channels into it, three celebrators cheer, and the Embodiment
 * speaks its ten lines (Turtle's delays), bows and fades; the celebrators
 * leave one per second and the quest is completed for the player who
 * started it.
 *
 * Turtle-only spell: 51187 Targeted Arcane Channeling (a beam into the
 * Embodiment) -> 23017 Arcane Channeling, the channel Turtle itself uses for
 * Riftmaster Ral'pekta in the same zone, cast while facing the Embodiment.
 *
 * "The Missing Caravans" (41970): Turtle credits it through area triggers
 * 5660/5661, which 3.3.5 uses for other places; the converter's invisible
 * credit NPCs at the three caravans already give the same three credits.
 */

#include "turtle_boss_common.h"
#include "QuestDef.h"
#include "Random.h"
#include <algorithm>

using namespace TurtleBoss;

namespace
{
    enum MoonhoofCelebration
    {
        QUEST_MOONHOOF_CELEBRATION  = 42085,

        NPC_ELDER_STARSTRIDER       = 63083,
        NPC_MOONHOOF_CELEBRATOR     = 63093,
        NPC_EMBODIMENT_OF_ANCESTORS = 63202,

        SPELL_ARCANE_CHANNELING     = 23017,   // stand-in for Turtle 51187

        SUMMON_EVENT_LIFETIME       = 3 * MINUTE * IN_MILLISECONDS,
    };

    Position const CelebratorPositions[] =
    {
        { 8313.31f, -5285.33f, 48.9957f,  5.5832f },
        { 8321.75f, -5288.21f, 48.9053f,  5.2376f },
        { 8314.87f, -5290.64f, 47.8030f,  5.8228f },
        { 8317.51f, -5298.32f, 46.5656f,  5.9995f },
        { 8307.52f, -5302.32f, 47.6486f,  6.2390f },
        { 8311.91f, -5302.39f, 47.3810f,  0.0304f },
        { 8317.24f, -5305.32f, 47.3404f,  0.1404f },
        { 8321.42f, -5309.38f, 47.65074f, 0.7569f },
    };
    constexpr uint8 CELEBRATOR_COUNT = sizeof(CelebratorPositions) / sizeof(CelebratorPositions[0]);

    Position const AncestorPosition = { 8327.3f, -5299.56f, 46.6297f, 2.854f };

    // Turtle broadcast texts 2593100-2593114.
    char const* const TEXT_GATHER_MOONHOOF      = "Gather Moonhoof! We are about to begin!";
    char const* const TEXT_PREPARES_CELEBRATION = "%s prepares for the celebration...";
    char const* const TEXT_CELEBRATOR[3] =
    {
        "Oh blessed ancestors...",
        "The Blue Moon shows its power...",
        "The Prophecy is true!",
    };
    // Line 2 (Turtle 2593107) is a text emote, the others are said.
    char const* const TEXT_ANCESTOR[10] =
    {
        "We have returned, at long last, and on the coming of the Blue Moon...",
        "Long has it been since we gazed upon this sacred land... Such beauty is a sight to behold.",
        "%s begins to shed a tear in longing.",
        "To gaze upon the earth again, a blessing for us, as I am sure our sight is a blessing for you. Heed our words friends, for we have walked this land for generations.",
        "Many things, both natural, and unnatural have come into being, and the Blue Moons return is not a coincidence.",
        "The new neighbors of this land are not here for the benefit of the Moonhoof, but for the benefit of themselves, they bring destruction, they bring something ancient.",
        "The meteor at Starshard Cradle was no accident, for it was not destined to happen.",
        "The future is uncertain, it is clouded in the unknown. These times require vigilance, the hand of great warriors to steer destiny for the better of all.",
        "Be wary our brothers and sisters, be steadfast.",
        "May our blessing grant you the wisdom, and strength to guide us to the next coming.",
    };
    constexpr uint8 ANCESTOR_EMOTE_LINE = 2;
    uint32 const AncestorLineDelays[] = { 10000, 10000, 5000, 15000, 10000, 15000, 10000, 15000, 8000 };
    constexpr uint8 ANCESTOR_DELAY_COUNT = sizeof(AncestorLineDelays) / sizeof(AncestorLineDelays[0]);

    constexpr uint32 PASSIVE_FLAGS = UNIT_FLAG_IMMUNE_TO_PC | UNIT_FLAG_IMMUNE_TO_NPC | UNIT_FLAG_NON_ATTACKABLE_2 | UNIT_FLAG_PACIFIED;

    void MakePassiveAndInvulnerable(Creature* creature)
    {
        creature->SetReactState(REACT_PASSIVE);
        creature->ReplaceAllNpcFlags(UNIT_NPC_FLAG_NONE);
        creature->SetUnitFlag(UnitFlags(PASSIVE_FLAGS));
    }

    struct PendingSpawn
    {
        uint8 positionIndex;
        uint32 timer;
    };

    struct npc_elder_starstriderAI : public ScriptedAI
    {
        explicit npc_elder_starstriderAI(Creature* c) : ScriptedAI(c) { }

        ObjectGuid _playerGuid;
        ObjectGuid _ancestorGuid;
        std::vector<ObjectGuid> _celebrators;
        std::vector<PendingSpawn> _pending;
        uint32 _eventTimer = 0;
        uint32 _originalNpcFlags = 0;
        ReactStates _originalReactState = REACT_AGGRESSIVE;
        uint8 _phase = 0;
        uint8 _spawnIndex = 0;
        uint8 _ancestorLine = 0;
        bool _active = false;
        bool _savedOriginal = false;

        void Reset() override
        {
            if (_active)
                RestoreStarstrider();
            DespawnSummons();
            ClearEvent();
        }

        void ClearEvent()
        {
            _playerGuid.Clear();
            _ancestorGuid.Clear();
            _celebrators.clear();
            _pending.clear();
            _eventTimer = 0;
            _phase = 0;
            _spawnIndex = 0;
            _ancestorLine = 0;
            _active = false;
        }

        void AttackStart(Unit* /*who*/) override { }
        void MoveInLineOfSight(Unit* /*who*/) override { }

        void sQuestAccept(Player* player, Quest const* quest) override
        {
            if (player && quest && quest->GetQuestId() == QUEST_MOONHOOF_CELEBRATION)
                StartEvent(player);
        }

        void StartEvent(Player* player)
        {
            if (_active)
                return;

            _playerGuid = player->GetGUID();
            _originalNpcFlags = me->GetNpcFlags();
            _originalReactState = me->GetReactState();
            _savedOriginal = true;
            _active = true;
            _phase = 1;
            _spawnIndex = 0;

            MakePassiveAndInvulnerable(me);
            Yell(me, TEXT_GATHER_MOONHOOF);

            // Each celebrator at a random moment within 15 s, in time order.
            _pending.clear();
            for (uint8 i = 0; i < CELEBRATOR_COUNT; ++i)
                _pending.push_back({ i, urand(0, 15000) });
            std::sort(_pending.begin(), _pending.end(), [](PendingSpawn const& a, PendingSpawn const& b) { return a.timer < b.timer; });
            uint32 previous = 0;
            for (PendingSpawn& spawn : _pending)
            {
                uint32 const absolute = spawn.timer;
                spawn.timer = absolute - previous;
                previous = absolute;
            }
            _eventTimer = _pending.empty() ? 0 : _pending[0].timer;
        }

        void UpdateAI(uint32 diff) override
        {
            if (!_active)
                return;

            if (_eventTimer > diff)
            {
                _eventTimer -= diff;
                return;
            }

            switch (_phase)
            {
                case 1: SpawnCelebrators(); break;
                case 2: SpawnAncestor(); break;
                case 3: StartChanneling(); break;
                case 4:
                case 5:
                case 6: SayRandomCelebratorLine(); break;
                case 7: SayAncestorLine(); break;
                case 8: BowAncestor(); break;
                case 9: EndAncestor(); break;
                case 10: DespawnNextCelebrator(); break;
                default: FinishEvent(); break;
            }
        }

        void SpawnCelebrators()
        {
            while (_spawnIndex < _pending.size())
            {
                Position const& pos = CelebratorPositions[_pending[_spawnIndex].positionIndex];
                if (Creature* celebrator = me->SummonCreature(NPC_MOONHOOF_CELEBRATOR, pos, TEMPSUMMON_TIMED_DESPAWN, SUMMON_EVENT_LIFETIME))
                {
                    MakePassiveAndInvulnerable(celebrator);
                    _celebrators.push_back(celebrator->GetGUID());
                }

                ++_spawnIndex;
                if (_spawnIndex >= _pending.size() || _pending[_spawnIndex].timer != 0)
                    break;
            }

            if (_spawnIndex >= _pending.size())
            {
                me->TextEmote(TEXT_PREPARES_CELEBRATION);
                _phase = 2;
                _eventTimer = 8000;
                return;
            }

            _eventTimer = _pending[_spawnIndex].timer;
        }

        void SpawnAncestor()
        {
            if (Creature* ancestor = me->SummonCreature(NPC_EMBODIMENT_OF_ANCESTORS, AncestorPosition, TEMPSUMMON_TIMED_DESPAWN, SUMMON_EVENT_LIFETIME))
            {
                MakePassiveAndInvulnerable(ancestor);
                _ancestorGuid = ancestor->GetGUID();
            }
            _phase = 3;
            _eventTimer = 1000;
        }

        void StartChanneling()
        {
            if (Creature* ancestor = GetAncestor())
            {
                me->SetFacingToObject(ancestor);
                me->CastSpell(me, SPELL_ARCANE_CHANNELING, false);
            }
            _phase = 4;
            _eventTimer = 1000;
        }

        void SayRandomCelebratorLine()
        {
            if (Creature* celebrator = GetRandomCelebrator())
                Say(celebrator, TEXT_CELEBRATOR[urand(0, 2)]);
            ++_phase;
            _eventTimer = 1000;
        }

        void SayAncestorLine()
        {
            Creature* ancestor = GetAncestor();
            if (!ancestor)
            {
                FinishEvent();
                return;
            }

            if (_ancestorLine == ANCESTOR_EMOTE_LINE)
                ancestor->TextEmote(TEXT_ANCESTOR[_ancestorLine]);
            else
                Say(ancestor, TEXT_ANCESTOR[_ancestorLine]);

            ++_ancestorLine;

            // First line: 10 s; then Turtle's table; after the last line 8 s to the bow.
            if (_ancestorLine == 1)
                _eventTimer = 10000;
            else if (_ancestorLine - 1 <= ANCESTOR_DELAY_COUNT && _ancestorLine < 10)
                _eventTimer = AncestorLineDelays[_ancestorLine - 1];
            else
            {
                _phase = 8;
                _eventTimer = 8000;
            }
        }

        void BowAncestor()
        {
            if (Creature* ancestor = GetAncestor())
                ancestor->HandleEmoteCommand(EMOTE_ONESHOT_BOW);
            _phase = 9;
            _eventTimer = 10000;
        }

        void EndAncestor()
        {
            if (Creature* ancestor = GetAncestor())
                ancestor->DespawnOrUnsummon();
            _ancestorGuid.Clear();
            me->InterruptNonMeleeSpells(false, SPELL_ARCANE_CHANNELING);

            for (size_t i = 0; i < _celebrators.size(); ++i)
                std::swap(_celebrators[i], _celebrators[urand(uint32(i), uint32(_celebrators.size() - 1))]);

            _phase = 10;
            _eventTimer = 1000;
        }

        void DespawnNextCelebrator()
        {
            while (!_celebrators.empty())
            {
                ObjectGuid guid = _celebrators.back();
                _celebrators.pop_back();
                if (Creature* celebrator = ObjectAccessor::GetCreature(*me, guid))
                {
                    celebrator->DespawnOrUnsummon();
                    _eventTimer = 1000;
                    return;
                }
            }
            FinishEvent();
        }

        void FinishEvent()
        {
            if (Player* player = ObjectAccessor::GetPlayer(*me, _playerGuid))
                if (player->GetQuestStatus(QUEST_MOONHOOF_CELEBRATION) == QUEST_STATUS_INCOMPLETE)
                    player->CompleteQuest(QUEST_MOONHOOF_CELEBRATION);

            RestoreStarstrider();
            DespawnSummons();
            ClearEvent();
        }

        void RestoreStarstrider()
        {
            if (_savedOriginal)
            {
                me->ReplaceAllNpcFlags(NPCFlags(_originalNpcFlags));
                me->SetReactState(_originalReactState);
            }
            me->RemoveUnitFlag(UnitFlags(PASSIVE_FLAGS));
            me->InterruptNonMeleeSpells(false, SPELL_ARCANE_CHANNELING);
        }

        Creature* GetAncestor()
        {
            return _ancestorGuid ? ObjectAccessor::GetCreature(*me, _ancestorGuid) : nullptr;
        }

        Creature* GetRandomCelebrator()
        {
            std::vector<Creature*> alive;
            for (ObjectGuid const& guid : _celebrators)
                if (Creature* celebrator = ObjectAccessor::GetCreature(*me, guid))
                    alive.push_back(celebrator);
            if (alive.empty())
                return nullptr;
            return alive[urand(0, uint32(alive.size() - 1))];
        }

        void DespawnSummons()
        {
            if (Creature* ancestor = GetAncestor())
                ancestor->DespawnOrUnsummon();
            for (ObjectGuid const& guid : _celebrators)
                if (Creature* celebrator = ObjectAccessor::GetCreature(*me, guid))
                    celebrator->DespawnOrUnsummon();
        }
    };

    // The Embodiment is driven by Elder Starstrider: its converted SmartAI
    // (which speaks the lines on its own) must not run as well.
    struct npc_embodiment_of_ancestorsAI : public ScriptedAI
    {
        explicit npc_embodiment_of_ancestorsAI(Creature* c) : ScriptedAI(c) { }
        void AttackStart(Unit* /*who*/) override { }
        void MoveInLineOfSight(Unit* /*who*/) override { }
        void UpdateAI(uint32 /*diff*/) override { }
    };

    CreatureAI* MakeStarstrider(Creature* c) { return new npc_elder_starstriderAI(c); }
    CreatureAI* MakeEmbodiment(Creature* c)  { return new npc_embodiment_of_ancestorsAI(c); }
}

void AddSC_turtle_moonwhisper_coast()
{
    RegisterAI(NPC_ELDER_STARSTRIDER,       &MakeStarstrider);
    RegisterAI(NPC_EMBODIMENT_OF_ANCESTORS, &MakeEmbodiment);
}
