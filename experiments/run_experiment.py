from __future__ import annotations
import argparse, csv, random
from pathlib import Path
from backend.orchestration import process_task

OUT = Path("analytics/results")
OUT.mkdir(parents=True, exist_ok=True)

def scenario_payload(scenario: str, i: int):
    payload = {
        "task_id": f"{scenario}-{i}",
        "sensor_id": "exp-001",
        "temperature": random.uniform(24, 32),
        "humidity": random.uniform(40, 70),
        "motion": False,
        "smoke": False,
        "intrusion": False,
        "task_type": random.choice(["monitoring", "aggregation", "analytics"]),
        "task_complexity": random.randint(1, 10),
        "data_size_kb": random.uniform(5, 200),
        "response_deadline_ms": random.choice([20, 50, 100, 250]),
    }
    latency = random.uniform(8, 40)
    if scenario == "priority":
        payload.update(smoke=True, intrusion=(i % 4 == 0), motion=True, temperature=random.uniform(75, 90),
                       task_type="emergency", response_deadline_ms=20)
    elif scenario == "network_degradation":
        latency = random.uniform(150, 350)
    elif scenario == "resource_contention":
        payload["task_complexity"] = random.randint(6, 10)
        payload["data_size_kb"] = random.uniform(100, 250)
        latency = random.uniform(20, 60)
    return payload, latency

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", choices=["normal","priority","network_degradation","resource_contention"], required=True)
    p.add_argument("--samples", type=int, default=100)
    a = p.parse_args()
    path = OUT / f"{a.scenario}.csv"
    rows = []
    for i in range(a.samples):
        payload, latency = scenario_payload(a.scenario, i)
        result = process_task(payload, latency)
        rows.append({**result, "scenario": a.scenario})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(path)

if __name__ == "__main__":
    main()
