"""Phase 1b item 5: calibrated tail estimate (c3sim/calibration.py), designed on A_dev, reported once on A_fresh.

  python -I -m experiments.e1b_fix --pool dev     # all variants + base on A_dev/B_dev: M0, M1b, M2   -> e1b_fix_dev.csv, selection
  python -I -m experiments.e1b_fix --pool fresh   # base + the dev-selected variant on A_fresh/B_fresh: M0, M1b, M2, M3 -> e1b_fix_fresh.csv
The fresh run refuses to start if e1b_fix_fresh.csv already exists (it is run once; no re-rolls).
Attacker: est = weights are the *deployed* estimate of the scheme under test (calibrated p^ for the fix, plain p^ for the base);
emp = leak counts. FSB at equal bucket size = sweep qbar and compare at interpolated average bucket sizes (report1b).
"""
import argparse
import gc
import json
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from c3sim import calibration
from experiments import common as C

R = C.RESULTS
VARIANTS = {"cal_w0.5": dict(width=0.5), "cal_w1.0": dict(width=1.0), "cal_iso_w0.5": dict(width=0.5, iso=True)}
QBARS = (10, 30, 100, 300, 1000, 3000)
SEED = {"dev": 5000, "fresh": 6000}
BUDGET = 6500


def make_world(variant):
    if variant == "fsb_base":
        return C.World()
    cfg = VARIANTS[variant]
    info = {}

    def post(w):
        cal = calibration.fit(w, **cfg)
        info["cal"] = cal
        return cal.phat, cal.phat_ranked(w.pw)

    w = C.World(postproc=post)
    t = pd.DataFrame(info["cal"].table)
    t.to_csv(os.path.join(R, f"e1b_cal_table_{variant}.csv"), index=False)
    tot_true, tot_model = t.held_out_tail_mass.sum(), t.model_tail_mass.sum()
    print(f"[cal {variant}] held-out tail mass {tot_true:.4f}, model tail mass {tot_model:.4f}; calibrated tail mass "
          f"{(t.model_tail_mass * t.factor).sum():.4f}; factor range {t.factor.min():.2e}..{t.factor.max():.2e}", flush=True)
    return w


def interp(d, budget, q=1000):
    d = d[d.q == q].sort_values("avg_bucket")
    return float(np.interp(np.log(budget), np.log(d.avg_bucket), d.loss)) if d.avg_bucket.min() <= budget <= d.avg_bucket.max() else np.nan


def select(df, out):
    lines = [f"Selection on the DEV pool only: mean over M0, M1b, M2 and over est/emp of loss at q=1000 interpolated at {BUDGET} entries per bucket",
             "(lower is better; every variant tried is listed, including failures)"]
    sc = {}
    for v in ["fsb_base"] + list(VARIANTS):
        per = {f"{c}/{m}": interp(df[(df.variant == v) & (df.condition == c) & (df.attacker == m)], BUDGET)
               for c in ("M0", "M1b", "M2") for m in C.MODELS}
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
    out = os.path.join(R, f"e1b_fix_{a.pool}.csv")
    if a.pool == "fresh":
        sel = os.path.join(R, "e1b_fix_selection.json")
        if os.path.exists(out):
            raise SystemExit("e1b_fix_fresh.csv exists: the fresh run is done once and is not repeated")
        variants = ["fsb_base", json.load(open(sel))["best"]]
        conds = ["M0", "M1b", "M2", ("M3", 0.5), ("M3", 1.0), ("M3", 1.5)]
    else:
        variants = ["fsb_base"] + list(VARIANTS)
        conds = ["M0", "M1b", "M2"]
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
            tag = f"{v}" if sig is None else f"{v}|s{sig}"
            for qb in QBARS:
                rows += C.run(w, c, atk.FSB(mem, qb, w.bits), "fsb", v if sig is None else f"{v}+noise_s{sig}", qb, n, rep, SEED[a.pool],
                              pool=a.pool, tag=f"{tag}|{a.pool}", extra_cfg={"sigma": sig})
        del w
        gc.collect()
    C.write_csv(out, rows, C.COLS1B)
    if a.pool == "dev":
        best = select(pd.DataFrame(rows), os.path.join(R, "e1b_fix_selection.txt"))
        json.dump({"best": best}, open(os.path.join(R, "e1b_fix_selection.json"), "w"))


if __name__ == "__main__":
    main()
