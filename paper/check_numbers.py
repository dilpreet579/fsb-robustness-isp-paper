"""Recompute every row of paper/numbers.csv from its source CSV (results/*.csv) and fail on any mismatch.
    .venv/bin/python -I paper/check_numbers.py
Exit code 0 = every stored value equals the recomputed value (absolute tolerance 1e-9, relative 1e-9; nan == nan); 1 = at least one mismatch, missing source or malformed row."""
import math
import os
import sys

import pandas as pd

from experiments.paper_common import PAPER, RES
from experiments.paper_numlib import compute


def check(path=None):
    """Returns (n_rows, list of problems)."""
    path = path or os.path.join(PAPER, "numbers.csv")
    df = pd.read_csv(path)
    problems = []
    for need in ("id", "claim", "description", "value", "unit", "source_csv", "filter"):
        if need not in df.columns:
            problems.append(f"numbers.csv lacks column {need}")
    if problems:
        return len(df), problems
    if not df.id.is_unique:
        problems.append("duplicate ids: " + ", ".join(df.id[df.id.duplicated()].astype(str)))
    for r in df.to_dict("records"):
        for s in (r["source_csv"], r.get("source_csv2")):
            if isinstance(s, str) and s and not os.path.exists(os.path.join(RES, s)):
                problems.append(f"{r['id']}: missing source {s}")
        try:
            v = compute(r)
        except Exception as e:  # noqa: BLE001
            problems.append(f"{r['id']}: cannot recompute ({type(e).__name__}: {e})")
            continue
        s = float(r["value"])
        if not ((math.isnan(v) and math.isnan(s)) or math.isclose(v, s, rel_tol=1e-9, abs_tol=1e-9)):
            problems.append(f"{r['id']}: stored {s!r} != recomputed {v!r}  ({r['source_csv']} [{r['filter']}])")
    return len(df), problems


if __name__ == "__main__":
    n, problems = check()
    if problems:
        print(f"FAIL: {len(problems)} problem(s) in {n} rows")
        print("\n".join(problems[:50]))
        sys.exit(1)
    print(f"OK: all {n} numbers in paper/numbers.csv recomputed from results/*.csv and match")
