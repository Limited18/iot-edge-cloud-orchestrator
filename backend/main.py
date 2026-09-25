from __future__ import annotations
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .resource_monitor import snapshot
from .orchestration import process_task
from .mqtt_client import start as start_mqtt
from .state import LATEST, record

mqtt_started = False

@asynccontextmanager
async def lifespan(app):
    global mqtt_started
    try:
        start_mqtt()
        mqtt_started = True
    except Exception as exc:
        print(f"[MQTT] not started: {exc}")
    yield

app = FastAPI(title="IoT Edge-Cloud Orchestrator", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "mqtt_started": mqtt_started, "time": time.time()}

@app.get("/api/status")
def status():
    LATEST["resources"] = snapshot()
    return LATEST

@app.post("/api/process")
def process(payload: dict):
    result = process_task(payload, payload.get("simulated_network_latency_ms"))
    record(payload, result)
    return result

@app.get("/api/history")
def history():
    return {"items": LATEST["history"]}
