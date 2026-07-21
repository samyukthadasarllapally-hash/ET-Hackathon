from fastapi import APIRouter

router = APIRouter()

def get_advisory(aqi: int):
    if aqi <= 50:
        return {"level": "Good", "advice": "Air quality is good. Enjoy outdoor activities.", "mask": "Not required", "color": "green"}
    elif aqi <= 100:
        return {"level": "Satisfactory", "advice": "Sensitive groups should limit prolonged outdoor exertion.", "mask": "Optional", "color": "yellow"}
    elif aqi <= 200:
        return {"level": "Moderate", "advice": "Avoid outdoor exercise. Keep windows closed.", "mask": "Recommended", "color": "orange"}
    elif aqi <= 300:
        return {"level": "Poor", "advice": "Stay indoors. Avoid all outdoor activity.", "mask": "N95 required", "color": "red"}
    else:
        return {"level": "Hazardous", "advice": "Do not go outside. Seal windows and doors.", "mask": "N95 mandatory", "color": "maroon"}

def get_source_mix(aqi: int):
    if aqi > 200:
        return {"traffic": 0.52, "construction": 0.21, "industrial": 0.18, "waste_burning": 0.09}
    elif aqi > 100:
        return {"traffic": 0.40, "construction": 0.30, "industrial": 0.20, "waste_burning": 0.10}
    else:
        return {"traffic": 0.35, "construction": 0.25, "industrial": 0.25, "waste_burning": 0.15}

@router.get("/citizen")
def citizen_recommendations(zone_id: str = "z001", aqi: int = 182):
    advisory = get_advisory(aqi)
    return {
        "zone_id": zone_id,
        "aqi": aqi,
        "level": advisory["level"],
        "color": advisory["color"],
        "advisory": advisory["advice"],
        "mask": advisory["mask"],
        "route_suggestion": "Use Route B via Green Zone (AQI 95) instead of Route A"
    }

@router.get("/government")
def government_recommendations(zone_id: str = "z001", aqi: int = 182):
    sources = get_source_mix(aqi)
    advisory = get_advisory(aqi)
    return {
        "zone_id": zone_id,
        "priority_rank": 2,
        "aqi": aqi,
        "level": advisory["level"],
        "source_mix": sources,
        "recommended_actions": [
            "Inspect construction site C-114 for dust suppression compliance",
            "Consider temporary traffic diversion on Ring Road segment R-7",
            "Issue advisory to industrial units in zone to reduce emissions"
        ],
        "basis": f"{int(sources['traffic']*100)}% traffic + {int(sources['construction']*100)}% construction contribution"
    }
