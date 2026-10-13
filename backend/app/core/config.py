from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    app_name: str = "AI Career Agent API"

    app_env: str = "development"

    api_v1_prefix: str = "/api/v1"

    frontend_url: str = "http://localhost:4200"

    database_url: str


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    gemini_api_key: str | None = None

    embedding_model: str = "gemini-embedding-2"

    groq_api_key: str | None = None

    groq_model: str = "qwen-3.8-27b"

    gemini_llm_model: str = "gemini-3.8-flash"    


@lru_cache
def get_settings() -> Settings:

    return Settings()


settings = get_settings()