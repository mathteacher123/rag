from unittest.mock import MagicMock, patch

SAMPLE_HTML = "<html><body><p>Test content</p></body></html>"

SAMPLE_CHUNKS = [
    MagicMock(
        text="# Introduction\n\nThis is the introduction section.",
        metadata={
            "title": "Test Page",
            "heading_path": "Introduction",
            "content_type": "prose",
            "chunk_index": 0,
        },
    ),
    MagicMock(
        text="## Background\n\nThe background section...",
        metadata={
            "title": "Test Page",
            "heading_path": "Introduction > Background",
            "content_type": "prose",
            "chunk_index": 1,
        },
    ),
]


class TestChunkingEndpoint:
    @patch("app.api.v1.endpoints.test.fetch_html", return_value=SAMPLE_HTML)
    @patch("app.api.v1.endpoints.test.chunk_html", return_value=SAMPLE_CHUNKS)
    def test_returns_chunks(self, mock_chunk, mock_fetch, client):
        response = client.post("/test/chunking", json={"url": "https://example.com"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["title"] == "Test Page"
        assert data[0]["content_type"] == "prose"
        assert data[0]["chunk_index"] == 0
        assert data[1]["heading_path"] == "Introduction > Background"

    @patch("app.api.v1.endpoints.test.fetch_html", return_value="")
    def test_returns_400_on_empty_content(self, mock_fetch, client):
        response = client.post("/test/chunking", json={"url": "https://invalid.url"})

        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to fetch content from URL"

    def test_returns_422_on_missing_body(self, client):
        response = client.post("/test/chunking")

        assert response.status_code == 422

    def test_returns_422_on_invalid_body(self, client):
        response = client.post("/test/chunking", json={"wrong": "field"})

        assert response.status_code == 422
