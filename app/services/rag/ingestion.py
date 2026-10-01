from llama_index.core import Document
from llama_index.core.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter

from app.services.rag.embedding import embed_model
from app.services.rag.scraping import fetch_url
from app.services.rag.url_utils import make_doc_id
from app.services.rag.vector_store import docstore, vector_store

pipeline = IngestionPipeline(
    transformations=[
        MarkdownNodeParser(),
        SentenceSplitter(chunk_size=1024, chunk_overlap=100),
        embed_model,
    ],
    docstore=docstore,
    vector_store=vector_store,
    docstore_strategy=DocstoreStrategy.UPSERTS,
)


def ingest_url(url: str) -> dict:
    result = fetch_url(url)
    text = result["text"]
    if not text:
        return {"url": url, "status": "failed_to_fetch"}

    metadata = result["metadata"]
    doc_id = make_doc_id(url, metadata.get("canonical_url"))

    document = Document(
        doc_id=doc_id,
        text=text,
        metadata={
            "source_uri": url,
            "source_type": "url",
        }
        | metadata,
        excluded_llm_metadata_keys=["source_uri", "source_type", "canonical_url"],
        excluded_embed_metadata_keys=["source_uri", "source_type", "canonical_url"],
    )

    nodes = pipeline.run(documents=[document])

    return {"url": url, "chunk_count": len(nodes), "status": "success"}


def delete_url(url: str) -> dict:
    result = fetch_url(url)
    text = result["text"]
    if not text:
        return {"url": url, "status": "failed_to_fetch"}

    metadata = result["metadata"]
    doc_id = make_doc_id(url, metadata.get("canonical_url"))
    vector_store.delete(ref_doc_id=doc_id)
    docstore.delete_ref_doc(doc_id, raise_error=False)
    return {"url": url, "status": "deleted"}
