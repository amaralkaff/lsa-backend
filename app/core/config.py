from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    """Application settings."""
    
    # MongoDB settings
    MONGODB_URL: str = config("MONGODB_URL", default="mongodb://localhost:27017")
    MONGODB_DATABASE: str = config("MONGODB_DATABASE", default="lsa_db")
    MONGODB_TEST_DB: str = config("MONGODB_TEST_DB", default="lsa_test_db")
    
    # JWT settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings() 