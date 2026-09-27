from __future__ import annotations
import hashlib
import time


def _bounded_work(units: int) -> str:
    value = b"cloud-processing"
    for _ in range(max(1, units)):
        value = hashlib.sha256(value).digest()
    return value.hex()[:16]


def process_in_cloud(data: dict, network_latency_ms: float) -> dict:
    """Software-only cloud model: uplink + cloud compute + downlink."""
    complexity = int(data.get("task_complexity", 1))
    units = 700 + complexity * 260
    transport_ms = max(0.0, float(network_latency_ms)) * 2.0
    started = time.perf_counter()
    time.sleep(transport_ms / 1000.0)
    digest = _bounded_work(units)
    compute_ms = (time.perf_counter() - started) * 1000 - transport_ms
    return {
        "execution_location": "CLOUD",
        "compute_latency_ms": round(max(0.0, compute_ms), 3),
        "transport_latency_ms": round(transport_ms, 3),
        "processor_result": digest,
    }
