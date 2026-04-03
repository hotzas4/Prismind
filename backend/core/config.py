from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://prismind:prismind@localhost:5432/prismind"
    SECRET_KEY: str = "changeme-in-production-use-strong-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    OPENAI_API_KEY: Optional[str] = None

    model_config = {"env_file": ".env"}


settings = Settings()
