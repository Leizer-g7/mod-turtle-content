"""Map Turtle (1.12-format) display IDs onto displays that exist in the 3.3.5 DBCs."""
import collections
from .dbc import load


def _L(p):
    n, f, rs, rows, s, _ = load(p)
    return {r[0]: r for r in rows}, s


def _norm(p):
    return p.lower().replace('/', '\\').replace('.mdx', '').replace('.m2', '').replace('.mdl', '')


class Displays:
    def __init__(self, tw_dbc, ac_dbc):
        self.tcdi, self.tcs = _L(tw_dbc + '/CreatureDisplayInfo.dbc')
        self.tcmd, self.tcms = _L(tw_dbc + '/CreatureModelData.dbc')
        self.tx, _ = _L(tw_dbc + '/CreatureDisplayInfoExtra.dbc')
        self.wcdi, self.wcs = _L(ac_dbc + '/CreatureDisplayInfo.dbc')
        self.wcmd, self.wcms = _L(ac_dbc + '/CreatureModelData.dbc')
        self.wx, _ = _L(ac_dbc + '/CreatureDisplayInfoExtra.dbc')
        self.tg, self.tgs = _L(tw_dbc + '/GameObjectDisplayInfo.dbc')
        self.wg, self.wgs = _L(ac_dbc + '/GameObjectDisplayInfo.dbc')
        self.ti, self.tis = _L(tw_dbc + '/ItemDisplayInfo.dbc')
        self.wi, self.wis = _L(ac_dbc + '/ItemDisplayInfo.dbc')
        self.wcdi_by_sig = collections.defaultdict(list)
        self.wcdi_by_model = collections.defaultdict(list)
        for k, r in self.wcdi.items():
            if r[3] == 0:
                sig = self._csig(r, self.wcs, self.wcmd, self.wcms)
                self.wcdi_by_sig[sig].append(k)
                self.wcdi_by_model[sig[0]].append(k)
        self.wcdi_by_extra = {r[3]: k for k, r in self.wcdi.items() if r[3]}
        self.wx_by_race_sex = collections.defaultdict(list)
        for eid, we in self.wx.items():
            if eid in self.wcdi_by_extra:
                self.wx_by_race_sex[(we[1], we[2])].append(eid)
        self.wg_by_sig = collections.defaultdict(list)
        for k, r in self.wg.items():
            self.wg_by_sig[_norm(self.wgs(r[1]))].append(k)
        self.wi_by_sig = collections.defaultdict(list)
        self.wi_by_icon = collections.defaultdict(list)
        for k, r in self.wi.items():
            self.wi_by_sig[self._isig(r, self.wis)].append(k)
            self.wi_by_icon[self.wis(r[5]).lower()].append(k)

    @staticmethod
    def _csig(r, s, cmd, ms):
        m = cmd.get(r[1])
        return (_norm(ms(m[2])) if m else '?', tuple(s(r[i]).lower() for i in (6, 7, 8)))

    @staticmethod
    def _isig(r, s):
        return tuple(_norm(s(r[i])) for i in (1, 2, 3, 4, 5) + tuple(range(15, 23)))

    def creature(self, d):
        """-> (display_for_335 or None, status) status in same|remap|substitute|none|missing"""
        t = self.tcdi.get(d)
        if not t:
            return None, 'missing'
        w = self.wcdi.get(d)
        if t[3] == 0:
            sig = self._csig(t, self.tcs, self.tcmd, self.tcms)
            if w and w[3] == 0 and self._csig(w, self.wcs, self.wcmd, self.wcms) == sig:
                return d, 'same'
            if self.wcdi_by_sig.get(sig):
                return min(self.wcdi_by_sig[sig]), 'remap'
            if self.wcdi_by_model.get(sig[0]):
                return min(self.wcdi_by_model[sig[0]]), 'substitute'
            return None, 'none'
        te = self.tx.get(t[3])
        if not te:
            return None, 'none'
        if w and w[3]:
            we = self.wx.get(w[3])
            if we and list(we[1:17]) == list(te[1:17]):
                return d, 'same'
        best, bscore = None, -1
        for eid in self.wx_by_race_sex.get((te[1], te[2]), []):
            we = self.wx[eid]
            score = sum(3 for a, b in zip(te[8:17], we[8:17]) if a and a == b)
            score += sum(1 for i in range(3, 8) if we[i] == te[i])
            if score > bscore:
                best, bscore = eid, score
        if best is None:
            return None, 'none'
        disp = self.wcdi_by_extra[best]
        return disp, ('remap' if list(self.wx[best][1:17]) == list(te[1:17]) else 'substitute')

    def gameobject(self, d):
        t = self.tg.get(d)
        if not t:
            return None, 'missing'
        sig = _norm(self.tgs(t[1]))
        if d in self.wg and _norm(self.wgs(self.wg[d][1])) == sig:
            return d, 'same'
        if self.wg_by_sig.get(sig):
            return min(self.wg_by_sig[sig]), 'remap'
        return None, 'needs-client-patch:' + self.tgs(t[1])

    def item(self, d):
        t = self.ti.get(d)
        if not t:
            return None, 'missing'
        sig = self._isig(t, self.tis)
        if d in self.wi and self._isig(self.wi[d], self.wis) == sig:
            return d, 'same'
        if self.wi_by_sig.get(sig):
            return min(self.wi_by_sig[sig]), 'remap'
        ic = self.tis(t[5]).lower()
        if self.wi_by_icon.get(ic):
            return min(self.wi_by_icon[ic]), 'icon-only'
        return None, 'nomatch:' + ic
