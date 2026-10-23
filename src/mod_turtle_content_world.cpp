/*
 * mod-turtle-content - Turtle WoW content for AzerothCore.
 *
 * The content itself is database data in data/sql/db-world, applied by the
 * AzerothCore DB updater. This script only reports what is loaded at startup,
 * so you can see at a glance that the module is active.
 * Zone-specific C++ scripts (dungeon bosses etc.) go in src/zones/.
 */

#include "Config.h"
#include "DatabaseEnv.h"
#include "Log.h"
#include "ScriptMgr.h"

namespace
{
    // Must match "ids.guid_base" in tools/turtle2ac/config.json
    constexpr uint32 TURTLE_GUID_FIRST = 9100001;
    constexpr uint32 TURTLE_GUID_LAST  = 9999999;

    uint64 CountRows(char const* table)
    {
        if (QueryResult result = WorldDatabase.Query("SELECT COUNT(*) FROM `{}` WHERE `guid` BETWEEN {} AND {}", table, TURTLE_GUID_FIRST, TURTLE_GUID_LAST))
            return result->Fetch()[0].Get<uint64>();
        return 0;
    }
}

class mod_turtle_content_world : public WorldScript
{
public:
    mod_turtle_content_world() : WorldScript("mod_turtle_content_world", { WORLDHOOK_ON_STARTUP }) { }

    void OnStartup() override
    {
        if (!sConfigMgr->GetOption<bool>("TurtleContent.Announce", true))
            return;

        uint64 creatures = CountRows("creature");
        uint64 gameobjects = CountRows("gameobject");

        if (!creatures && !gameobjects)
            LOG_WARN("module", ">> mod-turtle-content: no Turtle spawns found - was data/sql/db-world applied to the world database?");
        else
            LOG_INFO("module", ">> mod-turtle-content: {} creatures and {} gameobjects from Turtle WoW are loaded", creatures, gameobjects);
    }
};

void AddSC_mod_turtle_content_world()
{
    new mod_turtle_content_world();
}
