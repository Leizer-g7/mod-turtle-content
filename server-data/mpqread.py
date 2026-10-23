"""Minimal pure-Python MPQ reader (formats v1/v2) - no dependencies.
Supports: encrypted hash/block tables, encrypted files (incl. FIX_KEY), single-unit files,
sector CRC, compression zlib / bzip2 / PKWARE DCL (implode) / mixed masks.
"""
import struct, zlib, bz2, os

_CRYPT = []


def _init():
    seed = 0x00100001
    tbl = [0] * 0x500
    for i in range(0x100):
        idx = i
        for _ in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            t1 = (seed & 0xFFFF) << 16
            seed = (seed * 125 + 3) % 0x2AAAAB
            t2 = seed & 0xFFFF
            tbl[idx] = t1 | t2
            idx += 0x100
    return tbl


_CRYPT = _init()


def hash_string(s, htype):
    s1, s2 = 0x7FED7FED, 0xEEEEEEEE
    for ch in s.upper().encode('latin-1', 'replace'):
        s1 = (_CRYPT[(htype << 8) + ch] ^ (s1 + s2)) & 0xFFFFFFFF
        s2 = (ch + s1 + s2 + (s2 << 5) + 3) & 0xFFFFFFFF
    return s1


def decrypt(data, key):
    n = len(data) // 4
    vals = list(struct.unpack('<%dI' % n, data[:n * 4]))
    s2 = 0xEEEEEEEE
    for i in range(n):
        s2 = (s2 + _CRYPT[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        v = vals[i] ^ ((key + s2) & 0xFFFFFFFF)
        key = ((((~key) << 0x15) + 0x11111111) | (key >> 0x0B)) & 0xFFFFFFFF
        s2 = (v + s2 + (s2 << 5) + 3) & 0xFFFFFFFF
        vals[i] = v
    return struct.pack('<%dI' % n, *vals) + data[n * 4:]


# ---------------------------------------------------------------- PKWARE DCL explode (port of zlib/contrib/blast)
_LITLEN = [11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8, 9, 7, 6, 7, 8, 7, 6, 55, 8, 23, 24, 12, 11,
           7, 9, 11, 12, 6, 7, 22, 5, 7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9, 8, 25, 11, 8, 11, 9, 12, 8, 12, 5, 38,
           5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27, 44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45,
           12, 61, 12, 45, 44, 173]
_LENLEN = [2, 35, 36, 53, 38, 23]
_DISTLEN = [2, 20, 53, 230, 247, 151, 248]
_BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]


def _construct(rep):
    length = []
    for r in rep:
        length += [r & 15] * ((r >> 4) + 1)
    count = [0] * 14
    for l in length:
        count[l] += 1
    offs = [0] * 14
    for l in range(1, 13):
        offs[l + 1] = offs[l] + count[l]
    symbol = [0] * len(length)
    for s in range(len(length)):
        if length[s]:
            symbol[offs[length[s]]] = s
            offs[length[s]] += 1
    return count, symbol


_LIT = _construct(_LITLEN)
_LEN = _construct(_LENLEN)
_DIST = _construct(_DISTLEN)


class _Bits:
    def __init__(self, data):
        self.d, self.p, self.buf, self.cnt = data, 0, 0, 0

    def bits(self, need):
        val = self.buf
        while self.cnt < need:
            if self.p >= len(self.d):
                raise ValueError('pkware: out of input')
            val |= self.d[self.p] << self.cnt
            self.p += 1
            self.cnt += 8
        self.buf = val >> need
        self.cnt -= need
        return val & ((1 << need) - 1)

    def decode(self, h):
        count, symbol = h
        code = first = index = 0
        bitbuf, left, ln = self.buf, self.cnt, 1
        while True:
            while left:
                code |= (bitbuf & 1) ^ 1
                bitbuf >>= 1
                cnt = count[ln]
                if code < first + cnt:
                    self.buf, self.cnt = bitbuf, (self.cnt - ln) & 7
                    return symbol[index + (code - first)]
                index += cnt
                first += cnt
                first <<= 1
                code <<= 1
                ln += 1
                left -= 1
            left = 14 - ln
            if left == 0 or self.p >= len(self.d):
                raise ValueError('pkware: bad code')
            bitbuf = self.d[self.p]
            self.p += 1
            if left > 8:
                left = 8


def explode(data):
    s = _Bits(data)
    lit = s.bits(8)
    dictsz = s.bits(8)
    if lit > 1 or dictsz < 4 or dictsz > 6:
        raise ValueError('pkware: bad header')
    out = bytearray()
    while True:
        if s.bits(1):
            sym = s.decode(_LEN)
            ln = _BASE[sym] + s.bits(_EXTRA[sym])
            if ln == 519:
                break
            sym = 2 if ln == 2 else dictsz
            dist = s.decode(_DIST) << sym
            dist += s.bits(sym)
            dist += 1
            for _ in range(ln):
                out.append(out[-dist])
        else:
            out.append(s.decode(_LIT) if lit else s.bits(8))
    return bytes(out)


def _decompress(buf, outsize):
    if len(buf) >= outsize:
        return buf[:outsize]
    mask = buf[0]
    data = buf[1:]
    if mask & 0x10:
        data = bz2.decompress(data)
    if mask & 0x08:
        data = explode(data)
    if mask & 0x02:
        data = zlib.decompress(data)
    if mask & ~(0x10 | 0x08 | 0x02):
        raise ValueError('unsupported compression mask 0x%x' % mask)
    return data


class MPQ:
    def __init__(self, path):
        self.path = path
        self.f = open(path, 'rb')
        off = 0
        while True:
            self.f.seek(off)
            magic = self.f.read(4)
            if magic == b'MPQ\x1a':
                break
            if magic == b'MPQ\x1b':
                _, _, hdr_off = struct.unpack('<III', self.f.read(12))
                off += hdr_off
                continue
            off += 512
            if off > os.path.getsize(path):
                raise ValueError('not an MPQ: ' + path)
        self.base = off
        self.f.seek(off)
        h = self.f.read(44)
        (_, hsize, _, ver, sshift, htpos, btpos, htsize, btsize) = struct.unpack('<4sIIHHIIII', h[:32])
        hthi = bthi = 0
        if ver >= 1 and hsize >= 44:
            _, hthi, bthi = struct.unpack('<QHH', h[32:44])
        self.sector = 512 << sshift
        self.f.seek(off + htpos + (hthi << 32))
        ht = decrypt(self.f.read(htsize * 16), hash_string('(hash table)', 3))
        self.f.seek(off + btpos + (bthi << 32))
        bt = decrypt(self.f.read(btsize * 16), hash_string('(block table)', 3))
        self.hashes = {}
        for i in range(htsize):
            n1, n2, loc, plat, bi = struct.unpack('<IIHHI', ht[i * 16:i * 16 + 16])
            if bi < btsize:
                self.hashes.setdefault((n1, n2), bi)
        self.blocks = [struct.unpack('<IIII', bt[i * 16:i * 16 + 16]) for i in range(btsize)]

    def _block(self, name):
        bi = self.hashes.get((hash_string(name, 1), hash_string(name, 2)))
        if bi is None:
            return None
        b = self.blocks[bi]
        if not (b[3] & 0x80000000) or (b[3] & 0x02000000):
            return None
        return b

    def has(self, name):
        return self._block(name) is not None

    def read(self, name):
        b = self._block(name)
        if b is None:
            return None
        pos, csize, fsize, flags = b
        key = 0
        if flags & 0x10000:
            key = hash_string(name.replace('/', '\\').split('\\')[-1], 3)
            if flags & 0x20000:
                key = ((key + pos) ^ fsize) & 0xFFFFFFFF
        self.f.seek(self.base + pos)
        raw = self.f.read(csize)
        if flags & 0x01000000:   # single unit
            if flags & 0x10000:
                raw = decrypt(raw, key)
            if flags & 0x200:
                return _decompress(raw, fsize)
            if flags & 0x100:
                return explode(raw) if csize < fsize else raw
            return raw
        if not (flags & 0x300):
            data = raw
            if flags & 0x10000:
                n = (fsize + self.sector - 1) // self.sector
                data = b''.join(decrypt(raw[i * self.sector:(i + 1) * self.sector], (key + i) & 0xFFFFFFFF) for i in range(n))
            return data[:fsize]
        nsec = (fsize + self.sector - 1) // self.sector
        ntab = nsec + 1 + (1 if flags & 0x04000000 else 0)
        tab = raw[:ntab * 4]
        if flags & 0x10000:
            tab = decrypt(tab, (key - 1) & 0xFFFFFFFF)
        offs = struct.unpack('<%dI' % ntab, tab)
        out = []
        for i in range(nsec):
            sec = raw[offs[i]:offs[i + 1]]
            if flags & 0x10000:
                sec = decrypt(sec, (key + i) & 0xFFFFFFFF)
            want = min(self.sector, fsize - i * self.sector)
            if flags & 0x200:
                out.append(_decompress(sec, want))
            elif len(sec) < want:
                out.append(explode(sec))
            else:
                out.append(sec[:want])
        return b''.join(out)[:fsize]

    def listfile(self):
        d = self.read('(listfile)')
        if not d:
            return []
        return [x.strip() for x in d.decode('latin-1').replace('\r', '\n').split('\n') if x.strip()]
