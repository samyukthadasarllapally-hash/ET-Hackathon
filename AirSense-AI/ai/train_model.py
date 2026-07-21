"""
AirSense AI — AQI Prediction Model Training

Supports two modes:
  1. Real data  → place Kaggle CPCB 'city_day.csv' in data/aqi_dataset.csv
  2. Synthetic  → auto-generated if no file found

Run from project root:
    python ai/train_model.py
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

ROOT_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(ROOT_DIR, "data", "aqi_dataset.csv")
MODEL_PATH = os.path.join(ROOT_DIR, "models", "aqi_model.pkl")

# Features now include current_aqi for better prediction context
FEATURES = ["current_aqi", "pm25", "pm10", "no2", "so2", "co", "o3",
            "temperature", "humidity", "wind_speed", "pressure"]
TARGET = "next_day_aqi"

# ── Load Data ─────────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_PATH):
        print(f"Loading dataset: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)

        # Handle Kaggle CPCB format (city_day.csv)
        if "AQI" in df.columns and "next_day_aqi" not in df.columns:
            print("Detected Kaggle CPCB format — preprocessing...")
            df = preprocess_kaggle(df)
        else:
            # Fix old synthetic dataset missing columns
            df = fix_old_format(df)
        return df
    else:
        print("No dataset found — generating synthetic data...")
        df = generate_synthetic()
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print(f"Saved to {DATA_PATH}")
        return df

def preprocess_kaggle(df):
    """Convert Kaggle city_day.csv to training format."""
    df = df.rename(columns={
        "PM2.5": "pm25", "PM10": "pm10", "NO2": "no2",
        "SO2": "so2", "CO": "co", "Ozone": "o3", "AQI": "current_aqi"
    })
    # Add missing weather columns with defaults (not in CPCB dataset)
    if "temperature" not in df.columns: df["temperature"] = 28.0
    if "humidity"    not in df.columns: df["humidity"]    = 60.0
    if "wind_speed"  not in df.columns: df["wind_speed"]  = 3.0
    if "pressure"    not in df.columns: df["pressure"]    = 1010.0

    df = df.sort_values("Date") if "Date" in df.columns else df
    df["next_day_aqi"] = df["current_aqi"].shift(-1)
    df = df.dropna(subset=FEATURES + [TARGET])
    df = df[df["current_aqi"] > 0]
    return df[FEATURES + [TARGET]]

def generate_synthetic(n=10000):
    """
    Generates realistic Indian city AQI time-series data.
    next_day_aqi is strongly correlated with current_aqi + weather.
    """
    np.random.seed(42)

    # Current AQI drives next day AQI most strongly
    current_aqi = np.random.uniform(20, 450, n)

    # Pollutants derived from AQI (realistic Indian ratios)
    pm25        = current_aqi * np.random.uniform(0.4, 0.7, n)
    pm10        = pm25 * np.random.uniform(1.3, 2.2, n)
    no2         = current_aqi * np.random.uniform(0.05, 0.15, n)
    so2         = current_aqi * np.random.uniform(0.02, 0.08, n)
    co          = current_aqi * np.random.uniform(5, 20, n)
    o3          = np.random.uniform(10, 100, n)
    temperature = np.random.uniform(15, 45, n)
    humidity    = np.random.uniform(20, 95, n)
    wind_speed  = np.random.uniform(0.5, 12, n)
    pressure    = np.random.uniform(990, 1025, n)

    # next_day_aqi: strongly driven by current_aqi
    # wind disperses pollution, humidity traps it
    wind_effect     = -wind_speed * 3
    humidity_effect = (humidity - 50) * 0.3
    temp_effect     = (temperature - 25) * 0.2
    noise           = np.random.normal(0, 6, n)

    next_day_aqi = (
        current_aqi * 0.82 +
        wind_effect +
        humidity_effect +
        temp_effect +
        noise
    ).clip(10, 500)

    return pd.DataFrame({
        "current_aqi": current_aqi, "pm25": pm25, "pm10": pm10,
        "no2": no2, "so2": so2, "co": co, "o3": o3,
        "temperature": temperature, "humidity": humidity,
        "wind_speed": wind_speed, "pressure": pressure,
        "next_day_aqi": next_day_aqi
    })

def fix_old_format(df):
    """Add missing columns if old synthetic dataset is loaded."""
    if "current_aqi" not in df.columns and "aqi" in df.columns:
        df["current_aqi"] = df["aqi"]
    if "current_aqi" not in df.columns:
        df["current_aqi"] = df["pm25"] * 0.55 + df["pm10"] * 0.15
    if "pressure" not in df.columns:
        df["pressure"] = 1010.0
    if "next_day_aqi" not in df.columns:
        df["next_day_aqi"] = df["current_aqi"].shift(-1).fillna(df["current_aqi"])
    return df

# ── Train ─────────────────────────────────────────────────────────────────────
def train(df):
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(
        n_estimators=200, max_depth=15,
        min_samples_split=5, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"\nModel Performance:")
    print(f"  MAE : {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"  R²  : {r2_score(y_test, y_pred):.4f}")
    print("\nFeature Importances:")
    for feat, imp in sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1]):
        print(f"  {feat:<15} {imp:.4f}")
    return model

# ── Save ──────────────────────────────────────────────────────────────────────
def save_model(model):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"\nModel saved → {MODEL_PATH}")

if __name__ == "__main__":
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    model = train(df)
    save_model(model)
    print("\nDone. Restart backend — prediction API will use the trained model.")
