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

