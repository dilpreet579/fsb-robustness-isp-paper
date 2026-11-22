# REPORT 1h (Phase 1h: four splits of the leak)

Numbers and method statements only. Earlier results were not modified; Phase 1h adds `experiments/e1h_splits.py`, `experiments/report1h.py`, `results/e1h_splits*` and the argument `split_seeds` of `experiments.common.World` (default unchanged: split seeds 101, 102, 103).

## Method

- Four independent account splits of RockYou: seeds (a, b, dev) = (101, 102, 103) (the paper's split), (111, 112, 113), (121, 122, 123), (131, 132, 133); each split has its own 90% leak S~, server estimate (t = 1M), attackers and held-out target pool A_test.
- Configurations fixed in advance, nothing selected: plain FSB qbar = 100, FSB qbar = 100 with floor g = 2,048 (chosen on the first split's development pool, so the other three splits are out of sample for it), HPB size-matched by `hpb_l_for`. Conditions M0 and M2x. Attackers emp, gt, est, all over all of S~. Target seed 2000, 5 repeats x 5,000 targets, q in {1, 10, 100, 1000}.

## Largest loss over emp, gt and est, per split (points)

| cond | scheme | q | split 101 | split 111 | split 121 | split 131 | mean | sd | min | max |
|---|---|---|---|---|---|---|---|---|---|---|
| M0 | plain FSB | 1 | 4.99 | 5.28 | 4.82 | 5.01 | 5.03 | 0.19 | 4.82 | 5.28 |
| M0 | plain FSB | 100 | 10.92 | 11.02 | 11.00 | 10.89 | 10.96 | 0.06 | 10.89 | 11.02 |
| M0 | floor 2,048 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| M0 | floor 2,048 | 100 | 0.06 | 0.12 | 0.09 | 0.14 | 0.10 | 0.03 | 0.06 | 0.14 |
| M0 | matched HPB | 1 | 14.55 | 14.54 | 14.55 | 14.71 | 14.59 | 0.08 | 14.54 | 14.71 |
| M0 | matched HPB | 100 | 41.06 | 41.45 | 41.23 | 41.00 | 41.19 | 0.20 | 41.00 | 41.45 |
| M2x | plain FSB | 1 | 9.78 | 9.93 | 9.67 | 9.74 | 9.78 | 0.11 | 9.67 | 9.93 |
| M2x | plain FSB | 100 | 14.79 | 15.26 | 15.14 | 14.91 | 15.02 | 0.22 | 14.79 | 15.26 |
| M2x | floor 2,048 | 1 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 |
| M2x | floor 2,048 | 100 | 2.30 | 2.16 | 2.26 | 2.19 | 2.23 | 0.06 | 2.16 | 2.30 |
| M2x | matched HPB | 1 | 9.84 | 9.87 | 9.77 | 9.68 | 9.79 | 0.08 | 9.68 | 9.87 |
| M2x | matched HPB | 100 | 30.70 | 30.58 | 30.70 | 30.74 | 30.68 | 0.07 | 30.58 | 30.74 |

Average bucket size per split (M0, plain FSB / floor 2,048 / HPB): split 101: 2,565 / 4,007 / 3,204; split 111: 2,567 / 4,009 / 3,205; split 121: 2,562 / 4,004 / 3,205; split 131: 2,583 / 4,025 / 3,204

Runtime: 8.4 minutes (sum of per-run seconds), peak RSS 5.86 GB.

## Reproduce

    make e1h-splits report1h
