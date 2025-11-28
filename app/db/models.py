from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    plan = Column(String(50), default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resumes = relationship("Resume", back_populates="owner")
    usages = relationship("AiUsage", back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=False)
    cover_letter_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="resumes")

class AiUsage(Base):
    __tablename__ = "ai_usage"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    count = Column(Integer, default=0)
    user = relationship("User", back_populates="usages")
