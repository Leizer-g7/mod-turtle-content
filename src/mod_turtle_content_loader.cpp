/*
 * mod-turtle-content - Turtle WoW content for AzerothCore.
 * Script loader. AzerothCore calls Add<module_name>Scripts() for every module.
 */

void AddSC_mod_turtle_content_world();
void AddSC_mod_turtle_content_bosses();

void Addmod_turtle_contentScripts()
{
    AddSC_mod_turtle_content_world();
    AddSC_mod_turtle_content_bosses();
}
