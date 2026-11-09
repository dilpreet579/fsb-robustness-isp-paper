"""Phase 1f: target grouping, bin helpers and the tail-only noise member."""
import numpy as np

from experiments import e1f_mechanism as M
from experiments import e1f_tailnoise as TN


def test_group_of_head_tail_none():
    idx = np.array([0, 999_999, 1_000_000, 5_000_000, -1])
    assert M.group_of(idx, 1_000_000).tolist() == [0, 0, 1, 1, 2]  # head = rank < t; tail = stored, not head; none = not in S~


def test_bins_cover_every_value_and_isolate_the_extremes():
    B = 1 << 24
    g = np.array([1, 2, 10, 11, 100, 101, 1000, 1001, 10_000, 10_001, 100_000, 100_001, 1_000_000, 1_000_001, B - 1, B])
    b = M.gamma_bin(g, B)
    assert b.tolist() == [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8]
    assert len(M.GAMMA_LABELS) == 9 and b.max() == 8
    c = M.count_bin(np.array([0, 1, 2, 3, 5, 6, 20, 21, 100, 101, 1000, 1001, 10_000, 10_001]))
    assert c.tolist() == [0, 1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8] and len(M.COUNT_LABELS) == 9


def test_group_contributions_sum_to_total_loss():
    rng = np.random.default_rng(0)
    n = 5000
    grp = rng.integers(0, 3, n)
    base = rng.random(n) < 0.05
    succ = base | (rng.random(n) < 0.15)
    parts = sum((succ[grp == g].sum() - base[grp == g].sum()) / n for g in range(3))
    assert abs(parts - (succ.mean() - base.mean())) < 1e-12  # loss contribution = share * (success - baseline), summed over groups


def test_tail_member_leaves_head_untouched_and_scales_the_rest(corpora):
    from experiments import common as C
    w = C.World(t=100_000, n_cand=200_000)
    salt = b"c3sim-noise-v1-d1"
    fn, ph = TN.tail_member(w, 1.0, salt)
    assert (ph[: w.t] == w.ph_S[: w.t]).all()  # head rows exactly p^
    z = w._zs[salt]
    assert np.allclose(ph[w.t:], w.ph_S[w.t:] * np.exp(z[w.t:]), rtol=1e-12)
    idx = np.r_[0:50, w.t - 5:w.t + 50, 5_000_000:5_000_030]
    assert np.allclose(fn(w.pw[idx]), ph[idx], rtol=1e-9)  # the string-level function agrees with the S~ array on head and tail rows
