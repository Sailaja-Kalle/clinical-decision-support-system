def check_critical_alerts(data):
    alerts = []

    if data.get("oxygen") and data["oxygen"] < 85:
        alerts.append("CRITICAL: Oxygen below 85%")

    if data.get("temperature") and data["temperature"] > 104:
        alerts.append("CRITICAL: Temperature above 104F")

    if data.get("heart_rate") and data["heart_rate"] > 130:
        alerts.append("CRITICAL: Heart rate above 130")

    if alerts:
        print("[AlertHook] CRITICAL ALERTS DETECTED:")
        for a in alerts:
            print(f"  - {a}")

    return {
        "critical_alerts": alerts,
        "has_critical_alerts": len(alerts) > 0
    }