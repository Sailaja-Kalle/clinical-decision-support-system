import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess(df):
    df = df.dropna()
    X = df[["age", "oxygen", "temperature", "heart_rate", "diabetes"]]
    y = df["risk"]
    return X, y

def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    scaler_path = os.path.join(os.path.dirname(__file__), "saved_models", "scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    return X_train_scaled, X_test_scaled, scaler