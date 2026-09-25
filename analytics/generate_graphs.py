from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RESULTS = Path("analytics/results")
PNG = RESULTS / "plots"
PNG.mkdir(parents=True, exist_ok=True)

def main():
    files = list(RESULTS.glob("*.csv"))
    if not files:
        print("No experiment CSVs found.")
        return
    for f in files:
        df = pd.read_csv(f)
        if "processing_latency_ms" in df:
            ax = df["processing_latency_ms"].plot(title=f"{f.stem}: processing latency")
            ax.set_xlabel("Sample"); ax.set_ylabel("Latency (ms)")
            fig = ax.get_figure(); fig.tight_layout(); fig.savefig(PNG / f"{f.stem}_latency.png"); plt.close(fig)
        if "decision" in df:
            ax = df["decision"].value_counts().plot(kind="bar", title=f"{f.stem}: Edge vs Cloud")
            ax.set_xlabel("Decision"); ax.set_ylabel("Count")
            fig = ax.get_figure(); fig.tight_layout(); fig.savefig(PNG / f"{f.stem}_decision.png"); plt.close(fig)

if __name__ == "__main__":
    main()
