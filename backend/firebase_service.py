from datetime import datetime, timezone
from typing import Any
from .config import settings

_db = None
_initialized = False

def _init():
    global _db, _initialized
    if _initialized:
        return _db
    _initialized = True
    if not settings.firebase_credentials:
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if not firebase_admin._apps:
            firebase_admin.initialize_app(credentials.Certificate(settings.firebase_credentials))
        _db = firestore.client()
    except Exception as exc:
        print(f"[Firebase] disabled: {exc}")
    return _db

def write(collection: str, payload: dict[str, Any]) -> None:
    db = _init()
    if db is not None:
        db.collection(collection).add({
            **payload,
            "server_timestamp": datetime.now(timezone.utc).isoformat()
        })
