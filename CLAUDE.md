# Plan: HPB vs FSB robustness simulator (for Claude Code)

Project: "Beyond k-Anonymity in Password Breach Checking: Making Frequency-Smoothing Bucketization Robust" (working title).
This file is the whole plan. Put it in `docs/` and copy it to `CLAUDE.md` at the repo root.

## 0. Read this first

- You are building a simulator and producing **verified experimental results**. You are **not** writing the paper. When `results/REPORT.md` exists, stop and say so. Paper writing starts only after a human has verified the results.
- If an acceptance check fails and you cannot fix it within about an hour, write `BLOCKERS.md` (what failed, what you tried, your best guess) and stop.
- Put the base paper (Li et al., "Protocols for Checking Compromised Credentials", ACM CCS 2019, arXiv 1905.13737) in `docs/`. Read its Sections 3 to 6 and Appendices B and C before coding. If this plan disagrees with the paper, follow the paper and list the difference in `results/DISCREPANCIES.md`.

## 1. Research question

The base paper's frequency-smoothing bucketization (FSB) has near-zero attacker advantage only when the server's password-distribution estimate is accurate. Question: how much does FSB degrade when the estimate is wrong, and does a conservative replication rule fix it at the same bucket size?

Base-paper reference numbers (their scale is 436M passwords; ours is smaller, so reproduce the **shape**, not the numbers). Uncompromised users, q = 1000: HPB with l=16 (about 6.6k entries per bucket) reaches 59.7% attacker success against a 5.8% baseline; FSB with qbar=100 (about 6.3k per bucket) reaches 8.0%. Under an unknown password policy, FSB qbar=100 reaches 13.2% against a 3.4% baseline.

## 2. Definitions (follow exactly)

- S~ = the leaked unique passwords (the server's database). N = |S~|. |B| = smallest power of two >= N.
- f(w) = first log2|B| bits of salted SHA-256(w), as an integer.
- Estimate p^(w), defined for **any** string w (the client and the attacker both evaluate it):
  - if w is among the top t passwords of S~ by count (t = 100000, provisional): the histogram probability c(w) / total;
  - otherwise: p_n(w) * (1 - sum of histogram mass over the top t) / (1 - sum of p_n mass over the top t), where p_n is a smoothed character 3-gram model trained on the leak (weighted by counts; state your smoothing choice in the report).
- FSB: gamma(w) = min(|B|, ceil(|B| * p^(w) / p^(w_qbar))), where w_qbar is the qbar-th most probable password under p^. The password sits in buckets f(w), f(w)+1, ..., f(w)+gamma(w)-1 (mod |B|). The top qbar passwords therefore sit in every bucket. The client picks one bucket uniformly at random from that range. Targets outside S~ still get gamma from p^.
- HPB: bucket = first l bits of salted SHA-256(w); one bucket per password.
- Bucket sizes: for FSB, count coverage per bucket with a difference array over the circular ranges (exact, no interval trees); for HPB, bincount the prefixes. Report average and maximum over buckets, measured on S~ only. Average bucket size is the bandwidth proxy.
- Attacker, given bucket b: it knows S~, the scheme, and the public estimate, so it can evaluate beta(c) for **any** candidate c. Candidate list L = the top 2,000,000 unique passwords by p_att (or all, if fewer). Keep only candidates c with b in beta(c), score each by p_att(c) / |beta(c)|, break ties by p_att then lexicographically, and guess the top q. Check that success is unchanged between 1M and 2M candidates.
- Baseline attacker (no bucket): the top q of L by p_att.
- Success = fraction of sampled targets whose password is in the guess list. Loss = success with bucket minus baseline success. Report q in {1, 10, 100, 1000} from one top-1000 list.

## 3. Data

- Use SecLists (github.com/danielmiessler/SecLists), `Passwords/`, the **withcount** folder (plaintext passwords with occurrence counts). If you cannot reach it, ask the human; do not substitute other sources silently.
- Corpus A = `Passwords/Leaked-Databases/rockyou-withcount.txt.tar.gz` (extracts to `rockyou-withcount.txt`; checked by the human on 2026-11-14: 14,344,391 unique, 32,603,388 total, lines are `count password`).
- Corpus B = `Passwords/Leaked-Databases/phpbb-withcount.txt` (checked: 184,388 unique, 255,420 total; a 2009 forum breach, a different kind of site from RockYou). Do NOT use `honeynet-withcount.txt` even though it has more unique entries (226,927): it is a honeypot log of attackers' guesses (top entries are "server", "test1", "test2"), not user-chosen passwords. `muslimMatch` (95,072 unique) is under the 100k floor and `myspace`, `faithwriters`, `singles.org`, `hak5`, `bible`, `elitehacker`, `porn-unknown` are all smaller. These were the only withcount files in the repo at the time of checking (all in `Leaked-Databases/`, plus one PIN-code csv that is irrelevant). If a file is missing or the format differs, stop and ask; do not substitute silently.
- phpbb is small and mostly singletons (total/unique is about 1.4). Consequences to handle: the M1 target pool is about 128k accounts after the 50/50 split, which is enough for 5,000 targets; do not treat its tail as informative beyond the top few thousand passwords; report this limitation in `results/data_report.md` and `REPORT.md`.
- Record the final choice, unique counts, total mass, and top 10 per corpus in `results/data_report.md`.
- **Do not use** the RockYou2021 or RockYou2024 compilations.
- Preprocess: printable ASCII only, length 1 to 30, case kept, duplicate counts aggregated.
- Splits are by account, seeded. For each password with count c, draw c_train ~ Binomial(c, p) and c_test = c - c_train. Corpus A: p = 0.9, so A_train is the leak S~ and A_test is the matched target pool. Corpus B: p = 0.5, so B_attack trains the attacker and B_target is the cross-corpus target pool. Targets are then sampled by account (frequency-weighted).
- Public research corpora only; use in aggregate; no per-account analysis; never commit the corpora to git (add them to `.gitignore`).

## 4. Conditions

| ID | Targets | Server estimate | Attacker p_att |
|----|---------|-----------------|----------------|
| M0 matched | A_test | from A_train | empirical A_train |
| M1 cross-corpus | B_target | from A_train | empirical B_attack |
| M2 policy | A_test restricted to length >= 8 and not in a fixed banned list of about 370 most common passwords (name the list) | from A_train, unfiltered | A_train with the same policy, renormalised |
| M3 noise | A_test | p^ multiplied by exp(sigma * z_w), z_w ~ N(0,1) seeded by the password; sigma in {0.5, 1.0, 1.5}; w_qbar re-derived from the noisy estimate | empirical A_train |

## 5. Repo layout

```
docs/                 this file, base paper, plan export
c3sim/data.py         loading, cleaning, binomial splits
c3sim/estimators.py   histogram, 3-gram, combined p^, ensemble variants (E3)
c3sim/bucketizers.py  HPB, FSB, bucket-size counting, sorted-class lookup
c3sim/attacker.py     Guess and BucketGuess games
experiments/e1.py e2.py e3.py
tests/                pytest
results/              CSVs, REPORT.md (committed); corpora are not
figs/                 fig1_pareto, fig2_mismatch, fig3_fix (pdf and png)
Makefile              data, test, e1, e2, e3, figs, all
```

Performance rules: never scan all of S~ per query. Group passwords by distinct gamma, keep f-sorted arrays, answer a bucket query with numpy `searchsorted`. Vectorise; use numba or chunked numpy for the 3-gram pass over S~ and cache it to disk. Seed everything. Every result row carries a config hash. A `--fast` flag uses 2,000 targets and 3 repeats; the default is 5,000 targets and 5 repeats.

## 6. Tasks and acceptance checks

1. **T1 data and splits.** Check: same seed gives the same split; `data_report.md` written.
2. **T2 estimators.** Check: probabilities over a 10k sample of strings are finite and positive; top-1000 histogram mass matches the empirical share; p^(w_qbar) > 0 for every qbar tested.
3. **T3 bucketizers and lookup.** Check: on a 50k-password toy set the fast lookup equals a naive scan for 1,000 random buckets; average FSB bucket size equals sum(gamma) / |B|.
4. **T4 attacker and games.** Check: baseline success equals the top-q mass of the attacker's list within sampling error on a toy distribution with a known answer; print five worked examples (target, bucket, top-5 guesses and scores) to `results/worked_examples.txt` for the human to replay.
5. **T5 E1 (matched, M0).** HPB with l chosen so average bucket size spans about 200 to 100k entries; FSB with qbar in {1, 10, 100, 1000, 10000}. Check: FSB loss is at most 1 point for q <= qbar; HPB at about 7k entries per bucket loses tens of points at q=1000. If either fails, stop and investigate before E2.
6. **T6 E2 (M1, M2, M3).** FSB with qbar in {10, 100, 1000}; HPB at equal bucket size. Print the **gate statistic**: for qbar=100 at q=1000, loss under M1 minus loss under M0, and loss under M2 minus loss under M0.
7. **T7 E3 conservative fix** (run it regardless of the gate statistic; the human decides what to use). Variants: `fsb_base`; `ens_max`, where gamma uses the largest estimate among the base estimate, 5 bootstrap resamples of the leak counts, and tempered estimates p^tau with tau in {0.8, 0.6}; `smoothed`, a better-smoothed n-gram estimate. Sweep qbar per variant to trace bucket-size against loss. **Tune on a dev target pool; report only on a fresh pool.** Report the best variant and all others.
8. **T8 repro package.** `make all` regenerates every CSV and figure from raw data; README; pinned dependencies; tests for T2 to T4 pass.

## 7. Outputs

- `results/e1.csv`, `results/e2.csv`, `results/e3.csv`. Columns: `condition, scheme, variant, param, avg_bucket, max_bucket, q, baseline_success, bucket_success, loss, std_over_repeats, n_targets, repeats, pool, seed, cfg_hash`.
- `figs/fig1_pareto` (average bucket size vs loss at q=1000, HPB vs FSB, M0), `figs/fig2_mismatch` (loss at q=1000 vs mismatch condition and severity), `figs/fig3_fix` (Pareto under M0, M1, M2: baseline FSB vs best fix). Axis labels with units; error bars from the repeats.
- `results/REPORT.md`, in this order: data summary; correctness checks with pass/fail and the printed evidence; E1 table and whether the expected shape appeared; E2 table and the gate statistic; E3 table; runtimes; known issues and deviations from this plan; exact commands to reproduce.

## 8. Rules

- Report every run, including bad ones. Do not drop, re-roll or cherry-pick seeds.
- Never tune on the pool you report on.
- Do not write paper text, abstracts or conclusions. `REPORT.md` states numbers and whether checks passed, nothing more.
- No network access except fetching the corpora. Do not upload data anywhere.
- If something in this plan looks wrong or ambiguous, write the question to `results/QUESTIONS.md`, choose the most conservative reading, and carry on unless it blocks a check.

## 9. What the human will verify

They will replay `worked_examples.txt` by hand, compare the E1 shape with the base paper's Fig. 8, confirm targets and attacker training are disjoint, check that CSV numbers match the figures, and read `DISCREPANCIES.md` and `QUESTIONS.md`. Make that easy.
