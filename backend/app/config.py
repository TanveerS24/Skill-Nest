from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://skillnest:skillnest123@postgres:5432/skillnest"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Service
    AI_API_KEY: str = ""
    AI_API_URL: str = "https://api.openai.com/v1/chat/completions"
    
    # Rate Limiting
    RATE_LIMIT_SUBMISSIONS: int = 30  # per minute
    
    # Execution Limits
    DEFAULT_TIME_LIMIT: int = 5  # seconds
    DEFAULT_MEMORY_LIMIT: int = 256  # MB
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
