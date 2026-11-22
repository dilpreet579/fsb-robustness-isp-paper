"""Phase 1g: a floor on gamma (every string gets at least g copies), against the full emp attacker (all of S~), t = 1,000,000.
  python -I -m experiments.e1g_floor --pool dev      # base qbar sweep, size-matched HPB, floor grid; M0 and M2x on A_dev  -> e1g_floor_dev.csv, selection
  python -I -m experiments.e1g_floor --pool fresh    # the same grid on A_fresh, once (refuses to rerun)                  -> e1g_floor_fresh.csv
Selection (fixed BEFORE the dev run, dev pool only): score of a (qbar, floor) configuration = mean over M0 and M2x of
  [loss of the floored scheme at q = 100] - [loss of plain FSB at q = 100, interpolated in log(average bucket size) on the qbar sweep at the SAME
  average bucket size]; lower is better (negative = the floor beats simply raising qbar). Configurations outside the sweep's size range are
  not scored but are listed and run. Every configuration is reported on the fresh pool; the dev-selected one is only flagged."""
import argparse
import gc
import json
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from experiments import common as C
from experiments.e1e_common import RunLog
from experiments.e2 import hpb_l_for

T = 1_000_000
QBARS = (10, 100, 1000)
FLOORS = (2, 4, 16, 64, 256, 1024, 2048, 4096, 8192, 16384)
SWEEP = (1, 3, 10, 30, 100, 300, 1000, 3000)
SEED = {"dev": 5000, "fresh": 6000}
CONDS = ("M0", "M2x")
R = C.RESULTS


def interp(d, budget, q=100):
    d = d[d.q == q].sort_values("avg_bucket")
    if d.empty or not d.avg_bucket.min() <= budget <= d.avg_bucket.max():
        return np.nan
    return float(np.interp(np.log(budget), np.log(d.avg_bucket), d.loss))


def gains(df):
    """One row per floored configuration: average bucket, floored loss at q=100 and plain-FSB loss at the same average bucket size, per condition."""
    base = df[df.variant == "fsb_base"]
    out = []
    for (v, qb), d in df[df.variant.str.startswith("floor")].groupby(["variant", "param"]):
        r = dict(variant=v, qbar=int(qb), floor=int(v[5:]), avg_bucket=float(d.avg_bucket.iloc[0]))
        for c in CONDS:
            fl = float(d[(d.condition == c) & (d.q == 100)].loss.iloc[0])
            bs = interp(base[base.condition == c], r["avg_bucket"])
            r[f"{c}_floor_q100"], r[f"{c}_base_same_size_q100"], r[f"{c}_gain"] = fl, bs, fl - bs
        r["score"] = float(np.nanmean([r[f"{c}_gain"] for c in CONDS])) if not any(np.isnan(r[f"{c}_gain"]) for c in CONDS) else np.nan
        out.append(r)
    return pd.DataFrame(out).sort_values(["qbar", "floor"]).reset_index(drop=True)


def summary(df, pool, who="emp attacker"):
    g = gains(df)
    lines = [f"Gamma floor on the {pool} pool ({who}, all of S~, t=1M). gain = floored loss at q=100 minus plain-FSB loss at q=100 at the SAME average bucket size "
             "(interpolated on the qbar sweep); negative = the floor beats raising qbar.",
             f"{'qbar':>5} {'floor':>6} {'avg_bucket':>10} | " + " ".join(f"{c}: floor/base/gain".rjust(26) for c in CONDS) + " |  score"]
    for _, r in g.iterrows():
        lines.append(f"{r.qbar:>5} {r.floor:>6} {r.avg_bucket:>10.1f} | " +
                     " ".join(f"{r[c + '_floor_q100']:8.2f}/{r[c + '_base_same_size_q100']:8.2f}/{r[c + '_gain']:+7.2f}" for c in CONDS) + f" | {r.score:+7.2f}")
    return g, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", choices=("dev", "fresh"), required=True)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    n, rep = (2000, 3) if a.fast else (5000, 5)
    out = os.path.join(R, f"e1g_floor_{a.pool}.csv")
    sel_path = os.path.join(R, "e1g_floor_selection.json")
    if a.pool == "fresh":
        if os.path.exists(out):
            raise SystemExit("e1g_floor_fresh.csv exists: the fresh run is done once and is not repeated")
        if not os.path.exists(sel_path):
            raise SystemExit("run --pool dev first (the selection is made on the dev pool)")
    rl = RunLog(t=T, pool=a.pool, candidates="all of S~")
    w = rl.timed("world build", lambda: C.World(t=T, n_cand=None))
    mem, seed = [w.base_member()], SEED[a.pool]
    for qb in (10, 100, 1000):  # why the floor sizes matter: copies a count-1 password would need for the same flat score as the qbar-th password
        print(f"[ref] count of rank-{qb} password = {int(w.cnt[qb - 1]):,}; |B| / count = {(1 << w.bits) / w.cnt[qb - 1]:,.0f} copies for a count-1 password", flush=True)

    def go(cond, sch, name, variant, param, tag, extra=None):
        return rl.timed(f"{cond} {variant} {param}", lambda: C.run(w, cond, sch, name, variant, param, n, rep, seed, pool=a.pool,
                                                                    tag=f"{tag}|{a.pool}", extra_cfg=extra, models=("emp",)))

    rows, avg = [], {}
    for qb in SWEEP:  # plain FSB qbar sweep (the equal-bucket-size reference)
        sch = atk.FSB(mem, qb, w.bits)
        avg[qb] = sch.sizes(w.h_S)[0]
        for c in CONDS:
            rows += go(c, sch, "fsb", "fsb_base", qb, f"base{qb}")
    for qb in QBARS:  # size-matched HPB
        l = hpb_l_for(avg[qb], w.N)
        for c in CONDS:
            rows += go(c, atk.HPB(l), "hpb", f"match_qbar{qb}", l, f"hpb{qb}")
    for qb in QBARS:  # the floor grid
        for g in FLOORS:
            sch = atk.FSBFloor(mem, qb, w.bits, g)
            for c in CONDS:
                rows += go(c, sch, "fsb", f"floor{g}", qb, f"floor{g}_{qb}", extra={"floor": g})
    C.write_csv(out, rows, C.COLS1B)
    rl.save(os.path.join(R, f"e1g_floor_{a.pool}_runs.csv"))
    df = pd.DataFrame(rows)
    g, lines = summary(df, a.pool)
    if a.pool == "dev":
        ok = g.dropna(subset=["score"])
        best = ok.loc[ok.score.idxmin()]
        lines.append(f"selected on dev: qbar={int(best.qbar)} floor={int(best.floor)} (score {best.score:+.2f}); {len(g) - len(ok)} configurations outside the qbar sweep size range were not scored")
        json.dump({"qbar": int(best.qbar), "floor": int(best.floor), "score": float(best.score)}, open(sel_path, "w"))
    else:
        sel = json.load(open(sel_path))
        lines.append(f"dev-selected configuration (flag only): qbar={sel['qbar']} floor={sel['floor']}")
    open(os.path.join(R, f"e1g_floor_{a.pool}_summary.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    del w
    gc.collect()


if __name__ == "__main__":
    main()
