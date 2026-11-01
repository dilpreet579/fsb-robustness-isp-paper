"""Phase 1d items 4 and 5, t = 1,000,000, seed 2000, A_test / B_target, est and emp.
 Item 4  e1d_ablation.csv : M2 ablation, FSB qbar in {10,100,1000}: M2L = length >= 8 only, M2B = Xato blocklist only (no length rule),
                            M2x = both (rerun here, identical seeds to e1c_e2.csv).
 Item 5  e1d_ratio.csv    : attacker success / baseline success at q = 1 and q = qbar for M0, M1b, M2x (FSB and size-matched HPB).
                            ratio = mean bucket success / mean baseline success over the 5 repeats; ratio_sd = sd of the per-repeat ratios
                            (n/a if any repeat has baseline 0)."""
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e2 import hpb_l_for

T = 1_000_000


def ratio_rows(rows):
    out = []
    for r in rows:
        qbar = r["param"] if r["scheme"] == "fsb" else int(r["variant"].replace("match_qbar", ""))
        if r["q"] not in (1, qbar):
            continue
        b, a = np.array(r["bucket_by_repeat"]), np.array(r["baseline_by_repeat"])
        per = b / a if (a > 0).all() else None
        out.append(dict(condition=r["condition"], attacker=r["attacker"], scheme=r["scheme"], qbar=qbar, q=r["q"], avg_bucket=r["avg_bucket"],
                        baseline_success=r["baseline_success"], bucket_success=r["bucket_success"],
                        ratio=round(r["bucket_success"] / r["baseline_success"], 4) if r["baseline_success"] > 0 else None,
                        ratio_sd=round(float(per.std(ddof=1)), 4) if per is not None else None, loss=r["loss"], std_loss=r["std_over_repeats"]))
    return out


def main():
    a = C.args("Phase 1d M2 ablation and ratios")
    w = C.World(t=T)
    f = {qb: atk.FSB([w.base_member()], qb, w.bits) for qb in (10, 100, 1000)}
    abl, rat = [], []
    for cond in ("M2L", "M2B", "M2x"):
        for qb in (10, 100, 1000):
            abl += C.run(w, cond, f[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000)
    for cond in ("M0", "M1b", "M2x"):
        for qb in (10, 100, 1000):
            rat += C.run(w, cond, f[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000)
            l = hpb_l_for(f[qb].sizes(w.h_S)[0], w.N)
            rat += C.run(w, cond, atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, 2000)
    C.write_csv(os.path.join(C.RESULTS, "e1d_ablation.csv"), abl, C.COLS1B)
    pd.DataFrame(ratio_rows(rat)).to_csv(os.path.join(C.RESULTS, "e1d_ratio.csv"), index=False)


if __name__ == "__main__":
    main()
