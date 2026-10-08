"""T2: password-probability estimates p^ (histogram on the top t, character 3-gram elsewhere).

p^ is defined for ANY string over printable ASCII (length 1..30 is not enforced by the 3-gram; the model is a proper
distribution over strings because EOS is a symbol). Client and attacker both evaluate it.

Smoothing choices for the 3-gram p_n (trained on S~, weighted by counts):
  'adddelta': plain trigram, add-delta (delta=0.01), no back-off. This is the BASE model.
  'kn':       interpolated Kneser-Ney (D=0.75): trigram counts weighted by password counts, lower orders on
              continuation (type) counts. This is the E3 `smoothed` variant.
"""
import numpy as np
from numba import njit

from . import data

V = 96  # 95 printable chars (ids 0..94) + EOS (95)
BOS = 96  # context-only symbol


@njit(cache=True)
def _count(a, cnt, c3):
    for i in range(a.shape[0]):
        u = 96
        v = 96
        w_ = float(cnt[i])
        for j in range(31):
            ch = 95 if (j == 30 or a[i, j] == 0) else a[i, j] - 32
            c3[u, v, ch] += w_
            if ch == 95:
                break
            u = v
            v = ch


@njit(cache=True)
def _logp(a, lt, out):
    for i in range(a.shape[0]):
        u = 96
        v = 96
        s = 0.0
        for j in range(31):
            ch = 95 if (j == 30 or a[i, j] == 0) else a[i, j] - 32
            s += lt[u, v, ch]
            if ch == 95:
                break
            u = v
            v = ch
        out[i] = s


def _u8(pw):
    return np.ascontiguousarray(pw).view(np.uint8).reshape(len(pw), data.W)


def trigram_table(pw, cnt, smoothing="adddelta", delta=0.01, D=0.75):
    """Log-probability table lt[u, v, w] (97 x 97 x 96)."""
    c3 = np.zeros((97, 97, V))
    _count(_u8(pw), cnt.astype(np.int64), c3)
    if smoothing == "adddelta":
        p = (c3 + delta) / (c3.sum(2, keepdims=True) + V * delta)
    elif smoothing == "kn":
        # level 1: continuation counts of the symbol w over distinct (v) contexts
        cc2 = (c3 > 0).sum(0).astype(float)  # [v, w]: number of distinct u before (v, w)
        cc2[BOS] = c3[BOS, BOS]  # first character: use real counts
        cc1 = (cc2 > 0).sum(0).astype(float)
        p1 = (cc1 + 1e-3) / (cc1.sum() + V * 1e-3)
        s2 = cc2.sum(1, keepdims=True)
        nz2 = (cc2 > 0).sum(1, keepdims=True)
        p2 = np.where(s2 > 0, (np.maximum(cc2 - D, 0) + D * nz2 * p1[None]) / np.maximum(s2, 1e-300), p1[None])
        s3 = c3.sum(2, keepdims=True)
        nz3 = (c3 > 0).sum(2, keepdims=True)
        p = np.where(s3 > 0, (np.maximum(c3 - D, 0) + D * nz3 * p2[None]) / np.maximum(s3, 1e-300), p2[None])
    else:
        raise ValueError(smoothing)
    return np.log(p)


class Estimator:
    """p^_s built from a leak (pw sorted count desc, cnt). t = size of the histogram head."""

    def __init__(self, pw, cnt, t=100_000, smoothing="adddelta"):
        assert (np.diff(cnt) <= 0).all(), "corpus must be sorted by count desc"
        self.t, self.smoothing = min(t, len(pw)), smoothing
        self.total = float(cnt.sum())
        self.lt = trigram_table(pw, cnt, smoothing)
        top = pw[: self.t]
        self.hist_p = cnt[: self.t] / self.total
        o = np.argsort(top)
        self.top_sorted, self.top_p_sorted = top[o], self.hist_p[o]
        self.pn_top_mass = float(self.p_n(top).sum())
        self.scale = (1.0 - self.hist_p.sum()) / (1.0 - self.pn_top_mass)

    def p_n(self, strings):
        out = np.empty(len(strings))
        _logp(_u8(strings), self.lt, out)
        return np.exp(out)

    def phat(self, strings):
        """p^(w) for any array of strings."""
        pn = self.p_n(strings) * self.scale
        i = np.searchsorted(self.top_sorted, strings)
        i[i == len(self.top_sorted)] = 0
        hit = self.top_sorted[i] == strings
        pn[hit] = self.top_p_sorted[i[hit]]
        return pn

    def phat_head(self, strings):
        """Like phat, also returns the mask of strings that are in the histogram head."""
        pn = self.p_n(strings) * self.scale
        i = np.searchsorted(self.top_sorted, strings)
        i[i == len(self.top_sorted)] = 0
        hit = self.top_sorted[i] == strings
        pn[hit] = self.top_p_sorted[i[hit]]
        return pn, hit

    def phat_ranked(self, pw):
        """Fast path for the leak itself (rows sorted by count desc): head rows are the histogram."""
        out = self.p_n(pw) * self.scale
        out[: self.t] = self.hist_p
        return out


def kth_largest(x, k):
    """k-th largest value of x (1-based)."""
    return np.partition(x, len(x) - k)[len(x) - k]
