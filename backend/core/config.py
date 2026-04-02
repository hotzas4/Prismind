from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://prismind:prismind@localhost:5432/prismind"
    )
    OPENAI_API_KEY: str = Field(default="")
    SECRET_KEY: str = Field(default="changeme-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    ARXIV_API_KEY: Optional[str] = Field(default=None)
    PUBMED_API_KEY: Optional[str] = Field(default=None)
    ENVIRONMENT: str = Field(default="development")


settings = Settings()
