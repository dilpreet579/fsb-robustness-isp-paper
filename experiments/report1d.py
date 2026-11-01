"""Assemble results/REPORT_1d.md from the Phase 1d CSVs (Phase 1c files read only). Numbers and method statements only."""
import os

import numpy as np
import pandas as pd

from experiments import common as C
from experiments.report import md, rd
from experiments.report1b import fmt, rdcsv

R = C.RESULTS
THR = 5.0
SIG = (0.5, 0.75, 1.0, 1.5)


def crossing_curve(sig, loss, thr=THR):
    """First sigma where the loss reaches thr, by linear interpolation; None if not reached."""
    if loss[0] >= thr:
        return 0.0
    for i in range(1, len(sig)):
        if loss[i] >= thr:
            return sig[i - 1] + (thr - loss[i - 1]) * (sig[i] - sig[i - 1]) / (loss[i] - loss[i - 1])
    return None


def main():
    L = ["# REPORT 1d (Phase 1d)", "",
         "Numbers and method statements only. Phase 1 / 1b / 1c results were not modified. New files: `results/e1d_*`, `experiments/e1d_*.py`, `experiments/report1d.py`, "
         "`c3sim/esterror.py`, `tests/test_phase1d.py`; additive edits to `experiments/common.py` (noise salts, M2L/M2B conditions, per-repeat success values). "
         "All runs at t = 1,000,000 (the primary setting) unless a t is stated, seed 2000, pool A_test (M1b: B_target), 5 repeats x 5,000 targets, units percent / percentage points, "
         "± = sd over the repeats unless stated. `est` = attacker weights p^ (deployed estimate), `emp` = leak counts.", ""]

    # ------------------------------------------------------------------ 1. candidate cap
    cap = rdcsv("e1d_cap.csv")
    cap["cand"] = cap.variant.str.split("cand").str[1]
    L += ["## 1. Attacker candidate-list cap (emp attacker, FSB qbar = 100)", "",
          "Ran: candidate lists of 2M, 4M, 6M and all of S~ (13,125,513; an extra, it fit in memory as in Phase 1) at t = 1M and t = 3M, conditions M0 and M2x (Xato list). "
          "Same targets in every cell. Loss at q = 1, 10, 100 (q = 1000 is in the CSV).", ""]
    rows = []
    for (t, cond), g in cap.groupby(["t", "condition"], sort=False):
        for c in ("2M", "4M", "6M", "allM"):
            x = g[g.cand == c]
            if x.empty:
                continue
            x = x.set_index("q")
            r = dict(t=f"{int(t):,}", condition=cond, candidates={"allM": "all (13.1M)"}.get(c, c), avg_bucket=f"{x.avg_bucket.iloc[0]:.0f}",
                     cand_per_bucket=f"{x.cand_per_bucket.iloc[0]:.0f}")
            for q in (1, 10, 100):
                r[f"base@{q}"] = f"{x.baseline_success[q]:.2f}"
            for q in (1, 10, 100):
                r[f"loss@{q}"] = f"{x.loss[q]:+.2f} ±{x.std_over_repeats[q]:.2f}"
            rows.append(r)
    L += [md(pd.DataFrame(rows)), ""]
    chg = []
    for (t, cond), g in cap.groupby(["t", "condition"], sort=False):
        b2 = g[(g.cand == "2M")].set_index("q").loss
        for c in ("4M", "6M", "allM"):
            x = g[g.cand == c].set_index("q").loss
            chg.append(dict(t=f"{int(t):,}", condition=cond, candidates=c.replace("allM", "all"), **{f"change vs 2M @q={q}": f"{x[q] - b2[q]:+.2f}" for q in (1, 10, 100)}))
    L += ["Change in loss relative to the 2M list:", "", md(pd.DataFrame(chg)), ""]

    # ------------------------------------------------------------------ 2. noise draws
    nz = rdcsv("e1d_noise.csv")
    nz["sigma"] = nz.variant.str.extract(r"noise_s([\d.]+)_d")[0].astype(float)
    nz["draw"] = nz.variant.str.extract(r"_d(\d+)")[0].astype(int)
    m0 = rdcsv("e1c_e2.csv")
    m0 = m0[(m0.condition == "M0") & (m0.variant == "fsb_base") & (m0.scheme == "fsb")]
    L += ["## 2. M3 with 5 independent noise draws (t = 1,000,000)", "",
          "Draw k uses salt `c3sim-noise-v1-d{k}` (k = 1..5) in the salted SHA-256 that defines z_w (the Phase 1c draw is salt `c3sim-noise-v1`, not included here). "
          "sigma in {0.5, 0.75, 1.0} as requested, plus 1.5 as a fallback anchor. `loss` = loss at q = qbar. sigma = 0 is the noise-free M0 row of `e1c_e2.csv` (same targets). "
          "Per draw, the loss at each sigma is the mean over the 5 target repeats; the crossing of 5 points is linear interpolation along sigma in {0, 0.5, 0.75, 1.0, 1.5}; "
          "reported as mean ± sd across the 5 draws (sd with ddof = 1).", ""]
    rows, cr = [], []
    for m in C.MODELS:
        for qb in (10, 100, 1000):
            base0 = float(m0[(m0.attacker == m) & (m0.param == qb) & (m0.q == qb)].loss.iloc[0])
            per_draw = {}
            for d in sorted(nz.draw.unique()):
                ls = [base0]
                for s in SIG:
                    ls.append(float(nz[(nz.attacker == m) & (nz.param == qb) & (nz.q == qb) & (nz.sigma == s) & (nz.draw == d)].loss.iloc[0]))
                per_draw[d] = ls
            r = dict(attacker=m, qbar=qb, **{"sigma=0 (M0)": f"{base0:+.2f}"})
            for i, s in enumerate(SIG, 1):
                v = np.array([per_draw[d][i] for d in per_draw])
                r[f"sigma={s}"] = f"{v.mean():+.2f} ± {v.std(ddof=1):.2f}"
            rows.append(r)
            xs = [0.0, *SIG]
            cs = [crossing_curve(xs, per_draw[d]) for d in per_draw]
            ok = [c for c in cs if c is not None]
            cr.append(dict(attacker=m, qbar=qb, crossing_mean_sd=(f"{np.mean(ok):.3f} ± {np.std(ok, ddof=1):.3f}" if len(ok) == len(cs) else
                           f"{np.mean(ok):.3f} ± {np.std(ok, ddof=1) if len(ok) > 1 else float('nan'):.3f} ({len(cs) - len(ok)} of {len(cs)} draws never reached 5)"),
                           per_draw_crossings=", ".join("n/a" if c is None else f"{c:.3f}" for c in cs)))
    L += ["Loss at q = qbar, mean ± sd across the 5 noise draws:", "", md(pd.DataFrame(rows)), "",
          "Sigma at which the loss at q = qbar reaches 5 points:", "", md(pd.DataFrame(cr)), ""]
    p1c = rdcsv("e1c_m3_repeats.csv")
    from experiments.report1c import crossing as cross1c
    ref = []
    for m in C.MODELS:
        for qb in (10, 100, 1000):
            cm, per, _, _ = cross1c(p1c, m, qb)
            ref.append(dict(attacker=m, qbar=qb, phase1c_draw0_curve_crossing=fmt(cm) if cm is not None else "n/a"))
    L += ["For reference, Phase 1c (single noise draw, sigma grid 0, .25, .5, .75, 1, 1.5), crossing of the mean curve:", "", md(pd.DataFrame(ref)), ""]

    # ------------------------------------------------------------------ 3. estimator error
    es = rdcsv("e1d_esterror_summary.csv")
    eb = rdcsv("e1d_esterror_bins.csv")
    L += ["## 3. Estimator error sigma_hat = sd of log(p^ / true probability) on held-out A_dev", "",
          "Held-out data: A_dev (1,631,475 accounts; 62.7% of them have a password stored in A_train). p^ is the estimate trained on all of A_train at the stated t. "
          "`head` = the top-t passwords of A_train (p^ = train frequency), `tail` = the rest (p^ from the 3-gram). Bins: 0.5 decade of p^. "
          "Neither method takes log(count / n) per password, so Poisson noise at tiny counts does not enter:", "",
          "- **B, per-password dispersion** (the quantity M3's sigma stands for). Population: the passwords stored in S~ (so it is conditional on being leaked). In a bin, "
          "held-out count c_i ~ Poisson(m_i e^{u_i}), m_i = n_dev p^_i, u_i iid with variance sigma^2. With x_i = c_i / m_i, Var[x] = E[x] mean(1/m) + (e^{sigma^2} - 1) E[x]^2, so "
          "sigma^2 = log(1 + (s^2 - xbar mean(1/m)) / xbar^2) (0 if the numerator is not positive); the first term is the Poisson variance and is subtracted. "
          "Bias mu = log(xbar) - sigma^2/2 = log(true / p^) of the bin (positive: p^ too small). Bins need >= 100 passwords and >= 50 held-out accounts. "
          "Group sigma_hat = sqrt of the password-weighted mean of sigma^2 (`sigma_hat`) or of the account-weighted mean (`sigma_hat_alt`). "
          "`se_over_folds`: A_dev's counts split into 5 folds, sigma_hat recomputed on each, sd / sqrt(5). Validated on simulated data in `tests/test_phase1d.py` "
          "(true sigma 0 / 0.5 / 1.0 recovered as 0.000 / 0.498 / 0.997; naive sd of log(c/m) at sigma = 0 is 0.60).",
          "- **A, binned masses over all strings** (calibration-style). Per bin: held-out mass vs the model's mass (head: exact sum of p^; tail: 3-gram mass by sampling 20M strings, "
          "head strings excluded by hash). lr = log(held-out mass / model mass), bins with >= 100 held-out accounts; sigma_hat = sqrt(account-weighted mean of max(lr^2 - 1/N_b, 0)) "
          "(Poisson variance of lr subtracted); `sigma_hat_alt` is the raw RMS. It measures scale error by p^ bin, not scatter inside a bin, so it is a lower bound on B. `bias_mu` = weighted mean lr.", "",
          md(es.round(4)), ""]
    ub = eb[(eb.t == 1_000_000)]
    for meth, g in (("B", "head"), ("B", "tail"), ("A", "head"), ("A", "tail")):
        x = ub[(ub.method == meth) & (ub.group == g) & (ub.used)]
        if meth == "B":
            tb = pd.DataFrame(dict(bin_log10_p_lo=x.bin_log10_lo, passwords=x.passwords, heldout_accounts=x.heldout_accounts.round(0), xbar=x.xbar.round(3),
                                   mu=x.mu.round(3), sigma=np.sqrt(x.sigma2).round(3)))
        else:
            tb = pd.DataFrame(dict(bin_log10_p_lo=x.bin_log10_lo, heldout_accounts=x.heldout_accounts.round(0), model_accounts=x.model_accounts.round(1), log_ratio=x.log_ratio.round(3)))
        L += [f"Bins used, method {meth}, {g}, t = 1,000,000 ({len(x)} bins; all bins and t = 100,000 in `e1d_esterror_bins.csv`):", "", md(tb), ""]

    # ------------------------------------------------------------------ 4. M2 ablation
    ab = rdcsv("e1d_ablation.csv")
    lab = {"M2L": "length >= 8 only", "M2B": "Xato blocklist only", "M2x": "both (M2x)"}
    rows = []
    for c in ("M2L", "M2B", "M2x"):
        for qb in (10, 100, 1000):
            r = dict(policy=lab[c], qbar=qb)
            for m in C.MODELS:
                x = ab[(ab.condition == c) & (ab.attacker == m) & (ab.param == qb)].set_index("q")
                r[f"{m} loss@qbar"] = f"{x.loss[qb]:+.2f} ±{x.std_over_repeats[qb]:.2f}"
                r[f"{m} baseline@qbar"] = f"{x.baseline_success[qb]:.2f}"
            r["avg_bucket"] = f"{x.avg_bucket.iloc[0]:.0f}"
            rows.append(r)
    L += ["## 4. M2 ablation (t = 1,000,000)", "",
          "Targets and the attacker's candidate list are restricted to passwords that satisfy the policy; the server's estimate and buckets are unchanged. "
          "Blocklist = first 370 lines of the Xato list (D14). Loss at q = qbar; baseline = the same attacker's no-bucket success at q = qbar.", "", md(pd.DataFrame(rows)), ""]

    # ------------------------------------------------------------------ 5. ratios
    rt = rdcsv("e1d_ratio.csv")
    rt["ratio"] = rt.apply(lambda r: "n/a" if pd.isna(r.ratio) else f"{r.ratio:.2f}" + (f" ±{r.ratio_sd:.2f}" if not pd.isna(r.ratio_sd) else ""), axis=1)
    rt = rt.assign(baseline=rt.baseline_success.map("{:.2f}".format), attacker_success=rt.bucket_success.map("{:.2f}".format))
    L += ["## 5. Success ratio (attacker success / baseline success) at q = 1 and q = qbar", "",
          "ratio = mean bucket success / mean baseline success over the 5 repeats; ± = sd of the per-repeat ratios (n/a if some repeat has baseline 0). "
          "Rows: FSB and size-matched HPB (`scheme`, `qbar` = the FSB qbar the HPB row is matched to); conditions M0, M1b, M2x. Baseline success at q = 1 is small "
          "(M0 about 1%, M2x about 0.1%), so ratios at q = 1 are noisy.", ""]
    for m in C.MODELS:
        x = rt[rt.attacker == m]
        L += [f"### attacker `{m}`", "", md(x[["condition", "scheme", "qbar", "q", "avg_bucket", "baseline", "attacker_success", "ratio", "loss"]]), ""]

    L += ["## 6. Checks and runtimes", "", "```", rd("e1d_tests.txt"), "```", "", "```", rd("e1d_runtimes.txt"), "```", "",
          "## 7. New files", "",
          "`results/`: e1d_cap.csv, e1d_noise.csv, e1d_esterror_summary.csv, e1d_esterror_bins.csv, e1d_ablation.csv, e1d_ratio.csv, logs, time files, e1d_tests.txt, this report. "
          "Columns as in e1c_*.csv; e1d_ratio.csv has its own columns (see header).", ""]
    open(os.path.join(R, "REPORT_1d.md"), "w").write("\n".join(L))
    print("wrote REPORT_1d.md", len("\n".join(L)))


if __name__ == "__main__":
    main()
