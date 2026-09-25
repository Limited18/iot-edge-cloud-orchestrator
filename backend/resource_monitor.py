import psutil

def snapshot() -> dict:
    return {
        "edge_cpu_percent": round(psutil.cpu_percent(interval=0.05), 2),
        "edge_memory_percent": round(psutil.virtual_memory().percent, 2),
    }
