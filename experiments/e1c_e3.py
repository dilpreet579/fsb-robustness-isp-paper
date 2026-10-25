"""Phase 1c item 1: E3 at t = 1,000,000. Same protocol, seeds (dev 3000, fresh 4000), qbar grid and variants as experiments/e3.py.
Conditions: M0, M1a, M1b, M2 (top370_A_train), M2x (Xato top-370). Selection on dev only, over M0, M1b, M2x (the Phase 1c primary
conditions) at 6,500 entries per bucket, q = 1000, mean over est/emp. Outputs: e1c_e3.csv (fresh), e1c_e3_dev.csv, e1c_e3_selection.{txt,json}."""
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e3 import BUDGET, QBARS, SEED_DEV, SEED_FRESH, VARIANTS, interp_loss

R = C.RESULTS
T = 1_000_000
CONDS = ("M0", "M1a", "M1b", "M2", "M2x")
SELECT_ON = ("M0", "M1b", "M2x")


def select(dev, out):
    lines = [f"E3 at t=1e6, selection on the DEV pool only: mean over {SELECT_ON} and over est/emp of loss at q=1000 interpolated at {BUDGET} entries per bucket (lower is better)."]
    sc = {}
    for v in VARIANTS:
        per = {f"{c}/{m}": interp_loss(dev[(dev.attacker == m) & (dev.variant == v) & (dev.condition == c) & (dev.q == 1000)], BUDGET)
               for c in SELECT_ON for m in C.MODELS}
        sc[v] = float(np.mean(list(per.values())))
        lines.append(f"{v:<9} score={sc[v]:7.3f}  " + "  ".join(f"{k}={x:.2f}" for k, x in per.items()))
    best = min(sc, key=lambda v: sc[v] if not np.isnan(sc[v]) else 1e9)
    lines.append(f"selected on dev: {best}")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return best


def main():
    a = C.args("Phase 1c E3 at t=1e6")
    w = C.World(t=T)
    dev, fresh = [], []
    for v in VARIANTS:
        mem = w.members(v)
        for qb in QBARS:
            sch = atk.FSB(mem, qb, w.bits)
            for cond in CONDS:
                dev += C.run(w, cond, sch, "fsb", v, qb, a.n_targets, a.repeats, SEED_DEV, pool="dev", tag="dev")
                fresh += C.run(w, cond, sch, "fsb", v, qb, a.n_targets, a.repeats, SEED_FRESH, pool="fresh", tag="fresh")
        mem = None
    C.write_csv(os.path.join(R, "e1c_e3_dev.csv"), dev, C.COLS1B)
    C.write_csv(os.path.join(R, "e1c_e3.csv"), fresh, C.COLS1B)
    best = select(pd.DataFrame(dev), os.path.join(R, "e1c_e3_selection.txt"))
    pd.Series({"best": best}).to_json(os.path.join(R, "e1c_e3_selection.json"))


if __name__ == "__main__":
    main()
