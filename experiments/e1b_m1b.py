"""Phase 1b item 2: M1b = server estimate from A_train (t=1e5), targets B_target, attacker weights = the server's p^ (est)
over the top 2M of S~ (emp = counts over the top 2M, extra). Seed 2000. HPB prefix chosen to match the FSB average bucket size of THIS world."""
import os

from c3sim import attacker as atk
from experiments import common as C
from experiments.e2 import hpb_l_for


def main():
    a = C.args("M1b")
    w = C.World()
    rows = []
    for qb in (10, 100, 1000):
        f = atk.FSB([w.base_member()], qb, w.bits)
        rows += C.run(w, "M1b", f, "fsb", "fsb_base", qb, a.n_targets, a.repeats, 2000)
        l = hpb_l_for(f.sizes(w.h_S)[0], w.N)
        rows += C.run(w, "M1b", atk.HPB(l), "hpb", f"match_qbar{qb}", l, a.n_targets, a.repeats, 2000)
    C.write_csv(os.path.join(C.RESULTS, "e1b_m1b.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
