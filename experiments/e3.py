"""E3: conservative-replication variants, swept over qbar to trace bucket size against loss.

Variants: fsb_base | ens_max (max gamma over base, 5 Poisson-bootstrap resamples, tau=0.8, tau=0.6) | smoothed (Kneser-Ney 3-gram).
Conditions: M0, M1, M2. Both attacker models (see DISCREPANCIES D9).
Protocol: every (variant, qbar, condition) is run on the DEV pool (seed 3000) and on the FRESH pool (seed 4000).
The best variant is chosen from the dev rows only (E3_selection.txt) and then everything is reported from the fresh rows
(results/e3.csv). Dev rows are kept in results/e3_dev.csv as the tuning log.
"""
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from experiments import common as C

SEED_DEV, SEED_FRESH = 3000, 4000
QBARS = (1, 3, 10, 30, 100, 300, 1000, 3000)
VARIANTS = ("fsb_base", "ens_max", "smoothed")
CONDS = ("M0", "M1", "M2")
BUDGET = 6500  # average bucket size (entries) at which variants are compared for selection (paper's FSB qbar=100: 6.3k)


def interp_loss(d, budget):
    """Loss at q=1000 interpolated (log-linear in average bucket size) along one variant's qbar sweep."""
    d = d.sort_values("avg_bucket")
    return float(np.interp(np.log(budget), np.log(d.avg_bucket), d.loss)) if d.avg_bucket.min() <= budget <= d.avg_bucket.max() else np.nan


def select(dev, out):
    """Best variant per attacker model by mean (over M0, M1, M2) dev loss at q=1000 at average bucket size BUDGET."""
    lines = [f"E3 selection on the DEV pool only: mean over {CONDS} of loss at q=1000, interpolated at {BUDGET} entries per bucket.",
             "Lower is better. nan = the sweep does not reach that bucket size."]
    best = {}
    for m in C.MODELS:
        sc = {}
        for v in VARIANTS:
            per = [interp_loss(dev[(dev.attacker == m) & (dev.variant == v) & (dev.condition == c) & (dev.q == 1000)], BUDGET) for c in CONDS]
            sc[v] = (float(np.mean(per)), per)
            lines.append(f"[{m}] {v:<9} score={sc[v][0]:7.2f}   per condition {dict(zip(CONDS, np.round(per, 2)))}")
        ok = {v: s[0] for v, s in sc.items() if not np.isnan(s[0])}
        best[m] = min(ok, key=ok.get)
        lines.append(f"[{m}] selected on dev: {best[m]}")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return best


def main():
    a = C.args("E3")
    w = C.World()
    dev, fresh = [], []
    for v in VARIANTS:
        mem = w.members(v)
        for qb in QBARS:
            sch = atk.FSB(mem, qb, w.bits)
            for cond in CONDS:
                dev += C.run(w, cond, sch, "fsb", v, qb, a.n_targets, a.repeats, SEED_DEV, pool="dev", tag="dev")
                fresh += C.run(w, cond, sch, "fsb", v, qb, a.n_targets, a.repeats, SEED_FRESH, pool="fresh", tag="fresh")
        mem = None
    C.write_csv(os.path.join(C.RESULTS, "e3_dev.csv"), dev)
    C.write_csv(os.path.join(C.RESULTS, "e3.csv"), fresh)
    best = select(pd.DataFrame(dev), os.path.join(C.RESULTS, "E3_selection.txt"))
    pd.Series(best).to_json(os.path.join(C.RESULTS, "e3_best.json"))


if __name__ == "__main__":
    main()
