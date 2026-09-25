def evaluate_priority(data: dict) -> tuple[str, str]:
    if data.get("smoke") is True or data.get("intrusion") is True:
        return "CRITICAL", "Emergency event detected"
    if float(data.get("temperature", 0)) >= 70:
        return "HIGH", "Abnormal temperature threshold exceeded"
    if data.get("motion") is True:
        return "MEDIUM", "Motion event detected"
    return "NORMAL", "Routine telemetry"
