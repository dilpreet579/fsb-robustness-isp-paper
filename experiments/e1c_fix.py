"""Phase 1c item 6 (EXPLORATORY): the Phase 1b calibration fix (c3sim/calibration.py) rerun at t = 1,000,000, same pipeline.
  --pool dev   : base + 3 variants on A_dev/B_dev (seed 5000): M0, M1b, M2, M2x           -> e1c_fix_dev.csv, selection (dev only)
  --pool fresh : base + dev-selected variant on A_fresh/B_fresh (seed 6000): + M3 sigma   -> e1c_fix_fresh.csv (refuses to rerun)
NOTE: A_fresh/B_fresh and these exact targets (seed 6000) were already used in Phase 1 (E3) and Phase 1b (fresh calibration run), so
the fresh pool is no longer an untouched holdout for this design; the report labels it exploratory."""
import argparse
import gc
import json
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from c3sim import calibration
from experiments import common as C
from experiments.e1b_fix import BUDGET, QBARS, SEED, VARIANTS, interp

R = C.RESULTS
T = 1_000_000
SELECT_ON = ("M0", "M1b", "M2x")


def make_world(variant):
    if variant == "fsb_base":
        return C.World(t=T)
    info = {}

    def post(w):
        cal = calibration.fit(w, **VARIANTS[variant])
        info["cal"] = cal
        return cal.phat, cal.phat_ranked(w.pw)

    w = C.World(t=T, postproc=post)
    t = pd.DataFrame(info["cal"].table)
    t.to_csv(os.path.join(R, f"e1c_cal_table_{variant}.csv"), index=False)
    print(f"[cal {variant}] held-out tail mass {t.held_out_tail_mass.sum():.4f}, model tail mass {t.model_tail_mass.sum():.4f}; calibrated tail mass "
          f"{(t.model_tail_mass * t.factor).sum():.4f}; factor range {t.factor.min():.2e}..{t.factor.max():.2e}", flush=True)
    return w


def select(df, out):
    lines = [f"[EXPLORATORY, t=1e6] selection on the DEV pool only: mean over {SELECT_ON} and est/emp of loss at q=1000 interpolated at {BUDGET} entries per bucket",
             "(lower is better; every variant tried is listed, including failures)"]
    sc = {}
    for v in ["fsb_base"] + list(VARIANTS):
        per = {f"{c}/{m}": interp(df[(df.variant == v) & (df.condition == c) & (df.attacker == m)], BUDGET) for c in SELECT_ON for m in C.MODELS}
        sc[v] = float(np.mean(list(per.values())))
        lines.append(f"{v:<13} score={sc[v]:7.3f}  " + "  ".join(f"{k}={x:.2f}" for k, x in per.items()))
    best = min(VARIANTS, key=lambda v: sc[v])
    lines.append(f"best calibrated variant on dev: {best} (score {sc[best]:.3f} vs fsb_base {sc['fsb_base']:.3f})")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", choices=("dev", "fresh"), required=True)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    n, rep = (2000, 3) if a.fast else (5000, 5)
    out = os.path.join(R, f"e1c_fix_{a.pool}.csv")
    if a.pool == "fresh":
        if os.path.exists(out):
            raise SystemExit("e1c_fix_fresh.csv exists: the fresh run is done once and is not repeated")
        variants = ["fsb_base", json.load(open(os.path.join(R, "e1c_fix_selection.json")))["best"]]
        conds = ["M0", "M1b", "M2", "M2x", ("M3", 0.5), ("M3", 1.0), ("M3", 1.5)]
    else:
        variants = ["fsb_base"] + list(VARIANTS)
        conds = ["M0", "M1b", "M2", "M2x"]
    rows = []
    for v in variants:
        w = make_world(v)
        for c in conds:
            sig = None
            if isinstance(c, tuple):
                c, sig = c
                mem = [w.noisy_member(sig)]
            else:
                mem = [w.base_member()]
            for qb in QBARS:
                rows += C.run(w, c, atk.FSB(mem, qb, w.bits), "fsb", v if sig is None else f"{v}+noise_s{sig}", qb, n, rep, SEED[a.pool],
                              pool=a.pool, tag=f"{v}|{sig}|{a.pool}", extra_cfg={"sigma": sig})
        del w
        gc.collect()
    C.write_csv(out, rows, C.COLS1B)
    if a.pool == "dev":
        best = select(pd.DataFrame(rows), os.path.join(R, "e1c_fix_selection.txt"))
        json.dump({"best": best}, open(os.path.join(R, "e1c_fix_selection.json"), "w"))


if __name__ == "__main__":
    main()
