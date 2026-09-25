from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = Path("analytics/results")
PNG = RESULTS / "plots"
PNG.mkdir(parents=True, exist_ok=True)

SCENARIOS = ["normal", "priority", "network_degradation", "resource_contention"]


def load_results():
    frames = []
    for scenario in SCENARIOS:
        path = RESULTS / f"{scenario}.csv"
        if path.exists():
            df = pd.read_csv(path)
            df["scenario"] = scenario
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def summary_table(df):
    rows = []
    for scenario, g in df.groupby("scenario", sort=False):
        decisions = g["decision"].value_counts()
        rows.append({
            "scenario": scenario,
            "samples": len(g),
            "avg_processing_latency_ms": round(g["processing_latency_ms"].mean(), 3),
            "min_processing_latency_ms": round(g["processing_latency_ms"].min(), 3),
            "max_processing_latency_ms": round(g["processing_latency_ms"].max(), 3),
            "avg_network_latency_ms": round(g["network_latency_ms"].mean(), 3),
            "avg_edge_cpu_percent": round(g["edge_cpu_percent"].mean(), 3),
            "avg_edge_memory_percent": round(g["edge_memory_percent"].mean(), 3),
            "edge_decisions": int(decisions.get("EDGE", 0)),
            "cloud_decisions": int(decisions.get("CLOUD", 0)),
            "edge_percent": round(decisions.get("EDGE", 0) / len(g) * 100, 2),
            "cloud_percent": round(decisions.get("CLOUD", 0) / len(g) * 100, 2),
            "critical_events": int((g["priority"] == "CRITICAL").sum()),
        })
    return pd.DataFrame(rows)


def save_plot(fig, name):
    fig.tight_layout()
    fig.savefig(PNG / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    df = load_results()
    if df.empty:
        print("No experiment CSVs found.")
        return

    summary = summary_table(df)
    summary.to_csv(RESULTS / "experiment_summary.csv", index=False)

    # Cross-scenario average processing latency.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(summary["scenario"], summary["avg_processing_latency_ms"])
    ax.set_title("Average Processing Latency by Scenario")
    ax.set_ylabel("Latency (ms)")
    ax.tick_params(axis="x", rotation=20)
    save_plot(fig, "comparison_average_latency.png")

    # Cross-scenario network latency.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(summary["scenario"], summary["avg_network_latency_ms"])
    ax.set_title("Average Network Latency by Scenario")
    ax.set_ylabel("Network latency (ms)")
    ax.tick_params(axis="x", rotation=20)
    save_plot(fig, "comparison_network_latency.png")

    # CPU and memory.
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(summary))
    width = 0.36
    ax.bar([i - width / 2 for i in x], summary["avg_edge_cpu_percent"], width, label="CPU %")
    ax.bar([i + width / 2 for i in x], summary["avg_edge_memory_percent"], width, label="Memory %")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["scenario"], rotation=20)
    ax.set_title("Average Edge Resource Utilization")
    ax.set_ylabel("Utilization (%)")
    ax.legend()
    save_plot(fig, "comparison_edge_resources.png")

    # Edge/cloud routing distribution.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(summary["scenario"], summary["edge_percent"], label="EDGE")
    ax.bar(summary["scenario"], summary["cloud_percent"],
           bottom=summary["edge_percent"], label="CLOUD")
    ax.set_title("Edge vs Cloud Routing Distribution")
    ax.set_ylabel("Share of decisions (%)")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=20)
    ax.legend()
    save_plot(fig, "comparison_edge_cloud_distribution.png")

    # Individual scenario latency plots.
    for scenario, g in df.groupby("scenario"):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(g.index, g["processing_latency_ms"])
        ax.set_title(f"{scenario}: Processing Latency")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Latency (ms)")
        save_plot(fig, f"{scenario}_latency.png")

    print(RESULTS / "experiment_summary.csv")


if __name__ == "__main__":
    main()
