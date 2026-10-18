"""Phase 1b: calibration mechanics (sampler, bins, mass preservation)."""
from types import SimpleNamespace

import numpy as np

from c3sim import calibration as K


def test_calibration_mass_and_positivity(sp, est):
    pw, cnt = sp["A_train"]
    w = SimpleNamespace(pw=pw, cnt=cnt, t=est.t, est=est)
    cal = K.fit(w, width=1.0, n_samples=3_000_000)
    t = cal.table
    # head strings are excluded exactly, so the sampled model tail mass equals 1 - (3-gram mass on the head) scaled = 1 - hist mass (fit part)
    model, true, r = t["model_tail_mass"].sum(), t["held_out_tail_mass"].sum(), t["factor"]
    cal_mass = (t["model_tail_mass"] * r).sum()
    print(f"[1b] model tail mass {model:.4f} (expect about {1 - est.hist_p.sum():.4f}); held-out tail mass {true:.4f}; calibrated {cal_mass:.4f}")
    assert abs(model - (1 - est.hist_p.sum())) < 0.01  # sampler + hash exclusion are consistent with the exact estimator
    assert abs(cal_mass - true) < 1e-3                  # calibration reproduces the held-out tail mass
    assert (r > 0).all() and np.isfinite(r).all()
    ph = cal.phat_ranked(pw)
    assert (ph > 0).all() and np.isfinite(ph).all()
    assert (ph[: est.t] == est.phat_ranked(pw)[: est.t]).all()  # head unchanged
    s = pw[np.random.default_rng(0).choice(len(pw), 5000)]
    assert np.allclose(cal.phat(s), ph[np.searchsorted(np.sort(pw), s) * 0 + np.argsort(pw)[np.searchsorted(np.sort(pw), s)]], rtol=1e-12)


def test_pav_is_monotone():
    y = np.array([3.0, 1.0, 2.0, 5.0, 4.0])
    f = K._pav(y, np.ones(5))
    assert (np.diff(f) >= 0).all() and abs(f.sum() - y.sum()) < 1e-12
