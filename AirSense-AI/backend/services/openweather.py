import os
import requests
from fastapi import HTTPException

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_api_key():
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="OPENWEATHER_API_KEY not set in .env")
    return key

def get_coordinates(city: str):
    url = f"{BASE_URL}/weather?q={city}&appid={get_api_key()}&units=metric"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"OpenWeather error: {response.json().get('message', 'Unknown error')}")
    data = response.json()
    return data["coord"]["lat"], data["coord"]["lon"], data

def fetch_weather(city: str = "Hyderabad"):
    get_api_key()
    lat, lon, data = get_coordinates(city)
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": round(data["main"]["temp"], 1),
        "feels_like": round(data["main"]["feels_like"], 1),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "windSpeed": round(data["wind"]["speed"], 1),
        "windDirection": data["wind"].get("deg", 0),
        "visibility": data.get("visibility", 0),
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "lat": lat,
        "lon": lon
    }

def fetch_aqi(city: str = "Hyderabad"):
    get_api_key()
    lat, lon, _ = get_coordinates(city)
    url = f"{BASE_URL}/air_pollution?lat={lat}&lon={lon}&appid={os.getenv('OPENWEATHER_API_KEY')}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"OpenWeather AQI error: {response.json().get('message', 'Unknown error')}")
    data = response.json()
    components = data["list"][0]["components"]
    aqi_index = data["list"][0]["main"]["aqi"]
    aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
    return {
        "city": city,
        "aqi": aqi_index,
        "category": aqi_labels.get(aqi_index, "Unknown"),
        "pm25": round(components.get("pm2_5", 0), 2),
        "pm10": round(components.get("pm10", 0), 2),
        "co":   round(components.get("co", 0), 2),
        "no2":  round(components.get("no2", 0), 2),
        "o3":   round(components.get("o3", 0), 2),
        "so2":  round(components.get("so2", 0), 2),
        "nh3":  round(components.get("nh3", 0), 2),
        "lat": lat,
        "lon": lon
    }
