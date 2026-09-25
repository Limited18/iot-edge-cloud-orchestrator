from __future__ import annotations
import argparse, json, random, time, uuid
import paho.mqtt.client as mqtt

def make_reading(mode: str) -> dict:
    smoke = False
    intrusion = False
    motion = random.random() < 0.25
    if mode == "priority":
        smoke = True
        intrusion = random.random() < 0.5
        motion = True
    elif mode == "mixed":
        smoke = random.random() < 0.05
        intrusion = random.random() < 0.03
    temperature = random.uniform(22, 35)
    if smoke:
        temperature = random.uniform(72, 92)
    return {
        "task_id": str(uuid.uuid4()),
        "sensor_id": "sim-001",
        "timestamp": time.time(),
        "temperature": round(temperature, 2),
        "humidity": round(random.uniform(35, 75), 2),
        "motion": motion,
        "smoke": smoke,
        "intrusion": intrusion,
        "task_type": random.choice(["monitoring", "aggregation", "analytics"]),
        "task_complexity": random.randint(1, 10),
        "data_size_kb": round(random.uniform(1, 200), 2),
        "response_deadline_ms": random.choice([20, 50, 100, 250]),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=1883)
    p.add_argument("--topic", default="iot/sensors")
    p.add_argument("--interval", type=float, default=2.0)
    p.add_argument("--mode", choices=["normal", "priority", "mixed"], default="mixed")
    args = p.parse_args()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(args.host, args.port, 60)
    client.loop_start()
    print(f"Publishing to {args.topic} every {args.interval}s")
    try:
        while True:
            reading = make_reading(args.mode)
            client.publish(args.topic, json.dumps(reading), qos=0)
            print(reading)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
