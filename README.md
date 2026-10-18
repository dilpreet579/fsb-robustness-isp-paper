# HPB vs FSB robustness simulator (Phase 1)

Simulator for the base paper's hash-prefix (HPB) and frequency-smoothing (FSB) bucketization (Li et al., CCS 2019, arXiv 1905.13737)
under estimate mismatch. Plan: `docs/PLAN.md`. Results: `results/REPORT.md` (numbers and checks only, no paper text).

    make all        # fetch corpora from SecLists, tests, E1-E3, figures, report (about 30 min on a 10-core laptop)
    make test       # pytest: T1 data, T2 estimators, T3 bucketizers, T4 attacker
    make e1 e2 e3   # individual experiments (full size: 5,000 targets x 5 repeats)
    .venv/bin/python -I -m experiments.e1 --fast   # quick run: 2,000 targets x 3 repeats (also e2, e3)

Layout: `c3sim/` (data, estimators, bucketizers, attacker), `experiments/` (e1-e3, worked_examples, figs, report), `tests/`,
`results/` (CSVs, check outputs, REPORT.md, DISCREPANCIES.md, QUESTIONS.md), `figs/`. Corpora live in `data/` and `cache/` and are
git-ignored; never commit them. Dependencies are pinned in `requirements.txt` (Python 3.12).
Every CSV row carries a `cfg_hash` and the seeds; the extra trailing column `attacker` is explained in `results/DISCREPANCIES.md` D9.
