from __future__ import annotations
import os
import random
import time
import joblib
import pandas as pd
from .config import settings
from .priority_engine import evaluate_priority
from .resource_monitor import snapshot
from .firebase_service import write

_model = None

def _load_model():
    global _model
    if _model is None and os.path.exists(settings.model_path):
        try:
            _model = joblib.load(settings.model_path)
        except Exception as exc:
            print(f"[ML] model load failed: {exc}")
    return _model

def build_features(data: dict, resources: dict, network_latency_ms: float):
    priority_map = {"NORMAL": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    task_map = {"monitoring": 0, "aggregation": 1, "analytics": 2, "emergency": 3}
    priority, _ = evaluate_priority(data)
    return [
        resources["edge_cpu_percent"],
        resources["edge_memory_percent"],
        float(network_latency_ms),
        float(data.get("data_size_kb", 1)),
        float(data.get("task_complexity", 1)),
        priority_map[priority],
        task_map.get(data.get("task_type", "monitoring"), 0),
        float(data.get("response_deadline_ms", 100)),
    ]

def fallback_decision(data, resources, network_latency_ms):
    priority, reason = evaluate_priority(data)
    if priority in {"CRITICAL", "HIGH"}:
        return "EDGE", reason
    if network_latency_ms >= 120:
        return "EDGE", "High network latency"
    if resources["edge_cpu_percent"] >= 80 or resources["edge_memory_percent"] >= 85:
        return "CLOUD", "Edge resource contention"
    if data.get("task_type") == "analytics" and data.get("task_complexity", 1) >= 7:
        return "CLOUD", "Compute-heavy analytics task"
    return "EDGE", "Low-latency local execution"

def decide(data, network_latency_ms=None):
    resources = snapshot()
    net = float(network_latency_ms if network_latency_ms is not None else random.uniform(8, 45))
    priority, priority_reason = evaluate_priority(data)
    model = _load_model()
    source = "fallback"
    # Safety/priority override: urgent events must stay on the Edge
    # regardless of the ML prediction, because the orchestration policy
    # gives latency-sensitive critical/high events precedence.
    if priority in {"CRITICAL", "HIGH"}:
        decision = "EDGE"
        reason = f"Priority override; {priority_reason}"
        source = "priority_engine"
    elif model is not None:
        try:
            features = build_features(data, resources, net)
            feature_names = getattr(model, "feature_names_in_", None)
            if feature_names is not None:
                X = pd.DataFrame([features], columns=list(feature_names))
            else:
                X = [features]
            decision = str(model.predict(X)[0]).upper()
            reason = f"ML prediction; priority={priority}; {priority_reason}"
            source = "random_forest"
        except Exception:
            decision, reason = fallback_decision(data, resources, net)
    else:
        decision, reason = fallback_decision(data, resources, net)
    return {
        "decision": decision,
        "decision_source": source,
        "priority": priority,
        "priority_reason": priority_reason,
        "network_latency_ms": round(net, 2),
        **resources,
    }

def process_task(data, network_latency_ms=None):
    started = time.perf_counter()
    result = decide(data, network_latency_ms)
    time.sleep(settings.cloud_processing_delay_ms / 1000 if result["decision"] == "CLOUD" else 0.005)
    result["processing_latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
    result["task_id"] = data.get("task_id")
    result["task_type"] = data.get("task_type", "monitoring")
    write(settings.decision_collection, {**result, "sensor_id": data.get("sensor_id")})
    return result
