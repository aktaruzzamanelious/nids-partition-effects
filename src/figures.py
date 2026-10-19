"""Block 5 figures F2, F3 and F4. F1 is drawn separately in a vector tool.

Reads results/analysis.json. Writes results/figures/F*.pdf (primary) and .png at
1000 dpi (raster backup), sized to the final print width.
Usage: python src/figures.py
"""
import os

for _lib in ("OMP", "OPENBLAS", "MKL", "NUMEXPR"):
    os.environ[f"{_lib}_NUM_THREADS"] = "2"

import json
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

from analyze import ARMS, CONTRASTS, DATASETS, MODELS, OUT_JSON

FIGS = "results/figures"
MM = 1 / 25.4
DOUBLE_MM = 190
PNG_DPI = 1000
MIN_PT = 7
DS_TITLE = {"unsw": "UNSW-NB15", "nslkdd": "NSL-KDD"}
# Okabe and Ito palette, colourblind safe, no red against green.
OKABE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442",
         "#000000", "#999999", "#882255"]
ARM_STYLE = {"A": ("#0072B2", "o", "-"), "B": ("#E69F00", "s", "--"),
             "C-naive": ("#009E73", "^", ":"), "C-group": ("#CC79A7", "D", "-.")}
MODEL_MARKERS = ["o", "s", "^", "D", "v", "P", "X", "<", ">", "h"]
PANEL = {"unsw": "(a) UNSW-NB15", "nslkdd": "(b) NSL-KDD"}
# Figure labels only; the tables keep the M codes. Classes are listed in Table 2.
SHORT = {"M01": "NB", "M02": "LR", "M03": "Ridge", "M04": "DT", "M05": "RF", "M06": "ET",
         "M07": "AB", "M08": "HGB", "M09": "XGB", "M10": "LGBM"}

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "Nimbus Sans"],
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9, "xtick.labelsize": 8,
    "ytick.labelsize": 8, "legend.fontsize": 8, "axes.unicode_minus": False})


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def spread(values, gap):
    # Nudges label positions apart so tied ranks stay legible, keeping their order.
    order = np.argsort(values, kind="stable")
    pos = np.array(values, dtype=float)
    for a, b in zip(order[:-1], order[1:]):
        if pos[b] - pos[a] < gap:
            pos[b] = pos[a] + gap
    shift = (pos[order].mean() - np.mean(values))
    return pos - shift


def save(fig, name):
    fig.canvas.draw()
    sizes = [t.get_fontsize() for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip()]
    texts = [t.get_text() for t in fig.findobj(matplotlib.text.Text)]
    if any("\u2014" in t for t in texts):
        raise SystemExit(f"STOP: em dash found in {name}")
    if min(sizes) < MIN_PT:
        raise SystemExit(f"STOP: {name} has text at {min(sizes)} pt, below {MIN_PT} pt")
    # No creation date in the PDF, so a rerun writes a byte-identical file.
    fig.savefig(f"{FIGS}/{name}.pdf", metadata={"CreationDate": None})
    fig.savefig(f"{FIGS}/{name}.png", dpi=PNG_DPI)
    w, h = fig.get_size_inches() / MM
    log(f"{name}: {w:.0f} x {h:.0f} mm, smallest text {min(sizes)} pt, pdf and png written")
    plt.close(fig)
    return {"width_mm": w, "height_mm": h, "min_pt": min(sizes)}


def strictly_overlap(a, b):
    tol = 1e-6
    return (a.x0 < b.x1 - tol and b.x0 < a.x1 - tol and a.y0 < b.y1 - tol
            and b.y0 < a.y1 - tol)


def clear_label_overlaps(fig, labels):
    # labels: (panel, text) pairs. The visually lower label of an overlapping pair moves
    # down by exactly the overlap, then every pair is checked again.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    moved = {}
    for _ in range(200):
        boxes = [t.get_window_extent(renderer) for _, t in labels]
        hit = next(((i, j) for i in range(len(labels)) for j in range(i + 1, len(labels))
                    if strictly_overlap(boxes[i], boxes[j])), None)
        if hit is None:
            return moved
        i, j = sorted(hit, key=lambda k: -boxes[k].y1)
        (panel, upper), (_, lower) = labels[i], labels[j]
        shift_px = boxes[j].y1 - boxes[i].y0
        ax = lower.axes
        x, y = lower.get_position()
        _, y_disp = ax.transData.transform((x, y))
        new_y = ax.transData.inverted().transform((0, y_disp - shift_px))[1]
        lower.set_y(new_y)
        key = (panel, lower.get_text(), "left" if lower.get_ha() == "right" else "right")
        moved[key] = moved.get(key, 0.0) + shift_px * 72 / fig.dpi
        fig.canvas.draw()
    raise SystemExit("STOP: F2 label overlaps did not clear in 200 moves")


def f2_rank_slope(res):
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_MM * MM, 100 * MM))
    x = np.arange(len(ARMS))
    labels = []
    for ax, ds in zip(axes, DATASETS):
        ranks = np.array([res["mean_rank"][ds][arm] for arm in ARMS])
        for j, mid in enumerate(MODELS):
            ax.plot(x, ranks[:, j], color=OKABE[j], marker=MODEL_MARKERS[j], markersize=3.5,
                    linewidth=1.0, markeredgecolor="black", markeredgewidth=0.4)
        for col, ha, dx in ((0, "right", -0.12), (len(ARMS) - 1, "left", 0.12)):
            for j, y in enumerate(spread(ranks[col], 0.42)):
                labels.append((PANEL[ds], ax.text(x[col] + dx, y, SHORT[MODELS[j]], ha=ha,
                                                  va="center", fontsize=7, color="black")))
        ax.set_xticks(x, ARMS)
        ax.set_xlim(-0.75, len(ARMS) - 0.25)
        ax.set_ylim(10.8, 0.2)
        ax.set_yticks(range(1, 11))
        ax.set_ylabel("Mean MCC rank (1 = best)")
        ax.set_xlabel("Evaluation arm")
        ax.set_title(PANEL[ds])
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    moved = clear_label_overlaps(fig, labels)
    for (panel, name, side), pt in moved.items():
        log(f"F2 moved label: {panel}, {side} end, {name}, down {pt:.3f} pt")
    log(f"F2 labels moved: {len(moved)}")
    return save(fig, "F2_rank_slope")


def f3_mcc_by_arm(res):
    fig, axes = plt.subplots(2, 1, figsize=(DOUBLE_MM * MM, 150 * MM))
    x = np.arange(len(MODELS))
    offsets = np.linspace(-0.3, 0.3, len(ARMS))
    bars = []
    for ax, ds in zip(axes, DATASETS):
        for off, arm in zip(offsets, ARMS):
            colour, marker, ls = ARM_STYLE[arm]
            mean = np.array([res["per_model"][ds][arm][m]["mcc_mean"] for m in MODELS])
            ci = np.array([res["bootstrap"][ds]["model_ci"][arm]["mcc"][m] for m in MODELS])
            err = np.vstack([mean - ci[:, 0], ci[:, 1] - mean])
            eb = ax.errorbar(x + off, mean, yerr=err, fmt=marker, color=colour,
                             markersize=3.5, capsize=2, elinewidth=0.9, label=arm)
            eb[2][0].set_linestyle(ls)
            bars += [(ax, marker, x[j] + off, ci[j]) for j in range(len(MODELS))]
        ax.set_xticks(x, [SHORT[m] for m in MODELS])
        ax.set_ylabel("MCC, mean over seeds or repeats")
        ax.set_title(PANEL[ds])
        ax.grid(axis="y", linewidth=0.4, color="#cccccc")
        ax.spines[["top", "right"]].set_visible(False)
    handles, names = axes[0].get_legend_handles_labels()
    fig.legend(handles, names, title="Arm, error bars are 95% bootstrap intervals", ncols=4,
               frameon=False, loc="upper center", title_fontsize=8)
    axes[-1].set_xlabel("Model")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.canvas.draw()
    short = 0
    for ax, marker, xpos, (lo, hi) in bars:
        # Bar height and marker height both in points on the drawn figure.
        (_, y0), (_, y1) = ax.transData.transform([(xpos, lo), (xpos, hi)])
        style = matplotlib.markers.MarkerStyle(marker)
        path = style.get_path().transformed(style.get_transform())
        short += abs(y1 - y0) * 72 / fig.dpi < path.get_extents().height * 3.5
    log(f"F3 error bars shorter than their marker: {short} of {len(bars)}")
    return save(fig, "F3_mcc_by_arm")


def f4_bootstrap_tau(res):
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_MM * MM, 85 * MM))
    labels = [f"{a} vs\n{b}" for a, b in CONTRASTS]
    for ax, ds in zip(axes, DATASETS):
        dists = [np.array(res["bootstrap"][ds]["contrasts"][f"{a} vs {b}"]["mcc"]
                          ["tau_b_dist"]) for a, b in CONTRASTS]
        pos = np.arange(1, len(dists) + 1)
        varied = [i for i, d in enumerate(dists) if d.std() > 0]
        if varied:
            parts = ax.violinplot([dists[i] for i in varied], positions=pos[varied],
                                  widths=0.8, showmeans=False, showmedians=False,
                                  showextrema=False)
            for body in parts["bodies"]:
                body.set_facecolor("#56B4E9")
                body.set_edgecolor("black")
                body.set_alpha(0.6)
        for i, d in enumerate(dists):
            if d.std() == 0:
                ax.plot([pos[i] - 0.3, pos[i] + 0.3], [d[0], d[0]], color="black")
        cis = np.array([res["bootstrap"][ds]["contrasts"][f"{a} vs {b}"]["mcc"]["tau_b_ci"]
                        for a, b in CONTRASTS])
        est = np.array([res["between_arm"][ds][f"{a} vs {b}"]["ten"]["mcc"]["tau_b"]["mean"]
                        for a, b in CONTRASTS])
        ci_h = ax.errorbar(pos, cis.mean(axis=1), yerr=(cis[:, 1] - cis[:, 0]) / 2, fmt="none",
                           ecolor="black", elinewidth=1.0, capsize=3, zorder=3)
        pt_h, = ax.plot(pos, est, linestyle="none", marker="D", markersize=4.5,
                        color="black", zorder=4)
        floor = res["within_arm"][ds]["C-naive"]["mcc"]["p5"]
        fl_h = ax.axhline(floor, color="#D55E00", linestyle="--", linewidth=1.0)
        top = max(max(d.max() for d in dists), floor, cis.max(), est.max())
        bottom = min(min(d.min() for d in dists), cis.min(), est.min())
        ax.set_ylim(top=top + 0.35 * (top - bottom))
        ax.legend([pt_h, ci_h, fl_h], ["Point estimate", "95% percentile interval",
                                       f"C-naive within-arm floor, 5th percentile = {floor:.3f}"],
                  loc="upper left", frameon=False, fontsize=7)
        # Headroom for the legend only; tau-b cannot exceed 1, so no tick above it.
        ax.set_yticks([t for t in ax.get_yticks() if t <= 1.0 + 1e-9])
        ax.set_xticks(pos, labels)
        ax.set_xlim(0.4, len(dists) + 0.6)
        ax.set_ylabel("Mean Kendall tau-b, MCC ranks")
        ax.set_title(PANEL[ds])
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return save(fig, "F4_bootstrap_tau")


def main():
    os.makedirs(FIGS, exist_ok=True)
    with open(OUT_JSON) as fh:
        res = json.load(fh)
    family = font_manager.FontProperties(family=plt.rcParams["font.family"])
    log(f"resolved font file {font_manager.findfont(family)}")
    for fn in (f2_rank_slope, f3_mcc_by_arm, f4_bootstrap_tau):
        fn(res)


if __name__ == "__main__":
    main()
