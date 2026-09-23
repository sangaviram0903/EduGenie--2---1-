from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_version: str = "2.0.0"
    environment: str = "development"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"

    # "gemini" is the easiest setup. Set to "local" or "auto" to use
    # LaMini-Flan-T5-783M for explanations when it is installed/downloadable.
    explanation_provider: str = "gemini"
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"

    max_input_chars: int = 20000
    max_quiz_questions: int = 5
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
