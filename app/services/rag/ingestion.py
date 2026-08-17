from llama_index.core.schema import TextNode

from app.services.rag.chunking import chunk_html
from app.services.rag.embedding import embed_model
from app.services.rag.scraping import fetch_html
from app.services.rag.url_utils import normalize_url
from app.services.rag.vector_store import vector_store


def ingest_url(url: str) -> dict:
    norm_url = normalize_url(url)

    raw_html = fetch_html(norm_url)
    if not raw_html:
        return {"url": norm_url, "chunk_count": 0, "status": "failed_to_fetch"}

    chunks = chunk_html(raw_html)

    nodes = []
    for chunk in chunks:
        node = TextNode(
            text=chunk.text,
            metadata=chunk.metadata,
        )
        node.metadata["ref_doc_id"] = norm_url
        node.embedding = embed_model.get_text_embedding(chunk.text)
        nodes.append(node)

    vector_store.delete(ref_doc_id=norm_url)
    vector_store.add(nodes)

    return {"url": norm_url, "chunk_count": len(nodes), "status": "success"}
