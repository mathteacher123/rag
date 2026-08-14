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

## Hybrid Structural Chunking Sprint

### LlamaIndex/RAG Pipeline Tasks
- [x] Refactor `app/services/rag/chunking.py`: Phase A (MarkdownNodeParser header split) + Phase B (sentence-aware split with `.`, `?`, `\n\n` boundaries, backward scan, chunk_size=2048 chars, overlap=300 chars)
- [x] Update `app/services/rag/__init__.py` exports for new `chunk_text` signature

### Pytest Tasks
- [x] Update `tests/rag/conftest.py` with markdown fixtures (headers, nested sections, long paragraphs, mixed punctuation)
- [x] Rewrite `tests/rag/test_pipeline.py` tests: Phase A header splitting, Phase B sentence-aware splitting, overlap at sentence boundaries

### Quality Assurance
- [x] Run `ruff check . && ruff format .`
- [x] Run `pytest`

## Test Chunking Endpoint Sprint

### Backend/FastAPI Tasks
- [x] Create `app/main.py` with FastAPI app instance and include API router
- [x] Create `app/api/__init__.py` package init
- [x] Create `app/api/v1/__init__.py` package init
- [x] Create `app/api/v1/endpoints/test.py` with POST /test/chunking endpoint (takes URL, calls fetch_and_convert_to_markdown + chunk_text, returns JSON)
- [x] Create `app/api/v1/router.py` to include test endpoint
- [x] Create `app/api/router.py` to include v1 router

### Pytest Tasks
- [x] Create `tests/api/conftest.py` with FastAPI TestClient fixture
- [x] Create `tests/api/test_test_endpoint.py` with unit tests (mocked scraping/chunking)

### Quality Assurance
- [x] Run `ruff check . && ruff format .`
- [x] Run `pytest`