from agents.base_agent import BaseAgent

class AlertAgent(BaseAgent):
    def __init__(self):
        super().__init__("AlertAgent")

    def process(self, data):
        is_critical = data.get("is_critical", False)
        risk_level = data.get("risk_level", "LOW")

        alert = False
        alert_message = ""

        if is_critical or risk_level == "HIGH":
            alert = True
            alert_message = "CRITICAL ALERT: Patient requires immediate attention!"

        self.log(f"Alert: {alert}")

        return {
            "alert": alert,
            "alert_message": alert_message
        }