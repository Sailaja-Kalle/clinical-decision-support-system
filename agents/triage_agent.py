from agents.base_agent import BaseAgent

class TriageAgent(BaseAgent):
    def __init__(self):
        super().__init__("TriageAgent")

    def process(self, data):
        oxygen = data.get("oxygen", 100)
        temperature = data.get("temperature", 98)
        heart_rate = data.get("heart_rate", 80)

        is_critical = False
        reasons = []

        if oxygen < 90:
            is_critical = True
            reasons.append("Low oxygen")

        if temperature > 102:
            is_critical = True
            reasons.append("High temperature")

        if heart_rate > 110:
            is_critical = True
            reasons.append("High heart rate")

        self.log(f"Triage complete - Critical: {is_critical}")

        return {
            "is_critical": is_critical,
            "reasons": reasons
        }