"""AW change cell: mutate dot state; it does not know how to render pixels."""
from __future__ import annotations

import random
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class Dot(TypedDict):
    id: str
    x: float
    y: float
    radius: float
    opacity: float
    phase: float


class AnimationState(TypedDict):
    dots: list[Dot]
    frame: int
    width: int
    height: int
    seed: int


def aw_change(state: AnimationState) -> AnimationState:
    """One abstract visual change step.

    The cell deliberately returns state only. Pillow remains a separate renderer.
    """
    rng = random.Random(state["seed"] + state["frame"])
    dots: list[Dot] = []
    for dot in state["dots"]:
        angle = dot["phase"] + rng.uniform(-0.35, 0.35)
        step = rng.uniform(0.8, 3.2)
        dots.append(
            {
                **dot,
                "x": (dot["x"] + step * __import__("math").cos(angle)) % state["width"],
                "y": (dot["y"] + step * __import__("math").sin(angle)) % state["height"],
                "radius": max(1.0, min(8.0, dot["radius"] + rng.uniform(-0.25, 0.25))),
                "opacity": max(0.2, min(1.0, dot["opacity"] + rng.uniform(-0.03, 0.03))),
                "phase": angle,
            }
        )
    return {**state, "dots": dots, "frame": state["frame"] + 1}


def build_graph():
    graph = StateGraph(AnimationState)
    graph.add_node("aw", aw_change)
    graph.add_edge(START, "aw")
    graph.add_edge("aw", END)
    return graph.compile()


def step(state: AnimationState) -> AnimationState:
    return build_graph().invoke(state)
