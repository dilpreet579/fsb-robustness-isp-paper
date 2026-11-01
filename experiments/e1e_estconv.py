"""Phase 1e item 3: est-attacker convergence at t = 1,000,000, candidate list 2M vs all of S~. Seed 2000, A_test, est attacker only.
M0 and M2x, FSB qbar in {10,100,1000}, all q; plus M3 sigma = 0.75, noise draw d1 (salt c3sim-noise-v1-d1), qbar = 100.
Rows carry the list in `variant` (… cand2M / … candall). -> e1e_estconv.csv"""
import gc
import os

from c3sim import attacker as atk
from experiments import common as C

T = 1_000_000


def main():
    a = C.args("Phase 1e est convergence")
    rows = []
    for tag, nc in (("cand2M", C.N_CAND), ("candall", None)):
        w = C.World(t=T, n_cand=nc)
        for cond in ("M0", "M2x"):
            for qb in (10, 100, 1000):
                rows += C.run(w, cond, atk.FSB([w.base_member()], qb, w.bits), "fsb", f"fsb_base {tag}", qb, a.n_targets, a.repeats, 2000,
                              tag=tag, models=("est",))
        mem = [w.noisy_member(0.75, b"c3sim-noise-v1-d1")]
        rows += C.run(w, "M3", atk.FSB(mem, 100, w.bits), "fsb", f"noise_s0.75_d1 {tag}", 100, a.n_targets, a.repeats, 2000, tag=tag,
                      extra_cfg={"sigma": 0.75, "salt": "c3sim-noise-v1-d1"}, models=("est",))
        del w
        gc.collect()
    C.write_csv(os.path.join(C.RESULTS, "e1e_estconv.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
