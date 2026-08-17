from pydantic import ValidationError

from app.core.config import Settings


def test_settings_loads_from_env():
    s = Settings()
    assert s.SUPABASE_DB_URL == "postgresql://test:test@localhost:5432/test"
    assert (
        s.SUPABASE_DB_URL_ASYNC == "postgresql+asyncpg://test:test@localhost:5432/test"
    )
    assert s.GEMINI_API_KEY == "test-key"
    assert s.EMBEDDING_MODEL == "gemini-embedding-001"
    assert s.EMBEDDING_DIM == 768
    assert s.COLLECTION_NAME == "rag_documents"


def test_settings_requires_env_vars(monkeypatch):
    monkeypatch.delenv("SUPABASE_DB_URL", raising=False)
    monkeypatch.delenv("SUPABASE_DB_URL_ASYNC", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    try:
        Settings(_env_file=None)
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "SUPABASE_DB_URL" in str(e)
