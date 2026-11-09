"""Phase 1f item 1: where does the emp attacker's success come from? t = 1,000,000, seed 2000, pool A_test, emp attacker = ALL of S~.
M0 and M2x, FSB qbar = 100 and size-matched HPB (l = 12), q = 1 and q = 100. The games replay Phase 1e exactly (same targets, same bucket draws),
and the totals are asserted equal to results/e1e_headline.csv.

Target groups (by the target's password):
  head = in S~ and among the top t passwords of A_train by count (rank < t, the histogram head of p^)
  tail = stored in S~ but not in the head
  none = not in S~ (the attacker has no candidate for it, so it can never be guessed)
Per group: share of targets, bucket success, baseline success (both within the group) and loss contribution = share * (success - baseline), which sums to the loss.
Also: distribution of gamma and of the leak count (count in A_train) of the targets guessed correctly, and of the newly gained ones (bucket success, no baseline success).
Outputs: e1f_mech_groups.csv, e1f_mech_dist.csv, e1f_mech_quantiles.csv"""
import os

import numpy as np
import pandas as pd

from c3sim import attacker as atk
from c3sim import data
from experiments import common as C
from experiments.e2 import hpb_l_for

T = 1_000_000
GROUPS = ("head", "tail", "none")
QS = (1, 100)
GAMMA_EDGES = [2, 11, 101, 1001, 10_001, 100_001, 1_000_001]  # bins: 1 | 2-10 | 11-100 | 101-1k | 1k-10k | 10k-100k | 100k-1M | 1M..|B|-1 | |B|
GAMMA_LABELS = ["1", "2-10", "11-100", "101-1k", "1k-10k", "10k-100k", "100k-1M", "1M to <|B|", "|B| (every bucket)"]
COUNT_EDGES = [1, 2, 3, 6, 21, 101, 1001, 10_001]
COUNT_LABELS = ["0 (not in S~)", "1", "2", "3-5", "6-20", "21-100", "101-1k", "1k-10k", ">10k"]


def group_of(train_idx, t):
    """0 = head, 1 = tail (stored, not head), 2 = not in S~. train_idx = row in A_train (rank by count) or -1."""
    return np.where(train_idx < 0, 2, np.where(train_idx < t, 0, 1))


def gamma_bin(g, B):
    b = np.digitize(g, GAMMA_EDGES)  # 0 -> gamma 1 ... 6 -> 100k..1M, 7 -> >= 1M+1
    return np.where(g >= B, 8, b)


def count_bin(c):
    return np.digitize(c, COUNT_EDGES)


def main():
    a = C.args("Phase 1f mechanism")
    w = C.World(t=T, n_cand=None)
    srt = np.argsort(w.pw)
    spw = w.pw[srt]
    B = 1 << w.bits
    fsb = atk.FSB([w.base_member()], 100, w.bits)
    l = hpb_l_for(fsb.sizes(w.h_S)[0], w.N)
    schemes = {"fsb": (fsb, 100), "hpb": (atk.HPB(l), 100)}
    ref = pd.read_csv(os.path.join(C.RESULTS, "e1e_headline.csv"))
    grows, drows, qrows = [], [], []
    for cond in ("M0", "M2x"):
        att, (tp, tc), pool = w.condition(cond, model="emp")
        for sname, (sch, qbar) in schemes.items():
            per = []  # per repeat: dict of arrays
            for r in range(a.repeats):
                tgt = tp[data.sample_targets(tp, tc, a.n_targets, 2000 + r)]
                out = atk.play(att, sch, f"mech|{cond}|{sname}", tgt, np.random.default_rng(3000 + r))
                top, tr = out["top"], out["tr"]
                eq = top == tr[:, None]
                pos = np.where(eq.any(1), eq.argmax(1), 1000)
                s = np.searchsorted(spw, tgt)
                s[s == len(spw)] = 0
                tidx = np.where(spw[s] == tgt, srt[s], -1)
                per.append(dict(pos=pos, tr=tr, grp=group_of(tidx, T), gamma=out["gamma"], leak=np.where(tidx >= 0, w.cnt[np.maximum(tidx, 0)], 0)))
            for q in QS:
                reps = []
                for p in per:
                    bs = p["pos"] < q
                    bl = (p["tr"] >= 0) & (p["tr"] < q)
                    n = len(bs)
                    rec = {}
                    for gi, g in enumerate(GROUPS):
                        m = p["grp"] == gi
                        rec[g] = dict(share=m.mean() * 100, succ=bs[m].mean() * 100 if m.any() else np.nan, base=bl[m].mean() * 100 if m.any() else np.nan,
                                      contrib=(bs[m].sum() - bl[m].sum()) / n * 100, succ_contrib=bs[m].sum() / n * 100, base_contrib=bl[m].sum() / n * 100)
                    rec["total"] = dict(share=100.0, succ=bs.mean() * 100, base=bl.mean() * 100, contrib=(bs.sum() - bl.sum()) / n * 100,
                                        succ_contrib=bs.mean() * 100, base_contrib=bl.mean() * 100)
                    reps.append(rec)
                for g in (*GROUPS, "total"):
                    row = dict(condition=cond, scheme=sname, qbar=qbar, q=q, group=g, targets_pooled=int(sum((p["grp"] == GROUPS.index(g)).sum() if g != "total" else len(p["grp"]) for p in per)))
                    for k in ("share", "succ", "base", "contrib", "succ_contrib", "base_contrib"):
                        v = np.array([rc[g][k] for rc in reps])
                        row[k] = round(float(np.nanmean(v)), 3)
                        row[k + "_sd"] = round(float(np.nanstd(v, ddof=1)), 3)
                    grows.append(row)
                # cross-check against Phase 1e (same seeds, same targets): total success and baseline
                tot = [x for x in grows if x["condition"] == cond and x["scheme"] == sname and x["q"] == q and x["group"] == "total"][-1]
                e = ref[(ref.condition == cond) & (ref.scheme == sname) & (ref.q == q) & (ref.attacker == "emp") &
                        ((ref.param == 100) if sname == "fsb" else (ref.variant == "match_qbar100"))].iloc[0]
                assert abs(tot["succ"] - e.bucket_success) < 5e-3 and abs(tot["base"] - e.baseline_success) < 5e-3, (cond, sname, q, tot, e.bucket_success, e.baseline_success)
                # distributions of gamma and leak count among correct / newly gained targets (pooled over the repeats)
                cat = {k: np.concatenate([p[k] for p in per]) for k in ("pos", "tr", "grp", "gamma", "leak")}
                bs = cat["pos"] < q
                bl = (cat["tr"] >= 0) & (cat["tr"] < q)
                for subset, mask in (("correct", bs), ("newly_gained", bs & ~bl)):
                    for gname, gm in (("all", np.ones_like(bs)), ("head", cat["grp"] == 0), ("tail", cat["grp"] == 1)):
                        m = mask & gm
                        for var, vals, bins, labels in (("gamma", cat["gamma"][m], gamma_bin(cat["gamma"][m], B), GAMMA_LABELS),
                                                        ("leak_count", cat["leak"][m], count_bin(cat["leak"][m]), COUNT_LABELS)):
                            cnt = np.bincount(bins, minlength=len(labels))
                            for lab, c_ in zip(labels, cnt):
                                drows.append(dict(condition=cond, scheme=sname, q=q, subset=subset, group=gname, variable=var, bin=lab, n=int(c_),
                                                  share_pct=round(100 * c_ / max(m.sum(), 1), 2)))
                            if m.sum():
                                qs_ = np.percentile(vals, [0, 10, 25, 50, 75, 90, 100])
                                qrows.append(dict(condition=cond, scheme=sname, q=q, subset=subset, group=gname, variable=var, n=int(m.sum()),
                                                  **dict(zip(["min", "p10", "p25", "p50", "p75", "p90", "max"], [float(x) for x in qs_])), mean=float(np.mean(vals))))
            att._ix.clear()
    pd.DataFrame(grows).to_csv(os.path.join(C.RESULTS, "e1f_mech_groups.csv"), index=False)
    pd.DataFrame(drows).to_csv(os.path.join(C.RESULTS, "e1f_mech_dist.csv"), index=False)
    pd.DataFrame(qrows).to_csv(os.path.join(C.RESULTS, "e1f_mech_quantiles.csv"), index=False)
    print(pd.DataFrame(grows)[["condition", "scheme", "q", "group", "share", "succ", "base", "contrib"]].round(2).to_string())


if __name__ == "__main__":
    main()
