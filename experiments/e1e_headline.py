"""Phase 1e item 1 (and the timing half of item 5): headline rows with the emp attacker holding ALL of S~ (13,125,513 candidates), t = 1,000,000.
Conditions M0, M1b, M2x, M2L; FSB qbar in {10,100,1000} and size-matched HPB (same matching as 1c); every q in {1,10,100,1000}; seed 2000, A_test (M1b: B_target).
  e1e_headline.csv   emp, all of S~       e1e_ratio.csv  success / baseline at q = 1 and q = qbar (emp, all of S~)
  e1e_runs.csv       per-run seconds and memory (current / peak RSS of the process)
  e1e_m2l_2m.csv     M2L (length >= 8 only) FSB + size-matched HPB with the 2M list, est and emp (1c / 1d have no HPB row for M2L); e1e_ratio_m2l_2m.csv
"""
import os

import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e1d_m2 import ratio_rows
from experiments.e1e_common import RunLog
from experiments.e2 import hpb_l_for

T = 1_000_000
QBARS = (10, 100, 1000)
CONDS = ("M0", "M1b", "M2x", "M2L")


def main():
    a = C.args("Phase 1e headline")
    rl = RunLog(t=T, candidates="all of S~")
    w = C.World(t=T, n_cand=None)
    f = {qb: atk.FSB([w.base_member()], qb, w.bits) for qb in QBARS}
    avg = {qb: f[qb].sizes(w.h_S)[0] for qb in QBARS}
    rows = []
    for cond in CONDS:
        for qb in QBARS:
            rows += rl.timed(f"{cond} fsb qbar={qb}", lambda: C.run(w, cond, f[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000, models=("emp",)))
            l = hpb_l_for(avg[qb], w.N)
            rows += rl.timed(f"{cond} hpb l={l}", lambda: C.run(w, cond, atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, 2000, models=("emp",)))
    C.write_csv(os.path.join(C.RESULTS, "e1e_headline.csv"), rows, C.COLS1B)
    pd.DataFrame(ratio_rows(rows)).to_csv(os.path.join(C.RESULTS, "e1e_ratio.csv"), index=False)
    rl.save(os.path.join(C.RESULTS, "e1e_runs.csv"))
    del w, f
    # M2L with the 2M list (est and emp): fills the HPB rows 1c / 1d did not have
    w2 = C.World(t=T, n_cand=C.N_CAND)
    f2 = {qb: atk.FSB([w2.base_member()], qb, w2.bits) for qb in QBARS}
    rows2 = []
    for qb in QBARS:
        rows2 += C.run(w2, "M2L", f2[qb], "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000)
        l = hpb_l_for(f2[qb].sizes(w2.h_S)[0], w2.N)
        rows2 += C.run(w2, "M2L", atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, 2000)
    C.write_csv(os.path.join(C.RESULTS, "e1e_m2l_2m.csv"), rows2, C.COLS1B)
    pd.DataFrame(ratio_rows(rows2)).to_csv(os.path.join(C.RESULTS, "e1e_ratio_m2l_2m.csv"), index=False)


if __name__ == "__main__":
    main()
