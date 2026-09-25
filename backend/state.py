from __future__ import annotations

from .resource_monitor import snapshot

LATEST = {"sensor": None, "decision": None, "resources": snapshot(), "history": []}


def record(payload: dict, result: dict) -> None:
    LATEST["sensor"] = payload
    LATEST["decision"] = result
    LATEST["resources"] = {
        "edge_cpu_percent": result.get("edge_cpu_percent"),
        "edge_memory_percent": result.get("edge_memory_percent"),
    }
    LATEST["history"] = [result] + LATEST["history"][:49]
