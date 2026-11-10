# Everything is regenerated from the raw SecLists files. Python runs with -I (isolated: ignores cwd and PYTHONPATH).
# Run order (see README): venv, fetch, fetch-xato, data, test, then phase1, phase1b, phase1c, phase1d, phase1e (each ends with its report).
PY = .venv/bin/python -I
SECLISTS = https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords
R = results

.PHONY: all venv fetch fetch-xato data test phase1 phase1b phase1c phase1d phase1e \
        e1 e2 e3 worked figs report \
        e1b-basics e1b-m1b e1b-fix-dev e1b-fix-fresh report1b \
        e1c-e2 e1c-tsweep e1c-e3 e1c-fix-dev e1c-fix-fresh report1c \
        e1d-cap e1d-noise e1d-esterror e1d-m2 report1d \
        e1e-cost e1e-headline e1e-estconv e1e-fix e1e-tsweep e1e-tsweep-10m report1e

all: venv fetch fetch-xato data test phase1 phase1b phase1c phase1d phase1e

venv:
	uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt -e ".[test]"

fetch:
	mkdir -p data/rockyou data/phpbb
	test -f data/rockyou/rockyou-withcount.txt.tar.gz || curl -fsSL -o data/rockyou/rockyou-withcount.txt.tar.gz $(SECLISTS)/Leaked-Databases/rockyou-withcount.txt.tar.gz
	test -f data/phpbb/phpbb-withcount.txt || curl -fsSL -o data/phpbb/phpbb-withcount.txt $(SECLISTS)/Leaked-Databases/phpbb-withcount.txt

# Phase 1c M2x / Phase 1d ablation: banned list = first 370 lines of the Xato top-1000 (the brief's 10-million-password-list-top-1000.txt is not in SecLists)
fetch-xato:
	mkdir -p data/xato
	test -f data/xato/xato-net-10-million-passwords-1000.txt || curl -fsSL -o data/xato/xato-net-10-million-passwords-1000.txt $(SECLISTS)/Common-Credentials/xato-net-10-million-passwords-1000.txt

data:
	$(PY) -m experiments.data_report

# corpus-dependent tests skip (not error) when data/ and cache/ are absent
test:
	$(PY) -m pytest -q -s tests 2>&1 | tee $(R)/tests_all.txt

# ---- Phase 1: simulator, E1-E3 (t = 100,000) ----
phase1: e1 worked e2 e3 figs report
e1:
	$(PY) -m experiments.e1 | tee $(R)/E1_log.txt
e2:
	$(PY) -m experiments.e2 | tee $(R)/E2_log.txt
e3:
	$(PY) -m experiments.e3 | tee $(R)/E3_log.txt
worked:
	$(PY) -m experiments.worked_examples > $(R)/T4_worked_log.txt
figs:
	$(PY) -m experiments.figs
report:
	$(PY) -m experiments.report

# ---- Phase 1b: t = 1e6 sensitivity, M1b, calibration fix (dev, then ONE fresh run) ----
phase1b: e1b-basics e1b-m1b e1b-fix-dev e1b-fix-fresh report1b
e1b-basics:
	$(PY) -m experiments.e1b_basics > $(R)/e1b_basics_log.txt 2>&1
e1b-m1b:
	$(PY) -m experiments.e1b_m1b > $(R)/e1b_m1b_log.txt 2>&1
e1b-fix-dev:
	$(PY) -m experiments.e1b_fix --pool dev > $(R)/e1b_fix_dev_log.txt 2>&1
e1b-fix-fresh:
	test -f $(R)/e1b_fix_fresh.csv || $(PY) -m experiments.e1b_fix --pool fresh > $(R)/e1b_fix_fresh_log.txt 2>&1
report1b:
	$(PY) -m experiments.report1b

# ---- Phase 1c: t = 1e6 is primary ----
phase1c: e1c-e2 e1c-tsweep e1c-e3 e1c-fix-dev e1c-fix-fresh report1c
e1c-e2:
	$(PY) -m experiments.e1c_e2 > $(R)/e1c_e2_log.txt 2>&1
e1c-tsweep:
	$(PY) -m experiments.e1c_tsweep > $(R)/e1c_tsweep_log.txt 2>&1
e1c-e3:
	$(PY) -m experiments.e1c_e3 > $(R)/e1c_e3_log.txt 2>&1
e1c-fix-dev:
	$(PY) -m experiments.e1c_fix --pool dev > $(R)/e1c_fix_dev_log.txt 2>&1
e1c-fix-fresh:
	test -f $(R)/e1c_fix_fresh.csv || $(PY) -m experiments.e1c_fix --pool fresh > $(R)/e1c_fix_fresh_log.txt 2>&1
report1c:
	$(PY) -m experiments.report1c

# ---- Phase 1d: candidate cap, noise draws, estimator error, M2 ablation ----
phase1d: e1d-cap e1d-noise e1d-esterror e1d-m2 report1d
e1d-cap:
	$(PY) -m experiments.e1d_cap > $(R)/e1d_cap_log.txt 2>&1
e1d-noise:
	$(PY) -m experiments.e1d_noise > $(R)/e1d_noise_log.txt 2>&1
e1d-esterror:
	$(PY) -m experiments.e1d_esterror > $(R)/e1d_esterror_log.txt 2>&1
e1d-m2:
	$(PY) -m experiments.e1d_m2 > $(R)/e1d_m2_log.txt 2>&1
report1d:
	$(PY) -m experiments.report1d

# ---- Paper assets: figures, LaTeX tables, head-storage estimate, number map and its check (no new experiments; reads results/*.csv; head cost reads the corpora) ----
.PHONY: paper-assets
paper-assets:
	$(PY) -m experiments.paper_head_cost
	$(PY) -m experiments.paper_figs
	$(PY) -m experiments.paper_tables
	$(PY) -m experiments.paper_numbers
	$(PY) -m experiments.paper_captions
	$(PY) paper/check_numbers.py

# ---- Phase 1e: emp attacker = all of S~ (13.1M candidates) ----
phase1e: e1e-cost e1e-headline e1e-estconv e1e-fix e1e-tsweep e1e-tsweep-10m report1e
# cost probes: one fresh process per configuration (peak memory belongs to that configuration); run alone, before the heavy jobs
e1e-cost:
	rm -f $(R)/e1e_cost.csv
	$(PY) -m experiments.e1e_cost --model emp --cand 2M
	$(PY) -m experiments.e1e_cost --model emp --cand all
	$(PY) -m experiments.e1e_cost --model est --cand 2M
	$(PY) -m experiments.e1e_cost --model est --cand all
e1e-headline:
	$(PY) -m experiments.e1e_headline > $(R)/e1e_headline_log.txt 2>&1
e1e-estconv:
	$(PY) -m experiments.e1e_estconv > $(R)/e1e_estconv_log.txt 2>&1
e1e-fix:
	$(PY) -m experiments.e1e_fix > $(R)/e1e_fix_log.txt 2>&1
e1e-tsweep:
	$(PY) -m experiments.e1e_tsweep --ts 100000,300000,1000000,3000000 --out e1e_tsweep.csv > $(R)/e1e_tsweep_log.txt 2>&1
# t = 10M in its own process (memory-heavy case)
e1e-tsweep-10m:
	$(PY) -m experiments.e1e_tsweep --ts 10000000 --out e1e_tsweep_10M.csv > $(R)/e1e_tsweep_10M_log.txt 2>&1
report1e:
	$(PY) -m experiments.report1e
