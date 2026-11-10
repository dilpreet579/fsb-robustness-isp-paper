"""Paper figures 1-5 -> paper/figs/figN.{pdf,png} (3.3 in column width) and figN_wide.{pdf,png} (7 in), PNG at 300 dpi.
Computed from results/*.csv only. Colour-blind-safe palette (Okabe-Ito) AND distinguishable in grey scale (every series has its own line style and marker).
No titles inside the figures; axis labels carry units; error bars = sd over the 5 repeats (Fig. 2: sd over the 5 noise draws). Font >= 8 pt at the printed width.
Frozen labels: est = weights p^, 2M list; emp = weights from leak counts, all of S~; t = 1M unless stated."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from experiments.paper_common import FIGS, load, one, sel

BLUE, VERM, GREEN, ORANGE, SKY, PURPLE, BLACK, GREY = "#0072B2", "#D55E00", "#009E73", "#E69F00", "#56B4E9", "#CC79A7", "#000000", "#7a7a7a"
COND = {"M0": "M0", "M2x": r"M2x (len$\geq$8 + Xato)"}
STILDE = r"$\tilde{S}$"
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8, "axes.titlesize": 8,
                     "lines.linewidth": 1.2, "lines.markersize": 4.2, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.25, "grid.linewidth": 0.5, "pdf.fonttype": 42, "ps.fonttype": 42, "mathtext.default": "regular",
                     "figure.constrained_layout.use": True})
NARROW, WIDE = 3.3, 7.0


def save(fig, name, wide):
    stem = os.path.join(FIGS, f"{name}{'_wide' if wide else ''}")
    fig.savefig(stem + ".pdf")
    fig.savefig(stem + ".png", dpi=300)
    plt.close(fig)


def legend_below(fig, handles=None, labels=None, ncol=2):
    fig.legend(handles=handles, labels=labels, loc="outside lower center", ncol=ncol, frameon=False, handlelength=2.6, columnspacing=1.2)


def style(color, ls, marker, filled, ms=None):
    s = dict(color=color, ls=ls, marker=marker, markerfacecolor=color if filled else "white", markeredgecolor=color, markeredgewidth=1.0)
    if ms:
        s["markersize"] = ms
    return s


# ------------------------------------------------------------------------------------------------------------------ Fig 1
def fig1(wide):
    est, emp = load("e1c_e2"), load("e1e_headline")
    qs = [1, 10, 100, 1000]
    spec = [("fsb", "est", "FSB, est", style(BLUE, "-", "o", True)), ("fsb", "emp", f"FSB, emp (all of {STILDE})", style(VERM, "-", "^", True)),
            ("hpb", "est", "HPB l=12, est", style(BLUE, "--", "s", False)), ("hpb", "emp", f"HPB l=12, emp (all of {STILDE})", style(VERM, "--", "D", False))]
    fig, axs = plt.subplots(1, 2, figsize=(WIDE, 2.9)) if wide else plt.subplots(2, 1, figsize=(NARROW, 4.9), sharex=True)
    for ax, cond in zip(axs, ("M0", "M2x")):
        for sch, att, lab, st in spec:
            d = sel(est if att == "est" else emp, condition=cond, scheme=sch, attacker=att)
            d = d[d.param == 100] if sch == "fsb" else d[d.variant == "match_qbar100"]
            if sch == "fsb":
                d = d[d.variant == "fsb_base"]
            d = d.sort_values("q")
            assert list(d.q) == qs and (sch == "fsb" or (d.param == 12).all())
            ax.errorbar(d.q, d.loss, yerr=d.std_over_repeats, capsize=2, label=lab, **st)
        ax.axvline(100, color=GREY, lw=0.8, ls=(0, (1, 2)), zorder=0)
        ax.axhline(5, color=BLACK, lw=0.8, ls=":", zorder=0)
        ax.set_xscale("log")
        ax.set_xticks(qs)
        ax.set_xticklabels([str(q) for q in qs])
        ax.set_ylim(-1.5, 56)
        ax.text(0.03, 0.96, COND[cond], transform=ax.transAxes, va="top", ha="left", fontsize=8)
        ax.text(100, 53, r"$q=\bar{q}$", ha="center", va="top", fontsize=8, color=GREY, bbox=dict(fc="white", ec="none", pad=0.6))
        ax.set_ylabel("Loss (percentage points)")
    axs[-1].set_xlabel("Guess budget $q$ (guesses)")
    if wide:
        axs[0].set_xlabel("Guess budget $q$ (guesses)")
    h, l = axs[0].get_legend_handles_labels()
    from matplotlib.lines import Line2D
    h.append(Line2D([0], [0], color=BLACK, ls=":", lw=0.8))
    l.append("5-point reference")
    legend_below(fig, h, l, ncol=3 if wide else 2)
    save(fig, "fig1", wide)


# ------------------------------------------------------------------------------------------------------------------ Fig 2
def fig2(wide):
    sig = [0.5, 1.0, 1.6]
    est, emp = load("e1f_tailnoise"), load("e1f_tailnoise_emp")
    clean = {"est": float(one(sel(load("e1c_e2"), condition="M0", scheme="fsb", variant="fsb_base", attacker="est"), param=100, q=100).loss),
             "emp": float(one(sel(load("e1e_headline"), condition="M0", scheme="fsb", variant="fsb_base", attacker="emp"), param=100, q=100).loss)}
    es = load("e1d_esterror_summary")
    head = float(es[(es.t == 1_000_000) & (es.group == "head") & es.method.str.startswith("B")].sigma_hat.iloc[0])
    tail = float(es[(es.t == 1_000_000) & (es.group == "tail") & es.method.str.startswith("B")].sigma_hat.iloc[0])
    spec = [("est", "full", "est, noise on all strings", style(BLUE, "-", "o", True)), ("est", "tail", "est, noise on tail only", style(BLUE, "--", "s", False)),
            ("emp", "full", f"emp, noise on all strings", style(VERM, "-", "^", True)), ("emp", "tail", "emp, noise on tail only", style(VERM, "--", "D", False))]
    fig, ax = plt.subplots(figsize=(WIDE, 3.0) if wide else (NARROW, 3.5))
    for att, kind, lab, st in spec:
        df = est if att == "est" else emp
        ys, ss = [clean[att]], [np.nan]
        for s in sig:
            v = df[(df.q == 100) & (df.variant.str.startswith(f"{kind}noise_s{s}_d"))].loss.to_numpy()
            assert len(v) == 5
            ys.append(v.mean())
            ss.append(v.std(ddof=1))
        ax.errorbar([0.0] + sig, ys, yerr=ss, capsize=2, label=lab, **st)
    for x in (head, tail):
        ax.axvline(x, color=GREY, lw=0.9, ls=(0, (1, 2)), zorder=0)
    top = ax.secondary_xaxis("top")  # measured sigma_hat (method B, t = 1M) labelled along the top edge so the labels cannot hit data
    top.set_xticks([head, tail])
    top.set_xticklabels([f"head\n$\\hat\\sigma$={head:.2f}", f"tail\n$\\hat\\sigma$={tail:.2f}"], fontsize=8, color=GREY)
    top.tick_params(colors=GREY, length=3)
    ax.axhline(5, color=BLACK, lw=0.8, ls=":", zorder=0)
    ax.set_xticks([0.0] + sig)
    ax.set_xlim(-0.05, 1.75)
    ax.set_xlabel(r"Noise $\sigma$ (s.d. of the log multiplier)")
    ax.set_ylabel(r"Loss at $q=\bar{q}=100$ (percentage points)")
    h, l = ax.get_legend_handles_labels()
    from matplotlib.lines import Line2D
    h.append(Line2D([0], [0], color=BLACK, ls=":", lw=0.8))
    l.append("5-point reference")
    legend_below(fig, h, l, ncol=3 if wide else 1)
    save(fig, "fig2", wide)


# ------------------------------------------------------------------------------------------------------------------ Fig 3
def fig3(wide):
    g = load("e1f_mech_groups")
    layers = [("head", BLUE, ""), ("tail", ORANGE, "//"), ("none", "#bdbdbd", "..")]
    fig, axs = plt.subplots(1, 2, figsize=(WIDE, 3.0), sharey=True) if wide else plt.subplots(2, 1, figsize=(NARROW, 5.2), sharey=True)
    for ax, cond in zip(axs, ("M0", "M2x")):
        xs, ticks = [], []
        pos = 0.0
        for q in (1, 100):
            for sch in ("fsb", "hpb"):
                up = dn = 0.0
                for grp, col, hat in layers:
                    v = float(one(g, condition=cond, scheme=sch, q=q, group=grp).contrib)
                    if v >= 0:
                        ax.bar(pos, v, 0.72, bottom=up, color=col, hatch=hat, edgecolor="black", lw=0.5)
                        up += v
                    else:
                        ax.bar(pos, v, 0.72, bottom=dn, color=col, hatch=hat, edgecolor="black", lw=0.5)
                        dn += v
                tot = one(g, condition=cond, scheme=sch, q=q, group="total")
                ax.errorbar(pos, tot.contrib, yerr=tot.contrib_sd, fmt="D", color="black", ms=3.6, capsize=2, lw=0.9, zorder=5)
                ax.text(pos, max(up, tot.contrib) + 1.6, f"{tot.contrib:+.1f}", ha="center", va="bottom", fontsize=8)
                xs.append(pos)
                ticks.append(sch.upper())
                pos += 1.0
            pos += 0.7
        ax.set_xticks(xs)
        ax.set_xticklabels(ticks)
        for q, x0 in ((1, (xs[0] + xs[1]) / 2), (100, (xs[2] + xs[3]) / 2)):
            ax.text(x0, -0.12, f"$q={q}$", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=8)
        ax.text(0.02, 0.97, COND[cond], transform=ax.transAxes, va="top", ha="left", fontsize=8)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_ylabel("Loss contribution (pp)")  # pp = percentage points of all targets (stated in the caption)
        ax.set_ylim(-4, 52)
        ax.grid(axis="x", visible=False)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    h = [Patch(facecolor=c, hatch=hh, edgecolor="black", lw=0.5, label=n) for n, c, hh in layers] + [Line2D([0], [0], marker="D", color="black", ls="", ms=3.6, label="total (± sd)")]
    h[0].set_label("head targets")
    h[1].set_label("stored, not in head")
    h[2].set_label(f"not in {STILDE}")
    legend_below(fig, h, [x.get_label() for x in h], ncol=4 if wide else 2)
    save(fig, "fig3", wide)


# ------------------------------------------------------------------------------------------------------------------ Fig 4
def fig4(wide):
    ts = __import__("pandas").concat([load("e1e_tsweep"), load("e1e_tsweep_10M")], ignore_index=True)
    ts = ts[(ts.q == 100) & (ts.attacker == "emp")]
    est_t = load("e1c_tsweep")
    est_t = est_t[(est_t.attacker == "est") & (est_t.q == 100) & (est_t.condition == "M0")].sort_values("t")
    m2x_est = one(sel(load("e1c_e2"), condition="M2x", scheme="fsb", variant="fsb_base", attacker="est"), param=100, q=100)
    fig, ax = plt.subplots(figsize=(WIDE, 3.0) if wide else (NARROW, 3.4))
    for cond, st, lab in (("M0", style(VERM, "-", "^", True), "emp, M0"), ("M2x", style(VERM, "--", "D", False), "emp, M2x")):
        d = sel(ts, condition=cond).sort_values("t")
        ax.errorbar(d.t, d.loss, yerr=d.std_over_repeats, capsize=2, label=lab, **st)
    ax.plot(est_t.t, est_t.loss, **style(BLUE, "-.", "o", True), label="est, M0")
    ax.plot([1_000_000], [m2x_est.loss], ls="", marker="s", color=BLUE, markerfacecolor="white", markeredgewidth=1.0, label="est, M2x (t = 1M only)")
    ax.set_xscale("log")
    ax.set_xlabel("Histogram head size $t$ (passwords)")
    ax.set_ylabel(r"Loss at $q=\bar{q}=100$ (percentage points)")
    ax.set_xlim(8e4, 1.3e7)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.grid(False)
    d = sel(ts, condition="M0").sort_values("t")
    ax2.plot(d.t, d.avg_bucket, color=GREY, ls=":", marker="x", ms=4, lw=1.0, label="average bucket size")
    ax2.set_ylabel("Average bucket size (entries)")
    ax2.set_ylim(0, 6500)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    legend_below(fig, h1 + h2, l1 + l2, ncol=3 if wide else 2)
    save(fig, "fig4", wide)


# ------------------------------------------------------------------------------------------------------------------ Fig 5
def fig5(wide):
    fx = load("e1e_fix")
    # base is drawn large and first; smoothed (which coincides with it) is drawn smaller on top so both stay visible
    spec = [("fsb_base", "fsb_base (3-gram, add-delta)", style(BLUE, "-", "o", True, ms=7)), ("smoothed", "smoothed (Kneser-Ney)", style(GREEN, "--", "s", False, ms=4)),
            ("cal_iso_w0.5", "cal_iso_w0.5 (calibrated, exploratory)", style(VERM, ":", "^", True, ms=4.5))]
    fig, axs = plt.subplots(1, 2, figsize=(WIDE, 2.9), sharey=True) if wide else plt.subplots(2, 1, figsize=(NARROW, 5.0), sharey=True, sharex=True)
    for ax, cond in zip(axs, ("M0", "M2x")):
        for v, lab, st in spec:
            d = sel(fx, condition=cond, variant=v, q=100, attacker="emp").sort_values("avg_bucket")
            ax.errorbar(d.avg_bucket, d.loss, yerr=d.std_over_repeats, capsize=1.5, label=lab, **st)
        ax.set_xscale("log")
        ax.text(0.97, 0.97, COND[cond], transform=ax.transAxes, va="top", ha="right", fontsize=8)
        ax.set_ylabel(r"emp loss, $q=100$ (pp)")  # pp = percentage points (stated in the caption)
    for ax in (axs if wide else axs[-1:]):
        ax.set_xlabel("Average bucket size (entries)")
    h, l = axs[0].get_legend_handles_labels()
    legend_below(fig, h, l, ncol=3 if wide else 1)
    save(fig, "fig5", wide)


def main():
    os.makedirs(FIGS, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5):
        for wide in (False, True):
            f(wide)
    print("figures written to", FIGS)


if __name__ == "__main__":
    main()
