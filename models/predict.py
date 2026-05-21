import joblib
import numpy as np
import os

MODEL_PATH = "models/saved_models/risk_model.pkl"

def predict_risk(data):
    try:
        if not os.path.exists(MODEL_PATH):
            return {
                "ml_risk_prediction": "N/A",
                "ml_risk_probability": 0
            }

        model = joblib.load(MODEL_PATH)

        # Parse systolic BP
        bp = data.get("blood_pressure", "120/80")
        try:
            systolic = int(str(bp).split("/")[0])
        except:
            systolic = 120

        # Count symptoms
        symptoms = data.get("symptoms", [])
        symptom_count = len(symptoms) if isinstance(symptoms, list) else 0

        features = np.array([[
            data.get("age", 0),
            data.get("temperature", 98.6),
            data.get("oxygen", 100),
            data.get("heart_rate", 80),
            systolic,
            1 if data.get("diabetes", False) else 0,
            symptom_count
        ]])

        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        probability = max(probabilities)

        risk_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        risk_label = risk_map.get(int(prediction), "LOW")

        return {
            "ml_risk_prediction": risk_label,
            "ml_risk_probability": round(float(probability) * 100, 2)
        }

    except Exception as e:
        return {
            "ml_risk_prediction": "N/A",
            "ml_risk_probability": 0
        }