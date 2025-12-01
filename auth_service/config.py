from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    SECRET_KEY: str = "this-is-very-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security Configuration
    ENABLE_RATE_LIMIT: bool = True
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60
    
    # Service Configuration
    AUTH_SERVICE_PORT: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()
