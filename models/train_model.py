import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from models.preprocessing import load_data, preprocess, scale_features

def train():
    data_path = os.path.join(os.path.dirname(__file__), "datasets", "patient_data.csv")
    df = load_data(data_path)
    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    model_path = os.path.join(os.path.dirname(__file__), "saved_models", "risk_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("Model saved successfully!")
    return model, accuracy

if __name__ == "__main__":
    train()