import os
import pickle
import numpy as np

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "saved_models", "risk_model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__), "saved_models", "scaler.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    return model, scaler

def predict_risk(data):
    model, scaler = load_model()

    features = np.array([[
        data.get("age", 0),
        data.get("oxygen", 100),
        data.get("temperature", 98),
        data.get("heart_rate", 80),
        1 if data.get("diabetes", False) else 0
    ]])

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {
        "ml_risk_prediction": "HIGH" if prediction == 1 else "LOW",
        "ml_risk_probability": round(float(probability) * 100, 2)
    }