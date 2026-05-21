from tools.groq_client import ask_groq

def generate_summary(data):
    name = data.get("name", "Unknown")
    age = data.get("age", "N/A")
    oxygen = data.get("oxygen", "N/A")
    temperature = data.get("temperature", "N/A")
    heart_rate = data.get("heart_rate", "N/A")
    risk_level = data.get("risk_level", "N/A")
    conditions = data.get("possible_conditions", [])

    prompt = f"""
Patient Information:
- Name: {name}
- Age: {age}
- Oxygen: {oxygen}%
- Temperature: {temperature}F
- Heart Rate: {heart_rate}
- Risk Level: {risk_level}
- Possible Conditions: {', '.join(conditions)}

Generate a short 2-3 sentence clinical summary for the doctor.
"""

    try:
        summary = ask_groq(prompt)
    except Exception as e:
        summary = f"Patient {name} assessed. Risk Level: {risk_level}. Conditions: {', '.join(conditions)}."

    return {"summary": summary}