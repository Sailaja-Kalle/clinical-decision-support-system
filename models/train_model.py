import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

os.makedirs("models/saved_models", exist_ok=True)

# ── Enhanced Training Data ──────────────────────────────────
data = {
    "age": [
        25,30,35,40,45,50,55,60,65,70,75,80,
        22,28,33,42,48,52,58,63,68,72,78,82,
        20,27,32,38,44,49,54,59,64,69,74,79,
        26,31,36,41,46,51,56,61,66,71,76,81
    ],
    "temperature": [
        98.6,98.9,99.1,100.2,101.5,102.3,103.1,104.0,104.8,105.2,105.8,106.0,
        97.8,98.2,98.7,99.5,100.8,101.9,102.7,103.5,104.2,105.0,105.5,106.1,
        98.4,98.8,99.0,100.0,101.2,102.0,103.0,103.8,104.5,105.1,105.7,106.2,
        98.5,98.6,99.2,100.5,101.8,102.5,103.3,104.1,104.9,105.3,105.9,106.3
    ],
    "oxygen": [
        99,98,97,96,95,93,91,89,87,85,83,80,
        100,99,98,97,94,92,90,88,86,84,82,79,
        99,98,97,96,95,93,90,88,86,84,82,78,
        99,98,97,95,94,92,91,89,87,85,83,80
    ],
    "heart_rate": [
        70,72,75,85,95,105,112,120,128,135,142,150,
        68,71,74,88,98,108,115,122,130,138,145,152,
        72,74,76,86,96,106,113,121,129,136,143,151,
        69,73,77,87,97,107,114,123,131,137,144,153
    ],
    "systolic_bp": [
        115,118,120,130,140,150,158,165,172,178,182,188,
        112,116,122,132,142,152,160,167,174,180,184,190,
        114,117,121,131,141,151,159,166,173,179,183,189,
        116,119,123,133,143,153,161,168,175,181,185,191
    ],
    "diabetes": [
        0,0,0,0,1,0,1,1,0,1,1,1,
        0,0,0,1,0,1,0,1,1,0,1,1,
        0,0,0,0,1,1,0,1,1,1,0,1,
        0,0,0,1,0,0,1,1,0,1,1,1
    ],
    "symptom_count": [
        1,1,2,2,3,3,4,4,5,5,6,6,
        0,1,1,2,3,4,4,5,5,6,6,7,
        1,1,2,3,3,4,4,5,5,6,6,7,
        0,1,2,2,3,3,4,5,5,6,6,7
    ],
    "risk_label": [
        0,0,0,0,1,1,1,2,2,2,2,2,
        0,0,0,0,1,1,1,2,2,2,2,2,
        0,0,0,1,1,1,1,2,2,2,2,2,
        0,0,0,1,1,1,2,2,2,2,2,2
    ]
}

df = pd.DataFrame(data)

X = df[["age","temperature","oxygen","heart_rate","systolic_bp","diabetes","symptom_count"]]
y = df["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ── Model 1: Random Forest ──────────────────────────────────
rf_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        class_weight="balanced"
    ))
])
rf_pipeline.fit(X_train, y_train)
rf_pred = rf_pipeline.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)
print(f"✅ Random Forest Accuracy: {rf_acc:.2%}")
print(classification_report(y_test, rf_pred, target_names=["LOW","MEDIUM","HIGH"]))

# ── Model 2: Gradient Boosting ──────────────────────────────
gb_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    ))
])
gb_pipeline.fit(X_train, y_train)
gb_pred = gb_pipeline.predict(X_test)
gb_acc = accuracy_score(y_test, gb_pred)
print(f"✅ Gradient Boosting Accuracy: {gb_acc:.2%}")

# ── Save best model ─────────────────────────────────────────
best_model = rf_pipeline if rf_acc >= gb_acc else gb_pipeline
best_name = "RandomForest" if rf_acc >= gb_acc else "GradientBoosting"
print(f"\n🏆 Best Model: {best_name} ({max(rf_acc, gb_acc):.2%})")

joblib.dump(best_model, "models/saved_models/risk_model.pkl")
joblib.dump(["age","temperature","oxygen","heart_rate","systolic_bp","diabetes","symptom_count"],
            "models/saved_models/feature_names.pkl")
print("✅ Model saved to models/saved_models/risk_model.pkl")