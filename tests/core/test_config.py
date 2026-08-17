from app.core.config import Settings


def test_settings_loads_from_env():
    s = Settings()
    assert s.SUPABASE_DB_URL == "postgresql://test:test@localhost:5432/test"
    assert s.GEMINI_API_KEY == "test-key"
    assert s.EMBEDDING_MODEL == "gemini-embedding-001"
    assert s.EMBEDDING_DIM == 768
    assert s.COLLECTION_NAME == "rag_documents"


def test_settings_requires_env_vars(monkeypatch):
    monkeypatch.delenv("SUPABASE_DB_URL")
    try:
        Settings()
        assert False, "Should have raised ValidationError"
    except Exception as e:
        assert "SUPABASE_DB_URL" in str(e)
