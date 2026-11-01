"""Phase 1d item 3: how wrong is p^? sigma_hat = sd of log(p^ / true probability), estimated on held-out accounts.

Two estimators, both free of the Poisson inflation that comes from taking log(count / n) at tiny counts:

(B) per-password dispersion, within bins of p^ (moment method).  Population = the passwords stored in S~ (A_train rows), because
    those are what the buckets hold. Held-out count c_i ~ Poisson(m_i * exp(u_i)), m_i = n_dev * p^_i, u_i iid with variance sigma^2
    inside a bin (the same independent log-noise model as M3). With x_i = c_i / m_i:
        E[x] = exp(mu + sigma^2 / 2),   Var[x] = E[x] * mean(1/m) + (exp(sigma^2) - 1) * E[x]^2.
    Solving for sigma^2 with the sample mean and variance of x in the bin gives sigma^2 = log(1 + (s^2 - xbar*mean(1/m)) / xbar^2)
    (0 if the numerator is not positive); the first term of Var[x] is the Poisson part and is subtracted. mu is the bin's bias.
    Strings never stored in S~ are not in this population (it is conditional on being leaked).

(A) binned masses over all strings. For each bin of p^: held-out mass vs model mass (head: exact sum of p^ over the head; tail:
    the 3-gram's mass by sampling, head strings excluded). Bin log-ratio lr = log(held-out mass / model mass); bins with at least
    `min_acc` held-out accounts only; Poisson variance of lr (about 1/N_b) is subtracted: sigma^2_A = weighted mean(lr^2 - 1/N_b) (floored at 0).
    It measures scale error of p^ by p^ bin, not per-password scatter, so it is a lower bound on (B).
"""
import numpy as np

from . import calibration as K
from . import data, estimators


def moment_by_bin(b, c, m, nb):
    """Per-bin sufficient statistics and sigma^2 (method B). b: bin index per password, c: held-out counts, m: expected counts under p^."""
    n = np.bincount(b, minlength=nb).astype(float)
    x = c / m
    sx, sxx, sinv, sc = (np.bincount(b, weights=v, minlength=nb) for v in (x, x * x, 1.0 / m, c.astype(float)))
    with np.errstate(divide="ignore", invalid="ignore"):
        xbar = sx / n
        s2 = (sxx - n * xbar ** 2) / (n - 1)
        ratio = (s2 - xbar * sinv / n) / xbar ** 2
        sigma2 = np.where(ratio > 0, np.log1p(ratio), 0.0)
        mu = np.log(xbar) - sigma2 / 2
    return dict(n=n, accounts=sc, xbar=xbar, s2=s2, poisson_var=xbar * sinv / n, sigma2=sigma2, mu=mu)


def aggregate(st, min_n=100, min_acc=50):
    """Group sigma_hat from per-bin sigma^2: weights = passwords (per-password sd) and held-out accounts (mass-weighted)."""
    ok = (st["n"] >= min_n) & (st["accounts"] >= min_acc) & np.isfinite(st["sigma2"])
    out = {"bins_used": int(ok.sum()), "passwords_used": float(st["n"][ok].sum())}
    for name, w in (("per_password", st["n"]), ("mass_weighted", st["accounts"])):
        out[f"sigma_hat_{name}"] = float(np.sqrt((w[ok] * st["sigma2"][ok]).sum() / w[ok].sum())) if ok.any() else np.nan
    out["bias_mu_mass_weighted"] = float((st["accounts"][ok] * st["mu"][ok]).sum() / st["accounts"][ok].sum()) if ok.any() else np.nan
    return out


def split_counts(c, k, seed):
    """Split integer counts into k independent folds (sequential binomials); deterministic in seed."""
    rng, rest, out = np.random.default_rng(seed), c.astype(np.int64), []
    for i in range(k - 1):
        f = rng.binomial(rest, 1.0 / (k - i))
        out.append(f)
        rest = rest - f
    out.append(rest)
    return out


def binned_mass(est, dev_pw, dev_c, width=0.5, n_samples=20_000_000, seed=7, min_acc=100):
    """Method (A). Returns per-bin table (head and tail) and the two group sigma_hat values."""
    ntot = float(dev_c.sum())
    ph, head = est.phat_head(dev_pw)
    nb = int(round((K.HI - K.LO) / width))
    # tail: held-out mass in bins vs sampled model mass (head excluded by hash)
    bt, _ = K._bin(ph[~head], width)
    true_t = np.bincount(bt, weights=dev_c[~head], minlength=nb)
    lp, hs = np.empty(n_samples), np.empty(n_samples, np.uint64)
    cdf = np.cumsum(np.exp(est.lt), axis=2)
    K._sample(cdf, est.lt, n_samples, seed, lp, hs)
    keep = ~np.isin(hs, K._hashes(est.top_sorted))
    bm, _ = K._bin(np.exp(lp[keep]) * est.scale, width)
    model_t = est.scale * np.bincount(bm, minlength=nb) / n_samples * ntot  # in accounts
    # head: held-out accounts of head passwords vs n_dev * sum of p^ over the head, per p^ bin
    bh_all, _ = K._bin(est.hist_p, width)
    model_h = np.bincount(bh_all, weights=est.hist_p, minlength=nb) * ntot
    bh, _ = K._bin(ph[head], width)
    true_h = np.bincount(bh, weights=dev_c[head], minlength=nb)
    tabs, res = [], {}
    for g, tr, mo in (("head", true_h, model_h), ("tail", true_t, model_t)):
        with np.errstate(divide="ignore", invalid="ignore"):
            lr = np.log(tr / mo)
        ok = (tr >= min_acc) & (mo > 0) & np.isfinite(lr)
        var = np.where(ok, np.maximum(lr ** 2 - 1.0 / np.maximum(tr, 1), 0.0), 0.0)  # Poisson variance of lr ~ 1/N_b
        w = tr * ok
        res[g] = dict(bins_used=int(ok.sum()), heldout_accounts_used=float(w.sum()),
                      mean_log_ratio=float((w * np.where(ok, lr, 0)).sum() / w.sum()) if ok.any() else np.nan,
                      sigma_hat_raw=float(np.sqrt((w * np.where(ok, lr ** 2, 0)).sum() / w.sum())) if ok.any() else np.nan,
                      sigma_hat_poisson_corrected=float(np.sqrt((w * var).sum() / w.sum())) if ok.any() else np.nan)
        for i in np.flatnonzero(tr + mo > 0):
            tabs.append(dict(group=g, bin_log10_lo=K.LO + i * width, heldout_accounts=float(tr[i]), model_accounts=float(mo[i]),
                             log_ratio=float(lr[i]) if np.isfinite(lr[i]) else np.nan, used=bool(ok[i])))
    return tabs, res
