"""Phase 1h: how much do the headline numbers move when the leak is split again? Four independent account splits of RockYou:
the paper's split (seeds 101, 102, 103) and three new ones (111-113, 121-123, 131-133), each with its own server estimate and attackers.
Targets: A_test of that split (not tuned on), seed 2000, 5 repeats x 5,000 targets, emp + gt + est attackers over all of S~, t = 1,000,000.
Configurations are fixed in advance (nothing is selected here): plain FSB qbar = 100, FSB qbar = 100 with floor 2,048 (chosen on the paper's dev pool, so
the new splits are out of sample for it), and size-matched HPB. Conditions M0 and M2x.
  python -I -m experiments.e1h_splits            -> results/e1h_splits.csv, e1h_splits_runs.csv, e1h_splits_log.txt"""
import argparse
import gc
import os

from c3sim import attacker as atk
from experiments import common as C
from experiments.e1e_common import RunLog
from experiments.e2 import hpb_l_for

T = 1_000_000
QB, FLOOR = 100, 2048
SPLITS = {101: (101, 102, 103), 111: (111, 112, 113), 121: (121, 122, 123), 131: (131, 132, 133)}
MODELS = ("emp", "gt", "est")
COLS = C.COLS1B + ["split"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    n, rep = (2000, 3) if a.fast else (5000, 5)
    rows = []
    rl = RunLog(t=T, candidates="all of S~")
    for name, seeds in SPLITS.items():
        w = rl.timed(f"split {name} world build", lambda: C.World(t=T, n_cand=None, split_seeds=seeds))
        mem = [w.base_member()]
        plain = atk.FSB(mem, QB, w.bits)
        l = hpb_l_for(plain.sizes(w.h_S)[0], w.N)
        cfgs = [("fsb", "fsb_base", QB, plain), ("fsb", f"floor{FLOOR}", QB, atk.FSBFloor(mem, QB, w.bits, FLOOR)), ("hpb", f"match_qbar{QB}", l, atk.HPB(l))]
        for cond in ("M0", "M2x"):
            for sch, variant, param, scheme in cfgs:
                out = rl.timed(f"split {name} {cond} {variant}", lambda: C.run(w, cond, scheme, sch, variant, param, n, rep, 2000, tag=f"{variant}|split{name}",
                                                                              extra_cfg={"split": list(seeds)}, models=MODELS))
                for r in out:
                    r["split"] = name
                rows += out
        del w
        gc.collect()
    C.write_csv(os.path.join(C.RESULTS, "e1h_splits.csv"), rows, COLS)
    rl.save(os.path.join(C.RESULTS, "e1h_splits_runs.csv"))


if __name__ == "__main__":
    main()
