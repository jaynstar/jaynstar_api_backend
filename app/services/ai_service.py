import os
from datetime import datetime
from typing import List, Tuple
import httpx
from openai import OpenAI
from app.core.config import settings
from app.services.ai_provider import resolve_ai_provider

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

VOICE_PRESETS = {
    "female_soft": {"label": "female_soft"},
    "male_deep": {"label": "male_deep"},
    "neutral": {"label": "neutral"},
    "robotic": {"label": "robotic"},
}

HF_TTS_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"

async def generate_text(prompt: str, max_tokens=512, temperature=0.7, is_premium=False) -> str:
    provider = resolve_ai_provider(is_premium)
    if provider == "free":
        url = "https://api.deepseek.com/v1/chat/completions"
        body = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(url, json=body)
            data = r.json()
            return data["choices"][0]["message"]["content"]
    if provider == "openai" and client:
        rs = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return rs.choices[0].message.content
    return f"[DEV MODE] {prompt}"

async def generate_images(prompt: str, size="1024x1024", n=1, is_premium=False) -> List[str]:
    provider = resolve_ai_provider(is_premium)
    if provider == "free":
        return [f"https://cdn.jaynstar.com/dev/image/{hash((prompt, i))}.png" for i in range(n)]
    if provider == "openai" and client:
        rs = client.images.generate(model="gpt-image-1", prompt=prompt, size=size, n=n)
        return [i.url for i in rs.data]
    return [f"https://cdn.jaynstar.com/dev/image/{hash((prompt, i))}.png"]

async def generate_voice_audio(text: str, voice_preset: str, speed: float, is_premium: bool) -> Tuple[str, str]:
    provider = resolve_ai_provider(is_premium)
    headers = {"Content-Type": "application/json"}
    payload = {"inputs": text, "options": {"use_gpu": False, "wait_for_model": True}}
    async with httpx.AsyncClient(timeout=60) as client_http:
        r = await client_http.post(HF_TTS_URL, json=payload, headers=headers)
        if r.status_code != 200:
            fake_id = abs(hash((text, voice_preset, speed, provider)))
            fallback_url = f"https://cdn.jaynstar.com/dev/audio/{provider}_{fake_id}.mp3"
            return fallback_url, provider
        audio_bytes = r.content
    os.makedirs("static/audio", exist_ok=True)
    filename = f"{int(datetime.now().timestamp())}_{voice_preset}.wav"
    filepath = os.path.join("static/audio", filename)
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    audio_url = f"/static/audio/{filename}"
    return audio_url, provider
