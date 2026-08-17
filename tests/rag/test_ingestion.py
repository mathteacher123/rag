from unittest.mock import MagicMock, patch

from app.services.rag.ingestion import ingest_url


@patch("app.services.rag.ingestion.embed_model")
@patch("app.services.rag.ingestion.vector_store")
@patch("app.services.rag.ingestion.chunk_html")
@patch("app.services.rag.ingestion.fetch_html")
def test_ingest_returns_chunk_count(mock_fetch, mock_chunk, mock_vs, mock_embed):
    mock_fetch.return_value = "<html><p>Hello</p></html>"
    metadata = {
        "title": "T",
        "heading_path": "",
        "content_type": "prose",
        "chunk_index": 0,
    }
    mock_chunk.return_value = [MagicMock(text="Hello", metadata=metadata)]
    mock_embed.get_text_embedding.return_value = [0.1] * 768
    mock_vs.delete = MagicMock()
    mock_vs.add = MagicMock()

    result = ingest_url("https://example.com/page")
    assert result["chunk_count"] == 1
    assert result["status"] == "success"


@patch("app.services.rag.ingestion.embed_model")
@patch("app.services.rag.ingestion.vector_store")
@patch("app.services.rag.ingestion.chunk_html")
@patch("app.services.rag.ingestion.fetch_html")
def test_ingest_deletes_old_before_insert(mock_fetch, mock_chunk, mock_vs, mock_embed):
    mock_fetch.return_value = "<html><p>Hello</p></html>"
    metadata = {
        "title": "T",
        "heading_path": "",
        "content_type": "prose",
        "chunk_index": 0,
    }
    mock_chunk.return_value = [MagicMock(text="Hello", metadata=metadata)]
    mock_embed.get_text_embedding.return_value = [0.1] * 768
    mock_vs.delete = MagicMock()
    mock_vs.add = MagicMock()

    ingest_url("https://example.com/page")
    mock_vs.delete.assert_called_once()
    mock_vs.add.assert_called_once()


@patch("app.services.rag.ingestion.fetch_html")
def test_ingest_returns_failed_on_empty_html(mock_fetch):
    mock_fetch.return_value = ""
    result = ingest_url("https://example.com/missing")
    assert result["status"] == "failed_to_fetch"
    assert result["chunk_count"] == 0
