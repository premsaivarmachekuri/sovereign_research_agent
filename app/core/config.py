from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    tavily_api_key: str
    llm_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3:8b" # updated to llama3:8b as per planning
    tavily_max_results: int = 10
    pdf_max_chars: int = 15_000
    pdf_max_count: int = 5
    news_letter_max_tokens: int = 2000
    log_level: str = "INFO"
    environment: str = "development"

    class Config:
        case_sensitive = False
        env_file = ".env"
        # env_file_encoding = "utf-8" # standard default anyway

@lru_cache
def get_settings() -> Settings:
    return Settings()
