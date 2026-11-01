"""Phase 1d item 3: sigma_hat of the estimate p^ on held-out A_dev (method: c3sim/esterror.py docstring), t in {1e5, 1e6}.
Outputs: e1d_esterror_summary.csv (one row per t / group / method) and e1d_esterror_bins.csv (per-bin detail)."""
import os

import numpy as np
import pandas as pd

from c3sim import calibration as K
from c3sim import data, esterror, estimators
from experiments import common as C

WIDTH = 0.5
FOLDS = 5


def main():
    sp = data.splits()
    pw, cnt = sp["A_train"]
    dev_pw, dev_c = sp["A_dev"]
    n_dev = float(dev_c.sum())
    srt = np.argsort(pw)
    pos = np.searchsorted(pw[srt], dev_pw)
    pos[pos == len(pw)] = 0
    hit = pw[srt][pos] == dev_pw
    c_rows = np.zeros(len(pw), np.int64)
    c_rows[srt[pos[hit]]] = dev_c[hit]
    print(f"A_dev: {int(n_dev):,} accounts; {dev_c[hit].sum() / n_dev:.1%} of them have a password stored in A_train", flush=True)
    folds = esterror.split_counts(c_rows, FOLDS, seed=1234)
    summ, bins = [], []
    for t in (100_000, 1_000_000):
        est = estimators.Estimator(pw, cnt, t=t)
        ph = est.phat_ranked(pw)
        for g, sl in (("head", slice(0, t)), ("tail", slice(t, None))):
            b, nb = K._bin(ph[sl], WIDTH)
            m = n_dev * ph[sl]
            st = esterror.moment_by_bin(b, c_rows[sl], m, nb)
            ag = esterror.aggregate(st)
            per_fold = [esterror.aggregate(esterror.moment_by_bin(b, f[sl], (n_dev / FOLDS) * ph[sl], nb)) for f in folds]
            fold_sd = {k: float(np.std([p[k] for p in per_fold], ddof=1)) for k in ("sigma_hat_per_password", "sigma_hat_mass_weighted")}
            summ.append(dict(t=t, group=g, method="B per-password dispersion (stored passwords)", sigma_hat=ag["sigma_hat_per_password"],
                             sigma_hat_alt=ag["sigma_hat_mass_weighted"], alt_meaning="mass-weighted", se_over_folds=fold_sd["sigma_hat_per_password"] / np.sqrt(FOLDS),
                             bias_mu=ag["bias_mu_mass_weighted"], bins_used=ag["bins_used"], n_used=ag["passwords_used"]))
            for i in np.flatnonzero(st["n"] > 0):
                bins.append(dict(t=t, group=g, method="B", bin_log10_lo=K.LO + i * WIDTH, passwords=int(st["n"][i]), heldout_accounts=float(st["accounts"][i]),
                                 xbar=float(st["xbar"][i]), mu=float(st["mu"][i]), sigma2=float(st["sigma2"][i]),
                                 used=bool(st["n"][i] >= 100 and st["accounts"][i] >= 50)))
        tabs, res = esterror.binned_mass(est, dev_pw, dev_c, width=WIDTH)
        for g in ("head", "tail"):
            r = res[g]
            summ.append(dict(t=t, group=g, method="A binned masses (all strings)", sigma_hat=r["sigma_hat_poisson_corrected"], sigma_hat_alt=r["sigma_hat_raw"],
                             alt_meaning="raw (not Poisson-corrected)", se_over_folds=np.nan, bias_mu=r["mean_log_ratio"], bins_used=r["bins_used"],
                             n_used=r["heldout_accounts_used"]))
        bins += [dict(t=t, method="A", **x) for x in tabs]
        print(f"t={t:,} done", flush=True)
    pd.DataFrame(summ).to_csv(os.path.join(C.RESULTS, "e1d_esterror_summary.csv"), index=False)
    pd.DataFrame(bins).to_csv(os.path.join(C.RESULTS, "e1d_esterror_bins.csv"), index=False)
    print(pd.DataFrame(summ).round(3).to_string())


if __name__ == "__main__":
    main()
