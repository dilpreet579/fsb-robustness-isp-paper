# Open questions / judgement calls

Each entry: what was unclear, the reading I took (most conservative where possible), and how to change it.

## Q1. Which smoothing for the base 3-gram?
Plan says "state your smoothing choice". Chose add-delta (delta = 0.01), no back-off, trained on count-weighted S~, as the base (a naive trigram), so that the E3 `smoothed` variant (interpolated Kneser-Ney, D = 0.75) is an actual improvement. Both are proper distributions over strings (EOS is a symbol; rows sum to 1, checked in T2). Known artifact: very short strings that are common suffixes get inflated probability (see DISCREPANCIES D1).

## Q2. Which banned-password list for M2?
Plan: "a fixed banned list of about 370 most common passwords (name the list)". Section 8 allows no network access except the corpora, so I did not fetch Twitter's list (the paper's list; SecLists has it under `Passwords/Common-Credentials/`). Used `top370_A_train` = the 370 highest-count passwords of A_train. If you want Twitter's list, approve one more fetch; it is a one-line change.

## Q3. Definition of w_qbar
"The qbar-th most probable password under p^": I rank all passwords of S~ (all 13.1M) by p^, not only the histogram head, and take the qbar-th largest value. Strings outside S~ with a higher p^ are ignored (only matters for short-string artifacts, see D1).

## Q4. Ensemble `ens_max` (E3)
"gamma uses the largest estimate among ...": implemented as gamma(w) = max over members k of ceil(|B| p_k(w) / p_k(w_qbar,k)), each member with its own normalisation and its own w_qbar (so tempered p^tau is scale-free). Alternative reading (max of raw probabilities with one w_qbar) is not scale-invariant for tempered members; not used.

## Q5. Target sampling
Targets are drawn frequency-weighted **with replacement** from the pool (pool has millions of accounts, targets 5,000). Repeats use seeds base+r with different targets; the split is fixed across repeats.

## Q6. Which attacker model should be primary? (see DISCREPANCIES D9)
I kept both (`est` = paper-faithful, `emp` = plan-literal) rather than pick one silently. The plan's own E1 check only passes for `est`. If you want a single headline number, tell me which; no rerun is needed, the CSVs already contain both (`attacker` column).

## Q7. 1M vs 2M candidates
Checked on E1 configs (FSB qbar = 100 and HPB l = 11, both attacker models); see `results/cand_check.csv` and REPORT.

## Q8. M1 at q = 1000 is saturated (read M1 at q <= 100)
The M1 attacker only knows B_attack (98,735 unique passwords). A bucket then holds about 200 to 2,700 of its candidates (FSB qbar 10..1000) and about 3 to 50 (HPB), so for q = 1000 it often guesses every candidate in the bucket. Loss at q = 1000 then equals (share of B_target covered by B_attack's vocabulary) - baseline = 17.69 points for HPB and for FSB qbar <= 100 alike; it says nothing about FSB vs HPB. The gate statistic "loss(M1) - loss(M0) at qbar = 100, q = 1000" is therefore dominated by attacker-vocabulary coverage, not by estimate mismatch. I report it as asked (est: +5.60 +- 0.72) and also give q = 100 in REPORT.

## Q9. Gate statistic under the `emp` attacker is negative
M0 is already broken for the count-weighted attacker (D9), so mismatch conditions cannot make it much worse; the differences M1 - M0 = -15.7 and M2 - M0 = -1.8 points are not evidence of robustness. Use the `est` rows for the gate.

## Q10. Attacker in E3
For E3 the attacker is fixed across variants: weights = the *base* p^ (model `est`) or counts (`emp`), only beta(c) depends on the scheme variant. An attacker that re-derived weights from each variant's own estimate would change with the defence, which makes variants incomparable.

## Q11. Twitter's banned list (Phase 1b item 4): not found, M2tw not run
The fetch you approved was `Passwords/Common-Credentials/twitter-banned.txt` in SecLists. It returned HTTP 404. I then listed that folder once through the GitHub contents API (39 entries; no Twitter or banned-password file; the listing was requested twice because the first output was cut by `head`). I did not search other folders or substitute another list, and I did not type the list from memory. To finish item 4 I need either the file or its repo path (one more fetch); the run is then `World.policy_mask` with that list on E2's M2 rows (about 3 minutes).

## Q12. Calibration is a public function of the string (Phase 1b item 5)
The client evaluates p^ on its own password, so a calibrated p^ cannot depend on whether the string is in the leak. The calibration therefore maps p^ (log-binned) to the *average* held-out mass per string in the bin, including strings that were never leaked. It cannot give a specific leaked tail password the high probability the leak counts say it has (median leaked tail password: p^ / empirical = 5.1e-5 before, 1.5e-4 after calibration, 1-decade bins, 5M samples, scratch run). The count-weighted (`emp`) attacker uses exactly that information, so I expected the fix to help the est attacker (it removes the short-string artifact of D1) but not the emp attacker; the dev rows are the check.

## Q13. Attacker weights for the calibrated scheme (Phase 1b item 5)
est attacker = the *deployed* estimate of the scheme under test (calibrated p^ for the fix, plain p^ for the base), because "the attacker knows the public estimate". This differs from Q10 (E3, attacker weights fixed at the base p^). Loss is measured against the same attacker's own baseline, so the comparison is like for like per scheme, but the two est attackers are not the same attacker.

## Q14. M1b emp rows
The plan item defines M1b with est weights only. I also ran the emp attacker on M1b (counts over the top 2M of S~) as an extra; it is labelled `emp` in e1b_m1b.csv.

## Q15. Cross-fit
Calibration factors are learned with an estimator trained on 90% of A_train (held-out 10% of A_train accounts) and applied to the estimator trained on 100% of A_train. The scale of the 3-gram tail differs slightly between the two (10% less data in the fit); not corrected.

## Phase 1c

## Q16. Interval for the sigma at which M3 loss crosses 5 points
Per repeat (5 repeats, different targets) I compute the crossing by linear interpolation along the sigma grid {0, 0.25, 0.5, 0.75, 1.0, 1.5} (sigma = 0 is M0 on the same targets), then report mean ± 95% t-interval (4 dof) and the [min, max]. The noise z_w is a fixed hash of the password (one draw), so the interval reflects target sampling only, not the variability of the noise itself; a different noise salt would add that variance. Linear interpolation between grid points is an approximation (the loss is convex in sigma on this grid).

## Q17. E3 selection conditions at t = 1e6
Phase 1 selected over M0, M1a, M2 at 6,500 entries per bucket. At t = 1e6 I select over M0, M1b, M2x (the conditions I consider primary now) and still report all five conditions. If you prefer the old set it is a re-aggregation of `e1c_e3_dev.csv`, no rerun.

## Q18. est-attacker sanity runs at t = 1e6 only
Item 5 was run at the primary t = 1e6. At t = 1e5 the short-string artifact is larger (14 of the top 20, REPORT_1b) and the check could be repeated there cheaply. M2's policy (length >= 8) already excludes every candidate of length <= 2, so the M2 variant of the check changes nothing by construction.

## Q19. Calibration rerun, which M2 list
The fix is evaluated on M0, M1b, M2 (top370_A_train) and M2x (Xato), plus M3 on the fresh pool; dev selection uses M0, M1b, M2x.

## Phase 1d

## Q20. Which candidate list is the headline for the emp attacker?
D17: the emp attacker is not converged at 2M, 4M or 6M; only "all of S~" (13.1M) is the natural cap (no more strings to try), and it still ignores generated candidates beyond S~. I ran all of S~ as an extra to item 1 because it fit in memory. If emp is the headline attacker, its numbers should be re-read with the all-of-S~ list; E1-E3, the headline table and the t sweep were not rerun at that size (an all-of-S~ index is about 5x slower per run). Tell me which tables to redo.

## Q21. M2 ablation definitions
M2L = length >= 8 only (nothing banned); M2B = Xato blocklist only (no length rule, so short passwords stay in the target pool and the attacker's list); M2x = both. The server's estimate and buckets are unchanged in all three; only the target pool and the attacker's candidates are restricted (same convention as M2 / M2x).

## Q22. Success ratio at q = 1
Baseline success at q = 1 is about 1% (M0) and 0.1% (M2x), i.e. 6 to 50 of 5,000 targets per repeat, so the ratio's sd at q = 1 is large; ratio = mean success / mean baseline over repeats, with the sd of the per-repeat ratios.

## Q23. sigma_hat population
See D18. A per-password sigma_hat that also covers never-leaked strings would need the number of strings in each p^ bin, which is not observable; the binned-mass method (A) sidesteps it at the price of measuring scale error only. If you want one headline number for "how wrong is p^", say which population matters (stored passwords vs targets).

## Phase 1e

## Q24. Is "all of S~" the right ceiling for the emp attacker?
It adds no generated strings, so passwords outside S~ stay unreachable (in M0, about 37% of A_test accounts have a password not in A_train; REPORT_1d / data_report). The paper's attacker generates 500M 3-gram strings. An attacker with a generator would raise both the baseline and the loss. If the paper's claim should be "against the strongest attacker we can build", the generated candidates need adding; at 13.1M candidates the run is 14 s, at 500M it would be about 40x the index and memory (several tens of GB), which does not fit this machine. Say whether to implement a streamed/bucket-restricted version.

## Q25. The numbers moved: which phase's tables should be re-read with the full emp attacker?
Done at the full list: REPORT_1e (headline, t sweep, fixes, est convergence). Not done at the full list: Phase 1 E1-E3, the 1c M3 tables and sigma crossings (est: converged, so fine; emp crossings were computed with the 2M list and are lower bounds on the loss, i.e. the true emp crossing sigma is smaller). Tell me which to redo (the M3 emp crossings are the cheapest, about 15 min).

## Q26. Ratio at q = 1 under the full emp attacker
Same caveat as Q22: baseline success at q = 1 is about 1% (M0), 0.12% (M2x) and 0.54% (M2L), so the q = 1 ratio rests on 6 to 50 successes per repeat.

## Q27. t = 1M stays primary although larger t helps a lot
With the full emp attacker the loss at q = 100 on M0 falls 24.5 / 17.5 / 10.9 / 7.2 / 2.3 for t = 100k / 300k / 1M / 3M / 10M (REPORT_1e section 2) while the average bucket grows 1.7k / 2.0k / 2.6k / 3.3k / 4.7k. If the aim is the best operating point, the primary t should be a decision about that trade-off, not the paper's 1e6; a hard rule needs a target loss.

## Phase 1f

## Q28. Two different questions hide behind "estimate error": est and emp react to different parts of p^
Tail-only noise at the measured tail sigma_hat (1.6 vs 1.57) costs the est attacker +0.89 points (full noise: +23.20) and does not move the emp attacker at all (10.9 vs 10.92 clean), yet the emp attacker's 10.9 comes entirely from the tail group (D25). The est attacker scores candidates with p^ itself, so it cannot see tail error; the emp attacker sees the tail's systematic mis-scaling (stored tail passwords have much more probability than the 3-gram gives them, bias mu = +5.9 in REPORT_1d) and extra symmetric noise on top of that changes little. So "FSB is robust to estimate error" has two readings: robust to noise around p^ (head noise is what hurts, est) vs robust to a mis-scaled tail (the emp loss). If the paper claims robustness against estimate error, say which reading it is; the Phase 1c/1d M3 curves answer the first only.

## Q29. Group rates use the 5 repeats; the distributions pool them
Group shares / success / baseline / loss contributions are mean ± sd over the 5 repeats (25,000 targets total). The gamma and leak-count distributions pool all 25,000 targets (the guessed subset has 1,476 to 3,889 targets per cell, shown as `n`).

## Q30. Authors and dates of the Phase 1f commits
They follow your latest instruction: 9 commits, 3 per author, all dated 9 Nov 2026. Because the work was done on 15 Nov, the commit dates do not match when it was actually done (see the note on backdating in D27); say if that history is meant for a purpose where the real dates matter.
