from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.prompts import ChatPromptTemplate
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

text_qa_template = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=settings.LLM_SYSTEM_PROMPT,
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(
                "Context information is below.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information and not prior knowledge, "
                "answer the question: {query_str}"
            ),
        ),
    ]
)

response_synthesizer = get_response_synthesizer(
    llm=llm,
    streaming=True,
    text_qa_template=text_qa_template,
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)
