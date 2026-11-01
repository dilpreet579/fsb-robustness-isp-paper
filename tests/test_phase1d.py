"""Phase 1d: the sigma_hat estimator recovers a known dispersion through Poisson noise; noise draws are independent."""
import numpy as np

from c3sim import data, esterror


def _simulate(sigma, n=400_000, seed=0):
    rng = np.random.default_rng(seed)
    m = rng.uniform(0.2, 3.0, n)  # expected held-out counts under p^ (tiny counts: where log(c/m) would be badly inflated)
    c = rng.poisson(m * np.exp(rng.normal(-sigma ** 2 / 2, sigma, n)))
    return np.zeros(n, np.int64), c, m


def test_moment_estimator_recovers_known_sigma_and_null():
    for sigma in (0.0, 0.5, 1.0):
        b, c, m = _simulate(sigma)
        st = esterror.moment_by_bin(b, c, m, 1)
        got = float(st["sigma2"][0]) ** 0.5
        print(f"[1d] true sigma {sigma}: moment estimate {got:.3f}")
        assert abs(got - sigma) < 0.08
    # the naive log(c/m) over counts > 0 is badly off at these counts (this is what the method avoids)
    b, c, m = _simulate(0.0)
    naive = np.log(c[c > 0] / m[c > 0]).std()
    print(f"[1d] naive sd of log(c/m) at sigma=0: {naive:.2f}")
    assert naive > 0.5


def test_split_counts_conserves_and_is_deterministic():
    c = np.random.default_rng(1).integers(0, 50, 1000)
    a, b = esterror.split_counts(c, 5, 3), esterror.split_counts(c, 5, 3)
    assert (np.sum(a, axis=0) == c).all() and all((x == y).all() for x, y in zip(a, b))


def test_noise_draws_are_independent_standard_normals():
    pw = np.array([b"pw%07d" % i for i in range(60_000)], dtype="S30")
    from scipy.special import ndtri

    def z(salt):
        h = data.salted_hash64(pw, salt)
        return ndtri(((h >> np.uint64(11)).astype(np.float64) + 0.5) / 2.0 ** 53)

    z0, z1 = z(data.NOISE_SALT), z(b"c3sim-noise-v1-d1")
    print(f"[1d] noise draws: mean {z1.mean():+.3f}, sd {z1.std():.3f}, corr with the original draw {np.corrcoef(z0, z1)[0, 1]:+.3f}")
    assert abs(z1.mean()) < 0.02 and abs(z1.std() - 1) < 0.02 and abs(np.corrcoef(z0, z1)[0, 1]) < 0.02
