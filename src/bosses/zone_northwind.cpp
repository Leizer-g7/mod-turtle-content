/*
 * mod-turtle-content - Northwind zone NPC scripts (20-30 bracket).
 *
 * Ported from tortoise-wow-main:
 *  - src/scripts/miscellaneous/random_scripts_1.cpp  'rented_mount'
 *    (White Stallion 51560, Palomino 51561: hire a horse for 50 copper).
 *  - sql gossip_scripts 6229802 / 6229803 (Cutpurse Warren 62298,
 *    quest 41636 "Who Will Think Of The Children": pay 20 silver for the
 *    crate, or fight him). The converter kept the gossip menu and its
 *    conditions but not the two scripts.
 *
 * Turtle's rental spells 40700-40710 (5 min mount, +40% speed) are other
 * spells in 3.3.5; the matching 3.3.5 mount spells carry them, tuned to
 * Turtle's duration and speed. Rentable: the two Northwind horses, the
 * riding rams and kodos, the riding wolves and the skeletal horses (their
 * NPCs are only spawned once their zones are ported). Turtle's White
 * Thalassian Unicorn (40045) has no 3.3.5 mount and is left alone.
 *
 * Quest 41666 (Amberglaze Donuts) points at complete script 416660, which
 * does not exist in Turtle's own database either: nothing to port.
 */

#include "turtle_boss_common.h"
#include "Chat.h"
#include "ScriptMgr.h"
#include "ScriptedGossip.h"
#include "SmartAI.h"
#include "WorldSession.h"

using namespace TurtleBoss;

namespace
{
    // ---- Rented mounts ---------------------------------------------------
    enum RentedMount
    {
        RENT_PRICE_COPPER       = 50,
        RENT_DURATION_MS        = 5 * MINUTE * IN_MILLISECONDS,
        RENT_SPEED_PCT          = 40,
    };

    // Turtle rented_mount: entry -> 3.3.5 mount spell carrying the Turtle rental spell, gossip texts.
    struct RentalMount
    {
        uint32 entry;
        uint32 spell;
        char const* option;
        uint32 npcText;
    };

    RentalMount const RentalMounts[] =
    {
        { 51560, 16083, "Hire this horse for 50 copper.", 90365 },  // White Stallion  (Turtle 40701)
        { 51561, 16082, "Hire this horse for 50 copper.", 90365 },  // Palomino        (Turtle 40700)
        {  4779,  6899, "Hire this ram for 50 copper.",   90381 },  // Brown Riding Ram (Turtle 40707)
        {  4710,  6777, "Hire this ram for 50 copper.",   90381 },  // Gray Riding Ram  (Turtle 40708)
        { 12354, 18990, "Hire this kodo for 50 copper.",  90382 },  // Brown Riding Kodo (Turtle 40709)
        { 12355, 18989, "Hire this kodo for 50 copper.",  90382 },  // Gray Riding Kodo  (Turtle 40710)
        { 51580,  6653, "Hire this wolf for 50 copper.",  90368 },  // Dire Riding Wolf     (Turtle 40702)
        { 51581,   580, "Hire this wolf for 50 copper.",  90368 },  // Timber Riding Wolf   (Turtle 40703)
        { 51588, 17462, "Hire this horse for 50 copper.", 90369 },  // Red Skeletal Horse   (Turtle 40704)
        { 51589, 17463, "Hire this horse for 50 copper.", 90369 },  // Blue Skeletal Horse  (Turtle 40705)
        { 51587, 17464, "Hire this horse for 50 copper.", 90369 },  // Brown Skeletal Horse (Turtle 40706)
    };

    RentalMount const* RentalFor(uint32 entry)
    {
        for (RentalMount const& rental : RentalMounts)
            if (rental.entry == entry)
                return &rental;
        return nullptr;
    }

    // ---- Cutpurse Warren -------------------------------------------------
    enum CutpurseWarren
    {
        NPC_CUTPURSE_WARREN     = 62298,
        MENU_WARREN_CHOICE      = 6229802,
        OPTION_PAY              = 0,       // "Take it and get out of Northwind! <Pay 20 Silver.>"
        OPTION_FIGHT            = 1,       // "As if! Today you'll draw your last breath!"
        WARREN_PRICE_COPPER     = 2000,    // gossip_menu_option BoxMoney; the core takes it
        ITEM_CRATE_OF_BOOKS     = 1041606, // Turtle item 41606 (Crate of Donated Books)
        FACTION_HOSTILE         = 14,
    };

    class turtle_zone_gossip : public AllCreatureScript
    {
    public:
        turtle_zone_gossip() : AllCreatureScript("mod_turtle_content_zone_gossip") { }

        bool CanCreatureGossipHello(Player* player, Creature* creature) override
        {
            RentalMount const* rental = RentalFor(creature->GetEntry());
            if (!rental)
                return false;

            // Turtle: nothing to offer while already mounted.
            if (player->IsMounted())
                return false;

            ClearGossipMenuFor(player);
            AddGossipItemFor(player, GOSSIP_ICON_CHAT, rental->option, GOSSIP_SENDER_MAIN, GOSSIP_ACTION_INFO_DEF + 1);
            SendGossipMenuFor(player, rental->npcText, creature);
            return true;
        }

        bool CanCreatureGossipSelect(Player* player, Creature* creature, uint32 /*sender*/, uint32 action) override
        {
            RentalMount const* rental = RentalFor(creature->GetEntry());
            if (!rental)
                return false;
            uint32 spellId = rental->spell;

            if (action == GOSSIP_ACTION_INFO_DEF + 1 && !player->IsMounted())
            {
                if (player->HasEnoughMoney(uint32(RENT_PRICE_COPPER)))
                {
                    player->CastSpell(player, spellId, TRIGGERED_FULL_MASK);
                    if (Aura* aura = player->GetAura(spellId, player->GetGUID()))
                        TuneAura(aura, RENT_DURATION_MS, KEEP_AMOUNT, RENT_SPEED_PCT);
                    player->ModifyMoney(-int32(RENT_PRICE_COPPER));
                }
                else
                    ChatHandler(player->GetSession()).SendNotification("You don't have enough money!");
            }

            CloseGossipMenuFor(player);
            return true;
        }
    };

    struct npc_cutpurse_warrenAI : public SmartAI
    {
        explicit npc_cutpurse_warrenAI(Creature* c) : SmartAI(c) { }

        void sGossipSelect(Player* player, uint32 menuId, uint32 gossipListId) override
        {
            if (menuId != MENU_WARREN_CHOICE)
            {
                SmartAI::sGossipSelect(player, menuId, gossipListId);
                return;
            }

            if (gossipListId == OPTION_PAY)
            {
                // The option's BoxMoney (2000) makes the core ask, check and take the 20 silver
                // right after this hook; only hand over the crate when the player can pay.
                if (player->HasEnoughMoney(uint32(WARREN_PRICE_COPPER)))
                    player->AddItem(ITEM_CRATE_OF_BOOKS, 1);
            }
            else if (gossipListId == OPTION_FIGHT)
            {
                me->SetFaction(FACTION_HOSTILE);
                AttackStart(player);
            }
            CloseGossipMenuFor(player);
        }

        void EnterEvadeMode(EvadeReason why) override
        {
            me->RestoreFaction();
            SmartAI::EnterEvadeMode(why);
        }

        void JustRespawned() override
        {
            me->RestoreFaction();
            SmartAI::JustRespawned();
        }
    };

    template <class AI>
    CreatureAI* MakeNorthwind(Creature* creature) { return new AI(creature); }
}

void AddSC_turtle_zone_northwind()
{
    new turtle_zone_gossip();
    RegisterAI(NPC_CUTPURSE_WARREN, &MakeNorthwind<npc_cutpurse_warrenAI>);
}
