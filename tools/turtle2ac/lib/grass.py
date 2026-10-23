"""Ground clutter (grass) on the converted terrain (Max's fixes, 2026-10-09).

Per MCNK chunk:
  - layer effect ids: MCLY entry (16 bytes: texture, flags, alpha offset, effectId); the client draws the clutter of the
    GroundEffectTexture row named by the layer each cell's 2-bit map (header 0x40) picks.
  - noEffectDoodad: header 0x50, 8 bytes, byte = cell row, bit = cell column (LSB first); a set bit = no clutter there.

retag()          gives untagged layers of one texture an effect id (Turtle dirt layers carry 0, 65535 or 9906).
no_clutter()     sets noEffectDoodad on cells under water and on cells whose most visible texture is a road or sand.
"""
import struct

import numpy  # noqa: F401  (dominant())

LAYER_FLAG_COMPRESSED = 0x200
MCNK_FLAG_DO_NOT_FIX_ALPHA = 0x8000


def _layers(c):
    n = struct.unpack_from('<I', c, 0x0C)[0]
    o = struct.unpack_from('<I', c, 0x1C)[0]
    assert c[o - 8:o - 4] == b'YLCM', 'MCLY not found'
    return n, o


def layer_effects(t, i):
    """[(texture name, effect id)] of chunk i"""
    c = t.mcnk[i]
    n, o = _layers(c)
    return [(t.mtex[struct.unpack_from('<I', c, o + k * 16)[0]], struct.unpack_from('<I', c, o + k * 16 + 12)[0])
            for k in range(n)]


def retag(t, i, rules):
    """rules: [(texture substring, set of effect ids to replace, new id)] -> layers changed"""
    c = bytearray(t.mcnk[i])
    n, o = _layers(c)
    hit = 0
    for k in range(n):
        tid, _, _, eff = struct.unpack_from('<4I', c, o + k * 16)
        name = t.mtex[tid].lower().replace('/', '\\')
        for sub, old, new in rules:
            if sub in name and eff in old:
                struct.pack_into('<I', c, o + k * 16 + 12, new)
                hit += 1
                break
    if hit:
        t.mcnk[i] = bytes(c)
    return hit


def _alpha(c, k_off, nxt, flags, mcnk_flags, data):
    """64x64 alpha (0..255) of one layer from the MCAL data"""
    if flags & LAYER_FLAG_COMPRESSED:
        out, p = bytearray(), k_off
        while len(out) < 4096 and p < len(data):
            b = data[p]
            p += 1
            cnt = b & 0x7F
            if b & 0x80:
                out += bytes([data[p]]) * cnt
                p += 1
            else:
                out += data[p:p + cnt]
                p += cnt
        return list(out[:4096]) + [0] * max(0, 4096 - len(out))
    size = nxt - k_off
    if size >= 4096:
        return list(data[k_off:k_off + 4096])
    out = []
    for b in data[k_off:k_off + 2048]:
        out += [(b & 0x0F) * 17, (b >> 4) * 17]
    if not mcnk_flags & MCNK_FLAG_DO_NOT_FIX_ALPHA:        # 63x63 map: last row and column repeat their neighbour
        for r in range(64):
            out[r * 64 + 63] = out[r * 64 + 62]
        out[63 * 64:] = out[62 * 64:63 * 64]
    return out


def dominant(t, i):
    """index of the most visible texture layer in each of the 64 cells (cell = cy * 8 + cx)"""
    c = t.mcnk[i]
    n, o = _layers(c)
    if n <= 1:
        return [0] * 64
    oa = struct.unpack_from('<I', c, 0x24)[0]
    assert c[oa - 8:oa - 4] == b'LACM', 'MCAL not found'
    data = c[oa:oa + struct.unpack_from('<I', c, oa - 4)[0]]
    mf = struct.unpack_from('<I', c, 0)[0]
    ents = [struct.unpack_from('<4I', c, o + k * 16) for k in range(n)]
    offs = [e[2] for e in ents[1:]] + [len(data)]
    alphas = [_alpha(c, ents[k][2], offs[k], ents[k][1], mf, data) for k in range(1, n)]
    import numpy as np
    A = np.array(alphas, dtype=np.float32).reshape(n - 1, 64, 64) / 255.0
    w = np.zeros((n, 64, 64), dtype=np.float32)
    vis = np.ones((64, 64), dtype=np.float32)
    for k in range(n - 1, 0, -1):                       # top layer first
        w[k] = vis * A[k - 1]
        vis = vis * (1 - A[k - 1])
    w[0] = vis
    cell = w.reshape(n, 8, 8, 8, 8).sum(axis=(2, 4))    # layer, cell row, cell column
    return [int(v) for v in cell.argmax(axis=0).reshape(64)]


def _ground(hs, cx, cy):
    return (hs[cy * 17 + cx] + hs[cy * 17 + cx + 1] + hs[(cy + 1) * 17 + cx] + hs[(cy + 1) * 17 + cx + 1]) / 4


def water_cells(t, i, above=0.2):
    """cells whose MH2O or MCLQ surface is more than `above` yards over the cell's ground -> set of cell ids"""
    hs = t.heights(i)
    out = set()
    w = t.water[i]
    if w and w[1]:
        for raw, bm, vx in w[1]:
            lt, lvf, mn, mx, x, y, ww, hh, ob, ov = struct.unpack('<HHffBBBBII', raw)
            nv = (ww + 1) * (hh + 1)
            lv = struct.unpack_from('<%df' % nv, vx) if lvf in (0, 1, 3) and len(vx) >= 4 * nv else None
            for a in range(hh):
                for b in range(ww):
                    bit = a * ww + b
                    if bm and not (bm[bit // 8] >> (bit % 8)) & 1:
                        continue
                    if lv:
                        level = (lv[a * (ww + 1) + b] + lv[a * (ww + 1) + b + 1] + lv[(a + 1) * (ww + 1) + b] +
                                 lv[(a + 1) * (ww + 1) + b + 1]) / 4
                    else:
                        level = mx
                    if level > _ground(hs, x + b, y + a) + above:
                        out.add((y + a) * 8 + x + b)
    c = t.mcnk[i]
    o, sz = struct.unpack_from('<II', c, 0x60)
    if o and sz > 8 and c[o - 8:o - 4] == b'QLCM':
        base = o + 8                                         # min, max, then 9x9 vertices of 8 bytes
        lv = [struct.unpack_from('<f', c, base + k * 8 + 4)[0] for k in range(81)]
        fl = c[base + 81 * 8:base + 81 * 8 + 64]
        for cy in range(8):
            for cx in range(8):
                if fl[cy * 8 + cx] & 0x0F == 0x0F:
                    continue
                level = (lv[cy * 9 + cx] + lv[cy * 9 + cx + 1] + lv[(cy + 1) * 9 + cx] + lv[(cy + 1) * 9 + cx + 1]) / 4
                if level > _ground(hs, cx, cy) + above:
                    out.add(cy * 8 + cx)
    return out


def is_road(name, words):
    n = name.lower().replace('/', '\\').split('\\')[-1]
    return any(w in n for w in words)


def is_sand(name, words, not_words):
    n = name.lower().replace('/', '\\').split('\\')[-1]
    return any(w in n for w in words) and not any(w in n for w in not_words)


def no_clutter(t, i, road_words, sand_words, sand_not, above=0.2):
    """set noEffectDoodad on water, road and sand cells of chunk i -> (water, road, sand) cell counts newly set"""
    cells_w = water_cells(t, i, above)
    dom = dominant(t, i)
    texs = [n_ for n_, _ in layer_effects(t, i)]
    c = bytearray(t.mcnk[i])
    bits = list(c[0x50:0x58])
    cnt = [0, 0, 0]
    for cell in range(64):
        cy, cx = divmod(cell, 8)
        tex = texs[dom[cell]] if texs else ''
        kind = 0 if cell in cells_w else 1 if is_road(tex, road_words) else 2 if is_sand(tex, sand_words, sand_not) else None
        if kind is None:
            continue
        if not (bits[cy] >> cx) & 1:
            bits[cy] |= 1 << cx
            cnt[kind] += 1
    c[0x50:0x58] = bytes(bits)
    t.mcnk[i] = bytes(c)
    return cnt


def same_ground(t, i, base):
    """chunk i of t has the 3.3.5 tile's own texture layers and alpha maps (a stock chunk the grass pass leaves alone)"""
    a, b = t.mcnk[i], base.mcnk[i]
    try:
        la, lb = layer_effects(t, i), layer_effects(base, i)
    except AssertionError:
        return False
    if [n.lower().replace('/', '\\') for n, _ in la] != [n.lower().replace('/', '\\') for n, _ in lb]:
        return False

    def mcal(c):
        oa = struct.unpack_from('<I', c, 0x24)[0]
        if not oa or c[oa - 8:oa - 4] != b'LACM':
            return b''
        return c[oa:oa + struct.unpack_from('<I', c, oa - 4)[0]]
    return mcal(a) == mcal(b)
