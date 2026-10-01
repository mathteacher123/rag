from llama_index.storage.docstore.postgres import PostgresDocumentStore
from llama_index.storage.kvstore.postgres import PostgresKVStore  # Added this import
from llama_index.vector_stores.postgres import PGVectorStore

from app.core.config import settings

# 1. Setup the Vector Store
vector_store = PGVectorStore(
    connection_string=settings.SUPABASE_DB_URL,
    async_connection_string=settings.SUPABASE_DB_URL_ASYNC,
    table_name=settings.VECTOR_STORE_TABLE,
    embed_dim=settings.EMBEDDING_DIM,
)

# 2. Build the Key-Value store manually (bypasses broken from_uri)
kvstore = PostgresKVStore(
    connection_string=settings.SUPABASE_DB_URL,
    async_connection_string=settings.SUPABASE_DB_URL_ASYNC,
    table_name=settings.DOCSTORE_TABLE,
)

# 3. Inject the kvstore directly into the Document Store
docstore = PostgresDocumentStore(postgres_kvstore=kvstore)
