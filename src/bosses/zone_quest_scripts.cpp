/*
 * mod-turtle-content - quest NPC and quest object scripts.
 *
 * Ported from tortoise-wow-main:
 *  - src/scripts/miscellaneous/random_scripts_1.cpp
 *      npc_agne_gambler       Gold-Tooth Gary 60450 (dice gambling)
 *      go_portable_wormhole   Wormhole 1000081 (to Stormwind / Orgrimmar)
 *      go_survival_tent       Tent (Dwarf) 1000457 (rested experience nearby)
 *      npc_vip_invite         Baron Revilgaz 2496: "A present for you Baron." (quest 40180 Making a
 *                             Statement) also makes the player Hated with Booty Bay (-12000, no spillover).
 *  - src/scripts/miscellaneous/random_scripts_3.cpp
 *      npc_garfield_sparkblast  Garfield Sparkblast 60453 / 60496: "I want to join you."
 *                               also sets Bloodsail Buccaneers to neutral.
 *
 * The rest of the quest scripts in those two files are SmartAI rows (see mod_turtle_909_quest_scripts.sql
 * for the fixes made during the audit).
 */

#include "turtle_boss_common.h"
#include "CellImpl.h"
#include "Chat.h"
#include "DBCStores.h"
#include "GameObjectAI.h"
#include "GameTime.h"
#include "GridNotifiersImpl.h"
#include "ReputationMgr.h"
#include "ScriptMgr.h"
#include "ScriptedGossip.h"
#include "SmartAI.h"
#include "World.h"
#include "WorldSession.h"
#include <unordered_map>

using namespace TurtleBoss;

namespace
{
    // ---- Gold-Tooth Gary ---------------------------------------------------
    enum Gambler
    {
        NPC_GOLD_TOOTH_GARY     = 60450,
        NPC_TEXT_GAMBLING       = 9080602,  // Turtle npc_text 80602
        SOUND_COIN              = 1204,
        SPELL_FIREWORK          = 11543,
        GAMBLE_RESET_SECONDS    = 5 * 60,
    };

    struct GamblerInfo
    {
        uint32 betCount = 0;
        uint32 lastBet = 0;
        time_t timestamp = 0;
    };

    std::unordered_map<ObjectGuid, GamblerInfo>& GamblingRecords()
    {
        static std::unordered_map<ObjectGuid, GamblerInfo> records;
        return records;
    }

    // Turtle handleRecords(): a roll over 50 doubles the bet; the third bet in a row of the same amount
    // (within 5 minutes) pays three times the bet on a roll over 75 and nothing otherwise.
    uint32 GambleWinnings(Player* player, uint32 amount, uint32 roll)
    {
        time_t now = GameTime::GetGameTime().count();
        auto& records = GamblingRecords();
        auto itr = records.find(player->GetGUID());
        GamblerInfo info = itr != records.end() ? itr->second : GamblerInfo{ 0, amount, now };

        if (info.lastBet != amount || info.timestamp < now - GAMBLE_RESET_SECONDS)
            info.betCount = 0;
        ++info.betCount;

        uint32 winnings = 0;
        if (info.betCount == 3 && info.lastBet == amount)
        {
            if (roll > 75)
                winnings = amount * 3;
            info.betCount = 0;
        }
        else if (roll > 50)
            winnings = amount * 2;
        else
            info.betCount = 0;

        info.lastBet = amount;
        info.timestamp = now;
        records[player->GetGUID()] = info;
        return winnings;
    }

    uint32 BetForAction(uint32 action)
    {
        switch (action)
        {
            case GOSSIP_ACTION_INFO_DEF + 1: return 100;    // 1 silver
            case GOSSIP_ACTION_INFO_DEF + 2: return 1000;   // 10 silver
            case GOSSIP_ACTION_INFO_DEF + 3: return 5000;   // 50 silver
            case GOSSIP_ACTION_INFO_DEF + 4: return 10000;  // 1 gold
            default:                         return 0;
        }
    }

    class turtle_quest_npcs : public AllCreatureScript
    {
    public:
        turtle_quest_npcs() : AllCreatureScript("mod_turtle_content_quest_npcs") { }

        bool CanCreatureGossipHello(Player* player, Creature* creature) override
        {
            if (creature->GetEntry() != NPC_GOLD_TOOTH_GARY)
                return false;

            ClearGossipMenuFor(player);
            AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, "1 silver coin.", GOSSIP_SENDER_MAIN, GOSSIP_ACTION_INFO_DEF + 1);
            AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, "10 silver coins.", GOSSIP_SENDER_MAIN, GOSSIP_ACTION_INFO_DEF + 2);
            AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, "50 silver coins.", GOSSIP_SENDER_MAIN, GOSSIP_ACTION_INFO_DEF + 3);
            AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, "1 gold coin.", GOSSIP_SENDER_MAIN, GOSSIP_ACTION_INFO_DEF + 4);
            SendGossipMenuFor(player, NPC_TEXT_GAMBLING, creature);
            return true;
        }

        bool CanCreatureGossipSelect(Player* player, Creature* creature, uint32 /*sender*/, uint32 action) override
        {
            if (creature->GetEntry() != NPC_GOLD_TOOTH_GARY)
                return false;

            uint32 bet = BetForAction(action);
            CloseGossipMenuFor(player);
            if (!bet)
                return true;

            if (!player->HasEnoughMoney(bet))
            {
                ChatHandler(player->GetSession()).SendNotification("You don't have enough money!");
                return true;
            }

            player->ModifyMoney(-int32(bet));
            creature->HandleEmoteCommand(EMOTE_ONESHOT_ATTACK1H);
            creature->PlayDirectSound(SOUND_COIN, player);

            uint32 roll = urand(1, 100);
            creature->TextEmote(Acore::StringFormat("{} rolls a dice for {}... {}!", creature->GetName(), player->GetName(), roll));

            uint32 winnings = GambleWinnings(player, bet, roll);
            if (winnings)
            {
                player->ModifyMoney(int32(winnings));
                if (winnings >= bet * 3)
                {
                    creature->TextEmote("STREAK!");
                    player->CastSpell(player, SPELL_FIREWORK, true);
                }
                else
                    player->HandleEmoteCommand(EMOTE_ONESHOT_CHEER);
            }
            else
                player->HandleEmoteCommand(EMOTE_ONESHOT_CRY);
            return true;
        }
    };

    // ---- Garfield Sparkblast -----------------------------------------------
    enum Garfield
    {
        NPC_GARFIELD_A          = 60453,
        NPC_GARFIELD_B          = 60496,
        MENU_GARFIELD           = 9060496,
        OPTION_JOIN_BLOODSAIL   = 0,        // "I want to join you." (quest 40172 Red Flag over the Sea)
        FACTION_BLOODSAIL       = 87,
    };

    struct npc_garfield_sparkblastAI : public SmartAI
    {
        explicit npc_garfield_sparkblastAI(Creature* c) : SmartAI(c) { }

        void sGossipSelect(Player* player, uint32 menuId, uint32 gossipListId) override
        {
            // Turtle sets the Bloodsail Buccaneers standing to 0 (neutral) before the quest credit.
            if (menuId == MENU_GARFIELD && gossipListId == OPTION_JOIN_BLOODSAIL)
                if (FactionEntry const* bloodsail = sFactionStore.LookupEntry(FACTION_BLOODSAIL))
                    player->GetReputationMgr().SetReputation(bloodsail, 0.0f);

            SmartAI::sGossipSelect(player, menuId, gossipListId);
        }
    };

    // ---- Baron Revilgaz ----------------------------------------------------
    enum Revilgaz
    {
        NPC_BARON_REVILGAZ      = 2496,
        MENU_REVILGAZ           = 6685,
        OPTION_PRESENT          = 50,       // "A present for you Baron." (quest 40180, Jolly Roger 60254)
        FACTION_BOOTY_BAY       = 21,
    };

    struct npc_baron_revilgazAI : public SmartAI
    {
        explicit npc_baron_revilgazAI(Creature* c) : SmartAI(c) { }

        void sGossipSelect(Player* player, uint32 menuId, uint32 gossipListId) override
        {
            // Turtle: SetSingleReputation(Booty Bay, -12000) before the quest credit.
            if (menuId == MENU_REVILGAZ && gossipListId == OPTION_PRESENT)
                if (FactionEntry const* bootyBay = sFactionStore.LookupEntry(FACTION_BOOTY_BAY))
                {
                    ReputationMgr& rep = player->GetReputationMgr();
                    if (rep.SetOneFactionReputation(bootyBay, -12000.0f, false))
                        if (FactionState const* state = rep.GetState(bootyBay))
                            rep.SendState(state);
                }

            SmartAI::sGossipSelect(player, menuId, gossipListId);
        }
    };

    // ---- Wormhole and tent -------------------------------------------------
    enum Objects
    {
        GO_PORTABLE_WORMHOLE    = 1000081,
        GO_SURVIVAL_TENT        = 1000457,
    };

    class turtle_quest_objects : public AllGameObjectScript
    {
    public:
        turtle_quest_objects() : AllGameObjectScript("mod_turtle_content_quest_objects") { }

        bool CanGameObjectGossipHello(Player* player, GameObject* go) override
        {
            if (go->GetEntry() != GO_PORTABLE_WORMHOLE)
                return false;

            if (player->IsInCombat() || player->IsBeingTeleported() || !player->IsAlive() || player->isMoving())
                ChatHandler(player->GetSession()).SendSysMessage("The wormhole is currently unstable.");
            else if (player->GetTeamId() == TEAM_ALLIANCE)
                player->TeleportTo(0, -8828.231445f, 627.927490f, 94.055664f, 0.0f);   // Stormwind
            else
                player->TeleportTo(1, 1653.7f, -4416.6f, 16.8f, 0.65f);                  // Orgrimmar
            return true;
        }

        GameObjectAI* GetGameObjectAI(GameObject* go) const override;
    };

    // Turtle go_survival_tent: players within 10 yd gain rested experience while near it.
    // Turtle's tent rate constants are core-side and not in the scripts; this uses the inn rate.
    struct go_survival_tentAI : public GameObjectAI
    {
        explicit go_survival_tentAI(GameObject* go) : GameObjectAI(go) { }

        void UpdateAI(uint32 diff) override
        {
            _timer += diff;
            if (_timer < 1000)
                return;
            uint32 elapsedMs = _timer;
            _timer = 0;

            std::list<Player*> players;
            Acore::AnyPlayerInObjectRangeCheck checker(me, 10.0f);
            Acore::PlayerListSearcher<Acore::AnyPlayerInObjectRangeCheck> searcher(me, players, checker);
            Cell::VisitObjects(me, searcher, 10.0f);
            for (Player* player : players)
            {
                if (!player->IsAlive())
                    continue;
                // Same speed as Player::Update gives an inn: next-level XP / 72000 * 0.125 per second.
                float perSecond = float(player->GetUInt32Value(PLAYER_NEXT_LEVEL_XP)) / 72000.0f
                    * 0.125f * sWorld->getRate(RATE_REST_INGAME);
                player->SetRestBonus(player->GetRestBonus() + perSecond * (elapsedMs / 1000.0f));
            }
        }

    private:
        uint32 _timer = 0;
    };

    GameObjectAI* turtle_quest_objects::GetGameObjectAI(GameObject* go) const
    {
        if (go->GetEntry() == GO_SURVIVAL_TENT)
            return new go_survival_tentAI(go);
        return nullptr;
    }

    template <class AI>
    CreatureAI* MakeQuestAI(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_quest_scripts()
{
    new turtle_quest_npcs();
    new turtle_quest_objects();
    RegisterAI(NPC_GARFIELD_A, &MakeQuestAI<npc_garfield_sparkblastAI>);
    RegisterAI(NPC_GARFIELD_B, &MakeQuestAI<npc_garfield_sparkblastAI>);
    RegisterAI(NPC_BARON_REVILGAZ, &MakeQuestAI<npc_baron_revilgazAI>);
}
