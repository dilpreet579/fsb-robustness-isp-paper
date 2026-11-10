"""Shared helpers for the paper assets (figures, tables, numbers). Reads results/*.csv only; never writes to results/.
Frozen framing (labels): est = attacker weights p^ with the 2M list; emp = attacker weights from leak counts with ALL of S~ (headline). t = 1M unless stated.
Loss = bucket success - baseline success of the same attacker, percentage points (pp)."""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.environ.get("C3SIM_RESULTS", os.path.join(ROOT, "results"))  # overridable so the skip behaviour of the tests can be checked
PAPER = os.path.join(ROOT, "paper")
FIGS = os.path.join(PAPER, "figs")
TABLES = os.path.join(PAPER, "tables")

_cache = {}


def load(name):
    """results/<name>.csv as a DataFrame (cached)."""
    if name not in _cache:
        _cache[name] = pd.read_csv(os.path.join(RES, f"{name}.csv"))
    return _cache[name]


def sel(df, **kw):
    """Rows where every column equals the given value."""
    m = pd.Series(True, index=df.index)
    for k, v in kw.items():
        m &= df[k] == v
    return df[m]


def one(df, **kw):
    r = sel(df, **kw)
    assert len(r) == 1, (kw, len(r))
    return r.iloc[0]


def sources_exist(names):
    return all(os.path.exists(os.path.join(RES, f"{n}.csv")) for n in names)
