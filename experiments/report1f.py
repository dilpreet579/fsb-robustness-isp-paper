"""Assemble results/REPORT_1f.md from the Phase 1f CSVs (earlier phases' files are read only). Numbers and method statements only."""
import os
import re

import numpy as np
import pandas as pd

from experiments import common as C
from experiments.e1f_mechanism import COUNT_LABELS, GAMMA_LABELS
from experiments.report import md, rd
from experiments.report1b import rdcsv

R = C.RESULTS
CL = {"M0": "M0", "M2x": "M2x (len>=8 + Xato)"}
SL = {"fsb": "FSB qbar=100", "hpb": "HPB l=12 (size-matched)"}


def main():
    L = ["# REPORT 1f (Phase 1f: mechanism and tail-only noise)", "",
         "Numbers and method statements only. Earlier phases' results were not modified; Phase 1f adds `results/e1f_*`, `experiments/e1f_*.py`, `experiments/report1f.py`, `tests/test_phase1f.py`. "
         "Setting: t = 1,000,000, seed 2000, pool A_test, 5 repeats x 5,000 targets (the same targets and bucket draws as Phase 1e), units percent / percentage points, ± = sd over the repeats unless stated. "
         "The emp attacker (section 1) holds **all of S~** (13,125,513 candidates).", ""]

    # ------------------------------------------------------------------ 1 mechanism
    g = rdcsv("e1f_mech_groups.csv")
    L += ["## 1. Mechanism: which targets does the emp attacker get?", "",
          "Target groups (by the target's password): **head** = stored in S~ and among the top t = 1M passwords of A_train by count (the histogram head of p^); "
          "**tail** = stored in S~ but not in the head; **none** = not in S~ (no candidate, can never be guessed). Per group: `share` of all targets; `success` and `baseline` = rate within the group "
          "(bucket attacker / no-bucket attacker, top q); `loss contribution` = share x (success - baseline) = the group's part of the total loss, summed over groups (the `total` row). "
          "The games replay Phase 1e exactly and the totals are asserted equal to `e1e_headline.csv` (the script stops otherwise). qbar = 100.", ""]
    for cond in ("M0", "M2x"):
        for sch in ("fsb", "hpb"):
            rows = []
            for q in (1, 100):
                tot = g[(g.condition == cond) & (g.scheme == sch) & (g.q == q) & (g.group == "total")].iloc[0]
                for grp in ("head", "tail", "none", "total"):
                    x = g[(g.condition == cond) & (g.scheme == sch) & (g.q == q) & (g.group == grp)].iloc[0]
                    rows.append(dict(q=q, group=grp, share=f"{x.share:.2f} ±{x.share_sd:.2f}", success=("n/a" if pd.isna(x.succ) else f"{x.succ:.2f} ±{x.succ_sd:.2f}"),
                                     baseline=("n/a" if pd.isna(x.base) else f"{x.base:.2f} ±{x.base_sd:.2f}"), loss_contribution=f"{x.contrib:+.2f} ±{x.contrib_sd:.2f}",
                                     part_of_total_loss=(f"{100 * x.contrib / tot.contrib:.0f}%" if grp != "total" else "100%")))
            L += [f"### {CL[cond]}, {SL[sch]}", "", md(pd.DataFrame(rows)), ""]
    qq = rdcsv("e1f_mech_quantiles.csv")
    dd = rdcsv("e1f_mech_dist.csv")
    L += ["### 1.2 gamma and leak count of the targets the attacker guesses correctly", "",
          "`correct` = targets in the attacker's top-q list for their bucket; `newly_gained` = correct and not guessed by the no-bucket attacker (the part that is loss). Pooled over the 5 repeats (25,000 targets). "
          "gamma = the target's replication factor gamma(w) (HPB: always 1; |B| = 16,777,216 = in every bucket). Leak count = count of the password in A_train. "
          "`group` splits the guessed targets into head / tail.", ""]
    for cond in ("M0", "M2x"):
        for sch in ("fsb", "hpb"):
            for q in (1, 100):
                x = qq[(qq.condition == cond) & (qq.scheme == sch) & (qq.q == q)]
                if x.empty:
                    continue
                t = x[["subset", "group", "variable", "n", "min", "p10", "p25", "p50", "p75", "p90", "max", "mean"]].copy()
                for c in ("min", "p10", "p25", "p50", "p75", "p90", "max"):
                    t[c] = t[c].map(lambda v: f"{v:,.0f}")
                t["mean"] = t["mean"].map(lambda v: f"{v:,.1f}")
                L += [f"#### {CL[cond]}, {SL[sch]}, q = {q}: quantiles", "", md(t), ""]
    for cond in ("M0", "M2x"):
        for q in (1, 100):
            x = dd[(dd.condition == cond) & (dd.scheme == "fsb") & (dd.q == q) & (dd.group == "all")]
            rows = []
            for var, labels in (("gamma", GAMMA_LABELS), ("leak_count", COUNT_LABELS)):
                for lab in labels:
                    r = dict(variable=var, bin=lab)
                    for sub in ("correct", "newly_gained"):
                        y = x[(x.subset == sub) & (x.variable == var) & (x.bin == lab)]
                        r[f"{sub} n"] = int(y.n.iloc[0]) if len(y) else 0
                        r[f"{sub} %"] = f"{y.share_pct.iloc[0]:.1f}" if len(y) else "0.0"
                    rows.append(r)
            L += [f"#### {CL[cond]}, FSB qbar=100, q = {q}: binned shares (all guessed targets)", "", md(pd.DataFrame(rows)), ""]

    # ------------------------------------------------------------------ 2 tail-only noise
    tn = rdcsv("e1f_tailnoise.csv")
    d1 = rdcsv("e1d_noise.csv")
    es = rdcsv("e1d_esterror_summary.csv")
    for df in (tn,):
        df["kind"] = df.variant.str.split("_").str[0]
        df["sigma"] = df.variant.str.extract(r"_s([\d.]+)_d")[0].astype(float)
        df["draw"] = df.variant.str.extract(r"_d(\d+)")[0].astype(int)
    L += ["## 2. Tail-only noise (M3 variant), est attacker, FSB qbar = 100, t = 1,000,000", "",
          "`tailnoise`: p^ is multiplied by exp(sigma z_w) only for strings **outside the histogram head** (the top 1M passwords of A_train); head strings keep p^ exactly. "
          "`fullnoise`: the same draws with the noise on every string (the Phase 1c/1d M3). 5 independent draws (salts `c3sim-noise-v1-d1..d5`, as Phase 1d); loss at q = qbar = 100, "
          "mean ± sd across the 5 draws (each draw averages 5 repeats of 5,000 targets). est attacker with the 2M list, as in Phase 1d. sigma = 1.6 is new for the full-noise curve "
          "(Phase 1d stops at 1.5). sigma = 0 is M0: loss 0.00.", ""]
    rows = []
    for s in (0.5, 1.0, 1.6):
        r = dict(sigma=s)
        for kind in ("tailnoise", "fullnoise"):
            x = tn[(tn.kind == kind) & (tn.sigma == s) & (tn.q == 100)]
            r[f"{kind} loss@100"] = f"{x.loss.mean():+.2f} ± {x.loss.std(ddof=1):.2f}"
            r[f"{kind} avg_bucket"] = f"{x.avg_bucket.mean():.0f}"
        a, b = tn[(tn.kind == "tailnoise") & (tn.sigma == s) & (tn.q == 100)].loss.mean(), tn[(tn.kind == "fullnoise") & (tn.sigma == s) & (tn.q == 100)].loss.mean()
        r["tail-only / full"] = f"{a / b:.3f}" if abs(b) > 1e-9 else "n/a"
        rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "Loss at q = 1, 10, 100, 1000 for the same rows (mean over the 5 draws):", ""]
    rows = []
    for kind in ("tailnoise", "fullnoise"):
        for s in (0.5, 1.0, 1.6):
            r = dict(noise=kind, sigma=s)
            for q in C.QS:
                x = tn[(tn.kind == kind) & (tn.sigma == s) & (tn.q == q)]
                r[f"loss@{q}"] = f"{x.loss.mean():+.2f} ± {x.loss.std(ddof=1):.2f}"
            rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "Per-draw loss at q = 100:", ""]
    rows = []
    for kind in ("tailnoise", "fullnoise"):
        for s in (0.5, 1.0, 1.6):
            x = tn[(tn.kind == kind) & (tn.sigma == s) & (tn.q == 100)].sort_values("draw")
            rows.append(dict(noise=kind, sigma=s, **{f"d{int(r.draw)}": f"{r.loss:+.2f}" for r in x.itertuples()}))
    L += [md(pd.DataFrame(rows)), ""]
    d1["sigma"] = d1.variant.str.extract(r"noise_s([\d.]+)_d")[0].astype(float)
    cur = d1[(d1.attacker == "est") & (d1.param == 100) & (d1.q == 100)].groupby("sigma").loss.agg(["mean", "std"])
    L += ["Phase 1d full-noise curve for reference (est, qbar = 100, q = 100, 5 draws; `e1d_noise.csv`): " +
          "; ".join(f"sigma {s}: {r['mean']:+.2f} ± {r['std']:.2f}" for s, r in cur.iterrows()) + ".", ""]
    b = es[(es.t == 1_000_000)]
    pick = lambda grp, meth: b[(b.group == grp) & (b.method.str.startswith(meth))].iloc[0]
    L += ["Measured estimator error at t = 1M (REPORT_1d section 3, `e1d_esterror_summary.csv`): " +
          f"tail, per-password dispersion (method B) sigma_hat = {pick('tail', 'B').sigma_hat:.3f} (se over folds {pick('tail', 'B').se_over_folds:.3f}, bias mu = {pick('tail', 'B').bias_mu:+.2f}); "
          f"tail, binned masses (method A) {pick('tail', 'A').sigma_hat:.3f}; head, method B {pick('head', 'B').sigma_hat:.3f}, method A {pick('head', 'A').sigma_hat:.3f}. "
          f"The tail-only sigma = 1.6 row is the one closest to the measured tail sigma_hat ({pick('tail', 'B').sigma_hat:.2f}).", ""]
    p_emp = os.path.join(R, "e1f_tailnoise_emp.csv")
    if os.path.exists(p_emp):
        te = rdcsv("e1f_tailnoise_emp.csv")
        te["kind"] = te.variant.str.split("_").str[0]
        te["sigma"] = te.variant.str.extract(r"_s([\d.]+)_d")[0].astype(float)
        rows = []
        for s in (0.5, 1.0, 1.6):
            r = dict(sigma=s)
            for kind in ("tailnoise", "fullnoise"):
                x = te[(te.kind == kind) & (te.sigma == s) & (te.q == 100)]
                r[f"{kind} loss@100"] = f"{x.loss.mean():+.2f} ± {x.loss.std(ddof=1):.2f}"
            rows.append(r)
        m0 = rdcsv("e1e_headline.csv")
        base = m0[(m0.condition == "M0") & (m0.scheme == "fsb") & (m0.param == 100) & (m0.q == 100)].loss.iloc[0]
        L += ["### 2.1 Extra (not requested): the same experiment with the emp attacker (all of S~)", "",
              f"Same draws, same salts, qbar = 100, q = 100, emp attacker with all of S~ (the clean-estimate loss, sigma = 0, is {base:+.2f}; `e1e_headline.csv`).", "", md(pd.DataFrame(rows)), ""]

    L += ["## 3. Checks and runtimes", "", "```", rd("e1f_tests.txt"), "```", "",
          "Wall times (10-core laptop): " + "; ".join(f"{n}: {_dur(n)}" for n in ("mechanism", "tailnoise", "tailnoise_emp")) + ".", "",
          "## 4. New files", "",
          "`results/`: e1f_mech_groups.csv, e1f_mech_dist.csv, e1f_mech_quantiles.csv, e1f_tailnoise.csv, e1f_tailnoise_emp.csv (extra), logs, time files, e1f_tests.txt, this report. "
          "`e1f_tailnoise*.csv` columns as in the e1d / e1e CSVs; `e1f_mech_*.csv` have their own columns (see headers).", ""]
    open(os.path.join(R, "REPORT_1f.md"), "w").write("\n".join(L))
    print("wrote REPORT_1f.md", len("\n".join(L)))


def _dur(n):
    p = os.path.join(R, f"e1f_{n}_time.txt")
    if not os.path.exists(p):
        return "n/a"
    # each time file holds one line, e.g. 'elapsed: 8 min 29 s (509 s)'
    m = re.search(r"\((\d+(?:\.\d+)?) s", open(p).read())
    if not m:
        return "n/a"
    s = int(round(float(m.group(1))))
    return f"{s // 60} min {s % 60} s"


if __name__ == "__main__":
    main()
