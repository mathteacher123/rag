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

## HTML Chunking Sprint

### How `chunk_html` works (from `_llm/html-chunk.py`)
5-step pipeline:
1. Title extraction — parses `<title>` tag via BeautifulSoup
2. Structural parsing — `HTMLNodeParser` splits DOM into nodes by tag (`h1-h6`, `p`, `li`, `table`, `blockquote`). Consecutive `<li>` elements bundle into one node.
3. Heading hierarchy — walks nodes, maintains breadcrumb path. Headings become metadata only, not chunks.
4. Content-aware splitting — tables, blockquotes, lists stay unsplit. Prose split via `SentenceSplitter` (`chunk_size=600`, `chunk_overlap=75`).
5. Metadata enrichment — every chunk gets `title`, `heading_path`, `content_type`, `chunk_index`.
Returns `list[Document]`.

### Dependencies
- [x] Add `"beautifulsoup4"` to `pyproject.toml` dependencies

### LlamaIndex/RAG Pipeline Tasks
- [x] Replace `app/services/rag/chunking.py`: delete `chunk_text` and all Markdown logic, move `chunk_html` from `_llm/html-chunk.py` with imports (`BeautifulSoup`, `Document`, `HTMLNodeParser`, `SentenceSplitter`)
- [x] Update `app/services/rag/__init__.py`: export `chunk_html` instead of `chunk_text`
- [x] Update `app/services/rag/scraping.py`: remove `markdownify` import, rename `fetch_and_convert_to_markdown` to `fetch_html`, return raw HTML directly from `trafilatura.extract()`

### Backend/FastAPI Tasks
- [x] Update `app/api/v1/endpoints/test.py`: replace `ChunkResponse` model with `{content, title, heading_path, content_type, chunk_index}`, call `chunk_html(raw_html)`, map `Document` objects to response

### Pytest Tasks
- [x] Rewrite `tests/rag/conftest.py`: replace markdown fixtures with HTML fixtures (headings, tables, lists, blockquotes)
- [x] Rewrite `tests/rag/test_pipeline.py`: delete Markdown test classes, add HTML chunking tests (`test_returns_list_of_documents`, `test_heading_metadata`, `test_content_type_detection`, `test_chunk_index_sequential`, `test_empty_html_returns_empty`, `test_title_extracted`, `test_long_prose_is_split`, `test_table_stays_intact`, `test_list_stays_intact`)
- [x] Rewrite `tests/api/test_test_endpoint.py`: update `SAMPLE_CHUNKS` to new shape, mock `chunk_html` instead of `chunk_text`, assert new response fields

### Quality Assurance
- [x] Run `ruff check . && ruff format .`
- [x] Run `pytest`

## Supabase Embedding Storage Sprint

### Dependencies
- [ ] Add `llama-index-vector-stores-postgres`, `llama-index-embeddings-google-genai`, `python-dotenv`, `psycopg2-binary` to `pyproject.toml` dependencies

### Configuration Layer
- [ ] Create `app/core/__init__.py` (empty package init)
- [ ] Create `app/core/config.py`: Pydantic Settings with `SUPABASE_DB_URL`, `GEMINI_API_KEY`, model defaults
- [ ] Create `.env.example`: template with required env vars (placeholder values)

### LlamaIndex/RAG Pipeline Tasks
- [ ] Create `app/services/rag/embedding.py`: initialize `GoogleGenAIEmbedding(model_name="gemini-embedding-001")` from settings, export singleton
- [ ] Create `app/services/rag/url_utils.py`: `normalize_url(url)` — force https, lowercase domain, strip trailing slash, strip query string + fragment
- [ ] Create `app/services/rag/vector_store.py`: `PGVectorStore.from_params()` with `embed_dim=768`, no `hnsw_kwargs`, export singleton
- [ ] Create `app/services/rag/ingestion.py`: `ingest_url(url)` — normalize url, fetch_html, chunk_html, attach url metadata to each chunk, delete old by ref_doc_id, insert new via vector_store
- [ ] Update `app/services/rag/__init__.py`: export `embed_model`, `vector_store`, `ingest_url`, `normalize_url`

### Pytest Tasks
- [ ] Create `tests/core/__init__.py` (empty package init)
- [ ] Create `tests/core/conftest.py`: mock settings fixture
- [ ] Create `tests/core/test_config.py`: test settings load from env, defaults, validation
- [ ] Create `tests/rag/test_url_utils.py`: test normalize_url strips query string, fragment, trailing slash, lowercases domain
- [ ] Create `tests/rag/test_ingestion.py`: mock fetch_html, chunk_html, vector_store; test full pipeline; test upsert deletes old before insert
- [ ] Create `tests/rag/test_vector_store.py`: mock PGVectorStore; test upsert_by_url deletes then adds; test normalize_url integrated

### Quality Assurance
- [ ] Run `ruff check . && ruff format .`
- [ ] Run `pytest`
