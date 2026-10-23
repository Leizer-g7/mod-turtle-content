"""Read/modify/write client DBC files as Python values.

Table(path, strings={field indexes}, floats={field indexes}) loads a WDBC file; rows are lists of
int / float / str. add() appends or replaces a row by ID, save() writes a new WDBC with a fresh string block.
"""
import struct

LOC = 16          # 3.3.5 localized string: 16 locale columns + 1 flags mask


def loc_fields(start):
    """indexes of a 3.3.5 localized string block starting at `start` (16 strings, mask not included)."""
    return set(range(start, start + LOC))


# string / float field indexes of the 3.3.5 tables the module writes
LAYOUT = {
    'AreaTable': dict(n=36, s=loc_fields(11), f={33, 34}),
    'Map': dict(n=66, s={1} | loc_fields(5) | loc_fields(23) | loc_fields(40), f={58, 60, 61}),
    'LoadingScreens': dict(n=4, s={1, 2}, f=set()),
    'MapDifficulty': dict(n=23, s=loc_fields(3) | {22}, f=set()),
    'AreaTrigger': dict(n=10, s=set(), f=set(range(2, 10))),
    'TaxiNodes': dict(n=24, s=loc_fields(5), f={2, 3, 4}),
    'TaxiPath': dict(n=4, s=set(), f=set()),
    'TaxiPathNode': dict(n=11, s=set(), f={4, 5, 6}),
    'WMOAreaTable': dict(n=28, s=loc_fields(11), f=set()),
    'WorldMapArea': dict(n=11, s={3}, f={4, 5, 6, 7}),
    'WorldMapOverlay': dict(n=17, s={8}, f=set()),
    'Light': dict(n=15, s=set(), f={2, 3, 4, 5, 6}),
    'LightParams': dict(n=9, s=set(), f={4, 5, 6, 7, 8}),
    'LightIntBand': dict(n=34, s=set(), f=set()),
    'LightFloatBand': dict(n=34, s=set(), f=set(range(18, 34))),
    'GameObjectDisplayInfo': dict(n=19, s={1}, f=set(range(12, 18))),
    'Item': dict(n=8, s=set(), f=set()),
    'ZoneMusic': dict(n=8, s={1}, f=set()),
    'Faction': dict(n=57, s=loc_fields(23) | loc_fields(40), f={19, 20}),
    'FactionTemplate': dict(n=14, s=set(), f=set()),
    'GroundEffectTexture': dict(n=11, s=set(), f=set()),     # ID, doodad[4], weight[4], density, terrain type
    'GroundEffectDoodad': dict(n=3, s={1}, f=set()),         # ID, model, flags
}


# Row order. Most stock 3.3.5 tables are sorted by ID, but the client depends on the stock order of these
# (signed ints, field indexes). Written sorted by ID, AreaTrigger.dbc made the client ignore every area trigger
# on every map (no instance portal worked). save() uses this order and checks that the rows the table was loaded
# with keep their original sequence, so a table with some other order is caught before it ships.
ORDER = {
    'AreaTrigger': (1, 0),            # ContinentID, ID
    'MapDifficulty': (1, 2),          # MapID, Difficulty
    'TaxiPathNode': (1, 2),           # PathID, NodeIndex
    'WMOAreaTable': (1, 2, 3),        # WMOID, NameSetID, WMOGroupID (-1 first)
}


# Tables whose stock rows are in no sortable order (Max's GroundEffectTexture.dbc): written in the loaded order, new
# rows at the end.
KEEP_ORDER = {'GroundEffectTexture'}


def _s32(v):
    return v - 0x100000000 if isinstance(v, int) and v >= 0x80000000 else v


def _f(v):
    return struct.unpack('<f', struct.pack('<I', v))[0]


class Table:
    def __init__(self, path, name):
        lay = LAYOUT[name]
        self.name, self.sf, self.ff = name, lay['s'], lay['f']
        b = open(path, 'rb').read()
        magic, n, f, rs, ss = struct.unpack('<4s4I', b[:20])
        assert magic == b'WDBC' and f == lay['n'], f'{path}: {f} fields, expected {lay["n"]}'
        self.nf, self.rs = f, rs
        strs = b[20 + n * rs:20 + n * rs + ss]

        def s(o):
            return strs[o:strs.index(b'\0', o)].decode('utf-8', 'replace') if o else ''
        self.rows = {}
        self.order = []
        for i in range(n):
            raw = struct.unpack_from('<%dI' % f, b, 20 + i * rs)
            row = [s(v) if j in self.sf else (_f(v) if j in self.ff else v) for j, v in enumerate(raw)]
            if row[0] not in self.rows:
                self.order.append(row[0])
            self.rows[row[0]] = row
        self.added = []

    def get(self, i):
        return self.rows.get(i)

    def ids(self):
        return set(self.rows)

    def free_id(self, start, count=1):
        """first id >= start such that start..start+count-1 are all unused"""
        i = start
        res = getattr(self, 'reserved', set())          # ids someone else uses (Max's patch-z rows)
        while any(i + k in self.rows or i + k in res for k in range(count)):
            i += 1
        return i

    def add(self, row, replace=False):
        assert len(row) == self.nf, f'{self.name}: row has {len(row)} fields, expected {self.nf}'
        if row[0] in self.rows and not replace:
            raise ValueError(f'{self.name}: id {row[0]} already exists')
        if row[0] not in self.rows:
            self.order.append(row[0])
        self.rows[row[0]] = list(row)
        self.added.append(row[0])

    def sorted_ids(self):
        if self.name in KEEP_ORDER:
            return list(self.order)
        key = ORDER.get(self.name)
        if key:
            ids = sorted(self.rows, key=lambda i: tuple(_s32(self.rows[i][k]) for k in key))
        else:
            ids = sorted(self.rows)
        loaded = [i for i in self.order if i not in set(self.added)] if self.added else list(self.order)
        keep = set(loaded)
        got = [i for i in ids if i in keep]
        assert got == loaded, f'{self.name}: the stock rows are not in {"ID" if not key else str(key)} order - add the table to dbcw.ORDER'
        return ids

    def save(self, path, sort=True):
        blob = bytearray(b'\0')
        pool = {}

        def ref(x):
            if not x:
                return 0
            if x not in pool:
                pool[x] = len(blob)
                blob.extend(x.encode('utf-8') + b'\0')
            return pool[x]
        ids = self.sorted_ids() if sort else self.order
        out = bytearray()
        for i in ids:
            r = self.rows[i]
            for j, v in enumerate(r):
                if j in self.sf:
                    out += struct.pack('<I', ref(v))
                elif j in self.ff:
                    out += struct.pack('<f', float(v))
                else:
                    out += struct.pack('<I', int(v) & 0xFFFFFFFF)
        with open(path, 'wb') as fh:
            fh.write(struct.pack('<4s4I', b'WDBC', len(ids), self.nf, self.nf * 4, len(blob)))
            fh.write(out)
            fh.write(bytes(blob))
        return path


def loc(text):
    """16 copies of a string (all locales) for a 3.3.5 localized field; the mask goes after it."""
    return [text] * LOC
