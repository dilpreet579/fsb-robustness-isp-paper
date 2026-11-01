"""Phase 1d item 2: M3 with 5 independent noise draws (different hash salts), t = 1,000,000, est and emp, qbar in {10,100,1000},
sigma in {0.5, 0.75, 1.0} (+ 1.5 as a fallback anchor for crossings that fall beyond 1.0). Seed 2000, A_test (same targets as Phase 1c).
Variant = noise_s{sigma}_d{draw}; draw k uses salt b'c3sim-noise-v1-d{k}' (the Phase 1c draw is salt b'c3sim-noise-v1'). -> e1d_noise.csv"""
import os

from c3sim import attacker as atk
from experiments import common as C

SIGMAS = (0.5, 0.75, 1.0, 1.5)
DRAWS = (1, 2, 3, 4, 5)


def main():
    a = C.args("Phase 1d noise draws")
    w = C.World(t=1_000_000)
    rows = []
    for d in DRAWS:
        salt = f"c3sim-noise-v1-d{d}".encode()
        for s in SIGMAS:
            mem = [w.noisy_member(s, salt)]
            for qb in (10, 100, 1000):
                rows += C.run(w, "M3", atk.FSB(mem, qb, w.bits), "fsb", f"noise_s{s}_d{d}", qb, a.n_targets, a.repeats, 2000,
                              tag=f"d{d}", extra_cfg={"sigma": s, "salt": salt.decode()})
    C.write_csv(os.path.join(C.RESULTS, "e1d_noise.csv"), rows, C.COLS1B)


if __name__ == "__main__":
    main()
