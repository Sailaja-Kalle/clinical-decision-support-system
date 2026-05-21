import httpx

def search_medical_guidelines(condition):
    guidelines = {
        "respiratory": "Administer oxygen therapy, monitor SpO2, chest X-ray recommended.",
        "cardiac": "ECG monitoring, troponin levels, cardiology consult required.",
        "sepsis": "Blood cultures, IV antibiotics within 1 hour, fluid resuscitation.",
        "diabetes": "Blood glucose monitoring, insulin management, endocrinology consult.",
        "general": "Vital signs monitoring, hydration, general supportive care."
    }

    condition_lower = condition.lower()
    for key in guidelines:
        if key in condition_lower:
            return {
                "condition": condition,
                "guideline": guidelines[key],
                "source": "Clinical Guidelines Database"
            }

    return {
        "condition": condition,
        "guideline": guidelines["general"],
        "source": "Clinical Guidelines Database"
    }