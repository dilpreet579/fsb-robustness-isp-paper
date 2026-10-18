"""Assemble results/REPORT_1b.md from the Phase 1b CSVs (and the Phase 1 CSVs, read only). Numbers and pass/fail only."""
import json
import os
import re

import numpy as np
import pandas as pd

from experiments import common as C
from experiments import e1 as E1
from experiments.report import md, rd, table

R = C.RESULTS
QS = C.QS


def rdcsv(n):
    return pd.read_csv(os.path.join(R, n))


def interp(d, q, budget):
    d = d[d.q == q].sort_values("avg_bucket")
    if len(d) < 2 or not (d.avg_bucket.min() <= budget <= d.avg_bucket.max()):
        return np.nan
    return float(np.interp(np.log(budget), np.log(d.avg_bucket), d.loss))


def fmt(x):
    return "nan" if pd.isna(x) else f"{x:.2f}"


def interp_table(df, keys, budgets=(2000, 6500)):
    rows = []
    for k, g in df.groupby(keys, sort=False):
        r = dict(zip(keys, k if isinstance(k, tuple) else (k,)))
        for q in (100, 1000):
            for b in budgets:
                r[f"loss q={q} @{b}"] = fmt(interp(g, q, b))
        rows.append(r)
    return pd.DataFrame(rows)


def m1a_cand():
    """cand/bucket of the Phase-1 M1 rows, parsed from the E2 log (the CSV does not carry it)."""
    out = {}
    for m in re.finditer(r"\[M1/(est|emp)\] fsb fsb_base\s+param=(\d+).*?cand/bucket=(\d+)", rd("E2_log.txt")):
        out[(m.group(1), int(m.group(2)))] = int(m.group(3))
    return out


def main():
    L = ["# REPORT 1b (Phase 1b: t sensitivity, M1b, headline table, calibration fix)", "",
         "Numbers only. Existing results and CSVs from Phase 1 were not modified; Phase 1b adds `results/e1b_*` files and `experiments/e1b_*.py`, "
         "`experiments/report1b.py`, `c3sim/calibration.py`. Units as in REPORT.md: percent / percentage points; ± = sd of per-repeat loss over 5 repeats of 5,000 targets. "
         "`est` = attacker weights p^ (the deployed estimate), `emp` = leak counts. Seeds: E1 1000, E2 2000, calibration dev 5000, fresh 6000.", ""]

    # ---------------------------------------------------------------------------------------------- item 1
    L += ["## 1. t sensitivity (histogram head t = 100,000 vs 1,000,000)", "",
          "t = 100,000 rows are the existing `e1.csv` / `e2.csv` (unchanged); t = 1,000,000 rows are new (`e1b_t_e1.csv`, `e1b_t_m2.csv`), same seeds and targets. "
          "HPB does not depend on t (its rows are identical); FSB bucket sizes and the est attacker's list do.", ""]
    e1a, e1t = rdcsv("e1.csv"), rdcsv("e1b_t_e1.csv")
    chk = E1.check(e1t, os.path.join(R, "e1b_t_E1_check.txt"))
    L += ["### 1.1 E1 (M0) acceptance checks at t = 1,000,000", "", "```", rd("e1b_t_E1_check.txt"), "```", "",
          "(t = 100,000: see `E1_check.txt`, est PASS, emp FAIL.)", ""]
    for m in C.MODELS:
        for lab, d in (("t = 100,000", e1a), ("t = 1,000,000", e1t)):
            L += [f"### 1.2 E1 M0, attacker `{m}`, {lab}", "", md(table(d[d.attacker == m], ["scheme", "param"])), ""]
    e2 = rdcsv("e2.csv")
    m2a = e2[(e2.condition == "M2") & (e2.attacker == "est")]
    m2t = rdcsv("e1b_t_m2.csv")
    L += ["### 1.3 E2 M2 (est attacker; policy length >= 8 and not in top370_A_train)", "",
          "t = 100,000:", "", md(table(m2a, ["scheme", "variant", "param"])), "", "t = 1,000,000:", "", md(table(m2t, ["scheme", "variant", "param"])), ""]
    L += ["### 1.4 Top-20 guesses of the est attacker (no bucket) under each t", "", "```", rd("e1b_top20.txt"), "```", ""]

    # ---------------------------------------------------------------------------------------------- item 2
    mb = rdcsv("e1b_m1b.csv")
    m1a = e2[e2.condition == "M1"]
    ca = m1a_cand()
    L += ["## 2. M1b: server estimate from A_train, targets B_target, attacker = p^ over the top 2M of S~", "",
          "M1a = the Phase 1 M1 (attacker trained on B_attack, 98,735 candidates). M1b attacker candidate list: top 2,000,000 of S~ by p^ (est) or by count (emp, extra). "
          "`cand_per_bucket` = mean number of attacker candidates in the bucket; q is saturated when cand_per_bucket < q (the attacker guesses the whole bucket).", ""]
    for m in C.MODELS:
        L += [f"### M1b, attacker `{m}`", "", md(table(mb[mb.attacker == m], ["scheme", "variant", "param"])), ""]
    cpb = mb[(mb.attacker == "est") & (mb.q == 1)][["scheme", "variant", "param", "cand_per_bucket"]]
    satd = {}
    for r in cpb.itertuples():
        qs_ = [q for q in QS if r.cand_per_bucket < q]
        satd[(r.scheme, r.param)] = (r.cand_per_bucket, qs_)
    fsb_sat = {k: v for k, v in satd.items() if k[0] == "fsb" and v[1]}
    hpb_sat = {k: v for k, v in satd.items() if k[0] == "hpb" and v[1]}
    L += ["Candidates per bucket in M1b (est): " + "; ".join(f"{r.scheme} {r.variant} param={r.param}: {r.cand_per_bucket:.0f}" for r in cpb.itertuples()) + ".",
          "Saturated (cand_per_bucket < q) FSB configurations: " + ("; ".join(f"qbar={k[1]} at q in {v[1]}" for k, v in fsb_sat.items()) or "none") +
          ". Saturated HPB configurations: " + ("; ".join(f"l={k[1]} ({v[0]:.0f} candidates) at q in {v[1]}" for k, v in hpb_sat.items()) or "none") +
          ". M1b is therefore not saturated for FSB at q <= 100 (all q <= 100 columns are informative); at q=1000 only qbar=10 is saturated.", "",
          "M1a candidates per bucket (parsed from E2_log.txt): " + "; ".join(f"FSB qbar={k[1]} ({k[0]}): {v}" for k, v in sorted(ca.items())) + ".", "",
          "### M1a vs M1b, FSB, loss (est attacker)", ""]
    rows = []
    for qb in (10, 100, 1000):
        for q in (1, 10, 100, 1000):
            a = m1a[(m1a.attacker == "est") & (m1a.scheme == "fsb") & (m1a.param == qb) & (m1a.q == q)].iloc[0]
            b = mb[(mb.attacker == "est") & (mb.scheme == "fsb") & (mb.param == qb) & (mb.q == q)].iloc[0]
            rows.append(dict(qbar=qb, q=q, M1a_baseline=a.baseline_success, M1a_loss=f"{a.loss:+.2f} ±{a.std_over_repeats:.2f}",
                             M1b_baseline=b.baseline_success, M1b_loss=f"{b.loss:+.2f} ±{b.std_over_repeats:.2f}"))
    L += [md(pd.DataFrame(rows)), ""]

    # ---------------------------------------------------------------------------------------------- item 3
    base = rdcsv("e1b_base_sweep.csv")
    L += ["## 3. Headline table: loss at q = qbar (percentage points)", "",
          "Source: seed 2000 for every row (same targets across rows of one pool). M0, M1a, M2 (top370_A_train), M3 are the existing `e2.csv`; M1b is new. "
          "† = saturated (mean attacker candidates per bucket < q); M1a values from E2_log.txt. "
          "M3 rows: `avg bucket` is the noisy scheme's own average bucket size, `base@same size` = base FSB loss at q = qbar, M0 pool, interpolated "
          "(log-linear in average bucket size) along the dense base sweep `e1b_base_sweep.csv` (qbar 1..3000); nan = outside the sweep. "
          "M2 with Twitter's banned list: **not run** (section 4).", ""]
    rows = []
    srcs = [("M0", e2[(e2.condition == "M0") & (e2.variant == "fsb_base")], None), ("M1a", m1a, "M1a"), ("M1b", mb[mb.scheme == "fsb"], "M1b"),
            ("M2 top370", e2[(e2.condition == "M2") & (e2.scheme == "fsb")], None)]
    for s_ in (0.5, 1.0, 1.5):
        srcs.append((f"M3 sigma={s_}", e2[(e2.condition == "M3") & (e2.variant == f"noise_s{s_}")], "M3"))
    for lab, d, kind in srcs:
        for qb in (10, 100, 1000):
            r = dict(condition=lab, qbar=qb)
            for m in C.MODELS:
                x = d[(d.attacker == m) & (d.scheme == "fsb") & (d.param == qb) & (d.q == qb)]
                if x.empty:
                    r[f"{m} loss"] = "n/a"
                    continue
                x = x.iloc[0]
                sat_ = ""
                if kind == "M1a" and ca.get((m, qb), 1e9) < qb:
                    sat_ = " †"
                if kind == "M1b" and x.cand_per_bucket < qb:
                    sat_ = " †"
                r[f"{m} loss"] = f"{x.loss:+.2f} ±{x.std_over_repeats:.2f}{sat_}"
                r["avg bucket"] = f"{x.avg_bucket:.0f}"
                if kind == "M3":
                    bm = base[(base.attacker == m) & (base.scheme == "fsb") & (base.condition == "M0")]
                    r[f"{m} base@same size"] = fmt(interp(bm, qb, x.avg_bucket))
            rows.append(r)
    df = pd.DataFrame(rows).fillna("")
    L += [md(df), ""]

    # ---------------------------------------------------------------------------------------------- item 4
    L += ["## 4. M2 with Twitter's banned list", "",
          "**Not run.** The fetch you approved targeted `Passwords/Common-Credentials` in SecLists. `twitter-banned.txt` returned HTTP 404 there, and a single directory "
          "listing of that folder (39 entries) shows no Twitter or banned-password file. I did not substitute another list. "
          "Provide the file (or its path in the repo) and M2tw is a one-run addition; see QUESTIONS Q11.", ""]

    # ---------------------------------------------------------------------------------------------- item 5
    dev = rdcsv("e1b_fix_dev.csv")
    L += ["## 5. Calibrated tail estimate", "",
          "Method (`c3sim/calibration.py`): cross-fit. Split A_train accounts 90/10 (seed 104); fit histogram head + 3-gram on the 90%; in each log10(p^) bin the "
          "factor r = held-out tail mass / model tail mass (the model mass by sampling 20M strings from the 3-gram, head strings excluded exactly); "
          "apply r to the tail p^ of the estimator trained on all of A_train. Head (top 100,000) unchanged. It is a public function of the string. "
          "A_dev is used only as the design target pool; A_fresh was touched once (5.3). The est attacker uses the deployed (calibrated) p^ for the fix and plain p^ for the base. "
          "Equal bucket size = compare at average bucket sizes interpolated along the qbar sweep (10, 30, 100, 300, 1000, 3000).", "",
          "### 5.1 Variants tried (all on A_dev / B_dev; nothing here is the reported result)", "",
          "- `cal_w0.5`: 0.5-decade log bins. `cal_w1.0`: 1-decade bins. `cal_iso_w0.5`: 0.5-decade bins, then isotonic (non-decreasing) regression of the calibrated value on p^ (pool-adjacent-violators, weighted by model mass).", "",
          "```", "\n".join(l for l in rd("e1b_fix_dev_log.txt").split("\n") if l.startswith("[cal")), "```", "", "```", rd("e1b_fix_selection.txt"), "```", "",
          "Dev loss interpolated to equal bucket size:", "", md(interp_table(dev, ["condition", "attacker", "variant"])), ""]
    fr_path = os.path.join(R, "e1b_fix_fresh.csv")
    if os.path.exists(fr_path):
        fr = rdcsv("e1b_fix_fresh.csv")
        best = json.load(open(os.path.join(R, "e1b_fix_selection.json")))["best"]
        L += [f"### 5.2 Fresh pool (A_fresh / B_fresh, seed 6000), run once: fsb_base vs {best} (selected on dev)", "",
              "Loss interpolated to equal average bucket size (q = 100 and 1000; 2,000 and 6,500 entries):", ""]
        fr = fr.assign(scheme_variant=fr.variant)
        L += [md(interp_table(fr, ["condition", "attacker", "variant"])), "", "Per-qbar rows (loss at q = 1, 10, 100, 1000):", ""]
        for m in C.MODELS:
            L += [f"#### attacker `{m}`", "", md(table(fr[fr.attacker == m], ["condition", "variant", "param"])), ""]
        # direct comparison at q = qbar for the headline qbars
        L += ["Loss at q = qbar (fresh pool) base vs fix, same qbar (bucket sizes differ, see avg bucket):", ""]
        rows = []
        for c_ in sorted(fr.condition.unique()):
            for v in sorted(fr[fr.condition == c_].variant.unique()):
                for qb in (10, 100, 1000):
                    for m in C.MODELS:
                        x = fr[(fr.condition == c_) & (fr.variant == v) & (fr.attacker == m) & (fr.param == qb) & (fr.q == qb)]
                        if len(x):
                            rows.append(dict(condition=c_, variant=v, qbar=qb, attacker=m, avg_bucket=f"{x.avg_bucket.iloc[0]:.0f}", loss=f"{x.loss.iloc[0]:+.2f} ±{x.std_over_repeats.iloc[0]:.2f}"))
        L += [md(pd.DataFrame(rows)), ""]
    else:
        L += ["### 5.2 Fresh pool", "", "(not run yet)", ""]

    L += ["## 5.3 Checks for Phase 1b", "",
          "- Calibration mechanics (`tests/test_calibration.py`, PASS): sampled model tail mass vs exact expectation, calibrated tail mass = held-out tail mass, factors positive, head unchanged, PAV monotone.",
          "- E1 acceptance checks at t = 1,000,000: section 1.1 (est PASS, emp FAIL).",
          "- Process note: the first run of `e1b_basics.py` matched M1b's HPB prefix to the t = 1,000,000 FSB bucket sizes (bug). M1b moved to `e1b_m1b.py` and was rerun; "
          "the M1b lines in `e1b_basics_log.txt` are from the buggy run and are superseded by `e1b_m1b_log.txt` / `e1b_m1b.csv`. The other `e1b_basics` outputs were not affected.",
          "- The fresh-pool calibration run was done once (`e1b_fix_fresh.csv` is guarded against reruns).", "",
          "```", rd("e1b_tests.txt"), "```", "",
          "## 6. Runtimes", "", "```", rd("e1b_runtimes.txt"), "```", "",
          "## 7. New files", "",
          "`results/`: e1b_t_e1.csv, e1b_t_m2.csv, e1b_top20.txt, e1b_m1b.csv, e1b_base_sweep.csv, e1b_fix_dev.csv, e1b_fix_fresh.csv, e1b_fix_selection.{txt,json}, "
          "e1b_cal_table_*.csv (the calibration bins), e1b_t_E1_check.txt, logs, this report. Columns as in `e1.csv` plus `t` and `cand_per_bucket`. "
          "Code: `experiments/e1b_basics.py`, `experiments/e1b_fix.py`, `experiments/report1b.py`, `c3sim/calibration.py`; additive edits to `common.py` "
          "(World `postproc`, condition `M1b`, extra columns) and `estimators.py` (`phat_head`).", ""]
    open(os.path.join(R, "REPORT_1b.md"), "w").write("\n".join(L))
    print("wrote REPORT_1b.md", len("\n".join(L)))


if __name__ == "__main__":
    main()
