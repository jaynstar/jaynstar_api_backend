from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import AiUsage, User

LIMITS = {
    "free": {"text": 30, "image": 10, "voice": 10, "resume": 5},
    "premium": {"text": None, "image": None, "voice": None, "resume": None},
}

def check_and_increment_usage(db: Session, user: User, feature: str):
    plan = user.plan or "free"
    limits = LIMITS.get(plan, LIMITS["free"])
    limit = limits.get(feature)
    today = date.today()
    usage = (
        db.query(AiUsage)
        .filter(AiUsage.user_id == user.id, AiUsage.feature == feature, AiUsage.date == today)
        .first()
    )
    if not usage:
        usage = AiUsage(user_id=user.id, feature=feature, date=today, count=0)
        db.add(usage)
        db.flush()
    if limit is not None and usage.count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"{feature} daily limit reached for plan '{plan}'",
        )
    usage.count += 1
    db.commit()
