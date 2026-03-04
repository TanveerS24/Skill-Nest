from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://Tanveer:Tanveer@4321**@localhost:5432/skillnest"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # App
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # RAG
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b-instruct-q4_K_M"
    EMBED_MODEL: str = "nomic-embed-text"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Docker Execution
    DOCKER_MEMORY_LIMIT: str = "256m"
    DOCKER_CPU_LIMIT: float = 0.5
    EXECUTION_TIMEOUT: int = 2  # seconds
    MAX_CODE_SIZE: int = 50000  # bytes
    
    # Rate Limiting
    RATE_LIMIT_SUBMISSIONS: str = "10/minute"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
