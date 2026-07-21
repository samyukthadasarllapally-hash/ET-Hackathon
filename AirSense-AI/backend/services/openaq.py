import os
import requests

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

def fetch_aqi(city: str = "Delhi"):
    if not OPENAQ_API_KEY:
        # Return mock data if no API key
        return {
            "city": city,
            "aqi": 182,
            "category": "Poor",
            "pm25": 118.4,
            "pm10": 176.2,
            "no2": 42.1,
            "so2": 12.3,
            "co": 1.8,
            "source": "mock_data"
        }

    headers = {"X-API-Key": OPENAQ_API_KEY}
    url = f"https://api.openaq.org/v3/locations?city={city}&limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data.get("results"):
        return {"city": city, "aqi": 0, "error": "No data found"}

    location = data["results"][0]
    return {
        "city": city,
        "location": location.get("name"),
        "aqi": location.get("parameters", [{}])[0].get("lastValue", 0),
        "source": "openaq"
    }
