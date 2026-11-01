# HPB vs FSB robustness simulator

Simulator for the base paper's hash-prefix (HPB) and frequency-smoothing (FSB) bucketization (Li et al., CCS 2019, arXiv 1905.13737)
under estimate mismatch. Plan: `docs/PLAN.md`. Every phase ends in a report of numbers and method statements only (no paper text):
`results/REPORT.md`, `REPORT_1b.md`, `REPORT_1c.md`, `REPORT_1d.md`, `REPORT_1e.md`. Deviations from the paper / plan: `results/DISCREPANCIES.md`;
open questions: `results/QUESTIONS.md`.

## Setup

    make venv                # uv venv + pinned requirements (requirements.txt, Python 3.12) + editable install
    make fetch               # RockYou and phpbb withcount files from SecLists Passwords/Leaked-Databases -> data/ (git-ignored)
    make fetch-xato          # Phase 1c+ M2 banned list: SecLists Passwords/Common-Credentials/xato-net-10-million-passwords-1000.txt -> data/xato/
                             # (first 370 lines are used; the brief's 10-million-password-list-top-1000.txt is not in SecLists, see DISCREPANCIES D14)
    make data                # results/data_report.md

Corpora live in `data/` and `cache/` (cleaned files, hashes, estimates) and are git-ignored; never commit them.
Python always runs as `.venv/bin/python -I` (isolated: ignores the cwd and `PYTHONPATH`).

## Tests

    make test                # 28 tests; corpus-dependent tests SKIP (not error) when the corpora are absent

The corpus-dependent tests use the `corpora` fixture (`tests/conftest.py`, `data.corpora_available()`). `C3SIM_DATA` / `C3SIM_CACHE` point the code at other directories,
which is how `tests/test_phase1e.py` checks the skip behaviour: with both pointing at empty directories the other test files give 14 passed, 9 skipped, 0 errors.

## Phases, run order and reports

Run everything with `make all`, or phase by phase, **in this order** (later phases read earlier CSVs; the `*-fresh` runs are done once and are guarded against reruns):

| phase | what | targets (in order) | report |
|---|---|---|---|
| 1 | simulator, E1 (matched), E2 (M1 / M2 / M3), E3 (conservative variants), figures; t = 100,000 | `phase1`: `e1 worked e2 e3 figs report` | `results/REPORT.md` |
| 1b | t = 1e6 sensitivity, M1b, calibration fix (dev, then one fresh run) | `phase1b`: `e1b-basics e1b-m1b e1b-fix-dev e1b-fix-fresh report1b` | `REPORT_1b.md` |
| 1c | t = 1e6 primary: E2-type rows, M3 sweep, t sweep, E3, Xato list, calibration rerun (exploratory) | `phase1c`: `e1c-e2 e1c-tsweep e1c-e3 e1c-fix-dev e1c-fix-fresh report1c` | `REPORT_1c.md` |
| 1d | candidate cap, 5 noise draws, estimator error sigma_hat, M2 ablation, success ratios | `phase1d`: `e1d-cap e1d-noise e1d-esterror e1d-m2 report1d` | `REPORT_1d.md` |
| 1e | emp attacker = all of S~ (13.1M candidates): headline, t sweep to 10M, est convergence, fixes, cost | `phase1e`: `e1e-cost` (run alone, first) `e1e-headline e1e-estconv e1e-fix e1e-tsweep e1e-tsweep-10m report1e` | `REPORT_1e.md` |

Full order: `make venv fetch fetch-xato data test phase1 phase1b phase1c phase1d phase1e`. Quick runs: add `--fast` to any `experiments.e*` script (2,000 targets x 3 repeats).
`make e1e-cost` must run alone (it measures peak memory per process); the other targets can overlap if memory allows (about 4 GB each).

## Two attackers

`est`: guesses by the public estimate p^ (the base paper's attacker), candidate list = top 2M of S~ by p^ (it converges at 2M, REPORT_1e section 3).
`emp`: guesses by leak counts. Its candidate list matters: from Phase 1e the headline emp attacker holds **all of S~** (13,125,513 candidates, `World(n_cand=None)`);
2M-list emp numbers (Phases 1-1d) are lower bounds. Every results CSV has an `attacker` column (`est` / `emp`).

## Timings (10-core Apple laptop, 16 GB, 5,000 targets x 5 repeats; wall clock)

Times for Phases 1b-1d come from runs that overlapped several jobs, so they are upper bounds. A full sequential `make all` is roughly 4 to 5 hours, dominated by the E3 runs.

| script | time |
|---|---|
| `e1` (grid + candidate convergence) / `e2` | 2 min 46 s / 2 min 51 s |
| `e3` (Phase 1, dev + fresh, t = 1e5) | 40 min 45 s |
| `e1b_basics`, `e1b_m1b` | about 9 min, about 1 min |
| `e1b_fix` dev / fresh | 10 min 50 s / 14 min 11 s |
| `e1c_e2` / `e1c_tsweep` | 13 min 38 s / 1 min 28 s |
| `e1c_e3` (dev + fresh, 5 conditions) | 56 min 33 s |
| `e1c_fix` dev / fresh | 20 min 56 s / 28 min 49 s |
| `e1d_cap` / `e1d_noise` / `e1d_m2` / `e1d_esterror` | 4 min 36 s / 24 min 17 s / 4 min 5 s / 57 s |
| `e1e_cost` (4 cold probes) | under 1 min total (emp all-S~: 14 s, 3.6 GB peak) |
| `e1e_headline` / `e1e_estconv` | 2 min 28 s / 2 min 21 s |
| `e1e_tsweep` (t = 100k..3M) / t = 10M (own process) | 1 min 59 s / 33 s (4.6 GB peak) |
| `e1e_fix` | 5 min 46 s |
| tests | about 20 s |

## Layout

`c3sim/` (data, estimators, bucketizers, attacker, calibration, esterror), `experiments/` (e1..e3, e1b_* .. e1e_*, common harness, worked_examples, figs, report*), `tests/`,
`results/` (CSVs, check outputs, reports, DISCREPANCIES.md, QUESTIONS.md), `figs/`. Every CSV row carries a `cfg_hash` and the seeds. Added trailing columns:
`attacker` (D9), `t` and `cand_per_bucket` (Phase 1b+).
