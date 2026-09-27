from __future__ import annotations
import hashlib
import time


def _bounded_work(units: int) -> str:
    """Deterministic CPU work used by the software-only research prototype."""
    value = b"edge-cloud-orchestration"
    for _ in range(max(1, units)):
        value = hashlib.sha256(value).digest()
    return value.hex()[:16]


def process_on_edge(data: dict) -> dict:
    complexity = int(data.get("task_complexity", 1))
    units = 1200 + complexity * 450
    started = time.perf_counter()
    digest = _bounded_work(units)
    compute_ms = (time.perf_counter() - started) * 1000
    return {
        "execution_location": "EDGE",
        "compute_latency_ms": round(compute_ms, 3),
        "transport_latency_ms": 0.0,
        "processor_result": digest,
    }
