#!/usr/bin/env python3
"""mod-turtle-content - rebuild the pathing data (mmaps) of whole maps whose buildings the module changed.

install_server_data.py rebuilds the vmaps of every map (the module's buildings are in them) but the mmaps only of maps
with Turtle terrain tiles. A dungeon made of one building (the Deadmines, map 36) has no terrain tiles, so after
Turtle's extended Deadmines building is installed its old mmaps do not cover the new rooms: creatures there would
not chase or walk home. This script rebuilds such maps' mmaps from the installed maps + vmaps.

Run it AFTER install_server_data.bat, with the worldserver stopped:
    python rebuild_mmaps_map.py            (map 36, the Deadmines)
    python rebuild_mmaps_map.py 36 209     (several maps)
It uses install_server_data.py (next to this file) for your folders and the AzerothCore tools, asks before it
changes anything, and backs up the map's old mmaps files first (RESTORE.bat in the backup folder).
"""
import os, sys, shutil, datetime, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import install_server_data as isd            # your installer: folders (ACORE_DATA, WORK), find_tools, run, link, log

MAPS = [int(a) for a in sys.argv[1:] if a.isdigit()] or [36]


def main():
    os.makedirs(isd.WORK, exist_ok=True)
    isd.LOG = open(os.path.join(isd.WORK, 'rebuild_mmaps_map.log'), 'a', errors='replace')
    log = isd.log
    log(f'\n===== mod-turtle-content: rebuild mmaps of map(s) {MAPS}  {datetime.datetime.now():%Y-%m-%d %H:%M}')
    acore = isd.ACORE_DATA
    for d in ('maps', 'vmaps', 'mmaps'):
        if not os.path.isdir(os.path.join(acore, d)):
            isd.die(f'{os.path.join(acore, d)} not found')
    tools = isd.find_tools()
    log(f'AzerothCore tools: {tools}\nserver data: {acore}')
    work = os.path.join(isd.WORK, 'mmap_maps')
    if os.path.isdir(work):
        shutil.rmtree(work)
    for d in ('maps', 'vmaps', 'mmaps'):
        os.makedirs(os.path.join(work, d))
    log('   linking the installed maps and vmaps (hard links, no copies) ...')
    for d in ('maps', 'vmaps'):
        for f in os.listdir(os.path.join(acore, d)):
            src = os.path.join(acore, d, f)
            if os.path.isfile(src):
                isd.link(src, os.path.join(work, d, f))
    cfg_src = os.path.join(tools, 'mmaps-config.yaml')
    cfg = open(cfg_src).read() if os.path.exists(cfg_src) else isd.DEFAULT_MMAPS_CONFIG
    cfg = re.sub(r'(?m)^(\s*dataDir:).*$', r'\1 "./"', cfg)
    open(os.path.join(work, 'mmaps-config.yaml'), 'w').write(cfg)
    for mid in MAPS:
        isd.run(os.path.join(tools, 'mmaps_generator.exe'), [str(mid), '--threads', str(max(1, (os.cpu_count() or 2) - 1)), '--silent',
                                                             '--config', 'mmaps-config.yaml'], work, f'mmaps_generator_{mid:03d}')
    built = sorted(f for f in os.listdir(os.path.join(work, 'mmaps')) if f[:3] in {f'{m:03d}' for m in MAPS})
    if not built:
        isd.die('mmaps_generator wrote no files - see its log in ' + isd.WORK)
    log(f'   built {len(built)} files: {", ".join(built[:12])}{" ..." if len(built) > 12 else ""}')
    log('\n   Stop the worldserver now if it is running.')
    if input('   Type YES to back up and replace these mmaps files: ').strip().upper() != 'YES':
        log('   Skipped. The new files are in ' + os.path.join(work, 'mmaps'))
        return
    os.environ['TURTLE_INSTALLING'] = '1'
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bk = os.path.join(acore, f'backup_before_turtle_mmaps_{stamp}')
    os.makedirs(os.path.join(bk, 'mmaps'))
    old = [f for f in os.listdir(os.path.join(acore, 'mmaps')) if f[:3] in {f'{m:03d}' for m in MAPS}]
    for f in old:
        shutil.move(os.path.join(acore, 'mmaps', f), os.path.join(bk, 'mmaps', f))
    for f in built:
        shutil.copy2(os.path.join(work, 'mmaps', f), os.path.join(acore, 'mmaps', f))
    with open(os.path.join(bk, 'RESTORE.bat'), 'w') as fh:
        fh.write('@echo off\r\nrem Puts back the mmaps from before rebuild_mmaps_map.py.\r\n'
                 + ''.join(f'del "{os.path.join(acore, "mmaps", f)}"\r\n' for f in built)
                 + f'copy /y "{os.path.join(bk, "mmaps")}\\*" "{os.path.join(acore, "mmaps")}\\"\r\n'
                 + 'echo Restored.\r\npause\r\n')
    log(f'   Installed {len(built)} mmaps files (old ones: {bk}).\nDone. Start the worldserver.')


if __name__ == '__main__':
    try:
        main()
    finally:
        if sys.stdin and sys.stdin.isatty():
            input('\nPress Enter to close ...')
