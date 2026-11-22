"""Phase 1h report (results/REPORT_1h.md): stability across four splits of the leak. Numbers and method statements only; reads results/e1h_splits*.csv."""
import os

import pandas as pd

from experiments import common as C

R = C.RESULTS


def main():
    d = pd.read_csv(os.path.join(R, "e1h_splits.csv"))
    runs = pd.read_csv(os.path.join(R, "e1h_splits_runs.csv"))
    o = ["# REPORT 1h (Phase 1h: four splits of the leak)", "",
         "Numbers and method statements only. Earlier results were not modified; Phase 1h adds `experiments/e1h_splits.py`, `experiments/report1h.py`, `results/e1h_splits*` and the argument `split_seeds` "
         "of `experiments.common.World` (default unchanged: split seeds 101, 102, 103).", "",
         "## Method", "",
         "- Four independent account splits of RockYou: seeds (a, b, dev) = (101, 102, 103) (the paper's split), (111, 112, 113), (121, 122, 123), (131, 132, 133); each split has its own 90% leak S~, server estimate (t = 1M), "
         "attackers and held-out target pool A_test.",
         "- Configurations fixed in advance, nothing selected: plain FSB qbar = 100, FSB qbar = 100 with floor g = 2,048 (chosen on the first split's development pool, so the other three splits are out of sample for it), "
         "HPB size-matched by `hpb_l_for`. Conditions M0 and M2x. Attackers emp, gt, est, all over all of S~. Target seed 2000, 5 repeats x 5,000 targets, q in {1, 10, 100, 1000}.", "",
         "## Largest loss over emp, gt and est, per split (points)", "",
         "| cond | scheme | q | " + " | ".join(f"split {s}" for s in sorted(d.split.unique())) + " | mean | sd | min | max |", "|---|---|---|" + "---|" * (len(d.split.unique()) + 4)]
    for c in ("M0", "M2x"):
        for v, name in (("fsb_base", "plain FSB"), ("floor2048", "floor 2,048"), ("match_qbar100", "matched HPB")):
            for q in (1, 100):
                w = d[(d.condition == c) & (d.variant == v) & (d.q == q)].groupby("split").loss.max()
                o.append(f"| {c} | {name} | {q} | " + " | ".join(f"{x:.2f}" for x in w.values) + f" | {w.mean():.2f} | {w.std(ddof=1):.2f} | {w.min():.2f} | {w.max():.2f} |")
    o += ["", "Average bucket size per split (M0, plain FSB / floor 2,048 / HPB): " + "; ".join(
        f"split {s}: " + " / ".join(f"{d[(d.split == s) & (d.condition == 'M0') & (d.variant == v) & (d.q == 1)].avg_bucket.iloc[0]:,.0f}" for v in ("fsb_base", "floor2048", "match_qbar100"))
        for s in sorted(d.split.unique())), "",
          f"Runtime: {runs.seconds.sum() / 60:.1f} minutes (sum of per-run seconds), peak RSS {runs.peak_rss_so_far_gb.max():.2f} GB.", "",
          "## Reproduce", "", "    make e1h-splits report1h", ""]
    open(os.path.join(R, "REPORT_1h.md"), "w").write("\n".join(o))
    print("wrote results/REPORT_1h.md")


if __name__ == "__main__":
    main()
