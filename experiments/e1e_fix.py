"""Phase 1e item 4: fixes against the full emp attacker (all of S~), t = 1,000,000, seed 2000, A_test, emp only.
Variants: fsb_base; smoothed (Kneser-Ney 3-gram); cal_iso_w0.5 (EXPLORATORY: Phase 1b calibration, isotonic, 0.5-decade bins, fitted with the
t = 1M pipeline of e1c_fix.py, i.e. cross-fit on a 90/10 split of A_train). Conditions M0 and M2x. qbar sweep 1..3000 as in e1c_base_sweep.
Compared at equal average bucket size by interpolation in the report. -> e1e_fix.csv, e1e_fix_runs.csv"""
import os

from c3sim import attacker as atk
from c3sim import calibration
from experiments import common as C
from experiments.e1b_fix import VARIANTS as CAL_VARIANTS
from experiments.e1e_common import RunLog

T = 1_000_000
SWEEP = (1, 3, 10, 30, 100, 300, 1000, 3000)


def main():
    a = C.args("Phase 1e fixes vs full emp attacker")
    rl = RunLog(t=T, candidates="all of S~")
    w = C.World(t=T, n_cand=None)
    cal = calibration.fit(w, **CAL_VARIANTS["cal_iso_w0.5"])
    members = {"fsb_base": [w.base_member()], "smoothed": w.members("smoothed"), "cal_iso_w0.5": [(C.memo(cal.phat), cal.phat_ranked(w.pw))]}
    rows = []
    for v, mem in members.items():
        for qb in SWEEP:
            sch = atk.FSB(mem, qb, w.bits)
            for cond in ("M0", "M2x"):
                rows += rl.timed(f"{v} {cond} qbar={qb}", lambda: C.run(w, cond, sch, "fsb", v, qb, a.n_targets, a.repeats, 2000, tag=v, models=("emp",)))
    C.write_csv(os.path.join(C.RESULTS, "e1e_fix.csv"), rows, C.COLS1B)
    rl.save(os.path.join(C.RESULTS, "e1e_fix_runs.csv"))


if __name__ == "__main__":
    main()
