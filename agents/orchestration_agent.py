from agents.triage_agent import TriageAgent
from agents.risk_agent import RiskAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.alert_agent import AlertAgent
from agents.summary_agent import SummaryAgent

class OrchestrationAgent:
    def __init__(self):
        self.triage = TriageAgent()
        self.risk = RiskAgent()
        self.diagnosis = DiagnosisAgent()
        self.alert = AlertAgent()
        self.summary = SummaryAgent()

    def process(self, data):
        print("[Orchestration] Starting full patient analysis...")

        triage_result = self.triage.process(data)
        risk_result = self.risk.process(data)
        diagnosis_result = self.diagnosis.process(data)

        combined = {**data, **triage_result, **risk_result, **diagnosis_result}

        alert_result = self.alert.process(combined)
        combined.update(alert_result)

        summary_result = self.summary.process(combined)
        combined.update(summary_result)

        print("[Orchestration] Analysis complete!")

        return {
            "risk_score": risk_result["risk_score"],
            "risk_level": risk_result["risk_level"],
            "is_critical": triage_result["is_critical"],
            "possible_conditions": diagnosis_result["possible_conditions"],
            "alert": alert_result["alert"],
            "alert_message": alert_result["alert_message"],
            "summary": summary_result["summary"]
        }