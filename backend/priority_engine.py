def _is_active(value) -> bool:
    """Treat JSON booleans and common numeric/string sensor flags consistently."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "active"}
    return bool(value)


def evaluate_priority(data: dict) -> tuple[str, str]:
    if _is_active(data.get("smoke")) or _is_active(data.get("intrusion")):
        return "CRITICAL", "Emergency event detected"
    if float(data.get("temperature", 0)) >= 70:
        return "HIGH", "Abnormal temperature threshold exceeded"
    if _is_active(data.get("motion")):
        return "MEDIUM", "Motion event detected"
    return "NORMAL", "Routine telemetry"
