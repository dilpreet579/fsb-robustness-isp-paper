"""Computation of every number the paper text may quote, from results/*.csv only.

A number is described by a row (op, source_csv, filter, column, [source_csv2, filter2], [extra]); `compute(row)` evaluates it. paper_numbers.py writes the rows with their
values to paper/numbers.csv; paper/check_numbers.py calls compute() again on every row and fails on any mismatch, so a stale or hand-edited value cannot survive.
filter syntax: "col=v1|v2;col2=v3" (all conditions must hold; `|` separates alternatives). Numeric columns compare as floats, others as strings."""
import json
import os

import numpy as np
import pandas as pd

from experiments.paper_common import RES

_cache = {}


def csv(name):
    if name not in _cache:
        _cache[name] = pd.read_csv(os.path.join(RES, name))
    return _cache[name]


def parse_filter(s):
    out = {}
    for part in (s or "").split(";"):
        if part.strip():
            k, v = part.split("=", 1)
            out[k.strip()] = v.split("|")
    return out


def select(df, filt):
    m = pd.Series(True, index=df.index)
    for col, vals in parse_filter(filt).items():
        if pd.api.types.is_numeric_dtype(df[col]):
            m &= df[col].isin([float(v) for v in vals])
        else:
            m &= df[col].astype(str).isin(vals)
    return df[m]


def _one(src, filt, col):
    d = select(csv(src), filt)
    assert len(d) == 1, f"{src} [{filt}]: expected 1 row, got {len(d)}"
    return float(d[col].iloc[0])


def interp_log(d, q, budget):
    """Loss at q interpolated log-linearly in average bucket size along a qbar sweep (nan outside the sweep)."""
    d = d[d.q == q].sort_values("avg_bucket")
    if len(d) < 2 or not (d.avg_bucket.min() <= budget <= d.avg_bucket.max()):
        return float("nan")
    return float(np.interp(np.log(budget), np.log(d.avg_bucket), d.loss))


def crossing(x, y, thr=5.0):
    """First x where y reaches thr (linear interpolation); None if it never does. y[0] >= thr gives x[0]."""
    if y[0] >= thr:
        return x[0]
    for i in range(1, len(x)):
        if y[i] >= thr:
            return x[i - 1] + (thr - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1])
    return None


SIGMAS = (0.5, 0.75, 1.0, 1.5)
DRAWS = (1, 2, 3, 4, 5)


def crossing5_per_draw(qbar, attacker="est"):
    """sigma at which the loss at q = qbar reaches 5 points, one value per noise draw (e1d_noise.csv; sigma = 0 anchor = noise-free M0 row of e1c_e2.csv)."""
    anchor = _one("e1c_e2.csv", f"condition=M0;scheme=fsb;variant=fsb_base;param={qbar};attacker={attacker};q={qbar}", "loss")
    noise = csv("e1d_noise.csv")
    out = []
    for d in DRAWS:
        ys = [anchor]
        for s in SIGMAS:
            ys.append(_one("e1d_noise.csv", f"variant=noise_s{s}_d{d};param={qbar};attacker={attacker};q={qbar}", "loss"))
        out.append(crossing([0.0, *SIGMAS], ys))
    return out


def _s(v):
    """Empty CSV cells come back as NaN; treat anything that is not a string as ''."""
    return v if isinstance(v, str) else ""


def compute(row):
    op, src, filt, col = row["op"], _s(row["source_csv"]), _s(row.get("filter")), _s(row.get("column"))
    row = {**row, "source_csv2": _s(row.get("source_csv2")), "filter2": _s(row.get("filter2"))}
    extra = json.loads(row["extra"]) if isinstance(row.get("extra"), str) and row["extra"] else {}
    if op == "value":
        return _one(src, filt, col)
    if op == "max_of":  # largest of several single-row values of one column: extra = {"parts": [[source_csv, filter], ...]} (Phase 1g: worst case over attackers)
        return max(_one(s, f, col) for s, f in extra["parts"])
    if op == "split_worst":  # Phase 1h: per split the largest loss over the rows left by the filter (attackers), then extra["stat"] over the splits
        v = select(csv(src), filt).groupby("split")[col].max().to_numpy(dtype=float)
        return {"mean": float(v.mean()), "sd": float(v.std(ddof=1)), "min": float(v.min()), "max": float(v.max()), "n": float(len(v))}[extra["stat"]]
    d = select(csv(src), filt) if src else None
    if op == "sum":
        return float(d[col].sum())
    if op == "mean":
        return float(d[col].mean())
    if op == "sd":
        return float(d[col].std(ddof=1))
    if op == "count":
        return float(len(d))
    if op == "max_abs":
        return float(d[col].abs().max())
    if op == "max_abs_q_le_param":  # FSB: all rows of one qbar with q <= qbar
        return float(d[d.q <= d.param][col].abs().max())
    if op in ("frac_removed", "diff", "ratio"):
        a = _one(src, filt, col)
        b = _one(row["source_csv2"], row["filter2"], col)
        return {"frac_removed": 1 - a / b, "diff": a - b, "ratio": a / b}[op]
    if op == "interp_loss":
        return interp_log(d, extra["q"], extra["budget"])
    if op in ("crossing5_mean", "crossing5_sd"):
        v = crossing5_per_draw(extra["qbar"], extra.get("attacker", "est"))
        assert all(x is not None for x in v), "a draw never reaches 5 points"
        return float(np.mean(v)) if op == "crossing5_mean" else float(np.std(v, ddof=1))
    raise ValueError(op)
