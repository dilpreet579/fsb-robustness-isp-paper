import numpy as np

from c3sim import bucketizers as bz


def _toy(n=50_000, bits=14, seed=0):
    r = np.random.default_rng(seed)
    B = 1 << bits
    f = r.integers(0, B, n)
    # Zipf-ish weights, sorted desc (index = priority); gamma mixes 1, mid, and full replication
    w = np.floor(1e6 / np.arange(1, n + 1) ** 1.1) + 1
    gamma = np.minimum(np.ceil(B * (w / w[200])), B).astype(np.int64)
    return B, f, gamma, w


def test_fast_lookup_equals_naive_scan_1000_buckets():
    B, f, gamma, w = _toy()
    ix = bz.Index(f, gamma, w, B)
    bs = np.random.default_rng(1).integers(0, B, 1000)
    top, nh = ix.topk(bs, K=50)
    for k, b in enumerate(bs):
        naive = np.flatnonzero(((b - f) % B) < gamma)  # naive scan with wrap-around
        assert (ix.hits(b) == naive).all()
        assert nh[k] == len(naive)
        order = np.lexsort((naive, -(w[naive] / gamma[naive])))[:50]  # score desc, then index asc
        want = naive[order]
        assert (top[k][: len(want)] == want).all() and (top[k][len(want):] == -1).all()
    print(f"[T3] 1000 random buckets: fast lookup == naive scan (hit sets and top-50 order); "
          f"mean hits/bucket={nh.mean():.1f}, groups={len(ix.gval)}")


def test_bucket_sizes_difference_array_matches_brute_force_and_formula():
    B, f, gamma, w = _toy(n=3000, bits=10)
    cov = bz.fsb_bucket_sizes(f, gamma, B)
    brute = np.zeros(B, int)
    for s, g in zip(f, gamma):
        brute[(s + np.arange(g)) % B] += 1
    assert (cov == brute).all()
    assert cov.sum() == gamma.sum() and cov.mean() == gamma.sum() / B
    print(f"[T3] 3k-password toy: difference array == brute force; avg size {cov.mean():.3f} == sum(gamma)/|B| "
          f"{gamma.sum() / B:.3f}; max {cov.max()}")


def test_avg_fsb_bucket_equals_sum_gamma_over_B_50k():
    B, f, gamma, w = _toy()
    cov = bz.fsb_bucket_sizes(f, gamma, B)
    assert cov.sum() == gamma.sum()
    print(f"[T3] 50k toy: avg FSB bucket size {cov.mean():.4f} vs sum(gamma)/|B| {gamma.sum() / B:.4f}; max {cov.max()}")


def test_hpb_is_gamma1_special_case():
    B, f, gamma, w = _toy(bits=10)
    l = 6
    pre = f >> (10 - l)
    ix = bz.Index(pre, np.ones(len(pre), np.int64), w, 1 << l)
    for b in range(1 << l):
        assert (ix.hits(b) == np.flatnonzero(pre == b)).all()
    assert (bz.hpb_bucket_sizes(pre, l) == np.bincount(pre, minlength=1 << l)).all()
