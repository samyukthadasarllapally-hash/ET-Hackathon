import os
import requests
from fastapi import HTTPException

WAQI_API_KEY = os.getenv("WAQI_API_KEY")

def fetch_waqi(city: str = "Hyderabad"):
    if not WAQI_API_KEY:
        raise HTTPException(status_code=503, detail="WAQI_API_KEY not set in .env")

    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("status") != "ok":
        raise HTTPException(status_code=502, detail=f"WAQI error: {data.get('data', 'Unknown error')}")

    d = data["data"]
    iaqi = d.get("iaqi", {})

    return {
        "city": city,
        "aqi": int(d["aqi"]),
        "category": get_category(int(d["aqi"])),
        "pm25": iaqi.get("pm25", {}).get("v", 0),
        "pm10": iaqi.get("pm10", {}).get("v", 0),
        "no2":  iaqi.get("no2",  {}).get("v", 0),
        "so2":  iaqi.get("so2",  {}).get("v", 0),
        "co":   iaqi.get("co",   {}).get("v", 0),
        "o3":   iaqi.get("o3",   {}).get("v", 0),
        "source": "waqi"
    }

def get_category(aqi: int) -> str:
    if aqi <= 50:  return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Hazardous"
