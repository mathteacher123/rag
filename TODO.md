## Web Scraping & Chunking Sprint

### LlamaIndex/RAG Pipeline Tasks
- [ ] Create `pyproject.toml` with dependencies (trafilatura, markdownify, requests, pytest, ruff)
- [ ] Create directory structure: `app/`, `app/services/rag/`, `tests/`, `tests/rag/`
- [ ] Implement `app/services/rag/scraping.py` with `fetch_and_convert_to_markdown(url: str) -> str`
- [ ] Implement `app/services/rag/chunking.py` with `chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[dict]`
- [ ] Create `app/services/rag/__init__.py` for module exports

### Pytest Tasks
- [ ] Create `tests/rag/conftest.py` with test fixtures (sample HTML, mock responses)
- [ ] Implement `tests/rag/test_pipeline.py` with unit tests for scraping function
- [ ] Implement `tests/rag/test_pipeline.py` with unit tests for chunking function
- [ ] Add integration test with real URL (optional, marks as integration)

### Quality Assurance
- [ ] Run `ruff check . && ruff format .` to ensure code quality
- [ ] Run `pytest` to verify all tests pass