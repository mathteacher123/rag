import json
import os
from pathlib import Path

# 🔄 Swapped out google_genai for openai wrappers
from langchain_openai import ChatOpenAI
from llama_index.core import Document
from llama_index.core.node_parser import TokenTextSplitter
from ragas.testset import TestsetGenerator

from app.core.config import settings
from app.services.rag.scraping import fetch_url
from app.services.rag.vector_store import docstore

from google.genai import types
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DATASET_PATH = Path("evals/dataset.jsonl")

def load_documents() -> list[Document]:
    """Load ingested documents, falling back to refetching seed URLs."""
    documents = list(docstore.docs.values())
    if documents:
        return documents

    for url in settings.EVAL_SEED_URLS:
        result = fetch_url(url)
        text = result.get("text", "")
        if not text:
            continue
        metadata = result.get("metadata") or {}
        documents.append(
            Document(
                text=text,
                metadata={"source_uri": url} | metadata,
            )
        )
    return documents


def main() -> None:
    raw_documents = load_documents()
    if not raw_documents:
        raise RuntimeError(
            "No documents available. Ingest URLs or set EVAL_SEED_URLS."
        )

    # 💡 1. Chunk documents reliably using LlamaIndex BEFORE passing to Ragas
    splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=64)
    nodes = splitter.get_nodes_from_documents(raw_documents)
    
    # Convert LlamaIndex text nodes back into Document formats expected by Ragas
    chunked_documents = [
        Document(text=node.get_content(), metadata=node.metadata) 
        for node in nodes
    ]

    # 🔄 Check for the FreeLLMAPI Unified Token instead of Gemini key
    api_key = os.environ.get("FREELLMAPI_API_KEY")
    if not api_key:
        raise ValueError("FREELLMAPI_API_KEY environment variable is missing.")

    # 🔄 Point the base URL to your local Docker FreeLLMAPI proxy node
    # Using 'auto:intelligence' profile lets FreeLLMAPI swap providers to dodge rate blocks
    evaluator_llm = ChatOpenAI(
        model="auto:intelligence",
        openai_api_key=api_key,
        openai_api_base="http://localhost:3001/v1",
        temperature=0.3,
    )

    evaluator_embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", # Ensure the base model string is exact
        api_key=settings.GEMINI_API_KEY,
        # Map your production dimension rules here
        output_dimensionality=settings.EMBEDDING_DIM 
    )

    generator = TestsetGenerator.from_langchain(
        llm=evaluator_llm,
        embedding_model=evaluator_embeddings,
    )

    # 💡 2. Generate testset natively using our robust, pre-split chunks
    testset = generator.generate_with_llamaindex_docs(
        documents=chunked_documents,
        testset_size=settings.EVAL_TESTSET_SIZE,
    )

    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATASET_PATH.open("w", encoding="utf-8") as handle:
        for sample in testset.to_list():
            handle.write(
                json.dumps(
                    {
                        "question": sample.get("user_input"),
                        "ground_truth": sample.get("reference"),
                        "scenario": sample.get("synthesizer_name"),
                    }
                )
                + "\n"
            )

    print(f"Wrote {len(testset.to_list())} samples to {DATASET_PATH}")


if __name__ == "__main__":
    main()
