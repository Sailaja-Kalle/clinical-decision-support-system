from agents.base_agent import BaseAgent
from skills.symptom_extraction.extractor import extract_conditions
from tools.groq_client import ask_groq

class DiagnosisAgent(BaseAgent):
    def __init__(self):
        super().__init__("DiagnosisAgent")

    def process(self, data):
        symptoms = data.get("symptoms", [])
        result = extract_conditions(symptoms)

        prompt = f"""
Patient symptoms: {', '.join(symptoms)}
Oxygen level: {data.get('oxygen', 'N/A')}%
Temperature: {data.get('temperature', 'N/A')}F
Age: {data.get('age', 'N/A')}

Based on these symptoms, give one short recommendation in 1 sentence.
"""
        try:
            recommendation = ask_groq(prompt)
        except Exception:
            recommendation = "Please consult a doctor immediately."

        result["recommendation"] = recommendation
        self.log(f"Conditions: {result['possible_conditions']}")
        return result