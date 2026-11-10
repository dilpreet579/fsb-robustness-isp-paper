"""The paper-asset tests must SKIP (not fail or error) when the results/ CSVs are absent."""
import os
import subprocess
import sys

from experiments.paper_common import ROOT


def test_paper_asset_tests_skip_when_results_are_absent(tmp_path):
    env = {**os.environ, "C3SIM_RESULTS": str(tmp_path / "no_results_here")}
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rs", "tests/test_paper_assets.py"], cwd=ROOT, env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert "skipped" in out and "passed" not in out and "failed" not in out.lower() and "error" not in out.lower(), out
