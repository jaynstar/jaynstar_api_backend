from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.services import auth_service
from app.db import models

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(u: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, u.email, u.password, u.full_name)

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    tok = auth_service.create_user_token(user.email)
    return Token(access_token=tok)

@router.get("/me", response_model=UserRead)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
