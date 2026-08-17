from llama_index.vector_stores.postgres import PGVectorStore

from app.core.config import settings

vector_store = PGVectorStore(
    connection_string=settings.SUPABASE_DB_URL,
    async_connection_string=settings.SUPABASE_DB_URL_ASYNC,
    table_name=settings.COLLECTION_NAME,
    embed_dim=settings.EMBEDDING_DIM,
)
