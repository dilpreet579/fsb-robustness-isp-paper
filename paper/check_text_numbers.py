"""Audit of the numbers printed in paper/main.tex (prose, captions, input tables) against the number map.
    .venv/bin/python -I paper/check_text_numbers.py
Reads paper/main.tex (+ the tables it \\input s), paper/numbers.csv, paper/head_cost.csv, results/data_report.md and a few results CSVs. Writes nothing except
paper/text_numbers_audit.tsv (one row per numeric token). It does NOT fix anything: every token that no source explains is printed with its line, exit code 1.

A token is explained by the first source that matches it, tried in this order:
  numbers.csv   value, x100 or /100 of a numbers.csv row, equal to the token at the token's printed precision (|diff| <= half a unit of the last printed digit)
  head_cost     paper/head_cost.csv (storage estimate), same rule
  data_report   corpus constants copied from results/data_report.md (only the four listed below, each verified to occur in that file)
  derived       explicit derived claims (formulae printed in the output), e.g. exp(bias)=350, 0.693/0.31 = 2 to 1, 76.9/7.5 = 10, "1%/25%/13% larger"
  constant      stated setup constants (|B| = 2^24, N, t, 5 repeats, 5,000 targets, bucket sizes, l = 14/12/10 ...), listed in CONSTANTS
  table-prov    token inside a table whose file is byte-identical to a regeneration by experiments/paper_tables.py (numbers.csv does not hold every table cell)
Integers below 100 matched only by numbers.csv/head_cost are flagged 'weak' (coincidence-prone); they are listed in the TSV, not in the unmatched list.
Excluded from the audit: years (1990-2030, no decimals), the \\date line, labels/refs/citations/lengths/colspecs, identifiers (M0, M1b, C3, SHA-256 ...)."""
import csv
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.environ.get("C3SIM_RESULTS", os.path.join(ROOT, "results"))
TEX = os.path.join(HERE, "main.tex")

# ------------------------------------------------------------------------------------------------------------- reference values
_ROWS = list(csv.DictReader(open(os.path.join(HERE, "numbers.csv"))))
NUM = [(r["id"], float(r["value"])) for r in _ROWS]
NUMD = dict(NUM)
UNIT = {r["id"]: r["unit"] for r in _ROWS}
HC = list(csv.DictReader(open(os.path.join(HERE, "head_cost.csv"))))
HEAD = []  # (label, value)
for r in HC:
    t = int(r["t"])
    for col in ("head_mass_share",):
        HEAD.append((f"head_cost t={t} {col} x100", float(r[col]) * 100))
    for col in ("plain_MB", "gzip9_MB", "prob_float32_MB", "plain_plus_prob_MB", "gzip9_plus_prob_MB", "trigram_float32_MB", "trigram_float64_MB"):
        HEAD.append((f"head_cost t={t} {col}", float(r[col])))
ABL = []  # blocklist-only (M2B) emp loss at q = qbar from the 2M-list ablation file; numbers.csv has no M2B rows (D28)
if os.path.exists(os.path.join(RES, "e1d_ablation.csv")):
    for _r in csv.DictReader(open(os.path.join(RES, "e1d_ablation.csv"))):
        if (_r["condition"], _r["scheme"], _r["variant"], _r.get("attacker")) == ("M2B", "fsb", "fsb_base", "emp") and _r["q"] == _r["param"]:
            ABL.append((f"e1d_ablation.csv M2B emp loss q=qbar={_r['q']}", float(_r["loss"])))
DR = open(os.path.join(RES, "data_report.md")).read() if os.path.exists(os.path.join(RES, "data_report.md")) else ""
DATA_REPORT = [("RockYou unique passwords", 14326970), ("RockYou accounts", 32581870), ("phpbb unique passwords", 184381), ("phpbb accounts", 255417)]
DATA_REPORT = [(n, v) for n, v in DATA_REPORT if f"{v:,}" in DR]  # only constants that really occur in results/data_report.md

CONSTANTS = {  # value -> stated setup constant (text states it as a definition, not as a measured result)
    24: "|B| = 2^24 buckets", 2 ** 24: "|B| = 2^24", 13125513: "N = |S~| (C5_emp_all_n_candidates)", 13.1e6: "N rounded (13.1M)",
    1e6: "t = 1,000,000 / 1M", 2e6: "2M candidate list", 14e6: "RockYou unique, rounded (14M)", 14.3e6: "RockYou unique, rounded (14.3M)",
    10e6: "t = 10M", 100e3: "t = 100k", 300e3: "t = 300k", 3e6: "t = 3M",
    5: "5 repeats / 5 draws / 5 folds / 5 pp threshold (5-point)", 5000: "5,000 targets per repeat", 25000: "25,000 bucket queries = 5 x 5,000",
    1: "q = 1 (and counts such as 'leak count 1')", 10: "q / qbar = 10", 100: "q / qbar = 100", 1000: "q / qbar = 1000", 2: "'1 or 2', '2 to 1'",
    14: "l = 14 bits", 12: "l = 12 bits", 10.0: "l = 10 bits / qbar", 3: "3-gram", 0.5: "sigma grid 0.5 / 0.5-decade bins", 1.0: "sigma grid 1.0", 1.6: "sigma grid 1.6",
    0.01: "add-delta smoothing delta = 0.01", 90: "90% training split", 8: "policy: length >= 8", 30: "cleaning: length 1 to 30", 370: "Xato top-370 blocklist",
    3000: "qbar sweep 1 to 3000 (e1e_fix.csv)", 0: "zero (e.g. sigma = 0)", 4: "4-byte probability",
    2000: "fix comparison bucket size (T4)", 6500: "fix comparison bucket size 6,500 entries (T4: 2,000 / 6,500 / 20,000)", 20000: "fix comparison bucket size (T4)",
}
# t grid sizes etc. from head_cost.csv are constants too
for r in HC:
    CONSTANTS[float(r["t"])] = "t sweep grid (paper/head_cost.csv)"


def _derived():
    """list of (label, formula text, value, tolerance, kind) ; kind 'abs' tolerance in the unit of the printed token, 'rel' relative."""
    d = []
    g = NUMD
    d.append(("factor of about 350 = exp(bias_tail)", "exp(C2_bias_tail_B)", math.exp(g["C2_bias_tail_B"]), 0.01, "rel"))
    for q, key in ((100, "C2_cross5_est_qbar100_mean"), (1000, "C2_cross5_est_qbar1000_mean")):
        d.append((f"margin 'about 2 to 1' = crossing(qbar={q}) / sigma_hat_head", f"{key} / C2_sigmahat_head_B", g[key] / g["C2_sigmahat_head_B"], 0.15, "rel2"))
    h1 = next(r for r in HC if int(r["t"]) == 1000000)
    h10 = next(r for r in HC if int(r["t"]) == 10000000)
    d.append(("'ten times' = head storage(10M) / head storage(1M)", "gzip9_plus_prob_MB 10M / 1M", float(h10["gzip9_plus_prob_MB"]) / float(h1["gzip9_plus_prob_MB"]), 0.05, "rel10"))
    for q in (10, 100, 1000):
        d.append((f"HPB larger than FSB by (%), qbar={q}", f"C1_M0_qbar{q}_hpb_avg / C1_M0_qbar{q}_fsb_avg - 1",
                  (g[f"C1_M0_qbar{q}_hpb_avg"] / g[f"C1_M0_qbar{q}_fsb_avg"] - 1) * 100, 0.5, "abs"))
    d.append(("'under 1%' / 'less than 1%' of HPB's loss removed (M2x, qbar=100, q=1)", "C3_M2x_qbar100_frac_removed_q1 x 100 < 1", g["C3_M2x_qbar100_frac_removed_q1"] * 100, None, "lt1"))
    d.append(("M2x qbar=1000 q=1: share of HPB loss removed by FSB (negative: FSB worse)", "1 - 8.584/6.056 (C3_M2x_qbar1000_emp_fsb_loss_q1 / _hpb_loss_q1)",
              (1 - g["C3_M2x_qbar1000_emp_fsb_loss_q1"] / g["C3_M2x_qbar1000_emp_hpb_loss_q1"]) * 100, 0.05, "neg"))
    return d


DERIVED = _derived()


def e1c_est_m0_qbar100_q1000():
    for r in csv.DictReader(open(os.path.join(RES, "e1c_e2.csv"))):
        if (r["condition"], r["scheme"], r["variant"], r["param"], r["attacker"], r["q"]) == ("M0", "fsb", "fsb_base", "100", "est", "1000"):
            return float(r["loss"])
    return float("nan")


# ------------------------------------------------------------------------------------------------------------- tex -> plain text
SKIP_LINE = re.compile(r"^\s*(\\renewcommand|\\setlength|\\label|\\input\{preamble|\\bibliography|\\nocite|\\date|\\title|\\author|\\includegraphics|\\documentclass|\\usepackage|\\clearpage|\\onecolumn|\\appendix|\\begin\{document\}|\\end\{document\})")
IDENT = re.compile(r"\bM[0-3][a-zA-Z]?\b|\bC[1-5]\b|SHA-\d+|MIGP 2\.0|\bl=?\b")


def source_lines():
    """(origin, lineno, text) with \\input expanded; comments removed."""
    out = []

    def add(path, label):
        for i, line in enumerate(open(path, encoding="utf8"), 1):
            line = re.sub(r"(?<!\\)%.*$", "", line.rstrip("\n"))
            m = re.match(r"^\s*\\input\{([^}]*)\}\s*$", line)
            if m and not m.group(1).startswith("preamble"):
                p = os.path.join(HERE, m.group(1))
                add(p, os.path.relpath(p, HERE))
                continue
            if line.strip():
                out.append((label, i, line))

    add(TEX, "main.tex")
    return out


def clean(line):
    s = line
    s = re.sub(r"\\begin\{(figure|table)\*?\}\[[^\]]*\]", " ", s)
    s = re.sub(r"\\begin\{tabular\}\{[^}]*\}|\\begin\{minipage\}\{[^}]*\}|\\begin\{tabular\}\{@\{\}.*\}$", " ", s)
    s = re.sub(r"\\(cmidrule)(\([a-z]+\))?\{[^}]*\}", " ", s)
    s = re.sub(r"\\multicolumn\{\d+\}\{[^}]*(\{[^}]*\})?[^}]*\}", " ", s)
    s = re.sub(r"\\(cite[a-z]*|ref|url|vspace|label)(\[[^\]]*\])*\{[^}]*\}", " ", s)
    s = re.sub(r"\\url\{[^}]*\}", " ", s)
    s = re.sub(r"p\{[^}]*\}", " ", s)
    s = re.sub(r"\{[0-9.]+(\\[a-z]+|pt|em|in)\}", " ", s)
    s = re.sub(r"\\\{[^}]*\\\}", lambda m: m.group(0).replace(",", ", "), s)  # sets \{10,100,1000\}: keep the commas from reading as thousands separators
    s = re.sub(r"\\(\{|\})", lambda m: " ", s)  # set braces \{ \}
    s = s.replace("{,}", ",").replace(r"\,", "").replace("~", " ").replace("$", "")
    s = s.replace(r"\%", "%").replace(r"\ ", " ")
    s = re.sub(r"(\d)\^\{?(\d+)\}?", lambda m: str(int(m.group(1)) ** int(m.group(2))), s)
    s = re.sub(r"\d\^\{?[a-z]\}?", " ", s)
    s = re.sub(r"\\(pm)\b", "±", s)
    s = re.sub(r"\\(times|approx|geq|ge|le|leq|in|min|ceil|lceil|rceil|left|right|frac|cdot|exp|sigma|gamma|delta|bar|hat|tilde|ldots)\b", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = s.replace("{", " ").replace("}", " ")
    return s


NUM_RE = re.compile(r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s?(?:%|k\b|M\b|B\b))?")


def tokens(text):
    text = re.sub(r"(\d)(\s+to\s+\d+(?:\.\d+)?%)", r"\1%\2", text)  # "72 to 73%": the first number of a percentage range is a percentage too
    for m in NUM_RE.finditer(IDENT.sub(" ", text)):
        raw = m.group(0)
        mult = 1.0
        body = raw
        pct = False
        if raw.endswith("%"):
            pct, body = True, raw[:-1].strip()
        elif re.search(r"\s?k$", raw) and re.search(r"\d\s?k$", raw):
            mult, body = 1e3, re.sub(r"\s?k$", "", raw)
        elif re.search(r"\d\s?M$", raw):
            mult, body = 1e6, re.sub(r"\s?M$", "", raw)
        elif re.search(r"\d\s?B$", raw):
            mult, body = 1e9, re.sub(r"\s?B$", "", raw)
        body = body.replace(",", "").replace("−", "-")
        digits = len(body.split(".")[1]) if "." in body else 0
        try:
            val = float(body.lstrip("+-")) * mult
        except ValueError:
            continue
        yield raw, val, digits, pct, mult


def close(c, v, d, mult=1.0):
    half = 0.5 * 10 ** (-d) * mult
    return abs(c - v) <= half + 1e-9 * max(1.0, abs(v))


def match(val, d, pct, mult):
    """returns list of (priority, source) matches."""
    out = []
    for i, v in NUM:
        if pct:  # a printed percentage can only be a '%' row or a fraction row (x100)
            cands = (abs(v),) if UNIT[i] == "%" else (abs(v) * 100,) if UNIT[i] == "fraction" else ()
        else:
            cands = (abs(v),)
        if any(close(c, val, d, mult) for c in cands):
            out.append(("numbers.csv", i))
    for lab, v in HEAD:
        if close(abs(v), val, d, mult):
            out.append(("head_cost", lab))
    for n, v in DATA_REPORT:
        if close(v, val, d, mult):
            out.append(("data_report", n))
    for lab, v in ABL:
        if not pct and close(abs(v), val, d, mult):
            out.append(("e1d_ablation", lab))
    for lab, form, v, tol, kind in DERIVED:
        if kind == "rel" and abs(val - v) <= tol * v and val >= 100:
            out.append(("derived", f"{lab}: {form} = {v:.1f}"))
        elif kind == "rel2" and abs(val - v) <= tol * v and val == 2:
            out.append(("derived", f"{lab}: {form} = {v:.2f}"))
        elif kind == "rel10" and abs(val - v) <= tol * v and val == 10:
            out.append(("derived", f"{lab}: {form} = {v:.2f}"))
        elif kind == "abs" and pct and close(v, val, d):
            out.append(("derived", f"{lab}: {form} = {v:.2f}"))
        elif kind == "neg" and pct and close(abs(v), val, d):
            out.append(("derived", f"{lab}: {form} = {v:.2f}%"))
        elif kind == "lt1" and pct and val == 1 and v < 1:
            out.append(("derived", f"{lab}: {form} = {v:.3f}"))
    for c, lab in CONSTANTS.items():
        if close(c, val, d, mult) and (d == 0 or c != int(c) or val == c):
            out.append(("constant", lab))
    return out


YEAR = re.compile(r"^(199\d|20[0-2]\d|2030)$")


def table_provenance():
    """Regenerate the tables with experiments/paper_tables.py into a temp dir; return {table file: True/False (byte-identical)}; None if not importable."""
    try:
        sys.path.insert(0, ROOT)
        import experiments.paper_tables as pt  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        return None, f"cannot import experiments.paper_tables ({type(e).__name__}: {e})"
    res = {}
    old = pt.TABLES
    with tempfile.TemporaryDirectory() as tmp:
        pt.TABLES = tmp
        try:
            pt.main()
        except Exception as e:  # noqa: BLE001
            pt.TABLES = old
            return None, f"regeneration failed ({type(e).__name__}: {e})"
        pt.TABLES = old
        for f in os.listdir(tmp):
            a = open(os.path.join(tmp, f), "rb").read()
            p = os.path.join(HERE, "tables", f)
            res[f"tables/{f}"] = os.path.exists(p) and open(p, "rb").read() == a
    return res, ""


def main():
    prov, prov_msg = table_provenance()
    rows, unmatched = [], []
    n_year = 0
    for origin, ln, text in source_lines():
        if SKIP_LINE.match(text):
            continue
        plain = clean(text)
        for raw, val, d, pct, mult in tokens(plain):
            if YEAR.match(raw.strip("+-−")) and not pct and mult == 1.0:
                n_year += 1
                rows.append((origin, ln, raw, "excluded", "year", ""))
                continue
            ms = match(val, d, pct, mult)
            status, src = "UNMATCHED", ""
            if ms:
                pri = {"derived": -1, "numbers.csv": 0, "head_cost": 1, "data_report": 2, "e1d_ablation": 2, "constant": 4}  # an explicit derived claim is the stated basis, not a coincidental numbers.csv hit
                ms.sort(key=lambda x: pri[x[0]])
                status, src = ms[0][0], "; ".join(f"{s}:{x}" if s != ms[0][0] else x for s, x in ms[:3]) + (f" (+{len(ms) - 3} more)" if len(ms) > 3 else "")
                only_num = all(s in ("numbers.csv", "head_cost") for s, _ in ms)
                if only_num and d == 0 and val < 100 and mult == 1.0:
                    status = "weak:" + status
            elif origin.startswith("tables/") and prov and prov.get(origin):
                status, src = "table-prov", f"{origin} is byte-identical to a regeneration by experiments/paper_tables.py"
            if status == "UNMATCHED":
                unmatched.append((origin, ln, raw, text.strip()))
            rows.append((origin, ln, raw, status, src, text.strip()[:100]))
    with open(os.path.join(HERE, "text_numbers_audit.tsv"), "w", encoding="utf8") as f:
        f.write("origin\tline\ttoken\tstatus\tsource\tcontext\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    cnt = {}
    for r in rows:
        k = r[3].split(":")[0] if r[3].startswith("weak") else r[3]
        cnt[k] = cnt.get(k, 0) + 1
    print(f"numeric tokens audited: {len(rows)}   (full list: paper/text_numbers_audit.tsv)")
    for k, v in sorted(cnt.items()):
        print(f"  {k:12s} {v}")
    print(f"table provenance: {prov_msg or {k: ('identical' if v else 'DIFFERENT') for k, v in prov.items()}}")
    print("derived checks (values used):")
    for lab, form, v, tol, kind in DERIVED:
        print(f"  {lab}: {form} = {v:.4g}")
    est = e1c_est_m0_qbar100_q1000()
    print(f"  'FSB loss above 10 pp at q=1000 with qbar=100' (est, M0, e1c_e2.csv fsb_base param=100 q=1000): loss = {est:.3f} pp -> {'holds' if est > 10 else 'DOES NOT HOLD'}")
    if unmatched:
        print(f"\nUNMATCHED tokens ({len(unmatched)}):")
        for o, ln, raw, text in unmatched:
            print(f"  {o}:{ln}: {raw!r}   | {text[:140]}")
        sys.exit(1)
    print("\nOK: every numeric token is explained")


if __name__ == "__main__":
    main()
