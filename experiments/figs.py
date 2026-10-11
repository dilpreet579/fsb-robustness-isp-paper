"""Figures from the CSVs only (no recomputation): fig1_pareto, fig2_mismatch, fig3_fix (pdf + png) in figs/.
Colour is never the only encoding: each series also has its own marker and line style, and is labelled in the legend.
Error bars are the standard deviation of the per-repeat loss (std_over_repeats)."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from experiments import common as C

R, F = C.RESULTS, os.path.join(os.path.dirname(C.RESULTS), "figs")
INK = "#1f2933"
PAL = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]  # Okabe-Ito, fixed order
MK = ["o", "s", "^", "D", "v", "P"]
TITLE = {"est": "attacker weights = public estimate p^ (paper-faithful)", "emp": "attacker weights = leak counts (plan-literal)"}
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.25, "grid.linewidth": 0.5, "legend.frameon": False})
YL = "Attacker success gain over baseline at q=1000 (percentage points)"


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(F, f"{name}.{ext}"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def line(ax, d, label, i, ls="-"):
    d = d.sort_values("avg_bucket")
    ax.errorbar(d.avg_bucket, d.loss, yerr=d.std_over_repeats, label=label, color=PAL[i], marker=MK[i], ms=4, lw=1.4, ls=ls, capsize=2)


def fig1():
    d = pd.read_csv(os.path.join(R, "e1.csv"))
    d = d[d.q == 1000]
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for ax, m in zip(axs, C.MODELS):
        x = d[d.attacker == m]
        line(ax, x[x.scheme == "hpb"], "HPB (hash prefix, l = 7..16)", 1, "--")
        line(ax, x[x.scheme == "fsb"], "FSB (qbar = 1..10000)", 0)
        ax.set_xscale("log")
        ax.set_xlabel("Average bucket size (entries, measured on S~)")
        ax.set_title(TITLE[m], fontsize=8)
    axs[0].set_ylabel(YL)
    axs[0].legend(loc="upper right")
    fig.suptitle("Fig. 1  Bucket size vs attacker gain, matched condition M0 (RockYou 90/10 split)", fontsize=9)
    save(fig, "fig1_pareto")


def fig2():
    d = pd.read_csv(os.path.join(R, "e2.csv"))
    d = d[d.q == 1000]
    order = [("M0", "fsb_base"), ("M1", "fsb_base"), ("M2", "fsb_base"), ("M3", "noise_s0.5"), ("M3", "noise_s1.0"), ("M3", "noise_s1.5")]
    labels = ["M0\nmatched", "M1\ncross-corpus", "M2\npolicy", "M3\nsigma=0.5", "M3\nsigma=1.0", "M3\nsigma=1.5"]
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8), sharey=True)
    for ax, m in zip(axs, C.MODELS):
        x = d[d.attacker == m]
        for i, qb in enumerate((10, 100, 1000)):
            ys, es = [], []
            for c, v in order:
                r = x[(x.condition == c) & (x.variant == v) & (x.param == qb) & (x.scheme == "fsb")].iloc[0]
                ys.append(r.loss)
                es.append(r.std_over_repeats)
            ax.errorbar(range(6), ys, yerr=es, label=f"FSB qbar={qb}", color=PAL[i], marker=MK[i], ms=4, lw=1.4, capsize=2)
        for j, qb in enumerate((10, 100, 1000)):  # HPB at matched bucket size, for M0..M2 only (no estimate => no M3 effect)
            h = x[(x.scheme == "hpb") & (x.variant == f"match_qbar{qb}")].set_index("condition")
            ax.errorbar(range(3), [h.loc[c].loss for c in ("M0", "M1", "M2")], yerr=[h.loc[c].std_over_repeats for c in ("M0", "M1", "M2")],
                        label=f"HPB, size-matched to qbar={qb}", color=PAL[3 + j], marker=MK[3 + j], ms=4, lw=1, ls="--", capsize=2)
        ax.set_xticks(range(6))
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_title(TITLE[m], fontsize=8)
    axs[0].set_ylabel(YL)
    axs[1].legend(fontsize=7, loc="lower right")
    fig.suptitle("Fig. 2  Loss at q=1000 under estimate mismatch (M1 at q=1000 is saturated, see QUESTIONS Q8)", fontsize=9)
    save(fig, "fig2_mismatch")


def fig3():
    d = pd.read_csv(os.path.join(R, "e3.csv"))
    d = d[d.q == 1000]
    best = json.load(open(os.path.join(R, "e3_best.json")))
    fig, axs = plt.subplots(2, 3, figsize=(11, 6.2), sharey="row")
    for r, m in enumerate(C.MODELS):
        for c, cond in enumerate(("M0", "M1", "M2")):
            ax = axs[r, c]
            for i, v in enumerate(("fsb_base", "ens_max", "smoothed")):
                x = d[(d.attacker == m) & (d.condition == cond) & (d.variant == v)]
                line(ax, x, v + (" (best on dev)" if best[m] == v else ""), i, "-" if v == "fsb_base" else "--")
            ax.set_xscale("log")
            ax.set_title(f"{cond}, attacker {m}", fontsize=8)
            if r == 1:
                ax.set_xlabel("Average bucket size (entries)")
            if c == 0:
                ax.set_ylabel("Gain at q=1000 (pp)")
    axs[0, 0].legend(fontsize=7)
    fig.suptitle("Fig. 3  Fresh target pool: FSB baseline vs conservative variants (each point is one qbar in 1..3000)", fontsize=9)
    save(fig, "fig3_fix")


if __name__ == "__main__":
    os.makedirs(F, exist_ok=True)
    fig1()
    fig2()
    if os.path.exists(os.path.join(R, "e3_best.json")):
        fig3()
