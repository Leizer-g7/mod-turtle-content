"""Terrain helpers: zone/subzone lookup from Turtle server maps and ground height from
both Turtle (vmangos .map) and AzerothCore (.map) server map files."""
import os, struct

GRID = 533.3333333


class MapSet:
    """A folder of server .map tiles. kind='tw' (vmangos, header 40 bytes) or 'ac' (AzerothCore, header 44 bytes)."""

    def __init__(self, folder, kind):
        self.folder = folder
        self.kind = kind
        self.area_off = 8 if kind == 'tw' else 12
        self.height_off = 16 if kind == 'tw' else 20
        self._c = {}
        self.missing = set()

    def tile(self, m, gx, gy):
        k = (m, gx, gy)
        if k in self._c:
            return self._c[k]
        fn = os.path.join(self.folder, '%03d%02d%02d.map' % k)
        if not os.path.exists(fn):
            self.missing.add('%03d%02d%02d.map' % k)
            self._c[k] = None
            return None
        b = open(fn, 'rb').read()
        ao, asz = struct.unpack('<II', b[self.area_off:self.area_off + 8])
        a = b[ao:ao + asz]
        _, aflags, garea = struct.unpack('<4sHH', a[:8])
        area = [garea] * 256 if aflags & 1 else list(struct.unpack('<256H', a[8:520]))
        ho, hs = struct.unpack('<II', b[self.height_off:self.height_off + 8])
        h = b[ho:ho + hs]
        _, hflags, gh, gmax = struct.unpack('<4sIff', h[:16])
        if hflags & 1:
            v9 = None
        elif hflags & 2:
            mult = (gmax - gh) / 65535
            v9 = [gh + x * mult for x in struct.unpack('<%dH' % (129 * 129), h[16:16 + 2 * 129 * 129])]
        elif hflags & 4:
            mult = (gmax - gh) / 255
            v9 = [gh + x * mult for x in h[16:16 + 129 * 129]]
        else:
            v9 = list(struct.unpack('<%df' % (129 * 129), h[16:16 + 4 * 129 * 129]))
        self._c[k] = (area, gh, v9)
        return self._c[k]

    def _pos(self, x, y):
        fx = 32 - x / GRID
        fy = 32 - y / GRID
        return fx, fy, int(fx), int(fy)

    def area_value(self, m, x, y):
        fx, fy, gx, gy = self._pos(x, y)
        t = self.tile(m, gx, gy)
        if t is None:
            return None
        return t[0][(int(fx * 16) & 15) * 16 + (int(fy * 16) & 15)]

    def height(self, m, x, y):
        fx, fy, gx, gy = self._pos(x, y)
        t = self.tile(m, gx, gy)
        if t is None:
            return None
        _, gh, v9 = t
        if v9 is None:
            return gh
        lx = (fx - gx) * 128
        ly = (fy - gy) * 128
        ix, iy = int(lx), int(ly)
        dx, dy = lx - ix, ly - iy
        V = lambda i, j: v9[min(i, 128) * 129 + min(j, 128)]
        return (V(ix, iy) * (1 - dx) * (1 - dy) + V(ix + 1, iy) * dx * (1 - dy) +
                V(ix, iy + 1) * (1 - dx) * dy + V(ix + 1, iy + 1) * dx * dy)


class ZoneLookup:
    """Turtle .map files store the AreaTable *AreaBit* per cell; translate to (zone, area)."""

    def __init__(self, twmaps, tw_areatable_rows):
        self.maps = twmaps
        self.by_bit = {}
        for r in tw_areatable_rows:   # vanilla layout: 0 id, 1 map, 2 parent, 3 areabit
            self.by_bit[(r[1], r[3])] = r

    def zone_of(self, m, x, y):
        b = self.maps.area_value(m, x, y)
        if b is None:
            return None, None
        r = self.by_bit.get((m, b))
        if not r:
            return None, None
        return (r[0] if r[2] == 0 else r[2]), r[0]


class AdtAreas:
    """Zone/subzone lookup from the area id each map chunk carries in Turtle's client tiles (33-yard cells).
    Used where Turtle's server maps disagree with its own terrain (zone borders Turtle moved, e.g. Northwind
    against Elwynn). Positions on tiles Turtle did not change fall back to the server maps."""

    def __init__(self, folder, map_dirs, tw_areatable_rows, fallback):
        self.folder = folder
        self.map_dirs = map_dirs
        self.parent = {r[0]: r[2] for r in tw_areatable_rows}
        self.fallback = fallback
        self._c = {}

    def _tile(self, m, X, Y):
        k = (m, X, Y)
        if k not in self._c:
            d = self.map_dirs.get(m)
            fn = os.path.join(self.folder, 'World', 'Maps', d, f'{d}_{X}_{Y}.adt') if d else None
            if not fn or not os.path.exists(fn):
                self._c[k] = None
            else:
                b = open(fn, 'rb').read()
                ofs = [struct.unpack_from('<I', b, 92 + i * 16)[0] for i in range(256)]
                self._c[k] = [struct.unpack_from('<I', b, o + 8 + 0x34)[0] for o in ofs]
        return self._c[k]

    def area(self, m, x, y):
        px, pz = 32 * GRID - y, 32 * GRID - x
        X, Y = int(px // GRID), int(pz // GRID)
        t = self._tile(m, X, Y)
        if t is None:
            return None
        cx = min(15, int((px - X * GRID) // (GRID / 16)))
        cy = min(15, int((pz - Y * GRID) // (GRID / 16)))
        return t[cy * 16 + cx]

    def zone_of(self, m, x, y):
        a = self.area(m, x, y)
        if not a or a not in self.parent:
            return self.fallback.zone_of(m, x, y)
        return (self.parent[a] or a), a


class Client335Areas:
    """Zone/subzone from the area id each chunk carries in the 3.3.5 client tile (`tile_path(m, X, Y)` gives the
    file, or None). Used behind AdtAreas for a 3.3.5 zone Turtle only touched in places (Stranglethorn): where
    Turtle did not change a tile, Turtle's ground and areas are the vanilla ones, which 3.3.5 keeps, while
    Turtle's server maps miss parts of the zone. Positions outside the 3.3.5 tiles fall back to `fallback`."""

    def __init__(self, tile_path, ac_areatable_rows, fallback):
        self.tile_path = tile_path
        self.parent = {r[0]: r[2] for r in ac_areatable_rows}
        self.fallback = fallback
        self._c = {}

    def area(self, m, x, y):
        px, pz = 32 * GRID - y, 32 * GRID - x
        X, Y = int(px // GRID), int(pz // GRID)
        k = (m, X, Y)
        if k not in self._c:
            fn = self.tile_path(m, X, Y)
            if not fn or not os.path.exists(fn):
                self._c[k] = None
            else:
                b = open(fn, 'rb').read()
                ofs = [struct.unpack_from('<I', b, 92 + i * 16)[0] for i in range(256)]
                self._c[k] = [struct.unpack_from('<I', b, o + 8 + 0x34)[0] for o in ofs]
        t = self._c[k]
        if t is None:
            return None
        cx = min(15, int((px - X * GRID) // (GRID / 16)))
        cy = min(15, int((pz - Y * GRID) // (GRID / 16)))
        return t[cy * 16 + cx]

    def zone_of(self, m, x, y):
        a = self.area(m, x, y)
        if not a or a not in self.parent:
            return self.fallback.zone_of(m, x, y)
        return (self.parent[a] or a), a


def read_tw_grid(folder, m, X, Y):
    """Full height and liquid grid of one Turtle (vmangos) server .map tile, for ADT tile X_Y of map m (file 0mmYYXX.map).
    -> None or dict(v9=[129*129], v8=[128*128], liq_flags=[256] per chunk (0 = no liquid), liquid(r, c) -> level at
    outer vertex r, c (0..128) or None). Index: v9[r * 129 + c], r along the ADT chunk rows, c along the columns."""
    fn = os.path.join(folder, '%03d%02d%02d.map' % (m, Y, X))
    if not os.path.exists(fn):
        return None
    d = open(fn, 'rb').read()
    ho, hs, lo, ls = struct.unpack_from('<4I', d, 16)
    _, hf, gh, gmax = struct.unpack_from('<4sIff', d, ho)
    p = ho + 16
    if hf & 1:
        v9, v8 = [gh] * 16641, [gh] * 16384
    elif hf & 2:
        k = (gmax - gh) / 65535
        v9 = [gh + x * k for x in struct.unpack_from('<16641H', d, p)]
        v8 = [gh + x * k for x in struct.unpack_from('<16384H', d, p + 2 * 16641)]
    elif hf & 4:
        k = (gmax - gh) / 255
        v9 = [gh + x * k for x in d[p:p + 16641]]
        v8 = [gh + x * k for x in d[p + 16641:p + 16641 + 16384]]
    else:
        v9 = list(struct.unpack_from('<16641f', d, p))
        v8 = list(struct.unpack_from('<16384f', d, p + 4 * 16641))
    out = dict(v9=v9, v8=v8, liq_flags=[0] * 256, liquid=lambda r, c: None)
    if lo:
        _, lf, lt, ox, oy, w, h, lvl = struct.unpack_from('<4sHHBBBBf', d, lo)
        p = lo + 16
        if lf & 1:                       # no per-chunk type: one type everywhere
            out['liq_flags'] = [lt] * 256
        else:
            out['liq_flags'] = list(d[p + 512:p + 768])
            p += 768
        if lf & 2:                       # no height grid: one level
            out['liquid'] = lambda r, c: lvl
        else:
            hts = struct.unpack_from('<%df' % (w * h), d, p)
            out['liquid'] = lambda r, c: hts[(r - oy) * w + (c - ox)] if 0 <= r - oy < h and 0 <= c - ox < w else None
    return out
