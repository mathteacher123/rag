from llama_index.storage.docstore.postgres import PostgresDocumentStore
from llama_index.vector_stores.postgres import PGVectorStore

from app.core.config import settings

vector_store = PGVectorStore(
    connection_string=settings.SUPABASE_DB_URL,
    async_connection_string=settings.SUPABASE_DB_URL_ASYNC,
    table_name=settings.VECTOR_STORE_TABLE,
    embed_dim=settings.EMBEDDING_DIM,
)

docstore = PostgresDocumentStore.from_conn_string(
    conn_string=settings.SUPABASE_DB_URL,
    table_name=settings.DOCSTORE_TABLE,
)
