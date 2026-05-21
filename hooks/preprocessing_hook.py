def preprocess_patient_data(data):
    if isinstance(data.get("temperature"), str):
        data["temperature"] = float(data["temperature"].replace("F", "").strip())

    if isinstance(data.get("oxygen"), str):
        data["oxygen"] = float(data["oxygen"].replace("%", "").strip())

    if data.get("name"):
        data["name"] = data["name"].strip().title()

    if data.get("symptoms") is None:
        data["symptoms"] = []

    return data