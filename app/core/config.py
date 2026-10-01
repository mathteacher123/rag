from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_DB_URL: str
    SUPABASE_DB_URL_ASYNC: str
    GEMINI_API_KEY: str
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    EMBEDDING_DIM: int = 768
    VECTOR_STORE_TABLE: str = "llamaindex"
    DOCSTORE_TABLE: str = "docstore"
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1024
    RETRIEVAL_TOP_K: int = 4
    RETRIEVAL_SIMILARITY_CUTOFF: float = 0.7
    LLM_SYSTEM_PROMPT: str = (
        "You are a helpful assistant. Answer based on the provided context. "
        "If the context is insufficient, say you don't know. "
        "Be concise and accurate."
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
