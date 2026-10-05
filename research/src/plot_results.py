#!/usr/bin/env python3
"""Plot EXP-CTX-001 results (score transition over iterations)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


def load_runs(context_dir: Path) -> list[dict]:
    """Load all context-run*.json files and extract evaluation scores."""
    files = sorted(context_dir.glob("context-run*.json"))
    rows = []
    for f in files:
        ctx = json.loads(f.read_text(encoding="utf-8"))
        cr = ctx.get("current_run", {})
        pr = ctx.get("previous_runs", [])
        # Use current_run if it has evaluation, else last previous_run
        if cr.get("evaluation", {}).get("quality") is not None:
            run = cr
        elif pr:
            run = pr[-1]
        else:
            continue
        e = run.get("evaluation", {})
        rows.append({
            "run": len(rows) + 1,
            "quality": e.get("quality", 0),
            "composition": e.get("composition", 0),
            "color": e.get("color", 0),
            "line": e.get("line", 0),
            "mood": e.get("mood", 0),
            "semantic": e.get("semantic", 0),
            "preference": e.get("preference", 0),
        })
    return rows


def plot_scores(rows: list[dict], out_path: Path, title: str = "EXP-CTX-001 Score Transition") -> None:
    runs = [r["run"] for r in rows]
    axes = ["quality", "composition", "color", "line", "mood", "semantic", "preference"]
    colors = {
        "quality": "#2E86AB",
        "composition": "#A23B72",
        "color": "#F18F01",
        "line": "#C73E1D",
        "mood": "#3B1F2B",
        "semantic": "#06A77D",
        "preference": "#6A4C93",
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    for axis in axes:
        vals = [r[axis] for r in rows]
        ax.plot(runs, vals, marker="o", label=axis, color=colors.get(axis), linewidth=2)

    ax.axhline(y=4, color="green", linestyle="--", alpha=0.5, label="target threshold")
    ax.axhline(y=5, color="gold", linestyle="--", alpha=0.5, label="perfect score")
    ax.set_xlabel("Iteration (Run)", fontsize=12)
    ax.set_ylabel("Score (1–5)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xticks(runs)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0.5, 5.5)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

    # Annotate target achievement
    for r in rows:
        if all(r[a] == 5 for a in axes):
            ax.annotate("★ TARGET\n  ACHIEVED", xy=(r["run"], 5),
                       xytext=(r["run"] - 0.3, 4.2),
                       fontsize=10, color="darkgreen", fontweight="bold",
                       arrowprops=dict(arrowstyle="->", color="darkgreen"))

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved plot to {out_path}")


def plot_radar(rows: list[dict], out_path: Path, title: str = "EXP-CTX-001 Final State") -> None:
    """Radar chart for the final run."""
    if not rows:
        return
    final = rows[-1]
    axes = ["quality", "composition", "color", "line", "mood", "semantic", "preference"]
    labels = [a[:3].upper() for a in axes]
    vals = [final[a] for a in axes]
    angles = [n / float(len(axes)) * 2 * 3.14159 for n in range(len(axes))]
    vals += vals[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, vals, color="#2E86AB", alpha=0.25)
    ax.plot(angles, vals, color="#2E86AB", linewidth=2, marker="o")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_title(f"{title}\nRun {final['run']}", fontsize=12, fontweight="bold", pad=20)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved radar to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-dir", default="experiments/EXP-CTX-001/D")
    parser.add_argument("--output", default="experiments/EXP-CTX-001/scores.png")
    parser.add_argument("--radar", default="experiments/EXP-CTX-001/radar.png")
    args = parser.parse_args()

    ctx_dir = Path(args.context_dir)
    rows = load_runs(ctx_dir)
    if not rows:
        print("No data found.")
        return

    plot_scores(rows, Path(args.output))
    plot_radar(rows, Path(args.radar))


if __name__ == "__main__":
    main()
