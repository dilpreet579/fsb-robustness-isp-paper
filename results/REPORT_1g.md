# REPORT 1g (Phase 1g: a floor on gamma)

Numbers and method statements only. Earlier phases' results were not modified; Phase 1g adds `results/e1g_*`, `experiments/e1g_floor.py`, `experiments/e1g_robust.py`, `experiments/report1g.py`, `tests/test_phase1g.py`, the class `FSBFloor` in `c3sim/attacker.py` and the attacker model `gt` (`World.gt_weights`) in `experiments/common.py`. The paper (`paper/`) was not changed.

## 1. What was run

- **Scheme (`FSBFloor`)**: gamma(w) = min(|B|, max(gamma_FSB(w), g)) for every string w (a function of the string only, so the client computes it without knowing whether w is stored). g = 1 is plain FSB. t = 1,000,000, |B| = 2^24, N = 13,125,513.
- **Grid**: qbar in {10, 100, 1000}, g in {2, 4, 16, 64, 256, 1024, 2048, 4096, 8192, 16384}; plain FSB qbar sweep {1, 3, 10, 30, 100, 300, 1000, 3000}; size-matched HPB for qbar in {10, 100, 1000}. Conditions M0 and M2x.
- **Pools and seeds**: tuned on A_dev (seed 5000), reported on A_fresh (seed 6000), 5 repeats x 5,000 targets; the fresh run is done once (the scripts refuse to rerun it). A `--fast` smoke run (2,000 x 3, A_dev) preceded the full dev run; it is kept as `e1g_floor_dev_fast_smoke*`.
- **Attackers**: `emp` = raw leak counts over all of S~ (the headline attacker of the paper); `est` = the server's estimate over all of S~; `gt` = Good-Turing adjusted counts (Turing r* = (r+1) n_{r+1}/n_r for counts r <= 5, raw above). `est` and `gt` were added after the dev run of `emp` showed non-monotone and negative losses (section 4), and were fixed before any fresh-pool run of them. [gt] adjusted counts r* for r=1..5: [0.215, 0.884, 1.9, 2.996, 4.0]

Reference counts (dev log): count of rank-10 password = 15,003; |B| / count = 1,118 copies for a count-1 password; count of rank-100 password = 5,410; |B| / count = 3,101 copies for a count-1 password; count of rank-1000 password = 1,209; |B| / count = 13,877 copies for a count-1 password

## 2. Pre-registered selection (dev pool only)

Rule (written in `e1g_floor.py` before the dev run): score = mean over M0 and M2x of [floored loss at q = 100] - [plain-FSB loss at q = 100 interpolated at the same average bucket size], emp attacker; lowest score wins.

Result: `selected on dev: qbar=10 floor=256 (score -12.65); 0 configurations outside the qbar sweep size range were not scored`

The selected configuration (qbar = 10) is evaluated at q = 100, i.e. beyond its qbar, and against the raw-count attacker only; section 4 shows that this attacker is not the strongest one. The rule is reported as specified; a rule that scores loss at q = qbar against the worst attacker was not run as a selection.

## 3. M0, fresh pool, qbar = 100: loss in points at q = 1, 10, 100 and 1000

| config | avg bucket | emp q=1 | emp q=10 | emp q=100 | emp q=1000 | gt q=1 | gt q=10 | gt q=100 | gt q=1000 | est q=1 | est q=10 | est q=100 | est q=1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qbar=100 plain FSB | 2,565 | +4.87 ±0.43 | +9.16 ±0.60 | +10.68 ±0.64 | +24.32 ±0.39 | +4.98 ±0.36 | +9.24 ±0.54 | +10.52 ±0.59 | +24.17 ±0.40 | +0.00 ±0.00 | +0.00 ±0.00 | +0.00 ±0.00 | +11.49 ±0.31 |
| qbar=100 floor 256 | 2,734 | +0.00 ±0.00 | +0.40 ±0.24 | +3.27 ±0.47 | +20.26 ±0.54 | +0.00 ±0.00 | +0.58 ±0.17 | +3.74 ±0.50 | +20.13 ±0.53 | +0.00 ±0.00 | +0.00 ±0.00 | +0.00 ±0.00 | +11.45 ±0.32 |
| qbar=100 floor 1024 | 3,276 | +0.00 ±0.00 | -0.12 ±0.08 | +1.19 ±0.45 | +8.36 ±0.79 | +0.00 ±0.00 | +0.06 ±0.05 | +1.80 ±0.49 | +15.60 ±0.29 | +0.00 ±0.00 | +0.00 ±0.00 | +0.00 ±0.00 | +11.45 ±0.32 |
| qbar=100 floor 2048 | 4,007 | +0.00 ±0.00 | -0.06 ±0.07 | -0.32 ±0.36 | +0.24 ±0.70 | +0.00 ±0.00 | -0.04 ±0.05 | +0.08 ±0.18 | +13.94 ±0.28 | +0.00 ±0.00 | +0.00 ±0.00 | +0.00 ±0.00 | +11.45 ±0.32 |
| qbar=100 floor 4096 | 5,476 | +0.00 ±0.00 | +0.00 ±0.00 | -0.52 ±0.16 | +10.64 ±0.32 | +0.00 ±0.00 | +0.00 ±0.00 | +0.04 ±0.18 | +13.73 ±0.33 | +0.00 ±0.00 | +0.00 ±0.00 | +0.00 ±0.00 | +11.46 ±0.33 |
| qbar=100 floor 8192 | 8,436 | +0.00 ±0.00 | +0.00 ±0.00 | +0.02 ±0.17 | +13.76 ±0.34 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| qbar=100 floor 16384 | 14,590 | +0.00 ±0.00 | +0.00 ±0.00 | +0.02 ±0.17 | +13.76 ±0.34 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| size-matched HPB l=12 | 3,204 | +14.36 ±0.10 | +27.96 ±0.41 | +41.51 ±0.67 | +45.11 ±0.14 | +14.36 ±0.10 | +27.96 ±0.41 | +41.51 ±0.67 | +45.11 ±0.14 | +13.78 ±0.09 | +27.78 ±0.44 | +41.78 ±0.61 | +46.14 ±0.22 |

`n/a` = not run for that attacker (est and gt were run for floors 256, 1024, 2048, 4096 only). Values are mean ±sd over 5 repeats. A negative loss means the attacker did worse with the bucket than the same attacker without it.

## 3. M2x, fresh pool, qbar = 100: loss in points at q = 1, 10, 100 and 1000

| config | avg bucket | emp q=1 | emp q=10 | emp q=100 | emp q=1000 | gt q=1 | gt q=10 | gt q=100 | gt q=1000 | est q=1 | est q=10 | est q=100 | est q=1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qbar=100 plain FSB | 2,565 | +9.50 ±0.35 | +12.44 ±0.48 | +14.54 ±0.45 | +39.50 ±0.75 | +9.52 ±0.34 | +12.40 ±0.46 | +14.50 ±0.45 | +39.50 ±0.75 | +0.00 ±0.00 | +0.05 ±0.04 | +2.12 ±0.14 | +39.50 ±0.75 |
| qbar=100 floor 256 | 2,734 | +0.20 ±0.13 | +2.66 ±0.25 | +7.70 ±0.38 | +39.50 ±0.75 | +0.19 ±0.13 | +2.66 ±0.24 | +7.71 ±0.40 | +39.50 ±0.75 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.18 | +39.48 ±0.73 |
| qbar=100 floor 1024 | 3,276 | -0.02 ±0.09 | +0.26 ±0.30 | +2.00 ±0.12 | +27.51 ±0.76 | -0.02 ±0.09 | +0.26 ±0.30 | +4.02 ±0.18 | +32.72 ±0.56 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.18 | +33.86 ±0.57 |
| qbar=100 floor 2048 | 4,007 | -0.06 ±0.05 | -0.20 ±0.23 | +1.44 ±0.18 | +6.03 ±0.40 | -0.03 ±0.04 | -0.03 ±0.13 | +2.12 ±0.19 | +31.34 ±0.64 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.18 | +31.18 ±0.44 |
| qbar=100 floor 4096 | 5,476 | +0.00 ±0.00 | -0.16 ±0.13 | -0.16 ±0.23 | +30.53 ±0.56 | +0.00 ±0.00 | +0.03 ±0.12 | +2.12 ±0.17 | +30.56 ±0.54 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.18 | +29.47 ±0.39 |
| qbar=100 floor 8192 | 8,436 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.20 | +28.88 ±0.45 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| qbar=100 floor 16384 | 14,590 | +0.00 ±0.00 | +0.05 ±0.07 | +2.16 ±0.20 | +27.25 ±0.46 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| size-matched HPB l=12 | 3,204 | +9.57 ±0.33 | +20.30 ±0.52 | +30.74 ±0.41 | +33.44 ±0.64 | +9.57 ±0.33 | +20.30 ±0.52 | +30.74 ±0.41 | +33.44 ±0.64 | +9.57 ±0.33 | +20.30 ±0.52 | +30.74 ±0.43 | +34.82 ±0.59 |

`n/a` = not run for that attacker (est and gt were run for floors 256, 1024, 2048, 4096 only). Values are mean ±sd over 5 repeats. A negative loss means the attacker did worse with the bucket than the same attacker without it.

### M0, fresh pool, qbar = 10: loss in points at q = 1, 10, 1000

| config | avg bucket | emp q=1 | emp q=10 | emp q=1000 | gt q=1 | gt q=10 | gt q=1000 | est q=1 | est q=10 | est q=1000 |
|---|---|---|---|---|---|---|---|---|---|---|
| qbar=10 plain FSB | 790 | +5.71 ±0.49 | +10.40 ±0.57 | +51.77 ±0.38 | +5.76 ±0.49 | +10.30 ±0.60 | +51.77 ±0.38 | +0.00 ±0.00 | +0.00 ±0.00 | +52.37 ±0.35 |
| qbar=10 floor 256 | 967 | +0.00 ±0.00 | +0.54 ±0.23 | +51.77 ±0.38 | +0.00 ±0.00 | +0.65 ±0.21 | +51.77 ±0.38 | +0.00 ±0.00 | +0.00 ±0.00 | +52.32 ±0.37 |
| qbar=10 floor 1024 | 1,516 | +0.00 ±0.00 | -0.12 ±0.07 | +46.01 ±0.21 | +0.00 ±0.00 | +0.09 ±0.09 | +46.04 ±0.22 | +0.00 ±0.00 | +0.00 ±0.00 | +46.76 ±0.31 |
| qbar=10 floor 2048 | 2,253 | +0.00 ±0.00 | -0.03 ±0.07 | +44.53 ±0.17 | +0.00 ±0.00 | +0.06 ±0.10 | +44.56 ±0.16 | +0.00 ±0.00 | +0.00 ±0.00 | +44.58 ±0.19 |
| qbar=10 floor 4096 | 3,776 | +0.00 ±0.00 | +0.06 ±0.10 | +43.19 ±0.14 | +0.00 ±0.00 | +0.06 ±0.10 | +43.19 ±0.14 | +0.00 ±0.00 | +0.00 ±0.00 | +42.78 ±0.37 |
| qbar=10 floor 8192 | 6,906 | +0.00 ±0.00 | +0.06 ±0.10 | +40.69 ±0.44 | n/a | n/a | n/a | n/a | n/a | n/a |
| qbar=10 floor 16384 | 13,243 | +0.00 ±0.00 | +0.06 ±0.10 | +37.74 ±0.34 | n/a | n/a | n/a | n/a | n/a | n/a |
| size-matched HPB l=14 | 801 | +21.22 ±0.35 | +37.41 ±0.60 | +51.77 ±0.38 | +21.22 ±0.35 | +37.41 ±0.60 | +51.77 ±0.38 | +20.75 ±0.36 | +37.30 ±0.66 | +52.37 ±0.35 |

### M0, fresh pool, qbar = 1000: loss in points at q = 1, 1000

| config | avg bucket | emp q=1 | emp q=1000 | gt q=1 | gt q=1000 | est q=1 | est q=1000 |
|---|---|---|---|---|---|---|---|
| qbar=1000 plain FSB | 11,336 | +3.97 ±0.52 | +10.70 ±0.68 | +4.04 ±0.47 | +10.55 ±0.69 | +0.00 ±0.00 | +0.00 ±0.00 |
| qbar=1000 floor 256 | 11,493 | +0.00 ±0.00 | +9.93 ±0.67 | +0.00 ±0.00 | +9.88 ±0.70 | +0.00 ±0.00 | +0.00 ±0.00 |
| qbar=1000 floor 1024 | 12,010 | +0.00 ±0.00 | +6.35 ±0.92 | +0.00 ±0.00 | +6.12 ±0.88 | +0.00 ±0.00 | +0.00 ±0.00 |
| qbar=1000 floor 2048 | 12,722 | +0.00 ±0.00 | -0.18 ±0.83 | +0.00 ±0.00 | +2.72 ±0.49 | +0.00 ±0.00 | +0.00 ±0.00 |
| qbar=1000 floor 4096 | 14,167 | +0.00 ±0.00 | -0.82 ±0.67 | +0.00 ±0.00 | +2.19 ±0.44 | +0.00 ±0.00 | +0.00 ±0.00 |
| qbar=1000 floor 8192 | 17,085 | +0.00 ±0.00 | +0.48 ±0.55 | n/a | n/a | n/a | n/a |
| qbar=1000 floor 16384 | 22,956 | +0.00 ±0.00 | -1.02 ±0.30 | n/a | n/a | n/a | n/a |
| size-matched HPB l=10 | 12,818 | +8.76 ±0.33 | +40.32 ±0.46 | +8.76 ±0.33 | +40.32 ±0.46 | +8.23 ±0.24 | +40.80 ±0.51 |

### M2x, fresh pool, qbar = 10: loss in points at q = 1, 10, 1000

| config | avg bucket | emp q=1 | emp q=10 | emp q=1000 | gt q=1 | gt q=10 | gt q=1000 | est q=1 | est q=10 | est q=1000 |
|---|---|---|---|---|---|---|---|---|---|---|
| qbar=10 plain FSB | 790 | +9.95 ±0.37 | +13.44 ±0.52 | +39.50 ±0.75 | +9.98 ±0.39 | +13.40 ±0.52 | +39.50 ±0.75 | +0.08 ±0.09 | +1.11 ±0.25 | +39.50 ±0.75 |
| qbar=10 floor 256 | 967 | +0.20 ±0.13 | +2.68 ±0.26 | +39.50 ±0.75 | +0.19 ±0.13 | +2.80 ±0.25 | +39.50 ±0.75 | +0.11 ±0.07 | +1.09 ±0.21 | +39.50 ±0.75 |
| qbar=10 floor 1024 | 1,516 | -0.02 ±0.09 | +0.26 ±0.30 | +39.50 ±0.75 | +0.07 ±0.04 | +1.06 ±0.15 | +39.50 ±0.75 | +0.11 ±0.07 | +1.09 ±0.21 | +39.50 ±0.75 |
| qbar=10 floor 2048 | 2,253 | -0.01 ±0.03 | +1.00 ±0.15 | +36.78 ±0.68 | +0.11 ±0.07 | +1.08 ±0.18 | +36.78 ±0.68 | +0.11 ±0.07 | +1.09 ±0.21 | +37.88 ±0.75 |
| qbar=10 floor 4096 | 3,776 | +0.11 ±0.07 | +1.08 ±0.18 | +32.74 ±0.64 | +0.11 ±0.07 | +1.08 ±0.18 | +32.74 ±0.64 | +0.11 ±0.07 | +1.09 ±0.21 | +33.84 ±0.56 |
| qbar=10 floor 8192 | 6,906 | +0.11 ±0.07 | +1.08 ±0.18 | +31.16 ±0.67 | n/a | n/a | n/a | n/a | n/a | n/a |
| qbar=10 floor 16384 | 13,243 | +0.11 ±0.07 | +1.07 ±0.15 | +29.45 ±0.52 | n/a | n/a | n/a | n/a | n/a | n/a |
| size-matched HPB l=14 | 801 | +14.74 ±0.52 | +27.93 ±0.38 | +39.50 ±0.75 | +14.74 ±0.52 | +27.93 ±0.38 | +39.50 ±0.75 | +14.74 ±0.52 | +27.93 ±0.39 | +39.50 ±0.75 |

### M2x, fresh pool, qbar = 1000: loss in points at q = 1, 1000

| config | avg bucket | emp q=1 | emp q=1000 | gt q=1 | gt q=1000 | est q=1 | est q=1000 |
|---|---|---|---|---|---|---|---|
| qbar=1000 plain FSB | 11,336 | +8.34 ±0.33 | +16.06 ±0.39 | +8.41 ±0.38 | +16.02 ±0.40 | +0.00 ±0.00 | +3.63 ±0.16 |
| qbar=1000 floor 256 | 11,493 | +0.16 ±0.13 | +14.98 ±0.47 | +0.16 ±0.13 | +14.94 ±0.46 | +0.00 ±0.00 | +3.61 ±0.15 |
| qbar=1000 floor 1024 | 12,010 | -0.01 ±0.08 | +11.66 ±0.37 | -0.01 ±0.08 | +11.61 ±0.37 | +0.00 ±0.00 | +3.61 ±0.15 |
| qbar=1000 floor 2048 | 12,722 | -0.05 ±0.06 | +5.83 ±0.52 | -0.03 ±0.05 | +6.91 ±0.38 | +0.00 ±0.00 | +3.61 ±0.15 |
| qbar=1000 floor 4096 | 14,167 | +0.00 ±0.00 | +1.11 ±0.36 | +0.00 ±0.00 | +5.81 ±0.28 | +0.00 ±0.00 | +3.61 ±0.15 |
| qbar=1000 floor 8192 | 17,085 | +0.00 ±0.00 | +0.28 ±0.34 | n/a | n/a | n/a | n/a |
| qbar=1000 floor 16384 | 22,956 | +0.00 ±0.00 | +1.49 ±0.16 | n/a | n/a | n/a | n/a |
| size-matched HPB l=10 | 12,818 | +5.75 ±0.21 | +30.01 ±0.48 | +5.75 ±0.21 | +30.01 ±0.48 | +5.75 ±0.21 | +29.06 ±0.44 |

## 4. Worst case over the three attackers (fresh pool)

Largest loss over emp, gt and est, at the largest q <= qbar and at q = 1000, and the average bucket size relative to plain FSB with the same qbar. Floors 8192 and 16384 were run for emp only and are not in this table.

| cond | qbar | config | avg bucket (x plain FSB) | worst loss at q = qbar | worst loss at q = 1000 |
|---|---|---|---|---|---|
| M0 | 10 | plain FSB | 790 (1.00x) | +10.40 | +52.37 |
| M0 | 10 | floor 256 | 967 (1.22x) | +0.65 | +52.32 |
| M0 | 10 | floor 1024 | 1,516 (1.92x) | +0.09 | +46.76 |
| M0 | 10 | floor 2048 | 2,253 (2.85x) | +0.06 | +44.58 |
| M0 | 10 | floor 4096 | 3,776 (4.78x) | +0.06 | +43.19 |
| M0 | 100 | plain FSB | 2,565 (1.00x) | +10.68 | +24.32 |
| M0 | 100 | floor 256 | 2,734 (1.07x) | +3.74 | +20.26 |
| M0 | 100 | floor 1024 | 3,276 (1.28x) | +1.80 | +15.60 |
| M0 | 100 | floor 2048 | 4,007 (1.56x) | +0.08 | +13.94 |
| M0 | 100 | floor 4096 | 5,476 (2.14x) | +0.04 | +13.73 |
| M0 | 1000 | plain FSB | 11,336 (1.00x) | +10.70 | +10.70 |
| M0 | 1000 | floor 256 | 11,493 (1.01x) | +9.93 | +9.93 |
| M0 | 1000 | floor 1024 | 12,010 (1.06x) | +6.35 | +6.35 |
| M0 | 1000 | floor 2048 | 12,722 (1.12x) | +2.72 | +2.72 |
| M0 | 1000 | floor 4096 | 14,167 (1.25x) | +2.19 | +2.19 |
| M2x | 10 | plain FSB | 790 (1.00x) | +13.44 | +39.50 |
| M2x | 10 | floor 256 | 967 (1.22x) | +2.80 | +39.50 |
| M2x | 10 | floor 1024 | 1,516 (1.92x) | +1.09 | +39.50 |
| M2x | 10 | floor 2048 | 2,253 (2.85x) | +1.09 | +37.88 |
| M2x | 10 | floor 4096 | 3,776 (4.78x) | +1.09 | +33.84 |
| M2x | 100 | plain FSB | 2,565 (1.00x) | +14.54 | +39.50 |
| M2x | 100 | floor 256 | 2,734 (1.07x) | +7.71 | +39.50 |
| M2x | 100 | floor 1024 | 3,276 (1.28x) | +4.02 | +33.86 |
| M2x | 100 | floor 2048 | 4,007 (1.56x) | +2.16 | +31.34 |
| M2x | 100 | floor 4096 | 5,476 (2.14x) | +2.16 | +30.56 |
| M2x | 1000 | plain FSB | 11,336 (1.00x) | +16.06 | +16.06 |
| M2x | 1000 | floor 256 | 11,493 (1.01x) | +14.98 | +14.98 |
| M2x | 1000 | floor 1024 | 12,010 (1.06x) | +11.66 | +11.66 |
| M2x | 1000 | floor 2048 | 12,722 (1.12x) | +6.91 | +6.91 |
| M2x | 1000 | floor 4096 | 14,167 (1.25x) | +5.81 | +5.81 |

Per-configuration gains against plain FSB at the same average bucket size (q = 100, dev and fresh): `e1g_floor_*_summary.txt` (emp), `e1g_robust_*_summary.txt` (est, gt).

## 4b. Checks

`tests/test_phase1g.py` (output in `e1g_tests.txt`): floor = 1 equals plain FSB; gamma >= floor and <= |B|; floor never lowers gamma; average bucket = sum(gamma)/|B|; the sorted-class lookup equals a naive scan on every 7th bucket with a floor; Good-Turing weights adjust counts <= rmax only.

## 5. Runtimes

| run | wall minutes (sum of per-run seconds) | peak RSS (GB) |
|---|---|---|
| e1g_floor_dev | 8.4 | 4.82 |
| e1g_floor_fresh | 8.5 | 5.16 |
| e1g_robust_dev | 9.2 | 4.81 |
| e1g_robust_fresh | 9.3 | 5.16 |

## 6. Reproduce

    .venv/bin/python -I -m pytest -q tests/test_phase1g.py
    make phase1g      # dev, fresh (once), robust dev, robust fresh (once), report
