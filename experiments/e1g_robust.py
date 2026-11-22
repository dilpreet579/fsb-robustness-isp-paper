"""Phase 1g robustness: does the gamma floor survive attackers other than the raw-count emp attacker? Declared before running.
  est = ranks by the server's estimate p^ (all of S~); gt = ranks by Good-Turing adjusted leak counts (Context: the raw-count emp attacker takes
  a count-1 password at face value; Turing's r* = (r+1) n_{r+1}/n_r says a count-1 password is worth about 0.3 of an occurrence).
  python -I -m experiments.e1g_robust --pool dev      -> e1g_robust_dev.csv
  python -I -m experiments.e1g_robust --pool fresh    -> e1g_robust_fresh.csv (once; refuses to rerun)
Same seeds, targets, conditions (M0, M2x), qbar sweep and size-matched HPB as e1g_floor; floors 256, 1024, 2048, 4096 for qbar 10, 100, 1000.
No selection is made here: every configuration and attacker is reported."""
import argparse
import gc
import os

import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e1e_common import RunLog
from experiments.e1g_floor import CONDS, QBARS, SEED, SWEEP, T, summary
from experiments.e2 import hpb_l_for

FLOORS = (256, 1024, 2048, 4096)
MODELS = ("est", "gt")
R = C.RESULTS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", choices=("dev", "fresh"), required=True)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    n, rep = (2000, 3) if a.fast else (5000, 5)
    out = os.path.join(R, f"e1g_robust_{a.pool}.csv")
    if a.pool == "fresh" and os.path.exists(out):
        raise SystemExit("e1g_robust_fresh.csv exists: the fresh run is done once and is not repeated")
    rl = RunLog(t=T, pool=a.pool, candidates="all of S~")
    w = rl.timed("world build", lambda: C.World(t=T, n_cand=None))
    gt = w.gt_weights()
    print(f"[gt] adjusted counts r* for r=1..5: {[round(float(gt[w.cnt == r][0]), 3) for r in range(1, 6)]}", flush=True)
    mem, seed = [w.base_member()], SEED[a.pool]

    def go(cond, sch, name, variant, param, tag, extra=None):
        return rl.timed(f"{cond} {variant} {param}", lambda: C.run(w, cond, sch, name, variant, param, n, rep, seed, pool=a.pool,
                                                                    tag=f"{tag}|{a.pool}", extra_cfg=extra, models=MODELS))

    rows, avg = [], {}
    for qb in SWEEP:
        sch = atk.FSB(mem, qb, w.bits)
        avg[qb] = sch.sizes(w.h_S)[0]
        for c in CONDS:
            rows += go(c, sch, "fsb", "fsb_base", qb, f"base{qb}")
    for qb in QBARS:
        l = hpb_l_for(avg[qb], w.N)
        for c in CONDS:
            rows += go(c, atk.HPB(l), "hpb", f"match_qbar{qb}", l, f"hpb{qb}")
    for qb in QBARS:
        for g in FLOORS:
            sch = atk.FSBFloor(mem, qb, w.bits, g)
            for c in CONDS:
                rows += go(c, sch, "fsb", f"floor{g}", qb, f"floor{g}_{qb}", extra={"floor": g})
    C.write_csv(out, rows, C.COLS1B)
    rl.save(os.path.join(R, f"e1g_robust_{a.pool}_runs.csv"))
    df = pd.DataFrame(rows)
    lines = []
    for m, label in (("est", "est attacker (ranks by the server's estimate)"), ("gt", "gt attacker (Good-Turing adjusted counts)")):
        _, ls = summary(df[df.attacker == m], a.pool, label)
        lines += ls + [""]
    open(os.path.join(R, f"e1g_robust_{a.pool}_summary.txt"), "w").write("\n".join(lines))
    print("\n".join(lines))
    del w
    gc.collect()


if __name__ == "__main__":
    main()
