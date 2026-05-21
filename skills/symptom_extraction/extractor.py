import json
import os

def load_rules():
    path = os.path.join(os.path.dirname(__file__), "rules.json")
    with open(path) as f:
        return json.load(f)

def extract_conditions(symptoms):
    rules = load_rules()
    conditions = []

    for condition, keywords in rules.items():
        matches = [s for s in symptoms if s in keywords]
        if len(matches) >= 2:
            conditions.append(condition.capitalize())

    if not conditions:
        conditions.append("General Observation Required")

    return {"possible_conditions": conditions}