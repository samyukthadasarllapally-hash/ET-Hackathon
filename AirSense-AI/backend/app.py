from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# .env is one level above the backend/ folder
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from routes import aqi, weather, prediction, chatbot, recommendations

app = FastAPI(title="AirSense AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aqi.router,             prefix="/api/aqi",             tags=["AQI"])
app.include_router(weather.router,         prefix="/api/weather",         tags=["Weather"])
app.include_router(prediction.router,      prefix="/api/prediction",      tags=["Prediction"])
app.include_router(chatbot.router,         prefix="/api/chat",            tags=["Chatbot"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])

@app.get("/")
def root():
    return {"message": "AirSense AI Backend is running", "docs": "/docs"}
