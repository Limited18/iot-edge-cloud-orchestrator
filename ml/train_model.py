from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from .model import FEATURES

ART = Path("ml/artifacts")
ART.mkdir(parents=True, exist_ok=True)

def policy_label(row) -> str:
    if row.priority_level >= 2:
        return "EDGE"
    if row.response_deadline_ms <= 50 and row.network_latency_ms >= 80:
        return "EDGE"
    if row.edge_cpu_percent >= 82 or row.edge_memory_percent >= 88:
        return "CLOUD"
    if row.task_type == 2 and row.task_complexity >= 7 and row.data_size_kb >= 80:
        return "CLOUD"
    if row.network_latency_ms >= 180:
        return "EDGE"
    return "EDGE" if row.task_complexity < 6 else "CLOUD"

def make_dataset(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "edge_cpu_percent": rng.uniform(10, 98, n),
        "edge_memory_percent": rng.uniform(15, 95, n),
        "network_latency_ms": rng.uniform(5, 300, n),
        "data_size_kb": rng.uniform(1, 250, n),
        "task_complexity": rng.integers(1, 11, n),
        "priority_level": rng.integers(0, 4, n),
        "task_type": rng.integers(0, 4, n),
        "response_deadline_ms": rng.choice([20, 50, 100, 250, 500], n),
    })
    df["decision"] = df.apply(policy_label, axis=1)
    return df

def main():
    df = make_dataset()
    X, y = df[FEATURES], df["decision"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=180, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="weighted", zero_division=0)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision_weighted": round(float(precision), 4),
        "recall_weighted": round(float(recall), 4),
        "f1_weighted": round(float(f1), 4),
    }
    df.to_csv(ART / "synthetic_dataset.csv", index=False)
    joblib.dump(model, ART / "edge_cloud_model.joblib")
    (ART / "metrics.json").write_text(pd.Series(metrics).to_json(), encoding="utf-8")
    print(metrics)

if __name__ == "__main__":
    main()
