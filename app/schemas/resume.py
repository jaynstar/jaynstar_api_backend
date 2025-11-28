from pydantic import BaseModel
from typing import Optional

class ResumeGenerateRequest(BaseModel):
    user_summary: str
    job_description: str
    role_title: str
    tone: str = "professional"

class ResumeGenerateResponse(BaseModel):
    resume_text: str
    cover_letter_text: Optional[str] = None
