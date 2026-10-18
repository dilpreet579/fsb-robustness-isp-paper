# Everything is regenerated from the raw SecLists files. Python runs with -I (isolated: ignores cwd and PYTHONPATH).
PY = .venv/bin/python -I
SECLISTS = https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases

.PHONY: all venv fetch data test e1 e2 e3 worked figs report
all: venv fetch data test e1 worked e2 e3 figs report

venv:
	uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt -e ".[test]"

fetch:
	mkdir -p data/rockyou data/phpbb
	test -f data/rockyou/rockyou-withcount.txt.tar.gz || curl -fsSL -o data/rockyou/rockyou-withcount.txt.tar.gz $(SECLISTS)/rockyou-withcount.txt.tar.gz
	test -f data/phpbb/phpbb-withcount.txt || curl -fsSL -o data/phpbb/phpbb-withcount.txt $(SECLISTS)/phpbb-withcount.txt

data:
	$(PY) -m experiments.data_report

test:
	$(PY) -m pytest -q -s tests 2>&1 | tee results/tests_all.txt

e1:
	$(PY) -m experiments.e1 | tee results/E1_log.txt
e2:
	$(PY) -m experiments.e2 | tee results/E2_log.txt
e3:
	$(PY) -m experiments.e3 | tee results/E3_log.txt
worked:
	$(PY) -m experiments.worked_examples > results/T4_worked_log.txt
figs:
	$(PY) -m experiments.figs
report:
	$(PY) -m experiments.report
