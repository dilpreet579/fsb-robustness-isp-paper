"""Phase 1e helpers: per-run wall time and memory (current and peak resident set size of this process)."""
import os
import resource
import subprocess
import sys
import time

import pandas as pd


def peak_rss_gb():
    """Peak resident set size of this process so far (it never decreases within a process)."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 2 ** 30 if sys.platform == "darwin" else r / 2 ** 20  # macOS reports bytes, Linux KiB


def cur_rss_gb():
    try:
        return int(subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())], capture_output=True, text=True).stdout.strip()) / 2 ** 20
    except Exception:  # pragma: no cover
        return float("nan")


class RunLog:
    """timed(label, fn) runs fn(), records wall seconds and memory after it; .rows() gives the log."""

    def __init__(self, **ctx):
        self.ctx, self.log = ctx, []

    def timed(self, label, fn):
        t0 = time.perf_counter()
        out = fn()
        dt = time.perf_counter() - t0
        self.log.append(dict(**self.ctx, label=label, seconds=round(dt, 1), rss_after_gb=round(cur_rss_gb(), 2), peak_rss_so_far_gb=round(peak_rss_gb(), 2)))
        return out

    def save(self, path):
        pd.DataFrame(self.log).to_csv(path, index=False)
