"""T4: games on a toy distribution with a known answer."""
import numpy as np

from c3sim import attacker, data


def _toy_world(n=300_000, a=1.0, seed=0):
    """Zipf(a) over n synthetic passwords; exact probabilities known. Counts are scaled integers (sorted desc)."""
    p = 1.0 / np.arange(1, n + 1) ** a
    p /= p.sum()
    pw = np.array([b"w%07d" % i for i in range(n)], dtype="S30")
    cnt = np.maximum(np.round(p * 1e10), 1).astype(np.int64)
    return pw, cnt, p


class _Exact:
    """Server estimate = the true distribution (so Theorem 5.1(1) applies). phat is a lookup by string."""

    def __init__(self, pw, p):
        self.o = np.argsort(pw)
        self.s = pw[self.o]
        self.p = p[self.o]

    def __call__(self, strings):
        j = np.searchsorted(self.s, strings)
        j[j == len(self.s)] = 0
        return np.where(self.s[j] == strings, self.p[j], 1e-30)


def test_baseline_equals_top_q_mass_within_sampling_error():
    pw, cnt, p = _toy_world()
    att = attacker.Attacker(pw, cnt, n_cand=len(pw))
    rng = np.random.default_rng(1)
    n = 40_000
    t = pw[rng.choice(len(pw), n, p=p)]
    tr = att.rank_of(t)
    for q in (1, 10, 100, 1000):
        got = float(((tr >= 0) & (tr < q)).mean())
        want = float(p[:q].sum())
        sd = np.sqrt(want * (1 - want) / n)
        print(f"[T4] baseline q={q:>4}: empirical {got:.4f} vs exact top-q mass {want:.4f} (sd {sd:.4f}, z={(got - want) / sd:+.2f})")
        assert abs(got - want) < 4 * sd


def test_fsb_no_loss_below_qbar_and_hpb_large_loss_toy():
    pw, cnt, p = _toy_world()
    att = attacker.Attacker(pw, cnt, n_cand=len(pw))
    ph = p  # exact estimate for every password in S~ (rows are sorted desc already)
    bits = 19  # |B| = 524288 >= N
    fsb = attacker.FSB([(_Exact(pw, p), ph)], qbar=100, bits=bits)
    hpb = attacker.HPB(l=9)
    n = 20_000
    rng = np.random.default_rng(2)
    t = pw[rng.choice(len(pw), n, p=p)]
    r_f = attacker.play(att, fsb, "x", t, np.random.default_rng(3))
    r_h = attacker.play(att, hpb, "x", t, np.random.default_rng(3))
    avg_f, _ = fsb.sizes(att.h)
    avg_h, _ = hpb.sizes(att.h)
    print(f"[T4] toy Zipf(1.0) N={len(pw):,}; FSB qbar=100 avg bucket {avg_f:.0f}; HPB l=9 avg bucket {avg_h:.0f}")
    for q in (1, 10, 100, 1000):
        lf = r_f["bucket"][q] - r_f["baseline"][q]
        lh = r_h["bucket"][q] - r_h["baseline"][q]
        print(f"[T4]   q={q:>4}: baseline {r_f['baseline'][q]:.3f}  FSB loss {lf:+.3f}  HPB loss {lh:+.3f}")
        if q <= 100:
            assert abs(lf) < 0.012  # Theorem 5.1(1): no loss for q <= qbar (4 sd at n=20k is ~0.014)
    assert r_h["bucket"][1000] - r_h["baseline"][1000] > 0.10
