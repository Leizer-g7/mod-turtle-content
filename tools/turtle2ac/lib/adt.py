"""Turtle ADT -> 3.3.5 client/server-safe ADT.

Turtle's map tiles are already in the 3.3.5 chunk layout (MVER 18, MHDR with MH2O slot, 4-bit 2048-byte
alpha maps), but their tools leave a few things the 3.3.5 client and AzerothCore's map_extractor do not expect:

1. MCNK.ofsMCLQ = 0xFFFFFFFF with sizeMCLQ = 8 when a chunk has no legacy liquid. map_extractor follows the
   offset and crashes. -> set to 0/0.
2. MH2O chunks whose liquid instance list repeats the same layer 8 or 32 times. The client would draw the
   same water many times over. -> layer count set to 1 when every layer is identical (data left in place,
   so no offsets move).
3. Tiles that have MH2O *and* duplicated legacy MCLQ water. -> MCLQ dropped, MH2O is what 3.3.5 uses.
4. Doodad/WMO placement uniqueIds that Turtle allocated for its own objects (>= 1,000,000) could collide
   with ids Blizzard used in neighbouring 3.3.5 tiles, which makes the client skip one of the two objects.
   -> moved into a reserved range 0x7F000000 + slot * 0x10000 + n (same id in every tile that shares it).
"""
import struct

TURTLE_UID_MIN = 1000000
UID_BASE = 0x7F000000


def top_chunks(d):
    p = 0
    while p + 8 <= len(d):
        t = d[p:p + 4][::-1].decode('latin-1')
        s = struct.unpack_from('<I', d, p + 4)[0]
        if t == 'MCNK':
            return
        yield t, p + 8, s
        p += 8 + s


def mcnk_offsets(d):
    return [struct.unpack_from('<I', d, 92 + i * 16)[0] for i in range(256)]


def area_ids(d):
    return {struct.unpack_from('<I', d, off + 8 + 52)[0] for off in mcnk_offsets(d)}


def fix(data, uid_map, uid_alloc):
    """Return (fixed bytes, stats). uid_map is shared across all tiles of a build; uid_alloc() hands out new ids."""
    d = bytearray(data)
    st = dict(mclq_ff=0, mh2o_dedup=0, mclq_dropped=0, uids=0)
    assert d[0:4] == b'REVM' and d[12:16] == b'RDHM', 'not an ADT'
    mh = struct.unpack_from('<16I', d, 20)
    offs = mcnk_offsets(d)
    for off in offs:
        o, s = struct.unpack_from('<II', d, off + 8 + 96)
        if o == 0xFFFFFFFF:
            struct.pack_into('<II', d, off + 8 + 96, 0, 0)
            st['mclq_ff'] += 1
    if mh[10] and struct.unpack_from('<I', d, 20 + mh[10] + 4)[0] >= 256 * 12:     # some Turtle tiles carry an empty MH2O
        base = 20 + mh[10] + 8
        for i in range(256):
            oi, lc, oa = struct.unpack_from('<III', d, base + i * 12)
            if lc > 1:
                def sig(k):
                    lt, lvf, mn, mx, x, y, w, h, ob, ov = struct.unpack_from('<HHffBBBBII', d, base + oi + k * 24)
                    n = (w + 1) * (h + 1)
                    sz = {0: n * 5, 1: n * 8, 2: n, 3: n * 9}.get(lvf, 0)
                    mask = bytes(d[base + ob:base + ob + (w * h + 7) // 8]) if ob else b''
                    return (lt, lvf, mn, mx, x, y, w, h, mask, bytes(d[base + ov:base + ov + sz]) if ov else b'')
                first = sig(0)
                if all(sig(k) == first for k in range(1, lc)):
                    struct.pack_into('<I', d, base + i * 12 + 4, 1)
                    st['mh2o_dedup'] += 1
        for off in offs:
            o, s = struct.unpack_from('<II', d, off + 8 + 96)
            if o:
                struct.pack_into('<II', d, off + 8 + 96, 0, 0)
                st['mclq_dropped'] += 1
    for t, o, s in list(top_chunks(d)):
        rec = {'MDDF': 36, 'MODF': 64}.get(t)
        if not rec:
            continue
        for i in range(s // rec):
            u = struct.unpack_from('<I', d, o + i * rec + 4)[0]
            if u >= TURTLE_UID_MIN and u < UID_BASE:
                if u not in uid_map:
                    uid_map[u] = uid_alloc()
                struct.pack_into('<I', d, o + i * rec + 4, uid_map[u])
                st['uids'] += 1
    return bytes(d), st


def _subst_names(blob, sub):
    """Rebuild a NUL-separated name block with substitutions.
    -> (new blob, old offset -> new offset, list of (old, new) names that changed)"""
    names, p = [], 0
    while p < len(blob):
        e = blob.find(b'\0', p)
        if e < 0:
            e = len(blob)
        if e > p:
            names.append((p, blob[p:e].decode('latin-1')))
        p = e + 1
    out, remap, changed = bytearray(), {}, []
    for off, n in names:
        new = sub(n)
        if new != n:
            changed.append((n, new))
        remap[off] = len(out)
        out += new.encode('latin-1') + b'\0'
    while len(out) % 4:
        out += b'\0'
    return bytes(out), remap, changed


def substitute_models(data, sub):
    """Replace doodad model paths in an ADT (MMDX/MMID) using sub(name) -> name.
    Moves every chunk after MMDX and fixes the MHDR and MCIN offsets. -> (bytes, changed list)"""
    d = bytearray(data)
    tops = list(top_chunks(d))
    pos = {t: (o, s) for t, o, s in tops}
    if 'MMDX' not in pos:
        return data, []
    mo, ms = pos['MMDX']
    new, remap, changed = _subst_names(bytes(d[mo:mo + ms]), sub)
    if not changed:
        return data, []
    io, is_ = pos['MMID']
    ids = struct.unpack_from('<%dI' % (is_ // 4), d, io)
    struct.pack_into('<%dI' % len(ids), d, io, *[remap[i] for i in ids])
    delta = len(new) - ms
    cut = mo + ms                                   # everything at/after this file offset moves by delta
    out = d[:mo - 4] + struct.pack('<I', len(new)) + new + d[cut:]
    mh = 20
    for k in range(16):
        v = struct.unpack_from('<I', out, mh + k * 4)[0]
        if v and v + mh >= cut:
            struct.pack_into('<I', out, mh + k * 4, v + delta)
    mcin = struct.unpack_from('<I', out, mh + 4)[0] + mh + 8     # MHDR.ofsMCIN -> MCIN data
    for i in range(256):
        v = struct.unpack_from('<I', out, mcin + i * 16)[0]
        if v >= cut:
            struct.pack_into('<I', out, mcin + i * 16, v + delta)
    return bytes(out), changed


# --------------------------------------------------------------------------- MCNK sub-chunk layout
# The 3.3.5 client walks every MCNK's sub-chunks in order (tag, size, data) from the end of the 128-byte header.
# Bytes the header does not point at (e.g. an MCLQ block whose header offset was zeroed) are read as chunk
# headers and crash the client (#132, ACCESS_VIOLATION in the MCNK parser). strip_orphan_mclq() removes such
# bytes; mcnk_problems() is the validator every shipped tile must pass.
MCNK_TAGS = {'MCVT', 'MCNR', 'MCLY', 'MCRF', 'MCSH', 'MCAL', 'MCLQ', 'MCSE', 'MCCV', 'MCLV'}
# header field (byte offset) -> sub-chunk it points at
_HDR_OFS = {0x14: 'MCVT', 0x18: 'MCNR', 0x1C: 'MCLY', 0x20: 'MCRF', 0x24: 'MCAL', 0x2C: 'MCSH', 0x58: 'MCSE',
            0x60: 'MCLQ', 0x74: 'MCCV', 0x78: 'MCLV'}
MHDR_TAGS = ['', 'MCIN', 'MTEX', 'MMDX', 'MMID', 'MWMO', 'MWID', 'MDDF', 'MODF', 'MFBO', 'MH2O', 'MTXF']


def _sub_len(d, base, rel, mcnk_end, hdr):
    """total byte length of the sub-chunk at base+rel (header included)"""
    t = d[base + rel:base + rel + 4][::-1].decode('latin-1')
    s = struct.unpack_from('<I', d, base + rel + 4)[0]
    if t == 'MCLQ':
        sz = struct.unpack_from('<I', hdr, 0x64)[0]
        return max(sz, 8)
    if t == 'MCNR' and s == 435:
        return 8 + 435 + 13
    return 8 + s


def mcnk_problems(data):
    """Client-style walk of every MCNK. -> list of strings (empty = OK)."""
    d = data
    out = []
    for i, off in enumerate(mcnk_offsets(d)):
        size = struct.unpack_from('<I', d, off + 4)[0]
        end = off + 8 + size
        hdr = d[off + 8:off + 8 + 128]
        ofs_lq, sz_lq = struct.unpack_from('<II', hdr, 0x60)
        p = off + 8 + 128
        while p < end:
            if p + 8 > end:
                out.append(f'chunk {i}: {end - p} stray bytes at the end'); break
            t = d[p:p + 4][::-1].decode('latin-1')
            s = struct.unpack_from('<I', d, p + 4)[0]
            if t not in MCNK_TAGS:
                out.append(f'chunk {i}: unknown tag {t!r} at +{p - off}'); break
            if t == 'MCLQ':
                if p - off != ofs_lq or not ofs_lq:
                    out.append(f'chunk {i}: MCLQ at +{p - off} not referenced by the header (ofsMCLQ={ofs_lq})'); break
                p += max(sz_lq, 8)
                continue
            if t == 'MCNR' and s == 435:
                s += 13
            p += 8 + s
        if p != end and not (out and out[-1].startswith(f'chunk {i}:')):
            out.append(f'chunk {i}: walk ends at +{p - off}, MCNK ends at +{end - off}')
    return out


def strip_orphan_mclq(data):
    """Remove MCNK bytes the header does not reference (orphan MCLQ blocks). Recomputes MCNK sizes, header
    offsets, MCIN and MHDR. -> (bytes, number of chunks changed)"""
    d = bytes(data)
    tops, p = [], 0
    while p + 8 <= len(d):
        t = d[p:p + 4][::-1].decode('latin-1')
        s = struct.unpack_from('<I', d, p + 4)[0]
        tops.append((t, p, s))
        p += 8 + s
    changed = 0
    out = bytearray()
    pos = {}
    mcnk_new = []                         # (new offset, new total size)
    mcin_entries = struct.unpack_from('<1024I', d, [o for t, o, s in tops if t == 'MCIN'][0] + 8)
    for t, o, s in tops:
        if t != 'MCNK':
            pos.setdefault(t, len(out))
            out += d[o:o + 8 + s]
            continue
        hdr = bytearray(d[o + 8:o + 8 + 128])
        end = o + 8 + s
        refs = []
        for f, tag in _HDR_OFS.items():
            rel = struct.unpack_from('<I', hdr, f)[0]
            if not rel or o + rel + 8 > end:
                continue
            if d[o + rel:o + rel + 4][::-1].decode('latin-1') != tag:
                continue
            refs.append((rel, f, _sub_len(d, o, rel, end, hdr)))
        refs.sort()
        body = bytearray()
        newrel = {}
        for rel, f, ln in refs:
            if rel in newrel:
                continue
            newrel[rel] = 8 + 128 + len(body)
            body += d[o + rel:o + rel + ln]
        for rel, f, ln in refs:
            struct.pack_into('<I', hdr, f, newrel[rel])
        if len(body) != s - 128 or bytes(hdr) != d[o + 8:o + 8 + 128]:
            changed += 1
        mcnk_new.append((len(out), 8 + 128 + len(body)))
        out += b'KNCM' + struct.pack('<I', 128 + len(body)) + hdr + body
    if not changed:
        return data, 0
    mh = 20
    for k, tag in enumerate(MHDR_TAGS):
        if not tag:
            continue
        if struct.unpack_from('<I', out, mh + k * 4)[0]:
            assert tag in pos, tag
            struct.pack_into('<I', out, mh + k * 4, pos[tag] - mh)
    mcin = pos['MCIN'] + 8
    for i, (no, ns) in enumerate(mcnk_new):
        struct.pack_into('<II', out, mcin + i * 16, no, ns)
    return bytes(out), changed
