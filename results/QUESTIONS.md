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

