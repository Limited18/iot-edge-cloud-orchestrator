import time
from backend.config import settings

def process(payload: dict) -> dict:
    started = time.perf_counter()
    time.sleep(settings.cloud_processing_delay_ms / 1000)
    return {"status": "processed", "task_id": payload.get("task_id"), "processing_ms": round((time.perf_counter()-started)*1000, 3)}

if __name__ == "__main__":
    print("Cloud worker simulation ready.")
