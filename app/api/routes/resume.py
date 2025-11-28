from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.resume import ResumeGenerateRequest, ResumeGenerateResponse
from app.services.resume_service import generate_resume_and_cover
from app.services.usage_service import check_and_increment_usage
from app.db.models import Resume, User

router = APIRouter()

@router.post("/generate", response_model=ResumeGenerateResponse)
async def generate(
    req: ResumeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_and_increment_usage(db, current_user, "resume")
    resume_text, cover_text = await generate_resume_and_cover(
        req.user_summary, req.job_description, req.role_title, req.tone
    )
    obj = Resume(
        user_id=current_user.id,
        title=req.role_title,
        resume_text=resume_text,
        cover_letter_text=cover_text,
    )
    db.add(obj)
    db.commit()
    return ResumeGenerateResponse(resume_text=resume_text, cover_letter_text=cover_text)
