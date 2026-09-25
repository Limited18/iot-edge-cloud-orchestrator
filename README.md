# IoT Edge–Cloud Service Orchestrator

Software-only implementation of an IoT Edge–Cloud orchestration architecture for an IEEE-style research prototype.

## Architecture

Sensor Simulator → Mosquitto MQTT → FastAPI Edge Orchestrator → Priority Engine → ML Edge/Cloud Decision → Edge/Cloud Processing → Firebase Firestore → React Dashboard.

## Features
- Simulated temperature, humidity, motion, smoke and intrusion sensors
- MQTT publishing via Paho and Mosquitto
- Edge-side preprocessing
- Rule-based emergency priority engine
- Random Forest Edge/Cloud decision model with deterministic fallback
- CPU/RAM and latency metrics
- Firebase Firestore persistence when configured
- Experiment modes: normal workload, priority event, network degradation and resource contention
- React dashboard with live API polling
- Training/evaluation scripts and graph generation

## Prerequisites
- Python 3.11+
- Node.js 20+
- Mosquitto MQTT broker
- Firebase project with Firestore enabled (optional for local demo)

## Backend
Use:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
copy .env.example .env
uvicorn backend.main:app --reload --port 8000

## MQTT
mosquitto -c mosquitto/mosquitto.conf -v
python -m sensor_simulator.sensor_simulator

## ML
python -m ml.train_model

## Experiments
python -m experiments.run_experiment --scenario normal --samples 100
python -m experiments.run_experiment --scenario priority --samples 50
python -m experiments.run_experiment --scenario network_degradation --samples 100
python -m experiments.run_experiment --scenario resource_contention --samples 100
python -m analytics.generate_graphs

## Frontend
cd frontend
npm install
npm run dev

Dashboard: http://localhost:5173

See docs/FIREBASE.md for Firestore configuration. Never commit Firebase credentials.

The physical IoT layer is simulated in software; MQTT, orchestration, ML decisioning, processing, Firebase persistence and the dashboard are runnable software components. Use only measured outputs from the experiment scripts in paper results.
