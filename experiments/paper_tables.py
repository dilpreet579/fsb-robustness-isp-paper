"""Paper tables T1-T7 -> paper/tables/T*.tex (LaTeX tabular, booktabs, no vertical rules), generated from results/*.csv and paper/head_cost.csv only.
Frozen framing: est = attacker weights p^ with the 2M list; emp = weights from leak counts with ALL of S~; t = 1M unless stated; loss = bucket success - baseline success
of the same attacker, percentage points (pp); +- = sd over the 5 repeats (T7: over the 5 noise draws)."""
import os

import numpy as np
import pandas as pd

from experiments.paper_common import PAPER, TABLES, load, one, sel
from experiments.paper_numlib import SIGMAS, crossing5_per_draw, interp_log

QBARS = (10, 100, 1000)
PM = r"\pm"


def pm(v, sd, d=2):
    return "--" if pd.isna(v) else (f"${v:.{d}f}$" if pd.isna(sd) else f"${v:.{d}f} {PM} {sd:.{d}f}$")


def write(name, colspec, header, body):
    """header: list of header lines (already LaTeX, end with \\\\); body: list of rows (str) or None for a \\midrule."""
    out = [r"\begin{tabular}{" + colspec + "}", r"\toprule", *header, r"\midrule"]
    for r in body:
        out.append(r"\midrule" if r is None else r)
    out += [r"\bottomrule", r"\end{tabular}", ""]
    open(os.path.join(TABLES, name), "w").write("\n".join(out))


# ----------------------------------------------------------------------------------------------------------------- T1 headline
def t1():
    est, emp, ratio, abl = load("e1c_e2"), load("e1e_headline"), load("e1e_ratio"), load("e1d_ablation")
    body = []
    for ci, c in enumerate(("M0", "M1b", "M2x", "M2L")):
        if ci:
            body.append(None)
        for qb in QBARS:
            f = one(sel(emp, condition=c, scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=qb)
            h = one(sel(emp, condition=c, scheme="hpb", variant=f"match_qbar{qb}", attacker="emp"), q=qb)
            if c == "M2L":  # Phase 1c has no est row for M2L; the ablation run (est, 2M list) has the same seeds and targets
                e = one(sel(abl, condition="M2L", scheme="fsb", variant="fsb_base", attacker="est"), param=qb, q=qb)
            else:
                e = one(sel(est, condition=c, scheme="fsb", variant="fsb_base", attacker="est"), param=qb, q=qb)
            rf = one(sel(ratio, condition=c, scheme="fsb", attacker="emp"), qbar=qb, q=1)
            rh = one(sel(ratio, condition=c, scheme="hpb", attacker="emp"), qbar=qb, q=1)
            removed = 100 * (1 - f.loss / h.loss)
            body.append(" & ".join([c if qb == 10 else "", str(qb), f"{f.avg_bucket:,.0f}", pm(e.loss, e.std_over_repeats), pm(f.loss, f.std_over_repeats), pm(h.loss, h.std_over_repeats),
                                    f"${removed:.0f}$", pm(rf.ratio, rf.ratio_sd, 1), pm(rh.ratio, rh.ratio_sd, 1)]) + r" \\")
    hdr = [r"Cond. & $\bar q$ & Avg.\ bucket & \multicolumn{3}{c}{Loss at $q=\bar q$ (pp)} & Removed & \multicolumn{2}{c}{Success ratio at $q=1$} \\",
           r"\cmidrule(lr){4-6}\cmidrule(lr){8-9}",
           r" & & (entries) & FSB est & FSB emp & HPB emp & (\%) & FSB emp & HPB emp \\"]
    write("T1_headline.tex", "llrrrrrrr", hdr, body)


# ----------------------------------------------------------------------------------------------------------------- T2 M2 ablation
def t2():
    abl, hd = load("e1d_ablation"), load("e1e_headline")
    body = []
    for pi, (c, lab) in enumerate((("M2L", r"length $\geq 8$ only"), ("M2B", "blocklist only"), ("M2x", "both"))):
        if pi:
            body.append(None)
        for qb in QBARS:
            e = one(sel(abl, condition=c, scheme="fsb", variant="fsb_base", attacker="est"), param=qb, q=qb)
            if c == "M2B":  # no emp run with all of S~ exists for the blocklist-only policy: the 2M-list value is a lower bound
                m = one(sel(abl, condition=c, scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=qb)
                emp = pm(m.loss, m.std_over_repeats) + r"$^{\dagger}$"
            else:
                m = one(sel(hd, condition=c, scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=qb)
                emp = pm(m.loss, m.std_over_repeats)
            body.append(" & ".join([lab if qb == 10 else "", str(qb), pm(e.loss, e.std_over_repeats), emp]) + r" \\")
    hdr = [r"Policy & $\bar q$ & \multicolumn{2}{c}{Loss at $q=\bar q$ (pp)} \\", r"\cmidrule(lr){3-4}", r" & & est & emp \\"]
    write("T2_m2_ablation.tex", "llrr", hdr, body)
    open(os.path.join(TABLES, "T2_m2_ablation_note.tex"), "w").write(
        r"$^{\dagger}$ emp with the 2M candidate list (lower bound); no all-of-$\tilde S$ run exists for the blocklist-only policy." + "\n")


# ----------------------------------------------------------------------------------------------------------------- T3 t sweep + head storage
def t3():
    ts = pd.concat([load("e1e_tsweep"), load("e1e_tsweep_10M")], ignore_index=True)
    hc = pd.read_csv(os.path.join(PAPER, "head_cost.csv")).set_index("t")
    body = []
    for t in (100_000, 300_000, 1_000_000, 3_000_000, 10_000_000):
        r = [f"{t:,}".replace(",", r"\,"), f"{hc.loc[t].plain_MB:.1f}", f"{hc.loc[t].gzip9_MB:.1f}", f"{hc.loc[t].prob_float32_MB:.1f}",
             f"{one(sel(ts, condition='M0', t=t), q=100).avg_bucket:,.0f}"]
        for c in ("M0", "M2x"):
            for q in (1, 10, 100):
                x = one(sel(ts, condition=c, t=t, attacker="emp"), q=q)
                r.append(pm(x.loss, x.std_over_repeats, 1))
        body.append(" & ".join(r) + r" \\")
    hdr = [r"$t$ & \multicolumn{3}{c}{Head storage (MB)} & Avg.\ bucket & \multicolumn{3}{c}{emp loss, M0 (pp)} & \multicolumn{3}{c}{emp loss, M2x (pp)} \\",
           r"\cmidrule(lr){2-4}\cmidrule(lr){6-8}\cmidrule(lr){9-11}",
           r" & text & gzip & +probs & (entries) & $q{=}1$ & $q{=}10$ & $q{=}100$ & $q{=}1$ & $q{=}10$ & $q{=}100$ \\"]
    write("T3_tsweep_head_storage.tex", "rrrrrrrrrrr", hdr, body)
    open(os.path.join(TABLES, "T3_note.tex"), "w").write(
        "Storage is an estimate of data size, not an implementation: newline-delimited head strings (text), the same text under gzip -9, and 4 bytes per entry for a float32 "
        "probability (+probs); 1 MB = $10^6$ bytes. The 3-gram table adds " + f"{hc.iloc[0].trigram_float32_MB:.1f} MB (float32) or {hc.iloc[0].trigram_float64_MB:.1f} MB (float64). "
        "FSB with $\\bar q=100$, emp attacker holding all of $\\tilde S$.\n")


# ----------------------------------------------------------------------------------------------------------------- T4 fixes
def t4():
    fx = load("e1e_fix")
    body = []
    for ci, c in enumerate(("M0", "M2x")):
        if ci:
            body.append(None)
        for v, lab in (("fsb_base", "base (add-$\\delta$)"), ("smoothed", "Kneser--Ney"), ("cal_iso_w0.5", "calibrated$^{\\ast}$")):
            d = sel(fx, condition=c, variant=v, attacker="emp")
            vals = [interp_log(d, q, b) for q in (100, 1000) for b in (2000, 6500, 20000)]
            body.append(" & ".join([c if v == "fsb_base" else "", lab] + [("--" if np.isnan(x) else f"{x:.1f}") for x in vals]) + r" \\")
    hdr = [r"Cond. & Variant & \multicolumn{3}{c}{Loss at $q=100$ (pp)} & \multicolumn{3}{c}{Loss at $q=1000$ (pp)} \\", r"\cmidrule(lr){3-5}\cmidrule(lr){6-8}",
           r" & & 2k & 6.5k & 20k & 2k & 6.5k & 20k \\"]
    write("T4_fixes.tex", "llrrrrrr", hdr, body)
    open(os.path.join(TABLES, "T4_note.tex"), "w").write(
        "Loss of the emp attacker (all of $\\tilde S$) at equal average bucket size (2,000 / 6,500 / 20,000 entries; log-linear interpolation along a $\\bar q=1..3000$ sweep). "
        "$^{\\ast}$ exploratory: cross-fitted calibration of the 3-gram tail, isotonic, 0.5-decade bins.\n")


# ----------------------------------------------------------------------------------------------------------------- T5 cost
def t5():
    c = load("e1e_cost")
    body = []
    for att, lab in (("emp", "emp (leak counts)"), ("est", r"est ($\hat p$)")):
        for cand in ("2M", "all"):
            r = one(c, attacker=att, candidates=cand)
            body.append(" & ".join([lab if cand == "2M" else "", r"$2\,000\,000$" if cand == "2M" else r"all of $\tilde S$ ($13\,125\,513$)", f"{r.attacker_build_s:.1f}", f"{r.index_build_s:.1f}",
                                    f"{r.games_5x5000_s:.1f}", f"{r.total_s:.1f}", f"{r.peak_rss_gb:.1f}"]) + r" \\")
    hdr = [r"Attacker & Candidates & Build (s) & Index (s) & 25k queries (s) & Total (s) & Peak mem. (GB) \\"]
    write("T5_cost.tex", "llrrrrr", hdr, body)
    open(os.path.join(TABLES, "T5_note.tex"), "w").write(
        "One cold run (M0, FSB $\\bar q=100$, $t=1$M; $5\\times5{,}000$ targets) in a fresh process on a 10-core laptop; total adds the world build "
        f"({c.world_build_s.min():.1f}--{c.world_build_s.max():.1f} s, same for all rows) to the columns shown. Build = candidate list; Index = $\\gamma$ for every candidate and the lookup structure.\n")


# ----------------------------------------------------------------------------------------------------------------- T6 estimator error
def t6():
    es = load("e1d_esterror_summary")
    es = es[es.t == 1_000_000]
    body = []
    for gi, g in enumerate(("head", "tail")):
        if gi:
            body.append(None)
        for m, lab in (("B", "per-password dispersion (stored passwords)"), ("A", "binned masses (all strings)")):
            r = es[(es.group == g) & es.method.str.startswith(m)].iloc[0]
            se = "--" if pd.isna(r.se_over_folds) else f"{r.se_over_folds:.3f}"
            body.append(" & ".join([g if m == "B" else "", lab, f"{r.sigma_hat:.3f}", se, f"{r.sigma_hat_alt:.3f}", f"{r.bias_mu:+.2f}", f"{int(r.bins_used)}"]) + r" \\")
    hdr = [r"Group & Method & $\hat\sigma$ & s.e.\ & alt.\ & bias $\mu$ & Bins \\"]
    write("T6_estimator_error.tex", "llrrrrr", hdr, body)
    open(os.path.join(TABLES, "T6_note.tex"), "w").write(
        "$\\hat\\sigma$: sd of $\\log(\\hat p/p)$ on held-out A\\_dev at $t=1$M, Poisson noise subtracted. Method B: per-password dispersion within bins of $\\hat p$ over the passwords stored in the "
        "leak (alt. = account-weighted); s.e.\\ over 5 folds. Method A: held-out vs model mass per bin over all strings (alt. = raw RMS, not Poisson-corrected); a lower bound on B. "
        "Bias $\\mu=\\log(\\text{true}/\\hat p)$, mass-weighted (B) or mean log-ratio (A); positive: $\\hat p$ too small.\n")


# ----------------------------------------------------------------------------------------------------------------- T7 crossings
def t7():
    emp = load("e1e_headline")
    body = []
    for qb in QBARS:
        v = crossing5_per_draw(qb, "est")
        body.append(" & ".join([str(qb), f"${np.mean(v):.3f} {PM} {np.std(v, ddof=1):.3f}$", ", ".join(f"{x:.3f}" for x in v)]) + r" \\")
    z = [float(one(sel(emp, condition="M0", scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=qb).loss) for qb in QBARS]
    assert min(z) > 5, z  # the statement below is only true if emp is already above 5 points at sigma = 0
    body.append(None)
    body.append(r"\multicolumn{3}{p{0.92\linewidth}}{\footnotesize emp (all of $\tilde S$): crossing not defined, the loss at $\sigma=0$ already exceeds 5 points (" +
                " / ".join(f"{x:.1f}" for x in z) + r" pp for $\bar q=10/100/1000$).} \\")
    hdr = [r"$\bar q$ & $\sigma$ at 5 points (mean $\pm$ sd, 5 draws) & Per-draw values \\"]
    write("T7_m3_crossings.tex", "lrl", hdr, body)
    open(os.path.join(TABLES, "T7_note.tex"), "w").write(
        "est, M0, FSB, loss at $q=\\bar q$; noise multiplies $\\hat p$ on every string by $\\exp(\\sigma z_w)$; $\\sigma=0$ is the noise-free run; linear interpolation along "
        "$\\sigma\\in\\{0,0.5,0.75,1.0,1.5\\}$; draws use salts d1--d5.\n")


# ----------------------------------------------------------------------------------------------------------------- T8 gamma floor (Phase 1g)
def _worst(cond, scheme, variant, qb, q, param=None):
    """Largest loss over the emp (e1g_floor_fresh) and gt, est (e1g_robust_fresh) attackers on the fresh pool; also returns the average bucket size."""
    vals = []
    for src, atts in (("e1g_floor_fresh", ("emp",)), ("e1g_robust_fresh", ("gt", "est"))):
        d = load(src)
        for a in atts:
            vals.append(float(one(sel(d, condition=cond, scheme=scheme, variant=variant, attacker=a), param=qb if param is None else param, q=q).loss))
    return max(vals)


def t8():
    d = load("e1g_floor_fresh")
    body = []
    for qi, qb in enumerate(QBARS):
        if qi:
            body.append(None)
        base = float(one(sel(d, condition="M0", scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=1).avg_bucket)
        rows = [("plain FSB", "fsb", "fsb_base", qb)] + [(f"floor {g:,}", "fsb", f"floor{g}", qb) for g in (256, 1024, 2048, 4096)]
        l = int(one(sel(d, condition="M0", scheme="hpb", variant=f"match_qbar{qb}", attacker="emp"), q=1).param)
        rows.append((f"matched HPB ($l={l}$)", "hpb", f"match_qbar{qb}", l))
        for ri, (name, sch, v, par) in enumerate(rows):
            avg = float(one(sel(d, condition="M0", scheme=sch, variant=v, attacker="emp"), param=par, q=1).avg_bucket)
            ab = f"{avg:,.0f}" if v in ("fsb_base",) or sch == "hpb" else f"{avg:,.0f} (${avg / base:.2f}\\times$)"
            cells = [f"${_worst(c, sch, v, qb, q, par):.2f}$" for c in ("M0", "M2x") for q in (qb, 1000)]
            body.append(" & ".join([str(qb) if ri == 0 else "", name, ab, *cells]) + r" \\")
    hdr = [r"$\bar q$ & Scheme & Avg.\ bucket & \multicolumn{2}{c}{M0 (pp)} & \multicolumn{2}{c}{M2x (pp)} \\",
           r"\cmidrule(lr){4-5}\cmidrule(lr){6-7}",
           r" & & (entries) & $q=\bar q$ & $q=1000$ & $q=\bar q$ & $q=1000$ \\"]
    write("T8_floor.tex", "llrrrrr", hdr, body)
    open(os.path.join(TABLES, "T8_note.tex"), "w").write(
        "Fresh target pool (A\\_fresh), 5 repeats of 5,000 targets, FSB with $t=1$M; floor $g$: every string is stored in at least $g$ buckets. Each cell is the largest loss over three attackers "
        "that hold all of $\\tilde S$: emp (raw counts), gt (Good--Turing adjusted counts) and est (the server's estimate $\\hat p$); sizes in parentheses are relative to plain FSB with the same "
        "$\\bar q$. Plain FSB on this pool loses slightly less than on A\\_test (Table~\\ref{tab:headline}). The guarantee covers $q\\le\\bar q$; the $q=1000$ columns are outside it for $\\bar q<1000$.\n")


# ----------------------------------------------------------------------------------------------------------------- T10 stability across splits (Phase 1h)
def t10():
    d = load("e1h_splits")
    body = []
    for name, sch, v in (("plain FSB", "fsb", "fsb_base"), ("FSB, floor 2,048", "fsb", "floor2048"), (r"matched HPB ($l=12$)", "hpb", "match_qbar100")):
        cells = []
        for c in ("M0", "M2x"):
            for q in (1, 100):
                w = sel(d, condition=c, scheme=sch, variant=v, q=q).groupby("split").loss.max().to_numpy(dtype=float)  # per split: largest loss over emp, gt, est
                cells.append(f"${w.mean():.2f} {PM} {w.std(ddof=1):.2f}$ ({w.min():.2f}--{w.max():.2f})")
        body.append(" & ".join([name, *cells]) + r" \\")
    hdr = [r"Scheme ($\bar q=100$) & \multicolumn{2}{c}{M0 (pp)} & \multicolumn{2}{c}{M2x (pp)} \\", r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}", r" & $q=1$ & $q=100$ & $q=1$ & $q=100$ \\"]
    write("T10_splits.tex", "lllll", hdr, body)
    open(os.path.join(TABLES, "T10_note.tex"), "w").write(
        "Four independent account splits of RockYou (seeds 101, 111, 121, 131), each with its own server estimate and attackers; targets are the held-out pool A\\_test of that split, "
        "5 repeats of 5,000 targets. Each cell is the mean $\\pm$ sd over the four splits of the largest loss over the emp, gt and est attackers (minimum--maximum in parentheses). "
        "The floor $g=2{,}048$ was chosen on the development pool of the first split, so the other three splits are out of sample for it.\n")


# ----------------------------------------------------------------------------------------------------------------- T9 implementation environment
def t9():
    """Pinned versions from requirements.txt (deterministic); Python and the machine are the authors' build environment, stated as fixed strings."""
    req = {}
    for ln in open(os.path.join(os.path.dirname(PAPER), "requirements.txt")):
        if "==" in ln:
            k, v = ln.strip().split("==", 1)
            req[k.lower()] = v
    rows = [("Python", "3.12"), ("NumPy", req["numpy"]), ("Numba", req["numba"]), ("pandas", req["pandas"]), ("SciPy", req["scipy"]), ("Matplotlib", req["matplotlib"]),
            ("PDF build", "Tectonic 0.17"), ("Machine", "laptop, Apple M5, 10 cores, 16 GB RAM")]
    write("T9_env.tex", "ll", [r"Component & Version \\"], [f"{a} & {b}" + r" \\" for a, b in rows])


# ----------------------------------------------------------------------------------------------------------------- T11-T13: compact tables for the 6-page conference version
def t11():
    """Headline (M0 and M2x only): loss at q = qbar, FSB est, FSB emp, matched HPB emp, share of HPB's loss removed (emp)."""
    est, emp = load("e1c_e2"), load("e1e_headline")
    body = []
    for ci, c in enumerate(("M0", "M2x")):
        if ci:
            body.append(None)
        for qb in QBARS:
            f = one(sel(emp, condition=c, scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=qb)
            h = one(sel(emp, condition=c, scheme="hpb", variant=f"match_qbar{qb}", attacker="emp"), q=qb)
            e = one(sel(est, condition=c, scheme="fsb", variant="fsb_base", attacker="est"), param=qb, q=qb)
            body.append(" & ".join([c if qb == 10 else "", str(qb), f"{f.avg_bucket:,.0f}", pm(e.loss, e.std_over_repeats), pm(f.loss, f.std_over_repeats), pm(h.loss, h.std_over_repeats),
                                    f"${100 * (1 - f.loss / h.loss):.0f}$"]) + r" \\")
    hdr = [r"Cond. & $\bar q$ & Avg.\ bucket & \multicolumn{3}{c}{Loss at $q=\bar q$ (pp)} & Removed \\", r"\cmidrule(lr){4-6}", r" & & (entries) & FSB est & FSB emp & HPB emp & (\%) \\"]
    write("T11_fist_headline.tex", "llrrrrr", hdr, body)


def t12():
    """Floor (fresh pool), worst case over emp, gt, est at q = qbar: selected floors for qbar = 10, 100, 1000."""
    d = load("e1g_floor_fresh")
    body = []
    for qi, (qb, floors) in enumerate(((10, (256, 1024)), (100, (256, 1024, 2048, 4096)), (1000, (2048, 4096)))):
        if qi:
            body.append(None)
        base = float(one(sel(d, condition="M0", scheme="fsb", variant="fsb_base", attacker="emp"), param=qb, q=1).avg_bucket)
        rows = [("plain FSB", "fsb_base")] + [(f"floor {g:,}", f"floor{g}") for g in floors]
        for ri, (name, v) in enumerate(rows):
            avg = float(one(sel(d, condition="M0", scheme="fsb", variant=v, attacker="emp"), param=qb, q=1).avg_bucket)
            ab = f"{avg:,.0f}" if v == "fsb_base" else f"{avg:,.0f} (${avg / base:.2f}\\times$)"
            cells = [f"${_worst(c, 'fsb', v, qb, qb):.2f}$" for c in ("M0", "M2x")]
            body.append(" & ".join([str(qb) if ri == 0 else "", name, ab, *cells]) + r" \\")
    hdr = [r"$\bar q$ & Scheme & Avg.\ bucket & M0 (pp) & M2x (pp) \\"]
    write("T12_fist_floor.tex", "llrrr", hdr, body)


def t13():
    """One line of text for the implementation paragraph (versions from requirements.txt; Python and the machine are fixed strings, as in T9)."""
    req = {}
    for ln in open(os.path.join(os.path.dirname(PAPER), "requirements.txt")):
        if "==" in ln:
            k, v = ln.strip().split("==", 1)
            req[k.lower()] = v
    open(os.path.join(TABLES, "T13_env.tex"), "w").write(
        f"Python 3.12, NumPy {req['numpy']}, Numba {req['numba']}, pandas {req['pandas']} and SciPy {req['scipy']}, on a laptop with an Apple M5 processor (10 cores, 16 GB RAM)")


def main():
    os.makedirs(TABLES, exist_ok=True)
    for f in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13):
        f()
    print("tables written to", TABLES, sorted(os.listdir(TABLES)))


if __name__ == "__main__":
    main()
