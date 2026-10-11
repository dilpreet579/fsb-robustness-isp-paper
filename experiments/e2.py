"""E2: mismatch conditions. FSB qbar in {10,100,1000}; HPB at (nearest power-of-two) equal bucket size.
M0 is re-run here with the same seed as M1-M3 so the gate statistic compares like with like.
HPB does not use the estimate, so its M3 rows would equal M0; they are not repeated.
"""
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from experiments import common as C

SEED = 2000
QBARS = (10, 100, 1000)
SIGMAS = (0.5, 1.0, 1.5)


def hpb_l_for(avg, N):
    """Power-of-two prefix length whose average bucket size N/2^l is nearest to avg (log scale)."""
    ls = np.arange(5, 20)
    return int(ls[np.argmin(np.abs(np.log((N / 2.0 ** ls) / avg)))])


def gate(df, out):
    lines = ["Gate statistic (plan T6): FSB qbar=100, q=1000, loss in percentage points; difference = mismatch loss - M0 loss",
             "sd = sqrt(sd_a^2 + sd_b^2) of the per-repeat losses (independent target pools)"]
    for m in C.MODELS:
        d = df[(df.attacker == m) & (df.scheme == "fsb") & (df.param == 100) & (df.q == 1000) & (df.variant == "fsb_base")].set_index("condition")
        for c in ("M1", "M2"):
            diff = d.loc[c].loss - d.loc["M0"].loss
            sd = np.hypot(d.loc[c].std_over_repeats, d.loc["M0"].std_over_repeats)
            lines.append(f"[{m}] loss({c}) - loss(M0) = {d.loc[c].loss:.2f} - {d.loc['M0'].loss:.2f} = {diff:+.2f} points (sd {sd:.2f})")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    a = C.args("E2")
    w = C.World()
    N = w.N
    rows = []
    avg = {qb: atk.FSB([w.base_member()], qb, w.bits).sizes(w.h_S)[0] for qb in QBARS}
    for cond in ("M0", "M1", "M2"):
        for qb in QBARS:
            rows += C.run(w, cond, atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, SEED)
            l = hpb_l_for(avg[qb], N)
            rows += C.run(w, cond, atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, SEED)
    for s in SIGMAS:
        for qb in QBARS:
            rows += C.run(w, "M3", atk.FSB([w.noisy_member(s)], qb, w.bits), "fsb", f"noise_s{s}", qb, a.n_targets, a.repeats, SEED,
                          extra_cfg={"sigma": s})
    C.write_csv(os.path.join(C.RESULTS, "e2.csv"), rows)
    gate(pd.DataFrame(rows), os.path.join(C.RESULTS, "E2_gate.txt"))


if __name__ == "__main__":
    main()
