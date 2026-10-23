#!/usr/bin/env python3
"""mod-turtle-content - check a 3.3.5 client against the client patch (read-only, changes nothing).

    python check_client.py "<client Data folder>"

The patch (patch-y.mpq) replaces whole client tables (Map, AreaTrigger, Light, LoadingScreens ...) and files.
Each one was built from the copy in the client the build was given (client_tables.json). This script finds:

  ERROR  an archive that loads AFTER patch-y and carries one of its files: that file from patch-y is ignored by
         the client. (Today the hand-made world-map patch-z replaces WorldMapOverlay.dbc; expected until the
         converter makes the world-map work itself.)
  WARN   a table or file whose copy in this client differs from the one the patch was built from (another HD
         or custom patch): the patch hides that patch's rows. Send this client's tables (client335_extract.py)
         and rebuild.

Load order (tested): Data\\patch-<x> > Data\\enUS\\patch-enUS-<x> > patch-enUS > patch > base archives;
within a group alphabetical (digits first, case ignored), last wins.
"""
import os, sys, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'server-data'))
from mpqread import MPQ


def rank(a):
    folder_enus = '\\' in a
    n = os.path.splitext(a.split('\\')[-1])[0].lower()
    if n.startswith('patch-enus-') or (n.startswith('patch-') and len(n) == 7):
        suf = n.split('-')[-1]
        return (4 if not folder_enus and not n.startswith('patch-enus') else 3, (0 if suf.isdigit() else 1, suf))
    if n == 'patch-enus':
        return (2, (0, ''))
    if n == 'patch':
        return (1, (0, ''))
    return (0, (0, ''))


def main():
    man = json.load(open(os.path.join(HERE, 'client_tables.json')))
    data = sys.argv[1] if len(sys.argv) > 1 else input('3.3.5 client Data folder: ').strip().strip('"')
    archives = []
    for folder, prefix in [(data, '')] + [(os.path.join(data, d), 'enUS\\') for d in os.listdir(data)
                                          if d.lower() == 'enus' and os.path.isdir(os.path.join(data, d))]:
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith('.mpq') and 'speech' not in f.lower():
                archives.append((prefix + f, os.path.join(folder, f)))
    me = (man['patch'], None)
    mine = [a for a in archives if a[0].lower() == man['patch'].lower()]
    print('client:', data)
    print('patch :', mine[0][1] if mine else f"{man['patch']} NOT FOUND in the Data folder")
    my_rank = rank(man['patch'])
    above = [a for a in archives if rank(a[0]) > my_rank]
    below = sorted([a for a in archives if rank(a[0]) <= my_rank and a[0].lower() != man['patch'].lower()], key=lambda a: rank(a[0]))
    errors, warns = [], []
    want = {f.lower(): f for f in man['files']}
    for name, path in above:
        try:
            m = MPQ(path)
        except Exception as e:
            warns.append(f'could not open {name}: {e}')
            continue
        hit = [want[k] for k in want if m.has(want[k])]
        if hit:
            errors.append(f'{name} loads after {man["patch"]} and replaces {len(hit)} of its files ({", ".join(hit[:5])}): '
                          f'the client uses {name}\'s copies. Expected only for the hand-made world-map patch-z (WorldMapOverlay.dbc).')
    opened = {}
    def eff(path_in_mpq):
        for name, p in reversed(below):
            if name not in opened:
                try:
                    opened[name] = MPQ(p)
                except Exception:
                    opened[name] = None
            m = opened[name]
            if m and m.has(path_in_mpq):
                return name, hashlib.md5(m.read(path_in_mpq)).hexdigest()
        return None, None
    checks = [(f'DBFilesClient\\{t}.dbc', v) for t, v in man['tables'].items()] + list(man.get('based_on', {}).items())
    for key, v in checks:
        a, h = eff(key)
        if h != v['md5']:
            warns.append(f"{key}: this client loads it from {a or 'nowhere'}, the patch was built on the copy in {v['archive']} - "
                         f"the patch hides this client's version. Run client335_extract.py on this client and rebuild.")
    for e in errors:
        print('ERROR', e)
    for w in warns:
        print('WARN ', w)
    if not errors and not warns:
        print(f"OK - {len(checks)} client tables/files match what the patch was built on, nothing overrides it.")
    return 1 if errors or warns else 0


if __name__ == '__main__':
    rc = main()
    if os.name == 'nt' and len(sys.argv) < 2:
        input('press Enter')
    sys.exit(rc)
