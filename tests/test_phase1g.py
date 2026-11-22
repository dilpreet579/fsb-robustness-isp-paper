"""Phase 1g: the gamma floor (FSBFloor) on a toy distribution; no corpora needed."""
import numpy as np

from c3sim import attacker as atk
from c3sim import bucketizers as bz


def toy(n=3000, bits=8):
    pw = np.array([f"p{i:05d}".encode() for i in range(n)])  # sorted by construction, so searchsorted finds every string
    ph = 1.0 / (np.arange(n) + 1) ** 1.3
    ph /= ph.sum()
    fn = lambda s: ph[np.searchsorted(pw, s)]  # noqa: E731
    h = np.random.default_rng(1).integers(0, 2 ** 63, n, dtype=np.uint64) << np.uint64(1)
    return pw, ph, fn, h, bits


def test_good_turing_weights_adjust_small_counts_only():
    from types import SimpleNamespace

    from experiments import common as C
    cnt = np.array([100, 10, 3, 3, 2, 2, 2, 1, 1, 1, 1])  # n1 = 4, n2 = 3, n3 = 2
    w = C.World.gt_weights(SimpleNamespace(cnt=cnt), rmax=2)
    assert np.allclose(w[cnt == 1], 2 * 3 / 4) and np.allclose(w[cnt == 2], 3 * 2 / 3)  # Turing r* = (r+1) n_{r+1} / n_r
    assert (w[cnt > 2] == cnt[cnt > 2]).all()  # counts above rmax stay raw


def test_floor_one_is_plain_fsb():
    pw, ph, fn, h, bits = toy()
    a, b = atk.FSB([(fn, ph)], 10, bits), atk.FSBFloor([(fn, ph)], 10, bits, 1)
    assert (a.gamma_S == b.gamma_S).all() and (a.gamma(pw) == b.gamma(pw)).all() and a.sizes(h) == b.sizes(h)


def test_floor_is_a_lower_bound_capped_at_B_and_never_lowers_gamma():
    pw, ph, fn, h, bits = toy()
    base = atk.FSB([(fn, ph)], 10, bits)
    for g in (2, 7, 64, 255, 256, 10_000):
        s = atk.FSBFloor([(fn, ph)], 10, bits, g)
        want = np.maximum(base.gamma(pw), min(g, s.B))
        assert (s.gamma(pw) == want).all() and (s.gamma_S == want).all()
        assert s.gamma(pw).min() >= min(g, s.B) and s.gamma(pw).max() <= s.B


def test_average_bucket_equals_sum_gamma_over_B():
    pw, ph, fn, h, bits = toy()
    s = atk.FSBFloor([(fn, ph)], 10, bits, 40)
    assert abs(s.sizes(h)[0] - s.gamma_S.sum() / s.B) < 1e-9


def test_lookup_equals_naive_scan_with_a_floor():
    pw, ph, fn, h, bits = toy()
    s = atk.FSBFloor([(fn, ph)], 10, bits, 40)
    f, g = bz.f_of(h, bits), s.gamma_S
    ix = bz.Index(f, g, np.ones(len(pw)), s.B)
    for b in range(0, s.B, 7):
        naive = np.flatnonzero(((b - f) % s.B) < g)  # b in the circular range [f, f+gamma-1]
        assert (ix.hits(b) == naive).all()
