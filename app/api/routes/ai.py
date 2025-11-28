from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ai import (
    TextGenerateRequest, TextGenerateResponse,
    ImageGenerateRequest, ImageGenerateResponse,
    VoiceRequest, VoiceResponse,
)
from app.services.ai_service import (
    generate_text, generate_images, generate_voice_audio,
)
from app.services.usage_service import check_and_increment_usage
from app.api.deps import get_db, get_current_user
from app.db.models import User

router = APIRouter()

@router.post("/text", response_model=TextGenerateResponse)
async def ai_text(
    req: TextGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_and_increment_usage(db, current_user, "text")
    is_premium = (current_user.plan == "premium")
    txt = await generate_text(req.prompt, req.max_tokens, req.temperature, is_premium)
    return TextGenerateResponse(text=txt)

@router.post("/image", response_model=ImageGenerateResponse)
async def ai_image(
    req: ImageGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_and_increment_usage(db, current_user, "image")
    is_premium = (current_user.plan == "premium")
    urls = await generate_images(req.prompt, req.size, req.n, is_premium)
    return ImageGenerateResponse(urls=urls)

@router.post("/voice", response_model=VoiceResponse)
async def ai_voice(
    req: VoiceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_and_increment_usage(db, current_user, "voice")
    is_premium = (current_user.plan == "premium")
    audio_url, provider = await generate_voice_audio(
        req.text, req.voice_preset, req.speed, is_premium
    )
    return VoiceResponse(audio_url=audio_url, provider=provider, voice_preset=req.voice_preset)
