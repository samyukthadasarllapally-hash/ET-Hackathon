import os
import time
import requests
from fastapi import HTTPException

BASE_URL = "https://api.openweathermap.org/data/2.5"

# ── Simple in-memory cache (5 min TTL) ───────────────────────────────────────
_cache = {}
CACHE_TTL = 300  # seconds

def _cached(key, fn):
    now = time.time()
    if key in _cache and now - _cache[key]["ts"] < CACHE_TTL:
        return _cache[key]["data"]
    result = fn()
    _cache[key] = {"data": result, "ts": now}
    return result

def get_api_key():
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="OPENWEATHER_API_KEY not set in .env")
    return key

def get_coordinates(city: str):
    def _fetch():
        url = f"{BASE_URL}/weather?q={city}&appid={get_api_key()}&units=metric"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"OpenWeather error: {r.json().get('message')}")
        return r.json()
    return _cached(f"coord_{city}", _fetch)

def fetch_weather(city: str = "Hyderabad"):
    data = get_coordinates(city)
    return {
        "city":        data["name"],
        "country":     data["sys"]["country"],
        "temperature": round(data["main"]["temp"], 1),
        "feels_like":  round(data["main"]["feels_like"], 1),
        "humidity":    data["main"]["humidity"],
        "pressure":    data["main"]["pressure"],
        "windSpeed":   round(data["wind"]["speed"], 1),
        "windDirection": data["wind"].get("deg", 0),
        "visibility":  data.get("visibility", 0),
        "description": data["weather"][0]["description"].title(),
        "icon":        data["weather"][0]["icon"],
        "lat":         data["coord"]["lat"],
        "lon":         data["coord"]["lon"]
    }

def fetch_openweather_aqi(city: str = "Hyderabad"):
    """Returns raw pollutant concentrations — used as ML features only."""
    coord_data = get_coordinates(city)
    lat = coord_data["coord"]["lat"]
    lon = coord_data["coord"]["lon"]

    def _fetch():
        url = f"{BASE_URL}/air_pollution?lat={lat}&lon={lon}&appid={get_api_key()}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="OpenWeather AQI error")
        return r.json()

    data = _cached(f"aqi_{city}", _fetch)
    c = data["list"][0]["components"]
    return {
        "pm25": round(c.get("pm2_5", 0), 2),
        "pm10": round(c.get("pm10",  0), 2),
        "no2":  round(c.get("no2",   0), 2),
        "so2":  round(c.get("so2",   0), 2),
        "co":   round(c.get("co",    0), 2),
        "o3":   round(c.get("o3",    0), 2),
        "lat":  lat,
        "lon":  lon
    }
