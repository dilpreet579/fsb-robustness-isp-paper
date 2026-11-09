"""Phase 1f item 2: M3 with the lognormal noise applied ONLY to non-head strings (the histogram head, i.e. the top t = 1M passwords of A_train, keeps p^ exactly;
every other string, stored or not, gets p^ * exp(sigma z_w)). est attacker, FSB qbar = 100, sigma in {0.5, 1.0, 1.6}, 5 independent noise draws (salts c3sim-noise-v1-d1..d5, as Phase 1d),
seed 2000, pool A_test, t = 1M. For a like-for-like comparison the SAME draws are also run with the noise on every string (full noise), including sigma = 1.6, which Phase 1d did not have.
est list = top 2M of S~ by p^ (as Phase 1d's noise draws; est loss at q <= qbar is unchanged with all of S~, REPORT_1e section 3).
Variants: tailnoise_s{sigma}_d{k} / fullnoise_s{sigma}_d{k}.  -> e1f_tailnoise.csv"""
import os

import numpy as np

from c3sim import attacker as atk
from experiments import common as C

T = 1_000_000
SIGMAS = (0.5, 1.0, 1.6)
DRAWS = (1, 2, 3, 4, 5)
QBAR = 100


def tail_member(w, sigma, salt):
    """FSB member whose p^ is multiplied by exp(sigma z_w) for every string outside the histogram head; head strings are untouched.
    Returns (phat_fn(strings), ph_S) like World.noisy_member."""
    w.noisy_member(0.0, salt)  # fills the per-salt z cache for S~ (sigma = 0 -> unchanged estimate, only used for the side effect)
    z = w._zs[salt]
    ph_S = w.ph_S.copy()
    ph_S[w.t:] *= np.exp(sigma * z[w.t:])  # rows of S~ are sorted by count: rows >= t are the non-head passwords

    def fn(s):
        ph, head = w.est.phat_head(s)
        return ph * np.where(head, 1.0, np.exp(sigma * w.noise(s, salt)))

    return C.memo(fn), ph_S


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--attacker", choices=("est", "emp"), default="est", help="est (requested, 2M list) or emp (extra: all of S~)")
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    a.n_targets, a.repeats = (2000, 3) if a.fast else (5000, 5)
    w = C.World(t=T, n_cand=C.N_CAND if a.attacker == "est" else None)
    out = "e1f_tailnoise.csv" if a.attacker == "est" else "e1f_tailnoise_emp.csv"
    rows = []
    for d in DRAWS:
        salt = f"c3sim-noise-v1-d{d}".encode()
        for s in SIGMAS:
            for kind, mem in (("tailnoise", [tail_member(w, s, salt)]), ("fullnoise", [w.noisy_member(s, salt)])):
                rows += C.run(w, "M3", atk.FSB(mem, QBAR, w.bits), "fsb", f"{kind}_s{s}_d{d}", QBAR, a.n_targets, a.repeats, 2000,
                              tag=f"{kind}{d}", extra_cfg={"sigma": s, "salt": salt.decode(), "noise": kind}, models=(a.attacker,))
    C.write_csv(os.path.join(C.RESULTS, out), rows, C.COLS1B)


if __name__ == "__main__":
    main()
