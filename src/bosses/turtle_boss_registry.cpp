/*
 * mod-turtle-content - binds the ported Turtle WoW boss AIs to their creature
 * entries, plus the Gilneas City rain (Turtle instance_gilneas_city).
 *
 * The binding goes through AllCreatureScript::GetCreatureAI, which the core
 * asks before ScriptName and AIName. So the C++ AIs work whatever the
 * converter writes into creature_template, and TurtleContent.BossScripts = 0
 * hands the creatures back to their SmartAI rows.
 */

#include "turtle_boss_common.h"
#include "Config.h"
#include "Log.h"
#include "Map.h"
#include "MiscPackets.h"
#include "ScriptMgr.h"
#include "Weather.h"
#include <unordered_map>

void AddSC_turtle_stormwrought_ruins();
void AddSC_turtle_gilneas_city();
void AddSC_turtle_dragonmaw_retreat();
void AddSC_turtle_windhorn_canyon();
void AddSC_turtle_zone_northwind();
void AddSC_turtle_frostmane_hollow();
void AddSC_turtle_stormwind_vault();
void AddSC_turtle_spell_values();
void AddSC_turtle_zulfarrak();
void AddSC_turtle_quest_scripts();
void AddSC_turtle_hateforge_quarry();
void AddSC_turtle_moonwhisper_coast();

namespace
{
    std::unordered_map<uint32, TurtleBoss::AIFactory>& Registry()
    {
        static std::unordered_map<uint32, TurtleBoss::AIFactory> registry;
        return registry;
    }

    bool s_bossScriptsEnabled = true;
    bool s_gilneasRainEnabled = true;

    constexpr uint32 MAP_GILNEAS_CITY = 815;
}

void TurtleBoss::RegisterAI(uint32 entry, AIFactory factory)
{
    Registry()[entry] = factory;
}

class mod_turtle_content_boss_config : public WorldScript
{
public:
    mod_turtle_content_boss_config() : WorldScript("mod_turtle_content_boss_config", { WORLDHOOK_ON_AFTER_CONFIG_LOAD }) { }

    void OnAfterConfigLoad(bool /*reload*/) override
    {
        s_bossScriptsEnabled = sConfigMgr->GetOption<bool>("TurtleContent.BossScripts", true);
        s_gilneasRainEnabled = sConfigMgr->GetOption<bool>("TurtleContent.GilneasCityRain", true);
        LOG_INFO("module", ">> mod-turtle-content: boss scripts {} ({} creature AIs)",
            s_bossScriptsEnabled ? "enabled" : "disabled (SmartAI fallback)", Registry().size());
    }
};

class mod_turtle_content_boss_ai : public AllCreatureScript
{
public:
    mod_turtle_content_boss_ai() : AllCreatureScript("mod_turtle_content_boss_ai") { }

    CreatureAI* GetCreatureAI(Creature* creature) const override
    {
        if (!s_bossScriptsEnabled || !creature)
            return nullptr;

        // Pets/charmed creatures keep their own AI.
        if (creature->IsPet() || creature->IsCharmed())
            return nullptr;

        auto itr = Registry().find(creature->GetEntry());
        if (itr == Registry().end())
            return nullptr;

        return itr->second(creature);
    }
};

class mod_turtle_content_gilneas_rain : public PlayerScript
{
public:
    mod_turtle_content_gilneas_rain() : PlayerScript("mod_turtle_content_gilneas_rain", { PLAYERHOOK_ON_UPDATE_ZONE }) { }

    // Turtle instance_gilneas_city::OnPlayerEnter: heavy rain in the zone.
    void OnPlayerUpdateZone(Player* player, uint32 newZone, uint32 /*newArea*/) override
    {
        if (!s_gilneasRainEnabled || !player || player->GetMapId() != MAP_GILNEAS_CITY)
            return;

        Map* map = player->GetMap();
        if (!map || !map->IsDungeon())
            return;

        map->SetZoneWeather(newZone, WEATHER_STATE_HEAVY_RAIN, 0.9999f);
        player->SendDirectMessage(WorldPackets::Misc::Weather(WEATHER_STATE_HEAVY_RAIN, 0.9999f).Write());
    }
};

void AddSC_mod_turtle_content_bosses()
{
    AddSC_turtle_stormwrought_ruins();
    AddSC_turtle_gilneas_city();
    AddSC_turtle_dragonmaw_retreat();
    AddSC_turtle_windhorn_canyon();
    AddSC_turtle_zone_northwind();
    AddSC_turtle_frostmane_hollow();
    AddSC_turtle_stormwind_vault();
    AddSC_turtle_spell_values();
    AddSC_turtle_zulfarrak();
    AddSC_turtle_quest_scripts();
    AddSC_turtle_hateforge_quarry();
    AddSC_turtle_moonwhisper_coast();

    new mod_turtle_content_boss_config();
    new mod_turtle_content_boss_ai();
    new mod_turtle_content_gilneas_rain();
}
