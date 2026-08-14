from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag import chunk_text, fetch_and_convert_to_markdown

router = APIRouter()


class ChunkRequest(BaseModel):
    url: str


class ChunkResponse(BaseModel):
    content: str
    header: str
    start_char: int
    end_char: int


@router.post("/test/chunking", response_model=list[ChunkResponse])
def test_chunking(request: ChunkRequest) -> list[ChunkResponse]:
    """Fetch a URL, convert to markdown, and return chunks."""
    markdown = fetch_and_convert_to_markdown(request.url)
    if not markdown:
        raise HTTPException(status_code=400, detail="Failed to fetch content from URL")

    chunks = chunk_text(markdown)
    return [
        ChunkResponse(
            content=c["content"],
            header=c["header"],
            start_char=c["start_char"],
            end_char=c["end_char"],
        )
        for c in chunks
    ]
