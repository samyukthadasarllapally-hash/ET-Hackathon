from fastapi import APIRouter
from services.weather import fetch_weather

router = APIRouter()

@router.get("/current")
def get_weather(city: str = "Hyderabad"):
    return fetch_weather(city)
