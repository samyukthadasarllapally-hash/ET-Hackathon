import os
import pickle
import numpy as np
from fastapi import APIRouter
from services.weather import fetch_weather, fetch_openweather_aqi
from services.waqi import fetch_waqi, get_category

router = APIRouter()

# ── Load model once at startup ────────────────────────────────────────────────
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "models", "aqi_model.pkl")
)

_model = None

def get_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model

# ── Prediction ────────────────────────────────────────────────────────────────
def predict(model, current_aqi, pm25, pm10, no2, so2, co, o3, temperature, humidity, wind_speed, pressure):
    features = np.array([[current_aqi, pm25, pm10, no2, so2, co, o3, temperature, humidity, wind_speed, pressure]])
    base = float(model.predict(features)[0])
    base = max(0, min(500, base))
    return round(base, 1), round(min(500, base * 1.08), 1), round(min(500, base * 1.15), 1)

def mock_predict(current_aqi):
    return (
        round(min(500, current_aqi * 1.07), 1),
        round(min(500, current_aqi * 1.15), 1),
        round(min(500, current_aqi * 1.22), 1)
    )

# ── Route ─────────────────────────────────────────────────────────────────────
@router.get("/forecast")
def get_forecast(city: str = "Hyderabad"):
    # Fetch all data — coordinates resolved once inside fetch_weather (cached)
    weather     = fetch_weather(city)
    pollutants  = fetch_openweather_aqi(city)
    waqi_data   = fetch_waqi(city)

    current_aqi = waqi_data["aqi"]   # Real Indian AQI (0-500) from WAQI
    model       = get_model()

    if model:
        f24, f48, f72 = predict(
            model, current_aqi,
            pollutants["pm25"], pollutants["pm10"],
            pollutants["no2"],  pollutants["so2"],
            pollutants["co"],   pollutants["o3"],
            weather["temperature"], weather["humidity"],
            weather["windSpeed"],   weather["pressure"]
        )
        source = "ml_model"
    else:
        f24, f48, f72 = mock_predict(current_aqi)
        source = "mock_fallback"

    return {
        "city":       city,
        "currentAQI": current_aqi,
        "category":   get_category(current_aqi),
        "forecast24h": {"aqi": f24, "category": get_category(f24)},
        "forecast48h": {"aqi": f48, "category": get_category(f48)},
        "forecast72h": {"aqi": f72, "category": get_category(f72)},
        "source":     source,
        "inputs": {
            "pm25":        pollutants["pm25"],
            "pm10":        pollutants["pm10"],
            "temperature": weather["temperature"],
            "humidity":    weather["humidity"],
            "windSpeed":   weather["windSpeed"],
            "pressure":    weather["pressure"]
        }
    }
