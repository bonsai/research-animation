"""LangGraph AW cell: decide actions, not pixels."""
from __future__ import annotations

import math
import random
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .action import Action, apply_actions


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
    actions: list[Action]


def aw_action(state: AnimationState) -> AnimationState:
    """AW decides the next visual actions and returns no rendering concerns."""
    rng = random.Random(state["seed"] + state["frame"])
    actions: list[Action] = []
    for dot in state["dots"]:
        angle = dot["phase"] + rng.uniform(-0.35, 0.35)
        step = rng.uniform(0.8, 3.2)
        actions.append({
            "op": "move",
            "id": dot["id"],
            "value": step * math.cos(angle),
            "value_y": step * math.sin(angle),
        })
        actions.append({
            "op": "resize",
            "id": dot["id"],
            "value": rng.uniform(-0.25, 0.25),
            "value_y": 0,
        })
        actions.append({
            "op": "fade",
            "id": dot["id"],
            "value": rng.uniform(-0.03, 0.03),
            "value_y": 0,
        })
    return {**state, "actions": actions}


def apply(state: AnimationState) -> AnimationState:
    return apply_actions(state, state.get("actions", []))


def build_graph():
    graph = StateGraph(AnimationState)
    graph.add_node("aw", aw_action)
    graph.add_node("apply", apply)
    graph.add_edge(START, "aw")
    graph.add_edge("aw", "apply")
    graph.add_edge("apply", END)
    return graph.compile()


def step(state: AnimationState) -> AnimationState:
    return build_graph().invoke(state)
