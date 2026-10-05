#!/usr/bin/env python3
"""Plot comparison of all 4 groups (A/B/C/D) for EXP-CTX-001."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


def load_group(group_dir: Path) -> list[float]:
    """Load average scores per run for a group."""
    files = sorted(group_dir.glob("context-run*.json"))
    avgs = []
    for f in files:
        ctx = json.loads(f.read_text(encoding="utf-8"))
        cr = ctx.get("current_run", {})
        e = cr.get("evaluation", {})
        vals = [v for v in e.values() if isinstance(v, (int, float))]
        if vals:
            avgs.append(sum(vals) / len(vals))
        else:
            avgs.append(0)
    return avgs


def plot_comparison(base_dir: Path, out_path: Path) -> None:
    groups = {
        "A: Fixed prompt (no feedback)": load_group(base_dir / "A"),
        "B: Prompt inheritance": load_group(base_dir / "B"),
        "C: Prompt + aggregate score": load_group(base_dir / "C"),
        "D: Full context (sub-axis + ontology)": load_group(base_dir / "D"),
    }

    colors = {
        "A: Fixed prompt (no feedback)": "#999999",
        "B: Prompt inheritance": "#E69F00",
        "C: Prompt + aggregate score": "#56B4E9",
        "D: Full context (sub-axis + ontology)": "#009E73",
    }

    fig, ax = plt.subplots(figsize=(11, 6))

    for label, avgs in groups.items():
        runs = list(range(1, len(avgs) + 1))
        ax.plot(runs, avgs, marker="o", label=label, color=colors[label], linewidth=2.5, markersize=6)
        # Mark target achievement point
        for i, v in enumerate(avgs):
            if v >= 4.0:
                ax.scatter([i+1], [v], color=colors[label], s=150, zorder=5, edgecolors="black", linewidths=1.5)
                break

    ax.axhline(y=4, color="green", linestyle="--", alpha=0.4, label="target threshold (avg=4)")
    ax.axhline(y=5, color="gold", linestyle="--", alpha=0.3, label="perfect score")

    ax.set_xlabel("Iteration (Run)", fontsize=13)
    ax.set_ylabel("Average Score (1–5)", fontsize=13)
    ax.set_title("EXP-CTX-001: Comparison of Feedback Strategies\n(Full Context vs Baselines)", fontsize=14, fontweight="bold")
    ax.set_xticks(range(1, 11))
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(1.5, 5.3)
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Annotation for D
    ax.annotate("★ D achieves target\n   at Run 3", xy=(3, 5.0), xytext=(4.5, 4.5),
                fontsize=11, color="#009E73", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#009E73", lw=1.5))
    # Annotation for C
    ax.annotate("C achieves target\nat Run 6", xy=(6, groups["C: Prompt + aggregate score"][5]),
                xytext=(7, 3.2), fontsize=10, color="#0072B2",
                arrowprops=dict(arrowstyle="->", color="#0072B2", lw=1.2))

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved comparison plot to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default="experiments/EXP-CTX-001")
    parser.add_argument("--output", default="experiments/EXP-CTX-001/comparison.png")
    args = parser.parse_args()
    plot_comparison(Path(args.base_dir), Path(args.output))


if __name__ == "__main__":
    main()
