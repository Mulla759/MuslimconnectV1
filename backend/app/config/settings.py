"""Centralized environment-driven settings for the backend."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and `.env` files."""

    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    database_url: str = "db/database.db"
    cors_origins: list[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
