from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    database_url: str = "sqlite:///./data/tickets.db"
    vector_store_path: str = "./core/vectorstore/data/index"
    vector_store_type: str = "faiss"
    app_env: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()