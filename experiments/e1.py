"""E1: matched condition M0. HPB l=7..16 (avg bucket ~100k .. ~200), FSB qbar in {1,10,100,1000,10000}."""
import os

import pandas as pd

from c3sim import attacker as atk
from experiments import common as C

SEED = 1000
QBARS = (1, 10, 100, 1000, 10000)
LS = tuple(range(7, 17))


def check(df, out):
    lines = ["E1 acceptance checks (plan T5)"]
    ok_all = {}
    for m in C.MODELS:
        d = df[df.attacker == m]
        f = d[d.scheme == "fsb"]
        bad = [(int(r.param), int(r.q), r.loss, r.std_over_repeats) for r in f.itertuples() if r.q <= r.param and r.loss > 1.0]
        lines.append(f"[{m}] FSB loss <= 1 point for every q <= qbar: {'PASS' if not bad else 'FAIL'}"
                     + ("" if not bad else f"  violations (qbar, q, loss, sd): {bad}"))
        h = d[(d.scheme == "hpb") & (d.q == 1000)].copy()
        h["dist"] = (h.avg_bucket - 7000).abs()
        r = h.sort_values("dist").iloc[0]
        ok_h = r.loss >= 20
        lines.append(f"[{m}] HPB at {r.avg_bucket:.0f} entries/bucket (l={int(r.param)}) loses {r.loss:.1f} points at q=1000 "
                     f"(expect tens of points): {'PASS' if ok_h else 'FAIL'}")
        ok_all[m] = (not bad) and ok_h
    lines.append("overall: " + ", ".join(f"{m}={'PASS' if v else 'FAIL'}" for m, v in ok_all.items()))
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return ok_all


def main():
    a = C.args("E1")
    w = C.World()
    rows = []
    for l in LS:
        rows += C.run(w, "M0", atk.HPB(l), "hpb", "", l, a.n_targets, a.repeats, SEED)
    for qb in QBARS:
        rows += C.run(w, "M0", atk.FSB([w.base_member()], qb, w.bits), "fsb", "fsb_base", qb, a.n_targets, a.repeats, SEED)
    C.write_csv(os.path.join(C.RESULTS, "e1.csv"), rows)
    check(pd.DataFrame(rows), os.path.join(C.RESULTS, "E1_check.txt"))

    cand_check(a, w)


def cand_check(a, w2m):
    """Candidate-list convergence: same targets and buckets, list = top 1M / 2M / 4M / all of S~."""
    cc = []
    for lab, nc in (("1M", 1_000_000), ("2M", 2_000_000), ("4M", 4_000_000), ("all", None)):
        ww = w2m if lab == "2M" else C.World(n_cand=nc or w2m.N)
        for sch, nm, v, p in ((atk.HPB(11), "hpb", "", 11), (atk.HPB(8), "hpb", "", 8),
                              (atk.FSB([ww.base_member()], 100, ww.bits), "fsb", "fsb_base", 100)):
            for r in C.run(ww, "M0", sch, nm, v, p, a.n_targets, a.repeats, SEED, tag=lab):
                r["variant"] = (r["variant"] + " " + lab).strip()
                cc.append(r)
        if lab != "2M":
            del ww
    C.write_csv(os.path.join(C.RESULTS, "cand_check.csv"), cc)
    d = pd.DataFrame(cc)
    d["cand"] = d.variant.str.split(" ").str[-1]
    p = d.pivot_table(index=["attacker", "scheme", "param", "q"], columns="cand", values="bucket_success")[["1M", "2M", "4M", "all"]]
    p["|1M-2M|"] = (p["1M"] - p["2M"]).abs()
    p["|2M-all|"] = (p["2M"] - p["all"]).abs()
    txt = "Candidate-list convergence: bucket success (%) on identical targets/buckets\n" + p.round(3).to_string() + \
          "\n\nmax |1M-2M| (the plan's check) by attacker:\n" + p.groupby("attacker")["|1M-2M|"].max().round(3).to_string() + \
          "\nmax |2M-all| by attacker:\n" + p.groupby("attacker")["|2M-all|"].max().round(3).to_string()
    open(os.path.join(C.RESULTS, "cand_check.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
