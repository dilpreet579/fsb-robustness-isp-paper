"""Phase 1d item 1: attacker candidate-list cap. emp attacker, M0 and M2x, FSB qbar = 100, t in {1M, 3M}, candidates in {2M, 4M, 6M}
(and all of S~, 13.1M, as an extra: it fit in memory in Phase 1). Seed 2000, A_test, same targets in every cell.  -> e1d_cap.csv"""
import gc
import os

from c3sim import attacker as atk
from experiments import common as C

CANDS = (2_000_000, 4_000_000, 6_000_000, None)  # None = all of S~


def main():
    a = C.args("Phase 1d candidate cap")
    rows = []
    for t in (1_000_000, 3_000_000):
        for nc in CANDS:
            w = C.World(t=t, n_cand=nc or 13_125_513)
            tag = f"cand{'all' if nc is None else nc // 1_000_000}M"
            for cond in ("M0", "M2x"):
                for r in C.run(w, cond, atk.FSB([w.base_member()], 100, w.bits), "fsb", f"fsb_base {tag}", 100, a.n_targets, a.repeats, 2000,
                               tag=tag, models=("emp",)):
                    rows.append(r)
            del w
            gc.collect()
    C.write_csv(os.path.join(C.RESULTS, "e1d_cap.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
