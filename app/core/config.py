from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    tavily_api_key: str
    tavily_max_results: int = 10
    pdf_max_chars: int = 15_000
    pdf_max_count: int = 5
    news_letter_max_tokens: int = 2000
    log_level: str = "INFO"
    environment: str = "development"


    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()