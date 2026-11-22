# Number map

Every number the paper text may quote, computed from `results/*.csv` by `experiments/paper_numbers.py` (recipes in `numbers.csv`; `paper/check_numbers.py` recomputes every row). Frozen framing: est = attacker weights p^ with the 2M list; emp = weights from leak counts with ALL of S~; t = 1M unless stated; loss = bucket success - baseline success of the same attacker, in percentage points (pp).

## C1 Reproduction (est): HPB vs FSB at matched bucket sizes (63 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C1_M0_qbar10_hpb_l` | M0: prefix length l of the size-matched HPB for qbar=10 | 14.00 | bits | `e1c_e2.csv` |
| `C1_M0_qbar10_hpb_avg` | M0: average bucket size of the matched HPB (qbar=10) | 801.12 | entries | `e1c_e2.csv` |
| `C1_M0_qbar10_fsb_avg` | M0: average bucket size of FSB qbar=10 | 790.21 | entries | `e1c_e2.csv` |
| `C1_M0_qbar10_hpb_est_loss_q1` | M0: size-matched HPB loss, est, q=1 (qbar=10) | 20.68 | pp | `e1c_e2.csv` |
| `C1_M0_qbar10_hpb_est_loss_qbar` | M0: size-matched HPB loss, est, q=10 (qbar=10) | 36.99 | pp | `e1c_e2.csv` |
| `C1_M0_qbar10_fsb_est_loss_qbar` | M0: FSB loss, est, q=qbar=10 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M0_qbar10_fsb_est_maxabs_q_le_qbar` | M0: FSB est, max |loss| over q <= qbar=10 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M0_qbar100_hpb_l` | M0: prefix length l of the size-matched HPB for qbar=100 | 12.00 | bits | `e1c_e2.csv` |
| `C1_M0_qbar100_hpb_avg` | M0: average bucket size of the matched HPB (qbar=100) | 3204.47 | entries | `e1c_e2.csv` |
| `C1_M0_qbar100_fsb_avg` | M0: average bucket size of FSB qbar=100 | 2564.83 | entries | `e1c_e2.csv` |
| `C1_M0_qbar100_hpb_est_loss_q1` | M0: size-matched HPB loss, est, q=1 (qbar=100) | 14.09 | pp | `e1c_e2.csv` |
| `C1_M0_qbar100_hpb_est_loss_qbar` | M0: size-matched HPB loss, est, q=100 (qbar=100) | 41.06 | pp | `e1c_e2.csv` |
| `C1_M0_qbar100_fsb_est_loss_qbar` | M0: FSB loss, est, q=qbar=100 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M0_qbar100_fsb_est_maxabs_q_le_qbar` | M0: FSB est, max |loss| over q <= qbar=100 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M0_qbar1000_hpb_l` | M0: prefix length l of the size-matched HPB for qbar=1000 | 10.00 | bits | `e1c_e2.csv` |
| `C1_M0_qbar1000_hpb_avg` | M0: average bucket size of the matched HPB (qbar=1000) | 12,818 | entries | `e1c_e2.csv` |
| `C1_M0_qbar1000_fsb_avg` | M0: average bucket size of FSB qbar=1000 | 11,336 | entries | `e1c_e2.csv` |
| `C1_M0_qbar1000_hpb_est_loss_q1` | M0: size-matched HPB loss, est, q=1 (qbar=1000) | 8.36 | pp | `e1c_e2.csv` |
| `C1_M0_qbar1000_hpb_est_loss_qbar` | M0: size-matched HPB loss, est, q=1000 (qbar=1000) | 40.18 | pp | `e1c_e2.csv` |
| `C1_M0_qbar1000_fsb_est_loss_qbar` | M0: FSB loss, est, q=qbar=1000 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M0_qbar1000_fsb_est_maxabs_q_le_qbar` | M0: FSB est, max |loss| over q <= qbar=1000 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar10_hpb_l` | M1b: prefix length l of the size-matched HPB for qbar=10 | 14.00 | bits | `e1c_e2.csv` |
| `C1_M1b_qbar10_hpb_avg` | M1b: average bucket size of the matched HPB (qbar=10) | 801.12 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar10_fsb_avg` | M1b: average bucket size of FSB qbar=10 | 790.21 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar10_hpb_est_loss_q1` | M1b: size-matched HPB loss, est, q=1 (qbar=10) | 17.40 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar10_hpb_est_loss_qbar` | M1b: size-matched HPB loss, est, q=10 (qbar=10) | 31.48 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar10_fsb_est_loss_qbar` | M1b: FSB loss, est, q=qbar=10 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar10_fsb_est_maxabs_q_le_qbar` | M1b: FSB est, max |loss| over q <= qbar=10 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar100_hpb_l` | M1b: prefix length l of the size-matched HPB for qbar=100 | 12.00 | bits | `e1c_e2.csv` |
| `C1_M1b_qbar100_hpb_avg` | M1b: average bucket size of the matched HPB (qbar=100) | 3204.47 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar100_fsb_avg` | M1b: average bucket size of FSB qbar=100 | 2564.83 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar100_hpb_est_loss_q1` | M1b: size-matched HPB loss, est, q=1 (qbar=100) | 11.01 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar100_hpb_est_loss_qbar` | M1b: size-matched HPB loss, est, q=100 (qbar=100) | 35.74 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar100_fsb_est_loss_qbar` | M1b: FSB loss, est, q=qbar=100 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar100_fsb_est_maxabs_q_le_qbar` | M1b: FSB est, max |loss| over q <= qbar=100 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar1000_hpb_l` | M1b: prefix length l of the size-matched HPB for qbar=1000 | 10.00 | bits | `e1c_e2.csv` |
| `C1_M1b_qbar1000_hpb_avg` | M1b: average bucket size of the matched HPB (qbar=1000) | 12,818 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar1000_fsb_avg` | M1b: average bucket size of FSB qbar=1000 | 11,336 | entries | `e1c_e2.csv` |
| `C1_M1b_qbar1000_hpb_est_loss_q1` | M1b: size-matched HPB loss, est, q=1 (qbar=1000) | 6.05 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar1000_hpb_est_loss_qbar` | M1b: size-matched HPB loss, est, q=1000 (qbar=1000) | 36.12 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar1000_fsb_est_loss_qbar` | M1b: FSB loss, est, q=qbar=1000 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M1b_qbar1000_fsb_est_maxabs_q_le_qbar` | M1b: FSB est, max |loss| over q <= qbar=1000 | 0.00 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar10_hpb_l` | M2x: prefix length l of the size-matched HPB for qbar=10 | 14.00 | bits | `e1c_e2.csv` |
| `C1_M2x_qbar10_hpb_avg` | M2x: average bucket size of the matched HPB (qbar=10) | 801.12 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar10_fsb_avg` | M2x: average bucket size of FSB qbar=10 | 790.21 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar10_hpb_est_loss_q1` | M2x: size-matched HPB loss, est, q=1 (qbar=10) | 14.82 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar10_hpb_est_loss_qbar` | M2x: size-matched HPB loss, est, q=10 (qbar=10) | 27.82 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar10_fsb_est_loss_qbar` | M2x: FSB loss, est, q=qbar=10 | 0.96 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar10_fsb_est_maxabs_q_le_qbar` | M2x: FSB est, max |loss| over q <= qbar=10 | 0.96 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar100_hpb_l` | M2x: prefix length l of the size-matched HPB for qbar=100 | 12.00 | bits | `e1c_e2.csv` |
| `C1_M2x_qbar100_hpb_avg` | M2x: average bucket size of the matched HPB (qbar=100) | 3204.47 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar100_fsb_avg` | M2x: average bucket size of FSB qbar=100 | 2564.83 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar100_hpb_est_loss_q1` | M2x: size-matched HPB loss, est, q=1 (qbar=100) | 9.84 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar100_hpb_est_loss_qbar` | M2x: size-matched HPB loss, est, q=100 (qbar=100) | 30.70 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar100_fsb_est_loss_qbar` | M2x: FSB loss, est, q=qbar=100 | 2.10 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar100_fsb_est_maxabs_q_le_qbar` | M2x: FSB est, max |loss| over q <= qbar=100 | 2.10 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar1000_hpb_l` | M2x: prefix length l of the size-matched HPB for qbar=1000 | 10.00 | bits | `e1c_e2.csv` |
| `C1_M2x_qbar1000_hpb_avg` | M2x: average bucket size of the matched HPB (qbar=1000) | 12,818 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar1000_fsb_avg` | M2x: average bucket size of FSB qbar=1000 | 11,336 | entries | `e1c_e2.csv` |
| `C1_M2x_qbar1000_hpb_est_loss_q1` | M2x: size-matched HPB loss, est, q=1 (qbar=1000) | 6.06 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar1000_hpb_est_loss_qbar` | M2x: size-matched HPB loss, est, q=1000 (qbar=1000) | 28.80 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar1000_fsb_est_loss_qbar` | M2x: FSB loss, est, q=qbar=1000 | 3.89 | pp | `e1c_e2.csv` |
| `C1_M2x_qbar1000_fsb_est_maxabs_q_le_qbar` | M2x: FSB est, max |loss| over q <= qbar=1000 | 3.89 | pp | `e1c_e2.csv` |

## C2 Noise tolerance (est) (14 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C2_cross5_est_qbar10_mean` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=10 reaches 5 points, mean over 5 noise draws | 0.87 | sigma | `e1d_noise.csv` |
| `C2_cross5_est_qbar10_sd` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=10 reaches 5 points, sd over 5 noise draws | 0.06 | sigma | `e1d_noise.csv` |
| `C2_cross5_est_qbar100_mean` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=100 reaches 5 points, mean over 5 noise draws | 0.69 | sigma | `e1d_noise.csv` |
| `C2_cross5_est_qbar100_sd` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=100 reaches 5 points, sd over 5 noise draws | 0.03 | sigma | `e1d_noise.csv` |
| `C2_cross5_est_qbar1000_mean` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=1000 reaches 5 points, mean over 5 noise draws | 0.66 | sigma | `e1d_noise.csv` |
| `C2_cross5_est_qbar1000_sd` | M3 (noise on all strings), est: sigma at which the loss at q=qbar=1000 reaches 5 points, sd over 5 noise draws | 0.01 | sigma | `e1d_noise.csv` |
| `C2_sigmahat_head_B` | estimator error sigma_hat, head, method B (per-password dispersion), t=1M | 0.31 | sigma | `e1d_esterror_summary.csv` |
| `C2_sigmahat_head_A` | estimator error sigma_hat, head, method A (binned masses), t=1M | 0.11 | sigma | `e1d_esterror_summary.csv` |
| `C2_sigmahat_head_B_se` | standard error over 5 folds of sigma_hat (head, method B) | 0.01 | sigma | `e1d_esterror_summary.csv` |
| `C2_bias_head_B` | bias mu = log(true / p^) (head, method B; positive = p^ too small) | -0.09 | log units | `e1d_esterror_summary.csv` |
| `C2_sigmahat_tail_B` | estimator error sigma_hat, tail, method B (per-password dispersion), t=1M | 1.57 | sigma | `e1d_esterror_summary.csv` |
| `C2_sigmahat_tail_A` | estimator error sigma_hat, tail, method A (binned masses), t=1M | 0.92 | sigma | `e1d_esterror_summary.csv` |
| `C2_sigmahat_tail_B_se` | standard error over 5 folds of sigma_hat (tail, method B) | 0.003698 | sigma | `e1d_esterror_summary.csv` |
| `C2_bias_tail_B` | bias mu = log(true / p^) (tail, method B; positive = p^ too small) | 5.86 | log units | `e1d_esterror_summary.csv` |

## C3 Count-aware attacker (emp, all of S~) (100 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C3_M0_qbar10_emp_fsb_loss_qbar` | M0: FSB loss, emp (all of S~), q=qbar=10 | 10.52 | pp | `e1e_headline.csv` |
| `C3_M0_qbar10_emp_fsb_loss_qbar_sd` | M0: sd over repeats of the above | 0.39 | pp | `e1e_headline.csv` |
| `C3_M0_qbar10_emp_hpb_loss_qbar` | M0: matched-HPB loss, emp, q=qbar=10 | 37.09 | pp | `e1e_headline.csv` |
| `C3_M0_qbar10_frac_removed_qbar` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=10 (qbar=10); 1 - FSB/HPB | 0.72 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar10_frac_removed_q1` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=10); 1 - FSB/HPB | 0.72 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar10_emp_fsb_loss_q1` | M0: FSB loss, emp, q=1 (qbar=10) | 5.82 | pp | `e1e_headline.csv` |
| `C3_M0_qbar10_emp_hpb_loss_q1` | M0: matched-HPB loss, emp, q=1 (qbar=10) | 21.10 | pp | `e1e_headline.csv` |
| `C3_M0_qbar100_emp_fsb_loss_qbar` | M0: FSB loss, emp (all of S~), q=qbar=100 | 10.92 | pp | `e1e_headline.csv` |
| `C3_M0_qbar100_emp_fsb_loss_qbar_sd` | M0: sd over repeats of the above | 0.35 | pp | `e1e_headline.csv` |
| `C3_M0_qbar100_emp_hpb_loss_qbar` | M0: matched-HPB loss, emp, q=qbar=100 | 40.90 | pp | `e1e_headline.csv` |
| `C3_M0_qbar100_frac_removed_qbar` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=100 (qbar=100); 1 - FSB/HPB | 0.73 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar100_frac_removed_q1` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=100); 1 - FSB/HPB | 0.66 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar100_emp_fsb_loss_q1` | M0: FSB loss, emp, q=1 (qbar=100) | 4.99 | pp | `e1e_headline.csv` |
| `C3_M0_qbar100_emp_hpb_loss_q1` | M0: matched-HPB loss, emp, q=1 (qbar=100) | 14.55 | pp | `e1e_headline.csv` |
| `C3_M0_qbar1000_emp_fsb_loss_qbar` | M0: FSB loss, emp (all of S~), q=qbar=1000 | 10.91 | pp | `e1e_headline.csv` |
| `C3_M0_qbar1000_emp_fsb_loss_qbar_sd` | M0: sd over repeats of the above | 0.35 | pp | `e1e_headline.csv` |
| `C3_M0_qbar1000_emp_hpb_loss_qbar` | M0: matched-HPB loss, emp, q=qbar=1000 | 39.69 | pp | `e1e_headline.csv` |
| `C3_M0_qbar1000_frac_removed_qbar` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=1000 (qbar=1000); 1 - FSB/HPB | 0.73 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar1000_frac_removed_q1` | M0: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=1000); 1 - FSB/HPB | 0.55 | fraction | `e1e_headline.csv` |
| `C3_M0_qbar1000_emp_fsb_loss_q1` | M0: FSB loss, emp, q=1 (qbar=1000) | 3.97 | pp | `e1e_headline.csv` |
| `C3_M0_qbar1000_emp_hpb_loss_q1` | M0: matched-HPB loss, emp, q=1 (qbar=1000) | 8.91 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar10_emp_fsb_loss_qbar` | M1b: FSB loss, emp (all of S~), q=qbar=10 | 7.26 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar10_emp_fsb_loss_qbar_sd` | M1b: sd over repeats of the above | 0.30 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar10_emp_hpb_loss_qbar` | M1b: matched-HPB loss, emp, q=qbar=10 | 31.10 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar10_frac_removed_qbar` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=10 (qbar=10); 1 - FSB/HPB | 0.77 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar10_frac_removed_q1` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=10); 1 - FSB/HPB | 0.82 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar10_emp_fsb_loss_q1` | M1b: FSB loss, emp, q=1 (qbar=10) | 3.27 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar10_emp_hpb_loss_q1` | M1b: matched-HPB loss, emp, q=1 (qbar=10) | 17.67 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar100_emp_fsb_loss_qbar` | M1b: FSB loss, emp (all of S~), q=qbar=100 | 7.75 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar100_emp_fsb_loss_qbar_sd` | M1b: sd over repeats of the above | 0.34 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar100_emp_hpb_loss_qbar` | M1b: matched-HPB loss, emp, q=qbar=100 | 35.12 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar100_frac_removed_qbar` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=100 (qbar=100); 1 - FSB/HPB | 0.78 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar100_frac_removed_q1` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=100); 1 - FSB/HPB | 0.77 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar100_emp_fsb_loss_q1` | M1b: FSB loss, emp, q=1 (qbar=100) | 2.66 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar100_emp_hpb_loss_q1` | M1b: matched-HPB loss, emp, q=1 (qbar=100) | 11.52 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar1000_emp_fsb_loss_qbar` | M1b: FSB loss, emp (all of S~), q=qbar=1000 | 7.62 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar1000_emp_fsb_loss_qbar_sd` | M1b: sd over repeats of the above | 0.28 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar1000_emp_hpb_loss_qbar` | M1b: matched-HPB loss, emp, q=qbar=1000 | 34.99 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar1000_frac_removed_qbar` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=1000 (qbar=1000); 1 - FSB/HPB | 0.78 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar1000_frac_removed_q1` | M1b: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=1000); 1 - FSB/HPB | 0.72 | fraction | `e1e_headline.csv` |
| `C3_M1b_qbar1000_emp_fsb_loss_q1` | M1b: FSB loss, emp, q=1 (qbar=1000) | 1.86 | pp | `e1e_headline.csv` |
| `C3_M1b_qbar1000_emp_hpb_loss_q1` | M1b: matched-HPB loss, emp, q=1 (qbar=1000) | 6.74 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_emp_fsb_loss_qbar` | M2x: FSB loss, emp (all of S~), q=qbar=10 | 13.54 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_emp_fsb_loss_qbar_sd` | M2x: sd over repeats of the above | 0.43 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_emp_hpb_loss_qbar` | M2x: matched-HPB loss, emp, q=qbar=10 | 27.82 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_frac_removed_qbar` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=10 (qbar=10); 1 - FSB/HPB | 0.51 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar10_frac_removed_q1` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=10); 1 - FSB/HPB | 0.32 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar10_emp_fsb_loss_q1` | M2x: FSB loss, emp, q=1 (qbar=10) | 10.08 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_emp_hpb_loss_q1` | M2x: matched-HPB loss, emp, q=1 (qbar=10) | 14.82 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar100_emp_fsb_loss_qbar` | M2x: FSB loss, emp (all of S~), q=qbar=100 | 14.79 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar100_emp_fsb_loss_qbar_sd` | M2x: sd over repeats of the above | 0.69 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar100_emp_hpb_loss_qbar` | M2x: matched-HPB loss, emp, q=qbar=100 | 30.70 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar100_frac_removed_qbar` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=100 (qbar=100); 1 - FSB/HPB | 0.52 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar100_frac_removed_q1` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=100); 1 - FSB/HPB | 0.00813 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar100_emp_fsb_loss_q1` | M2x: FSB loss, emp, q=1 (qbar=100) | 9.76 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar100_emp_hpb_loss_q1` | M2x: matched-HPB loss, emp, q=1 (qbar=100) | 9.84 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar1000_emp_fsb_loss_qbar` | M2x: FSB loss, emp (all of S~), q=qbar=1000 | 16.59 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar1000_emp_fsb_loss_qbar_sd` | M2x: sd over repeats of the above | 0.35 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar1000_emp_hpb_loss_qbar` | M2x: matched-HPB loss, emp, q=qbar=1000 | 29.84 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar1000_frac_removed_qbar` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=1000 (qbar=1000); 1 - FSB/HPB | 0.44 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar1000_frac_removed_q1` | M2x: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=1000); 1 - FSB/HPB | -0.42 | fraction | `e1e_headline.csv` |
| `C3_M2x_qbar1000_emp_fsb_loss_q1` | M2x: FSB loss, emp, q=1 (qbar=1000) | 8.58 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar1000_emp_hpb_loss_q1` | M2x: matched-HPB loss, emp, q=1 (qbar=1000) | 6.06 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar10_emp_fsb_loss_qbar` | M2L: FSB loss, emp (all of S~), q=qbar=10 | 12.80 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar10_emp_fsb_loss_qbar_sd` | M2L: sd over repeats of the above | 0.59 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar10_emp_hpb_loss_qbar` | M2L: matched-HPB loss, emp, q=qbar=10 | 28.15 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar10_frac_removed_qbar` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=10 (qbar=10); 1 - FSB/HPB | 0.55 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar10_frac_removed_q1` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=10); 1 - FSB/HPB | 0.43 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar10_emp_fsb_loss_q1` | M2L: FSB loss, emp, q=1 (qbar=10) | 9.49 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar10_emp_hpb_loss_q1` | M2L: matched-HPB loss, emp, q=1 (qbar=10) | 16.64 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar100_emp_fsb_loss_qbar` | M2L: FSB loss, emp (all of S~), q=qbar=100 | 14.15 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar100_emp_fsb_loss_qbar_sd` | M2L: sd over repeats of the above | 0.58 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar100_emp_hpb_loss_qbar` | M2L: matched-HPB loss, emp, q=qbar=100 | 30.36 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar100_frac_removed_qbar` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=100 (qbar=100); 1 - FSB/HPB | 0.53 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar100_frac_removed_q1` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=100); 1 - FSB/HPB | 0.24 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar100_emp_fsb_loss_q1` | M2L: FSB loss, emp, q=1 (qbar=100) | 8.93 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar100_emp_hpb_loss_q1` | M2L: matched-HPB loss, emp, q=1 (qbar=100) | 11.71 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar1000_emp_fsb_loss_qbar` | M2L: FSB loss, emp (all of S~), q=qbar=1000 | 16.07 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar1000_emp_fsb_loss_qbar_sd` | M2L: sd over repeats of the above | 0.41 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar1000_emp_hpb_loss_qbar` | M2L: matched-HPB loss, emp, q=qbar=1000 | 29.18 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar1000_frac_removed_qbar` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=1000 (qbar=1000); 1 - FSB/HPB | 0.45 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar1000_frac_removed_q1` | M2L: fraction of the matched-HPB loss removed by FSB, emp, q=1 (qbar=1000); 1 - FSB/HPB | -0.002537 | fraction | `e1e_headline.csv` |
| `C3_M2L_qbar1000_emp_fsb_loss_q1` | M2L: FSB loss, emp, q=1 (qbar=1000) | 7.90 | pp | `e1e_headline.csv` |
| `C3_M2L_qbar1000_emp_hpb_loss_q1` | M2L: matched-HPB loss, emp, q=1 (qbar=1000) | 7.88 | pp | `e1e_headline.csv` |
| `C3_M2x_qbar10_fsb_ratio_q1` | M2x: success ratio (attacker success / baseline success), FSB, emp, q=1 (qbar=10) | 87.93 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar10_fsb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (FSB, qbar=10) | 24.37 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar10_hpb_ratio_q1` | M2x: success ratio (attacker success / baseline success), HPB, emp, q=1 (qbar=10) | 128.76 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar10_hpb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (HPB, qbar=10) | 34.86 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar100_fsb_ratio_q1` | M2x: success ratio (attacker success / baseline success), FSB, emp, q=1 (qbar=100) | 85.14 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar100_fsb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (FSB, qbar=100) | 24.59 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar100_hpb_ratio_q1` | M2x: success ratio (attacker success / baseline success), HPB, emp, q=1 (qbar=100) | 85.83 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar100_hpb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (HPB, qbar=100) | 21.34 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar1000_fsb_ratio_q1` | M2x: success ratio (attacker success / baseline success), FSB, emp, q=1 (qbar=1000) | 75.00 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar1000_fsb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (FSB, qbar=1000) | 20.16 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar1000_hpb_ratio_q1` | M2x: success ratio (attacker success / baseline success), HPB, emp, q=1 (qbar=1000) | 53.21 | ratio | `e1e_ratio.csv` |
| `C3_M2x_qbar1000_hpb_ratio_q1_sd` | M2x: sd over repeats of the above ratio (HPB, qbar=1000) | 11.25 | ratio | `e1e_ratio.csv` |
| `C3_M0_baseline_q1` | M0: baseline success of the emp attacker at q=1 | 0.97 | % | `e1e_headline.csv` |
| `C3_M1b_baseline_q1` | M1b: baseline success of the emp attacker at q=1 | 1.16 | % | `e1e_headline.csv` |
| `C3_M2x_baseline_q1` | M2x: baseline success of the emp attacker at q=1 | 0.12 | % | `e1e_headline.csv` |
| `C3_M2L_baseline_q1` | M2L: baseline success of the emp attacker at q=1 | 0.54 | % | `e1e_headline.csv` |

## C4 Mechanism (167 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C4_M0_fsb_q1_head_contrib` | M0, FSB, q=1: loss contribution of the head group (share x (success - baseline)) | -0.92 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q1_tail_contrib` | M0, FSB, q=1: loss contribution of the tail group (share x (success - baseline)) | 5.90 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q1_none_contrib` | M0, FSB, q=1: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q1_total_contrib` | M0, FSB, q=1: loss contribution of the total group (share x (success - baseline)) | 4.99 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q1_tail_guess_rate` | M0, FSB, q=1: share of stored-but-not-head targets guessed | 50.48 | % | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q1_head_guess_rate` | M0, FSB, q=1: share of head targets guessed | 0.10 | % | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_head_contrib` | M0, FSB, q=100: loss contribution of the head group (share x (success - baseline)) | -0.51 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_tail_contrib` | M0, FSB, q=100: loss contribution of the tail group (share x (success - baseline)) | 11.44 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_none_contrib` | M0, FSB, q=100: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_total_contrib` | M0, FSB, q=100: loss contribution of the total group (share x (success - baseline)) | 10.92 | pp | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_tail_guess_rate` | M0, FSB, q=100: share of stored-but-not-head targets guessed | 97.80 | % | `e1f_mech_groups.csv` |
| `C4_M0_fsb_q100_head_guess_rate` | M0, FSB, q=100: share of head targets guessed | 8.11 | % | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_head_contrib` | M0, HPB, q=1: loss contribution of the head group (share x (success - baseline)) | 14.55 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_tail_contrib` | M0, HPB, q=1: loss contribution of the tail group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_none_contrib` | M0, HPB, q=1: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_total_contrib` | M0, HPB, q=1: loss contribution of the total group (share x (success - baseline)) | 14.55 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_tail_guess_rate` | M0, HPB, q=1: share of stored-but-not-head targets guessed | 0.00 | % | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q1_head_guess_rate` | M0, HPB, q=1: share of head targets guessed | 30.53 | % | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_head_contrib` | M0, HPB, q=100: loss contribution of the head group (share x (success - baseline)) | 40.90 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_tail_contrib` | M0, HPB, q=100: loss contribution of the tail group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_none_contrib` | M0, HPB, q=100: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_total_contrib` | M0, HPB, q=100: loss contribution of the total group (share x (success - baseline)) | 40.90 | pp | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_tail_guess_rate` | M0, HPB, q=100: share of stored-but-not-head targets guessed | 0.00 | % | `e1f_mech_groups.csv` |
| `C4_M0_hpb_q100_head_guess_rate` | M0, HPB, q=100: share of head targets guessed | 89.58 | % | `e1f_mech_groups.csv` |
| `C4_M0_share_head` | M0: share of targets in the head group | 50.83 | % | `e1f_mech_groups.csv` |
| `C4_M0_share_tail` | M0: share of targets in the tail group | 11.69 | % | `e1f_mech_groups.csv` |
| `C4_M0_share_none` | M0: share of targets in the none group | 37.48 | % | `e1f_mech_groups.csv` |
| `C4_M0_q1_newly_leak12` | M0, FSB, q=1: share of newly gained targets with leak count 1 or 2 | 98.64 | % | `e1f_mech_dist.csv` |
| `C4_M0_q1_newly_gamma_median` | M0, FSB, q=1: median gamma of the newly gained targets | 1.00 | gamma | `e1f_mech_quantiles.csv` |
| `C4_M0_q1_newly_leak_median` | M0, FSB, q=1: median leak count of the newly gained targets | 1.00 | count | `e1f_mech_quantiles.csv` |
| `C4_M0_q1_newly_n` | M0, FSB, q=1: number of newly gained targets (pooled over 5 repeats) | 1476.00 | targets | `e1f_mech_quantiles.csv` |
| `C4_M0_q100_newly_leak12` | M0, FSB, q=100: share of newly gained targets with leak count 1 or 2 | 98.67 | % | `e1f_mech_dist.csv` |
| `C4_M0_q100_newly_gamma_median` | M0, FSB, q=100: median gamma of the newly gained targets | 2.00 | gamma | `e1f_mech_quantiles.csv` |
| `C4_M0_q100_newly_leak_median` | M0, FSB, q=100: median leak count of the newly gained targets | 1.00 | count | `e1f_mech_quantiles.csv` |
| `C4_M0_q100_newly_n` | M0, FSB, q=100: number of newly gained targets (pooled over 5 repeats) | 2868.00 | targets | `e1f_mech_quantiles.csv` |
| `C4_M2x_fsb_q1_head_contrib` | M2x, FSB, q=1: loss contribution of the head group (share x (success - baseline)) | -0.11 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q1_tail_contrib` | M2x, FSB, q=1: loss contribution of the tail group (share x (success - baseline)) | 9.87 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q1_none_contrib` | M2x, FSB, q=1: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q1_total_contrib` | M2x, FSB, q=1: loss contribution of the total group (share x (success - baseline)) | 9.76 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q1_tail_guess_rate` | M2x, FSB, q=1: share of stored-but-not-head targets guessed | 77.38 | % | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q1_head_guess_rate` | M2x, FSB, q=1: share of head targets guessed | 0.02 | % | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_head_contrib` | M2x, FSB, q=100: loss contribution of the head group (share x (success - baseline)) | 2.04 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_tail_contrib` | M2x, FSB, q=100: loss contribution of the tail group (share x (success - baseline)) | 12.75 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_none_contrib` | M2x, FSB, q=100: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_total_contrib` | M2x, FSB, q=100: loss contribution of the total group (share x (success - baseline)) | 14.79 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_tail_guess_rate` | M2x, FSB, q=100: share of stored-but-not-head targets guessed | 99.97 | % | `e1f_mech_groups.csv` |
| `C4_M2x_fsb_q100_head_guess_rate` | M2x, FSB, q=100: share of head targets guessed | 13.50 | % | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_head_contrib` | M2x, HPB, q=1: loss contribution of the head group (share x (success - baseline)) | 9.84 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_tail_contrib` | M2x, HPB, q=1: loss contribution of the tail group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_none_contrib` | M2x, HPB, q=1: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_total_contrib` | M2x, HPB, q=1: loss contribution of the total group (share x (success - baseline)) | 9.84 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_tail_guess_rate` | M2x, HPB, q=1: share of stored-but-not-head targets guessed | 0.00 | % | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q1_head_guess_rate` | M2x, HPB, q=1: share of head targets guessed | 29.38 | % | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_head_contrib` | M2x, HPB, q=100: loss contribution of the head group (share x (success - baseline)) | 30.68 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_tail_contrib` | M2x, HPB, q=100: loss contribution of the tail group (share x (success - baseline)) | 0.02 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_none_contrib` | M2x, HPB, q=100: loss contribution of the none group (share x (success - baseline)) | 0.00 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_total_contrib` | M2x, HPB, q=100: loss contribution of the total group (share x (success - baseline)) | 30.70 | pp | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_tail_guess_rate` | M2x, HPB, q=100: share of stored-but-not-head targets guessed | 0.13 | % | `e1f_mech_groups.csv` |
| `C4_M2x_hpb_q100_head_guess_rate` | M2x, HPB, q=100: share of head targets guessed | 98.06 | % | `e1f_mech_groups.csv` |
| `C4_M2x_share_head` | M2x: share of targets in the head group | 33.88 | % | `e1f_mech_groups.csv` |
| `C4_M2x_share_tail` | M2x: share of targets in the tail group | 12.76 | % | `e1f_mech_groups.csv` |
| `C4_M2x_share_none` | M2x: share of targets in the none group | 53.36 | % | `e1f_mech_groups.csv` |
| `C4_M2x_q1_newly_leak12` | M2x, FSB, q=1: share of newly gained targets with leak count 1 or 2 | 98.70 | % | `e1f_mech_dist.csv` |
| `C4_M2x_q1_newly_gamma_median` | M2x, FSB, q=1: median gamma of the newly gained targets | 1.00 | gamma | `e1f_mech_quantiles.csv` |
| `C4_M2x_q1_newly_leak_median` | M2x, FSB, q=1: median leak count of the newly gained targets | 1.00 | count | `e1f_mech_quantiles.csv` |
| `C4_M2x_q1_newly_n` | M2x, FSB, q=1: number of newly gained targets (pooled over 5 repeats) | 2467.00 | targets | `e1f_mech_quantiles.csv` |
| `C4_M2x_q100_newly_leak12` | M2x, FSB, q=100: share of newly gained targets with leak count 1 or 2 | 84.99 | % | `e1f_mech_dist.csv` |
| `C4_M2x_q100_newly_gamma_median` | M2x, FSB, q=100: median gamma of the newly gained targets | 1.00 | gamma | `e1f_mech_quantiles.csv` |
| `C4_M2x_q100_newly_leak_median` | M2x, FSB, q=100: median leak count of the newly gained targets | 1.00 | count | `e1f_mech_quantiles.csv` |
| `C4_M2x_q100_newly_n` | M2x, FSB, q=100: number of newly gained targets (pooled over 5 repeats) | 3712.00 | targets | `e1f_mech_quantiles.csv` |
| `C4_tsweep_M0_t100000_q1` | t sweep, emp (all of S~), M0, FSB qbar=100, t=100,000: loss at q=1 | 11.49 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t100000_q10` | t sweep, emp (all of S~), M0, FSB qbar=100, t=100,000: loss at q=10 | 20.54 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t100000_q100` | t sweep, emp (all of S~), M0, FSB qbar=100, t=100,000: loss at q=100 | 24.49 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t100000_q1` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=100,000: loss at q=1 | 20.12 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t100000_q10` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=100,000: loss at q=10 | 25.92 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t100000_q100` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=100,000: loss at q=100 | 28.90 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_t100000_avg_bucket` | t sweep, FSB qbar=100, t=100,000: average bucket size | 1733.26 | entries | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t300000_q1` | t sweep, emp (all of S~), M0, FSB qbar=100, t=300,000: loss at q=1 | 8.08 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t300000_q10` | t sweep, emp (all of S~), M0, FSB qbar=100, t=300,000: loss at q=10 | 14.90 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t300000_q100` | t sweep, emp (all of S~), M0, FSB qbar=100, t=300,000: loss at q=100 | 17.48 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t300000_q1` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=300,000: loss at q=1 | 15.12 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t300000_q10` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=300,000: loss at q=10 | 19.54 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t300000_q100` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=300,000: loss at q=100 | 22.40 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_t300000_avg_bucket` | t sweep, FSB qbar=100, t=300,000: average bucket size | 2023.18 | entries | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t1000000_q1` | t sweep, emp (all of S~), M0, FSB qbar=100, t=1,000,000: loss at q=1 | 4.99 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t1000000_q10` | t sweep, emp (all of S~), M0, FSB qbar=100, t=1,000,000: loss at q=10 | 9.29 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t1000000_q100` | t sweep, emp (all of S~), M0, FSB qbar=100, t=1,000,000: loss at q=100 | 10.92 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t1000000_q1` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=1,000,000: loss at q=1 | 9.76 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t1000000_q10` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=1,000,000: loss at q=10 | 12.72 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t1000000_q100` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=1,000,000: loss at q=100 | 14.79 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_t1000000_avg_bucket` | t sweep, FSB qbar=100, t=1,000,000: average bucket size | 2564.83 | entries | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t3000000_q1` | t sweep, emp (all of S~), M0, FSB qbar=100, t=3,000,000: loss at q=1 | 3.18 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t3000000_q10` | t sweep, emp (all of S~), M0, FSB qbar=100, t=3,000,000: loss at q=10 | 6.34 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t3000000_q100` | t sweep, emp (all of S~), M0, FSB qbar=100, t=3,000,000: loss at q=100 | 7.23 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t3000000_q1` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=3,000,000: loss at q=1 | 6.49 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t3000000_q10` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=3,000,000: loss at q=10 | 8.28 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_M2x_t3000000_q100` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=3,000,000: loss at q=100 | 10.10 | pp | `e1e_tsweep.csv` |
| `C4_tsweep_t3000000_avg_bucket` | t sweep, FSB qbar=100, t=3,000,000: average bucket size | 3261.69 | entries | `e1e_tsweep.csv` |
| `C4_tsweep_M0_t10000000_q1` | t sweep, emp (all of S~), M0, FSB qbar=100, t=10,000,000: loss at q=1 | 1.49 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_M0_t10000000_q10` | t sweep, emp (all of S~), M0, FSB qbar=100, t=10,000,000: loss at q=10 | 2.20 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_M0_t10000000_q100` | t sweep, emp (all of S~), M0, FSB qbar=100, t=10,000,000: loss at q=100 | 2.32 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_M2x_t10000000_q1` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=10,000,000: loss at q=1 | 2.61 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_M2x_t10000000_q10` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=10,000,000: loss at q=10 | 2.77 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_M2x_t10000000_q100` | t sweep, emp (all of S~), M2x, FSB qbar=100, t=10,000,000: loss at q=100 | 4.26 | pp | `e1e_tsweep_10M.csv` |
| `C4_tsweep_t10000000_avg_bucket` | t sweep, FSB qbar=100, t=10,000,000: average bucket size | 4682.36 | entries | `e1e_tsweep_10M.csv` |
| `C4_fix_M0_fsb_base_q100_at2000` | fixes, emp (all of S~), M0, fsb_base: loss at q=100 interpolated to 2000 entries per bucket | 11.44 | pp | `e1e_fix.csv` |
| `C4_fix_M0_fsb_base_q100_at6500` | fixes, emp (all of S~), M0, fsb_base: loss at q=100 interpolated to 6500 entries per bucket | 10.14 | pp | `e1e_fix.csv` |
| `C4_fix_M0_fsb_base_q100_at20000` | fixes, emp (all of S~), M0, fsb_base: loss at q=100 interpolated to 20000 entries per bucket | 8.77 | pp | `e1e_fix.csv` |
| `C4_fix_M0_fsb_base_q1000_at2000` | fixes, emp (all of S~), M0, fsb_base: loss at q=1000 interpolated to 2000 entries per bucket | 31.40 | pp | `e1e_fix.csv` |
| `C4_fix_M0_fsb_base_q1000_at6500` | fixes, emp (all of S~), M0, fsb_base: loss at q=1000 interpolated to 6500 entries per bucket | 13.33 | pp | `e1e_fix.csv` |
| `C4_fix_M0_fsb_base_q1000_at20000` | fixes, emp (all of S~), M0, fsb_base: loss at q=1000 interpolated to 20000 entries per bucket | 10.45 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q100_at2000` | fixes, emp (all of S~), M0, smoothed: loss at q=100 interpolated to 2000 entries per bucket | 11.43 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q100_at6500` | fixes, emp (all of S~), M0, smoothed: loss at q=100 interpolated to 6500 entries per bucket | 10.14 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q100_at20000` | fixes, emp (all of S~), M0, smoothed: loss at q=100 interpolated to 20000 entries per bucket | 8.77 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q1000_at2000` | fixes, emp (all of S~), M0, smoothed: loss at q=1000 interpolated to 2000 entries per bucket | 31.40 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q1000_at6500` | fixes, emp (all of S~), M0, smoothed: loss at q=1000 interpolated to 6500 entries per bucket | 13.35 | pp | `e1e_fix.csv` |
| `C4_fix_M0_smoothed_q1000_at20000` | fixes, emp (all of S~), M0, smoothed: loss at q=1000 interpolated to 20000 entries per bucket | 10.45 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q100_at2000` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=100 interpolated to 2000 entries per bucket | 11.46 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q100_at6500` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=100 interpolated to 6500 entries per bucket | 9.91 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q100_at20000` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=100 interpolated to 20000 entries per bucket | 7.95 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q1000_at2000` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=1000 interpolated to 2000 entries per bucket | 29.09 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q1000_at6500` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=1000 interpolated to 6500 entries per bucket | 12.94 | pp | `e1e_fix.csv` |
| `C4_fix_M0_cal_iso_w0.5_q1000_at20000` | fixes, emp (all of S~), M0, cal_iso_w0.5: loss at q=1000 interpolated to 20000 entries per bucket | 10.38 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q100_at2000` | fixes, emp (all of S~), M2x, fsb_base: loss at q=100 interpolated to 2000 entries per bucket | 16.39 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q100_at6500` | fixes, emp (all of S~), M2x, fsb_base: loss at q=100 interpolated to 6500 entries per bucket | 12.87 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q100_at20000` | fixes, emp (all of S~), M2x, fsb_base: loss at q=100 interpolated to 20000 entries per bucket | 12.52 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q1000_at2000` | fixes, emp (all of S~), M2x, fsb_base: loss at q=1000 interpolated to 2000 entries per bucket | 39.58 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q1000_at6500` | fixes, emp (all of S~), M2x, fsb_base: loss at q=1000 interpolated to 6500 entries per bucket | 24.63 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_fsb_base_q1000_at20000` | fixes, emp (all of S~), M2x, fsb_base: loss at q=1000 interpolated to 20000 entries per bucket | 14.11 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q100_at2000` | fixes, emp (all of S~), M2x, smoothed: loss at q=100 interpolated to 2000 entries per bucket | 16.39 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q100_at6500` | fixes, emp (all of S~), M2x, smoothed: loss at q=100 interpolated to 6500 entries per bucket | 12.87 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q100_at20000` | fixes, emp (all of S~), M2x, smoothed: loss at q=100 interpolated to 20000 entries per bucket | 12.52 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q1000_at2000` | fixes, emp (all of S~), M2x, smoothed: loss at q=1000 interpolated to 2000 entries per bucket | 39.58 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q1000_at6500` | fixes, emp (all of S~), M2x, smoothed: loss at q=1000 interpolated to 6500 entries per bucket | 24.62 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_smoothed_q1000_at20000` | fixes, emp (all of S~), M2x, smoothed: loss at q=1000 interpolated to 20000 entries per bucket | 14.11 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q100_at2000` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=100 interpolated to 2000 entries per bucket | 15.83 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q100_at6500` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=100 interpolated to 6500 entries per bucket | 12.78 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q100_at20000` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=100 interpolated to 20000 entries per bucket | 12.32 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q1000_at2000` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=1000 interpolated to 2000 entries per bucket | 39.51 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q1000_at6500` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=1000 interpolated to 6500 entries per bucket | 22.96 | pp | `e1e_fix.csv` |
| `C4_fix_M2x_cal_iso_w0.5_q1000_at20000` | fixes, emp (all of S~), M2x, cal_iso_w0.5: loss at q=1000 interpolated to 20000 entries per bucket | 13.81 | pp | `e1e_fix.csv` |
| `C4_noise_est_tail_s0.5_mean` | M3 tail-noise (noise on tail strings only), est, sigma=0.5, q=qbar=100: mean over 5 draws | -0.04 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_tail_s0.5_sd` | M3 tail-noise (noise on tail strings only), est, sigma=0.5, q=qbar=100: sd over 5 draws | 0.02 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_tail_s1.0_mean` | M3 tail-noise (noise on tail strings only), est, sigma=1.0, q=qbar=100: mean over 5 draws | 0.28 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_tail_s1.0_sd` | M3 tail-noise (noise on tail strings only), est, sigma=1.0, q=qbar=100: sd over 5 draws | 0.04 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_tail_s1.6_mean` | M3 tail-noise (noise on tail strings only), est, sigma=1.6, q=qbar=100: mean over 5 draws | 0.89 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_tail_s1.6_sd` | M3 tail-noise (noise on tail strings only), est, sigma=1.6, q=qbar=100: sd over 5 draws | 0.14 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s0.5_mean` | M3 full-noise (noise on all strings), est, sigma=0.5, q=qbar=100: mean over 5 draws | 2.63 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s0.5_sd` | M3 full-noise (noise on all strings), est, sigma=0.5, q=qbar=100: sd over 5 draws | 0.26 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s1.0_mean` | M3 full-noise (noise on all strings), est, sigma=1.0, q=qbar=100: mean over 5 draws | 9.77 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s1.0_sd` | M3 full-noise (noise on all strings), est, sigma=1.0, q=qbar=100: sd over 5 draws | 0.45 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s1.6_mean` | M3 full-noise (noise on all strings), est, sigma=1.6, q=qbar=100: mean over 5 draws | 23.20 | pp | `e1f_tailnoise.csv` |
| `C4_noise_est_full_s1.6_sd` | M3 full-noise (noise on all strings), est, sigma=1.6, q=qbar=100: sd over 5 draws | 0.28 | pp | `e1f_tailnoise.csv` |
| `C4_noise_emp_tail_s0.5_mean` | M3 tail-noise (noise on tail strings only), emp, sigma=0.5, q=qbar=100: mean over 5 draws | 10.88 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_tail_s0.5_sd` | M3 tail-noise (noise on tail strings only), emp, sigma=0.5, q=qbar=100: sd over 5 draws | 0.02 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_tail_s1.0_mean` | M3 tail-noise (noise on tail strings only), emp, sigma=1.0, q=qbar=100: mean over 5 draws | 10.84 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_tail_s1.0_sd` | M3 tail-noise (noise on tail strings only), emp, sigma=1.0, q=qbar=100: sd over 5 draws | 0.08 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_tail_s1.6_mean` | M3 tail-noise (noise on tail strings only), emp, sigma=1.6, q=qbar=100: mean over 5 draws | 10.94 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_tail_s1.6_sd` | M3 tail-noise (noise on tail strings only), emp, sigma=1.6, q=qbar=100: sd over 5 draws | 0.05 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s0.5_mean` | M3 full-noise (noise on all strings), emp, sigma=0.5, q=qbar=100: mean over 5 draws | 12.92 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s0.5_sd` | M3 full-noise (noise on all strings), emp, sigma=0.5, q=qbar=100: sd over 5 draws | 0.28 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s1.0_mean` | M3 full-noise (noise on all strings), emp, sigma=1.0, q=qbar=100: mean over 5 draws | 19.60 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s1.0_sd` | M3 full-noise (noise on all strings), emp, sigma=1.0, q=qbar=100: sd over 5 draws | 0.41 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s1.6_mean` | M3 full-noise (noise on all strings), emp, sigma=1.6, q=qbar=100: mean over 5 draws | 33.03 | pp | `e1f_tailnoise_emp.csv` |
| `C4_noise_emp_full_s1.6_sd` | M3 full-noise (noise on all strings), emp, sigma=1.6, q=qbar=100: sd over 5 draws | 0.33 | pp | `e1f_tailnoise_emp.csv` |
| `C4_clean_emp_M0_q100` | clean estimate (sigma=0): emp loss, M0, FSB qbar=100, q=100 | 10.92 | pp | `e1e_headline.csv` |
| `C4_clean_est_M0_q100` | clean estimate (sigma=0): est loss, M0, FSB qbar=100, q=100 | 0.00 | pp | `e1c_e2.csv` |

## C5 Attacker cost (20 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C5_emp_2M_n_candidates` | emp attacker, candidate list 2M: number of candidates | 2,000,000 | candidates | `e1e_cost.csv` |
| `C5_emp_2M_total_s` | emp attacker, candidate list 2M: time of one cold run (5 x 5,000 targets) | 4.90 | s | `e1e_cost.csv` |
| `C5_emp_2M_index_build_s` | emp attacker, candidate list 2M: index build time | 0.90 | s | `e1e_cost.csv` |
| `C5_emp_2M_games_5x5000_s` | emp attacker, candidate list 2M: time of the 25,000 bucket queries | 1.30 | s | `e1e_cost.csv` |
| `C5_emp_2M_peak_rss_gb` | emp attacker, candidate list 2M: peak resident memory of the process | 2.66 | GB | `e1e_cost.csv` |
| `C5_emp_all_n_candidates` | emp attacker, candidate list all of S~: number of candidates | 13,125,513 | candidates | `e1e_cost.csv` |
| `C5_emp_all_total_s` | emp attacker, candidate list all of S~: time of one cold run (5 x 5,000 targets) | 14.10 | s | `e1e_cost.csv` |
| `C5_emp_all_index_build_s` | emp attacker, candidate list all of S~: index build time | 8.60 | s | `e1e_cost.csv` |
| `C5_emp_all_games_5x5000_s` | emp attacker, candidate list all of S~: time of the 25,000 bucket queries | 2.30 | s | `e1e_cost.csv` |
| `C5_emp_all_peak_rss_gb` | emp attacker, candidate list all of S~: peak resident memory of the process | 3.57 | GB | `e1e_cost.csv` |
| `C5_est_2M_n_candidates` | est attacker, candidate list 2M: number of candidates | 2,000,000 | candidates | `e1e_cost.csv` |
| `C5_est_2M_total_s` | est attacker, candidate list 2M: time of one cold run (5 x 5,000 targets) | 7.60 | s | `e1e_cost.csv` |
| `C5_est_2M_index_build_s` | est attacker, candidate list 2M: index build time | 1.30 | s | `e1e_cost.csv` |
| `C5_est_2M_games_5x5000_s` | est attacker, candidate list 2M: time of the 25,000 bucket queries | 2.10 | s | `e1e_cost.csv` |
| `C5_est_2M_peak_rss_gb` | est attacker, candidate list 2M: peak resident memory of the process | 2.67 | GB | `e1e_cost.csv` |
| `C5_est_all_n_candidates` | est attacker, candidate list all of S~: number of candidates | 13,125,513 | candidates | `e1e_cost.csv` |
| `C5_est_all_total_s` | est attacker, candidate list all of S~: time of one cold run (5 x 5,000 targets) | 22.20 | s | `e1e_cost.csv` |
| `C5_est_all_index_build_s` | est attacker, candidate list all of S~: index build time | 13.30 | s | `e1e_cost.csv` |
| `C5_est_all_games_5x5000_s` | est attacker, candidate list all of S~: time of the 25,000 bucket queries | 2.20 | s | `e1e_cost.csv` |
| `C5_est_all_peak_rss_gb` | est attacker, candidate list all of S~: peak resident memory of the process | 3.63 | GB | `e1e_cost.csv` |

## C6 Floor on gamma (fresh pool; emp, gt, est attackers) (393 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C6_M0_qbar10_plain_emp_loss_q1` | M0, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=1 | 5.71 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_plain_gt_loss_q1` | M0, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=1 | 5.76 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_est_loss_q1` | M0, fresh pool, FSB qbar=10 plain, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_worst_q1` | M0, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=1 | 5.76 | pp | `` |
| `C6_M0_qbar10_plain_emp_loss_qbar` | M0, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=10 | 10.40 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_plain_gt_loss_qbar` | M0, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=10 | 10.30 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_est_loss_qbar` | M0, fresh pool, FSB qbar=10 plain, est attacker: loss at q=10 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_worst_qbar` | M0, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=10 | 10.40 | pp | `` |
| `C6_M0_qbar10_plain_emp_loss_q1000` | M0, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=1000 | 51.77 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_plain_gt_loss_q1000` | M0, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=1000 | 51.77 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_est_loss_q1000` | M0, fresh pool, FSB qbar=10 plain, est attacker: loss at q=1000 | 52.37 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_plain_worst_q1000` | M0, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=1000 | 52.37 | pp | `` |
| `C6_M0_qbar10_floor256_emp_loss_q1` | M0, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor256_gt_loss_q1` | M0, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_est_loss_q1` | M0, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_worst_q1` | M0, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar10_floor256_emp_loss_qbar` | M0, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=10 | 0.54 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor256_gt_loss_qbar` | M0, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=10 | 0.65 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_est_loss_qbar` | M0, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=10 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_worst_qbar` | M0, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=10 | 0.65 | pp | `` |
| `C6_M0_qbar10_floor256_emp_loss_q1000` | M0, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=1000 | 51.77 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor256_gt_loss_q1000` | M0, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=1000 | 51.77 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_est_loss_q1000` | M0, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=1000 | 52.32 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor256_worst_q1000` | M0, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=1000 | 52.32 | pp | `` |
| `C6_M0_qbar10_floor1024_emp_loss_q1` | M0, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor1024_gt_loss_q1` | M0, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_est_loss_q1` | M0, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_worst_q1` | M0, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar10_floor1024_emp_loss_qbar` | M0, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=10 | -0.12 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor1024_gt_loss_qbar` | M0, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=10 | 0.09 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_est_loss_qbar` | M0, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=10 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_worst_qbar` | M0, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=10 | 0.09 | pp | `` |
| `C6_M0_qbar10_floor1024_emp_loss_q1000` | M0, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=1000 | 46.01 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor1024_gt_loss_q1000` | M0, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=1000 | 46.04 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_est_loss_q1000` | M0, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=1000 | 46.76 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor1024_worst_q1000` | M0, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 46.76 | pp | `` |
| `C6_M0_qbar10_floor2048_emp_loss_q1` | M0, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor2048_gt_loss_q1` | M0, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_est_loss_q1` | M0, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_worst_q1` | M0, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar10_floor2048_emp_loss_qbar` | M0, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=10 | -0.03 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor2048_gt_loss_qbar` | M0, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=10 | 0.06 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_est_loss_qbar` | M0, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=10 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_worst_qbar` | M0, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=10 | 0.06 | pp | `` |
| `C6_M0_qbar10_floor2048_emp_loss_q1000` | M0, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=1000 | 44.53 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor2048_gt_loss_q1000` | M0, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=1000 | 44.56 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_est_loss_q1000` | M0, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=1000 | 44.58 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor2048_worst_q1000` | M0, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 44.58 | pp | `` |
| `C6_M0_qbar10_floor4096_emp_loss_q1` | M0, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor4096_gt_loss_q1` | M0, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_est_loss_q1` | M0, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_worst_q1` | M0, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar10_floor4096_emp_loss_qbar` | M0, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=10 | 0.06 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor4096_gt_loss_qbar` | M0, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=10 | 0.06 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_est_loss_qbar` | M0, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=10 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_worst_qbar` | M0, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=10 | 0.06 | pp | `` |
| `C6_M0_qbar10_floor4096_emp_loss_q1000` | M0, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=1000 | 43.19 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar10_floor4096_gt_loss_q1000` | M0, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=1000 | 43.19 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_est_loss_q1000` | M0, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=1000 | 42.78 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar10_floor4096_worst_q1000` | M0, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 43.19 | pp | `` |
| `C6_M0_qbar10_hpb_emp_loss_qbar` | M0, fresh pool, matched HPB, emp: loss at q=qbar=10 | 37.41 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_plain_emp_loss_q1` | M0, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=1 | 4.87 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_plain_gt_loss_q1` | M0, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=1 | 4.98 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_est_loss_q1` | M0, fresh pool, FSB qbar=100 plain, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_worst_q1` | M0, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=1 | 4.98 | pp | `` |
| `C6_M0_qbar100_plain_emp_loss_qbar` | M0, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=100 | 10.68 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_plain_gt_loss_qbar` | M0, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=100 | 10.52 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_est_loss_qbar` | M0, fresh pool, FSB qbar=100 plain, est attacker: loss at q=100 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_worst_qbar` | M0, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=100 | 10.68 | pp | `` |
| `C6_M0_qbar100_plain_emp_loss_q1000` | M0, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=1000 | 24.32 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_plain_gt_loss_q1000` | M0, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=1000 | 24.17 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_est_loss_q1000` | M0, fresh pool, FSB qbar=100 plain, est attacker: loss at q=1000 | 11.49 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_plain_worst_q1000` | M0, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=1000 | 24.32 | pp | `` |
| `C6_M0_qbar100_floor256_emp_loss_q1` | M0, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor256_gt_loss_q1` | M0, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_est_loss_q1` | M0, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_worst_q1` | M0, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar100_floor256_emp_loss_qbar` | M0, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=100 | 3.27 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor256_gt_loss_qbar` | M0, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=100 | 3.74 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_est_loss_qbar` | M0, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=100 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_worst_qbar` | M0, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=100 | 3.74 | pp | `` |
| `C6_M0_qbar100_floor256_emp_loss_q1000` | M0, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=1000 | 20.26 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor256_gt_loss_q1000` | M0, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=1000 | 20.13 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_est_loss_q1000` | M0, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=1000 | 11.45 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor256_worst_q1000` | M0, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=1000 | 20.26 | pp | `` |
| `C6_M0_qbar100_floor1024_emp_loss_q1` | M0, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor1024_gt_loss_q1` | M0, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_est_loss_q1` | M0, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_worst_q1` | M0, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar100_floor1024_emp_loss_qbar` | M0, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=100 | 1.19 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor1024_gt_loss_qbar` | M0, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=100 | 1.80 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_est_loss_qbar` | M0, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=100 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_worst_qbar` | M0, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=100 | 1.80 | pp | `` |
| `C6_M0_qbar100_floor1024_emp_loss_q1000` | M0, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=1000 | 8.36 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor1024_gt_loss_q1000` | M0, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=1000 | 15.60 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_est_loss_q1000` | M0, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=1000 | 11.45 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor1024_worst_q1000` | M0, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 15.60 | pp | `` |
| `C6_M0_qbar100_floor2048_emp_loss_q1` | M0, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor2048_gt_loss_q1` | M0, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_est_loss_q1` | M0, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_worst_q1` | M0, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar100_floor2048_emp_loss_qbar` | M0, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=100 | -0.32 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor2048_gt_loss_qbar` | M0, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=100 | 0.08 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_est_loss_qbar` | M0, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=100 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_worst_qbar` | M0, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=100 | 0.08 | pp | `` |
| `C6_M0_qbar100_floor2048_emp_loss_q1000` | M0, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=1000 | 0.24 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor2048_gt_loss_q1000` | M0, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=1000 | 13.94 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_est_loss_q1000` | M0, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=1000 | 11.45 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor2048_worst_q1000` | M0, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 13.94 | pp | `` |
| `C6_M0_qbar100_floor4096_emp_loss_q1` | M0, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor4096_gt_loss_q1` | M0, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_est_loss_q1` | M0, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_worst_q1` | M0, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar100_floor4096_emp_loss_qbar` | M0, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=100 | -0.52 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor4096_gt_loss_qbar` | M0, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=100 | 0.04 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_est_loss_qbar` | M0, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=100 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_worst_qbar` | M0, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=100 | 0.04 | pp | `` |
| `C6_M0_qbar100_floor4096_emp_loss_q1000` | M0, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=1000 | 10.64 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar100_floor4096_gt_loss_q1000` | M0, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=1000 | 13.73 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_est_loss_q1000` | M0, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=1000 | 11.46 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar100_floor4096_worst_q1000` | M0, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 13.73 | pp | `` |
| `C6_M0_qbar100_hpb_emp_loss_qbar` | M0, fresh pool, matched HPB, emp: loss at q=qbar=100 | 41.51 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_plain_emp_loss_q1` | M0, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1 | 3.97 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_plain_gt_loss_q1` | M0, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1 | 4.04 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_est_loss_q1` | M0, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_worst_q1` | M0, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1 | 4.04 | pp | `` |
| `C6_M0_qbar1000_plain_emp_loss_qbar` | M0, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1000 | 10.70 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_plain_gt_loss_qbar` | M0, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1000 | 10.55 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_est_loss_qbar` | M0, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_worst_qbar` | M0, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1000 | 10.70 | pp | `` |
| `C6_M0_qbar1000_plain_emp_loss_q1000` | M0, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1000 | 10.70 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_plain_gt_loss_q1000` | M0, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1000 | 10.55 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_est_loss_q1000` | M0, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_plain_worst_q1000` | M0, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1000 | 10.70 | pp | `` |
| `C6_M0_qbar1000_floor256_emp_loss_q1` | M0, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor256_gt_loss_q1` | M0, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_est_loss_q1` | M0, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_worst_q1` | M0, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar1000_floor256_emp_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1000 | 9.93 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor256_gt_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1000 | 9.88 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_est_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_worst_qbar` | M0, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1000 | 9.93 | pp | `` |
| `C6_M0_qbar1000_floor256_emp_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1000 | 9.93 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor256_gt_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1000 | 9.88 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_est_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor256_worst_q1000` | M0, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1000 | 9.93 | pp | `` |
| `C6_M0_qbar1000_floor1024_emp_loss_q1` | M0, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor1024_gt_loss_q1` | M0, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_est_loss_q1` | M0, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_worst_q1` | M0, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar1000_floor1024_emp_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1000 | 6.35 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor1024_gt_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1000 | 6.12 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_est_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_worst_qbar` | M0, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 6.35 | pp | `` |
| `C6_M0_qbar1000_floor1024_emp_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1000 | 6.35 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor1024_gt_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1000 | 6.12 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_est_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor1024_worst_q1000` | M0, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 6.35 | pp | `` |
| `C6_M0_qbar1000_floor2048_emp_loss_q1` | M0, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor2048_gt_loss_q1` | M0, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_est_loss_q1` | M0, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_worst_q1` | M0, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar1000_floor2048_emp_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1000 | -0.18 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor2048_gt_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1000 | 2.72 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_est_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_worst_qbar` | M0, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 2.72 | pp | `` |
| `C6_M0_qbar1000_floor2048_emp_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1000 | -0.18 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor2048_gt_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1000 | 2.72 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_est_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor2048_worst_q1000` | M0, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 2.72 | pp | `` |
| `C6_M0_qbar1000_floor4096_emp_loss_q1` | M0, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor4096_gt_loss_q1` | M0, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_est_loss_q1` | M0, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_worst_q1` | M0, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M0_qbar1000_floor4096_emp_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1000 | -0.82 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor4096_gt_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1000 | 2.19 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_est_loss_qbar` | M0, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_worst_qbar` | M0, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 2.19 | pp | `` |
| `C6_M0_qbar1000_floor4096_emp_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1000 | -0.82 | pp | `e1g_floor_fresh.csv` |
| `C6_M0_qbar1000_floor4096_gt_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1000 | 2.19 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_est_loss_q1000` | M0, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1000 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M0_qbar1000_floor4096_worst_q1000` | M0, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 2.19 | pp | `` |
| `C6_M0_qbar1000_hpb_emp_loss_qbar` | M0, fresh pool, matched HPB, emp: loss at q=qbar=1000 | 40.32 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_plain_emp_loss_q1` | M2x, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=1 | 9.95 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_plain_gt_loss_q1` | M2x, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=1 | 9.98 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_est_loss_q1` | M2x, fresh pool, FSB qbar=10 plain, est attacker: loss at q=1 | 0.08 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_worst_q1` | M2x, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=1 | 9.98 | pp | `` |
| `C6_M2x_qbar10_plain_emp_loss_qbar` | M2x, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=10 | 13.44 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_plain_gt_loss_qbar` | M2x, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=10 | 13.40 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_est_loss_qbar` | M2x, fresh pool, FSB qbar=10 plain, est attacker: loss at q=10 | 1.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_worst_qbar` | M2x, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=10 | 13.44 | pp | `` |
| `C6_M2x_qbar10_plain_emp_loss_q1000` | M2x, fresh pool, FSB qbar=10 plain, emp attacker: loss at q=1000 | 39.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_plain_gt_loss_q1000` | M2x, fresh pool, FSB qbar=10 plain, gt attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_est_loss_q1000` | M2x, fresh pool, FSB qbar=10 plain, est attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_plain_worst_q1000` | M2x, fresh pool, FSB qbar=10 plain: largest loss over the emp, gt and est attackers at q=1000 | 39.50 | pp | `` |
| `C6_M2x_qbar10_floor256_emp_loss_q1` | M2x, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=1 | 0.20 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor256_gt_loss_q1` | M2x, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=1 | 0.19 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_est_loss_q1` | M2x, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_worst_q1` | M2x, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.20 | pp | `` |
| `C6_M2x_qbar10_floor256_emp_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=10 | 2.68 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor256_gt_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=10 | 2.80 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_est_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=10 | 1.09 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_worst_qbar` | M2x, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=10 | 2.80 | pp | `` |
| `C6_M2x_qbar10_floor256_emp_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor256, emp attacker: loss at q=1000 | 39.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor256_gt_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor256, gt attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_est_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor256, est attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor256_worst_q1000` | M2x, fresh pool, FSB qbar=10 floor256: largest loss over the emp, gt and est attackers at q=1000 | 39.50 | pp | `` |
| `C6_M2x_qbar10_floor1024_emp_loss_q1` | M2x, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=1 | -0.02 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor1024_gt_loss_q1` | M2x, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=1 | 0.07 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_est_loss_q1` | M2x, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_worst_q1` | M2x, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.11 | pp | `` |
| `C6_M2x_qbar10_floor1024_emp_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=10 | 0.26 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor1024_gt_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=10 | 1.06 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_est_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=10 | 1.09 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_worst_qbar` | M2x, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=10 | 1.09 | pp | `` |
| `C6_M2x_qbar10_floor1024_emp_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor1024, emp attacker: loss at q=1000 | 39.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor1024_gt_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor1024, gt attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_est_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor1024, est attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor1024_worst_q1000` | M2x, fresh pool, FSB qbar=10 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 39.50 | pp | `` |
| `C6_M2x_qbar10_floor2048_emp_loss_q1` | M2x, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=1 | -0.01 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor2048_gt_loss_q1` | M2x, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_est_loss_q1` | M2x, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_worst_q1` | M2x, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.11 | pp | `` |
| `C6_M2x_qbar10_floor2048_emp_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=10 | 1.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor2048_gt_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=10 | 1.08 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_est_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=10 | 1.09 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_worst_qbar` | M2x, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=10 | 1.09 | pp | `` |
| `C6_M2x_qbar10_floor2048_emp_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor2048, emp attacker: loss at q=1000 | 36.78 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor2048_gt_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor2048, gt attacker: loss at q=1000 | 36.78 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_est_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor2048, est attacker: loss at q=1000 | 37.88 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor2048_worst_q1000` | M2x, fresh pool, FSB qbar=10 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 37.88 | pp | `` |
| `C6_M2x_qbar10_floor4096_emp_loss_q1` | M2x, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=1 | 0.11 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor4096_gt_loss_q1` | M2x, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_est_loss_q1` | M2x, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=1 | 0.11 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_worst_q1` | M2x, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.11 | pp | `` |
| `C6_M2x_qbar10_floor4096_emp_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=10 | 1.08 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor4096_gt_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=10 | 1.08 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_est_loss_qbar` | M2x, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=10 | 1.09 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_worst_qbar` | M2x, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=10 | 1.09 | pp | `` |
| `C6_M2x_qbar10_floor4096_emp_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor4096, emp attacker: loss at q=1000 | 32.74 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar10_floor4096_gt_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor4096, gt attacker: loss at q=1000 | 32.74 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_est_loss_q1000` | M2x, fresh pool, FSB qbar=10 floor4096, est attacker: loss at q=1000 | 33.84 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar10_floor4096_worst_q1000` | M2x, fresh pool, FSB qbar=10 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 33.84 | pp | `` |
| `C6_M2x_qbar10_hpb_emp_loss_qbar` | M2x, fresh pool, matched HPB, emp: loss at q=qbar=10 | 27.93 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_plain_emp_loss_q1` | M2x, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=1 | 9.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_plain_gt_loss_q1` | M2x, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=1 | 9.52 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_est_loss_q1` | M2x, fresh pool, FSB qbar=100 plain, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_worst_q1` | M2x, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=1 | 9.52 | pp | `` |
| `C6_M2x_qbar100_plain_emp_loss_qbar` | M2x, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=100 | 14.54 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_plain_gt_loss_qbar` | M2x, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=100 | 14.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_est_loss_qbar` | M2x, fresh pool, FSB qbar=100 plain, est attacker: loss at q=100 | 2.12 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_worst_qbar` | M2x, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=100 | 14.54 | pp | `` |
| `C6_M2x_qbar100_plain_emp_loss_q1000` | M2x, fresh pool, FSB qbar=100 plain, emp attacker: loss at q=1000 | 39.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_plain_gt_loss_q1000` | M2x, fresh pool, FSB qbar=100 plain, gt attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_est_loss_q1000` | M2x, fresh pool, FSB qbar=100 plain, est attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_plain_worst_q1000` | M2x, fresh pool, FSB qbar=100 plain: largest loss over the emp, gt and est attackers at q=1000 | 39.50 | pp | `` |
| `C6_M2x_qbar100_floor256_emp_loss_q1` | M2x, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=1 | 0.20 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor256_gt_loss_q1` | M2x, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=1 | 0.19 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_est_loss_q1` | M2x, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_worst_q1` | M2x, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.20 | pp | `` |
| `C6_M2x_qbar100_floor256_emp_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=100 | 7.70 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor256_gt_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=100 | 7.71 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_est_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=100 | 2.16 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_worst_qbar` | M2x, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=100 | 7.71 | pp | `` |
| `C6_M2x_qbar100_floor256_emp_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor256, emp attacker: loss at q=1000 | 39.50 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor256_gt_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor256, gt attacker: loss at q=1000 | 39.50 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_est_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor256, est attacker: loss at q=1000 | 39.48 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor256_worst_q1000` | M2x, fresh pool, FSB qbar=100 floor256: largest loss over the emp, gt and est attackers at q=1000 | 39.50 | pp | `` |
| `C6_M2x_qbar100_floor1024_emp_loss_q1` | M2x, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=1 | -0.02 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor1024_gt_loss_q1` | M2x, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=1 | -0.02 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_est_loss_q1` | M2x, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_worst_q1` | M2x, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar100_floor1024_emp_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=100 | 2.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor1024_gt_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=100 | 4.02 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_est_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=100 | 2.16 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_worst_qbar` | M2x, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=100 | 4.02 | pp | `` |
| `C6_M2x_qbar100_floor1024_emp_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor1024, emp attacker: loss at q=1000 | 27.51 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor1024_gt_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor1024, gt attacker: loss at q=1000 | 32.72 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_est_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor1024, est attacker: loss at q=1000 | 33.86 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor1024_worst_q1000` | M2x, fresh pool, FSB qbar=100 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 33.86 | pp | `` |
| `C6_M2x_qbar100_floor2048_emp_loss_q1` | M2x, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=1 | -0.06 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor2048_gt_loss_q1` | M2x, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=1 | -0.03 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_est_loss_q1` | M2x, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_worst_q1` | M2x, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar100_floor2048_emp_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=100 | 1.44 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor2048_gt_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=100 | 2.12 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_est_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=100 | 2.16 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_worst_qbar` | M2x, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=100 | 2.16 | pp | `` |
| `C6_M2x_qbar100_floor2048_emp_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor2048, emp attacker: loss at q=1000 | 6.03 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor2048_gt_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor2048, gt attacker: loss at q=1000 | 31.34 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_est_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor2048, est attacker: loss at q=1000 | 31.18 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor2048_worst_q1000` | M2x, fresh pool, FSB qbar=100 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 31.34 | pp | `` |
| `C6_M2x_qbar100_floor4096_emp_loss_q1` | M2x, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor4096_gt_loss_q1` | M2x, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_est_loss_q1` | M2x, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_worst_q1` | M2x, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar100_floor4096_emp_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=100 | -0.16 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor4096_gt_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=100 | 2.12 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_est_loss_qbar` | M2x, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=100 | 2.16 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_worst_qbar` | M2x, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=100 | 2.16 | pp | `` |
| `C6_M2x_qbar100_floor4096_emp_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor4096, emp attacker: loss at q=1000 | 30.53 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar100_floor4096_gt_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor4096, gt attacker: loss at q=1000 | 30.56 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_est_loss_q1000` | M2x, fresh pool, FSB qbar=100 floor4096, est attacker: loss at q=1000 | 29.47 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar100_floor4096_worst_q1000` | M2x, fresh pool, FSB qbar=100 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 30.56 | pp | `` |
| `C6_M2x_qbar100_hpb_emp_loss_qbar` | M2x, fresh pool, matched HPB, emp: loss at q=qbar=100 | 30.74 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_plain_emp_loss_q1` | M2x, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1 | 8.34 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_plain_gt_loss_q1` | M2x, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1 | 8.41 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_est_loss_q1` | M2x, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_worst_q1` | M2x, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1 | 8.41 | pp | `` |
| `C6_M2x_qbar1000_plain_emp_loss_qbar` | M2x, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1000 | 16.06 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_plain_gt_loss_qbar` | M2x, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1000 | 16.02 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_est_loss_qbar` | M2x, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1000 | 3.63 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_worst_qbar` | M2x, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1000 | 16.06 | pp | `` |
| `C6_M2x_qbar1000_plain_emp_loss_q1000` | M2x, fresh pool, FSB qbar=1000 plain, emp attacker: loss at q=1000 | 16.06 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_plain_gt_loss_q1000` | M2x, fresh pool, FSB qbar=1000 plain, gt attacker: loss at q=1000 | 16.02 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_est_loss_q1000` | M2x, fresh pool, FSB qbar=1000 plain, est attacker: loss at q=1000 | 3.63 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_plain_worst_q1000` | M2x, fresh pool, FSB qbar=1000 plain: largest loss over the emp, gt and est attackers at q=1000 | 16.06 | pp | `` |
| `C6_M2x_qbar1000_floor256_emp_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1 | 0.16 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor256_gt_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1 | 0.16 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_est_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_worst_q1` | M2x, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1 | 0.16 | pp | `` |
| `C6_M2x_qbar1000_floor256_emp_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1000 | 14.98 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor256_gt_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1000 | 14.94 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_est_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_worst_qbar` | M2x, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1000 | 14.98 | pp | `` |
| `C6_M2x_qbar1000_floor256_emp_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor256, emp attacker: loss at q=1000 | 14.98 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor256_gt_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor256, gt attacker: loss at q=1000 | 14.94 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_est_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor256, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor256_worst_q1000` | M2x, fresh pool, FSB qbar=1000 floor256: largest loss over the emp, gt and est attackers at q=1000 | 14.98 | pp | `` |
| `C6_M2x_qbar1000_floor1024_emp_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1 | -0.01 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_gt_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1 | -0.01 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_est_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_worst_q1` | M2x, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar1000_floor1024_emp_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1000 | 11.66 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_gt_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1000 | 11.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_est_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_worst_qbar` | M2x, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 11.66 | pp | `` |
| `C6_M2x_qbar1000_floor1024_emp_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor1024, emp attacker: loss at q=1000 | 11.66 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_gt_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor1024, gt attacker: loss at q=1000 | 11.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_est_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor1024, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor1024_worst_q1000` | M2x, fresh pool, FSB qbar=1000 floor1024: largest loss over the emp, gt and est attackers at q=1000 | 11.66 | pp | `` |
| `C6_M2x_qbar1000_floor2048_emp_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1 | -0.05 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_gt_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1 | -0.03 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_est_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_worst_q1` | M2x, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar1000_floor2048_emp_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1000 | 5.83 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_gt_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1000 | 6.91 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_est_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_worst_qbar` | M2x, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 6.91 | pp | `` |
| `C6_M2x_qbar1000_floor2048_emp_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor2048, emp attacker: loss at q=1000 | 5.83 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_gt_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor2048, gt attacker: loss at q=1000 | 6.91 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_est_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor2048, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor2048_worst_q1000` | M2x, fresh pool, FSB qbar=1000 floor2048: largest loss over the emp, gt and est attackers at q=1000 | 6.91 | pp | `` |
| `C6_M2x_qbar1000_floor4096_emp_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1 | 0.00 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_gt_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_est_loss_q1` | M2x, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1 | 0.00 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_worst_q1` | M2x, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1 | 0.00 | pp | `` |
| `C6_M2x_qbar1000_floor4096_emp_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1000 | 1.11 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_gt_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1000 | 5.81 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_est_loss_qbar` | M2x, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_worst_qbar` | M2x, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 5.81 | pp | `` |
| `C6_M2x_qbar1000_floor4096_emp_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor4096, emp attacker: loss at q=1000 | 1.11 | pp | `e1g_floor_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_gt_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor4096, gt attacker: loss at q=1000 | 5.81 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_est_loss_q1000` | M2x, fresh pool, FSB qbar=1000 floor4096, est attacker: loss at q=1000 | 3.61 | pp | `e1g_robust_fresh.csv` |
| `C6_M2x_qbar1000_floor4096_worst_q1000` | M2x, fresh pool, FSB qbar=1000 floor4096: largest loss over the emp, gt and est attackers at q=1000 | 5.81 | pp | `` |
| `C6_M2x_qbar1000_hpb_emp_loss_qbar` | M2x, fresh pool, matched HPB, emp: loss at q=qbar=1000 | 30.01 | pp | `e1g_floor_fresh.csv` |
| `C6_qbar10_plain_avg` | FSB qbar=10 plain: average bucket size | 790.21 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor256_avg` | FSB qbar=10 floor256: average bucket size | 966.67 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor256_avg_ratio` | FSB qbar=10 floor256: average bucket size relative to plain FSB with the same qbar | 1.22 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor1024_avg` | FSB qbar=10 floor1024: average bucket size | 1516.07 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor1024_avg_ratio` | FSB qbar=10 floor1024: average bucket size relative to plain FSB with the same qbar | 1.92 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor2048_avg` | FSB qbar=10 floor2048: average bucket size | 2252.76 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor2048_avg_ratio` | FSB qbar=10 floor2048: average bucket size relative to plain FSB with the same qbar | 2.85 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor4096_avg` | FSB qbar=10 floor4096: average bucket size | 3776.07 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar10_floor4096_avg_ratio` | FSB qbar=10 floor4096: average bucket size relative to plain FSB with the same qbar | 4.78 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar100_plain_avg` | FSB qbar=100 plain: average bucket size | 2564.83 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor256_avg` | FSB qbar=100 floor256: average bucket size | 2734.44 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor256_avg_ratio` | FSB qbar=100 floor256: average bucket size relative to plain FSB with the same qbar | 1.07 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor1024_avg` | FSB qbar=100 floor1024: average bucket size | 3275.60 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor1024_avg_ratio` | FSB qbar=100 floor1024: average bucket size relative to plain FSB with the same qbar | 1.28 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor2048_avg` | FSB qbar=100 floor2048: average bucket size | 4006.55 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor2048_avg_ratio` | FSB qbar=100 floor2048: average bucket size relative to plain FSB with the same qbar | 1.56 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor4096_avg` | FSB qbar=100 floor4096: average bucket size | 5476.27 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar100_floor4096_avg_ratio` | FSB qbar=100 floor4096: average bucket size relative to plain FSB with the same qbar | 2.14 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar1000_plain_avg` | FSB qbar=1000 plain: average bucket size | 11,336 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor256_avg` | FSB qbar=1000 floor256: average bucket size | 11,493 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor256_avg_ratio` | FSB qbar=1000 floor256: average bucket size relative to plain FSB with the same qbar | 1.01 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor1024_avg` | FSB qbar=1000 floor1024: average bucket size | 12,010 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor1024_avg_ratio` | FSB qbar=1000 floor1024: average bucket size relative to plain FSB with the same qbar | 1.06 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor2048_avg` | FSB qbar=1000 floor2048: average bucket size | 12,722 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor2048_avg_ratio` | FSB qbar=1000 floor2048: average bucket size relative to plain FSB with the same qbar | 1.12 | ratio | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor4096_avg` | FSB qbar=1000 floor4096: average bucket size | 14,167 | entries | `e1g_floor_fresh.csv` |
| `C6_qbar1000_floor4096_avg_ratio` | FSB qbar=1000 floor4096: average bucket size relative to plain FSB with the same qbar | 1.25 | ratio | `e1g_floor_fresh.csv` |

## C7 Stability across four splits of the leak (A_test of each split; worst case over emp, gt, est) (49 numbers)

| id | description | value | unit | source |
|---|---|---|---|---|
| `C7_M0_plain_q1_worst_mean` | M0, plain, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 5.03 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q1_worst_sd` | M0, plain, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.19 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q1_worst_min` | M0, plain, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 4.82 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q1_worst_max` | M0, plain, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 5.28 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q100_worst_mean` | M0, plain, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 10.96 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q100_worst_sd` | M0, plain, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.06 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q100_worst_min` | M0, plain, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 10.89 | pp | `e1h_splits.csv` |
| `C7_M0_plain_q100_worst_max` | M0, plain, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 11.02 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q1_worst_mean` | M0, floor2048, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 0.00 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q1_worst_sd` | M0, floor2048, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.00 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q1_worst_min` | M0, floor2048, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 0.00 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q1_worst_max` | M0, floor2048, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 0.00 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q100_worst_mean` | M0, floor2048, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 0.10 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q100_worst_sd` | M0, floor2048, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.03 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q100_worst_min` | M0, floor2048, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 0.06 | pp | `e1h_splits.csv` |
| `C7_M0_floor2048_q100_worst_max` | M0, floor2048, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 0.14 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q1_worst_mean` | M0, hpb, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 14.59 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q1_worst_sd` | M0, hpb, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.08 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q1_worst_min` | M0, hpb, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 14.54 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q1_worst_max` | M0, hpb, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 14.71 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q100_worst_mean` | M0, hpb, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 41.19 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q100_worst_sd` | M0, hpb, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.20 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q100_worst_min` | M0, hpb, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 41.00 | pp | `e1h_splits.csv` |
| `C7_M0_hpb_q100_worst_max` | M0, hpb, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 41.45 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q1_worst_mean` | M2x, plain, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 9.78 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q1_worst_sd` | M2x, plain, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.11 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q1_worst_min` | M2x, plain, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 9.67 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q1_worst_max` | M2x, plain, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 9.93 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q100_worst_mean` | M2x, plain, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 15.02 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q100_worst_sd` | M2x, plain, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.22 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q100_worst_min` | M2x, plain, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 14.79 | pp | `e1h_splits.csv` |
| `C7_M2x_plain_q100_worst_max` | M2x, plain, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 15.26 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q1_worst_mean` | M2x, floor2048, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 0.002 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q1_worst_sd` | M2x, floor2048, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.004 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q1_worst_min` | M2x, floor2048, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 0.00 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q1_worst_max` | M2x, floor2048, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 0.008 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q100_worst_mean` | M2x, floor2048, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 2.23 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q100_worst_sd` | M2x, floor2048, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.06 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q100_worst_min` | M2x, floor2048, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 2.16 | pp | `e1h_splits.csv` |
| `C7_M2x_floor2048_q100_worst_max` | M2x, floor2048, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 2.30 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q1_worst_mean` | M2x, hpb, qbar=100, q=1: mean over 4 splits of the per-split largest loss over emp, gt, est | 9.79 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q1_worst_sd` | M2x, hpb, qbar=100, q=1: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.08 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q1_worst_min` | M2x, hpb, qbar=100, q=1: min over 4 splits of the per-split largest loss over emp, gt, est | 9.68 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q1_worst_max` | M2x, hpb, qbar=100, q=1: max over 4 splits of the per-split largest loss over emp, gt, est | 9.87 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q100_worst_mean` | M2x, hpb, qbar=100, q=100: mean over 4 splits of the per-split largest loss over emp, gt, est | 30.68 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q100_worst_sd` | M2x, hpb, qbar=100, q=100: sd over 4 splits of the per-split largest loss over emp, gt, est | 0.07 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q100_worst_min` | M2x, hpb, qbar=100, q=100: min over 4 splits of the per-split largest loss over emp, gt, est | 30.58 | pp | `e1h_splits.csv` |
| `C7_M2x_hpb_q100_worst_max` | M2x, hpb, qbar=100, q=100: max over 4 splits of the per-split largest loss over emp, gt, est | 30.74 | pp | `e1h_splits.csv` |
| `C7_n_splits` | number of independent splits of the leak | 4.00 | splits | `e1h_splits.csv` |
