"""Merge two 3.3.5-layout ADTs of the same tile chunk by chunk.

Used where a Turtle zone shares a map tile with live 3.3.5 content (Northwind against Stormwind City, the harbor,
Searing Gorge, Burning Steppes ...): the tile is the 3.3.5 one, and only the chunks that belong to the Turtle zone
come from Turtle's tile.

    t = Tile(bytes)                       # parse
    out = merge(base, donor, take)        # take = set of chunk indices (0..255) that come from donor
    stitch(...)                           # make chunk borders between the two sources meet exactly

Per chunk the terrain (heights, normals, texture layers + alpha, shadows, vertex colours, legacy liquid) and the
MH2O water come from the chosen source. Texture / model / WMO name lists are merged; doodads and WMOs are kept
from each source by where they stand:
  - a donor doodad/WMO is kept when its origin lies in a donor chunk;
  - a base doodad is dropped when its origin lies in a donor chunk; a base WMO is dropped only when its whole
    bounding box lies in donor chunks (big city WMOs are never lost).
Every chunk references (MCRF) the kept objects that either source tile referenced for that chunk.
"""
import struct

TILE = 1600.0 / 3.0            # 533.333
CHUNK = TILE / 16.0
HALF = 32 * TILE               # 17066.666


def _chunks(d, start, end):
    p = start
    while p + 8 <= end:
        t = d[p:p + 4][::-1].decode('latin-1')
        s = struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, s
        p += 8 + s


def _names(blob):
    out, p = [], 0
    while p < len(blob):
        e = blob.find(b'\0', p)
        if e < 0:
            e = len(blob)
        if e > p:
            out.append((p, blob[p:e].decode('latin-1')))
        p = e + 1
    return out


MCNK_OFS_FIELDS = {0x14: 'MCVT', 0x18: 'MCNR', 0x1C: 'MCLY', 0x20: 'MCRF', 0x24: 'MCAL', 0x2C: 'MCSH', 0x58: 'MCSE', 0x60: 'MCLQ',
                   0x74: 'MCCV', 0x78: 'MCLV'}


class Tile:
    def __init__(self, data):
        d = bytes(data)
        assert d[0:4] == b'REVM' and d[12:16] == b'RDHM', 'not an ADT'
        self.mhdr = list(struct.unpack_from('<16I', d, 20))
        top = {}
        for t, p, s in _chunks(d, 0, len(d)):
            if t == 'MCNK':
                continue
            top.setdefault(t, d[p + 8:p + 8 + s])
        mcin = top['MCIN']
        self.mcnk = []
        for i in range(256):
            o, s = struct.unpack_from('<II', mcin, i * 16)
            assert d[o:o + 4] == b'KNCM', f'chunk {i}: no MCNK at {o}'
            s = struct.unpack_from('<I', d, o + 4)[0]
            self.mcnk.append(bytes(d[o + 8:o + 8 + s]))
        self.mtex = [n for _, n in _names(top.get('MTEX', b''))]
        mmdx = dict(_names(top.get('MMDX', b'')))
        self.models = [mmdx[o] for o in struct.unpack('<%dI' % (len(top.get('MMID', b'')) // 4), top.get('MMID', b''))]
        mwmo = dict(_names(top.get('MWMO', b'')))
        self.wmos = [mwmo[o] for o in struct.unpack('<%dI' % (len(top.get('MWID', b'')) // 4), top.get('MWID', b''))]
        md = top.get('MDDF', b'')
        self.mddf = [bytearray(md[i:i + 36]) for i in range(0, len(md), 36)]
        mo = top.get('MODF', b'')
        self.modf = [bytearray(mo[i:i + 64]) for i in range(0, len(mo), 64)]
        self.mfbo = top.get('MFBO')
        self.mtxf = top.get('MTXF')
        self.water = self._water(d)

    def _water(self, d):
        """MH2O -> per chunk: (attributes bytes or None, [(instance 24 bytes, bitmap bytes, vertex bytes)])"""
        out = [None] * 256
        if not self.mhdr[10] or struct.unpack_from('<I', d, 20 + self.mhdr[10] + 4)[0] < 256 * 12:
            return out
        base = 20 + self.mhdr[10] + 8
        for i in range(256):
            oi, lc, oa = struct.unpack_from('<III', d, base + i * 12)
            if not lc:
                continue
            insts = []
            for k in range(lc):
                raw = bytes(d[base + oi + k * 24:base + oi + k * 24 + 24])
                lt, lvf, mn, mx, x, y, w, h, ob, ov = struct.unpack('<HHffBBBBII', raw)
                n = (w + 1) * (h + 1)
                vsz = {0: n * 5, 1: n * 8, 2: n, 3: n * 9}.get(lvf, 0)
                bm = bytes(d[base + ob:base + ob + (w * h + 7) // 8]) if ob else b''
                vx = bytes(d[base + ov:base + ov + vsz]) if ov else b''
                insts.append((raw, bm, vx))
            attr = bytes(d[base + oa:base + oa + 16]) if oa else None
            out[i] = (attr, insts)
        return out

    # chunk geometry --------------------------------------------------------------------------------
    def chunk_pos(self, i):
        return struct.unpack_from('<3f', self.mcnk[i], 0x68)

    def area(self, i):
        return struct.unpack_from('<I', self.mcnk[i], 0x34)[0]

    def heights(self, i):
        c = self.mcnk[i]
        o = struct.unpack_from('<I', c, 0x14)[0] - 8          # offsets count from the MCNK tag
        base = struct.unpack_from('<f', c, 0x68 + 8)[0]
        return [base + v for v in struct.unpack_from('<145f', c, o + 8)]


def moved_tile(data, X, Y):
    """A copy of a stock open-sea ADT placed at Azeroth_X_Y: only the chunk positions change (the sea tiles of one
    continent are otherwise the same file). Used as the base where 3.3.5 has no tile at all. The tile must hold no
    doodads or WMOs (their positions are absolute)."""
    d = bytearray(data)
    t = Tile(bytes(d))
    assert not t.mddf and not t.modf, 'ocean base tile holds objects'
    p = 0
    while p + 8 <= len(d):
        if bytes(d[p:p + 4]) == b'NICM':
            mcin = p + 8
            break
        p += 8 + struct.unpack_from('<I', d, p + 4)[0]
    for k in range(256):
        o = struct.unpack_from('<I', d, mcin + k * 16)[0]
        struct.pack_into('<ff', d, o + 8 + 0x68, HALF - Y * TILE - (k // 16) * CHUNK, HALF - X * TILE - (k % 16) * CHUNK)
    return bytes(d)


def chunk_of(tile_xy, px, pz):
    """placement position (ADT space x, z) -> chunk index inside tile tile_xy=(X, Y) of Azeroth_X_Y, or None"""
    tx, ty = tile_xy
    cx = int((px - tx * TILE) // CHUNK)
    cy = int((pz - ty * TILE) // CHUNK)
    if 0 <= cx < 16 and 0 <= cy < 16:
        return cy * 16 + cx
    return None


def _wmo_chunks(tile_xy, rec):
    lo = struct.unpack_from('<3f', rec, 32)          # extents: lower corner, upper corner (ADT placement space)
    hi = struct.unpack_from('<3f', rec, 44)
    tx, ty = tile_xy
    out = set()
    x0, x1 = sorted((lo[0], hi[0]))
    z0, z1 = sorted((lo[2], hi[2]))
    for cy in range(16):
        for cx in range(16):
            ax0, az0 = tx * TILE + cx * CHUNK, ty * TILE + cy * CHUNK
            if x0 <= ax0 + CHUNK and x1 >= ax0 and z0 <= az0 + CHUNK and z1 >= az0:
                out.add(cy * 16 + cx)
    return out


def _mcnk_rebuild(c, mcly_tex=None, mcrf=None):
    """MCNK body with MCLY texture ids remapped and MCRF replaced (offsets fixed). c = MCNK data without its 8-byte header."""
    hdr = bytearray(c[:128])
    offs = {}
    for f in MCNK_OFS_FIELDS:
        v = struct.unpack_from('<I', hdr, f)[0]
        if v and v - 8 < len(c):
            offs[f] = v - 8
    starts = sorted(set(offs.values()) | {len(c)})
    segs = {}
    for k, s in enumerate(starts[:-1]):
        segs[s] = bytearray(c[s:starts[k + 1]])
    # MCLY texture ids
    if mcly_tex is not None and 0x1C in offs:
        sg = segs[offs[0x1C]]
        n = struct.unpack_from('<I', sg, 4)[0] // 16
        for k in range(n):
            t = struct.unpack_from('<I', sg, 8 + k * 16)[0]
            struct.pack_into('<I', sg, 8 + k * 16, mcly_tex[t])
    # MCRF
    if mcrf is not None:
        dd, ww = mcrf
        body = struct.pack('<%dI' % (len(dd) + len(ww)), *(dd + ww))
        new = bytearray(b'FRCM' + struct.pack('<I', len(body)) + body)
        if 0x20 in offs:
            old = segs[offs[0x20]]
            osz = struct.unpack_from('<I', old, 4)[0]
            new += old[8 + osz:]                               # keep any padding that followed
            segs[offs[0x20]] = new
        struct.pack_into('<I', hdr, 0x10, len(dd))
        struct.pack_into('<I', hdr, 0x38, len(ww))
    # re-lay segments in their original order
    out = bytearray(hdr) + bytearray(c[128:starts[0]] if starts[0] > 128 else b'')
    newpos = {}
    for s in starts[:-1]:
        newpos[s] = len(out)
        out += segs[s]
    for f, s in offs.items():
        struct.pack_into('<I', out, f, newpos[s] + 8)
    if 0x24 in offs:                                           # sizeAlpha follows MCAL
        pass
    return bytes(out)


def merge(base, donor, take, tile_xy, donor_owns=None, drop_removed_wmos=False, drop_uids=()):
    """base, donor: Tile. take: set of chunk indices from donor. tile_xy: (X, Y) of Azeroth_X_Y. -> ADT bytes
    donor_owns(px, pz) -> bool says whether a placement position (in any tile) lies in a donor chunk; it decides
    which objects are kept when their origin is in a neighbouring tile. Default: only this tile's chunks.
    drop_removed_wmos: a 3.3.5 building whose origin is in a taken chunk and that the donor tile no longer has
    (Turtle removed or replaced it: the Wetlands' Grim Batol) is dropped even if its footprint reaches 3.3.5 chunks.
    drop_uids: placements (doodads or WMOs) with these unique ids are left out (a 3.3.5 building in the way of Turtle land)."""
    take = set(take)
    drop_uids = set(drop_uids)
    if donor_owns is None:
        donor_owns = lambda px, pz: chunk_of(tile_xy, px, pz) in take
    # texture list: base first, then donor names not in it
    mtex = list(base.mtex)
    low = {n.lower(): i for i, n in enumerate(mtex)}
    dtex = []
    for n in donor.mtex:
        if n.lower() not in low:
            low[n.lower()] = len(mtex)
            mtex.append(n)
        dtex.append(low[n.lower()])
    mtxf = None
    if base.mtxf is not None or donor.mtxf is not None:
        bf = list(struct.unpack('<%dI' % (len(base.mtxf or b'') // 4), base.mtxf or b''))
        df = list(struct.unpack('<%dI' % (len(donor.mtxf or b'') // 4), donor.mtxf or b''))
        fl = bf + [0] * (len(mtex) - len(bf))
        for i, j in enumerate(dtex):
            if j >= len(base.mtex) and i < len(df):
                fl[j] = df[i]
        mtxf = struct.pack('<%dI' % len(fl), *fl)

    # placements
    def keep_base_doodad(r):
        x, y, z = struct.unpack_from('<3f', r, 8)
        return not donor_owns(x, z)

    def keep_base_wmo(r):
        lo, hi = struct.unpack_from('<3f', r, 32), struct.unpack_from('<3f', r, 44)
        x0, x1 = sorted((lo[0], hi[0]))
        z0, z1 = sorted((lo[2], hi[2]))
        n = 8                                                  # sample the footprint on a grid
        pts = [(x0 + (x1 - x0) * a / n, z0 + (z1 - z0) * b / n) for a in range(n + 1) for b in range(n + 1)]
        if drop_removed_wmos:
            ox, oy, oz = struct.unpack_from('<3f', r, 8)
            nm = base.wmos[struct.unpack_from('<I', r, 0)[0]].lower()
            if donor_owns(ox, oz) and not any(
                    donor.wmos[struct.unpack_from('<I', d, 0)[0]].lower() == nm and
                    abs(struct.unpack_from('<f', d, 8)[0] - ox) < 3 and abs(struct.unpack_from('<f', d, 16)[0] - oz) < 3
                    for d in donor.modf):
                return False
        return not all(donor_owns(px, pz) for px, pz in pts)

    def keep_donor(r):
        x, y, z = struct.unpack_from('<3f', r, 8)
        return donor_owns(x, z)

    models, mlow = [], {}

    def model_idx(n):
        if n.lower() not in mlow:
            mlow[n.lower()] = len(models)
            models.append(n)
        return mlow[n.lower()]
    wmos, wlow = [], {}

    def wmo_idx(n):
        if n.lower() not in wlow:
            wlow[n.lower()] = len(wmos)
            wmos.append(n)
        return wlow[n.lower()]
    mddf, modf = [], []
    bmap_d, dmap_d, bmap_w, dmap_w = {}, {}, {}, {}
    seen_uid = set()
    for src, recs, keep, mp, names in ((base, base.mddf, keep_base_doodad, bmap_d, base.models),
                                       (donor, donor.mddf, keep_donor, dmap_d, donor.models)):
        for i, r in enumerate(recs):
            if keep(r) and struct.unpack_from('<I', r, 4)[0] not in drop_uids:
                uid = struct.unpack_from('<I', r, 4)[0]
                nr = bytearray(r)
                struct.pack_into('<I', nr, 0, model_idx(names[struct.unpack_from('<I', r, 0)[0]]))
                mp[i] = len(mddf)
                mddf.append(bytes(nr))
    for src, recs, keep, mp, names in ((base, base.modf, keep_base_wmo, bmap_w, base.wmos),
                                       (donor, donor.modf, keep_donor, dmap_w, donor.wmos)):
        for i, r in enumerate(recs):
            if keep(r) and struct.unpack_from('<I', r, 4)[0] not in drop_uids:
                uid = struct.unpack_from('<I', r, 4)[0]
                if uid in seen_uid:                               # same WMO placed by both tiles: keep one
                    mp[i] = next(k for k, x in enumerate(modf) if struct.unpack_from('<I', x, 4)[0] == uid)
                    continue
                seen_uid.add(uid)
                nr = bytearray(r)
                struct.pack_into('<I', nr, 0, wmo_idx(names[struct.unpack_from('<I', r, 0)[0]]))
                mp[i] = len(modf)
                modf.append(bytes(nr))

    def refs(t, i):
        c = t.mcnk[i]
        o = struct.unpack_from('<I', c, 0x20)[0]
        nd, nw = struct.unpack_from('<I', c, 0x10)[0], struct.unpack_from('<I', c, 0x38)[0]
        if not o or not (nd + nw):
            return [], []
        v = struct.unpack_from('<%dI' % (nd + nw), c, o - 8 + 8)
        return list(v[:nd]), list(v[nd:])

    chunks = []
    water = []
    for i in range(256):
        bd, bw = refs(base, i)
        dd, dw = refs(donor, i)
        nd = sorted({bmap_d[k] for k in bd if k in bmap_d} | {dmap_d[k] for k in dd if k in dmap_d})
        nw = sorted({bmap_w[k] for k in bw if k in bmap_w} | {dmap_w[k] for k in dw if k in dmap_w})
        if i in take:
            chunks.append(_mcnk_rebuild(donor.mcnk[i], mcly_tex=dtex, mcrf=(nd, nw)))
            water.append(donor.water[i])
        else:
            chunks.append(_mcnk_rebuild(base.mcnk[i], mcly_tex=None, mcrf=(nd, nw)))
            water.append(base.water[i])

    mfbo = base.mfbo
    if base.mfbo and donor.mfbo:
        a = struct.unpack('<18h', base.mfbo)
        b = struct.unpack('<18h', donor.mfbo)
        mfbo = struct.pack('<18h', *([max(x, y) for x, y in zip(a[:9], b[:9])] + [min(x, y) for x, y in zip(a[9:], b[9:])]))
    elif donor.mfbo and not base.mfbo:
        mfbo = donor.mfbo
    return _write(mtex, models, wmos, mddf, modf, water, chunks, mfbo, mtxf, base.mhdr[0] | (1 if mfbo else 0))


def rewrite(data, tile_xy, drop_uids=(), tex_sub=None):
    """a finished tile written again through merge() (every offset, MCRF, MHDR and MCIN rebuilt): placements with the
    given unique ids dropped, MTEX names replaced (tex_sub: lower-case name -> new name)"""
    t = Tile(data)
    if tex_sub:
        t.mtex = [tex_sub.get(n.lower(), n) for n in t.mtex]
    return merge(t, t, set(), tile_xy, drop_uids=drop_uids)


def _cell_ground(hs, cx, cy):
    return (hs[cy * 17 + cx] + hs[cy * 17 + cx + 1] + hs[(cy + 1) * 17 + cx] + hs[(cy + 1) * 17 + cx + 1]) / 4


def fix_dark_water(t, base=None, limit=-60.0):
    """Turtle water marked "deep" (MH2O attributes deep mask, legacy MCLQ cell flag 0x80) right off the beach: AzerothCore's
    map_extractor turns it into dark water and players get the Fatigue bar a few yards from the shore. The mark is kept only
    on cells whose ground is below `limit` (open sea); water without an attributes block (read as deep everywhere) gets one.
    Chunks whose water is the 3.3.5 tile's own (base) are left alone.
    Mutates t; -> number of cells cleared."""
    n = 0
    for i in range(256):
        hs = t.heights(i)
        w = t.water[i]
        if w and w[1] and not (base is not None and base.water[i] == w):
            # no attributes block: AzerothCore's extractor reads that as deep everywhere
            attr_ = w[0] if w[0] else struct.pack('<QQ', 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF)
            dm = struct.unpack_from('<Q', attr_, 8)[0]
            keep = 0
            for cy in range(8):
                for cx in range(8):
                    b = 1 << (cy * 8 + cx)
                    if dm & b:
                        if _cell_ground(hs, cx, cy) < limit:
                            keep |= b
                        else:
                            n += 1
            if keep != dm:
                t.water[i] = (attr_[:8] + struct.pack('<Q', keep) + attr_[16:], w[1])
        c = t.mcnk[i]
        o, sz = struct.unpack_from('<II', c, 0x60)
        if o and sz > 8 and c[o - 8:o - 4] == b'QLCM':
            fo = o - 8 + 8 + 8 + 81 * 8
            if base is not None:
                bc = base.mcnk[i]
                bo, bsz = struct.unpack_from('<II', bc, 0x60)
                if bo and bsz == sz and bc[bo - 8:bo - 8 + sz] == c[o - 8:o - 8 + sz]:
                    continue
            cb = bytearray(c)
            for cy in range(8):
                for cx in range(8):
                    f = cb[fo + cy * 8 + cx]
                    if f != 0x0F and f & 0x80 and _cell_ground(hs, cx, cy) >= limit:
                        cb[fo + cy * 8 + cx] = f & 0x7F
                        n += 1
            t.mcnk[i] = bytes(cb)
    return n


def _blob(names):
    out, offs = bytearray(), []
    for n in names:
        offs.append(len(out))
        out += n.encode('latin-1') + b'\0'
    return bytes(out), offs


def _water_blob(water):
    if not any(water):
        return None
    hdr = bytearray(256 * 12)
    body = bytearray()
    base = 256 * 12
    for i, w in enumerate(water):
        if not w:
            continue
        attr, insts = w
        oi = base + len(body)
        inst_area = bytearray(24 * len(insts))
        body += inst_area
        oa = 0
        if attr:
            oa = base + len(body)
            body += attr
        for k, (raw, bm, vx) in enumerate(insts):
            lt, lvf, mn, mx, x, y, w_, h, ob, ov = struct.unpack('<HHffBBBBII', raw)
            nob = nov = 0
            if bm:
                nob = base + len(body)
                body += bm
            if vx:
                nov = base + len(body)
                body += vx
            struct.pack_into('<HHffBBBBII', body, oi - base + k * 24, lt, lvf, mn, mx, x, y, w_, h, nob, nov)
        struct.pack_into('<III', hdr, i * 12, oi, len(insts), oa)
    return bytes(hdr + body)


def _write(mtex, models, wmos, mddf, modf, water, chunks, mfbo, mtxf, mhdr_flags):
    def ch(tag, data):
        return tag[::-1].encode() + struct.pack('<I', len(data)) + data
    mtex_b, _ = _blob(mtex)
    mmdx_b, mmid = _blob(models)
    mwmo_b, mwid = _blob(wmos)
    parts = [('MTEX', mtex_b), ('MMDX', mmdx_b), ('MMID', struct.pack('<%dI' % len(mmid), *mmid)),
             ('MWMO', mwmo_b), ('MWID', struct.pack('<%dI' % len(mwid), *mwid)),
             ('MDDF', b''.join(mddf)), ('MODF', b''.join(modf))]
    wb = _water_blob(water)
    out = bytearray(ch('MVER', struct.pack('<I', 18)))
    mhdr_pos = len(out)
    out += ch('MHDR', bytes(64))
    mcin_pos = len(out)
    out += ch('MCIN', bytes(256 * 16))
    ofs = {}
    for tag, data in parts:
        ofs[tag] = len(out) - (mhdr_pos + 8)
        out += ch(tag, data)
    if wb:
        ofs['MH2O'] = len(out) - (mhdr_pos + 8)
        out += ch('MH2O', wb)
    mcin = bytearray(256 * 16)
    for i, c in enumerate(chunks):
        struct.pack_into('<IIII', mcin, i * 16, len(out), len(c) + 8, 0, 0)
        out += ch('MCNK', c)
    if mfbo:
        ofs['MFBO'] = len(out) - (mhdr_pos + 8)
        out += ch('MFBO', mfbo)
    if mtxf:
        ofs['MTXF'] = len(out) - (mhdr_pos + 8)
        out += ch('MTXF', mtxf)
    out[mcin_pos + 8:mcin_pos + 8 + len(mcin)] = mcin
    mh = [0] * 16
    mh[0] = mhdr_flags
    mh[1] = mcin_pos - (mhdr_pos + 8)
    for k, tag in ((2, 'MTEX'), (3, 'MMDX'), (4, 'MMID'), (5, 'MWMO'), (6, 'MWID'), (7, 'MDDF'), (8, 'MODF'), (9, 'MFBO'), (10, 'MH2O'), (11, 'MTXF')):
        mh[k] = ofs.get(tag, 0)
    struct.pack_into('<16I', out, mhdr_pos + 8, *mh)
    return bytes(out)


def set_outer_heights(t, i, values):
    """values: {(row, col): absolute height} for outer vertices (row, col in 0..8) of chunk i of Tile t."""
    c = bytearray(t.mcnk[i])
    o = struct.unpack_from('<I', c, 0x14)[0] - 8 + 8
    base = struct.unpack_from('<f', c, 0x68 + 8)[0]
    for (r, k), h in values.items():
        struct.pack_into('<f', c, o + (r * 17 + k) * 4, h - base)
    t.mcnk[i] = bytes(c)


def stitch(sources, taken, log=None, onto='base'):
    """Make shared outer vertices identical where a donor chunk meets a base chunk (inside a tile or across tiles).
    sources: {(X, Y): (base Tile, donor Tile or None)}; taken: {(X, Y): set of chunk ids}. Tiles missing from
    sources are ignored. onto='base': the donor side is moved onto the base side (3.3.5 ground with live spawns
    stays exactly where it was). onto='donor': the base side is moved onto the donor (Turtle land on empty 3.3.5
    sea: the Turtle ground keeps its shape and the 3.3.5 sea floor rises to meet it).
    -> (vertices moved, largest move); stitch.base_tiles_edited lists the base tiles changed (onto='donor')"""
    owner = {}

    def src(tx, ty, cx, cy):                    # (Tile, chunk id, is_donor) for a chunk in global chunk coords
        X, Y = tx, ty
        if (X, Y) not in sources:
            return None
        b, d = sources[(X, Y)]
        i = cy * 16 + cx
        if d is not None and i in taken.get((X, Y), ()):
            return d, i, True
        return b, i, False
    moved, worst = 0, 0.0
    edits, base_edits = {}, {}
    for (X, Y), (b, d) in sources.items():
        if d is None:
            continue
        for i in taken.get((X, Y), ()):
            cy, cx = divmod(i, 16)
            h = d.heights(i)
            gx0, gy0 = X * 16 + cx, Y * 16 + cy
            for r in range(9):
                for k in range(9):
                    if 0 < r < 8 and 0 < k < 8:
                        continue
                    # chunks sharing this vertex: offsets in chunk units
                    nb = []
                    for dx in ((-1, 0) if k == 0 else (0, 1) if k == 8 else (0,)):
                        for dy in ((-1, 0) if r == 0 else (0, 1) if r == 8 else (0,)):
                            if dx == 0 and dy == 0:
                                continue
                            gx, gy = gx0 + dx, gy0 + dy
                            s_ = src(gx // 16, gy // 16, gx % 16, gy % 16)
                            if s_ and not s_[2]:
                                nr, nk = r - dy * 8, k - dx * 8
                                nb.append(s_[0].heights(s_[1])[nr * 17 + nk])
                                if onto == 'donor':
                                    dv = abs(s_[0].heights(s_[1])[nr * 17 + nk] - h[r * 17 + k])
                                    if dv > 1e-4:
                                        base_edits.setdefault(((gx // 16, gy // 16), s_[1]), [s_[0], {}])[1][(nr, nk)] = h[r * 17 + k]
                                        moved += 1
                                        worst = max(worst, dv)
                    if nb and onto == 'base':
                        target = nb[0]
                        dv = abs(h[r * 17 + k] - target)
                        if dv > 1e-4:
                            if dv > 2 and log is not None:
                                log.append((X, Y, i, r, k, round(dv, 2)))
                            edits.setdefault(((X, Y), i), {})[(r, k)] = target
                            moved += 1
                            worst = max(worst, dv)
    for ((X, Y), i), vals in edits.items():
        set_outer_heights(sources[(X, Y)][1], i, vals)
    for (_, i), (tile_, vals) in base_edits.items():
        set_outer_heights(tile_, i, vals)
    stitch.base_tiles_edited = {k[0] for k in base_edits}      # onto='donor': base tiles whose sea floor was raised
    return moved, worst


def _edge(t, i, side):
    """outer vertices of chunk i along one side, as (row, col) list in order: side 'E','W','S','N'"""
    if side == 'E':
        return [(v, 8) for v in range(9)]
    if side == 'W':
        return [(v, 0) for v in range(9)]
    if side == 'S':
        return [(8, v) for v in range(9)]
    return [(0, v) for v in range(9)]


_OPP = {'E': 'W', 'W': 'E', 'S': 'N', 'N': 'S'}
_STEP = {'E': (1, 0), 'W': (-1, 0), 'S': (0, 1), 'N': (0, -1)}


def tile_edge_pairs(X, Y, side):
    """(chunk in tile X_Y, chunk in the neighbouring tile) pairs along one tile edge"""
    out = []
    for j in range(16):
        if side == 'E':
            out.append((j * 16 + 15, j * 16))
        elif side == 'W':
            out.append((j * 16, j * 16 + 15))
        elif side == 'S':
            out.append((15 * 16 + j, j))
        else:
            out.append((j, 15 * 16 + j))
    return out


def heal_donor_seams(chunks_of):
    """Turtle's own tiles do not always meet (up to a few yards at some tile borders). chunks_of: {(X, Y): (Tile, set of
    chunk ids that come from it)}. Where two such chunks of neighbouring tiles touch, both edges get the average.
    -> vertices changed"""
    n = 0
    for (X, Y), (t, ids) in chunks_of.items():
        for side in ('E', 'S'):
            dx, dy = _STEP[side]
            nb = chunks_of.get((X + dx, Y + dy))
            if not nb:
                continue
            u, uids = nb
            for a, b in tile_edge_pairs(X, Y, side):
                if a not in ids or b not in uids:
                    continue
                ha, hb = t.heights(a), u.heights(b)
                va, vb = {}, {}
                for (r, k), (r2, k2) in zip(_edge(t, a, side), _edge(u, b, _OPP[side])):
                    x, y = ha[r * 17 + k], hb[r2 * 17 + k2]
                    if abs(x - y) > 1e-4:
                        va[(r, k)] = vb[(r2, k2)] = (x + y) / 2
                        n += 1
                if va:
                    set_outer_heights(t, a, va)
                    set_outer_heights(u, b, vb)
    return n


def match_tile_edges(t, X, Y, keep, neighbour):
    """t: a tile 3.3.5 does not have (built on moved open sea). Its chunks not in `keep` take the edge heights of the
    tile next to them, so no crack opens where the new tile meets the old ones. neighbour(X, Y) -> (base Tile, donor Tile
    or None, set of its chunks taken from the donor) or None. -> vertices changed"""
    n = 0
    for side in ('E', 'W', 'S', 'N'):
        dx, dy = _STEP[side]
        nb = neighbour(X + dx, Y + dy)
        if not nb:
            continue
        ub, ud, utk = nb
        for a, b in tile_edge_pairs(X, Y, side):
            if a in keep:
                continue
            hb = (ud if ud is not None and b in utk else ub).heights(b)
            vals = {}
            for (r, k), (r2, k2) in zip(_edge(t, a, side), _edge(ub, b, _OPP[side])):
                if abs(t.heights(a)[r * 17 + k] - hb[r2 * 17 + k2]) > 1e-4:
                    vals[(r, k)] = hb[r2 * 17 + k2]
            if vals:
                set_outer_heights(t, a, vals)
                n += len(vals)
    return n


def match_stock_edges(t, X, Y, take, neighbour):
    """t: the donor (Turtle) tile at X, Y. Its taken chunks on the tile border next to a tile no Turtle tile replaces
    (neighbour(...) -> (base Tile, None, set())) take that tile's edge heights, so no crack opens at the region's rim
    (Turtle's own tile there may differ slightly from 3.3.5's). -> vertices changed"""
    n = 0
    for side in ('E', 'W', 'S', 'N'):
        dx, dy = _STEP[side]
        nb = neighbour(X + dx, Y + dy)
        if not nb or nb[1] is not None:
            continue
        ub = nb[0]
        for a, b in tile_edge_pairs(X, Y, side):
            if a not in take:
                continue
            hb = ub.heights(b)
            vals = {}
            for (r, k), (r2, k2) in zip(_edge(t, a, side), _edge(ub, b, _OPP[side])):
                if abs(t.heights(a)[r * 17 + k] - hb[r2 * 17 + k2]) > 1e-4:
                    vals[(r, k)] = hb[r2 * 17 + k2]
            if vals:
                set_outer_heights(t, a, vals)
                n += len(vals)
    return n


# ---- sea floor from Turtle's server maps (Max, 2026-10-09) -------------------------------------------------------------
UNIT = CHUNK / 8               # distance between two outer vertices


def set_heights(t, i, hs):
    """all 145 absolute heights of chunk i (MCVT order), normals (MCNR) recomputed from them"""
    c = bytearray(t.mcnk[i])
    o = struct.unpack_from('<I', c, 0x14)[0]
    base = struct.unpack_from('<f', c, 0x68 + 8)[0]
    struct.pack_into('<145f', c, o, *[h - base for h in hs])
    t.mcnk[i] = bytes(c)
    set_normals(t, i)


def set_normals(t, i):
    """MCNR of chunk i from its own heights (central differences; one-sided on the chunk rim)"""
    hs = t.heights(i)
    O = lambda r, k: hs[min(max(r, 0), 8) * 17 + min(max(k, 0), 8)]
    out = []
    for j in range(145):
        r, k = divmod(j, 17)
        if k < 9:                    # outer vertex r, k
            r0, r1, k0, k1 = max(r - 1, 0), min(r + 1, 8), max(k - 1, 0), min(k + 1, 8)
            gr = (O(r1, k) - O(r0, k)) / ((r1 - r0) * UNIT)
            gc = (O(r, k1) - O(r, k0)) / ((k1 - k0) * UNIT)
        else:                        # inner vertex between outer rows r, r+1 and columns k-9, k-8
            k -= 9
            gr = (O(r + 1, k) + O(r + 1, k + 1) - O(r, k) - O(r, k + 1)) / (2 * UNIT)
            gc = (O(r, k + 1) + O(r + 1, k + 1) - O(r, k) - O(r + 1, k)) / (2 * UNIT)
        n = (gr * gr + gc * gc + 1) ** 0.5
        out += [max(-127, min(127, round(127 * gr / n))), max(-127, min(127, round(127 * gc / n))), round(127 / n)]
    c = bytearray(t.mcnk[i])
    o = struct.unpack_from('<I', c, 0x18)[0]
    assert c[o - 8:o - 4] == b'RNCM', 'MCNR not found'
    struct.pack_into('<435b', c, o, *out)
    t.mcnk[i] = bytes(c)


def grid_chunk(grid, i):
    """the 145 heights (MCVT order) of chunk i from a server-map grid (terrain.read_tw_grid)"""
    cy, cx = divmod(i, 16)
    out = []
    for r in range(17):
        if r % 2 == 0:
            out += [grid['v9'][(cy * 8 + r // 2) * 129 + cx * 8 + k] for k in range(9)]
        else:
            out += [grid['v8'][(cy * 8 + r // 2) * 128 + cx * 8 + k] for k in range(8)]
    return out


def sea_pits(t, grid, deeper_than=30.0, clamp=-480.0):
    """Chunks of t that lie far below Turtle's own sea floor: a vertex more than `deeper_than` yards below Turtle's server
    height where Turtle has water above it (stock -516 open-sea chunks left next to a Turtle island, or a 3.3.5 chunk
    whose edge was raised onto a Turtle neighbour). Turtle heights at the extractor clamp (-500) are not compared.
    The chunk must carry MH2O water of a vertex format whose depth can be written. -> sorted chunk ids"""
    out = []
    for i in range(256):
        if not grid['liq_flags'][i] or not t.water[i] or not t.water[i][1]:
            continue
        if any(struct.unpack_from('<H', raw, 2)[0] not in (0, 2) for raw, _, _ in t.water[i][1]):
            continue
        cy, cx = divmod(i, 16)
        hs, tw = t.heights(i), grid_chunk(grid, i)
        for j in range(145):
            if tw[j] > clamp and hs[j] < tw[j] - deeper_than:
                r, k = divmod(j, 17)
                lv = grid['liquid'](cy * 8 + r, cx * 8 + min(k, 8)) if k < 9 else grid['liquid'](cy * 8 + r, cx * 8 + k - 9)
                if lv is not None and lv > tw[j]:
                    out.append(i)
                    break
    return out


def set_water_depth(t, i, depth_scale=1.72, deep_below=-60.0):
    """MH2O of chunk i follows its ground: depth bytes = depth_scale x yards of water (3.3.5's own ratio), "deep" only on
    cells whose ground is below deep_below (else AzerothCore's extractor makes the whole chunk dark water)"""
    hs = t.heights(i)
    attr, insts = t.water[i]
    new = []
    for raw, bm, vx in insts:
        lt, lvf, mn, mx, x, y, w, h, ob, ov = struct.unpack('<HHffBBBBII', raw)
        n = (w + 1) * (h + 1)
        lv = list(struct.unpack_from('<%df' % n, vx)) if lvf == 0 and vx else [mx] * n
        dep = bytes(max(0, min(255, round(depth_scale * (lv[a * (w + 1) + b] - hs[(y + a) * 17 + x + b]))))
                    for a in range(h + 1) for b in range(w + 1))
        vx = (struct.pack('<%df' % n, *lv) + dep) if lvf == 0 else dep
        new.append((raw, bm, vx))
    deep = 0
    for cy in range(8):
        for cx in range(8):
            if _cell_ground(hs, cx, cy) < deep_below:
                deep |= 1 << (cy * 8 + cx)
    fish = struct.unpack_from('<Q', attr, 0)[0] if attr else 0xFFFFFFFFFFFFFFFF
    t.water[i] = (struct.pack('<QQ', fish, deep), new)


def stitch_to_neighbours(tiles, changed, other=None):
    """Chunks whose heights were replaced (changed: {(X, Y): set of chunk ids}, tiles: {(X, Y): Tile}) take the edge
    heights of the unchanged chunks next to them, inside the tile and across tile borders, so no crack opens. other(X, Y)
    -> Tile for a neighbouring tile that is not in tiles (the 3.3.5 one), or None. -> vertices moved, largest move"""
    def get(X, Y):
        if (X, Y) in tiles:
            return tiles[(X, Y)]
        return other(X, Y) if other else None
    moved, worst = 0, 0.0
    for (X, Y), ids in changed.items():
        t = tiles[(X, Y)]
        for i in sorted(ids):
            cy, cx = divmod(i, 16)
            gx0, gy0 = X * 16 + cx, Y * 16 + cy
            h = t.heights(i)
            vals = {}
            for r in range(9):
                for k in range(9):
                    if 0 < r < 8 and 0 < k < 8:
                        continue
                    for dx in ((-1, 0) if k == 0 else (0, 1) if k == 8 else (0,)):
                        for dy in ((-1, 0) if r == 0 else (0, 1) if r == 8 else (0,)):
                            if (dx, dy) == (0, 0) or (r, k) in vals:
                                continue
                            gx, gy = gx0 + dx, gy0 + dy
                            nX, nY, ni = gx // 16, gy // 16, (gy % 16) * 16 + gx % 16
                            if ni in changed.get((nX, nY), ()):
                                continue
                            u = get(nX, nY)
                            if u is None:
                                continue
                            v = u.heights(ni)[(r - dy * 8) * 17 + (k - dx * 8)]
                            if abs(v - h[r * 17 + k]) > 1e-4:
                                vals[(r, k)] = v
                                worst = max(worst, abs(v - h[r * 17 + k]))
            if vals:
                set_outer_heights(t, i, vals)
                set_normals(t, i)
                moved += len(vals)
    return moved, worst
