"""Assemble results/REPORT_1e.md from the Phase 1e CSVs (Phase 1c / 1d files are read, never modified). Numbers and method statements only."""
import os

import numpy as np
import pandas as pd

from experiments import common as C
from experiments.report import md, rd
from experiments.report1b import fmt, interp, rdcsv

R = C.RESULTS
QS = C.QS
QBARS = (10, 100, 1000)
CONDS = ("M0", "M1b", "M2x", "M2L")
CLAB = {"M0": "M0", "M1b": "M1b", "M2x": "M2x (len>=8 + Xato)", "M2L": "M2L (len>=8 only)"}


def pick(df, cond, scheme, qb, q, attacker):
    """One row of a results frame. FSB: param == qb. HPB: variant == match_qbar{qb}."""
    x = df[(df.condition == cond) & (df.scheme == scheme) & (df.q == q) & (df.attacker == attacker)]
    x = x[x.param == qb] if scheme == "fsb" else x[x.variant == f"match_qbar{qb}"]
    if scheme == "fsb":
        x = x[x.variant.isin(["fsb_base"])]
    return x.iloc[0] if len(x) else None


def cell(r):
    return "n/a" if r is None else f"{r.loss:+.2f} ±{r.std_over_repeats:.2f}"


def load_est():
    """est attacker (2M list), t = 1M: Phase 1c rows for M0 / M1b / M2x, Phase 1e's e1e_m2l_2m for M2L (1c/1d had no HPB row for M2L)."""
    a = rdcsv("e1c_e2.csv")
    b = rdcsv("e1e_m2l_2m.csv")
    return pd.concat([a[a.condition.isin(["M0", "M1b", "M2x"])], b[b.condition == "M2L"]], ignore_index=True)


def main():
    emp = rdcsv("e1e_headline.csv")
    est = load_est()
    emp2m_src = pd.concat([rdcsv("e1c_e2.csv").query("condition in ['M0','M1b','M2x']"), rdcsv("e1e_m2l_2m.csv").query("condition == 'M2L'")], ignore_index=True)
    L = ["# REPORT 1e (Phase 1e: emp attacker = all of S~)", "",
         "Numbers and method statements only. Phase 1-1d results were not modified; Phase 1e adds `results/e1e_*` files, `experiments/e1e_*.py`, `experiments/report1e.py`, `tests/test_phase1e.py`, "
         "and housekeeping edits (Makefile, README, tests/conftest.py, `c3sim/data.py` env overrides, `experiments/common.py` `n_cand=None`). "
         "Setting: t = 1,000,000; seed 2000; pool A_test (M1b: B_target); 5 repeats x 5,000 targets, same targets as 1c / 1d; units percent / percentage points; ± = sd over the repeats. "
         "**emp** (headline) = attacker with weights from leak counts and a candidate list of **all of S~ (13,125,513 passwords, no generated strings)**; "
         "**est** = attacker with weights p^ and the 2M list, numbers reused from Phase 1c (M2L from `e1e_m2l_2m.csv`, see below). Appendix A holds the 2M-list emp numbers, which are lower bounds (REPORT_1d section 1). "
         "Size-matched HPB uses the same prefix lengths as Phase 1c (l = 14 / 12 / 10 for qbar = 10 / 100 / 1000). Loss = bucket success - baseline success of the same attacker.", ""]

    # ------------------------------------------------------------------ 1 headline
    L += ["## 1. Headline tables, t = 1,000,000", "", "### 1.1 Baseline success (no bucket), percent", ""]
    rows = []
    for c in CONDS:
        r = dict(condition=CLAB[c])
        for q in QS:
            e = pick(emp, c, "fsb", 100, q, "emp")
            s = pick(est, c, "fsb", 100, q, "est")
            r[f"q={q} emp / est"] = f"{e.baseline_success:.2f} / {s.baseline_success:.2f}"
        rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "### 1.2 Loss (percentage points); each cell is emp (all of S~) / est (2M list)", "",
          "`avg_bucket` is the same for both attackers (the scheme's); `cand/bucket` = mean attacker candidates per bucket (emp / est).", ""]
    rows = []
    for c in CONDS:
        for sch in ("fsb", "hpb"):
            for qb in QBARS:
                e1, s1 = pick(emp, c, sch, qb, 1, "emp"), pick(est, c, sch, qb, 1, "est")
                r = dict(condition=CLAB[c], scheme=sch, qbar=qb if sch == "fsb" else f"matched to {qb} (l={int(e1.param)})", avg_bucket=f"{e1.avg_bucket:.0f}",
                         cand_per_bucket=f"{e1.cand_per_bucket:.0f} / {s1.cand_per_bucket:.0f}")
                for q in QS:
                    r[f"loss@{q}"] = f"{cell(pick(emp, c, sch, qb, q, 'emp'))}  /  {cell(pick(est, c, sch, qb, q, 'est'))}"
                rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "### 1.3 Success ratio (attacker success / baseline success) at q = 1 and q = qbar", "",
          "ratio = mean bucket success / mean baseline success; ± = sd of the per-repeat ratios (n/a: some repeat has baseline 0; est M2L has no per-repeat ratio file, ratio of means only). "
          "emp: `e1e_ratio.csv`; est: `e1d_ratio.csv` (M0, M1b, M2x) and `e1e_ratio_m2l_2m.csv` (M2L).", ""]
    re_ = rdcsv("e1e_ratio.csv")
    rs = pd.concat([rdcsv("e1d_ratio.csv"), rdcsv("e1e_ratio_m2l_2m.csv")], ignore_index=True)

    def rat(df, c, sch, qb, q, m):
        x = df[(df.condition == c) & (df.scheme == sch) & (df.qbar == qb) & (df.q == q) & (df.attacker == m)]
        if x.empty:
            return None
        return x.iloc[0]

    def fr(x):
        if x is None or pd.isna(x.ratio):
            return "n/a"
        return f"{x.ratio:.2f}" + (f" ±{x.ratio_sd:.2f}" if not pd.isna(x.ratio_sd) else "")

    rows = []
    for c in CONDS:
        for sch in ("fsb", "hpb"):
            for qb in QBARS:
                for q in sorted({1, qb}):
                    e, s = rat(re_, c, sch, qb, q, "emp"), rat(rs, c, sch, qb, q, "est")
                    rows.append(dict(condition=CLAB[c], scheme=sch, qbar=qb, q=q, avg_bucket=f"{e.avg_bucket:.0f}",
                                     baseline_emp=f"{e.baseline_success:.2f}", success_emp=f"{e.bucket_success:.2f}", ratio_emp=fr(e),
                                     baseline_est=f"{s.baseline_success:.2f}", success_est=f"{s.bucket_success:.2f}", ratio_est=fr(s)))
    L += [md(pd.DataFrame(rows)), ""]
    L += ["Source note for est M2L: Phase 1c/1d had FSB rows only (`e1d_ablation.csv`); `e1e_m2l_2m.csv` reruns M2L FSB and size-matched HPB with the 2M list, est and emp, same seeds "
          "(its FSB rows equal `e1d_ablation.csv`).", ""]

    # ------------------------------------------------------------------ 2 t sweep
    ts = rdcsv("e1e_tsweep.csv")
    p10 = os.path.join(R, "e1e_tsweep_10M.csv")
    if os.path.exists(p10):
        ts = pd.concat([ts, rdcsv("e1e_tsweep_10M.csv")], ignore_index=True)
    L += ["## 2. t sweep, emp = all of S~, FSB qbar = 100", "",
          "Conditions M0 and M2x, seed 2000, same targets across t. `base@q` = no-bucket success of the attacker; loss at q = 1, 10, 100, 1000.", ""]
    rows = []
    for (t, c), g in ts.groupby(["t", "condition"], sort=True):
        g = g.set_index("q")
        r = dict(t=f"{int(t):,}", condition=CLAB[c], avg_bucket=f"{g.avg_bucket.iloc[0]:.0f}", cand_per_bucket=f"{g.cand_per_bucket.iloc[0]:.0f}")
        for q in QS:
            r[f"base@{q}"] = f"{g.baseline_success[q]:.2f}"
        for q in QS:
            r[f"loss@{q}"] = f"{g.loss[q]:+.2f} ±{g.std_over_repeats[q]:.2f}"
        rows.append(r)
    L += [md(pd.DataFrame(rows)), ""]
    if os.path.exists(p10):
        L += ["t = 10,000,000 ran (it fit in memory; see section 5 for its time and peak memory).", ""]
    else:
        L += ["t = 10,000,000 did not complete / was skipped; log: `" + rd("e1e_tsweep_10M_log.txt").strip().split("\n")[-1][:200] + "`.", ""]

    # ------------------------------------------------------------------ 3 est convergence
    ec = rdcsv("e1e_estconv.csv")
    ec["cand"] = ec.variant.str.split(" ").str[-1]
    ec["base"] = ec.variant.str.rsplit(" ", n=1).str[0]
    L += ["## 3. est attacker convergence, t = 1,000,000: candidate list 2M vs all of S~", "",
          "Both lists rerun here with the same targets (seed 2000). est attacker; FSB qbar in {10, 100, 1000}, conditions M0 and M2x, plus M3 sigma = 0.75, noise draw d1 "
          "(salt `c3sim-noise-v1-d1`), qbar = 100. Cells: loss ± sd; `diff` = all minus 2M.", ""]
    rows = []
    for (c, b, qb), g in ec.groupby(["condition", "base", "param"], sort=False):
        for q in QS:
            a2 = g[(g.cand == "cand2M") & (g.q == q)].iloc[0]
            al = g[(g.cand == "candall") & (g.q == q)].iloc[0]
            rows.append(dict(condition=c, variant=b, qbar=qb, q=q, avg_bucket=f"{a2.avg_bucket:.0f}", cand_per_bucket_2M_all=f"{a2.cand_per_bucket:.0f} / {al.cand_per_bucket:.0f}",
                             baseline_2M_all=f"{a2.baseline_success:.2f} / {al.baseline_success:.2f}", loss_2M=f"{a2.loss:+.2f} ±{a2.std_over_repeats:.2f}",
                             loss_all=f"{al.loss:+.2f} ±{al.std_over_repeats:.2f}", diff=f"{al.loss - a2.loss:+.2f}"))
    L += [md(pd.DataFrame(rows)), ""]
    m0 = ec[(ec.condition == "M0") & (ec.q <= ec.param)]
    m2 = ec[(ec.condition == "M2x") & (ec.q <= ec.param)]
    m3 = ec[ec.condition == "M3"]
    L += ["Statements computed from the table:", "",
          f"- M0, q <= qbar (FSB qbar 10 / 100 / 1000), maximum |loss|: 2M list {m0[m0.cand == 'cand2M'].loss.abs().max():.2f}, all of S~ {m0[m0.cand == 'candall'].loss.abs().max():.2f}. "
          f"est loss at q <= qbar {'stays at 0' if m0[m0.cand == 'candall'].loss.abs().max() < 0.05 else 'does NOT stay at 0'} with all of S~ (M0).",
          f"- M2x, q <= qbar, maximum |loss|: 2M list {m2[m2.cand == 'cand2M'].loss.abs().max():.2f}, all of S~ {m2[m2.cand == 'candall'].loss.abs().max():.2f}.",
          "- M3 sigma = 0.75, d1, qbar = 100: loss at q = 1 / 10 / 100 / 1000, 2M -> all: " +
          "; ".join(f"q={q}: {m3[(m3.cand == 'cand2M') & (m3.q == q)].loss.iloc[0]:+.2f} -> {m3[(m3.cand == 'candall') & (m3.q == q)].loss.iloc[0]:+.2f} "
                    f"(diff {m3[(m3.cand == 'candall') & (m3.q == q)].loss.iloc[0] - m3[(m3.cand == 'cand2M') & (m3.q == q)].loss.iloc[0]:+.2f})" for q in QS) +
          f". Largest absolute change across the four q: {max(abs(m3[(m3.cand == 'candall') & (m3.q == q)].loss.iloc[0] - m3[(m3.cand == 'cand2M') & (m3.q == q)].loss.iloc[0]) for q in QS):.2f}.", ""]

    # ------------------------------------------------------------------ 4 fixes vs full emp
    fx = rdcsv("e1e_fix.csv")
    L += ["## 4. Fixes against the full emp attacker (all of S~), t = 1,000,000", "",
          "Variants: `fsb_base`; `smoothed` (interpolated Kneser-Ney 3-gram); `cal_iso_w0.5` (**exploratory**: the Phase 1b calibration, isotonic, 0.5-decade bins, built from the t = 1M pipeline of "
          "`e1c_fix.py`, i.e. cross-fit on a 90/10 split of A_train, with no dev tuning and evaluated on A_test seed 2000 like every other row here). "
          "Each variant is swept over qbar 1, 3, 10, 30, 100, 300, 1000, 3000 (as `e1c_base_sweep.csv`) and compared at equal average bucket size by log-linear interpolation of the loss along the sweep "
          "(nan = the sweep does not reach that size).", ""]
    rows = []
    for c in ("M0", "M2x"):
        for v in ("fsb_base", "smoothed", "cal_iso_w0.5"):
            d = fx[(fx.condition == c) & (fx.variant == v)]
            r = dict(condition=CLAB[c], variant=v)
            for q in (100, 1000):
                for b in (2000, 6500, 20000):
                    r[f"loss q={q} @{b}"] = fmt(interp(d, q, b))
            rows.append(r)
    L += [md(pd.DataFrame(rows)), "", "Sweep rows (loss ± sd at q = 1, 10, 100, 1000):", ""]
    for c in ("M0", "M2x"):
        rows = []
        for v in ("fsb_base", "smoothed", "cal_iso_w0.5"):
            for qb in sorted(fx.param.unique()):
                g = fx[(fx.condition == c) & (fx.variant == v) & (fx.param == qb)].set_index("q")
                r = dict(variant=v, qbar=int(qb), avg_bucket=f"{g.avg_bucket.iloc[0]:.0f}")
                for q in QS:
                    r[f"loss@{q}"] = f"{g.loss[q]:+.2f} ±{g.std_over_repeats[q]:.2f}"
                rows.append(r)
        L += [f"### {CLAB[c]}", "", md(pd.DataFrame(rows)), ""]

    # ------------------------------------------------------------------ 5 cost
    cost = rdcsv("e1e_cost.csv")
    runs = rdcsv("e1e_runs.csv")
    L += ["## 5. Runtime and memory of the all-of-S~ attacker", "",
          "### 5.1 One cold run in a fresh process (`e1e_cost.py`): M0, FSB qbar = 100, t = 1M, 5 x 5,000 targets, run alone on the 10-core laptop", "",
          "`world_build` = splits + 3-gram + p^ for all of S~; `attacker_build` = candidate list (est: ordering S~ by p^); `index_build` = gamma for every candidate and the sorted-class lookup; "
          "`games` = 25,000 bucket queries and scoring. `peak_rss_gb` = peak resident memory of the whole process.", "", md(cost), ""]
    ok = runs[runs.label.str.contains("fsb|hpb")]
    L += ["### 5.2 Per-run time and memory inside the headline job (`e1e_runs.csv`, one process, all-of-S~ emp)", "",
          f"{len(ok)} runs (5 repeats x 5,000 targets each): seconds min / median / max = {ok.seconds.min():.1f} / {ok.seconds.median():.1f} / {ok.seconds.max():.1f}; "
          f"process peak resident memory over the job {ok.peak_rss_so_far_gb.max():.2f} GB (resident after the runs {ok.rss_after_gb.min():.2f} to {ok.rss_after_gb.max():.2f} GB). "
          f"The first run of each condition includes building the attacker and its index.", "", md(runs[["label", "seconds", "rss_after_gb", "peak_rss_so_far_gb"]]), ""]
    tr = []
    for t in (100_000, 300_000, 1_000_000, 3_000_000, 10_000_000):
        p = os.path.join(R, f"e1e_tsweep_runs_t{t}.csv") if t != 10_000_000 else os.path.join(R, f"e1e_tsweep_10M_runs_t{t}.csv")
        if not os.path.exists(p):
            p = os.path.join(R, f"e1e_tsweep_runs_t{t}.csv")
        if os.path.exists(p):
            x = pd.read_csv(p)
            tr.append(dict(t=f"{t:,}", **{r.label: f"{r.seconds:.0f} s" for r in x.itertuples()}, peak_rss_gb=x.peak_rss_so_far_gb.max()))
    L += ["### 5.3 t sweep: time per step and peak memory (one process per group; t = 10M in its own process)", "", md(pd.DataFrame(tr)) if tr else "(no per-run files)", ""]

    # ------------------------------------------------------------------ appendix A
    L += ["## Appendix A. emp attacker with the 2M list (lower bounds), t = 1,000,000", "",
          "Rows reused from Phase 1c (`e1c_e2.csv`: M0, M1b, M2x) and `e1e_m2l_2m.csv` (M2L). Compare with section 1.2 (all of S~). Loss ± sd at q = 1, 10, 100, 1000.", ""]
    rows = []
    for c in CONDS:
        for sch in ("fsb", "hpb"):
            for qb in QBARS:
                e1 = pick(emp2m_src, c, sch, qb, 1, "emp")
                r = dict(condition=CLAB[c], scheme=sch, qbar=qb if sch == "fsb" else f"matched to {qb} (l={int(e1.param)})", avg_bucket=f"{e1.avg_bucket:.0f}",
                         cand_per_bucket=f"{e1.cand_per_bucket:.0f}")
                for q in QS:
                    r[f"loss@{q}"] = cell(pick(emp2m_src, c, sch, qb, q, "emp"))
                rows.append(r)
    L += [md(pd.DataFrame(rows)), ""]

    L += ["## 6. Checks, housekeeping and runtimes", "", "```", rd("e1e_tests.txt"), "```", "",
          "Housekeeping done in this phase: `Makefile` (targets for phases 1b-1e, `fetch-xato`, guarded one-shot fresh runs, run order in the header), `README.md` (phase section, Xato fetch, exact run order, "
          "timings), corpus-dependent tests skip when data is absent (`tests/conftest.py` `corpora` fixture; `data.corpora_available()`; `C3SIM_DATA` / `C3SIM_CACHE` override), "
          "`tests/test_phase1e.py`.", "", "```", rd("e1e_runtimes.txt"), "```", "",
          "## 7. New files", "",
          "`results/`: e1e_headline.csv, e1e_ratio.csv, e1e_m2l_2m.csv, e1e_ratio_m2l_2m.csv, e1e_runs.csv, e1e_tsweep.csv, e1e_tsweep_10M.csv (if it ran), e1e_tsweep*_runs_t*.csv, e1e_estconv.csv, "
          "e1e_fix.csv, e1e_fix_runs.csv, e1e_cost.csv, logs, time files, e1e_tests.txt, e1e_runtimes.txt, this report. Columns as in e1c / e1d CSVs.", ""]
    open(os.path.join(R, "REPORT_1e.md"), "w").write("\n".join(L))
    print("wrote REPORT_1e.md", len("\n".join(L)))


if __name__ == "__main__":
    main()
