"""Phase 1c items 1, 2, 5 at t = 1,000,000 (the new primary setting), seed 2000, pools as in E2.
  e1c_e2.csv         M0, M1a, M1b, M2x (Xato top-370 list, primary), M2 (top370_A_train, secondary), M3 sigma in {0.25,0.5,0.75,1.0,1.5}
  e1c_base_sweep.csv base FSB, M0, qbar 1..3000 (for interpolating the base loss at the M3 bucket sizes)
  e1c_sanity.csv     est attacker with length<=2 candidates outside the histogram head removed (M0s, M2s)
  e1c_m3_repeats.csv per-repeat loss at q = qbar (sigma = 0 is M0), for the sigma-crossing interval
"""
import os

import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e2 import hpb_l_for

R = C.RESULTS
SEED = 2000
T = 1_000_000
QBARS = (10, 100, 1000)
SIGMAS = (0.25, 0.5, 0.75, 1.0, 1.5)
SWEEP = (1, 3, 10, 30, 100, 300, 1000, 3000)


def main():
    a = C.args("Phase 1c E2 at t=1e6")
    w = C.World(t=T)
    f = {qb: atk.FSB([w.base_member()], qb, w.bits) for qb in QBARS}
    avg = {qb: f[qb].sizes(w.h_S)[0] for qb in QBARS}
    rows, rep = [], []
    for cond in ("M0", "M1a", "M1b", "M2x", "M2"):
        for qb in QBARS:
            rows += C.run(w, cond, f[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, SEED)
            l = hpb_l_for(avg[qb], w.N)
            rows += C.run(w, cond, atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, SEED)
    for s in SIGMAS:
        mem = [w.noisy_member(s)]
        for qb in QBARS:
            rows += C.run(w, "M3", atk.FSB(mem, qb, w.bits), "fsb", f"noise_s{s}", qb, a.n_targets, a.repeats, SEED, extra_cfg={"sigma": s})
    for r in rows:  # per-repeat losses at q = qbar (sigma = 0 is M0)
        if r["scheme"] == "fsb" and r["q"] == r["param"] and (r["condition"] == "M3" or (r["condition"] == "M0" and r["variant"] == "fsb_base")):
            s = float(r["variant"].split("_s")[1]) if r["condition"] == "M3" else 0.0
            for i, v in enumerate(r["loss_by_repeat"]):
                rep.append(dict(attacker=r["attacker"], sigma=s, qbar=r["param"], repeat=i, loss=v, avg_bucket=r["avg_bucket"]))
    C.write_csv(os.path.join(R, "e1c_e2.csv"), rows, C.COLS1B)
    pd.DataFrame(rep).to_csv(os.path.join(R, "e1c_m3_repeats.csv"), index=False)
    sw = []
    for qb in SWEEP:
        sw += C.run(w, "M0", atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, SEED)
    C.write_csv(os.path.join(R, "e1c_base_sweep.csv"), sw, C.COLS1B)
    # item 5: est attacker without short (<= 2 chars) candidates that lie outside the histogram head
    sn = []
    for cond in ("M0s", "M2s"):
        for qb in QBARS:
            sn += C.run(w, cond, f[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, SEED, models=("est",))
            sn += C.run(w, cond, atk.HPB(hpb_l_for(avg[qb], w.N)), "hpb", f"match_qbar{qb}", hpb_l_for(avg[qb], w.N), a.n_targets, a.repeats, SEED, models=("est",))
    C.write_csv(os.path.join(R, "e1c_sanity.csv"), sn, C.COLS1B)


if __name__ == "__main__":
    main()
