def test_vector_store_singleton():
    from app.services.rag.vector_store import vector_store

    assert vector_store is not None


def test_vector_store_is_pg_vector_store():
    from llama_index.vector_stores.postgres import PGVectorStore

    from app.services.rag.vector_store import vector_store

    assert isinstance(vector_store, PGVectorStore)
