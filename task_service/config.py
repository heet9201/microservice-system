from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "this-is-very-secret-key"
    ALGORITHM: str = "HS256"
    
    # Security Configuration
    ENABLE_RATE_LIMIT: bool = True
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60
    
    # Service Configuration
    TASK_SERVICE_PORT: int = 8001
    AUTH_SERVICE_URL: str = "http://localhost:8000"
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8002"
    
    class Config:
        env_file = ".env"


settings = Settings()
