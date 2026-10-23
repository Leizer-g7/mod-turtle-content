"""WMO root helpers: doodad model path substitution (MODN/MODD) and the WMO id (MOHD)."""
import struct
from lib.adt import _subst_names


def chunks(d):
    p = 0
    while p + 8 <= len(d):
        t = d[p:p + 4][::-1].decode('latin-1')
        s = struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, s
        p += 8 + s


def substitute_models(data, sub):
    """-> (bytes, changed). Root files have no absolute offsets, so chunks are simply rebuilt."""
    parts, changed, remap = [], [], None
    for t, p, s in chunks(data):
        body = data[p + 8:p + 8 + s]
        if t == 'MODN':
            body, remap, changed = _subst_names(body, sub)
        parts.append((t, bytearray(body)))
    if not changed:
        return data, []
    for t, body in parts:
        if t == 'MODD':
            for i in range(len(body) // 40):
                v = struct.unpack_from('<I', body, i * 40)[0]
                struct.pack_into('<I', body, i * 40, remap[v & 0xFFFFFF] | (v & 0xFF000000))
    return b''.join(t[::-1].encode('latin-1') + struct.pack('<I', len(b)) + bytes(b) for t, b in parts), changed


def info(data):
    for t, p, s in chunks(data):
        if t == 'MOHD':
            return dict(groups=struct.unpack_from('<I', data, p + 8 + 4)[0], wmo_id=struct.unpack_from('<I', data, p + 8 + 32)[0])
    return {}


# --------------------------------------------------------------------------- group liquid
# Turtle roots set MOHD flag 0x4 ("groupLiquid is a LiquidType.dbc id") and write groupLiquid = 15 in every group.
# Without the flag 15 means "no liquid"; with it the 3.3.5 client (and AzerothCore's vmap4_extractor) map 15 to
# WMO Magma, and a group with a liquid type but no MLIQ is treated as completely filled -> lava inside every
# building, on the client and on the server. fix_group_liquid() gives every group the value 3.3.5 expects.
MOHD_LIQUID_DBC = 0x4
MOGP_LIQUID_OFS = 52                 # groupLiquid in the 68-byte MOGP header
MOGP_OCEAN = 0x80000                 # 'water' in this group is ocean


def root_flags(data):
    for t, p, s in chunks(data):
        if t == 'MOHD':
            return struct.unpack_from('<H', data, p + 8 + 60)[0]
    return 0


def _mogp(data):
    for t, p, s in chunks(data):
        if t == 'MOGP':
            return p + 8, s
    return None, 0


def _mliq_type(data, base, size):
    """liquid kind (0 water, 1 ocean, 2 magma, 3 slime) of the group's MLIQ, or None when it has none"""
    p = base + 68
    end = base + size
    while p + 8 <= end:
        t = data[p:p + 4][::-1].decode('latin-1')
        s = struct.unpack_from('<I', data, p + 4)[0]
        if t == 'MLIQ':
            xv, yv, xt, yt = struct.unpack_from('<4I', data, p + 8)
            flags = data[p + 8 + 30 + xv * yv * 8:p + 8 + 30 + xv * yv * 8 + xt * yt]
            kinds = [f & 0xF for f in flags if f & 0xF != 0xF]
            return (kinds[0] & 3) if kinds else 0
        p += 8 + s
    return None


def group_liquid_wanted(rflags, data):
    """-> (current groupLiquid, value 3.3.5 needs)"""
    base, size = _mogp(data)
    cur = struct.unpack_from('<I', data, base + MOGP_LIQUID_OFS)[0]
    if not rflags & MOHD_LIQUID_DBC:
        return cur, cur
    kind = _mliq_type(data, base, size)
    if kind is None:
        return cur, 0
    mflags = struct.unpack_from('<I', data, base + 8)[0]
    want = {0: 13 + (1 if mflags & MOGP_OCEAN else 0), 1: 14, 2: 19, 3: 20}[kind]
    return cur, (cur if cur in (13, 14, 19, 20) or cur >= 21 else want)


def fix_group_liquid(rflags, data):
    """-> (bytes, changed?)"""
    cur, want = group_liquid_wanted(rflags, data)
    if cur == want:
        return data, False
    d = bytearray(data)
    struct.pack_into('<I', d, _mogp(data)[0] + MOGP_LIQUID_OFS, want)
    return bytes(d), True
