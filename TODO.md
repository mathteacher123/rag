## Web Scraping & Chunking Sprint

### LlamaIndex/RAG Pipeline Tasks
- [x] Create `pyproject.toml` with dependencies (trafilatura, markdownify, requests, pytest, ruff)
- [x] Create directory structure: `app/`, `app/services/rag/`, `tests/`, `tests/rag/`
- [x] Implement `app/services/rag/scraping.py` with `fetch_and_convert_to_markdown(url: str) -> str`
- [x] Implement `app/services/rag/chunking.py` with `chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[dict]`
- [x] Create `app/services/rag/__init__.py` for module exports

### Pytest Tasks
- [x] Create `tests/rag/conftest.py` with test fixtures (sample HTML, mock responses)
- [x] Implement `tests/rag/test_pipeline.py` with unit tests for scraping function
- [x] Implement `tests/rag/test_pipeline.py` with unit tests for chunking function
- [x] Add integration test with real URL (optional, marks as integration)

### Quality Assurance
- [x] Run `ruff check . && ruff format .` to ensure code quality
- [x] Run `pytest` to verify all tests pass