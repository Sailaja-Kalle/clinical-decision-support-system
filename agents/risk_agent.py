from agents.base_agent import BaseAgent
from skills.risk_scoring.scorer import get_risk

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("RiskAgent")

    def process(self, data):
        result = get_risk(data)
        self.log(f"Risk score: {result['risk_score']} - Level: {result['risk_level']}")
        return result