import numpy as np

from c3sim import data, estimators

QBARS = [1, 10, 100, 1000, 10000]


def _random_strings(n, seed):
    r = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        L = int(r.integers(1, 31))
        out.append(bytes(r.integers(32, 127, L).astype(np.uint8)))
    return np.array(out, dtype="S30")


def test_probabilities_finite_positive_10k_sample(sp, est):
    pw, cnt = sp["A_train"]
    r = np.random.default_rng(0)
    s = np.concatenate([pw[r.choice(len(pw), 5000, p=cnt / cnt.sum())],  # frequency weighted
                        pw[r.choice(len(pw), 2000)],                     # uniform over unique
                        _random_strings(3000, 1)])                       # arbitrary strings, not in S~
    assert len(s) == 10_000
    p = est.phat(s)
    print(f"[T2] 10k sample: min={p.min():.3e} max={p.max():.3e} all finite={np.isfinite(p).all()} all>0={(p > 0).all()}")
    assert np.isfinite(p).all() and (p > 0).all()


def test_trigram_rows_normalised(est):
    # every (u,v) context is a distribution over the 96 next symbols; also for KN
    for lt in (est.lt, estimators.trigram_table(*data.splits()["A_train"], smoothing="kn")):
        s = np.exp(lt).sum(2)
        print(f"[T2] row-sum range over 97x97 contexts: {s.min():.12f} .. {s.max():.12f}")
        assert np.allclose(s, 1.0, atol=1e-9)


def test_top1000_hist_mass_matches_empirical(sp, est):
    pw, cnt = sp["A_train"]
    got = est.phat(pw[:1000]).sum()
    want = cnt[:1000].sum() / cnt.sum()
    ngram_only = est.p_n(pw[:1000]).sum()
    print(f"[T2] top-1000 mass: p^={got:.6f} empirical={want:.6f}  (3-gram alone would give {ngram_only:.6f})")
    assert abs(got - want) < 1e-12


def test_fast_path_equals_general_path(sp, est):
    pw, _ = sp["A_train"]
    idx = np.r_[0:2000, np.random.default_rng(1).choice(len(pw), 20000)]
    assert np.allclose(est.phat(pw[idx]), est.phat_ranked(pw)[idx], rtol=1e-12)


def test_phat_at_wqbar_positive_and_mass_sane(sp, est):
    pw, cnt = sp["A_train"]
    ph = est.phat_ranked(pw)
    print(f"[T2] sum of p^ over S~ = {ph.sum():.6f} (must be <= 1); t={est.t}, scale={est.scale:.6f}, "
          f"3-gram mass on top-t = {est.pn_top_mass:.6f}")
    assert 0 < ph.sum() <= 1.0 + 1e-9
    for q in QBARS:
        pq = estimators.kth_largest(ph, q)
        print(f"[T2] qbar={q:>6}: p^(w_qbar)={pq:.4e}  (hist rank-{q} p={cnt[q - 1] / cnt.sum():.4e})")
        assert pq > 0 and np.isfinite(pq)


def test_tail_never_outranks_hist_head(sp, est):
    # w_qbar is defined over S~; make sure no tail password has a larger p^ than the t-th histogram entry
    pw, _ = sp["A_train"]
    ph = est.phat_ranked(pw)
    print(f"[T2] max tail p^ = {ph[est.t:].max():.3e}, smallest head p^ = {ph[est.t - 1]:.3e}, "
          f"#tail > head-min = {(ph[est.t:] > ph[est.t - 1]).sum()}")
