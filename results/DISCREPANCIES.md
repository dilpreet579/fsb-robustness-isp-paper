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

