from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, email: str, password: str, full_name: str | None):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = models.User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        plan="free",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user_token(email: str) -> str:
    return create_access_token(email)
