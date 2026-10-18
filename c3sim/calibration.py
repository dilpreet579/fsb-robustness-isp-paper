"""Phase 1b fix: calibrate the 3-gram TAIL of p^ against held-out data.

Problem (REPORT D1/D9): the tail estimate p_n * scale is badly mis-scaled (median leaked tail password gets 5e-5 of its empirical
frequency; short strings like '12' get 1e-3). The client must evaluate p^ on any string, so the correction has to be a public function
of the string alone, not of membership in the leak.

Method (cross-fit): split A_train accounts 90/10 (Binomial per password). Fit the histogram head + 3-gram on the 90% part.
In each log10(p^) bin, factor r = (held-out tail mass in the bin) / (model tail mass in the bin). Model mass comes from sampling the
3-gram (the exact histogram-head strings are excluded by hash). The factor is then applied to the tail p^ of the estimator trained on
ALL of A_train. Head probabilities (top t by count) are unchanged. Variants: bin width, and isotonic (monotone) regression of the
calibrated value on p^.
"""
import numpy as np
from numba import njit

from . import data, estimators

LO, HI = -60.0, -1.0  # log10 p^ range; values outside are clipped into the end bins
SEED_CAL = 104


@njit(cache=True)
def _sample(cdf, lt, n, seed, lp, hs):
    """Ancestral samples from the trigram. lp = log p_n of the sample, hs = polynomial hash of its characters (mod 2^64)."""
    np.random.seed(seed)
    for i in range(n):
        u = 96
        v = 96
        s = 0.0
        h = np.uint64(1469598103934665603)
        for j in range(31):
            r = np.random.random()
            row = cdf[u, v]
            lo, hi = 0, 95
            while lo < hi:  # first k with row[k] > r
                mid = (lo + hi) >> 1
                if row[mid] > r:
                    hi = mid
                else:
                    lo = mid + 1
            ch = lo
            s += lt[u, v, ch]  # exact log-prob (differences of the cdf lose precision for tiny probabilities)
            if ch == 95 or j == 30:
                break
            h = (h ^ np.uint64(ch + 1)) * np.uint64(1099511628211)
            u = v
            v = ch
        lp[i] = s
        hs[i] = h


@njit(cache=True)
def _hash_rows(a, hs):
    for i in range(a.shape[0]):
        h = np.uint64(1469598103934665603)
        for j in range(30):
            if a[i, j] == 0:
                break
            h = (h ^ np.uint64(a[i, j] - 32 + 1)) * np.uint64(1099511628211)
        hs[i] = h


def _hashes(pw):
    out = np.empty(len(pw), np.uint64)
    _hash_rows(estimators._u8(pw), out)
    return out


def _bin(ph, width):
    nb = int(round((HI - LO) / width))
    return np.clip(np.floor((np.log10(ph) - LO) / width).astype(np.int64), 0, nb - 1), nb


def _pav(y, w):
    """Weighted pool-adjacent-violators, non-decreasing fit."""
    blocks = []  # [value, weight, count]
    for yi, wi in zip(y, w):
        blocks.append([yi, wi, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            (v2, w2, c2), (v1, w1, c1) = blocks[-1], blocks[-2]
            blocks[-2:] = [[(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, c1 + c2]]
    return np.concatenate([[b[0]] * b[2] for b in blocks])


class Calibrator:
    def __init__(self, est_full, width, r, table):
        self.est, self.width, self.r, self.table = est_full, width, r, table

    def phat(self, strings):
        ph, head = self.est.phat_head(strings)
        b, _ = _bin(ph, self.width)
        return np.where(head, ph, ph * self.r[b])

    def phat_ranked(self, pw):
        ph = self.est.phat_ranked(pw)
        t = self.est.t
        b, _ = _bin(ph[t:], self.width)
        ph[t:] *= self.r[b]
        return ph


def fit(world, width=0.5, iso=False, n_samples=20_000_000, seed=SEED_CAL):
    """Fit calibration factors from world.pw/world.cnt (= A_train only) and return a Calibrator around world.est."""
    pw, cnt, t, smoothing = world.pw, world.cnt, world.t, world.est.smoothing
    c_fit, c_cal = data.binom_split(cnt, 0.9, seed)
    m = c_fit > 0
    pw_fit, c_fit = data.sort_corpus(pw[m], c_fit[m])
    est = estimators.Estimator(pw_fit, c_fit, t=t, smoothing=smoothing)
    # held-out tail mass per bin
    k = c_cal > 0
    cal_pw, cal_c = pw[k], c_cal[k]
    ph, head = est.phat_head(cal_pw)
    b, nb = _bin(ph[~head], width)
    tot = float(c_cal.sum())
    true = np.bincount(b, weights=cal_c[~head], minlength=nb) / tot
    # model tail mass per bin, by sampling; exclude the histogram head exactly (hash match)
    lp, hs = np.empty(n_samples), np.empty(n_samples, np.uint64)
    cdf = np.cumsum(np.exp(est.lt), axis=2)
    _sample(cdf, est.lt, n_samples, seed, lp, hs)
    nonhead = ~np.isin(hs, _hashes(est.top_sorted))
    bm, _ = _bin(np.exp(lp[nonhead]) * est.scale, width)
    model = est.scale * np.bincount(bm, minlength=nb) / n_samples
    eps = 0.5 / tot  # half a held-out account per bin, so no factor is exactly zero
    r = np.where(model > 0, (true + eps) / np.maximum(model, 1e-300), 1.0)
    centre = 10.0 ** (LO + (np.arange(nb) + 0.5) * width)
    if iso:  # monotone calibrated value g(p^) = r * centre
        g = _pav(r * centre, model + 1e-300)
        r = g / centre
    table = dict(bin_log10_lo=LO + np.arange(nb) * width, held_out_tail_mass=true, model_tail_mass=model, factor=r,
                 n_held_out_tail_passwords=np.bincount(b, minlength=nb))
    return Calibrator(world.est, width, r, table)
