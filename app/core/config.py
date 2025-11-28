from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Jaynstar API"
    API_V1_STR: str = "/v1"
    ENVIRONMENT: str = "development"
    ALLOWED_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"
    DATABASE_URL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    AI_MODE: str = "auto"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
