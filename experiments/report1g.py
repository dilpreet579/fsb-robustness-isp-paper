"""Phase 1g report (results/REPORT_1g.md): gamma floor. Numbers and method statements only; reads results/e1g_*.csv."""
import os
import re

import pandas as pd

from experiments import common as C

R = C.RESULTS
FLOORS_ALL = (256, 1024, 2048, 4096, 8192, 16384)
POOLS = ("dev", "fresh")


def load():
    out = {}
    for p in POOLS:
        a = pd.read_csv(os.path.join(R, f"e1g_floor_{p}.csv"))
        b = pd.read_csv(os.path.join(R, f"e1g_robust_{p}.csv"))
        out[p] = pd.concat([a, b], ignore_index=True)
    return out


def cell(d, cond, att, variant, qb, q):
    x = d[(d.condition == cond) & (d.attacker == att) & (d.variant == variant) & (d.param == qb) & (d.q == q)]
    return "n/a" if x.empty else f"{x.loss.iloc[0]:+.2f} ±{x.std_over_repeats.iloc[0]:.2f}"


def avg_of(d, variant, qb):
    x = d[(d.variant == variant) & (d.param == qb)]
    return float(x.avg_bucket.iloc[0])


def table(d, cond, qb, qs):
    hdr = "| config | avg bucket | " + " | ".join(f"{a} q={q}" for a in ("emp", "gt", "est") for q in qs) + " |"
    lines = [hdr, "|" + "---|" * (2 + 3 * len(qs))]
    for v, name in [("fsb_base", "plain FSB")] + [(f"floor{g}", f"floor {g}") for g in FLOORS_ALL]:
        lines.append(f"| qbar={qb} {name} | {avg_of(d, v, qb):,.0f} | " + " | ".join(cell(d, cond, a, v, qb, q) for a in ("emp", "gt", "est") for q in qs) + " |")
    h = d[(d.variant == f"match_qbar{qb}") & (d.condition == cond)]
    if not h.empty:
        l = int(h.param.iloc[0])
        lines.append(f"| size-matched HPB l={l} | {h.avg_bucket.iloc[0]:,.0f} | " +
                     " | ".join(cell(d, cond, a, f"match_qbar{qb}", l, q) for a in ("emp", "gt", "est") for q in qs) + " |")
    return "\n".join(lines)


def runtimes():
    tot = {}
    for stem in ("e1g_floor_dev", "e1g_floor_fresh", "e1g_robust_dev", "e1g_robust_fresh"):
        f = os.path.join(R, f"{stem}_runs.csv")
        if os.path.exists(f):
            x = pd.read_csv(f)
            tot[stem] = (x.seconds.sum() / 60, x.peak_rss_so_far_gb.max())
    return tot


def main():
    d = load()
    ref = [ln.strip() for ln in open(os.path.join(R, "e1g_floor_dev_log.txt")) if ln.startswith("[ref]")]
    gt = [ln.strip() for ln in open(os.path.join(R, "e1g_robust_dev_log.txt")) if ln.startswith("[gt]")]
    sel = open(os.path.join(R, "e1g_floor_dev_summary.txt")).read().strip().splitlines()[-1]
    o = ["# REPORT 1g (Phase 1g: a floor on gamma)", "",
         "Numbers and method statements only. Earlier phases' results were not modified; Phase 1g adds `results/e1g_*`, `experiments/e1g_floor.py`, "
         "`experiments/e1g_robust.py`, `experiments/report1g.py`, `tests/test_phase1g.py`, the class `FSBFloor` in `c3sim/attacker.py` and the attacker model `gt` "
         "(`World.gt_weights`) in `experiments/common.py`. The paper (`paper/`) was not changed.", "",
         "## 1. What was run", "",
         "- **Scheme (`FSBFloor`)**: gamma(w) = min(|B|, max(gamma_FSB(w), g)) for every string w (a function of the string only, so the client computes it without knowing whether w is stored). g = 1 is plain FSB. t = 1,000,000, |B| = 2^24, N = 13,125,513.",
         "- **Grid**: qbar in {10, 100, 1000}, g in {2, 4, 16, 64, 256, 1024, 2048, 4096, 8192, 16384}; plain FSB qbar sweep {1, 3, 10, 30, 100, 300, 1000, 3000}; size-matched HPB for qbar in {10, 100, 1000}. Conditions M0 and M2x.",
         "- **Pools and seeds**: tuned on A_dev (seed 5000), reported on A_fresh (seed 6000), 5 repeats x 5,000 targets; the fresh run is done once (the scripts refuse to rerun it). A `--fast` smoke run (2,000 x 3, A_dev) preceded the full dev run; it is kept as `e1g_floor_dev_fast_smoke*`.",
         "- **Attackers**: `emp` = raw leak counts over all of S~ (the headline attacker of the paper); `est` = the server's estimate over all of S~; `gt` = Good-Turing adjusted counts (Turing r* = (r+1) n_{r+1}/n_r for counts r <= 5, raw above). "
         "`est` and `gt` were added after the dev run of `emp` showed non-monotone and negative losses (section 4), and were fixed before any fresh-pool run of them. " + (gt[0] if gt else ""), "",
         "Reference counts (dev log): " + "; ".join(r.replace("[ref] ", "") for r in ref), "",
         "## 2. Pre-registered selection (dev pool only)", "",
         "Rule (written in `e1g_floor.py` before the dev run): score = mean over M0 and M2x of [floored loss at q = 100] - [plain-FSB loss at q = 100 interpolated at the same average bucket size], emp attacker; lowest score wins.", "",
         f"Result: `{sel}`", "",
         "The selected configuration (qbar = 10) is evaluated at q = 100, i.e. beyond its qbar, and against the raw-count attacker only; section 4 shows that this attacker is not the strongest one. The rule is reported as specified; a rule that scores loss at q = qbar against the worst attacker was not run as a selection.", ""]
    for cond in ("M0", "M2x"):
        for qb in (100,):
            o += [f"## 3. {cond}, fresh pool, qbar = {qb}: loss in points at q = 1, 10, {qb} and 1000", "",
                  table(d["fresh"], cond, qb, (1, 10, qb, 1000)), "",
                  "`n/a` = not run for that attacker (est and gt were run for floors 256, 1024, 2048, 4096 only). Values are mean ±sd over 5 repeats. A negative loss means the attacker did worse with the bucket than the same attacker without it.", ""]
    for cond in ("M0", "M2x"):
        for qb in (10, 1000):
            qs = tuple(sorted({1, qb, 1000}))
            o += [f"### {cond}, fresh pool, qbar = {qb}: loss in points at q = {', '.join(map(str, qs))}", "", table(d["fresh"], cond, qb, qs), ""]
    o += ["## 4. Worst case over the three attackers (fresh pool)", "",
          "Largest loss over emp, gt and est, at the largest q <= qbar and at q = 1000, and the average bucket size relative to plain FSB with the same qbar. "
          "Floors 8192 and 16384 were run for emp only and are not in this table.", "",
          "| cond | qbar | config | avg bucket (x plain FSB) | worst loss at q = qbar | worst loss at q = 1000 |", "|---|---|---|---|---|---|"]
    f = d["fresh"]
    for cond in ("M0", "M2x"):
        for qb in (10, 100, 1000):
            base_avg = avg_of(f, "fsb_base", qb)
            for v, name in [("fsb_base", "plain FSB")] + [(f"floor{g}", f"floor {g}") for g in (256, 1024, 2048, 4096)]:
                x = f[(f.condition == cond) & (f.variant == v) & (f.param == qb) & f.attacker.isin(["emp", "gt", "est"])]
                w1 = x[x.q == qb].loss.max()
                w2 = x[x.q == 1000].loss.max()
                o.append(f"| {cond} | {qb} | {name} | {avg_of(f, v, qb):,.0f} ({avg_of(f, v, qb) / base_avg:.2f}x) | {w1:+.2f} | {w2:+.2f} |")
    o += ["", "Per-configuration gains against plain FSB at the same average bucket size (q = 100, dev and fresh): `e1g_floor_*_summary.txt` (emp), `e1g_robust_*_summary.txt` (est, gt).", ""]
    o += ["## 4b. Checks", "", "`tests/test_phase1g.py` (output in `e1g_tests.txt`): floor = 1 equals plain FSB; gamma >= floor and <= |B|; floor never lowers gamma; average bucket = sum(gamma)/|B|; "
          "the sorted-class lookup equals a naive scan on every 7th bucket with a floor; Good-Turing weights adjust counts <= rmax only.", ""]
    rt = runtimes()
    o += ["## 5. Runtimes", "", "| run | wall minutes (sum of per-run seconds) | peak RSS (GB) |", "|---|---|---|"]
    o += [f"| {k} | {v[0]:.1f} | {v[1]:.2f} |" for k, v in rt.items()]
    o += ["", "## 6. Reproduce", "", "    .venv/bin/python -I -m pytest -q tests/test_phase1g.py", "    make phase1g      # dev, fresh (once), robust dev, robust fresh (once), report", ""]
    open(os.path.join(R, "REPORT_1g.md"), "w").write("\n".join(o))
    print("wrote results/REPORT_1g.md")


if __name__ == "__main__":
    main()
