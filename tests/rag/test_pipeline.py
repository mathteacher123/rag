from unittest.mock import patch

import pytest

from app.services.rag.chunking import chunk_text
from app.services.rag.scraping import fetch_and_convert_to_markdown


class TestScraping:
    @patch("app.services.rag.scraping.trafilatura")
    def test_fetch_and_convert_returns_markdown(self, mock_trafilatura, sample_html):
        mock_trafilatura.fetch_url.return_value = sample_html
        mock_trafilatura.extract.return_value = sample_html

        result = fetch_and_convert_to_markdown("https://example.com")

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("app.services.rag.scraping.trafilatura")
    def test_fetch_and_convert_returns_empty_on_none(self, mock_trafilatura):
        mock_trafilatura.fetch_url.return_value = None

        result = fetch_and_convert_to_markdown("https://invalid.url")

        assert result == ""


class TestChunking:
    def test_chunk_text_returns_list_of_dicts(self, sample_text):
        chunks = chunk_text(sample_text)

        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all("content" in c and "start" in c and "end" in c for c in chunks)

    def test_chunk_text_respects_chunk_size(self, sample_text):
        chunk_size = 100
        chunks = chunk_text(sample_text, chunk_size=chunk_size)

        for chunk in chunks:
            assert len(chunk["content"]) <= chunk_size

    def test_chunk_text_empty_string(self):
        chunks = chunk_text("")
        assert chunks == []

    def test_chunk_text_short_text(self):
        text = "Short"
        chunks = chunk_text(text, chunk_size=100)

        assert len(chunks) == 1
        assert chunks[0]["content"] == text

    def test_chunk_text_overlap(self):
        text = "A" * 200
        chunks = chunk_text(text, chunk_size=100, overlap=20)

        assert len(chunks) > 1
        for i in range(1, len(chunks)):
            prev_end = chunks[i - 1]["end"]
            curr_start = chunks[i]["start"]
            assert prev_end - curr_start == 20


@pytest.mark.integration
class TestIntegration:
    def test_fetch_real_url(self):
        result = fetch_and_convert_to_markdown("https://example.com")

        assert isinstance(result, str)
        assert len(result) > 0
