"""T4: schemes (client side), the attacker, and the Guess / BucketGuess games.

The attacker knows S~, the scheme and the public estimate, so it evaluates |beta(c)| for every candidate c.
Guess list for a bucket b: candidates c with b in beta(c), ordered by p_att(c)/|beta(c)| desc, ties by p_att desc, then
lexicographic (candidate index order already encodes p_att desc, lexicographic).
"""
import numpy as np

from . import bucketizers as bz
from . import data, estimators


class FSB:
    """FSB with one or more estimator members; gamma = max over members of ceil(|B| p_k(w)/p_k(w_qbar,k)).
    members: list of (phat_fn(strings) -> probs, ph_S = the member's p^ over every password of S~)."""

    kind = "fsb"

    def __init__(self, members, qbar, bits):
        self.bits, self.B, self.qbar = bits, 1 << bits, qbar
        self.members = [(fn, estimators.kth_largest(ph_S, qbar)) for fn, ph_S in members]
        self.gamma_S = np.max([bz.fsb_gamma(ph_S, pq, self.B) for (_, ph_S), (_, pq) in zip(members, self.members)], axis=0)

    def gamma(self, strings):
        return np.max([bz.fsb_gamma(fn(strings), pq, self.B) for fn, pq in self.members], axis=0)

    def sizes(self, h_S):
        cov = bz.fsb_bucket_sizes(bz.f_of(h_S, self.bits), self.gamma_S, self.B)
        return float(cov.mean()), int(cov.max())


class FSBFloor(FSB):
    """Phase 1g: FSB with a lower bound on the number of copies, gamma(w) = min(|B|, max(gamma_FSB(w), floor)) for EVERY string.
    The floor depends only on the string (not on whether it is stored), so the client can compute it. floor = 1 is plain FSB."""

    def __init__(self, members, qbar, bits, floor):
        super().__init__(members, qbar, bits)
        self.floor = int(min(floor, self.B))
        self.gamma_S = np.maximum(self.gamma_S, self.floor)

    def gamma(self, strings):
        return np.maximum(super().gamma(strings), self.floor)


class HPB:
    kind = "hpb"

    def __init__(self, l):
        self.bits, self.B = l, 1 << l

    def gamma(self, strings):
        return np.ones(len(strings), np.int64)

    def sizes(self, h_S):
        c = bz.hpb_bucket_sizes(bz.f_of(h_S, self.bits), self.bits)
        return float(c.mean()), int(c.max())


class Attacker:
    """Candidate list = top n_cand unique passwords by attacker weight w (after an optional policy mask).
    w is the attacker's p_att up to a constant: leak counts ('emp') or the public estimate p^ ('est').
    Candidates are ordered by w desc, ties lexicographic; that order is the tie-break rank used by the lookup."""

    def __init__(self, pw, w, n_cand=2_000_000, keep=None, name=""):
        h_all = data.pool_hash(pw)
        idx = np.flatnonzero(keep) if keep is not None else np.arange(len(pw))
        wi = np.asarray(w, dtype=np.float64)[idx]
        if not (np.diff(wi) <= 0).all():
            idx = idx[np.lexsort((pw[idx], -wi))]
        w = np.asarray(w, dtype=np.float64)
        self.total = float(w[idx].sum())  # renormalised over the allowed set
        idx = idx[:n_cand]
        self.name, self.pw, self.cnt, self.h = name, pw[idx], w[idx], h_all[idx]
        self._o = np.argsort(self.pw)
        self._sorted = self.pw[self._o]
        self._ix = {}

    def p_att(self, i):
        return self.cnt[i] / self.total

    def rank_of(self, strings):
        """Candidate index of each string, or -2 if it is not a candidate."""
        j = np.searchsorted(self._sorted, strings)
        j[j == len(self._sorted)] = 0
        hit = self._sorted[j] == strings
        return np.where(hit, self._o[j], -2)

    def index(self, scheme, cache_key):
        k = (scheme.kind, cache_key)
        if k not in self._ix:
            g = scheme.gamma(self.pw)
            self._ix[k] = (bz.Index(bz.f_of(self.h, scheme.bits), g, self.cnt, scheme.B), g)
        return self._ix[k]


def play(att, scheme, cache_key, targets, rng, qs=(1, 10, 100, 1000), n_cand=None):
    """One repetition of both games on the same targets. Returns dict with success rates and diagnostics.
    n_cand restricts the candidate list (used for the 1M vs 2M check) by rebuilding the index on a prefix."""
    K = max(qs)
    h = data.salted_hash64(targets)
    f = bz.f_of(h, scheme.bits)
    g = scheme.gamma(targets)
    b = (f + rng.integers(0, g)) % scheme.B  # client picks one bucket uniformly from beta(w)
    ix, _ = att.index(scheme, cache_key)
    top, nh = ix.topk(b, K)
    tr = att.rank_of(targets)
    eq = top == tr[:, None]
    found = eq.any(1)
    pos = np.where(found, eq.argmax(1), K)
    out = {"bucket": {q: float((pos < q).mean()) for q in qs},
           "baseline": {q: float(((tr >= 0) & (tr < q)).mean()) for q in qs},
           "mean_cand_in_bucket": float(nh.mean()), "n_cand_in_bucket": nh, "b": b, "f": f, "gamma": g, "top": top, "tr": tr}
    return out
