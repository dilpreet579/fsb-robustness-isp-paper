# REPORT 1d (Phase 1d)

Numbers and method statements only. Phase 1 / 1b / 1c results were not modified. New files: `results/e1d_*`, `experiments/e1d_*.py`, `experiments/report1d.py`, `c3sim/esterror.py`, `tests/test_phase1d.py`; additive edits to `experiments/common.py` (noise salts, M2L/M2B conditions, per-repeat success values). All runs at t = 1,000,000 (the primary setting) unless a t is stated, seed 2000, pool A_test (M1b: B_target), 5 repeats x 5,000 targets, units percent / percentage points, ± = sd over the repeats unless stated. `est` = attacker weights p^ (deployed estimate), `emp` = leak counts.

## 1. Attacker candidate-list cap (emp attacker, FSB qbar = 100)

Ran: candidate lists of 2M, 4M, 6M and all of S~ (13,125,513; an extra, it fit in memory as in Phase 1) at t = 1M and t = 3M, conditions M0 and M2x (Xato list). Same targets in every cell. Loss at q = 1, 10, 100 (q = 1000 is in the CSV).

| t | condition | candidates | avg_bucket | cand_per_bucket | base@1 | base@10 | base@100 | loss@1 | loss@10 | loss@100 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000,000 | M0 | 2M | 2565 | 2388 | 0.97 | 2.15 | 4.63 | +1.64 ±0.28 | +2.49 ±0.19 | +2.94 ±0.25 |
| 1,000,000 | M0 | 4M | 2565 | 2433 | 0.97 | 2.15 | 4.63 | +2.48 ±0.23 | +3.92 ±0.22 | +4.56 ±0.30 |
| 1,000,000 | M0 | 6M | 2565 | 2454 | 0.97 | 2.15 | 4.63 | +3.00 ±0.18 | +4.93 ±0.35 | +5.77 ±0.38 |
| 1,000,000 | M0 | all (13.1M) | 2565 | 2565 | 0.97 | 2.15 | 4.63 | +4.99 ±0.30 | +9.29 ±0.26 | +10.92 ±0.35 |
| 1,000,000 | M2x | 2M | 2565 | 819 | 0.12 | 0.60 | 2.54 | +4.30 ±0.23 | +4.59 ±0.24 | +6.63 ±0.39 |
| 1,000,000 | M2x | 4M | 2565 | 820 | 0.12 | 0.60 | 2.54 | +5.83 ±0.26 | +6.54 ±0.31 | +8.58 ±0.51 |
| 1,000,000 | M2x | 6M | 2565 | 820 | 0.12 | 0.60 | 2.54 | +7.68 ±0.28 | +9.22 ±0.44 | +11.28 ±0.64 |
| 1,000,000 | M2x | all (13.1M) | 2565 | 821 | 0.12 | 0.60 | 2.54 | +9.76 ±0.39 | +12.72 ±0.50 | +14.79 ±0.69 |
| 3,000,000 | M0 | 2M | 3262 | 2920 | 0.97 | 2.15 | 4.63 | +0.00 ±0.00 | +0.00 ±0.00 | +0.04 ±0.03 |
| 3,000,000 | M0 | 4M | 3262 | 3145 | 0.97 | 2.15 | 4.63 | +0.26 ±0.17 | +0.61 ±0.10 | +0.75 ±0.10 |
| 3,000,000 | M0 | 6M | 3262 | 3163 | 0.97 | 2.15 | 4.63 | +0.83 ±0.25 | +1.71 ±0.37 | +1.97 ±0.35 |
| 3,000,000 | M0 | all (13.1M) | 3262 | 3263 | 0.97 | 2.15 | 4.63 | +3.18 ±0.12 | +6.34 ±0.24 | +7.23 ±0.27 |
| 3,000,000 | M2x | 2M | 3262 | 1263 | 0.12 | 0.60 | 2.54 | +0.09 ±0.05 | +0.16 ±0.06 | +1.96 ±0.27 |
| 3,000,000 | M2x | 4M | 3262 | 1263 | 0.12 | 0.60 | 2.54 | +1.88 ±0.15 | +2.10 ±0.18 | +3.90 ±0.32 |
| 3,000,000 | M2x | 6M | 3262 | 1264 | 0.12 | 0.60 | 2.54 | +4.05 ±0.21 | +4.79 ±0.27 | +6.58 ±0.46 |
| 3,000,000 | M2x | all (13.1M) | 3262 | 1264 | 0.12 | 0.60 | 2.54 | +6.49 ±0.15 | +8.28 ±0.39 | +10.10 ±0.48 |

Change in loss relative to the 2M list:

| t | condition | candidates | change vs 2M @q=1 | change vs 2M @q=10 | change vs 2M @q=100 |
|---|---|---|---|---|---|
| 1,000,000 | M0 | 4M | +0.84 | +1.42 | +1.62 |
| 1,000,000 | M0 | 6M | +1.35 | +2.44 | +2.83 |
| 1,000,000 | M0 | all | +3.34 | +6.80 | +7.99 |
| 1,000,000 | M2x | 4M | +1.53 | +1.94 | +1.95 |
| 1,000,000 | M2x | 6M | +3.38 | +4.63 | +4.65 |
| 1,000,000 | M2x | all | +5.46 | +8.13 | +8.16 |
| 3,000,000 | M0 | 4M | +0.26 | +0.61 | +0.72 |
| 3,000,000 | M0 | 6M | +0.83 | +1.71 | +1.94 |
| 3,000,000 | M0 | all | +3.18 | +6.34 | +7.19 |
| 3,000,000 | M2x | 4M | +1.79 | +1.94 | +1.93 |
| 3,000,000 | M2x | 6M | +3.96 | +4.63 | +4.62 |
| 3,000,000 | M2x | all | +6.40 | +8.12 | +8.14 |

## 2. M3 with 5 independent noise draws (t = 1,000,000)

Draw k uses salt `c3sim-noise-v1-d{k}` (k = 1..5) in the salted SHA-256 that defines z_w (the Phase 1c draw is salt `c3sim-noise-v1`, not included here). sigma in {0.5, 0.75, 1.0} as requested, plus 1.5 as a fallback anchor. `loss` = loss at q = qbar. sigma = 0 is the noise-free M0 row of `e1c_e2.csv` (same targets). Per draw, the loss at each sigma is the mean over the 5 target repeats; the crossing of 5 points is linear interpolation along sigma in {0, 0.5, 0.75, 1.0, 1.5}; reported as mean ± sd across the 5 draws (sd with ddof = 1).

Loss at q = qbar, mean ± sd across the 5 noise draws:

| attacker | qbar | sigma=0 (M0) | sigma=0.5 | sigma=0.75 | sigma=1.0 | sigma=1.5 |
|---|---|---|---|---|---|---|
| est | 10 | +0.00 | +1.56 ± 0.20 | +3.54 ± 0.59 | +6.60 ± 0.86 | +17.50 ± 0.85 |
| est | 100 | +0.00 | +2.63 ± 0.26 | +5.71 ± 0.36 | +9.77 ± 0.45 | +20.69 ± 0.21 |
| est | 1000 | +0.00 | +3.00 ± 0.11 | +6.18 ± 0.20 | +10.22 ± 0.23 | +20.41 ± 0.33 |
| emp | 10 | +2.79 | +3.95 ± 0.20 | +5.92 ± 0.65 | +8.97 ± 0.87 | +19.90 ± 0.86 |
| emp | 100 | +2.94 | +5.27 ± 0.28 | +8.23 ± 0.35 | +12.10 ± 0.40 | +22.87 ± 0.21 |
| emp | 1000 | +2.84 | +5.77 ± 0.14 | +8.91 ± 0.21 | +12.87 ± 0.24 | +22.61 ± 0.30 |

Sigma at which the loss at q = qbar reaches 5 points:

| attacker | qbar | crossing_mean_sd | per_draw_crossings |
|---|---|---|---|
| est | 10 | 0.874 ± 0.059 | 0.940, 0.878, 0.913, 0.851, 0.788 |
| est | 100 | 0.693 ± 0.027 | 0.661, 0.731, 0.708, 0.687, 0.677 |
| est | 1000 | 0.658 ± 0.013 | 0.653, 0.665, 0.675, 0.651, 0.643 |
| emp | 10 | 0.642 ± 0.050 | 0.707, 0.665, 0.638, 0.630, 0.571 |
| emp | 100 | 0.442 ± 0.047 | 0.383, 0.513, 0.451, 0.435, 0.429 |
| emp | 1000 | 0.370 ± 0.017 | 0.361, 0.384, 0.392, 0.357, 0.354 |

For reference, Phase 1c (single noise draw, sigma grid 0, .25, .5, .75, 1, 1.5), crossing of the mean curve:

| attacker | qbar | phase1c_draw0_curve_crossing |
|---|---|---|
| est | 10 | 0.99 |
| est | 100 | 0.76 |
| est | 1000 | 0.67 |
| emp | 10 | 0.78 |
| emp | 100 | 0.51 |
| emp | 1000 | 0.44 |

## 3. Estimator error sigma_hat = sd of log(p^ / true probability) on held-out A_dev

Held-out data: A_dev (1,631,475 accounts; 62.7% of them have a password stored in A_train). p^ is the estimate trained on all of A_train at the stated t. `head` = the top-t passwords of A_train (p^ = train frequency), `tail` = the rest (p^ from the 3-gram). Bins: 0.5 decade of p^. Neither method takes log(count / n) per password, so Poisson noise at tiny counts does not enter:

- **B, per-password dispersion** (the quantity M3's sigma stands for). Population: the passwords stored in S~ (so it is conditional on being leaked). In a bin, held-out count c_i ~ Poisson(m_i e^{u_i}), m_i = n_dev p^_i, u_i iid with variance sigma^2. With x_i = c_i / m_i, Var[x] = E[x] mean(1/m) + (e^{sigma^2} - 1) E[x]^2, so sigma^2 = log(1 + (s^2 - xbar mean(1/m)) / xbar^2) (0 if the numerator is not positive); the first term is the Poisson variance and is subtracted. Bias mu = log(xbar) - sigma^2/2 = log(true / p^) of the bin (positive: p^ too small). Bins need >= 100 passwords and >= 50 held-out accounts. Group sigma_hat = sqrt of the password-weighted mean of sigma^2 (`sigma_hat`) or of the account-weighted mean (`sigma_hat_alt`). `se_over_folds`: A_dev's counts split into 5 folds, sigma_hat recomputed on each, sd / sqrt(5). Validated on simulated data in `tests/test_phase1d.py` (true sigma 0 / 0.5 / 1.0 recovered as 0.000 / 0.498 / 0.997; naive sd of log(c/m) at sigma = 0 is 0.60).
- **A, binned masses over all strings** (calibration-style). Per bin: held-out mass vs the model's mass (head: exact sum of p^; tail: 3-gram mass by sampling 20M strings, head strings excluded by hash). lr = log(held-out mass / model mass), bins with >= 100 held-out accounts; sigma_hat = sqrt(account-weighted mean of max(lr^2 - 1/N_b, 0)) (Poisson variance of lr subtracted); `sigma_hat_alt` is the raw RMS. It measures scale error by p^ bin, not scatter inside a bin, so it is a lower bound on B. `bias_mu` = weighted mean lr.

| t | group | method | sigma_hat | sigma_hat_alt | alt_meaning | se_over_folds | bias_mu | bins_used | n_used |
|---|---|---|---|---|---|---|---|---|---|
| 100000 | head | B per-password dispersion (stored passwords) | 0.1641 | 0.1047 | mass-weighted | 0.0285 | -0.0166 | 6 | 99966.0 |
| 100000 | tail | B per-password dispersion (stored passwords) | 1.6337 | 1.4886 | mass-weighted | 0.0013 | 4.9026 | 41 | 12939105.0 |
| 100000 | head | A binned masses (all strings) | 0.0154 | 0.0156 | raw (not Poisson-corrected) | nan | -0.0097 | 9 | 593029.0 |
| 100000 | tail | A binned masses (all strings) | 0.8814 | 0.8814 | raw (not Poisson-corrected) | nan | 0.6304 | 56 | 1037606.0 |
| 1000000 | head | B per-password dispersion (stored passwords) | 0.3081 | 0.1907 | mass-weighted | 0.0118 | -0.0933 | 7 | 999966.0 |
| 1000000 | tail | B per-password dispersion (stored passwords) | 1.5698 | 1.4782 | mass-weighted | 0.0037 | 5.8619 | 39 | 12025064.0 |
| 1000000 | head | A binned masses (all strings) | 0.1143 | 0.1143 | raw (not Poisson-corrected) | nan | -0.0612 | 10 | 832251.0 |
| 1000000 | tail | A binned masses (all strings) | 0.9182 | 0.9182 | raw (not Poisson-corrected) | nan | 0.6826 | 55 | 798404.0 |

Bins used, method B, head, t = 1,000,000 (7 bins; all bins and t = 100,000 in `e1d_esterror_bins.csv`):

| bin_log10_p_lo | passwords | heldout_accounts | xbar | mu | sigma |
|---|---|---|---|---|---|
| -7.0 | 768773.0 | 145281.0 | 0.731 | -0.367 | 0.329 |
| -6.5 | 162025.0 | 134955.0 | 0.937 | -0.097 | 0.253 |
| -6.0 | 51234.0 | 136807.0 | 0.974 | -0.038 | 0.156 |
| -5.5 | 13017.0 | 109961.0 | 0.99 | -0.012 | 0.07 |
| -5.0 | 3561.0 | 97947.0 | 0.999 | -0.002 | 0.038 |
| -4.5 | 1103.0 | 93136.0 | 1.001 | 0.001 | 0.035 |
| -4.0 | 253.0 | 65360.0 | 1.001 | 0.001 | 0.016 |

Bins used, method B, tail, t = 1,000,000 (39 bins; all bins and t = 100,000 in `e1d_esterror_bins.csv`):

| bin_log10_p_lo | passwords | heldout_accounts | xbar | mu | sigma |
|---|---|---|---|---|---|
| -24.5 | 16177.0 | 61.0 | 4199700361295200.5 | 34.331 | 1.812 |
| -24.0 | 18874.0 | 70.0 | 1273346627081398.8 | 33.23 | 1.761 |
| -23.5 | 22414.0 | 91.0 | 459105026377579.7 | 32.144 | 1.798 |
| -23.0 | 27320.0 | 117.0 | 143481348516553.8 | 31.37 | 1.567 |
| -22.5 | 33039.0 | 166.0 | 55927726395954.84 | 29.996 | 1.822 |
| -22.0 | 39748.0 | 159.0 | 14737709064870.025 | 28.514 | 1.901 |
| -21.5 | 46777.0 | 202.0 | 4803288395393.024 | 27.528 | 1.829 |
| -21.0 | 55325.0 | 231.0 | 1498402244597.208 | 26.316 | 1.855 |
| -20.5 | 64959.0 | 366.0 | 636925284681.099 | 25.559 | 1.801 |
| -20.0 | 75662.0 | 376.0 | 179466619017.042 | 24.211 | 1.845 |
| -19.5 | 87431.0 | 478.0 | 62450232609.881 | 23.18 | 1.832 |
| -19.0 | 102257.0 | 550.0 | 18639476553.104 | 22.253 | 1.671 |
| -18.5 | 119137.0 | 712.0 | 6697538225.903 | 21.032 | 1.785 |
| -18.0 | 138795.0 | 815.0 | 2071138783.752 | 19.975 | 1.718 |
| -17.5 | 161550.0 | 965.0 | 667284497.511 | 18.73 | 1.782 |
| -17.0 | 192423.0 | 1293.0 | 236911869.165 | 17.757 | 1.747 |
| -16.5 | 229825.0 | 1538.0 | 75954722.401 | 16.588 | 1.765 |
| -16.0 | 274869.0 | 1995.0 | 25844940.598 | 15.575 | 1.728 |
| -15.5 | 327699.0 | 2464.0 | 8348368.362 | 14.544 | 1.669 |
| -15.0 | 390736.0 | 3258.0 | 2932018.135 | 13.484 | 1.677 |
| -14.5 | 471939.0 | 4289.0 | 1017284.693 | 12.394 | 1.696 |
| -14.0 | 570197.0 | 5579.0 | 349406.648 | 11.342 | 1.686 |
| -13.5 | 669913.0 | 6971.0 | 116984.386 | 10.285 | 1.664 |
| -13.0 | 807922.0 | 8868.0 | 39053.143 | 9.232 | 1.638 |
| -12.5 | 926971.0 | 11063.0 | 13469.021 | 8.232 | 1.598 |
| -12.0 | 952459.0 | 12715.0 | 4786.553 | 7.241 | 1.57 |
| -11.5 | 948368.0 | 14497.0 | 1736.107 | 6.294 | 1.527 |
| -11.0 | 915070.0 | 15823.0 | 625.125 | 5.282 | 1.52 |
| -10.5 | 899184.0 | 17210.0 | 217.735 | 4.282 | 1.484 |
| -10.0 | 797139.0 | 17434.0 | 80.029 | 3.369 | 1.423 |
| -9.5 | 613404.0 | 16632.0 | 31.442 | 2.532 | 1.353 |
| -9.0 | 476479.0 | 15917.0 | 12.292 | 1.667 | 1.298 |
| -8.5 | 301558.0 | 13101.0 | 5.184 | 0.978 | 1.156 |
| -8.0 | 146706.0 | 7537.0 | 1.982 | -0.032 | 1.197 |
| -7.5 | 64512.0 | 3756.0 | 0.717 | -0.954 | 1.115 |
| -7.0 | 25165.0 | 1806.0 | 0.284 | -1.792 | 1.034 |
| -6.5 | 9330.0 | 672.0 | 0.09 | -2.88 | 0.971 |
| -6.0 | 2748.0 | 212.0 | 0.031 | -4.073 | 1.106 |
| -5.5 | 983.0 | 80.0 | 0.01 | -5.074 | 0.996 |

Bins used, method A, head, t = 1,000,000 (10 bins; all bins and t = 100,000 in `e1d_esterror_bins.csv`):

| bin_log10_p_lo | heldout_accounts | model_accounts | log_ratio |
|---|---|---|---|
| -7.0 | 145281.0 | 189668.6 | -0.267 |
| -6.5 | 134955.0 | 143080.6 | -0.058 |
| -6.0 | 136807.0 | 140243.6 | -0.025 |
| -5.5 | 109961.0 | 110841.3 | -0.008 |
| -5.0 | 97947.0 | 98007.6 | -0.001 |
| -4.5 | 93136.0 | 93017.7 | 0.001 |
| -4.0 | 65360.0 | 65407.9 | -0.001 |
| -3.5 | 19296.0 | 19340.1 | -0.002 |
| -3.0 | 15030.0 | 14936.1 | 0.006 |
| -2.5 | 14478.0 | 14569.7 | -0.006 |

Bins used, method A, tail, t = 1,000,000 (55 bins; all bins and t = 100,000 in `e1d_esterror_bins.csv`):

| bin_log10_p_lo | heldout_accounts | model_accounts | log_ratio |
|---|---|---|---|
| -32.5 | 122.0 | 1017.8 | -2.121 |
| -32.0 | 115.0 | 1062.9 | -2.224 |
| -31.5 | 126.0 | 1132.8 | -2.196 |
| -31.0 | 152.0 | 1191.8 | -2.059 |
| -30.5 | 192.0 | 1286.1 | -1.902 |
| -30.0 | 209.0 | 1383.5 | -1.89 |
| -29.5 | 233.0 | 1475.2 | -1.846 |
| -29.0 | 271.0 | 1592.6 | -1.771 |
| -28.5 | 299.0 | 1708.1 | -1.743 |
| -28.0 | 374.0 | 1818.4 | -1.581 |
| -27.5 | 393.0 | 1976.1 | -1.615 |
| -27.0 | 499.0 | 2122.8 | -1.448 |
| -26.5 | 546.0 | 2300.6 | -1.438 |
| -26.0 | 572.0 | 2487.4 | -1.47 |
| -25.5 | 722.0 | 2677.8 | -1.311 |
| -25.0 | 839.0 | 2891.1 | -1.237 |
| -24.5 | 960.0 | 3107.8 | -1.175 |
| -24.0 | 1107.0 | 3318.6 | -1.098 |
| -23.5 | 1399.0 | 3599.4 | -0.945 |
| -23.0 | 1636.0 | 3893.0 | -0.867 |
| -22.5 | 1990.0 | 4183.3 | -0.743 |
| -22.0 | 2333.0 | 4482.2 | -0.653 |
| -21.5 | 2839.0 | 4862.6 | -0.538 |
| -21.0 | 3204.0 | 5220.5 | -0.488 |
| -20.5 | 3819.0 | 5629.6 | -0.388 |
| -20.0 | 4499.0 | 6052.0 | -0.297 |
| -19.5 | 5203.0 | 6474.7 | -0.219 |
| -19.0 | 5885.0 | 7004.8 | -0.174 |
| -18.5 | 7151.0 | 7546.1 | -0.054 |
| -18.0 | 8223.0 | 8108.5 | 0.014 |
| -17.5 | 9454.0 | 8743.2 | 0.078 |
| -17.0 | 11420.0 | 9396.5 | 0.195 |
| -16.5 | 13681.0 | 10050.7 | 0.308 |
| -16.0 | 16328.0 | 10832.5 | 0.41 |
| -15.5 | 19626.0 | 11644.4 | 0.522 |
| -15.0 | 23612.0 | 12520.1 | 0.634 |
| -14.5 | 28969.0 | 13400.6 | 0.771 |
| -14.0 | 34806.0 | 14371.8 | 0.885 |
| -13.5 | 41624.0 | 15458.7 | 0.991 |
| -13.0 | 50141.0 | 16556.8 | 1.108 |
| -12.5 | 58500.0 | 17732.6 | 1.194 |
| -12.0 | 60987.0 | 18990.7 | 1.167 |
| -11.5 | 62287.0 | 20245.3 | 1.124 |
| -11.0 | 61048.0 | 21726.8 | 1.033 |
| -10.5 | 61490.0 | 23140.2 | 0.977 |
| -10.0 | 55830.0 | 24682.8 | 0.816 |
| -9.5 | 45330.0 | 26107.6 | 0.552 |
| -9.0 | 37289.0 | 27771.0 | 0.295 |
| -8.5 | 26037.0 | 28696.3 | -0.097 |
| -8.0 | 13502.0 | 29106.6 | -0.768 |
| -7.5 | 6355.0 | 29123.1 | -1.522 |
| -7.0 | 2743.0 | 28548.9 | -2.343 |
| -6.5 | 1024.0 | 29601.3 | -3.364 |
| -6.0 | 300.0 | 28660.5 | -4.559 |
| -5.5 | 109.0 | 30484.3 | -5.634 |

## 4. M2 ablation (t = 1,000,000)

Targets and the attacker's candidate list are restricted to passwords that satisfy the policy; the server's estimate and buckets are unchanged. Blocklist = first 370 lines of the Xato list (D14). Loss at q = qbar; baseline = the same attacker's no-bucket success at q = qbar.

| policy | qbar | est loss@qbar | est baseline@qbar | emp loss@qbar | emp baseline@qbar | avg_bucket |
|---|---|---|---|---|---|---|
| length >= 8 only | 10 | +0.38 ±0.10 | 1.93 | +4.60 ±0.32 | 1.93 | 790 |
| length >= 8 only | 100 | +1.66 ±0.03 | 4.45 | +5.92 ±0.30 | 4.45 | 2565 |
| length >= 8 only | 1000 | +3.58 ±0.12 | 9.28 | +7.82 ±0.29 | 9.28 | 11336 |
| Xato blocklist only | 10 | +0.11 ±0.05 | 0.16 | +3.43 ±0.36 | 0.50 | 790 |
| Xato blocklist only | 100 | +0.52 ±0.20 | 1.34 | +3.93 ±0.31 | 1.96 | 2565 |
| Xato blocklist only | 1000 | -0.06 ±0.14 | 6.59 | +3.31 ±0.33 | 7.16 | 11336 |
| both (M2x) | 10 | +0.96 ±0.09 | 0.60 | +5.47 ±0.19 | 0.60 | 790 |
| both (M2x) | 100 | +2.10 ±0.24 | 2.54 | +6.63 ±0.39 | 2.54 | 2565 |
| both (M2x) | 1000 | +3.89 ±0.23 | 7.05 | +8.42 ±0.22 | 7.05 | 11336 |

## 5. Success ratio (attacker success / baseline success) at q = 1 and q = qbar

ratio = mean bucket success / mean baseline success over the 5 repeats; ± = sd of the per-repeat ratios (n/a if some repeat has baseline 0). Rows: FSB and size-matched HPB (`scheme`, `qbar` = the FSB qbar the HPB row is matched to); conditions M0, M1b, M2x. Baseline success at q = 1 is small (M0 about 1%, M2x about 0.1%), so ratios at q = 1 are noisy.

### attacker `est`

| condition | scheme | qbar | q | avg_bucket | baseline | attacker_success | ratio | loss |
|---|---|---|---|---|---|---|---|---|
| M0 | fsb | 10 | 1 | 790.21 | 0.97 | 0.97 | 1.00 ±0.00 | 0.0 |
| M0 | fsb | 10 | 10 | 790.21 | 1.85 | 1.85 | 1.00 ±0.00 | 0.0 |
| M0 | hpb | 10 | 1 | 801.12 | 0.97 | 21.65 | 22.37 ±4.65 | 20.684 |
| M0 | hpb | 10 | 10 | 801.12 | 1.85 | 38.84 | 20.97 ±2.88 | 36.988 |
| M0 | fsb | 100 | 1 | 2564.83 | 0.97 | 0.97 | 1.00 ±0.00 | 0.0 |
| M0 | fsb | 100 | 100 | 2564.83 | 4.16 | 4.16 | 1.00 ±0.00 | 0.0 |
| M0 | hpb | 100 | 1 | 3204.47 | 0.97 | 15.06 | 15.55 ±2.96 | 14.088 |
| M0 | hpb | 100 | 100 | 3204.47 | 4.16 | 45.22 | 10.87 ±1.12 | 41.06 |
| M0 | fsb | 1000 | 1 | 11335.85 | 0.97 | 0.97 | 1.00 ±0.00 | 0.0 |
| M0 | fsb | 1000 | 1000 | 11335.85 | 10.69 | 10.69 | 1.00 ±0.00 | 0.0 |
| M0 | hpb | 1000 | 1 | 12817.88 | 0.97 | 9.33 | 9.64 ±1.80 | 8.36 |
| M0 | hpb | 1000 | 1000 | 12817.88 | 10.69 | 50.87 | 4.76 ±0.28 | 40.18 |
| M1b | fsb | 10 | 1 | 790.21 | 1.16 | 1.16 | 1.00 ±0.00 | 0.0 |
| M1b | fsb | 10 | 10 | 790.21 | 1.88 | 1.88 | 1.00 ±0.00 | 0.0 |
| M1b | hpb | 10 | 1 | 801.12 | 1.16 | 18.56 | 16.00 ±3.45 | 17.404 |
| M1b | hpb | 10 | 10 | 801.12 | 1.88 | 33.36 | 17.78 ±3.22 | 31.48 |
| M1b | fsb | 100 | 1 | 2564.83 | 1.16 | 1.16 | 1.00 ±0.00 | 0.0 |
| M1b | fsb | 100 | 100 | 2564.83 | 3.57 | 3.57 | 1.00 ±0.00 | 0.0 |
| M1b | hpb | 100 | 1 | 3204.47 | 1.16 | 12.17 | 10.49 ±2.03 | 11.008 |
| M1b | hpb | 100 | 100 | 3204.47 | 3.57 | 39.31 | 11.00 ±1.55 | 35.736 |
| M1b | fsb | 1000 | 1 | 11335.85 | 1.16 | 1.16 | 1.00 ±0.00 | 0.0 |
| M1b | fsb | 1000 | 1000 | 11335.85 | 8.17 | 8.17 | 1.00 ±0.00 | 0.0 |
| M1b | hpb | 1000 | 1 | 12817.88 | 1.16 | 7.21 | 6.22 ±1.08 | 6.052 |
| M1b | hpb | 1000 | 1000 | 12817.88 | 8.17 | 44.29 | 5.42 ±0.24 | 36.12 |
| M2x | fsb | 10 | 1 | 790.21 | 0.12 | 0.13 | 1.10 ±0.28 | 0.012 |
| M2x | fsb | 10 | 10 | 790.21 | 0.60 | 1.56 | 2.59 ±0.31 | 0.956 |
| M2x | hpb | 10 | 1 | 801.12 | 0.12 | 14.94 | 128.76 ±34.86 | 14.82 |
| M2x | hpb | 10 | 10 | 801.12 | 0.60 | 28.42 | 47.37 ±8.57 | 27.824 |
| M2x | fsb | 100 | 1 | 2564.83 | 0.12 | 0.12 | 1.00 ±0.00 | 0.0 |
| M2x | fsb | 100 | 100 | 2564.83 | 2.54 | 4.64 | 1.83 ±0.20 | 2.096 |
| M2x | hpb | 100 | 1 | 3204.47 | 0.12 | 9.96 | 85.83 ±21.34 | 9.84 |
| M2x | hpb | 100 | 100 | 3204.47 | 2.54 | 33.24 | 13.09 ±1.76 | 30.696 |
| M2x | fsb | 1000 | 1 | 11335.85 | 0.12 | 0.12 | 1.00 ±0.00 | 0.0 |
| M2x | fsb | 1000 | 1000 | 11335.85 | 7.05 | 10.94 | 1.55 ±0.04 | 3.888 |
| M2x | hpb | 1000 | 1 | 12817.88 | 0.12 | 6.17 | 53.21 ±11.25 | 6.056 |
| M2x | hpb | 1000 | 1000 | 12817.88 | 7.05 | 35.86 | 5.08 ±0.27 | 28.804 |

### attacker `emp`

| condition | scheme | qbar | q | avg_bucket | baseline | attacker_success | ratio | loss |
|---|---|---|---|---|---|---|---|---|
| M0 | fsb | 10 | 1 | 790.21 | 0.97 | 2.97 | 3.07 ±0.60 | 2.0 |
| M0 | fsb | 10 | 10 | 790.21 | 2.15 | 4.94 | 2.30 ±0.21 | 2.792 |
| M0 | hpb | 10 | 1 | 801.12 | 0.97 | 22.07 | 22.80 ±4.77 | 21.1 |
| M0 | hpb | 10 | 10 | 801.12 | 2.15 | 39.24 | 18.23 ±2.47 | 37.088 |
| M0 | fsb | 100 | 1 | 2564.83 | 0.97 | 2.61 | 2.70 ±0.54 | 1.644 |
| M0 | fsb | 100 | 100 | 2564.83 | 4.63 | 7.57 | 1.63 ±0.05 | 2.936 |
| M0 | hpb | 100 | 1 | 3204.47 | 0.97 | 15.52 | 16.03 ±3.03 | 14.548 |
| M0 | hpb | 100 | 100 | 3204.47 | 4.63 | 45.53 | 9.83 ±0.89 | 40.9 |
| M0 | fsb | 1000 | 1 | 11335.85 | 0.97 | 2.19 | 2.26 ±0.44 | 1.22 |
| M0 | fsb | 1000 | 1000 | 11335.85 | 11.23 | 14.07 | 1.25 ±0.02 | 2.84 |
| M0 | hpb | 1000 | 1 | 12817.88 | 0.97 | 9.88 | 10.21 ±1.94 | 8.912 |
| M0 | hpb | 1000 | 1000 | 12817.88 | 11.23 | 50.92 | 4.53 ±0.24 | 39.692 |
| M1b | fsb | 10 | 1 | 790.21 | 1.16 | 2.44 | 2.10 ±0.31 | 1.28 |
| M1b | fsb | 10 | 10 | 790.21 | 2.16 | 4.24 | 1.96 ±0.14 | 2.076 |
| M1b | hpb | 10 | 1 | 801.12 | 1.16 | 18.83 | 16.23 ±3.46 | 17.668 |
| M1b | hpb | 10 | 10 | 801.12 | 2.16 | 33.26 | 15.40 ±2.00 | 31.1 |
| M1b | fsb | 100 | 1 | 2564.83 | 1.16 | 2.20 | 1.90 ±0.35 | 1.04 |
| M1b | fsb | 100 | 100 | 2564.83 | 3.96 | 6.19 | 1.56 ±0.08 | 2.232 |
| M1b | hpb | 100 | 1 | 3204.47 | 1.16 | 12.68 | 10.93 ±2.16 | 11.516 |
| M1b | hpb | 100 | 100 | 3204.47 | 3.96 | 39.08 | 9.88 ±1.29 | 35.124 |
| M1b | fsb | 1000 | 1 | 11335.85 | 1.16 | 1.92 | 1.65 ±0.35 | 0.756 |
| M1b | fsb | 1000 | 1000 | 11335.85 | 8.71 | 10.94 | 1.26 ±0.01 | 2.232 |
| M1b | hpb | 1000 | 1 | 12817.88 | 1.16 | 7.90 | 6.81 ±1.23 | 6.74 |
| M1b | hpb | 1000 | 1000 | 12817.88 | 8.71 | 43.70 | 5.02 ±0.18 | 34.988 |
| M2x | fsb | 10 | 1 | 790.21 | 0.12 | 4.50 | 38.79 ±10.27 | 4.384 |
| M2x | fsb | 10 | 10 | 790.21 | 0.60 | 6.07 | 10.11 ±1.64 | 5.468 |
| M2x | hpb | 10 | 1 | 801.12 | 0.12 | 14.94 | 128.76 ±34.86 | 14.82 |
| M2x | hpb | 10 | 10 | 801.12 | 0.60 | 28.42 | 47.37 ±8.57 | 27.82 |
| M2x | fsb | 100 | 1 | 2564.83 | 0.12 | 4.42 | 38.07 ±10.29 | 4.3 |
| M2x | fsb | 100 | 100 | 2564.83 | 2.54 | 9.17 | 3.61 ±0.48 | 6.628 |
| M2x | hpb | 100 | 1 | 3204.47 | 0.12 | 9.96 | 85.83 ±21.34 | 9.84 |
| M2x | hpb | 100 | 100 | 3204.47 | 2.54 | 33.24 | 13.09 ±1.76 | 30.7 |
| M2x | fsb | 1000 | 1 | 11335.85 | 0.12 | 4.17 | 35.93 ±10.19 | 4.052 |
| M2x | fsb | 1000 | 1000 | 11335.85 | 7.05 | 15.47 | 2.19 ±0.08 | 8.416 |
| M2x | hpb | 1000 | 1 | 12817.88 | 0.12 | 6.17 | 53.21 ±11.25 | 6.056 |
| M2x | hpb | 1000 | 1000 | 12817.88 | 7.05 | 36.90 | 5.23 ±0.27 | 29.844 |

## 6. Checks and runtimes

```
[1d] true sigma 0.0: moment estimate 0.000
[1d] true sigma 0.5: moment estimate 0.498
[1d] true sigma 1.0: moment estimate 0.997
[1d] naive sd of log(c/m) at sigma=0: 0.60
..[1d] noise draws: mean +0.001, sd 0.998, corr with the original draw +0.002
.
3 passed in 0.41s
```

```
Phase 1d, 10-core laptop, 5,000 targets x 5 repeats (jobs overlapped, so times are inflated):
e1d_cap: 4 min 36 s
e1d_noise: 24 min 17 s
e1d_m2: 4 min 5 s
e1d_esterror: 57 s
```

## 7. New files

`results/`: e1d_cap.csv, e1d_noise.csv, e1d_esterror_summary.csv, e1d_esterror_bins.csv, e1d_ablation.csv, e1d_ratio.csv, logs, time files, e1d_tests.txt, this report. Columns as in e1c_*.csv; e1d_ratio.csv has its own columns (see header).
