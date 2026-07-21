from fastapi import APIRouter

router = APIRouter()

@router.get("/heatmap")
def get_heatmap(zone_id: str = "z001"):
    # TODO: Replace with real MongoDB query + GeoJSON generation
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [77.2090, 28.6139]},
                "properties": {"zone_id": "z001", "aqi": 182, "category": "Poor"}
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [77.2300, 28.6300]},
                "properties": {"zone_id": "z002", "aqi": 95, "category": "Moderate"}
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [77.1900, 28.6000]},
                "properties": {"zone_id": "z003", "aqi": 310, "category": "Hazardous"}
            }
        ]
    }
