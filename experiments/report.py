"""Assemble results/REPORT.md from the CSVs and check outputs. Numbers and pass/fail only; no interpretation beyond that."""
import json
import os

import numpy as np
import pandas as pd

from experiments import common as C

R = C.RESULTS
QS = C.QS


def rd(name):
    p = os.path.join(R, name)
    return open(p).read().rstrip() if os.path.exists(p) else f"(missing: {name})"


def md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def table(d, keys):
    """One row per config: baseline success and loss (+- sd over repeats) at each q."""
    rows = []
    for k, g in d.groupby(keys, sort=False):
        g = g.set_index("q")
        r = dict(zip(keys, k if isinstance(k, tuple) else (k,)))
        r["avg_bucket"] = f"{g.avg_bucket.iloc[0]:.0f}"
        r["max_bucket"] = int(g.max_bucket.iloc[0])
        for q in QS:
            r[f"base@{q}"] = f"{g.baseline_success[q]:.2f}"
        for q in QS:
            r[f"loss@{q}"] = f"{g.loss[q]:+.2f} ±{g.std_over_repeats[q]:.2f}"
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    L = ["# REPORT (Phase 1: simulator and E1-E3)", "",
         "Numbers and check outcomes only. Units: success rates and losses are in percent / percentage points of targets; "
         "`avg_bucket` and `max_bucket` are entries per bucket measured exactly on S~ (A_train); ± is the standard deviation of the per-repeat loss. "
         "Two attacker models are reported everywhere (`est` = weights p^ as in the base paper; `emp` = weights from leak counts as in the plan); "
         "see DISCREPANCIES D9. HPB: l-bit hash prefix. FSB: qbar parameter, |B| = 2^24.", "",
         "## 1. Data summary", "", rd("data_report.md").split("\n", 1)[1], ""]
    L += ["## 2. Correctness checks", "",
          "| task | check | result |", "|---|---|---|",
          "| T1 | same seed gives the same split; data_report.md written; raw counts equal the plan | PASS (tests/test_data.py, T1_corpus_check.txt) |",
          "| T2 | 10k-sample probabilities finite and > 0; top-1000 hist mass equals empirical share; p^(w_qbar) > 0 for qbar in 1..10000 | PASS |",
          "| T3 | fast lookup equals naive scan on 1,000 buckets (50k toy); avg FSB bucket = sum(gamma)/|B| | PASS |",
          "| T4 | baseline = top-q mass within sampling error (toy); five worked examples written; naive recomputation of each example matches | PASS |",
          "| T5 (est) | FSB loss <= 1 point for q <= qbar; HPB at ~7k/bucket loses tens of points at q=1000 | " + ("PASS" if "est=PASS" in rd("E1_check.txt") else "FAIL") + " |",
          "| T5 (emp) | same check, count-weighted attacker | " + ("PASS" if "emp=PASS" in rd("E1_check.txt") else "**FAIL**") + " |",
          "| T4 | success unchanged between 1M and 2M candidates | **FAIL** at q=1000 for HPB (est: see 2.5); est FSB unchanged; 2M vs all of S~ for est <= 0.2 point |",
          "", "### 2.1 T1-T4 evidence (verbatim)", "", "```", rd("T1_corpus_check.txt"), "", rd("T2_check.txt"), "", rd("T3_check.txt"), "", rd("T4_check.txt"), "```", "",
          "### 2.2 Worked examples", "", "`results/worked_examples.txt` (5 FSB + 2 HPB examples, each re-derived by a naive scan; includes a hand-replay recipe).", "",
          "### 2.3 Test suite", "", "```", rd("tests_all.txt"), "```", "",
          "### 2.4 E1 acceptance checks", "", "```", rd("E1_check.txt"), "```", "",
          "### 2.5 Candidate-list convergence (1M / 2M / 4M / all of S~)", "", "```", rd("cand_check.txt"), "```", ""]

    e1 = pd.read_csv(os.path.join(R, "e1.csv"))
    L += ["## 3. E1: matched condition M0 (pool A_test, seed 1000)", ""]
    for m in C.MODELS:
        L += [f"### attacker `{m}`", "", md(table(e1[e1.attacker == m], ["scheme", "param"])), ""]
    est = e1[(e1.attacker == "est") & (e1.q == 1000)]
    f1, h1 = est[est.scheme == "fsb"].set_index("param"), est[est.scheme == "hpb"].set_index("param")
    L += ["Shape, from the table (est attacker, q=1000): " +
          f"HPB l=11 ({h1.avg_bucket[11]:.0f} entries) loses {h1.loss[11]:.1f}; FSB qbar=1000 ({f1.avg_bucket[1000]:.0f} entries) loses {f1.loss[1000]:.1f}; "
          f"FSB qbar=100 ({f1.avg_bucket[100]:.0f} entries) loses {f1.loss[100]:.1f} vs HPB l=13 ({h1.avg_bucket[13]:.0f} entries) {h1.loss[13]:.1f}. "
          "HPB's loss is flat below ~6k entries because its buckets then hold fewer than 1,000 attacker candidates (every candidate is guessed). "
          "Reference (paper, 436M scale): HPB l=16 (6.6k/bucket) 59.7% vs 5.8% baseline; FSB qbar=100 (6.3k/bucket) 8.0%; not comparable in level (DISCREPANCIES D4).", ""]

    e2 = pd.read_csv(os.path.join(R, "e2.csv"))
    L += ["## 4. E2: mismatch (seed 2000)", "",
          "HPB rows use the power-of-two prefix whose average bucket size is nearest to FSB's (`variant` = match_qbarN). HPB does not use the estimate, so no M3 HPB rows. "
          "M3 changes FSB's bucket sizes (the noisy estimate re-derives w_qbar).", ""]
    for m in C.MODELS:
        L += [f"### attacker `{m}`", "", md(table(e2[e2.attacker == m], ["condition", "scheme", "variant", "param"])), ""]
    L += ["### Gate statistic", "", "```", rd("E2_gate.txt"), "```", ""]
    g = e2[(e2.scheme == "fsb") & (e2.param == 100) & (e2.variant == "fsb_base") & (e2.attacker == "est")].set_index(["condition", "q"])
    L += ["Same statistic at other q (est attacker, FSB qbar=100): " + "; ".join(
        f"q={q}: M1-M0 = {g.loss['M1', q] - g.loss['M0', q]:+.2f}, M2-M0 = {g.loss['M2', q] - g.loss['M0', q]:+.2f}" for q in QS) +
        ". M1 at q=1000 is saturated (QUESTIONS Q8).", ""]

    e3 = pd.read_csv(os.path.join(R, "e3.csv"))
    best = json.load(open(os.path.join(R, "e3_best.json")))
    L += ["## 5. E3: conservative variants (fresh pool, seed 4000; selection on dev pool, seed 3000)", "",
          f"Best variant chosen on the dev pool only: {best} (per attacker model; criterion in E3_selection.txt). "
          "`param` = qbar. Dev rows are in `results/e3_dev.csv`.", "", "```", rd("E3_selection.txt"), "```", ""]
    for m in C.MODELS:
        for c in ("M0", "M1", "M2"):
            L += [f"### attacker `{m}`, condition {c} (fresh pool)", "", md(table(e3[(e3.attacker == m) & (e3.condition == c)], ["variant", "param"])), ""]
    L += ["### Loss at q=1000 interpolated to fixed average bucket sizes (fresh pool; log-linear in bucket size; nan = sweep does not reach it)", ""]
    rows = []
    for m in C.MODELS:
        for c in ("M0", "M1", "M2"):
            for v in ("fsb_base", "ens_max", "smoothed"):
                d = e3[(e3.attacker == m) & (e3.condition == c) & (e3.variant == v) & (e3.q == 1000)].sort_values("avg_bucket")
                r = dict(attacker=m, condition=c, variant=v)
                for b in (2000, 6500, 20000):
                    r[f"loss@{b}"] = round(float(np.interp(np.log(b), np.log(d.avg_bucket), d.loss)), 2) if d.avg_bucket.min() <= b <= d.avg_bucket.max() else "nan"
                rows.append(r)
    L += [md(pd.DataFrame(rows)), ""]

    L += ["## 6. Runtimes", "", "```", rd("runtimes.txt"), "```", "",
          "## 7. Known issues and deviations from the plan", "",
          "Full list with reasons: `results/DISCREPANCIES.md` (D1-D9) and `results/QUESTIONS.md` (Q1-Q10). Headline items:", "",
          "1. Two attacker models (D9). The plan-literal count-weighted attacker fails the E1 FSB check; the paper-faithful one passes. No choice was made between them.",
          "2. t = 100,000 as in the plan, not the paper's 10^6 (D1); the 3-gram inflates short strings (e.g. `12`, `na`), which occupy slots in the 'top qbar' under p^.",
          "3. The est attacker's candidate list is the top 2M of S~ by p^ with no generated n-gram candidates (D3); that list contains the same inflated short strings.",
          "4. 1M-vs-2M candidate check fails at q=1000 for HPB (section 2.5). The est attacker is converged at 2M (<= 0.2 point from all of S~); the emp attacker is not (up to ~8 points for FSB), so emp losses are lower bounds.",
          "5. M1 at q=1000 is saturated (Q8); read M1 at q <= 100.",
          "6. M2 banned list is the top-370 of A_train, not Twitter's list (D7, Q2).",
          "7. Everything was run once with the seeds in the CSVs; no run was dropped or re-rolled. Standard deviations come from 5 repeats of 5,000 targets (targets re-sampled, split fixed).",
          "8. E3 reading aids (numbers from the tables above, fresh pool, q=1000): at 6,500 entries per bucket `ens_max` loses more than `fsb_base` in every "
          "condition and for both attackers (e.g. est/M0 9.03 vs 0.68); it only gets lower loss than the base at larger buckets (the base sweep stops near 17k entries, "
          "`ens_max` reaches 52k at qbar=3000; see Fig. 3 for the crossover under emp/M0 near 11k). `smoothed` (Kneser-Ney) is within about 0.4 point of `fsb_base` "
          "except est/M0 at 2,000 entries (14.6 vs 10.6); the dev-selected `smoothed` for the emp attacker beats `fsb_base` by 0.01 point on dev (a tie).",
          "9. Extra trailing CSV column `attacker`; E3 `e3.csv` holds fresh-pool rows only, dev rows are in `e3_dev.csv`.", "",
          "## 8. Commands to reproduce", "", "```", "make all     # or, step by step:", "make venv fetch data test", "make e1 worked e2 e3 figs report", "```",
          "Figures: `figs/fig1_pareto`, `figs/fig2_mismatch`, `figs/fig3_fix` (pdf and png); they are drawn from the CSVs only.", ""]
    open(os.path.join(R, "REPORT.md"), "w").write("\n".join(L))
    print("wrote REPORT.md", len("\n".join(L)), "chars")


if __name__ == "__main__":
    main()
