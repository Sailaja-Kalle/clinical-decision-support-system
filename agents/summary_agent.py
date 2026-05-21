from agents.base_agent import BaseAgent
from tools.groq_client import ask_groq

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummaryAgent")

    def process(self, data):
        name = data.get("name", "Unknown")
        risk_level = data.get("risk_level", "LOW")
        conditions = data.get("possible_conditions", [])

        prompt = f"""
Patient: {name}, Age: {data.get('age')}, Oxygen: {data.get('oxygen')}%, 
Temperature: {data.get('temperature')}F, Risk: {risk_level}, 
Conditions: {', '.join(conditions)}

Write a 2 sentence clinical summary for the doctor.
"""
        try:
            summary = ask_groq(prompt)
        except Exception:
            summary = f"Patient {name} assessed. Risk Level: {risk_level}."

        self.log("Summary generated")
        return {"summary": summary}