"""Turtle client files a set of map tiles needs (buildings, textures), from the extractor's output folder.

Only files that came from a Turtle patch are shipped (the extractor's manifest 'copied' list); everything
else is original game data that a 3.3.5 client already has. Turtle models (.m2/.mdx) are never shipped:
they are in the 1.12 format, which the 3.3.5 client cannot read. References to them are rewritten to a
3.3.5 stand-in (config m2_substitutions) or left pointing at a missing file (the client then skips them).
"""
import os, json, struct
from lib import wmo as wmolib
from lib.adt import top_chunks


def norm(p):
    return p.replace('/', '\\').strip('\\').strip()


class TurtleAssets:
    def __init__(self, folder, m2_subs, never_ship=()):
        self.folder = folder
        self.never = {norm(x).lower() for x in never_ship}   # stock-named files that must not replace the client's
        self.not_shipped = set()
        man = json.load(open(os.path.join(folder, 'manifest.json')))
        self.turtle = {k.lower(): k for k in man['copied']}
        self.vanilla = {k.lower() for k in man['vanilla_only']}
        self.local = {}
        for d, _, fs in os.walk(folder):
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), folder).replace('/', '\\')
                if rel.lower().startswith('_deep\\'):
                    rel = rel[6:].replace('#', '\\')   # flat copies of files nested too deep to fetch (turtle_extract.py)
                self.local.setdefault(rel.lower(), os.path.join(d, f))
        self.subs = {k.lower(): v for k, v in m2_subs.items() if not k.startswith('_')}
        self.changed = {}          # old model path -> new path (report)
        self.missing = set()       # Turtle files referenced but not in the extract folder
        self.liquid_fixed = 0      # WMO groups whose liquid type was corrected (lib/wmo.py fix_group_liquid)
        self.unchecked_groups = set()   # groups of a liquid-flagged Turtle root that come from the 3.3.5 client

    def is_turtle(self, p):
        return norm(p).lower() in self.turtle

    def read(self, p):
        lp = self.local.get(norm(p).lower())
        return open(lp, 'rb').read() if lp else None

    def model_sub(self, name):
        """doodad path -> path to write in the tile/WMO"""
        stem = os.path.splitext(norm(name).lower())[0]
        if stem in self.subs:
            self.changed[name] = self.subs[stem]
            return self.subs[stem]
        return name

    def closure(self, tiles, extra=(), textures=(), wmos=()):
        """tiles: list of ADT bytes; textures / wmos: further names (from tiles merged with 3.3.5 ones).
        -> {archive path: bytes or local path} of the Turtle files to ship."""
        out = {}
        wmos = set(wmos)

        def want(p):
            k = norm(p).lower()
            if not k or k not in self.turtle or k.endswith(('.m2', '.mdx', '.mdl', '.skin')):
                return False
            if k in self.never:                  # config never_ship: the client's own file stays
                self.not_shipped.add(self.turtle[k])
                return True
            if '\\expansion01\\' in k or '\\expansion02\\' in k:
                return False                     # Burning Crusade / Wrath files: the 3.3.5 client has its own
            if k in self.local:
                out.setdefault(self.turtle[k], self.local[k])
            else:
                self.missing.add(self.turtle[k])
            return True
        for n in textures:
            want(n)
        for data in tiles:
            for t, o, s in top_chunks(data):
                names = [x.decode('latin-1') for x in data[o:o + s].split(b'\0') if x]
                if t == 'MTEX':
                    for n in names:
                        want(n)
                elif t == 'MWMO':
                    wmos |= set(names)
        for e in extra:                          # asked for by name (loading screens): must be a Turtle file
            if not want(e):
                self.missing.add(e)
        for w in sorted(wmos, key=str.lower):
            k = norm(w).lower()
            if k in self.never and k in self.turtle:
                # never_ship building (a TBC/Wrath building Turtle copied that the 3.3.5 client has at the same path):
                # the client's own root and groups are used
                self.not_shipped.add(self.turtle[k])
                continue
            if k not in self.turtle or k not in self.local:
                if k in self.turtle:
                    self.missing.add(w)
                continue
            data = open(self.local[k], 'rb').read()
            new, _ = wmolib.substitute_models(data, self.model_sub)
            out[self.turtle[k]] = new
            ng = 0
            for t, p, s in wmolib.chunks(data):
                body = data[p + 8:p + 8 + s]
                if t == 'MOHD':
                    ng = struct.unpack_from('<I', body, 4)[0]
                elif t == 'MOTX':
                    for n in body.split(b'\0'):
                        if n:
                            want(n.decode('latin-1'))
            stem = os.path.splitext(self.turtle[k])[0]
            rflags = wmolib.root_flags(data)
            for g in range(ng):
                gp = f'{stem}_{g:03d}.wmo'
                if not want(gp):                 # groups Turtle did not change are original game files
                    if rflags & wmolib.MOHD_LIQUID_DBC:
                        self.unchecked_groups.add(gp)
                    continue
                gk = self.turtle[norm(gp).lower()]
                if gk in out:
                    gd, ch_ = wmolib.fix_group_liquid(rflags, open(out[gk], 'rb').read() if isinstance(out[gk], str) else out[gk])
                    if ch_:
                        out[gk] = gd
                        self.liquid_fixed += 1
        return out
