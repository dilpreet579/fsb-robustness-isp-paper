"""Assemble results/REPORT_1c.md from the Phase 1c CSVs (Phase 1 / 1b files are read only where noted). Numbers and pass/fail only."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

from c3sim import data
from experiments import common as C
from experiments.report import md, rd, table
from experiments.report1b import fmt, interp, interp_table, rdcsv

R = C.RESULTS
QS = C.QS
THR = 5.0


def crossing(rep, att, qb, xs=None):
    """sigma at which loss at q = qbar first reaches THR points, by linear interpolation along the sigma grid (sigma = 0 is M0).
    Returns (mean-curve crossing, per-repeat crossings with None for 'not reached by the largest sigma')."""
    d = rep[(rep.attacker == att) & (rep.qbar == qb)]
    xs = sorted(d.sigma.unique())

    def cross(y):
        if y[0] >= THR:
            return 0.0
        for i in range(1, len(xs)):
            if y[i] >= THR:
                return xs[i - 1] + (THR - y[i - 1]) * (xs[i] - xs[i - 1]) / (y[i] - y[i - 1])
        return None

    mean_curve = [d[d.sigma == s].loss.mean() for s in xs]
    per = [cross([d[(d.sigma == s) & (d.repeat == r)].loss.iloc[0] for s in xs]) for r in sorted(d.repeat.unique())]
    return cross(mean_curve), per, mean_curve, xs


def main():
    e2 = rdcsv("e1c_e2.csv")
    sw = rdcsv("e1c_base_sweep.csv")
    rep = rdcsv("e1c_m3_repeats.csv")
    L = ["# REPORT 1c (Phase 1c: t = 1,000,000 as the primary setting)", "",
         "Numbers only. Phase 1 / 1b results were not modified; Phase 1c adds `results/e1c_*` files and `experiments/e1c_*.py`, `experiments/report1c.py`, "
         "`tests/test_phase1c.py`, plus additive edits to `experiments/common.py` (Xato list, conditions M1a/M2x/M0s/M2s, per-repeat losses). "
         "Units: percent / percentage points; ± = sd of the per-repeat loss (5 repeats x 5,000 targets). `est` = attacker weights = the deployed p^ (histogram head t = 1,000,000), "
         "`emp` = leak counts. Seeds as before: E2-type rows 2000, E3 dev 3000 / fresh 4000, calibration dev 5000 / fresh 6000. "
         "M1a = Phase 1's M1 (B_attack attacker); M1b = server estimate from A_train, B_target targets, attacker over the top 2M of S~. "
         "**M2x** = M2 with the Xato list (primary, section 4); **M2** = `top370_A_train` (secondary).", ""]

    # ------------------------------------------------------------------ items 1 and 2: headline + E2-type tables
    L += ["## 1. E2-type rows at t = 1,000,000", ""]
    for m in C.MODELS:
        L += [f"### attacker `{m}`", "", md(table(e2[e2.attacker == m], ["condition", "scheme", "variant", "param"])), ""]
    L += ["### Headline table: loss at q = qbar, t = 1,000,000", "",
          "M3 rows: `avg bucket` = the noisy scheme's own average bucket size; `base@same size` = base FSB loss at q = qbar (M0 pool, seed 2000), interpolated "
          "(log-linear in average bucket size) along the dense base sweep `e1c_base_sweep.csv` (qbar 1..3000). † = mean attacker candidates per bucket < q.", ""]
    rows = []
    srcs = [("M0", e2[(e2.condition == "M0") & (e2.variant == "fsb_base")], None), ("M1a", e2[e2.condition == "M1a"], None),
            ("M1b", e2[e2.condition == "M1b"], None), ("M2x (Xato list, primary)", e2[e2.condition == "M2x"], None),
            ("M2 (top370_A_train)", e2[e2.condition == "M2"], None)]
    for s_ in (0.25, 0.5, 0.75, 1.0, 1.5):
        srcs.append((f"M3 sigma={s_}", e2[(e2.condition == "M3") & (e2.variant == f"noise_s{s_}")], "M3"))
    for lab, d, kind in srcs:
        for qb in (10, 100, 1000):
            r = dict(condition=lab, qbar=qb)
            for m in C.MODELS:
                x = d[(d.attacker == m) & (d.scheme == "fsb") & (d.param == qb) & (d.q == qb)].iloc[0]
                r[f"{m} loss"] = f"{x.loss:+.2f} ±{x.std_over_repeats:.2f}" + (" †" if x.cand_per_bucket < qb else "")
                r["avg bucket"] = f"{x.avg_bucket:.0f}"
                if kind == "M3":
                    r[f"{m} base@same size"] = fmt(interp(sw[(sw.attacker == m) & (sw.scheme == "fsb")], qb, x.avg_bucket))
            rows.append(r)
    L += [md(pd.DataFrame(rows).fillna("")), ""]

    L += ["## 2. M3: where does the loss at q = qbar reach 5 points? (t = 1,000,000)", "",
          "sigma grid 0 (= M0), 0.25, 0.5, 0.75, 1.0, 1.5; linear interpolation in sigma. `curve` = crossing of the mean-over-repeats curve. Interval: the crossing "
          "is computed per repeat (5 repeats, different targets, same noise function since z_w is a fixed hash of the password), then mean ± 95% t-interval (4 dof) and [min, max]. "
          "The interval therefore reflects target sampling only, not a different draw of the noise.", ""]
    rows, curves = [], []
    for m in C.MODELS:
        for qb in (10, 100, 1000):
            cm, per, mc, xs = crossing(rep, m, qb)
            ok = [p for p in per if p is not None]
            if len(ok) == len(per):
                mu, sd = float(np.mean(ok)), float(np.std(ok, ddof=1))
                hw = stats.t.ppf(0.975, len(ok) - 1) * sd / np.sqrt(len(ok))
                iv = f"{mu:.3f} ± {hw:.3f}  [{min(ok):.3f}, {max(ok):.3f}]"
            else:
                iv = f"not reached by sigma={xs[-1]} in {len(per) - len(ok)} of {len(per)} repeats"
            rows.append(dict(attacker=m, qbar=qb, curve_crossing=fmt(cm) if cm is not None else f">{xs[-1]}", per_repeat_mean_CI_minmax=iv))
            curves.append(dict(attacker=m, qbar=qb, **{f"sigma={s}": f"{v:.2f}" for s, v in zip(xs, mc)}))
    L += [md(pd.DataFrame(rows)), "", "Mean loss at q = qbar by sigma:", "", md(pd.DataFrame(curves)), ""]

    # ------------------------------------------------------------------ item 3
    ts = rdcsv("e1c_tsweep.csv")
    x = ts[(ts.q == 100)]
    L += ["## 3. t sweep (M0, FSB qbar = 100, q = 100; seed 2000, A_test)", "",
          md(pd.DataFrame([dict(t=f"{int(r.t):,}", attacker=r.attacker, avg_bucket=f"{r.avg_bucket:.0f}", max_bucket=int(r.max_bucket),
                                baseline_q100=f"{r.baseline_success:.2f}", loss_q100=f"{r.loss:+.2f} ±{r.std_over_repeats:.2f}") for r in x.itertuples()])), "",
          "All four q for the same rows:", "", md(table(ts[ts.attacker == "emp"].assign(t=ts.t.map(lambda v: f"{int(v):,}")), ["t", "scheme", "param"])), ""]

    # ------------------------------------------------------------------ item 4
    sp = data.splits()
    pw, cnt = sp["A_train"]
    xa = C.load_xato()
    top = pw[:370]
    inA = np.isin(xa, pw)
    L += ["## 4. M2 banned list: Xato top-370 (primary) vs top370_A_train (secondary)", "",
          "`10-million-password-list-top-1000.txt` is not in SecLists `Passwords/Common-Credentials` (folder listing checked). Nearest fixed public list used: "
          "`xato-net-10-million-passwords-1000.txt` from the same folder (the top 1000 of the Xato 10M list, SecLists' current name for it), first 370 lines. "
          f"Policy: length >= 8 and not in the list. Line 43 of the file is blank, so the 370 lines hold {int((xa != b'').sum())} real passwords. "
          f"Entries of length >= 8 among the 370: {int((data.lengths(xa) >= 8).sum())}. "
          f"Overlap with top370_A_train: {int(np.isin(xa, top).sum())} of 370. Xato entries present in A_train: {int(inA.sum())} of 370; "
          f"share of A_train mass they hold: {cnt[np.searchsorted(np.sort(pw), xa[inA]) * 0 + np.argsort(pw)[np.searchsorted(np.sort(pw), xa[inA])]].sum() / cnt.sum():.3%}.", ""]
    rows = []
    for qb in (10, 100, 1000):
        for m in C.MODELS:
            r = dict(qbar=qb, attacker=m)
            for c, lab in (("M2x", "M2x Xato"), ("M2", "M2 top370_A_train")):
                z = e2[(e2.condition == c) & (e2.attacker == m) & (e2.scheme == "fsb") & (e2.param == qb)].set_index("q")
                r[f"{lab} base@1000"] = f"{z.baseline_success[1000]:.2f}"
                r[f"{lab} loss@q=qbar"] = f"{z.loss[qb]:+.2f} ±{z.std_over_repeats[qb]:.2f}"
                r[f"{lab} loss@1000"] = f"{z.loss[1000]:+.2f}"
            rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "Full rows for M2x and M2 are in section 1.", ""]

    # ------------------------------------------------------------------ item 5
    sn = rdcsv("e1c_sanity.csv")
    L += ["## 5. est-attacker sanity: candidates of length <= 2 outside the histogram head removed (t = 1,000,000)", "",
          "M0s / M2s = the attacker's candidate list without strings of length <= 2 whose rank by count is > t (the server's scheme and the targets are unchanged). "
          "Compared with the same est rows of section 1 (M0, M2x). M2's policy already requires length >= 8, so M2s removes nothing by construction.", ""]
    rows = []
    for cs, c0 in (("M0s", "M0"), ("M2s", "M2x")):
        for sch in ("fsb", "hpb"):
            for p in sorted(sn[(sn.condition == cs) & (sn.scheme == sch)].param.unique()):
                for q in QS:
                    a = sn[(sn.condition == cs) & (sn.scheme == sch) & (sn.param == p) & (sn.q == q)].iloc[0]
                    b = e2[(e2.condition == c0) & (e2.attacker == "est") & (e2.scheme == sch) & (e2.param == p) & (e2.q == q) &
                           ((e2.variant == "fsb_base") if sch == "fsb" else e2.variant.str.startswith("match"))].iloc[0]
                    rows.append(dict(pair=f"{c0} -> {cs}", scheme=sch, param=p, q=q, baseline=f"{b.baseline_success:.2f} -> {a.baseline_success:.2f}",
                                     loss=f"{b.loss:+.2f} -> {a.loss:+.2f}", change_in_loss=f"{a.loss - b.loss:+.2f}"))
    L += [md(pd.DataFrame(rows)), ""]

    # ------------------------------------------------------------------ item 1 (E3)
    e3 = rdcsv("e1c_e3.csv")
    best = json.load(open(os.path.join(R, "e1c_e3_selection.json")))["best"]
    L += ["## 6. E3 at t = 1,000,000 (fresh pool seed 4000; selection on dev, seed 3000)", "",
          "Variants as Phase 1 (fsb_base, ens_max, smoothed), qbar 1..3000, conditions M0, M1a, M1b, M2, M2x. Selection criterion changed to the Phase 1c primary conditions "
          "(M0, M1b, M2x); dev rows in `e1c_e3_dev.csv`.", "", "```", rd("e1c_e3_selection.txt"), "```", "",
          "Loss at q=1000, interpolated to fixed average bucket sizes (fresh pool; nan = sweep does not reach it):", ""]
    rows = []
    for m in C.MODELS:
        for c in CONDS_E3:
            for v in ("fsb_base", "ens_max", "smoothed"):
                d = e3[(e3.attacker == m) & (e3.condition == c) & (e3.variant == v)]
                r = dict(attacker=m, condition=c, variant=v)
                for b in (2000, 6500, 20000):
                    r[f"loss@{b}"] = fmt(interp(d, 1000, b))
                rows.append(r)
    L += [md(pd.DataFrame(rows)), ""]
    for m in C.MODELS:
        for c in ("M0", "M1b", "M2x"):
            L += [f"### attacker `{m}`, {c} (fresh pool)", "", md(table(e3[(e3.attacker == m) & (e3.condition == c)], ["variant", "param"])), ""]

    # ------------------------------------------------------------------ item 6
    dev = rdcsv("e1c_fix_dev.csv")
    L += ["## 7. Calibration fix at t = 1,000,000 (EXPLORATORY)", "",
          "Same pipeline as Phase 1b (`c3sim/calibration.py`; cross-fit 90/10 split of A_train; variants cal_w0.5, cal_w1.0, cal_iso_w0.5), rerun at t = 1e6: design on A_dev / B_dev "
          "(seed 5000), then one run on A_fresh / B_fresh (seed 6000). **Exploratory:** A_fresh / B_fresh and these exact targets were already used in Phase 1 (E3) and in the Phase 1b "
          "fresh calibration run, so the fresh pool is not an untouched holdout for this design. est attacker = the deployed (calibrated) p^; emp = counts. "
          "Dev selection uses M0, M1b, M2x.", "",
          "```", "\n".join(l for l in rd("e1c_fix_dev_log.txt").split("\n") if l.startswith("[cal")), "```", "", "```", rd("e1c_fix_selection.txt"), "```", "",
          "Dev loss interpolated to equal bucket size (q = 100, 1000; 2,000 and 6,500 entries):", "", md(interp_table(dev, ["condition", "attacker", "variant"])), ""]
    fp = os.path.join(R, "e1c_fix_fresh.csv")
    if os.path.exists(fp):
        fr = rdcsv("e1c_fix_fresh.csv")
        bst = json.load(open(os.path.join(R, "e1c_fix_selection.json")))["best"]
        L += [f"### 7.1 Fresh pool, one run: fsb_base vs {bst}", "", md(interp_table(fr, ["condition", "attacker", "variant"])), "",
              "Loss at q = qbar (fresh pool):", ""]
        rows = []
        for c_ in sorted(fr.condition.unique()):
            for v in sorted(fr[fr.condition == c_].variant.unique()):
                for qb in (10, 100, 1000):
                    for m in C.MODELS:
                        z = fr[(fr.condition == c_) & (fr.variant == v) & (fr.attacker == m) & (fr.param == qb) & (fr.q == qb)]
                        if len(z):
                            rows.append(dict(condition=c_, variant=v, qbar=qb, attacker=m, avg_bucket=f"{z.avg_bucket.iloc[0]:.0f}",
                                             loss=f"{z.loss.iloc[0]:+.2f} ±{z.std_over_repeats.iloc[0]:.2f}"))
        L += [md(pd.DataFrame(rows)), ""]
    else:
        L += ["### 7.1 Fresh pool", "", "(not run yet)", ""]

    L += ["## 8. Checks and runtimes", "", "```", rd("e1c_tests.txt"), "```", "", "```", rd("e1c_runtimes.txt"), "```", "",
          "## 9. New files", "",
          "`results/`: e1c_e2.csv, e1c_base_sweep.csv, e1c_m3_repeats.csv, e1c_sanity.csv, e1c_tsweep.csv, e1c_e3.csv, e1c_e3_dev.csv, e1c_e3_selection.{txt,json}, "
          "e1c_fix_dev.csv, e1c_fix_fresh.csv, e1c_fix_selection.{txt,json}, e1c_cal_table_*.csv, logs, this report. Columns as in e1b_*.csv. "
          "Data: `data/xato/xato-net-10-million-passwords-1000.txt` (git-ignored).", ""]
    open(os.path.join(R, "REPORT_1c.md"), "w").write("\n".join(L))
    print("wrote REPORT_1c.md", len("\n".join(L)))


CONDS_E3 = ("M0", "M1a", "M1b", "M2", "M2x")

if __name__ == "__main__":
    main()
