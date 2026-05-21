import json
import os

def load_thresholds():
    path = os.path.join(os.path.dirname(__file__), "thresholds.json")
    with open(path) as f:
        return json.load(f)

def calculate_risk_score(data):
    t = load_thresholds()
    score = 0

    if data.get("age", 0) > t["age_threshold"]:
        score += t["age_score"]

    if data.get("oxygen", 100) < t["oxygen_threshold"]:
        score += t["oxygen_score"]

    if data.get("temperature", 98) > t["temperature_threshold"]:
        score += t["temperature_score"]

    if data.get("heart_rate", 80) > t["heart_rate_threshold"]:
        score += t["heart_rate_score"]

    if "chest pain" in data.get("symptoms", []):
        score += t["chest_pain_score"]

    if score >= t["high_risk_threshold"]:
        level = "HIGH"
    elif score >= t["medium_risk_threshold"]:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {"risk_score": score, "risk_level": level}