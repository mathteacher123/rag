import re

from llama_index.core import Document
from llama_index.core.node_parser import MarkdownNodeParser

SENTENCE_DELIMITERS = re.compile(r"(?<=[.?])\s+|\n\n")


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on `.`, `?`, or `\n\n` boundaries."""
    if not text:
        return []
    parts = SENTENCE_DELIMITERS.split(text)
    return [p for p in parts if p.strip()]


def _find_boundary_backward(text: str, max_chars: int) -> int:
    """Scan backward from max_chars to find the nearest sentence boundary."""
    if max_chars >= len(text):
        return len(text)

    search_region = text[:max_chars]

    last_period = search_region.rfind(". ")
    last_question = search_region.rfind("? ")
    last_newline = search_region.rfind("\n\n")

    boundaries = [b for b in [last_period, last_question, last_newline] if b >= 0]

    if not boundaries:
        return max_chars

    return max(boundaries) + 2


def _refine_long_section(
    section_text: str,
    header: str,
    chunk_size: int,
    overlap: int,
) -> list[dict]:
    """Phase B: Sentence-aware split for sections exceeding chunk_size."""
    if len(section_text) <= chunk_size:
        return [
            {
                "content": section_text,
                "header": header,
                "start_char": 0,
                "end_char": len(section_text),
            }
        ]

    chunks = []
    start = 0

    while start < len(section_text):
        end = _find_boundary_backward(section_text, start + chunk_size)

        chunk_content = section_text[start:end]
        chunks.append(
            {
                "content": chunk_content,
                "header": header,
                "start_char": start,
                "end_char": end,
            }
        )

        if end == len(section_text):
            break

        overlap_start = max(0, end - overlap)
        start = _find_boundary_backward(section_text, overlap_start)

        if start >= end:
            start = end

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 2048,
    overlap: int = 300,
) -> list[dict]:
    """Split markdown into chunks using hybrid structural split.

    Phase A: Split by Markdown headers (#, ##, ###) using MarkdownNodeParser.
    Phase B: For sections exceeding chunk_size, split at sentence boundaries.

    Args:
        text: Markdown content to chunk.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        A list of dicts with 'content', 'header', 'start_char', and 'end_char' keys.
    """
    if not text or not text.strip():
        return []

    doc = Document(text=text)
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents([doc])

    all_chunks = []
    for node in nodes:
        section_text = node.text
        header = _extract_header(section_text)
        body = _strip_header(section_text)

        chunks = _refine_long_section(body, header, chunk_size, overlap)
        all_chunks.extend(chunks)

    return all_chunks


def _extract_header(text: str) -> str:
    """Extract the markdown header line from a section."""
    first_line = text.split("\n", 1)[0]
    if first_line.startswith("#"):
        return first_line
    return ""


def _strip_header(text: str) -> str:
    """Remove the header line, returning only the body."""
    if text.startswith("#"):
        parts = text.split("\n", 1)
        if len(parts) > 1:
            return parts[1].strip()
    return text
