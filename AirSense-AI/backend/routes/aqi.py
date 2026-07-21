from fastapi import APIRouter
from services.waqi import fetch_waqi

router = APIRouter()

@router.get("/current")
def get_current_aqi(city: str = "Hyderabad"):
    return fetch_waqi(city)
