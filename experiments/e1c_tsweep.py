"""Phase 1c item 3: t sweep {100k, 300k, 1M, 3M}. M0, FSB qbar = 100, E2 seed 2000 / pool A_test (identical targets across t).
Both attackers are run; the emp attacker at q = 100 is the requested quantity. Output: e1c_tsweep.csv."""
import gc
import os

from c3sim import attacker as atk
from experiments import common as C

TS = (100_000, 300_000, 1_000_000, 3_000_000)


def main():
    a = C.args("Phase 1c t sweep")
    rows = []
    for t in TS:
        w = C.World(t=t)
        rows += C.run(w, "M0", atk.FSB([w.base_member()], 100, w.bits), "fsb", "fsb_base", 100, a.n_targets, a.repeats, 2000)
        del w
        gc.collect()
    C.write_csv(os.path.join(C.RESULTS, "e1c_tsweep.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
