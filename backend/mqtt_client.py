import json
import paho.mqtt.client as mqtt
from .config import settings
from .orchestration import process_task

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def start():
    def on_connect(c, userdata, flags, reason_code, properties):
        print(f"[MQTT] connected: {reason_code}")
        c.subscribe(settings.mqtt_topic)
    def on_message(c, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            result = process_task(data, data.get("simulated_network_latency_ms"))
            print(f"[EDGE] {result['task_id']} -> {result['decision']} ({result['processing_latency_ms']} ms)")
        except Exception as exc:
            print(f"[MQTT] message error: {exc}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.mqtt_host, settings.mqtt_port, 60)
    client.loop_start()
