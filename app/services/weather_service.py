import httpx

async def get_current_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
    temp = data["current"]["temperature_2m"]
    code = data["current"]["weather_code"]
    desc = "Clear" if code == 0 else "Cloudy"
    return float(temp), desc
