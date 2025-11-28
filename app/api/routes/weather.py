from fastapi import APIRouter
from app.schemas.weather import WeatherRequest, WeatherResponse
from app.services.weather_service import get_current_weather

router = APIRouter()

@router.post("/current", response_model=WeatherResponse)
async def current(req: WeatherRequest):
    temp, desc = await get_current_weather(req.latitude, req.longitude)
    return WeatherResponse(
        latitude=req.latitude,
        longitude=req.longitude,
        temperature_c=temp,
        description=desc,
    )
