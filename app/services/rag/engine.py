from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

from app.core.config import settings
from app.services.rag.embedding import embed_model
from app.services.rag.llm import llm
from app.services.rag.vector_store import vector_store

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model,
)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=settings.RETRIEVAL_TOP_K,
    vector_store_similarity_cutoff=settings.RETRIEVAL_SIMILARITY_CUTOFF,
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    llm=llm,
)
