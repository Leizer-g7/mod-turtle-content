#!/usr/bin/env python3
"""mod-turtle-content - rebuild and install the server's map, collision (vmaps) and pathing (mmaps) data
for the Turtle terrain tiles shipped in client/patch-y.mpq.

What it does (nothing in your client or Acore Data is changed until step 5, and step 5 backs up first):
  1. Checks that every model/texture the Turtle tiles use exists in your 3.3.5 client.
  2. Builds an "extraction client" out of hard links to your client's MPQs (no copying, no extra disk space)
     with patch-y added as patch-99.MPQ AND as enUS\\patch-enUS-99.MPQ: vmap4_extractor ranks the enUS locale
     patches above Data\\patch-*, so with patch-99 alone the stock Map.dbc hides the module's maps (818 got no
     vmaps: bosses fell through the floor and could not chase).
  3. Runs vmap4_extractor + vmap4_assembler -> new vmaps.
  4. Runs mmaps_generator for each map with Turtle tiles (map 0: only the Turtle tiles and their neighbours;
     a map the module adds, like 818 Stormwrought Ruins, is built whole).
  5. Backs up and replaces: Acore Data\\maps (the tiles), Acore Data\\vmaps (whole folder), Acore Data\\mmaps (the tiles).

Usage:  python install_server_data.py            (run from this folder, or use install_server_data.bat)
        python install_server_data.py --check    (step 1 only)
Stop the worldserver before step 5; the script asks before it touches Acore Data.
"""
import os, sys, json, shutil, subprocess, time, datetime, re

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# ---------------------------------------------------------------- your folders (edit if they move)
# The first layout whose folders exist is used: the server PC (Desktop\AzerothCore), then the build PC (ScourgeLands).
_HOME = os.path.expanduser('~')
_LAYOUTS = [
    dict(client=os.path.join(_HOME, r"Desktop\world of warcraft 3.3.5a hd\Data"),
         acore=os.path.join(_HOME, r"Desktop\AzerothCore\Server\Data"),
         work=os.path.join(_HOME, r"Desktop\AzerothCore\turtle_server_build")),
    dict(client=r"D:\Games\PC\World of Warcraft\Personal Server\ScourgeLands\Clients\Backup Client\world of warcraft 3.3.5a hd\data",
         acore=r"D:\Games\PC\World of Warcraft\Personal Server\ScourgeLands\Acore Data",
         work=r"D:\Games\PC\World of Warcraft\Personal Server\ScourgeLands\TWoW Data\turtle_server_build"),
]
_L = next((l for l in _LAYOUTS if os.path.isdir(l['client']) and os.path.isdir(l['acore'])), _LAYOUTS[0])
CLIENT_DATA = _L['client']
ACORE_DATA = _L['acore']
WORK = _L['work']
TOOLS_DIR = os.path.join(_HOME, r"Desktop\AzerothCore\Server")          # folder with vmap4_extractor.exe / vmap4_assembler.exe / mmaps_generator.exe; found automatically if empty
PATCH = os.path.join(MODULE, "client", "patch-y.mpq")
PATCH_Z = os.path.join(MODULE, "client", "patch-z.mpq")   # our fixes on top of patch-y (Moonwhisper buildings, Gilneas/Gillijim tiles...)
# ----------------------------------------------------------------

LOG = None


def log(*a):
    msg = ' '.join(str(x) for x in a)
    print(msg, flush=True)
    if LOG:
        LOG.write(msg + '\n')
        LOG.flush()


def die(msg):
    log('\n!! ' + msg)
    if not os.environ.get('TURTLE_INSTALLING'):
        log('Nothing in Acore Data was changed.')
    sys.exit(1)


def files_ci(folder):
    return {f.lower(): f for f in os.listdir(folder)} if os.path.isdir(folder) else {}


def find_tools():
    want = ['vmap4_extractor.exe', 'vmap4_assembler.exe', 'mmaps_generator.exe']
    if TOOLS_DIR and os.path.isdir(TOOLS_DIR):
        return TOOLS_DIR
    found = {}
    skip = {'clients', 'turtlewow eng client 1.18.1', 'acore data', 'twow data', 'databases', '.vs', 'cmakefiles', '.git'}
    for root, dirs, files in os.walk(SCOURGE):
        dirs[:] = [d for d in dirs if d.lower() not in skip]
        low = {f.lower() for f in files}
        if all(w in low for w in want):
            found[root] = max(os.path.getmtime(os.path.join(root, f)) for f in files if f.lower() in want)
    if not found:
        die('Could not find vmap4_extractor.exe, vmap4_assembler.exe and mmaps_generator.exe together under\n   '
            + SCOURGE + '\n   Set TOOLS_DIR at the top of install_server_data.py to the folder that has them (usually next to worldserver.exe).')
    # prefer Release builds, then the newest
    return sorted(found, key=lambda p: ('release' in p.lower(), found[p]))[-1]


def run(exe, args, cwd, name):
    log(f'\n>> {name}: {os.path.basename(exe)} {" ".join(args)}   (in {cwd})')
    out = open(os.path.join(WORK, f'{name}.log'), 'w', errors='replace')
    t0 = time.time()
    p = subprocess.Popen([exe] + args, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    last = t0
    while p.poll() is None:
        time.sleep(2)
        if time.time() - last >= 60:
            last = time.time()
            log(f'   ... still running ({int(last - t0) // 60} min)')
    out.close()
    log(f'   finished in {int(time.time() - t0) // 60} min {int(time.time() - t0) % 60} s, exit code {p.returncode} (output: {name}.log)')
    if p.returncode != 0:
        die(f'{name} failed - see {os.path.join(WORK, name + ".log")}')


def link(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


# ================================================================ 1. asset check
def check_assets():
    from mpqread import MPQ
    log('== 1. Checking the client has every model/texture the Turtle tiles use')
    names = []
    for folder in (CLIENT_DATA, os.path.join(CLIENT_DATA, 'enUS')):
        for low, real in sorted(files_ci(folder).items()):
            if low.endswith('.mpq') and 'speech' not in low:
                names.append(os.path.join(folder, real))
    archives = []
    for n in names:
        try:
            archives.append(MPQ(n))
        except Exception as e:
            log(f'   (could not read {os.path.basename(n)}: {e})')
    req = [l.strip() for l in open(os.path.join(HERE, 'required_assets.txt')) if l.strip()]
    missing = []
    for p in req:
        b, ext = os.path.splitext(p)
        cands = [b + '.m2', p] if ext.lower() in ('.mdx', '.mdl', '.m2') else [p]
        if not any(m.has(c) for m in archives for c in cands):
            missing.append(p)
    log(f'   {len(req) - len(missing)} of {len(req)} found in {len(archives)} archives.')
    with open(os.path.join(WORK, 'missing_assets.txt'), 'w') as fh:
        fh.write('\n'.join(missing) + ('\n' if missing else ''))
    if missing:
        log(f'   {len(missing)} missing (they would be invisible in game) - listed in missing_assets.txt:')
        for p in missing[:20]:
            log('     ' + p)
    return missing


# ================================================================ 2. extraction client
def make_client():
    log('\n== 2. Building the extraction client (hard links, no copies)')
    cdata = os.path.join(WORK, 'client', 'Data')
    if os.path.isdir(os.path.join(WORK, 'client')):
        shutil.rmtree(os.path.join(WORK, 'client'))
    os.makedirs(os.path.join(cdata, 'enUS'))
    top = files_ci(CLIENT_DATA)
    # base archives + numbered patches only: exactly what AzerothCore's extractors read from your client
    keep = re.compile(r'^(common|common-2|expansion|lichking|patch|patch-\d+)\.mpq$')
    for low, real in top.items():
        if keep.match(low):
            link(os.path.join(CLIENT_DATA, real), os.path.join(cdata, real))
    loc_dir = os.path.join(CLIENT_DATA, next((v for k, v in top.items() if k == 'enus'), 'enUS'))
    lkeep = re.compile(r'^(locale-enus|expansion-locale-enus|lichking-locale-enus|patch-enus|patch-enus-\d+)\.mpq$')
    for low, real in files_ci(loc_dir).items():
        if lkeep.match(low):
            link(os.path.join(loc_dir, real), os.path.join(cdata, 'enUS', real))
    # 2026-10-13: patch-z goes on top of patch-y, as in the game client (a later archive wins). Without it the buildings
    # patch-z adds (Moonwhisper Coast) get no collision and the tiles it overrides are extracted from patch-y.
    link(PATCH, os.path.join(cdata, 'patch-98.MPQ'))
    link(PATCH, os.path.join(cdata, 'enUS', 'patch-enUS-98.MPQ'))      # the extractor ranks enUS patches above Data\patch-*
    if os.path.exists(PATCH_Z):
        link(PATCH_Z, os.path.join(cdata, 'patch-99.MPQ'))
        link(PATCH_Z, os.path.join(cdata, 'enUS', 'patch-enUS-99.MPQ'))
    log(f'   {len(os.listdir(cdata)) - 1} archives + {len(os.listdir(os.path.join(cdata, "enUS")))} locale archives, '
        f'patch-y added as patch-98 / enUS\\patch-enUS-98' + (', patch-z as patch-99 / enUS\\patch-enUS-99' if os.path.exists(PATCH_Z) else ' (no client\\patch-z.mpq)'))
    return cdata


# ================================================================ 3. vmaps
def build_vmaps(tools, cdata):
    log('\n== 3. Collision data (vmaps) - this is the long step')
    vdir = os.path.join(WORK, 'vmap')
    if os.path.isdir(vdir):
        shutil.rmtree(vdir)
    os.makedirs(os.path.join(vdir, 'vmaps'))
    run(os.path.join(tools, 'vmap4_extractor.exe'), ['-d', cdata], vdir, 'vmap4_extractor')
    run(os.path.join(tools, 'vmap4_assembler.exe'), ['Buildings', 'vmaps'], vdir, 'vmap4_assembler')
    n = len(os.listdir(os.path.join(vdir, 'vmaps')))
    old = len(os.listdir(os.path.join(ACORE_DATA, 'vmaps')))
    log(f'   new vmaps: {n} files (your current vmaps: {old} files)')
    if n < old * 0.9:
        die('The new vmaps folder is much smaller than the current one - stopping before anything is replaced.')
    return os.path.join(vdir, 'vmaps')


# ================================================================ 4. mmaps
def build_mmaps(tools, new_vmaps):
    log('\n== 4. Pathing data (mmaps) for the Turtle tiles and their neighbours')
    tiles = json.load(open(os.path.join(HERE, 'tiles.json')))
    mdir = os.path.join(WORK, 'mmap')
    if os.path.isdir(mdir):
        shutil.rmtree(mdir)
    for d in ('maps', 'mmaps'):
        os.makedirs(os.path.join(mdir, d))
    ours = set(tiles['maps'])
    for f in os.listdir(os.path.join(ACORE_DATA, 'maps')):
        if f.endswith('.map') and f not in ours:
            link(os.path.join(ACORE_DATA, 'maps', f), os.path.join(mdir, 'maps', f))
    for f in ours:
        shutil.copy2(os.path.join(HERE, 'maps', f), os.path.join(mdir, 'maps', f))
    os.rename(new_vmaps, os.path.join(mdir, 'vmaps'))
    # tiles to rebuild: ours + the 8 around each (their edges include a strip of our terrain)
    redo = set()
    for f in ours:
        mid, ty, tx = f[:3], int(f[3:5]), int(f[5:7])
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                redo.add(f'{mid}{ty + dy:02d}{tx + dx:02d}')
    maps_ids = {f[:3] for f in ours}
    old_mm = os.path.join(ACORE_DATA, 'mmaps')
    for f in os.listdir(old_mm):
        if f[:3] in maps_ids and f.endswith('.mmtile') and f[:7] not in redo:
            link(os.path.join(old_mm, f), os.path.join(mdir, 'mmaps', f))
    cfg_src = os.path.join(tools, 'mmaps-config.yaml')
    cfg = open(cfg_src).read() if os.path.exists(cfg_src) else DEFAULT_MMAPS_CONFIG
    cfg = re.sub(r'(?m)^(\s*dataDir:).*$', r'\1 "./"', cfg)
    open(os.path.join(mdir, 'mmaps-config.yaml'), 'w').write(cfg)
    for mid in sorted(maps_ids):
        run(os.path.join(tools, 'mmaps_generator.exe'), [str(int(mid)), '--threads', str(max(1, (os.cpu_count() or 2) - 1)), '--silent',
                                                         '--config', 'mmaps-config.yaml'], mdir, f'mmaps_generator_{mid}')
    built = sorted(f for f in os.listdir(os.path.join(mdir, 'mmaps')) if f[:7] in redo or f.endswith('.mmap'))
    log(f'   rebuilt {len([b for b in built if b.endswith(".mmtile")])} tiles')
    return mdir, built, redo


# ================================================================ 5. install
def install(mdir, built, redo):
    tiles = json.load(open(os.path.join(HERE, 'tiles.json')))
    log('\n== 5. Install into ' + ACORE_DATA)
    log('   Stop the worldserver now if it is running.')
    if input('   Type YES to back up and replace the server data: ').strip().upper() != 'YES':
        log('   Skipped. Everything is ready in ' + WORK + ' - run the script again to install.')
        return
    os.environ['TURTLE_INSTALLING'] = '1'
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bk = os.path.join(ACORE_DATA, f'backup_before_turtle_{stamp}')
    os.makedirs(os.path.join(bk, 'maps'))
    os.makedirs(os.path.join(bk, 'mmaps'))
    for f in tiles['maps']:
        src = os.path.join(ACORE_DATA, 'maps', f)
        if os.path.exists(src):
            shutil.move(src, os.path.join(bk, 'maps', f))
        shutil.copy2(os.path.join(HERE, 'maps', f), src)
    os.rename(os.path.join(ACORE_DATA, 'vmaps'), os.path.join(bk, 'vmaps'))
    os.rename(os.path.join(mdir, 'vmaps'), os.path.join(ACORE_DATA, 'vmaps'))
    for f in built:
        dst = os.path.join(ACORE_DATA, 'mmaps', f)
        if os.path.exists(dst):
            shutil.move(dst, os.path.join(bk, 'mmaps', f))
        shutil.copy2(os.path.join(mdir, 'mmaps', f), dst)
    with open(os.path.join(bk, 'RESTORE.bat'), 'w') as fh:
        fh.write('@echo off\r\nrem Puts back the server data from before mod-turtle-content terrain was installed.\r\n'
                 f'cd /d "{bk}"\r\n'
                 f'rmdir /s /q "{os.path.join(ACORE_DATA, "vmaps")}"\r\n'
                 f'move "{os.path.join(bk, "vmaps")}" "{os.path.join(ACORE_DATA, "vmaps")}"\r\n'
                 f'copy /y "{os.path.join(bk, "maps")}\\*" "{os.path.join(ACORE_DATA, "maps")}\\"\r\n'
                 f'copy /y "{os.path.join(bk, "mmaps")}\\*" "{os.path.join(ACORE_DATA, "mmaps")}\\"\r\n'
                 + ''.join(f'del "{os.path.join(ACORE_DATA, "mmaps", f)}"\r\n' for f in built
                           if not os.path.exists(os.path.join(bk, 'mmaps', f)))
                 + 'echo Restored.\r\npause\r\n')
    log(f'   Installed: {len(tiles["maps"])} map tiles, new vmaps, {len(built)} mmaps files.')
    log(f'   Backup + RESTORE.bat: {bk}')
    log(f'   The work folder ({WORK}) can be deleted once you have tested in game.')


DEFAULT_MMAPS_CONFIG = """mmapsConfig:
  skipLiquid: false
  skipContinents: false
  skipJunkMaps: true
  skipBattlegrounds: false
  dataDir: "./"
  meshSettings:
    walkableSlopeAngle: 60
    walkableHeight: 6
    walkableClimb: 4
    walkableRadius: 2
    verticesPerMapEdge: 2000
    verticesPerTileEdge: 80
    maxSimplificationError: 0.8
  debugOutput: false
"""


def main():
    global LOG
    os.makedirs(WORK, exist_ok=True)
    LOG = open(os.path.join(WORK, 'install_server_data.log'), 'a', errors='replace')
    log(f'\n===== mod-turtle-content server data  {datetime.datetime.now():%Y-%m-%d %H:%M}')
    log(f'client: {CLIENT_DATA}\nserver data: {ACORE_DATA}\nwork folder: {WORK}')
    for p, what in ((CLIENT_DATA, '3.3.5 client Data folder'), (ACORE_DATA, 'server Data folder (dbc, maps, vmaps, mmaps)'), (PATCH, 'client/patch-y.mpq')):
        if not os.path.exists(p):
            die(f'{what} not found: {p}\n   Edit the paths at the top of install_server_data.py.')
    missing = check_assets()
    if '--check' in sys.argv:
        return
    if missing:
        log('   (continuing - missing files only affect what is drawn, not the server data)')
    tools = find_tools()
    log(f'\nAzerothCore tools: {tools}')
    if os.path.splitdrive(WORK)[0].lower() != os.path.splitdrive(CLIENT_DATA)[0].lower():
        log('   note: work folder and client are on different drives, so MPQs will be copied instead of linked (needs ~15 GB).')
    cdata = make_client()
    new_vmaps = build_vmaps(tools, cdata)
    mdir, built, redo = build_mmaps(tools, new_vmaps)
    install(mdir, built, redo)
    log('\nDone. Start the worldserver.')


if __name__ == '__main__':
    try:
        main()
    finally:
        if sys.stdin and sys.stdin.isatty():
            input('\nPress Enter to close ...')
