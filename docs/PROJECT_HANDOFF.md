# Project handoff: HPB vs FSB robustness simulator and paper

Authors: Dilpreet Singh, Ishita Gupta, Madhav Raj (National Institute of Technology Delhi).

## 1. What this project is

A simulation study of frequency-smoothing bucketization (FSB) against size-matched hash-prefix bucketization (HPB) for compromised-credential checking. The base paper is Li et al., "Protocols for Checking Compromised Credentials" (ACM CCS 2019, arXiv 1905.13737; a copy is in `docs/`). The question: FSB's guarantee holds relative to the server's own estimate of the password distribution, so how much does it degrade when the estimate is wrong and the attacker holds the leak counts?

The deliverables are (1) the simulator and verified experimental results, and (2) the paper `paper/main.pdf` (title: "Beyond k-Anonymity in Password Breach Checking: How Robust Is Frequency-Smoothing Bucketization?").

Only public leaked-password corpora are used (RockYou and phpbb via SecLists, plus the Xato top-1000 list for the policy blocklist), in aggregate; nothing is uploaded and no live service or account is touched.

## 2. Repository map

| Path | Content |
|---|---|
| `docs/PLAN.md` (copy in `CLAUDE.md`) | the plan the work followed: definitions, conditions, tasks and acceptance checks |
| `docs/1905.13737v3.pdf` | base paper |
| `docs/paper.md` | local markdown source of the paper text (kept untracked on purpose; the LaTeX in `paper/` is the maintained version) |
| `c3sim/` | library: `data`, `estimators`, `bucketizers`, `attacker`, `calibration`, `esterror` |
| `experiments/` | experiment drivers (`e1`, `e2`, `e3`, then `e1b_*` to `e1g_*`), the shared harness `common.py`, report writers `report*.py`, paper-asset scripts `paper_*.py` |
| `tests/` | pytest suite (39 tests; corpus-dependent tests skip when the data is absent) |
| `results/` | result CSVs, `REPORT.md` and `REPORT_1b` to `REPORT_1g`, `REPORT_paper.md`, `DISCREPANCIES.md` (D1 to D35), `QUESTIONS.md` (Q1 to Q39), `data_report.md`, `worked_examples.txt` |
| `figs/` | the original E1 to E3 figures |
| `paper/` | LaTeX paper: `main.tex`, `preamble.tex`, `refs.bib`; generated `figs/`, `tables/`, `numbers.csv`, `captions.md`, `head_cost.csv`; the checkers `check_numbers.py` and `check_text_numbers.py`; `main.pdf` |
| `Makefile`, `README.md` | entry points (see section 5) |

Corpora and caches live in `data/` and `cache/` and are git-ignored. Never commit them.

## 3. How the code was written

The plan in `docs/PLAN.md` was the specification. Work proceeded in phases, each ending in a report that states numbers and method only:

1. **Phase 1 (T1 to T8 of the plan).** Data loading and seeded binomial account splits; estimators (histogram head plus smoothed character 3-gram tail); bucketizers (HPB, FSB with a difference-array bucket-size count and a sorted-class lookup); the attacker and the Guess / BucketGuess games; then E1 (matched), E2 (mismatch conditions M1 to M3) and E3 (conservative fixes), with the gate statistic and worked examples.
2. **Phases 1b to 1f.** Follow-ups on the same simulator: cross-corpus and fix variants (1b), larger sweeps and the t sweep (1c), noise calibration, estimator-error measurement and the policy ablations (1d), the count-aware attacker over all stored passwords and the cost measurements (1e), and the mechanism analysis by target group and tail-only noise (1f). **Phase 1g** tests a floor on gamma (every string stored in at least g buckets; class `FSBFloor`, `experiments/e1g_floor.py`, `e1g_robust.py`, `report1g.py`, `make phase1g`) against three attackers: emp (raw counts), gt (Good-Turing adjusted counts) and est; tuned on A_dev, reported once on A_fresh (`results/REPORT_1g.md`, D35, Q39).
3. **Paper assets.** Scripts that turn result CSVs into the five figures, the LaTeX tables, a head-storage estimate, a caption draft file and a checked number map (`paper/numbers.csv`, 364 numbers, claims C1 to C5).

Working rules used throughout:
- Every acceptance check from the plan has a test or a printed check; a failing check was investigated before moving on.
- Seeds are fixed; every result row carries a config hash; runs are reported even when the result was unwelcome.
- Anything that deviated from the plan or the base paper is logged in `results/DISCREPANCIES.md`; anything ambiguous, with the reading taken, is logged in `results/QUESTIONS.md`.
- Tuning used a development target pool; headline numbers come from a fresh pool.
- The simulator, the experiment drivers and drafts of the paper were produced with generative AI assistance, and the authors reviewed the code and results and take responsibility for the content (the same statement is in the paper).

## 4. How the paper was written

1. The experiments and reports came first; the paper text was drafted afterwards from the verified results (`docs/paper.md`), with every number taken from `paper/numbers.csv`, the figures from `paper/figs/` and the tables from `paper/tables/`.
2. The text was converted to LaTeX (`paper/main.tex`, one preamble file for the layout, `refs.bib` built from the reference list). Figures 1 to 4 are in the body; Table 1 is `T1_headline.tex`; Appendix A is the per-draw noise table, Appendix B the head-storage table and Appendix C Figure 5 (the fixes).
3. A number audit (`paper/check_text_numbers.py`) extracts every numeric token from `main.tex` and matches it to the number map, the head-storage file, the data report, listed derived claims (for example exp(5.86) is about 350) and stated setup constants. Tables are checked by regenerating them and comparing bytes. The authors read the audit result and the md-versus-CSV points listed in `results/REPORT_paper.md` and corrected the text where the data disagreed.
4. The text was later extended with comparisons to Li et al. (their estimator, 436-million-password leak, 8.9 MB estimate and policy experiment, each checked against the base paper in `docs/`), a short note on HIBP's padded responses and Microsoft Password Monitor, and the M2x case at qbar = 1000, where FSB is worse than size-matched HPB at q = 1 (8.58 pp against 6.06 pp). Each edit is listed in `results/REPORT_paper.md`.
5. The layout target is 7.5 to 7.75 pages for text plus references, with the appendices on a further page. The current PDF is 9 pages: the text and references run to about 7.6 pages (page 8 is about 64% filled), and Appendices A to C are on page 9.

## 5. How to reproduce

All Python runs as `.venv/bin/python -I`.

    make venv            # pinned environment (Python 3.12)
    make fetch           # RockYou and phpbb withcount files from SecLists into data/
    make fetch-xato      # Xato top-1000 list (first 370 lines are the blocklist)
    make data            # results/data_report.md
    make test            # 39 tests
    make phase1          # E1, E2, E3, worked examples, figures, report (plan phase 1)
    make phase1b phase1c phase1d phase1e   # follow-up phases (targets inside the Makefile)
    make paper-assets    # figures, tables, number map, captions, number check
    make paper-pdf       # paper/main.pdf (needs tectonic; it runs BibTeX itself)
    .venv/bin/python -I paper/check_numbers.py        # recompute the number map from the CSVs
    .venv/bin/python -I paper/check_text_numbers.py   # audit of the numbers printed in main.tex

Fixed settings: seed 2000, pool A_test, 5 repeats of 5,000 targets, t = 1,000,000 histogram head, 2^24 buckets, N = 13,125,513 stored passwords. The attacker called est ranks guesses by the server's estimate over the 2M most probable passwords; emp ranks by leak counts over all stored passwords and is the headline attacker. Environment variables `C3SIM_DATA`, `C3SIM_CACHE` and `C3SIM_RESULTS` redirect the data, cache and results directories.

## 6. Headline results (details in `results/REPORT_paper.md` and the CSVs)

- C1: against the estimate-based attacker FSB's loss at q = qbar is 0.0 pp for qbar = 10, 100, 1000, against 37.0, 41.1, 40.2 pp for size-matched HPB.
- C2: the loss reaches 5 pp at noise sigma = 0.87, 0.69, 0.66; the measured head error is 0.31, so the margin is about 2 to 1.
- C3: the count-aware attacker gains 10.5, 10.9, 10.9 pp, still about 73% below HPB; under a length-and-blocklist policy FSB removes under 1% of HPB's loss at q = 1 for qbar = 100, and at qbar = 1000 it is worse than size-matched HPB (it removes -41.7% of HPB's loss).
- C4: the residual loss sits on rare stored passwords outside the histogram head; a 10M-entry head cuts it to 2.3 pp.
- C5: a cold run of the count-aware attacker takes 14 s and 3.6 GB.
- C6 (fresh pool, worst case over emp, gt, est, at q = qbar): for qbar = 100 a floor of 2,048 cuts the loss from 10.68 to 0.08 pp on M0 and from 14.54 to 2.16 pp on M2x at 1.56 times the average bucket; it does not help for q > qbar, and at qbar = 1000 it is not enough (2.72 pp M0 at 1.12 times).

## 7. Open items and known limits

- Two claims in Related Work (1.5% from Thomas et al.; 16% from Pal et al. 2019) are not checked against the cited papers; the audit lists them as unmatched, together with the 436 million of Li et al. (confirmed in the base paper). The sentence "We are not aware of an earlier study ..." needs a literature check by the authors.
- The Microsoft Password Monitor reference is undated ("n.d.") because the year could not be confirmed, and the statements about HIBP's padded responses (Cloudflare blog, 4 March 2020) and Password Monitor (OPRF and homomorphic encryption) are not checked against the pages (`results/QUESTIONS.md` Q38).
- The blocklist-only policy ablation (M2B) has no run over all stored passwords; its emp numbers come from the 2M-candidate file (DISCREPANCIES D28).
- Figure 4 shows a single est point for M2x at t = 1M because that is the only measurement; the est reference is not a flat zero everywhere (D30).
- The calibration variant is exploratory (tuned on a held-out split).
- The study uses one leak and one split; the standard deviations come from re-sampling targets, not from re-splitting the leak.
- The floor (C6): one fresh pool, three stored-password attackers, a flawed pre-registered selection rule (D35), no M1b / M3 run, not tested at the scale of Li et al., server storage and lookup cost not measured (Q39). Text plus references now fill 8 pages (target was 7.5 to 7.75); Appendix D is on its own page.
- `docs/paper.md` is an untracked local copy; it does not include the latest LaTeX edits (the Li et al. comparisons, the references added for Ali and Microsoft, and the M2x qbar = 1000 result). The LaTeX is the maintained source.
- Tooling note: the PDF is built with `tectonic` (no pdflatex was installed on the build machine).
