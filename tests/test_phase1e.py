"""Phase 1e: the all-of-S~ attacker option, the timing helper, the ratio helper, and corpus-dependent tests skipping when data is absent."""
import os
import subprocess
import sys
import time

import numpy as np

from c3sim import attacker as atk
from c3sim import data
from experiments import common as C
from experiments import e1d_m2, e1e_common

ROOT = data.ROOT


def test_attacker_with_all_candidates_keeps_every_password_in_weight_order():
    pw = np.array([b"aa", b"bb", b"cc", b"dd", b"ee"], dtype="S30")
    w = np.array([5.0, 5.0, 3.0, 1.0, 1.0])
    for cap in (5, 10**9):  # cap == len and cap far above len are the same list: everything
        att = atk.Attacker(pw, w, n_cand=cap)
        assert att.pw.tolist() == pw.tolist() and (att.cnt == w).all()
    assert len(atk.Attacker(pw, w, n_cand=2).pw) == 2  # a smaller cap still truncates, best first


def test_world_n_cand_none_means_all_of_S(corpora):
    w = C.World(t=100_000, n_cand=None)
    assert w.n_cand == w.N == 13_125_513
    att, _, _ = w.condition("M0", model="emp")
    assert len(att.pw) == w.N and (np.diff(att.cnt) <= 0).all()


def test_runlog_records_time_and_memory():
    rl = e1e_common.RunLog(t=1)
    out = rl.timed("sleep", lambda: (time.sleep(0.05), 42)[1])
    assert out == 42
    r = rl.log[0]
    assert r["seconds"] >= 0.0 and r["peak_rss_so_far_gb"] > 0 and r["rss_after_gb"] > 0 and r["t"] == 1 and r["label"] == "sleep"


def test_ratio_rows_ratio_and_undefined_baseline():
    base = dict(condition="M0", attacker="emp", scheme="fsb", variant="fsb_base", param=100, avg_bucket=1.0, std_over_repeats=0.0)
    rows = [dict(base, q=1, baseline_success=1.0, bucket_success=3.0, loss=2.0, bucket_by_repeat=[3.0, 3.0], baseline_by_repeat=[1.0, 1.0]),
            dict(base, q=100, baseline_success=0.0, bucket_success=1.0, loss=1.0, bucket_by_repeat=[1.0, 1.0], baseline_by_repeat=[0.0, 0.0]),
            dict(base, q=10, baseline_success=1.0, bucket_success=1.0, loss=0.0, bucket_by_repeat=[1.0], baseline_by_repeat=[1.0])]
    out = e1d_m2.ratio_rows(rows)
    assert [r["q"] for r in out] == [1, 100]  # only q = 1 and q = qbar
    assert out[0]["ratio"] == 3.0 and out[0]["ratio_sd"] == 0.0
    assert out[1]["ratio"] is None and out[1]["ratio_sd"] is None  # baseline 0: undefined, not inf


def test_corpus_tests_skip_not_error_when_data_absent(tmp_path):
    """With data/ and cache/ pointing at empty (writable) directories, every other test file must still pass or SKIP: nothing errors or fails."""
    env = {**os.environ, "C3SIM_DATA": str(tmp_path / "data"), "C3SIM_CACHE": str(tmp_path / "cache")}
    others = sorted(f"tests/{f}" for f in os.listdir(os.path.join(ROOT, "tests")) if f.startswith("test_") and f != "test_phase1e.py")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rs", *others], cwd=ROOT, env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert "skipped" in out and "error" not in out.lower() and "failed" not in out.lower(), out
