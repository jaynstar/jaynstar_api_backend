from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserRead
from app.db.models import User

router = APIRouter()

@router.post("/upgrade", response_model=UserRead)
def upgrade_to_premium(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.plan = "premium"
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/downgrade", response_model=UserRead)
def downgrade_to_free(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.plan = "free"
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
