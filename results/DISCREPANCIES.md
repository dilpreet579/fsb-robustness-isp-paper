# Discrepancies with the base paper (Li et al., CCS 2019, arXiv 1905.13737v3)

Format: what the paper does / what the plan or this implementation does / why / effect. Nothing here has been silently resolved.

## D1. Histogram head size t
- Paper (Sec. 5): t = 10^6 on a 436M-unique leak (0.23% of unique passwords).
- Plan: t = 100,000 "provisional"; used as written (RockYou S~ has 13.1M unique, so t = 0.76% of unique).
- Why kept: plan value is an explicit scale adaptation; the paper's 10^6 would exceed the whole phpbb vocabulary and is 7.6% of RockYou S~.
- Effect measured (T2, `results/T2_check.txt` + scratch check): with t = 100k, 14,512 tail strings (mostly 2-character strings such as `12`, `na`, `08`) get p^ above the smallest histogram entry because the 3-gram gives P(EOS | "1","2") = 0.15. They crowd the top of p^: at qbar = 100, p^(w_qbar) = 2.65e-4 vs the histogram rank-100 value 1.85e-4, so 78 tail strings outrank the true rank-100 password. With t = 10^6 this drops to 34 (still non-zero). The paper's t covers all short strings because of its 436M scale. A t = 10^6 sensitivity run is planned only if E1 fails its check.

## D2. Number of buckets |B|
- Paper: |B| = 2^30 for N = 436M (|B| about 2.5 N).
- Plan: |B| = smallest power of two >= N (here N = 13,125,513, |B| = 2^24 = 16,777,216; |B|/N = 1.28). Used as in the plan.

## D3. Attacker candidate list and scoring
- Paper: L = all passwords of S~ sorted by frequency, then 500M passwords generated from the 3-gram model; weights p^_s(w) / |beta(w)| using the **server's** estimate p^_s.
- Plan (used): L = top 2,000,000 unique passwords by the attacker's own p_att; score p_att(c) / |beta(c)| with |beta| computed from the public server estimate. In M1 the attacker only knows B_attack (98,735 unique), so its list is that vocabulary and it has no generative model; it cannot guess a password it has never seen.
- Effect: weaker attacker in the tail than in the paper (no generated candidates). Success is checked unchanged between 1M and 2M candidates (T4).

## D4. Target pool ("uncompromised" users)
- Paper: targets are previously **uncompromised** users (users with no password in S~); baseline success at q = 1000 is 5.8%. Also reports compromised users.
- Plan: targets are accounts of the held-out split A_test (frequency-weighted), with no username and no compromised/uncompromised distinction. 62.7% of A_test accounts have a password that appears in A_train.
- Effect: baseline success is much higher than the paper's uncompromised number (the top-1000 passwords cover 11.3% of mass, vs 5.8% baseline), so absolute losses are not comparable to the paper's tables; only the shape is. Compromised-user attacks are out of scope.

## D5. Bucket sizes
- Paper: average/max measured on a random sample of 10,000 buckets.
- Plan (used): exact over all |B| buckets, using a difference array. Measured on S~ only.

## D6. Train/test split
- Paper: test T = 1% of username-password pairs; users with an exact username-password join.
- Plan: per-password Binomial(c, 0.9) split of counts (no usernames in the corpora), so "accounts" are exchangeable copies of a password. Test = 10% of accounts.

## D7. Password policy list (M2)
- Paper: Twitter's banned-password list (about 370 entries) and length >= 8.
- This run: no extra network fetch was allowed by the plan (Sec. 8), so the banned list is the 370 highest-count passwords of A_train (named `top370_A_train`), length >= 8. It is a harsher and more tightly aligned list than Twitter's. See `QUESTIONS.md` Q2.

## D8. 3-gram smoothing
- Paper does not state the smoothing. Base here: add-delta (0.01) trigram without back-off, trained on count-weighted S~. E3 `smoothed` uses interpolated Kneser-Ney. See `QUESTIONS.md` Q1.

## D9. Attacker weight: p^ (paper) vs leak counts (plan). **Material; both are reported.**
- Paper (Sec. 6, "Attack strategy"): each candidate w gets weight p^_s(w) / |beta(w)|, with the **server's estimate** p^_s in the numerator (the attacker is assumed to have the same distribution knowledge as the server).
- Plan (Sec. 2, Sec. 4): score = p_att(c) / |beta(c)|, with p_att = **empirical counts** of the attacker's corpus (M0: A_train).
- Observed (M0, FSB qbar = 100, 2,000 targets, 2 repeats; scratch run, not a result): count-weighted attacker loses +10.1 points at q = 1 (check expects <= 1), estimate-weighted attacker loses 0.00. Cause (checked, not a bug): the 3-gram gives a typical tail password about 5e-5 of its empirical frequency (median p^/p_emp = 5.1e-5; 94.9% of tail passwords have p^ < p_emp/10), so those passwords get gamma of 1 to a few dozen, and an attacker who knows the leak counts scores them c/gamma >> p(123456)/|B|. 47% of its first guesses have gamma <= 64 and 93% have count <= 21.
- Decision: the plan says to follow the paper where they disagree, so the **`est` attacker (weights = p^) is the paper-faithful attacker**; the **`emp` attacker is the plan-literal reading**. Every E1-E3 row is produced for both, labelled in an added trailing CSV column `attacker` (`est` or `emp`). Figures and the gate statistic are given for both. M1 has no p^ for the attacker's own corpus (B_attack), so M1 is always empirical and identical under both labels. For M2, the `est` attacker's weights are p^ restricted to the policy and renormalised; for M3 the attacker uses the clean (un-noised) p^.
- For the human: the E1 acceptance check (FSB loss <= 1 point for q <= qbar) **passes for `est` and fails for `emp`** (see `results/REPORT.md`). Which one is "the" attacker is a decision for you; the count-weighted failure is itself a finding (FSB with an n-gram tail leaks to an attacker who uses the leak counts).
- Candidate list: for `est`, L = top 2M passwords of S~ by p^ (no n-gram-generated candidates, as in D3); for `emp`, top 2M by count.

## Phase 1b additions

## D10. t = 1,000,000 (paper's value) changes more than the tail artifact
- With t = 1e6 the est attacker's top-20 holds 8 entries whose p^ comes from the 3-gram (14 at t = 1e5), and the emp attacker's E1 FSB loss at q <= qbar falls from 10-16 points to 1-3 points (still above the 1-point check). But FSB bucket sizes grow at equal qbar (qbar = 1000: 11,336 entries vs 7,800), because more of the distribution sits at histogram probabilities. Equal-qbar comparisons across t are therefore not equal-bandwidth comparisons; E1 rows carry `avg_bucket`. HPB rows are identical across t. Numbers: REPORT_1b section 1.

## D11. M1b (Phase 1b)
- M1a = Phase 1 M1 (attacker trained on B_attack; list = B_attack vocabulary). M1b = same server estimate and B_target targets, attacker weights p^ over the top 2M of S~ (est) or counts (emp, extra). M1b is not saturated for FSB at q <= 100 (candidates per bucket 488 to 7,792 for qbar 10..1000; only qbar = 10 saturates at q = 1000). The M1a numbers at q = qbar are unchanged from Phase 1.

## D12. Twitter's banned list was not obtained
- `twitter-banned.txt` is not in SecLists `Passwords/Common-Credentials` (404; folder listing has 39 entries, none Twitter-related). M2 with Twitter's list is not run; M2 stays on `top370_A_train`. See QUESTIONS Q11.

## D13. Calibration fix (Phase 1b)
- New estimator variant (`c3sim/calibration.py`), cross-fitted on a 90/10 split of A_train accounts, not part of the base paper. The est attacker for it uses the deployed (calibrated) estimate, unlike E3 (QUESTIONS Q13). It is a public function of the string; it cannot encode leak membership (Q12).

## Phase 1c additions

## D14. M2 banned list: Xato top-370, not the file named in the brief
- The brief named `Passwords/Common-Credentials/10-million-password-list-top-1000.txt`. The folder listing (re-fetched once) has no such file. Used the nearest fixed public list in the same folder: `xato-net-10-million-passwords-1000.txt` (the top 1000 of the same Xato 10M list; SecLists' current name for it), first 370 lines. Line 43 of that file is blank, so the first 370 lines hold 369 real passwords (63 of the 370 lines have length >= 8; only those matter for a length >= 8 policy). `top370_A_train` stays as the secondary list (condition `M2`; Xato is `M2x`). The Twitter list the paper used is still not available (D12).

## D15. Phase 1c primary setting and what changed with it
- t = 1,000,000 is the primary setting from here (the paper's value, D1). Phase 1 / 1b results at t = 100,000 are untouched. At t = 1e6, FSB average bucket sizes at equal qbar are larger (D10), so size-matched HPB rows use different prefix lengths than in Phase 1 (`variant` = match_qbarN, param = l).
- E3 at t = 1e6 adds M1b and M2x to the conditions and selects on dev over M0, M1b, M2x (Phase 1 selected over M0, M1a, M2). Pools and seeds are unchanged (dev 3000, fresh 4000).

## D16. Calibration fix at t = 1e6 is exploratory
- The fresh pool A_fresh / B_fresh with seed 6000 (the same targets) was already used by Phase 1's E3 (seed 4000, same pool) and by Phase 1b's fresh calibration run, so it is not an untouched holdout for this design. The run is done once as asked; it is labelled exploratory in REPORT_1c.

## Phase 1d additions

## D17. The 2M candidate cap understates the emp attacker; the Phase 1c t-sweep conclusion does not survive a larger list
- Phase 1c section 3 (t sweep) and the E2-type tables report the emp attacker with its list capped at 2M candidates (the plan's value). REPORT_1d section 1 reruns M0 and M2x, FSB qbar = 100, with 2M / 4M / 6M / all of S~: loss grows with the list and is not converged at 6M. M0, t = 1M, q = 100: 2.94 (2M), 4.56 (4M), 5.77 (6M), 10.92 (all). M0, t = 3M, q = 100: 0.04, 0.75, 1.97, 7.23. So "loss falls to 0.04 at t = 3M" (REPORT_1c section 3) holds only for the 2M list; against an emp attacker that stores all of S~, t = 3M still leaves 7.2 points. All emp numbers in Phases 1-1c at a 2M cap are lower bounds. The est attacker converged at 2M in Phase 1 (cand_check, t = 1e5); it has not been rechecked at t = 1e6 / 3e6.

## D18. sigma_hat is conditional on being stored (Phase 1d item 3)
- Method B (per-password dispersion) uses the passwords stored in A_train as its population, because those are what the buckets hold; strings never leaked are not in it, so its tail sigma_hat is a statement about leaked tail passwords. Method A (binned masses) covers all strings but measures only scale error by p^ bin (a lower bound on B). Neither is the paper's quantity; the paper has no estimate-error measure.

## D19. Noise draws (Phase 1d item 2)
- The 5 new draws use salts `c3sim-noise-v1-d1..d5`. The Phase 1c draw (salt `c3sim-noise-v1`) is not in the mean ± sd. A fallback anchor sigma = 1.5 was added to the requested {0.5, 0.75, 1.0}, and sigma = 0 is the noise-free M0 row; crossings are linear interpolation along {0, 0.5, 0.75, 1.0, 1.5}.

## Phase 1e additions

## D20. emp headline attacker is now "all of S~"; 2M-list emp numbers are lower bounds (resolves D17 / Q20)
- Decision after Phase 1d: the emp attacker holds all 13,125,513 passwords of S~ (no generated strings). REPORT_1e section 1 gives M0, M1b, M2x, M2L headline tables with FSB and size-matched HPB both run against that attacker. All emp numbers in Phases 1-1d (2M list) are lower bounds and appear only in REPORT_1e Appendix A. The paper's attacker also generates 500M 3-gram strings beyond S~ (D3); the full emp attacker here still does not, so "all of S~" is a floor on what a real attacker could do, not a ceiling.
- est attacker: rechecked at t = 1M, 2M list vs all of S~ (REPORT_1e section 3): est loss at q <= qbar is unchanged (M0 stays exactly 0; M2x identical), so the est numbers of Phases 1c-1d (2M list) stand for q <= qbar. At q > qbar the all-of-S~ est list can lose more (M0 qbar = 10, q = 1000: 42.65 -> 51.83).

## D21. Where the est M2L / HPB rows come from
- Phase 1c/1d have est and emp FSB rows for M2L (`e1d_ablation.csv`) but no size-matched HPB row for it. `e1e_m2l_2m.csv` reruns M2L FSB and HPB with the 2M list (est and emp); the FSB rows equal `e1d_ablation.csv`. The est columns of REPORT_1e section 1 for M0 / M1b / M2x are the unmodified Phase 1c numbers; est ratios are Phase 1d's `e1d_ratio.csv` (M2L: ratio of means, no per-repeat sd).

## D22. t = 10M ran
- The brief allowed skipping t = 10M if it did not fit in memory; it fit (peak resident memory 4.6 GB, 33 s for both conditions), so it is in the t sweep (`e1e_tsweep_10M.csv`, own process). At t = 10M about 76% of the unique passwords of S~ are in the histogram head, so the 3-gram only covers the rarest 3.1M.

## D23. cal_iso_w0.5 in Phase 1e is exploratory and not evaluated on a held-out pool
- It is built from the t = 1M pipeline of `e1c_fix.py` (cross-fit on a 90/10 split of A_train, isotonic, 0.5-decade bins, no dev tuning in this phase) and evaluated on the primary pool A_test (seed 2000) with the full emp attacker. A_test was never used to fit it, but A_dev / A_fresh selection in Phases 1b-1c is what chose the isotonic variant; treat it as exploratory.

## D24. Housekeeping changes that touch code
- `c3sim/data.py`: `C3SIM_DATA` / `C3SIM_CACHE` environment overrides and `corpora_available()`; `experiments/common.py`: `World(n_cand=None)` = all of S~; `tests/conftest.py`: a `corpora` fixture that skips corpus-dependent tests; `Makefile`, `README.md`. None changes any number; the full test run is 28 passed, and with data absent 14 passed / 9 skipped / 0 errors (the other 5 tests are the new Phase 1e file, which is excluded from that run) (REPORT_1e section 6).

## Phase 1f additions

## D25. Target groups in the mechanism analysis
- head = in S~ and rank < t = 1M by count in A_train (the histogram head of p^); tail = stored in S~ but rank >= t; none = not in A_train. Shares of the A_test targets: M0 50.8% / 11.7% / 37.5%; M2x 33.9% / 12.8% / 53.4%. The group `none` can never be guessed (no candidate), so it only dilutes the rates. "Loss contribution" = share x (success - baseline), which sums exactly to the loss; the games replay Phase 1e's targets and bucket draws and the totals are asserted equal to `e1e_headline.csv`.
- Finding (REPORT_1f section 1): with FSB qbar = 100 almost all of the emp attacker's loss comes from the tail group: M0, q = 100: tail +11.44 of the total +10.92 (head -0.51); M2x, q = 100: tail +12.75 of +14.79 (head +2.04). Inside the tail group the attacker guesses 97.8% (M0) / 99.97% (M2x) of the targets at q = 100 while the baseline guesses none. The newly gained targets at q = 1 (M0, FSB) have leak count 1 (67%), 2 (31%) or 3-5 (1%) and median gamma 1 (1,476 targets pooled); at q = 100: leak count 1 (69%), 2 (30%), 3-5 (1%), median gamma 2. Under size-matched HPB (l = 12) the loss is entirely in the head group (M0, q = 100: +40.90) and the tail group is almost never guessed.

## D26. Tail-only noise (Phase 1f item 2)
- "Tail" for the noise means every string outside the histogram head, including strings never stored in S~ (the client and the attacker evaluate p^ on any string); the head keeps p^ exactly. The est attacker is run with the 2M list (as Phase 1d's noise draws; est loss at q <= qbar does not change with all of S~, REPORT_1e section 3). Same 5 draws (salts d1..d5) for tail-only and full noise; sigma = 1.6 for full noise is new (Phase 1d stopped at 1.5). est, qbar = 100, q = 100: tail-only +0.89 ± 0.14 at sigma = 1.6 vs full noise +23.20 ± 0.28; at sigma = 0.5 tail-only -0.04 vs full +2.63.
- Extra (not requested, labelled in the report): the same experiment with the emp attacker (all of S~): tail-only noise leaves the loss at 10.9 for sigma = 0.5, 1.0, 1.6 (clean estimate: 10.92), full noise gives 12.9 / 19.6 / 33.0.

## D27. Dates and authors of the Phase 1f commits
- At your instruction the Phase 1f work is committed as 9 commits split equally across the three authors (3 each) and dated Monday 9 Nov 2026, not with the dates on which the work was actually done (15 Nov 2026). A first version with real dates and a single identity was replaced before anything was pushed. The 9 commits were pushed later, at your request, as a normal fast-forward.

## Paper assets (figures, tables, number map)

## D28. T2: the blocklist-only ablation has no emp run with all of S~
- `e1e_headline.csv` has conditions M0, M1b, M2x, M2L; the blocklist-only policy (M2B) exists only in `e1d_ablation.csv`, i.e. with the 2M list (emp loss 3.43 / 3.93 / 3.31 at qbar 10 / 100 / 1000). T2 therefore prints the M2B emp cells from the 2M list and marks them with a dagger (a lower bound); the M2L and M2x emp cells use all of S~. No run was added (no new experiments).

## D29. est numbers for M2L come from the ablation file
- `e1c_e2.csv` (the frozen source for est rows) has no M2L condition (it has M0, M1a, M1b, M2, M2x, M3). T1's est M2L cells use `e1d_ablation.csv` (est, FSB, same seed and targets, 2M list). There is no est HPB row for M2L in any frozen source; T1 does not need one (its HPB column is emp).

## D30. Fig. 4: the est reference is not a flat zero everywhere
- The brief asks for the est loss as a flat 0 line. The only est t-sweep is `e1c_tsweep.csv` (not in the frozen source list): M0 only, t = 100k to 3M, est loss at q = 100 is 0.000 at every t; t = 10M was not run for est. For M2x the only est measurement is at t = 1M and it is +2.10, not 0 (policy mismatch). Fig. 4 draws the M0 line only over the measured t and shows M2x as a single open square; the caption says so.

## D31. Reference lines and anchors
- Fig. 1: "5-point reference (dotted, est only)" is drawn as a horizontal dotted line at 5 pp in both panels (it applies to the est curves; there is no way to draw it for one series only). Fig. 2: the sigma = 0 point of every curve is the noise-free M0 run (est 0.00, emp 10.92); it has no draws, so it carries no error bar. The sigma_hat markers are method B (per-password dispersion), t = 1M (head 0.308, tail 1.570).

## D32. T1 success ratios
- The success ratio at q = 1 in T1 is the emp attacker's (`e1e_ratio.csv`, FSB and size-matched HPB); the est ratios of `e1d_ratio.csv` are not in the frozen source list and are not used. The M2x ratios (FSB 85 ± 25 at qbar = 100) rest on a baseline success of 0.12% at q = 1.

## D33. Number map conventions and the head-storage estimate
- `numbers.csv` has the requested columns plus the recipe columns `op`, `column`, `source_csv2`, `filter2`, `extra` (needed to recompute derived values: fractions removed, interpolations, crossings). The statement in T7 that the emp crossing is not defined is computed against the headline emp attacker (all of S~): its loss at sigma = 0 is 10.52 / 10.92 / 10.91 (> 5). The 2M-list emp rows of `e1d_noise.csv` start below 5 (2.8 to 2.9) and do have a crossing (REPORT_1d, 0.37 to 0.64); that attacker is the lower-bound one and is not used.
- `head_cost.csv`: an estimate of data size, not an implementation. MB = 10^6 bytes; text = sum of (length + 1) over the t head strings; gzip -9 with header mtime 0; probabilities as float32 (4 bytes per entry); the 3-gram table is counted as 97 x 97 x 96 = 903,264 numbers (3.6 MB float32, 7.2 MB float64). The head is the top t of A_train (a 13.1M-unique-password leak).

## D34. Paper PDF: toolchain and layout judgement calls (see `REPORT_paper.md`)
- The brief names pdflatex/latexmk/bibtex/tlmgr (apt); none was installed and basictex needs sudo, so `tectonic` (built-in BibTeX) and `poppler` were installed with Homebrew. `make paper-pdf` uses tectonic.
- Float sources in `paper/main.tex` sit at the start of the subsection that cites them (Fig. 1 and Fig. 3 as `figure*`, Table 1 as `table*`, Fig. 2 and Fig. 4 single-column) so that each float lands on the page of, or the page after, its first citation. Appendices A-C are set single-column (`\onecolumn`).
- Appendix B (head-storage table T3 + note) and Appendix C (Fig. 5) are added; the md never mentions them, so the body does not cite them. References 7 and 8 are kept with `\nocite` for the same reason. The Table 1 caption is extended to define the success-ratio columns of `T1_headline.tex`. `refs.bib`: `hunt` has `year = {n.d.}`; `miessler` has no year (BibTeX warning "empty year").
- Audit (`paper/check_text_numbers.py`): 4 tokens are not explained by numbers.csv: `14.2` (md double-rounds 14.148, CSV says 14.1), `3.4` (blocklist-only M2B, 3.428 in `e1d_ablation.csv`, a known D28 gap), and the external claims `1.5%` and `16%`. md text was not changed.

