def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[dict]:
    """Split text into overlapping chunks.

    Args:
        text: The text to chunk.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        A list of dicts with 'content', 'start', and 'end' keys.
    """
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_content = text[start:end]
        chunks.append(
            {
                "content": chunk_content,
                "start": start,
                "end": end,
            }
        )
        if end == len(text):
            break
        start += chunk_size - overlap

    return chunks
