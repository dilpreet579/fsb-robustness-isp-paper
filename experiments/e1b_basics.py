"""Phase 1b items 1-3: t sensitivity (t=1e6), M1b, and the base-FSB sweep used to interpolate M3 at equal bucket size.
New files only: e1b_t_e1.csv, e1b_t_m2.csv, e1b_top20.txt, e1b_m1b.csv, e1b_base_sweep.csv. Existing CSVs are not touched.
Seeds are the same as E1 (1000) / E2 (2000) so rows are paired with the t=1e5 results in e1.csv / e2.csv."""
import os

import numpy as np

from c3sim import attacker as atk
from experiments import common as C
from experiments.e2 import hpb_l_for

R = C.RESULTS


def top20(w, label, out):
    order = np.lexsort((w.pw, -w.ph_S))[:1000]  # the est attacker's candidate order (p^ desc, then lexicographic)
    tail = lambda k: int((order[:k] >= w.t).sum())
    out.append(f"--- t = {w.t:,}: est attacker's top-20 guesses with no bucket (candidate-list order, weight = p^)")
    out.append(f"    entries whose p^ comes from the 3-gram (not in the histogram head): top-20 {tail(20)}, top-100 {tail(100)}, top-1000 {tail(1000)}")
    out.append("    rank  password            p^            leak count  rank by leak count  source")
    for i, j in enumerate(order[:20]):
        out.append(f"    {i + 1:>4}  {w.pw[j].decode():<18} {w.ph_S[j]:.4e}  {int(w.cnt[j]):>10}  {j + 1:>18}  {'histogram' if j < w.t else '3-gram'}")
    out.append("")


def main():
    a = C.args("Phase 1b basics")
    lines = ["Top-20 guesses of the est attacker (M0, no bucket), A_train as the leak", ""]
    # ---- item 1: t = 1e6 ----------------------------------------------------------------------------------------
    w = C.World(t=1_000_000)
    top20(w, "t=1e6", lines)
    rows = []
    for l in range(7, 17):
        rows += C.run(w, "M0", atk.HPB(l), "hpb", "", l, a.n_targets, a.repeats, 1000)
    for qb in (1, 10, 100, 1000, 10000):
        rows += C.run(w, "M0", atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, 1000)
    C.write_csv(os.path.join(R, "e1b_t_e1.csv"), rows, C.COLS1B)
    rows = []
    avg = {qb: atk.FSB([w.base_member()], qb, w.bits).sizes(w.h_S)[0] for qb in (10, 100, 1000)}
    for qb in (10, 100, 1000):
        rows += C.run(w, "M2", atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000, models=("est",))
        l = hpb_l_for(avg[qb], w.N)
        rows += C.run(w, "M2", atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, 2000, models=("est",))
    C.write_csv(os.path.join(R, "e1b_t_m2.csv"), rows, C.COLS1B)
    del w
    w = C.World()  # t = 1e5, for the other half of the top-20 comparison, M1b and the base sweep
    top20(w, "t=1e5", lines)
    open(os.path.join(R, "e1b_top20.txt"), "w").write("\n".join(lines))
    # item 2 (M1b) lives in experiments/e1b_m1b.py (it used to be here and reused the t=1e6 bucket sizes for HPB matching: a bug, fixed)
    # ---- item 3 support: dense base-FSB sweep on the E2 M0 pool/seed ---------------------------------------------
    rows = []
    for qb in (1, 3, 10, 30, 100, 300, 1000, 3000):
        rows += C.run(w, "M0", atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000)
    C.write_csv(os.path.join(R, "e1b_base_sweep.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
