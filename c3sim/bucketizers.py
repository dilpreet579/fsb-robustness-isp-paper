"""T3: HPB / FSB bucket maps, exact bucket sizes, and the sorted-class lookup.

Bucket of a password under FSB: the circular range [f, f+gamma-1] mod |B|. HPB is the same machine with
gamma = 1 and |B| = 2^l (f = first l bits of the hash).

Lookup (answering "which candidates c have bucket b in beta(c)?"): group candidates by distinct gamma, keep each
group's f values sorted, and for a query bucket b binary-search the circular window [b-gamma+1, b] in every group.
Cost is (#groups x log n) per query, never a scan of the leak.
"""
import numpy as np
from numba import njit, prange


def f_of(h64, bits):
    """First `bits` bits of the 64-bit salted hash, as int64."""
    return (h64 >> np.uint64(64 - bits)).astype(np.int64)


def fsb_gamma(ph, p_q, B):
    """gamma(w) = min(|B|, ceil(|B| p^(w) / p^(w_qbar)))."""
    return np.minimum(np.ceil(B * ph / p_q), B).astype(np.int64)


def fsb_bucket_sizes(f, gamma, B):
    """Exact per-bucket coverage by a difference array over the circular ranges. Returns int64[B]."""
    end = f + gamma
    wrap = end > B
    d = np.bincount(f, minlength=B + 1).astype(np.int64)
    d -= np.bincount(np.where(wrap, B, end), minlength=B + 1)  # non-wrapping range closes at `end`
    d[0] += int(wrap.sum())  # wrapping range also covers [0, end-B-1]
    d -= np.bincount((end - B)[wrap], minlength=B + 1)
    return np.cumsum(d)[:B]


def hpb_bucket_sizes(prefix, l):
    return np.bincount(prefix, minlength=1 << l)


@njit(cache=True)
def _lb(F, lo, hi, x):
    while lo < hi:
        mid = (lo + hi) >> 1
        if F[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


@njit(cache=True)
def _span(F, s, e, b, g, B):
    """Positions in group [s, e) with f in the circular window [b-g+1, b]: returns (lo1, hi1, lo2, hi2)."""
    a = b - g + 1
    if a >= 0:
        return _lb(F, s, e, a), _lb(F, s, e, b + 1), 0, 0
    return s, _lb(F, s, e, b + 1), _lb(F, s, e, B + a), e


@njit(cache=True)
def _hits(F, gstart, gval, I, S, b, B):
    n = 0
    for g in range(len(gval)):
        l1, h1, l2, h2 = _span(F, gstart[g], gstart[g + 1], b, gval[g], B)
        n += (h1 - l1) + (h2 - l2)
    ids = np.empty(n, np.int32)
    sc = np.empty(n)
    k = 0
    for g in range(len(gval)):
        l1, h1, l2, h2 = _span(F, gstart[g], gstart[g + 1], b, gval[g], B)
        for j in range(l1, h1):
            ids[k] = I[j]
            sc[k] = S[j]
            k += 1
        for j in range(l2, h2):
            ids[k] = I[j]
            sc[k] = S[j]
            k += 1
    return ids, sc


@njit(parallel=True, cache=True)
def _topk(F, gstart, gval, I, S, bs, B, K, out, nh):
    for qi in prange(len(bs)):
        ids, sc = _hits(F, gstart, gval, I, S, bs[qi], B)
        o = np.argsort(ids)  # index order = (p_att desc, lexicographic) so a stable sort on score breaks ties right
        ids = ids[o]
        sc = sc[o]
        o2 = np.argsort(-sc, kind="mergesort")
        m = min(K, len(ids))
        for j in range(m):
            out[qi, j] = ids[o2[j]]
        for j in range(m, K):
            out[qi, j] = -1
        nh[qi] = len(ids)


class Index:
    """Candidate lookup. f, gamma: per-candidate start bucket and replication; w: attacker weight (count).
    Candidates must be given in guess-priority order (p_att desc, then lexicographic), so index = tie-break rank."""

    def __init__(self, f, gamma, w, B):
        self.B = int(B)
        o = np.lexsort((f, gamma))
        self.F = np.ascontiguousarray(f[o], dtype=np.int64)
        gs = gamma[o]
        self.I = o.astype(np.int32)
        self.S = np.ascontiguousarray(w[o] / gs, dtype=np.float64)  # score = p_att / |beta| (constant factor dropped)
        cut = np.flatnonzero(np.diff(gs)) + 1
        self.gstart = np.r_[0, cut, len(gs)].astype(np.int64)
        self.gval = gs[self.gstart[:-1]].astype(np.int64)

    def topk(self, buckets, K=1000):
        """Top-K candidate indices per bucket (-1 padded) and the number of candidates in each bucket."""
        buckets = np.ascontiguousarray(buckets, dtype=np.int64)
        out = np.empty((len(buckets), K), np.int32)
        nh = np.empty(len(buckets), np.int64)
        _topk(self.F, self.gstart, self.gval, self.I, self.S, buckets, self.B, K, out, nh)
        return out, nh

    def hits(self, b):
        """Indices (sorted) of all candidates whose bucket range contains b."""
        ids, _ = _hits(self.F, self.gstart, self.gval, self.I, self.S, int(b), self.B)
        return np.sort(ids)
