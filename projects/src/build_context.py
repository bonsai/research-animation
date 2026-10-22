#!/usr/bin/env python3
"""Build a contextual prompt from an experiment context JSON for EXP-CTX-001.

Reads a context file with previous runs, evaluations, and ontology,
then constructs a natural-language prompt prefixed with history and feedback.
Outputs the prompt and writes the next-run context JSON.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


def format_run(run: dict) -> str:
    """Format a single previous run as a compact history entry."""
    evals = run.get("evaluation", {})
    scores = [f"{k[0:3]}={v}" for k, v in evals.items() if v is not None]
    fb = run.get("feedback_text", "").strip()
    parts = [
        f"Run{run.get('run_index', '?')}: {run.get('prompt', '')}",
        f"  p={run.get('parameters', {})}",
        f"  scores=({', '.join(scores)})",
    ]
    if fb:
        parts.append(f"  feedback: {fb}")
    return "\n".join(parts)


def build_history(previous_runs: list[dict]) -> str:
    if not previous_runs:
        return "(no previous runs)"
    return "\n---\n".join(format_run(r) for r in previous_runs)


def target_line(target: dict) -> str:
    lines = [target.get("description", "")]
    onto = target.get("ontology", [])
    if onto:
        lines.append(f"Ontology: {', '.join(onto)}")
    return "\n".join(lines)


def build_prompt(ctx: dict) -> str:
    target = ctx.get("target", {})
    prev = ctx.get("previous_runs", [])

    lines = []
    lines.append("[Target]")
    lines.append(target_line(target))
    lines.append("")

    if prev:
        lines.append("[History]")
        lines.append(build_history(prev))
        lines.append("")

        # Summarize the most recent feedback as a compact directive
        last = prev[-1]
        fb = last.get("feedback_text", "").strip()
        if fb:
            lines.append("[Directive from last evaluation]")
            lines.append(fb)
            lines.append("")

    # Carry forward the prompt from the current run (already updated by feedback)
    # or fall back to the latest previous run / initial parameters.
    current_run = ctx.get("current_run", {})
    if current_run and current_run.get("prompt"):
        current_prompt = current_run["prompt"]
    elif prev:
        current_prompt = prev[-1].get("prompt", "")
    else:
        current_prompt = ctx.get("initial_parameters", {}).get("prompt", "")

    lines.append("[Generate]")
    lines.append(current_prompt)

    return "\n".join(lines)


def build_next_context(ctx: dict) -> dict:
    """Append the current_run to previous_runs and initialize a new current_run."""
    current = ctx.get("current_run", {})
    if current.get("image_path") or current.get("evaluation", {}).get("quality") is not None:
        # There is data: move current to previous
        ctx.setdefault("previous_runs", []).append(current)

    # Derive next prompt from feedback if any
    prev_fb = current.get("feedback_text", "").strip()
    next_prompt = current.get("prompt", "")
    if prev_fb:
        # Simple concatenation strategy: append feedback as prefix
        next_prompt = f"{prev_fb}, {next_prompt}"

    # Slightly mutate seed for variation
    old_seed = current.get("parameters", {}).get("seed", 42)
    next_seed = old_seed + 1

    ctx["current_run"] = {
        "run_index": current.get("run_index", 0) + 1,
        "prompt": next_prompt,
        "negative_prompt": current.get("negative_prompt", ""),
        "parameters": {
            **current.get("parameters", {}),
            "seed": next_seed,
        },
        "ontology": current.get("ontology", []),
        "image_path": "",
        "evaluation": {
            "quality": None,
            "composition": None,
            "color": None,
            "line": None,
            "mood": None,
            "semantic": None,
            "preference": None,
        },
        "feedback_text": "",
    }
    return ctx


def main() -> None:
    parser = argparse.ArgumentParser(description="Build contextual prompt from experiment context.")
    parser.add_argument("--context", required=True, help="Path to context JSON (input)")
    parser.add_argument("--output-prompt", default="-", help="Path to write the built prompt (default: stdout)")
    parser.add_argument("--output-context", help="Path to write the next-run context JSON")
    args = parser.parse_args()

    ctx_path = Path(args.context)
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))

    prompt = build_prompt(ctx)

    if args.output_prompt == "-":
        print(prompt)
    else:
        Path(args.output_prompt).write_text(prompt, encoding="utf-8")
        print(f"Wrote prompt to {args.output_prompt}")

    if args.output_context:
        next_ctx = build_next_context(ctx)
        Path(args.output_context).write_text(
            json.dumps(next_ctx, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote next context to {args.output_context}")


if __name__ == "__main__":
    main()
