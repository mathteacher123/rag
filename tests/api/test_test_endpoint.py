from unittest.mock import patch

SAMPLE_MARKDOWN = """# Introduction

This is the introduction section.

## Background

The background section contains important context."""

SAMPLE_CHUNKS = [
    {
        "content": "# Introduction\n\nThis is the introduction section.",
        "header": "# Introduction",
        "start_char": 0,
        "end_char": 45,
    },
    {
        "content": "## Background\n\nThe background section...",
        "header": "## Background",
        "start_char": 47,
        "end_char": 109,
    },
]


class TestChunkingEndpoint:
    @patch(
        "app.api.v1.endpoints.test.fetch_and_convert_to_markdown",
        return_value=SAMPLE_MARKDOWN,
    )
    @patch(
        "app.api.v1.endpoints.test.chunk_text",
        return_value=SAMPLE_CHUNKS,
    )
    def test_returns_chunks(self, mock_chunk, mock_fetch, client):
        response = client.post("/test/chunking", json={"url": "https://example.com"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["header"] == "# Introduction"
        assert data[1]["header"] == "## Background"

    @patch(
        "app.api.v1.endpoints.test.fetch_and_convert_to_markdown",
        return_value="",
    )
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
