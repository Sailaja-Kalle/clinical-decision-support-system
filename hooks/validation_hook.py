def validate_patient_data(data):
    errors = []

    if not data.get("name"):
        errors.append("name is required")

    if not data.get("age"):
        errors.append("age is required")

    if data.get("age") and data["age"] < 0:
        errors.append("age cannot be negative")

    if data.get("oxygen") and (data["oxygen"] < 0 or data["oxygen"] > 100):
        errors.append("oxygen must be between 0 and 100")

    if data.get("temperature") and data["temperature"] > 115:
        errors.append("temperature value seems invalid")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }