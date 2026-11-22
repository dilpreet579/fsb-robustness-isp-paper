"""Paper number map: every number the text may quote, computed by code from results/*.csv -> paper/numbers.csv and paper/numbers.md.
Columns of numbers.csv: id, claim (C1..C5), description, value, unit, source_csv, filter (column=value pairs), plus the recipe columns op, column, source_csv2, filter2, extra
that paper/check_numbers.py needs to recompute the value. Frozen framing: est = weights p^, 2M list; emp = weights from leak counts, ALL of S~; t = 1M unless stated; loss in pp.
  C1 reproduction     C2 noise tolerance     C3 count-aware attacker     C4 mechanism     C5 attacker cost     C6 floor on gamma (Phase 1g, fresh pool)"""
import os

import numpy as np
import pandas as pd

from experiments.paper_common import PAPER
from experiments.paper_numlib import compute

ROWS = []
QBARS = (10, 100, 1000)
CONDS4 = ("M0", "M1b", "M2x", "M2L")


def add(claim, id_, desc, unit, op, src, filt="", col="loss", src2="", filt2="", extra=""):
    row = dict(id=id_, claim=claim, description=desc, unit=unit, source_csv=src, filter=filt, op=op, column=col, source_csv2=src2, filter2=filt2, extra=extra)
    row["value"] = compute(row)
    ROWS.append(row)


def main():
    import json
    # ------------------------------------------------------------------------------------------------ C1 reproduction (est, 2M list)
    for c in ("M0", "M1b", "M2x"):
        for qb in QBARS:
            hp = f"condition={c};scheme=hpb;variant=match_qbar{qb};attacker=est"
            fs = f"condition={c};scheme=fsb;variant=fsb_base;param={qb};attacker=est"
            add("C1", f"C1_{c}_qbar{qb}_hpb_l", f"{c}: prefix length l of the size-matched HPB for qbar={qb}", "bits", "value", "e1c_e2.csv", hp + ";q=1", "param")
            add("C1", f"C1_{c}_qbar{qb}_hpb_avg", f"{c}: average bucket size of the matched HPB (qbar={qb})", "entries", "value", "e1c_e2.csv", hp + ";q=1", "avg_bucket")
            add("C1", f"C1_{c}_qbar{qb}_fsb_avg", f"{c}: average bucket size of FSB qbar={qb}", "entries", "value", "e1c_e2.csv", fs + ";q=1", "avg_bucket")
            for q, tag in ((1, "q1"), (qb, "qbar")):
                add("C1", f"C1_{c}_qbar{qb}_hpb_est_loss_{tag}", f"{c}: size-matched HPB loss, est, q={q} (qbar={qb})", "pp", "value", "e1c_e2.csv", hp + f";q={q}")
            add("C1", f"C1_{c}_qbar{qb}_fsb_est_loss_qbar", f"{c}: FSB loss, est, q=qbar={qb}", "pp", "value", "e1c_e2.csv", fs + f";q={qb}")
            add("C1", f"C1_{c}_qbar{qb}_fsb_est_maxabs_q_le_qbar", f"{c}: FSB est, max |loss| over q <= qbar={qb}", "pp", "max_abs_q_le_param", "e1c_e2.csv", fs)
    # ------------------------------------------------------------------------------------------------ C2 noise tolerance (est)
    for qb in QBARS:
        for op, nm in (("crossing5_mean", "mean"), ("crossing5_sd", "sd")):
            add("C2", f"C2_cross5_est_qbar{qb}_{nm}", f"M3 (noise on all strings), est: sigma at which the loss at q=qbar={qb} reaches 5 points, {nm} over 5 noise draws", "sigma", op,
                "e1d_noise.csv", extra=json.dumps({"qbar": qb, "attacker": "est"}))
    for grp in ("head", "tail"):
        for m, mn in (("B per-password dispersion (stored passwords)", "B"), ("A binned masses (all strings)", "A")):
            f = f"t=1000000;group={grp};method={m}"
            add("C2", f"C2_sigmahat_{grp}_{mn}", f"estimator error sigma_hat, {grp}, method {mn} ({'per-password dispersion' if mn == 'B' else 'binned masses'}), t=1M", "sigma", "value",
                "e1d_esterror_summary.csv", f, "sigma_hat")
        fb = f"t=1000000;group={grp};method=B per-password dispersion (stored passwords)"
        add("C2", f"C2_sigmahat_{grp}_B_se", f"standard error over 5 folds of sigma_hat ({grp}, method B)", "sigma", "value", "e1d_esterror_summary.csv", fb, "se_over_folds")
        add("C2", f"C2_bias_{grp}_B", f"bias mu = log(true / p^) ({grp}, method B; positive = p^ too small)", "log units", "value", "e1d_esterror_summary.csv", fb, "bias_mu")
    # ------------------------------------------------------------------------------------------------ C3 count-aware attacker (emp, all of S~)
    for c in CONDS4:
        for qb in QBARS:
            fs = f"condition={c};scheme=fsb;variant=fsb_base;param={qb};attacker=emp"
            hp = f"condition={c};scheme=hpb;variant=match_qbar{qb};attacker=emp"
            add("C3", f"C3_{c}_qbar{qb}_emp_fsb_loss_qbar", f"{c}: FSB loss, emp (all of S~), q=qbar={qb}", "pp", "value", "e1e_headline.csv", fs + f";q={qb}")
            add("C3", f"C3_{c}_qbar{qb}_emp_fsb_loss_qbar_sd", f"{c}: sd over repeats of the above", "pp", "value", "e1e_headline.csv", fs + f";q={qb}", "std_over_repeats")
            add("C3", f"C3_{c}_qbar{qb}_emp_hpb_loss_qbar", f"{c}: matched-HPB loss, emp, q=qbar={qb}", "pp", "value", "e1e_headline.csv", hp + f";q={qb}")
            for q, tag in ((qb, "qbar"), (1, "q1")):
                add("C3", f"C3_{c}_qbar{qb}_frac_removed_{tag}", f"{c}: fraction of the matched-HPB loss removed by FSB, emp, q={q} (qbar={qb}); 1 - FSB/HPB", "fraction", "frac_removed",
                    "e1e_headline.csv", fs + f";q={q}", "loss", "e1e_headline.csv", hp + f";q={q}")
            add("C3", f"C3_{c}_qbar{qb}_emp_fsb_loss_q1", f"{c}: FSB loss, emp, q=1 (qbar={qb})", "pp", "value", "e1e_headline.csv", fs + ";q=1")
            add("C3", f"C3_{c}_qbar{qb}_emp_hpb_loss_q1", f"{c}: matched-HPB loss, emp, q=1 (qbar={qb})", "pp", "value", "e1e_headline.csv", hp + ";q=1")
    for qb in QBARS:
        for sch in ("fsb", "hpb"):
            f = f"condition=M2x;scheme={sch};qbar={qb};q=1;attacker=emp"
            add("C3", f"C3_M2x_qbar{qb}_{sch}_ratio_q1", f"M2x: success ratio (attacker success / baseline success), {sch.upper()}, emp, q=1 (qbar={qb})", "ratio", "value", "e1e_ratio.csv", f, "ratio")
            add("C3", f"C3_M2x_qbar{qb}_{sch}_ratio_q1_sd", f"M2x: sd over repeats of the above ratio ({sch.upper()}, qbar={qb})", "ratio", "value", "e1e_ratio.csv", f, "ratio_sd")
    for c in ("M0", "M1b", "M2x", "M2L"):
        add("C3", f"C3_{c}_baseline_q1", f"{c}: baseline success of the emp attacker at q=1", "%", "value", "e1e_headline.csv",
            f"condition={c};scheme=fsb;variant=fsb_base;param=100;attacker=emp;q=1", "baseline_success")
    # ------------------------------------------------------------------------------------------------ C4 mechanism
    for c in ("M0", "M2x"):
        for sch in ("fsb", "hpb"):
            for q in (1, 100):
                for g in ("head", "tail", "none", "total"):
                    add("C4", f"C4_{c}_{sch}_q{q}_{g}_contrib", f"{c}, {sch.upper()}, q={q}: loss contribution of the {g} group (share x (success - baseline))", "pp", "value",
                        "e1f_mech_groups.csv", f"condition={c};scheme={sch};q={q};group={g}", "contrib")
                add("C4", f"C4_{c}_{sch}_q{q}_tail_guess_rate", f"{c}, {sch.upper()}, q={q}: share of stored-but-not-head targets guessed", "%", "value",
                    "e1f_mech_groups.csv", f"condition={c};scheme={sch};q={q};group=tail", "succ")
                add("C4", f"C4_{c}_{sch}_q{q}_head_guess_rate", f"{c}, {sch.upper()}, q={q}: share of head targets guessed", "%", "value",
                    "e1f_mech_groups.csv", f"condition={c};scheme={sch};q={q};group=head", "succ")
        for g in ("head", "tail", "none"):
            add("C4", f"C4_{c}_share_{g}", f"{c}: share of targets in the {g} group", "%", "value", "e1f_mech_groups.csv", f"condition={c};scheme=fsb;q=1;group={g}", "share")
        for q in (1, 100):
            nf = f"condition={c};scheme=fsb;q={q};subset=newly_gained;group=all"
            add("C4", f"C4_{c}_q{q}_newly_leak12", f"{c}, FSB, q={q}: share of newly gained targets with leak count 1 or 2", "%", "sum", "e1f_mech_dist.csv",
                nf + ";variable=leak_count;bin=1|2", "share_pct")
            add("C4", f"C4_{c}_q{q}_newly_gamma_median", f"{c}, FSB, q={q}: median gamma of the newly gained targets", "gamma", "value", "e1f_mech_quantiles.csv", nf + ";variable=gamma", "p50")
            add("C4", f"C4_{c}_q{q}_newly_leak_median", f"{c}, FSB, q={q}: median leak count of the newly gained targets", "count", "value", "e1f_mech_quantiles.csv",
                nf + ";variable=leak_count", "p50")
            add("C4", f"C4_{c}_q{q}_newly_n", f"{c}, FSB, q={q}: number of newly gained targets (pooled over 5 repeats)", "targets", "value", "e1f_mech_quantiles.csv", nf + ";variable=gamma", "n")
    for t in (100_000, 300_000, 1_000_000, 3_000_000, 10_000_000):
        src = "e1e_tsweep_10M.csv" if t == 10_000_000 else "e1e_tsweep.csv"
        for c in ("M0", "M2x"):
            for q in (1, 10, 100):
                add("C4", f"C4_tsweep_{c}_t{t}_q{q}", f"t sweep, emp (all of S~), {c}, FSB qbar=100, t={t:,}: loss at q={q}", "pp", "value", src, f"condition={c};t={t};q={q}")
        add("C4", f"C4_tsweep_t{t}_avg_bucket", f"t sweep, FSB qbar=100, t={t:,}: average bucket size", "entries", "value", src, f"condition=M0;t={t};q=100", "avg_bucket")
    for c in ("M0", "M2x"):
        for v in ("fsb_base", "smoothed", "cal_iso_w0.5"):
            for q in (100, 1000):
                for b in (2000, 6500, 20000):
                    add("C4", f"C4_fix_{c}_{v}_q{q}_at{b}", f"fixes, emp (all of S~), {c}, {v}: loss at q={q} interpolated to {b} entries per bucket", "pp", "interp_loss", "e1e_fix.csv",
                        f"condition={c};variant={v}", extra=json.dumps({"q": q, "budget": b}))
    for att, src in (("est", "e1f_tailnoise.csv"), ("emp", "e1f_tailnoise_emp.csv")):
        for kind in ("tail", "full"):
            for s in (0.5, 1.0, 1.6):
                f = "q=100;variant=" + "|".join(f"{kind}noise_s{s}_d{d}" for d in (1, 2, 3, 4, 5))
                for op, nm in (("mean", "mean"), ("sd", "sd")):
                    add("C4", f"C4_noise_{att}_{kind}_s{s}_{nm}", f"M3 {kind}-noise ({'noise on tail strings only' if kind == 'tail' else 'noise on all strings'}), {att}, sigma={s}, q=qbar=100: {nm} over 5 draws",
                        "pp", op, src, f, "loss")
    add("C4", "C4_clean_emp_M0_q100", "clean estimate (sigma=0): emp loss, M0, FSB qbar=100, q=100", "pp", "value", "e1e_headline.csv", "condition=M0;scheme=fsb;variant=fsb_base;param=100;attacker=emp;q=100")
    add("C4", "C4_clean_est_M0_q100", "clean estimate (sigma=0): est loss, M0, FSB qbar=100, q=100", "pp", "value", "e1c_e2.csv", "condition=M0;scheme=fsb;variant=fsb_base;param=100;attacker=est;q=100")
    # ------------------------------------------------------------------------------------------------ C5 attacker cost
    for att in ("emp", "est"):
        for cand in ("2M", "all"):
            f = f"attacker={att};candidates={cand}"
            for col, nm, unit in (("n_candidates", "number of candidates", "candidates"), ("total_s", "time of one cold run (5 x 5,000 targets)", "s"), ("index_build_s", "index build time", "s"),
                                  ("games_5x5000_s", "time of the 25,000 bucket queries", "s"), ("peak_rss_gb", "peak resident memory of the process", "GB")):
                add("C5", f"C5_{att}_{cand}_{col}", f"{att} attacker, candidate list {'all of S~' if cand == 'all' else cand}: {nm}", unit, "value", "e1e_cost.csv", f, col)
    # ------------------------------------------------------------------------------------------------ C6 gamma floor (fresh pool A_fresh, seed 6000, M0 and M2x)
    # emp rows: e1g_floor_fresh.csv (all of S~, raw counts); est and gt rows: e1g_robust_fresh.csv (est = p^ over all of S~; gt = Good-Turing adjusted counts)
    src6 = {"emp": "e1g_floor_fresh.csv", "est": "e1g_robust_fresh.csv", "gt": "e1g_robust_fresh.csv"}
    cfgs6 = [("fsb_base", "plain")] + [(f"floor{g}", f"floor{g}") for g in (256, 1024, 2048, 4096)]
    for c in ("M0", "M2x"):
        for qb in QBARS:
            for v, tag in cfgs6:
                flt = lambda a, q: f"condition={c};scheme=fsb;variant={v};param={qb};attacker={a};q={q}"  # noqa: E731
                for q, qt in ((1, "q1"), (qb, "qbar"), (1000, "q1000")):
                    for a in ("emp", "gt", "est"):
                        add("C6", f"C6_{c}_qbar{qb}_{tag}_{a}_loss_{qt}", f"{c}, fresh pool, FSB qbar={qb} {tag}, {a} attacker: loss at q={q}", "pp", "value", src6[a], flt(a, q))
                    add("C6", f"C6_{c}_qbar{qb}_{tag}_worst_{qt}", f"{c}, fresh pool, FSB qbar={qb} {tag}: largest loss over the emp, gt and est attackers at q={q}", "pp", "max_of", "",
                        col="loss", extra=json.dumps({"parts": [[src6[a], flt(a, q)] for a in ("emp", "gt", "est")]}))
            add("C6", f"C6_{c}_qbar{qb}_hpb_emp_loss_qbar", f"{c}, fresh pool, matched HPB, emp: loss at q=qbar={qb}", "pp", "value", "e1g_floor_fresh.csv",
                f"condition={c};scheme=hpb;variant=match_qbar{qb};attacker=emp;q={qb}")
    for qb in QBARS:
        for v, tag in cfgs6:
            add("C6", f"C6_qbar{qb}_{tag}_avg", f"FSB qbar={qb} {tag}: average bucket size", "entries", "value", "e1g_floor_fresh.csv",
                f"condition=M0;scheme=fsb;variant={v};param={qb};attacker=emp;q=1", "avg_bucket")
            if tag != "plain":
                add("C6", f"C6_qbar{qb}_{tag}_avg_ratio", f"FSB qbar={qb} {tag}: average bucket size relative to plain FSB with the same qbar", "ratio", "ratio", "e1g_floor_fresh.csv",
                    f"condition=M0;scheme=fsb;variant={v};param={qb};attacker=emp;q=1", "avg_bucket", "e1g_floor_fresh.csv",
                    f"condition=M0;scheme=fsb;variant=fsb_base;param={qb};attacker=emp;q=1")
    # ------------------------------------------------------------------------------------------------ C7 stability across four splits of the leak (Phase 1h, A_test of each split)
    for c in ("M0", "M2x"):
        for v, tag, sch in (("fsb_base", "plain", "fsb"), ("floor2048", "floor2048", "fsb"), ("match_qbar100", "hpb", "hpb")):
            for q in (1, 100):
                for st in ("mean", "sd", "min", "max"):
                    add("C7", f"C7_{c}_{tag}_q{q}_worst_{st}", f"{c}, {tag}, qbar=100, q={q}: {st} over 4 splits of the per-split largest loss over emp, gt, est", "pp", "split_worst",
                        "e1h_splits.csv", f"condition={c};scheme={sch};variant={v};q={q}", "loss", extra=json.dumps({"stat": st}))
    add("C7", "C7_n_splits", "number of independent splits of the leak", "splits", "split_worst", "e1h_splits.csv", "condition=M0;scheme=fsb;variant=fsb_base;q=100", "loss", extra=json.dumps({"stat": "n"}))
    df = pd.DataFrame(ROWS)
    assert df.id.is_unique, df.id[df.id.duplicated()].tolist()
    cols = ["id", "claim", "description", "value", "unit", "source_csv", "filter", "op", "column", "source_csv2", "filter2", "extra"]
    os.makedirs(PAPER, exist_ok=True)
    df[cols].to_csv(os.path.join(PAPER, "numbers.csv"), index=False, float_format="%.12g")
    lines = ["# Number map", "",
             "Every number the paper text may quote, computed from `results/*.csv` by `experiments/paper_numbers.py` (recipes in `numbers.csv`; `paper/check_numbers.py` recomputes every row). "
             "Frozen framing: est = attacker weights p^ with the 2M list; emp = weights from leak counts with ALL of S~; t = 1M unless stated; loss = bucket success - baseline success of the "
             "same attacker, in percentage points (pp).", ""]
    names = {"C1": "C1 Reproduction (est): HPB vs FSB at matched bucket sizes", "C2": "C2 Noise tolerance (est)", "C3": "C3 Count-aware attacker (emp, all of S~)",
             "C4": "C4 Mechanism", "C5": "C5 Attacker cost", "C6": "C6 Floor on gamma (fresh pool; emp, gt, est attackers)",
             "C7": "C7 Stability across four splits of the leak (A_test of each split; worst case over emp, gt, est)"}
    for cl in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
        sub = df[df.claim == cl]
        lines += [f"## {names[cl]} ({len(sub)} numbers)", "", "| id | description | value | unit | source |", "|---|---|---|---|---|"]
        for r in sub.itertuples():
            v = "nan" if np.isnan(r.value) else (f"{r.value:,.0f}" if abs(r.value) >= 1e4 else f"{r.value:.4g}" if abs(r.value) < 0.01 and r.value != 0 else f"{r.value:.2f}")
            lines.append(f"| `{r.id}` | {r.description} | {v} | {r.unit} | `{r.source_csv}` |")
        lines.append("")
    open(os.path.join(PAPER, "numbers.md"), "w").write("\n".join(lines))
    print(f"{len(df)} numbers written to paper/numbers.csv and paper/numbers.md")


if __name__ == "__main__":
    main()
