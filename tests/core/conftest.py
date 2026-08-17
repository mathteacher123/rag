import pytest


@pytest.fixture(autouse=True)
def _mock_settings(monkeypatch):
    monkeypatch.setenv("SUPABASE_DB_URL", "postgresql://test:test@localhost:5432/test")
    monkeypatch.setenv(
        "SUPABASE_DB_URL_ASYNC",
        "postgresql+asyncpg://test:test@localhost:5432/test",
    )
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    from app.core.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
