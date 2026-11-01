"""Phase 1e item 2: t sweep with the emp attacker holding all of S~. M0 and M2x, FSB qbar = 100, seed 2000, A_test, all q.
  python -I -m experiments.e1e_tsweep --ts 100000,300000,1000000,3000000 --out e1e_tsweep.csv
  python -I -m experiments.e1e_tsweep --ts 10000000 --out e1e_tsweep_10M.csv     (own process: t = 10M is the memory-heavy case)
Per-run time and memory go to <out stem>_runs.csv."""
import argparse
import gc
import os

from c3sim import attacker as atk
from experiments import common as C
from experiments.e1e_common import RunLog


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    n, rep = (2000, 3) if a.fast else (5000, 5)
    rows = []
    stem = os.path.splitext(a.out)[0]
    for t in (int(x) for x in a.ts.split(",")):
        rl = RunLog(t=t, candidates="all of S~")
        w = rl.timed("world build", lambda: C.World(t=t, n_cand=None))
        for cond in ("M0", "M2x"):
            rows += rl.timed(f"{cond} fsb qbar=100", lambda: C.run(w, cond, atk.FSB([w.base_member()], 100, w.bits), "fsb", "fsb_base", 100, n, rep, 2000,
                                                                   models=("emp",)))
        rl.save(os.path.join(C.RESULTS, f"{stem}_runs_t{t}.csv"))
        del w
        gc.collect()
    C.write_csv(os.path.join(C.RESULTS, a.out), rows, C.COLS1B)


if __name__ == "__main__":
    main()
