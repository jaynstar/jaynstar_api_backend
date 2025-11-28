from pydantic import BaseModel
from typing import List

class TextGenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7

class TextGenerateResponse(BaseModel):
    text: str

class ImageGenerateRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    n: int = 1

class ImageGenerateResponse(BaseModel):
    urls: List[str]

class VoiceRequest(BaseModel):
    text: str
    voice_preset: str = "female_soft"
    speed: float = 1.0

class VoiceResponse(BaseModel):
    audio_url: str
    provider: str
    voice_preset: str
