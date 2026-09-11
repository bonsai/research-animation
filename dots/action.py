"""AW action interface.

An action is the explicit, serializable change produced for one animation step.
It can later be replaced by another policy without changing the Pillow renderer.
"""
from __future__ import annotations

from typing import Literal, TypedDict


class Action(TypedDict):
    op: Literal["move", "resize", "fade"]
    id: str
    value: float
    value_y: float


def apply_actions(state: dict, actions: list[Action]) -> dict:
    """Apply serialized actions to a dot state."""
    by_id = {dot["id"]: dot for dot in state["dots"]}
    for action in actions:
        dot = by_id.get(action["id"])
        if dot is None:
            continue
        if action["op"] == "move":
            dot["x"] = (dot["x"] + action["value"]) % state["width"]
            dot["y"] = (dot["y"] + action["value_y"]) % state["height"]
        elif action["op"] == "resize":
            dot["radius"] = max(1.0, min(8.0, dot["radius"] + action["value"]))
        elif action["op"] == "fade":
            dot["opacity"] = max(0.0, min(1.0, dot["opacity"] + action["value"]))
    return {**state, "frame": state["frame"] + 1}
