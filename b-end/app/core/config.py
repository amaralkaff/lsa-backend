from pydantic_settings import BaseSettings, SettingsConfigDict
from decouple import config
from typing import List
import os
import json

class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Lembaga Sinergi Analitika API"
    VERSION: str = "1.0.0"
    DEBUG_MODE: bool = config("DEBUG_MODE", default=False, cast=bool)
    
    # MongoDB settings
    MONGODB_URL: str = config("MONGODB_URL")
    MONGODB_DATABASE: str = config("MONGODB_DATABASE")
    MONGODB_TEST_DB: str = config("MONGODB_TEST_DB")
    
    # JWT settings
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = json.loads(config("ALLOWED_ORIGINS"))
    
    # File upload settings
    STATIC_DIR: str = "static"
    UPLOAD_DIR: str = os.path.join("static", "uploads")
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"]
    
    # Admin settings
    ADMIN_EMAIL: str = config("ADMIN_EMAIL")
    ADMIN_USERNAME: str = config("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD")
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

# Inisialisasi settings
settings = Settings() 