import json
import os

def load_interactions():
    path = os.path.join(os.path.dirname(__file__), "interactions.json")
    with open(path) as f:
        return json.load(f)

def check_medications(medications):
    interactions = load_interactions()
    warnings = []

    for med in medications:
        if med in interactions:
            for conflict in interactions[med]:
                if conflict in medications:
                    warnings.append(f"{med} + {conflict} = DANGEROUS")

    return {
        "interaction_warning": len(warnings) > 0,
        "warnings": warnings
    }