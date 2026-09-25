from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mqtt_host: str = os.getenv("MQTT_HOST", "127.0.0.1")
    mqtt_port: int = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_topic: str = os.getenv("MQTT_TOPIC", "iot/sensors")
    firebase_credentials: str = os.getenv("FIREBASE_CREDENTIALS", "")
    decision_collection: str = os.getenv("FIREBASE_COLLECTION_DECISION", "decisions")
    cloud_processing_delay_ms: float = float(os.getenv("CLOUD_PROCESSING_DELAY_MS", "25"))
    model_path: str = os.getenv("MODEL_PATH", "ml/artifacts/edge_cloud_model.joblib")

settings = Settings()
