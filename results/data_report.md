# Data report (T1)

Source: SecLists `Passwords/Leaked-Databases/` withcount files, downloaded from raw.githubusercontent.com/danielmiessler/SecLists/master (never committed; `data/` is in `.gitignore`).
Corpus A = RockYou (`rockyou-withcount.txt.tar.gz`), Corpus B = phpbb (`phpbb-withcount.txt`). honeynet, RockYou2021 and RockYou2024 are not used (plan section 3).

## Raw vs plan (checked in `results/T1_corpus_check.txt`)

| corpus | raw unique lines | raw total | plan unique | plan total | match |
|---|---|---|---|---|---|
| rockyou | 14,344,391 | 32,603,388 | 14,344,391 | 32,603,388 | True |
| phpbb | 184,388 | 255,420 | 184,388 | 255,420 | True |

Parser notes: phpbb has 1 unparsable line (count 1, empty password; dropped by the length filter) and 4 passwords that occur on two lines (`666`, `monalisa`, `b`, `ola`; counts aggregated).

## After cleaning (printable ASCII 0x20-0x7e, length 1-30, case kept, duplicates aggregated)

| pool | unique | total mass | mass/unique | singleton share of unique | top-1000 mass share |
|---|---|---|---|---|---|
| rockyou | 14,326,970 | 32,581,870 | 2.27 | 82.8% | 11.30% |
| phpbb | 184,381 | 255,417 | 1.39 | 88.6% | 12.89% |

Dropped by cleaning: rockyou 17,421 unique rows; phpbb 7 unique rows.

### Top 10, rockyou (cleaned)

| rank | password | count | share |
|---|---|---|---|
| 1 | `123456` | 290,729 | 0.8923% |
| 2 | `12345` | 79,076 | 0.2427% |
| 3 | `123456789` | 76,789 | 0.2357% |
| 4 | `password` | 59,462 | 0.1825% |
| 5 | `iloveyou` | 49,952 | 0.1533% |
| 6 | `princess` | 33,291 | 0.1022% |
| 7 | `1234567` | 21,725 | 0.0667% |
| 8 | `rockyou` | 20,901 | 0.0641% |
| 9 | `12345678` | 20,553 | 0.0631% |
| 10 | `abc123` | 16,648 | 0.0511% |

### Top 10, phpbb (cleaned)

| rank | password | count | share |
|---|---|---|---|
| 1 | `123456` | 2,650 | 1.0375% |
| 2 | `password` | 1,244 | 0.4870% |
| 3 | `phpbb` | 708 | 0.2772% |
| 4 | `qwerty` | 562 | 0.2200% |
| 5 | `12345` | 418 | 0.1637% |
| 6 | `12345678` | 371 | 0.1453% |
| 7 | `letmein` | 343 | 0.1343% |
| 8 | `111111` | 313 | 0.1225% |
| 9 | `1234` | 273 | 0.1069% |
| 10 | `123456789` | 253 | 0.0991% |

## Splits (seeds A=101, B=102, dev/fresh=103; per-password c_train ~ Binomial(c, p))

| pool | role | unique | total mass | top-1000 mass share |
|---|---|---|---|---|
| A_train | leak S~ (server), p=0.9 | 13,125,513 | 29,320,495 | 11.30% |
| A_test | matched target pool (M0, M2, M3) | 1,973,299 | 3,261,375 | 11.34% |
| A_dev | E3 tuning pool (50% of A_test accounts) | 1,066,861 | 1,631,475 | 11.35% |
| A_fresh | E3 reporting pool (other 50% of A_test) | 1,065,067 | 1,629,900 | 11.39% |
| B_attack | M1 attacker training, p=0.5 | 98,735 | 127,629 | 13.30% |
| B_target | M1 cross-corpus target pool | 99,252 | 127,788 | 13.00% |
| B_dev | E3 M1 tuning pool (50% of B_target accounts) | 52,701 | 63,991 | 13.59% |
| B_fresh | E3 M1 reporting pool (other 50%) | 52,520 | 63,797 | 13.55% |

S~ = A_train: N = 13,125,513 unique passwords, |B| = 2^24 = 16,777,216.

A_test accounts whose password is in A_train: 62.7% (of test mass); unique-test-rows in A_train: 39.1%.

Disjointness: splits are by account (the count of each password is divided between the two sides), so the *pools* share passwords but never accounts. A_train / A_test and B_attack / B_target are disjoint at the account level by construction (`c_train + c_test == c`, checked in `tests/test_data.py`). Cross-corpus: B_target accounts are never in A_train (different corpus), but passwords overlap.

B_target mass whose password is in A_train: 52.8%.

## Limitations (phpbb)

phpbb is small and mostly singletons (total/unique about 1.4). After the 50/50 split B_target holds 127,788 accounts, enough for 5,000 targets, but its tail carries no information beyond the top few thousand passwords. The M1 attacker (B_attack) only knows the passwords it has seen (98,735 unique), so its candidate list is that vocabulary, not 2,000,000 entries. Cross-corpus results mix a distribution shift (RockYou 2009 social-site users vs phpbb forum users) with attacker-vocabulary size; the two effects cannot be separated here.
