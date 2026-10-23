"""Minimap images and the client's md5translate.trs (Max's fixes, 2026-10-09).

The trs is a list of "dir: <Dir>" blocks, each holding "<Dir>\\mapX_Y.blp<TAB><file>.blp" lines; the client finds a
tile's image through the block of its map directory, so a new line must go into its own block (a Giln line appended
under another block is never found).

A minimap image covers one ADT tile: 256 x 256 pixels, 16 x 16 per chunk, x along the chunk columns, y along the rows.
compose() takes some chunks from one image and the rest from another; blp_dxt1() writes the result as BLP2 DXT1 with
mipmaps (the format of the stock images).
"""
import io
import struct

import numpy as np


# ---- md5translate.trs -------------------------------------------------------------------------------------------------
class Trs:
    def __init__(self, text):
        self.blocks = []                    # [dir name, [lines]]
        cur = None
        for line in text.replace('\r\n', '\n').split('\n'):
            if not line.strip():
                continue
            if line.lower().startswith('dir:'):
                cur = [line[4:].strip(), []]
                self.blocks.append(cur)
                continue
            if cur is None:
                cur = ['', []]
                self.blocks.append(cur)
            cur[1].append(line)

    def entries(self):
        """{plain name lower: (plain, target)}"""
        out = {}
        for d, lines in self.blocks:
            for l in lines:
                p = l.split('\t')
                if len(p) == 2:
                    plain = p[0] if '\\' in p[0] or not d else d + '\\' + p[0]
                    out.setdefault(plain.lower(), (plain, p[1]))
        return out

    def set(self, plain, target):
        """replace the line of `plain` in its directory's block, or add it there (new block at the end if needed)"""
        d = plain.rsplit('\\', 1)[0] if '\\' in plain else ''
        blk = next((b for b in self.blocks if b[0].lower() == d.lower()), None)
        if blk is None:
            blk = [d, []]
            self.blocks.append(blk)
        low = plain.lower()
        for k, l in enumerate(blk[1]):
            if l.split('\t')[0].lower() == low:
                blk[1][k] = f'{plain}\t{target}'
                return 'replaced'
        blk[1].append(f'{plain}\t{target}')
        return 'added'

    def text(self):
        out = []
        for d, lines in self.blocks:
            if d:
                out.append(f'dir: {d}')
            out += lines
        return '\r\n'.join(out) + '\r\n'


# ---- images ---------------------------------------------------------------------------------------------------------
def load_rgb(blob):
    from PIL import Image
    im = Image.open(io.BytesIO(blob))
    im.load()
    im = im.convert('RGB')
    if im.size != (256, 256):
        im = im.resize((256, 256), Image.BILINEAR)
    return np.asarray(im, dtype=np.uint8).copy()


def compose(base_rgb, top_rgb, top_chunks):
    """base image with the chunks in top_chunks (ids 0..255) taken from top"""
    out = base_rgb.copy()
    for i in top_chunks:
        cy, cx = divmod(i, 16)
        out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = top_rgb[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
    return out


def _q565(c):
    r = np.clip(np.rint(c[:, 0] * 31 / 255), 0, 31).astype(np.uint32)
    g = np.clip(np.rint(c[:, 1] * 63 / 255), 0, 63).astype(np.uint32)
    b = np.clip(np.rint(c[:, 2] * 31 / 255), 0, 31).astype(np.uint32)
    v = (r << 11) | (g << 5) | b
    rgb = np.stack([(r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)], 1).astype(np.float32)
    return v, rgb


def dxt1(rgb):
    """DXT1 blocks (opaque, 4-colour mode) of an H x W x 3 image (H, W multiples of 4)"""
    H, W, _ = rgb.shape
    blk = rgb.reshape(H // 4, 4, W // 4, 4, 3).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 3).astype(np.float32)
    n = blk.shape[0]
    mean = blk.mean(1)
    c = blk - mean[:, None]
    cov = np.einsum('nki,nkj->nij', c, c)
    v = np.ones((n, 3), np.float32)
    for _ in range(6):
        v = np.einsum('nij,nj->ni', cov, v)
        v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
    proj = np.einsum('nki,ni->nk', c, v)
    hi = np.clip(mean + proj.max(1)[:, None] * v, 0, 255)
    lo = np.clip(mean + proj.min(1)[:, None] * v, 0, 255)
    c0, p0 = _q565(hi)
    c1, p1 = _q565(lo)
    swap = c0 < c1
    c0, c1 = np.where(swap, c1, c0), np.where(swap, c0, c1)
    p0, p1 = np.where(swap[:, None], p1, p0), np.where(swap[:, None], p0, p1)
    pal = np.stack([p0, p1, (2 * p0 + p1) / 3, (p0 + 2 * p1) / 3], 1)          # n, 4, 3
    d = ((blk[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(-1)                # n, 16, 4
    idx = d.argmin(-1).astype(np.uint32)
    idx[c0 == c1] = 0
    bits = (idx << (2 * np.arange(16, dtype=np.uint32))).sum(1).astype(np.uint32)
    out = np.zeros((n, 2), np.uint32)
    out[:, 0] = c0 | (c1 << 16)
    out[:, 1] = bits
    return out.astype('<u4').tobytes()


def blp_dxt1(rgb):
    """BLP2, DXT1 without alpha, full mipmap chain"""
    from PIL import Image
    im = Image.fromarray(rgb, 'RGB')
    w, h = im.size
    mips = []
    while True:
        a = np.asarray(im, dtype=np.uint8)
        ph, pw = max(4, (a.shape[0] + 3) // 4 * 4), max(4, (a.shape[1] + 3) // 4 * 4)
        if (ph, pw) != a.shape[:2]:
            a = np.pad(a, ((0, ph - a.shape[0]), (0, pw - a.shape[1]), (0, 0)), mode='edge')
        mips.append(dxt1(a))
        if im.size == (1, 1):
            break
        im = im.resize((max(1, im.size[0] // 2), max(1, im.size[1] // 2)), Image.BOX)
    offs, sizes, pos = [], [], 148
    for m in mips[:16]:
        offs.append(pos)
        sizes.append(len(m))
        pos += len(m)
    offs += [0] * (16 - len(offs))
    sizes += [0] * (16 - len(sizes))
    hdr = b'BLP2' + struct.pack('<IBBBBII', 1, 2, 0, 0, 1, w, h) + struct.pack('<16I', *offs) + struct.pack('<16I', *sizes)
    return hdr + b''.join(mips[:16])
