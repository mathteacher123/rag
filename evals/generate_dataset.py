import json
import os
from pathlib import Path

from llama_index.core.schema import MetadataMode
from llama_index.core import Document
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from ragas.testset import TestsetGenerator
from ragas.testset.transforms.default import default_transforms_for_prechunked

from app.core.config import settings
from app.services.rag.scraping import fetch_url
from app.services.rag.embedding import embed_model
from app.services.rag.llm import llm
from app.services.rag.url_utils import make_doc_id

from google.genai import types
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_core.documents import Document as LangChainDocument

DATASET_PATH = Path("evals/dataset.jsonl")

def load_documents() -> list[Document]:
    """Load ingested document from seed URLs."""
    documents = []
    for url in settings.EVAL_SEED_URLS:
        result = fetch_url(url)
        text = result.get("text", "")
        if not text:
            raise ValueError(f"Failed to fetch content or text is empty for URL: {url}")
        metadata = result.get("metadata") or {}
        documents.append(
            Document(
                text=text,
                metadata={
                    "source_uri": url,
                    "source_type": "url",
                    "filename": make_doc_id(url, metadata.get("canonical_url"))
                }
                | metadata,
                excluded_llm_metadata_keys=["source_uri", "source_type", "canonical_url"],
                excluded_embed_metadata_keys=["source_uri", "source_type", "canonical_url"],
            )
        )
    return documents

def transform_documents(
    raw_documents: list[Document], 
    chunk_size: int = 1024, 
    chunk_overlap: int = 100
) -> list[Document]:
    """Parses documents with Markdown structural rules and splits them into uniform chunks."""
    # 1. Instantiate the isolated transformation components
    markdown_parser = MarkdownNodeParser()
    sentence_splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # 2. Sequentially apply the transformations in-memory
    markdown_nodes = markdown_parser.get_nodes_from_documents(raw_documents)
    final_nodes = sentence_splitter.get_nodes_from_documents(markdown_nodes)

    # 3. Re-wrap into Document objects matching downstream requirements (like Ragas)
    return [
        Document(text=node.get_content(), metadata=node.metadata) 
        for node in final_nodes
    ]

def main() -> None:
    raw_documents = load_documents()
    if not raw_documents:
        raise RuntimeError(
            "No documents available. Ingest URLs or set EVAL_SEED_URLS."
        )

    # Get your transformed chunks instantly
    chunked_documents = transform_documents(raw_documents, chunk_size=1024, chunk_overlap=100)
    
    langchain_docs = [
        LangChainDocument(
            page_content=node.text,
            metadata=node.metadata
        )
        for node in chunked_documents
    ]
    """
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
    """
    evaluator_llm = llm
    evaluator_embeddings = embed_model

    generator = TestsetGenerator.from_llama_index(
        llm=evaluator_llm,
        embedding_model=evaluator_embeddings,
    )

    # Generate testset natively using our robust, pre-split chunks
    testset = generator.generate_with_chunks(
        chunks=langchain_docs,
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
