from pydantic_settings import BaseSettings
from decouple import config
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "Lembaga Sinergi Analitika API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = config("DEBUG_MODE", default=False, cast=bool)
    
    # MongoDB settings
    MONGODB_URL: str = config("MONGODB_URL", default="mongodb://localhost:27017")
    MONGODB_DATABASE: str = config("MONGODB_DATABASE", default="lsa_db")
    MONGODB_TEST_DB: str = config("MONGODB_TEST_DB", default="lsa_test_db")
    
    # JWT settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = config("ALLOWED_ORIGINS", default="*").split(",")
    
    # File upload settings
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"]
    
    # Admin settings
    ADMIN_EMAIL: str = config("ADMIN_EMAIL", default="admin@admin.com")
    ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", default="admin123")
    
    class Config:
        case_sensitive = True

settings = Settings() 