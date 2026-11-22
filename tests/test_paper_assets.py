"""Paper assets: the number check passes, every figure/table file exists and is well formed. Skips when the results/ CSVs are absent. Generate first: make paper-assets."""
import importlib.util
import os

import pandas as pd
import pytest

from experiments.paper_common import FIGS, PAPER, RES, TABLES, sources_exist

SOURCES = ["e1c_e2", "e1c_tsweep", "e1d_ablation", "e1d_esterror_summary", "e1d_noise", "e1e_cost", "e1e_fix", "e1e_headline", "e1e_ratio", "e1e_tsweep", "e1e_tsweep_10M",
           "e1f_mech_dist", "e1f_mech_groups", "e1f_mech_quantiles", "e1f_tailnoise", "e1f_tailnoise_emp", "e1g_floor_fresh", "e1g_robust_fresh", "e1h_splits"]
FIGURES = [f"fig{i}{w}.{e}" for i in range(1, 6) for w in ("", "_wide") for e in ("pdf", "png")]
TABLES_TEX = ["T1_headline", "T2_m2_ablation", "T3_tsweep_head_storage", "T4_fixes", "T5_cost", "T6_estimator_error", "T7_m3_crossings", "T8_floor", "T9_env", "T10_splits", "T11_fist_headline", "T12_fist_floor"]
NOTES = ["T2_m2_ablation_note", "T3_note", "T4_note", "T5_note", "T6_note", "T7_note", "T8_note", "T10_note"]
OTHER = ["head_cost.csv", "numbers.csv", "numbers.md", "captions.md", "check_numbers.py", "README.md"]

pytestmark = pytest.mark.skipif(not sources_exist(SOURCES), reason="results/*.csv not available")


def _checker():
    spec = importlib.util.spec_from_file_location("check_numbers", os.path.join(PAPER, "check_numbers.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_number_check_passes_and_covers_all_claims():
    n, problems = _checker().check()
    assert not problems, problems[:10]
    df = pd.read_csv(os.path.join(PAPER, "numbers.csv"))
    assert n == len(df) > 300
    assert set(df.claim) == {"C1", "C2", "C3", "C4", "C5", "C6", "C7"}
    assert {"id", "claim", "description", "value", "unit", "source_csv", "filter"} <= set(df.columns)
    assert df.value.notna().all() or df.id[df.value.isna()].str.contains("fix").all()  # only an out-of-range interpolation may be nan


def test_number_check_catches_a_tampered_value(tmp_path):
    df = pd.read_csv(os.path.join(PAPER, "numbers.csv"))
    df.loc[0, "value"] += 1.0
    p = tmp_path / "numbers.csv"
    df.to_csv(p, index=False)
    _, problems = _checker().check(str(p))
    assert problems and df.id[0] in problems[0]


def test_every_figure_table_and_support_file_exists():
    ok = lambda p: os.path.exists(p) and os.path.getsize(p) > 0
    missing = [f"figs/{f}" for f in FIGURES if not ok(os.path.join(FIGS, f))]
    missing += [f"tables/{t}.tex" for t in TABLES_TEX + NOTES if not ok(os.path.join(TABLES, f"{t}.tex"))]
    missing += [f for f in OTHER if not ok(os.path.join(PAPER, f))]
    assert not missing, f"missing (run `make paper-assets`): {missing}"


def test_tables_are_booktabs_without_vertical_rules():
    for t in TABLES_TEX:
        s = open(os.path.join(TABLES, f"{t}.tex")).read()
        spec = s.split("\\begin{tabular}{", 1)[1].split("}", 1)[0]
        assert "|" not in spec and "\\hline" not in s, t
        assert s.count("\\toprule") == 1 and s.count("\\bottomrule") == 1 and "\\midrule" in s, t
        assert s.count("\\begin{tabular}") == s.count("\\end{tabular}") == 1, t
        commands = ("\\toprule", "\\midrule", "\\bottomrule", "\\cmidrule", "\\begin", "\\end")
        rows = [ln for ln in s.splitlines() if ln.strip() and not ln.startswith(commands)]  # header and data rows
        assert rows and all(ln.rstrip().endswith("\\\\") for ln in rows), (t, [ln for ln in rows if not ln.rstrip().endswith("\\\\")])


def test_figures_use_fonts_of_at_least_8pt_at_the_printed_width(monkeypatch):
    """Rebuild every figure without saving: all visible text >= 8 pt, widths exactly 3.3 in (column) and 7.0 in (wide), no title inside a figure."""
    import matplotlib.text as mt

    from experiments import paper_figs as pf

    seen = []

    def check(fig, name, wide):
        assert abs(fig.get_size_inches()[0] - (7.0 if wide else 3.3)) < 1e-6, (name, wide)
        assert not fig._suptitle and all(not ax.get_title() for ax in fig.axes), name
        small = [(t.get_text(), t.get_fontsize()) for t in fig.findobj(mt.Text) if t.get_visible() and t.get_text().strip() and t.get_fontsize() < 8 - 1e-9]
        assert not small, (name, wide, small)
        seen.append((name, wide))

    monkeypatch.setattr(pf, "save", check)
    for f in (pf.fig1, pf.fig2, pf.fig3, pf.fig4, pf.fig5):
        for wide in (False, True):
            f(wide)
    assert len(seen) == 10


def test_readme_lists_every_produced_file():
    txt = open(os.path.join(PAPER, "README.md")).read()
    names = FIGURES + [f"{t}.tex" for t in TABLES_TEX + NOTES] + OTHER
    # figures are listed by stem (fig1 ... fig5, with _wide, .pdf/.png)
    absent = [n for n in names if n.split(".")[0].replace("_wide", "") not in txt and n not in txt]
    assert not absent, absent
