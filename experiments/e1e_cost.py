"""Phase 1e item 5: cost of one attacker, measured in a FRESH process per configuration (so the peak RSS belongs to that configuration only).
  python -I -m experiments.e1e_cost --model emp --cand all     (also: --cand 2M, --model est)
One cold M0, FSB qbar = 100, t = 1M run split into stages; appends one row to results/e1e_cost.csv. Targets: 5 repeats x 5,000, the E2 seed."""
import argparse
import csv
import os
import time

import numpy as np

from c3sim import attacker as atk
from c3sim import data
from experiments import common as C
from experiments.e1e_common import cur_rss_gb, peak_rss_gb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=("emp", "est"), required=True)
    ap.add_argument("--cand", choices=("2M", "all"), required=True)
    a = ap.parse_args()
    st = {}
    t0 = time.perf_counter()
    w = C.World(t=1_000_000, n_cand=None if a.cand == "all" else C.N_CAND)
    st["world_build_s"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    att, (tp, tc), _ = w.condition("M0", model=a.model)
    st["attacker_build_s"] = time.perf_counter() - t0  # for est this includes ordering S~ by p^
    scheme = atk.FSB([w.base_member()], 100, w.bits)
    t0 = time.perf_counter()
    att.index(scheme, "cost")
    st["index_build_s"] = time.perf_counter() - t0  # gamma for every candidate + grouping/sorting
    t0 = time.perf_counter()
    for r in range(5):
        atk.play(att, scheme, "cost", tp[data.sample_targets(tp, tc, 5000, 2000 + r)], np.random.default_rng(3000 + r))
    st["games_5x5000_s"] = time.perf_counter() - t0
    row = dict(attacker=a.model, candidates=a.cand, n_candidates=len(att.pw), **{k: round(v, 1) for k, v in st.items()},
               total_s=round(sum(st.values()), 1), rss_now_gb=round(cur_rss_gb(), 2), peak_rss_gb=round(peak_rss_gb(), 2))
    p = os.path.join(C.RESULTS, "e1e_cost.csv")
    new = not os.path.exists(p)
    with open(p, "a", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(row))
        if new:
            wr.writeheader()
        wr.writerow(row)
    print(row)


if __name__ == "__main__":
    main()
