# REPORT 1f (Phase 1f: mechanism and tail-only noise)

Numbers and method statements only. Earlier phases' results were not modified; Phase 1f adds `results/e1f_*`, `experiments/e1f_*.py`, `experiments/report1f.py`, `tests/test_phase1f.py`. Setting: t = 1,000,000, seed 2000, pool A_test, 5 repeats x 5,000 targets (the same targets and bucket draws as Phase 1e), units percent / percentage points, ± = sd over the repeats unless stated. The emp attacker (section 1) holds **all of S~** (13,125,513 candidates).

## 1. Mechanism: which targets does the emp attacker get?

Target groups (by the target's password): **head** = stored in S~ and among the top t = 1M passwords of A_train by count (the histogram head of p^); **tail** = stored in S~ but not in the head; **none** = not in S~ (no candidate, can never be guessed). Per group: `share` of all targets; `success` and `baseline` = rate within the group (bucket attacker / no-bucket attacker, top q); `loss contribution` = share x (success - baseline) = the group's part of the total loss, summed over groups (the `total` row). The games replay Phase 1e exactly and the totals are asserted equal to `e1e_headline.csv` (the script stops otherwise). qbar = 100.

### M0, FSB qbar=100

| q | group | share | success | baseline | loss_contribution | part_of_total_loss |
|---|---|---|---|---|---|---|
| 1 | head | 50.83 ±0.81 | 0.10 ±0.07 | 1.90 ±0.39 | -0.92 ±0.20 | -18% |
| 1 | tail | 11.69 ±0.27 | 50.48 ±2.75 | 0.00 ±0.00 | +5.90 ±0.39 | 118% |
| 1 | none | 37.48 ±0.65 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | total | 100.00 ±0.00 | 5.96 ±0.40 | 0.97 ±0.21 | +4.99 ±0.30 | 100% |
| 100 | head | 50.83 ±0.81 | 8.11 ±0.82 | 9.11 ±0.87 | -0.51 ±0.06 | -5% |
| 100 | tail | 11.69 ±0.27 | 97.80 ±0.62 | 0.00 ±0.00 | +11.44 ±0.31 | 105% |
| 100 | none | 37.48 ±0.65 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 100 | total | 100.00 ±0.00 | 15.56 ±0.60 | 4.63 ±0.45 | +10.92 ±0.35 | 100% |

### M0, HPB l=12 (size-matched)

| q | group | share | success | baseline | loss_contribution | part_of_total_loss |
|---|---|---|---|---|---|---|
| 1 | head | 50.83 ±0.81 | 30.53 ±1.37 | 1.90 ±0.39 | +14.55 ±0.56 | 100% |
| 1 | tail | 11.69 ±0.27 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | none | 37.48 ±0.65 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | total | 100.00 ±0.00 | 15.52 ±0.72 | 0.97 ±0.21 | +14.55 ±0.56 | 100% |
| 100 | head | 50.83 ±0.81 | 89.58 ±0.77 | 9.11 ±0.87 | +40.90 ±0.65 | 100% |
| 100 | tail | 11.69 ±0.27 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 100 | none | 37.48 ±0.65 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 100 | total | 100.00 ±0.00 | 45.53 ±0.73 | 4.63 ±0.45 | +40.90 ±0.65 | 100% |

### M2x (len>=8 + Xato), FSB qbar=100

| q | group | share | success | baseline | loss_contribution | part_of_total_loss |
|---|---|---|---|---|---|---|
| 1 | head | 33.88 ±0.71 | 0.02 ±0.05 | 0.34 ±0.08 | -0.11 ±0.04 | -1% |
| 1 | tail | 12.76 ±0.49 | 77.38 ±1.80 | 0.00 ±0.00 | +9.87 ±0.37 | 101% |
| 1 | none | 53.36 ±0.67 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | total | 100.00 ±0.00 | 9.88 ±0.38 | 0.12 ±0.03 | +9.76 ±0.39 | 100% |
| 100 | head | 33.88 ±0.71 | 13.50 ±0.66 | 7.48 ±0.94 | +2.04 ±0.24 | 14% |
| 100 | tail | 12.76 ±0.49 | 99.97 ±0.07 | 0.00 ±0.00 | +12.75 ±0.50 | 86% |
| 100 | none | 53.36 ±0.67 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 100 | total | 100.00 ±0.00 | 17.33 ±0.58 | 2.54 ±0.36 | +14.79 ±0.69 | 100% |

### M2x (len>=8 + Xato), HPB l=12 (size-matched)

| q | group | share | success | baseline | loss_contribution | part_of_total_loss |
|---|---|---|---|---|---|---|
| 1 | head | 33.88 ±0.71 | 29.38 ±0.78 | 0.34 ±0.08 | +9.84 ±0.41 | 100% |
| 1 | tail | 12.76 ±0.49 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | none | 53.36 ±0.67 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 1 | total | 100.00 ±0.00 | 9.96 ±0.42 | 0.12 ±0.03 | +9.84 ±0.41 | 100% |
| 100 | head | 33.88 ±0.71 | 98.06 ±0.25 | 7.48 ±0.94 | +30.68 ±0.40 | 100% |
| 100 | tail | 12.76 ±0.49 | 0.13 ±0.07 | 0.00 ±0.00 | +0.02 ±0.01 | 0% |
| 100 | none | 53.36 ±0.67 | 0.00 ±0.00 | 0.00 ±0.00 | +0.00 ±0.00 | 0% |
| 100 | total | 100.00 ±0.00 | 33.24 ±0.69 | 2.54 ±0.36 | +30.70 ±0.40 | 100% |

### 1.2 gamma and leak count of the targets the attacker guesses correctly

`correct` = targets in the attacker's top-q list for their bucket; `newly_gained` = correct and not guessed by the no-bucket attacker (the part that is loss). Pooled over the 5 repeats (25,000 targets). gamma = the target's replication factor gamma(w) (HPB: always 1; |B| = 16,777,216 = in every bucket). Leak count = count of the password in A_train. `group` splits the guessed targets into head / tail.

#### M0, FSB qbar=100, q = 1: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 1489 | 1 | 1 | 1 | 1 | 2 | 8 | 16,777,216 | 146,480.1 |
| correct | all | leak_count | 1489 | 1 | 1 | 1 | 1 | 2 | 2 | 261,844 | 2,287.4 |
| correct | head | gamma | 13 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216.0 |
| correct | head | leak_count | 13 | 261,844 | 261,844 | 261,844 | 261,844 | 261,844 | 261,844 | 261,844 | 261,844.0 |
| correct | tail | gamma | 1476 | 1 | 1 | 1 | 1 | 2 | 7 | 108 | 3.4 |
| correct | tail | leak_count | 1476 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | all | gamma | 1476 | 1 | 1 | 1 | 1 | 2 | 7 | 108 | 3.4 |
| newly_gained | all | leak_count | 1476 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | tail | gamma | 1476 | 1 | 1 | 1 | 1 | 2 | 7 | 108 | 3.4 |
| newly_gained | tail | leak_count | 1476 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |

#### M0, FSB qbar=100, q = 100: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 3889 | 1 | 1 | 1 | 17 | 16,777,216 | 16,777,216 | 16,777,216 | 4,421,189.6 |
| correct | all | leak_count | 3889 | 1 | 1 | 1 | 1 | 7,103 | 53,451 | 261,844 | 21,205.6 |
| correct | head | gamma | 1030 | 2,595,624 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,692,852.2 |
| correct | head | leak_count | 1030 | 1,018 | 7,574 | 9,484 | 18,459 | 71,140 | 261,844 | 261,844 | 80,063.1 |
| correct | tail | gamma | 2859 | 1 | 1 | 1 | 2 | 40 | 302 | 4,896 | 128.9 |
| correct | tail | leak_count | 2859 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | all | gamma | 2868 | 1 | 1 | 1 | 2 | 41 | 317 | 13,006,167 | 24,498.5 |
| newly_gained | all | leak_count | 2868 | 1 | 1 | 1 | 1 | 2 | 2 | 5,101 | 10.9 |
| newly_gained | head | gamma | 9 | 2,595,624 | 3,513,526 | 5,341,682 | 8,388,608 | 10,833,798 | 11,268,272 | 13,006,167 | 7,765,907.6 |
| newly_gained | head | leak_count | 9 | 1,018 | 1,378 | 2,095 | 3,290 | 4,249 | 4,419 | 5,101 | 3,045.8 |
| newly_gained | tail | gamma | 2859 | 1 | 1 | 1 | 2 | 40 | 302 | 4,896 | 128.9 |
| newly_gained | tail | leak_count | 2859 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |

#### M0, HPB l=12 (size-matched), q = 1: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 3879 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | all | leak_count | 3879 | 74 | 438 | 903 | 2,375 | 7,103 | 53,451 | 261,844 | 22,718.1 |
| correct | head | gamma | 3879 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | head | leak_count | 3879 | 74 | 438 | 903 | 2,375 | 7,103 | 53,451 | 261,844 | 22,718.1 |
| newly_gained | all | gamma | 3637 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | all | leak_count | 3637 | 74 | 424 | 851 | 2,095 | 5,444 | 12,660 | 71,140 | 6,807.1 |
| newly_gained | head | gamma | 3637 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | head | leak_count | 3637 | 74 | 424 | 851 | 2,095 | 5,444 | 12,660 | 71,140 | 6,807.1 |

#### M0, HPB l=12 (size-matched), q = 100: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 11383 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | all | leak_count | 11383 | 4 | 11 | 28 | 139 | 1,173 | 5,534 | 261,844 | 7,847.9 |
| correct | head | gamma | 11383 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | head | leak_count | 11383 | 4 | 11 | 28 | 139 | 1,173 | 5,534 | 261,844 | 7,847.9 |
| newly_gained | all | gamma | 10225 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | all | leak_count | 10225 | 4 | 10 | 24 | 95 | 622 | 1,975 | 5,388 | 592.4 |
| newly_gained | head | gamma | 10225 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | head | leak_count | 10225 | 4 | 10 | 24 | 95 | 622 | 1,975 | 5,388 | 592.4 |

#### M2x (len>=8 + Xato), FSB qbar=100, q = 1: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 2469 | 1 | 1 | 1 | 1 | 1 | 6 | 16,777,216 | 13,594.7 |
| correct | all | leak_count | 2469 | 1 | 1 | 1 | 1 | 2 | 2 | 13,662 | 12.4 |
| correct | head | gamma | 2 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216 | 16,777,216.0 |
| correct | head | leak_count | 2 | 13,662 | 13,662 | 13,662 | 13,662 | 13,662 | 13,662 | 13,662 | 13,662.0 |
| correct | tail | gamma | 2467 | 1 | 1 | 1 | 1 | 1 | 6 | 703 | 4.4 |
| correct | tail | leak_count | 2467 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | all | gamma | 2467 | 1 | 1 | 1 | 1 | 1 | 6 | 703 | 4.4 |
| newly_gained | all | leak_count | 2467 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | tail | gamma | 2467 | 1 | 1 | 1 | 1 | 1 | 6 | 703 | 4.4 |
| newly_gained | tail | leak_count | 2467 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |

#### M2x (len>=8 + Xato), FSB qbar=100, q = 100: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 4332 | 1 | 1 | 1 | 1 | 423,255 | 7,055,100 | 16,777,216 | 1,751,400.2 |
| correct | all | leak_count | 4332 | 1 | 1 | 1 | 1 | 166 | 2,767 | 13,662 | 779.8 |
| correct | head | gamma | 1144 | 122,387 | 777,922 | 2,415,231 | 5,341,682 | 9,897,411 | 16,777,216 | 16,777,216 | 6,632,018.9 |
| correct | head | leak_count | 1144 | 48 | 305 | 947 | 2,095 | 3,882 | 6,987 | 13,662 | 2,949.4 |
| correct | tail | gamma | 3188 | 1 | 1 | 1 | 1 | 2 | 14 | 3,681 | 11.3 |
| correct | tail | leak_count | 3188 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |
| newly_gained | all | gamma | 3712 | 1 | 1 | 1 | 1 | 8 | 1,157,577 | 4,699,151 | 319,629.1 |
| newly_gained | all | leak_count | 3712 | 1 | 1 | 1 | 1 | 2 | 454 | 1,843 | 126.5 |
| newly_gained | head | gamma | 524 | 122,387 | 395,208 | 976,546 | 2,202,966 | 3,495,679 | 4,352,388 | 4,699,151 | 2,264,174.1 |
| newly_gained | head | leak_count | 524 | 48 | 155 | 383 | 864 | 1,371 | 1,707 | 1,843 | 888.0 |
| newly_gained | tail | gamma | 3188 | 1 | 1 | 1 | 1 | 2 | 14 | 3,681 | 11.3 |
| newly_gained | tail | leak_count | 3188 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1.3 |

#### M2x (len>=8 + Xato), HPB l=12 (size-matched), q = 1: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 2489 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | all | leak_count | 2489 | 29 | 145 | 273 | 703 | 1,978 | 4,190 | 13,662 | 1,624.8 |
| correct | head | gamma | 2489 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | head | leak_count | 2489 | 29 | 145 | 273 | 703 | 1,978 | 4,190 | 13,662 | 1,624.8 |
| newly_gained | all | gamma | 2460 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | all | leak_count | 2460 | 29 | 145 | 271 | 687 | 1,817 | 4,032 | 10,144 | 1,482.9 |
| newly_gained | head | gamma | 2460 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | head | leak_count | 2460 | 29 | 145 | 271 | 687 | 1,817 | 4,032 | 10,144 | 1,482.9 |

#### M2x (len>=8 + Xato), HPB l=12 (size-matched), q = 100: quantiles

| subset | group | variable | n | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | all | gamma | 8310 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | all | leak_count | 8310 | 2 | 5 | 10 | 42 | 263 | 1,360 | 13,662 | 524.4 |
| correct | head | gamma | 8306 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | head | leak_count | 8306 | 3 | 5 | 10 | 42 | 263 | 1,362 | 13,662 | 524.7 |
| correct | tail | gamma | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| correct | tail | leak_count | 4 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 2.8 |
| newly_gained | all | gamma | 7675 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | all | leak_count | 7675 | 2 | 5 | 9 | 33 | 164 | 607 | 1,843 | 184.7 |
| newly_gained | head | gamma | 7671 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | head | leak_count | 7671 | 3 | 5 | 9 | 33 | 164 | 608 | 1,843 | 184.8 |
| newly_gained | tail | gamma | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| newly_gained | tail | leak_count | 4 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 2.8 |

#### M0, FSB qbar=100, q = 1: binned shares (all guessed targets)

| variable | bin | correct n | correct % | newly_gained n | newly_gained % |
|---|---|---|---|---|---|
| gamma | 1 | 1085 | 72.9 | 1085 | 73.5 |
| gamma | 2-10 | 286 | 19.2 | 286 | 19.4 |
| gamma | 11-100 | 104 | 7.0 | 104 | 7.0 |
| gamma | 101-1k | 1 | 0.1 | 1 | 0.1 |
| gamma | 1k-10k | 0 | 0.0 | 0 | 0.0 |
| gamma | 10k-100k | 0 | 0.0 | 0 | 0.0 |
| gamma | 100k-1M | 0 | 0.0 | 0 | 0.0 |
| gamma | 1M to <|B| | 0 | 0.0 | 0 | 0.0 |
| gamma | |B| (every bucket) | 13 | 0.9 | 0 | 0.0 |
| leak_count | 0 (not in S~) | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1 | 995 | 66.8 | 995 | 67.4 |
| leak_count | 2 | 461 | 31.0 | 461 | 31.2 |
| leak_count | 3-5 | 20 | 1.3 | 20 | 1.4 |
| leak_count | 6-20 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 21-100 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 101-1k | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1k-10k | 0 | 0.0 | 0 | 0.0 |
| leak_count | >10k | 13 | 0.9 | 0 | 0.0 |

#### M0, FSB qbar=100, q = 100: binned shares (all guessed targets)

| variable | bin | correct n | correct % | newly_gained n | newly_gained % |
|---|---|---|---|---|---|
| gamma | 1 | 1311 | 33.7 | 1311 | 45.7 |
| gamma | 2-10 | 510 | 13.1 | 510 | 17.8 |
| gamma | 11-100 | 512 | 13.2 | 512 | 17.9 |
| gamma | 101-1k | 419 | 10.8 | 419 | 14.6 |
| gamma | 1k-10k | 107 | 2.8 | 107 | 3.7 |
| gamma | 10k-100k | 0 | 0.0 | 0 | 0.0 |
| gamma | 100k-1M | 0 | 0.0 | 0 | 0.0 |
| gamma | 1M to <|B| | 11 | 0.3 | 9 | 0.3 |
| gamma | |B| (every bucket) | 1019 | 26.2 | 0 | 0.0 |
| leak_count | 0 (not in S~) | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1 | 1983 | 51.0 | 1983 | 69.1 |
| leak_count | 2 | 847 | 21.8 | 847 | 29.5 |
| leak_count | 3-5 | 29 | 0.8 | 29 | 1.0 |
| leak_count | 6-20 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 21-100 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 101-1k | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1k-10k | 297 | 7.6 | 9 | 0.3 |
| leak_count | >10k | 733 | 18.9 | 0 | 0.0 |

#### M2x (len>=8 + Xato), FSB qbar=100, q = 1: binned shares (all guessed targets)

| variable | bin | correct n | correct % | newly_gained n | newly_gained % |
|---|---|---|---|---|---|
| gamma | 1 | 1918 | 77.7 | 1918 | 77.8 |
| gamma | 2-10 | 374 | 15.2 | 374 | 15.2 |
| gamma | 11-100 | 165 | 6.7 | 165 | 6.7 |
| gamma | 101-1k | 10 | 0.4 | 10 | 0.4 |
| gamma | 1k-10k | 0 | 0.0 | 0 | 0.0 |
| gamma | 10k-100k | 0 | 0.0 | 0 | 0.0 |
| gamma | 100k-1M | 0 | 0.0 | 0 | 0.0 |
| gamma | 1M to <|B| | 0 | 0.0 | 0 | 0.0 |
| gamma | |B| (every bucket) | 2 | 0.1 | 0 | 0.0 |
| leak_count | 0 (not in S~) | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1 | 1647 | 66.7 | 1647 | 66.8 |
| leak_count | 2 | 788 | 31.9 | 788 | 31.9 |
| leak_count | 3-5 | 32 | 1.3 | 32 | 1.3 |
| leak_count | 6-20 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 21-100 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 101-1k | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1k-10k | 0 | 0.0 | 0 | 0.0 |
| leak_count | >10k | 2 | 0.1 | 0 | 0.0 |

#### M2x (len>=8 + Xato), FSB qbar=100, q = 100: binned shares (all guessed targets)

| variable | bin | correct n | correct % | newly_gained n | newly_gained % |
|---|---|---|---|---|---|
| gamma | 1 | 2271 | 52.4 | 2271 | 61.2 |
| gamma | 2-10 | 552 | 12.7 | 552 | 14.9 |
| gamma | 11-100 | 303 | 7.0 | 303 | 8.2 |
| gamma | 101-1k | 59 | 1.4 | 59 | 1.6 |
| gamma | 1k-10k | 3 | 0.1 | 3 | 0.1 |
| gamma | 10k-100k | 0 | 0.0 | 0 | 0.0 |
| gamma | 100k-1M | 134 | 3.1 | 134 | 3.6 |
| gamma | 1M to <|B| | 893 | 20.6 | 390 | 10.5 |
| gamma | |B| (every bucket) | 117 | 2.7 | 0 | 0.0 |
| leak_count | 0 (not in S~) | 0 | 0.0 | 0 | 0.0 |
| leak_count | 1 | 2248 | 51.9 | 2248 | 60.6 |
| leak_count | 2 | 907 | 20.9 | 907 | 24.4 |
| leak_count | 3-5 | 33 | 0.8 | 33 | 0.9 |
| leak_count | 6-20 | 0 | 0.0 | 0 | 0.0 |
| leak_count | 21-100 | 35 | 0.8 | 35 | 0.9 |
| leak_count | 101-1k | 267 | 6.2 | 267 | 7.2 |
| leak_count | 1k-10k | 781 | 18.0 | 222 | 6.0 |
| leak_count | >10k | 61 | 1.4 | 0 | 0.0 |

## 2. Tail-only noise (M3 variant), est attacker, FSB qbar = 100, t = 1,000,000

`tailnoise`: p^ is multiplied by exp(sigma z_w) only for strings **outside the histogram head** (the top 1M passwords of A_train); head strings keep p^ exactly. `fullnoise`: the same draws with the noise on every string (the Phase 1c/1d M3). 5 independent draws (salts `c3sim-noise-v1-d1..d5`, as Phase 1d); loss at q = qbar = 100, mean ± sd across the 5 draws (each draw averages 5 repeats of 5,000 targets). est attacker with the 2M list, as in Phase 1d. sigma = 1.6 is new for the full-noise curve (Phase 1d stops at 1.5). sigma = 0 is M0: loss 0.00.

| sigma | tailnoise loss@100 | tailnoise avg_bucket | fullnoise loss@100 | fullnoise avg_bucket | tail-only / full |
|---|---|---|---|---|---|
| 0.5 | -0.04 ± 0.02 | 2528 | +2.63 ± 0.26 | 2499 | -0.016 |
| 1.0 | +0.28 ± 0.04 | 2449 | +9.77 ± 0.45 | 2103 | 0.029 |
| 1.6 | +0.89 ± 0.14 | 2149 | +23.20 ± 0.28 | 1583 | 0.038 |

Loss at q = 1, 10, 100, 1000 for the same rows (mean over the 5 draws):

| noise | sigma | loss@1 | loss@10 | loss@100 | loss@1000 |
|---|---|---|---|---|---|
| tailnoise | 0.5 | +0.00 ± 0.00 | +0.02 ± 0.01 | -0.04 ± 0.02 | +13.52 ± 0.41 |
| tailnoise | 1.0 | -0.00 ± 0.00 | +0.23 ± 0.03 | +0.28 ± 0.04 | +15.34 ± 0.82 |
| tailnoise | 1.6 | -0.01 ± 0.01 | +0.40 ± 0.04 | +0.89 ± 0.14 | +21.89 ± 1.21 |
| fullnoise | 0.5 | +0.00 ± 0.00 | +0.35 ± 0.03 | +2.63 ± 0.26 | +21.58 ± 0.89 |
| fullnoise | 1.0 | -0.01 ± 0.02 | +1.78 ± 0.10 | +9.77 ± 0.45 | +33.21 ± 0.60 |
| fullnoise | 1.6 | +1.33 ± 0.12 | +7.69 ± 0.22 | +23.20 ± 0.28 | +40.99 ± 0.24 |

Per-draw loss at q = 100:

| noise | sigma | d1 | d2 | d3 | d4 | d5 |
|---|---|---|---|---|---|---|
| tailnoise | 0.5 | -0.02 | -0.06 | -0.04 | -0.04 | -0.04 |
| tailnoise | 1.0 | +0.24 | +0.26 | +0.35 | +0.28 | +0.26 |
| tailnoise | 1.6 | +0.84 | +0.92 | +1.09 | +0.89 | +0.70 |
| fullnoise | 0.5 | +3.00 | +2.26 | +2.57 | +2.68 | +2.66 |
| fullnoise | 1.0 | +10.05 | +9.24 | +9.33 | +10.19 | +10.06 |
| fullnoise | 1.6 | +23.06 | +22.85 | +23.12 | +23.51 | +23.44 |

Phase 1d full-noise curve for reference (est, qbar = 100, q = 100, 5 draws; `e1d_noise.csv`): sigma 0.5: +2.63 ± 0.26; sigma 0.75: +5.71 ± 0.36; sigma 1.0: +9.77 ± 0.45; sigma 1.5: +20.69 ± 0.21.

Measured estimator error at t = 1M (REPORT_1d section 3, `e1d_esterror_summary.csv`): tail, per-password dispersion (method B) sigma_hat = 1.570 (se over folds 0.004, bias mu = +5.86); tail, binned masses (method A) 0.918; head, method B 0.308, method A 0.114. The tail-only sigma = 1.6 row is the one closest to the measured tail sigma_hat (1.57).

### 2.1 Extra (not requested): the same experiment with the emp attacker (all of S~)

Same draws, same salts, qbar = 100, q = 100, emp attacker with all of S~ (the clean-estimate loss, sigma = 0, is +10.92; `e1e_headline.csv`).

| sigma | tailnoise loss@100 | fullnoise loss@100 |
|---|---|---|
| 0.5 | +10.88 ± 0.02 | +12.92 ± 0.28 |
| 1.0 | +10.84 ± 0.08 | +19.60 ± 0.41 |
| 1.6 | +10.94 ± 0.05 | +33.03 ± 0.33 |

## 3. Checks and runtimes

```
....                                                                     [100%]
4 passed in 2.73s
```

Wall times (10-core laptop): mechanism: 0 min 30 s; tailnoise: 8 min 29 s; tailnoise_emp: 15 min 8 s.

## 4. New files

`results/`: e1f_mech_groups.csv, e1f_mech_dist.csv, e1f_mech_quantiles.csv, e1f_tailnoise.csv, e1f_tailnoise_emp.csv (extra), logs, time files, e1f_tests.txt, this report. `e1f_tailnoise*.csv` columns as in the e1d / e1e CSVs; `e1f_mech_*.csv` have their own columns (see headers).
