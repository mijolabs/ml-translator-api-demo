from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


APP_ROOT: Path = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ML Translator API Demo"
    app_version: str = "0.1.0"
    translation_models: list[str] = ["Helsinki-NLP/opus-mt-ru-en", "Helsinki-NLP/opus-mt-en-ru"]
    log_level: str = "INFO"
