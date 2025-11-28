from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

async def generate_resume_and_cover(user_summary: str, job_description: str, role_title: str, tone: str):
    if not client:
        resume = f"[DEV RESUME] {role_title}\n{user_summary}\n{job_description}"
        cover = f"[DEV COVER LETTER] Tone: {tone}"
        return resume, cover
    prompt = (
        f"You are an Australian resume writer. Role: {role_title}. Tone: {tone}.\n"
        f"User summary:\n{user_summary}\nJob description:\n{job_description}\n"
        "Write resume then '---COVER_LETTER---' then cover letter."
    )
    rs = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.7,
    )
    text = rs.choices[0].message.content or ""
    parts = text.split("---COVER_LETTER---")
    resume = parts[0].strip()
    cover = parts[1].strip() if len(parts) > 1 else ""
    return resume, cover
