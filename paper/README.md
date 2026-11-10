# Paper assets

Figures, LaTeX tables, a head-storage estimate and a checked number map for the paper. **No new experiments**: everything is computed from the existing `results/*.csv`
(the head-storage estimate also reads the corpora). Nothing in `results/` is written to by these scripts.

## Regenerate

    make paper-assets          # runs the six steps below in order, ending with the number check

| step | command | needs |
|---|---|---|
| 1 head storage estimate | `.venv/bin/python -I -m experiments.paper_head_cost` | corpora (`make fetch`), about 25 s |
| 2 figures | `.venv/bin/python -I -m experiments.paper_figs` | `results/*.csv` |
| 3 tables | `.venv/bin/python -I -m experiments.paper_tables` | `results/*.csv`, `paper/head_cost.csv` (step 1) |
| 4 number map | `.venv/bin/python -I -m experiments.paper_numbers` | `results/*.csv` |
| 5 captions | `.venv/bin/python -I -m experiments.paper_captions` | `results/*.csv` |
| 6 check | `.venv/bin/python -I paper/check_numbers.py` | `paper/numbers.csv`, `results/*.csv` (exit code 1 on any mismatch) |

Test: `.venv/bin/python -I -m pytest -q tests/test_paper_assets.py tests/test_paper_assets_skip.py`. `test_paper_assets.py` checks the number map (and that a tampered value is caught), that every figure /
table / support file exists, that tables are booktabs without vertical rules, that every figure uses fonts of at least 8 pt at its printed width, and that this README lists every produced file; it SKIPS
when the results CSVs are absent. `test_paper_assets_skip.py` verifies that skip by pointing `C3SIM_RESULTS` at an empty directory.

## Frozen framing (labels)

est = attacker weights p^ with the 2M candidate list. emp = attacker weights from leak counts with **all of S~** (13,125,513 candidates, no generated strings), the headline attacker.
t = 1,000,000 unless stated. Loss = bucket success - baseline (no-bucket) success of the same attacker, in percentage points (pp). Seed 2000, pool A_test, 5 repeats x 5,000 targets;
± is the sd over the repeats (over the 5 noise draws for the M3 crossings and Fig. 2). Tables are `tabular` bodies using `booktabs` (`\usepackage{booktabs}`), no vertical rules; the `*_note.tex`
files hold one-paragraph table notes. No LaTeX engine is installed in this repository's environment, so the tables are checked structurally (tests), not compiled.

## Files produced

### Figures (`paper/figs/`; PDF and 300-dpi PNG; `figN` = 3.3 in column width, `figN_wide` = 7 in)

| file | content | sources |
|---|---|---|
| `fig1`, `fig1_wide` (.pdf, .png) | loss vs q, M0 and M2x; FSB qbar=100 and HPB l=12, est and emp | `e1c_e2.csv`, `e1e_headline.csv` |
| `fig2`, `fig2_wide` | M3: loss at q=qbar=100 vs sigma, noise on all strings vs tail only, est and emp, with measured sigma_hat | `e1f_tailnoise.csv`, `e1f_tailnoise_emp.csv`, `e1c_e2.csv`, `e1e_headline.csv`, `e1d_esterror_summary.csv` |
| `fig3`, `fig3_wide` | loss contribution by target group (head / stored, not in head / not in S~) at q=1 and q=100, FSB vs HPB | `e1f_mech_groups.csv` |
| `fig4`, `fig4_wide` | t sweep: emp loss at q=100 vs head size t, with average bucket size; est reference | `e1e_tsweep.csv`, `e1e_tsweep_10M.csv`, `e1c_tsweep.csv`, `e1c_e2.csv` |
| `fig5`, `fig5_wide` (appendix) | fixes at equal average bucket size (base, Kneser-Ney, calibrated), emp | `e1e_fix.csv` |

### Tables (`paper/tables/`)

| file | content | sources |
|---|---|---|
| `T1_headline.tex` | headline: M0, M1b, M2x, M2L; qbar 10/100/1000; avg bucket, loss at q=qbar (FSB est, FSB emp, matched HPB emp), fraction of HPB loss removed, success ratio at q=1 | `e1c_e2.csv`, `e1d_ablation.csv` (est M2L), `e1e_headline.csv`, `e1e_ratio.csv` |
| `T2_m2_ablation.tex`, `T2_m2_ablation_note.tex` | M2 ablation: length only / blocklist only / both, est and emp | `e1d_ablation.csv`, `e1e_headline.csv` |
| `T3_tsweep_head_storage.tex`, `T3_note.tex` | t sweep with head storage (MB), emp loss at q=1,10,100 | `e1e_tsweep.csv`, `e1e_tsweep_10M.csv`, `head_cost.csv` |
| `T4_fixes.tex`, `T4_note.tex` | fixes: loss at q=100 and q=1000 at 2,000 / 6,500 / 20,000 entries per bucket | `e1e_fix.csv` |
| `T5_cost.tex`, `T5_note.tex` | attacker cost: candidates, time, peak memory | `e1e_cost.csv` |
| `T6_estimator_error.tex`, `T6_note.tex` | head / tail sigma_hat, both methods, t = 1M | `e1d_esterror_summary.csv` |
| `T7_m3_crossings.tex`, `T7_note.tex` | sigma at 5 points over 5 noise draws (est); emp crossing not defined | `e1d_noise.csv`, `e1c_e2.csv`, `e1e_headline.csv` |

### Data and checks (`paper/`)

| file | content |
|---|---|
| `head_cost.csv` | estimated size of the histogram head for t = 100k, 300k, 1M, 3M, 10M (plain text, gzip -9, float32 probabilities) and of the 3-gram table; an estimate of data size, not an implementation |
| `numbers.csv` | every number the text may quote: id, claim (C1..C5), description, value, unit, source_csv, filter, plus the recipe columns op, column, source_csv2, filter2, extra |
| `numbers.md` | the same numbers as a readable table grouped by claim |
| `captions.md` | factual caption drafts for Figures 1-5, with numbers computed from the CSVs (includes the note that tail-only noise leaves emp at the clean 10.92) |
| `check_numbers.py` | recomputes every row of `numbers.csv` from its source CSV and exits 1 on any mismatch |
| `README.md` | this file |

### Code

`experiments/paper_common.py` (paths, loaders), `paper_figs.py`, `paper_tables.py`, `paper_head_cost.py`, `paper_numlib.py` (the recipes used by both the generator and the checker),
`paper_numbers.py`, `paper_captions.py`; `tests/test_paper_assets.py`, `tests/test_paper_assets_skip.py`.

## Claims covered by `numbers.csv`

C1 reproduction (est: HPB loss at q=1 and q=qbar at matched sizes; FSB max |loss| for q <= qbar) | C2 noise tolerance (sigma crossings at 5 points, head and tail sigma_hat) |
C3 count-aware attacker (emp loss at q=qbar, fraction of HPB loss removed at q=qbar and q=1, M2x success ratios) | C4 mechanism (loss contribution by group, tail guess rate, leak-count and gamma
of newly gained targets, t sweep, fixes at equal size, tail-only vs full noise) | C5 attacker cost (time and memory).

## Things to know before using these assets

See `results/DISCREPANCIES.md` D28-D33 and `results/QUESTIONS.md` Q31-Q36 (sources that are missing or ambiguous: no emp all-of-S~ run for the blocklist-only ablation; est reference
in Fig. 4 only exists for M0 at t <= 3M; est M2L comes from the ablation file; the "5-point reference" is drawn in both panels; the M2x success ratio at q=1 rests on a baseline of 0.12%).
