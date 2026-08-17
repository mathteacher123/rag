from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag import chunk_html, fetch_html

router = APIRouter()


class ChunkRequest(BaseModel):
    url: str


class ChunkResponse(BaseModel):
    content: str
    title: str | None
    heading_path: str
    content_type: str
    chunk_index: int


@router.post("/test/chunking", response_model=list[ChunkResponse])
def test_chunking(request: ChunkRequest) -> list[ChunkResponse]:
    """Fetch a URL, chunk the HTML, and return chunks with metadata."""
    raw_html = fetch_html(request.url)
    if not raw_html:
        raise HTTPException(status_code=400, detail="Failed to fetch content from URL")

    chunks = chunk_html(raw_html)
    return [
        ChunkResponse(
            content=chunk.text,
            title=chunk.metadata.get("title"),
            heading_path=chunk.metadata.get("heading_path", ""),
            content_type=chunk.metadata.get("content_type", ""),
            chunk_index=chunk.metadata.get("chunk_index", 0),
        )
        for chunk in chunks
    ]
