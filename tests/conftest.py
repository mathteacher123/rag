import os

os.environ.setdefault("SUPABASE_DB_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault(
    "SUPABASE_DB_URL_ASYNC", "postgresql+asyncpg://test:test@localhost:5432/test"
)
os.environ.setdefault("GEMINI_API_KEY", "test-key")
