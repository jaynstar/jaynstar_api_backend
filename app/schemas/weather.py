from pydantic import BaseModel

class WeatherRequest(BaseModel):
    latitude: float
    longitude: float

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature_c: float
    description: str
