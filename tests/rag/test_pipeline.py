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


class TestChunkingPhaseA:
    """Phase A: Markdown header splitting."""

    def test_returns_list_of_dicts(self, sample_markdown):
        chunks = chunk_text(sample_markdown)

        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(
            "content" in c and "header" in c and "start_char" in c and "end_char" in c
            for c in chunks
        )

    def test_splits_by_headers(self, multi_header_markdown):
        chunks = chunk_text(multi_header_markdown, chunk_size=5000)

        headers = [c["header"] for c in chunks]
        assert "# First Header" in headers
        assert "## Second Header" in headers
        assert "### Third Header" in headers
        assert "## Another Second Header" in headers

    def test_empty_string(self):
        chunks = chunk_text("")
        assert chunks == []

    def test_whitespace_only(self):
        chunks = chunk_text("   \n\n  ")
        assert chunks == []

    def test_no_headers_returns_single_chunk(self):
        text = "Just plain text without any headers."
        chunks = chunk_text(text, chunk_size=5000)

        assert len(chunks) == 1
        assert chunks[0]["header"] == ""


class TestChunkingPhaseB:
    """Phase B: Sentence-aware splitting for long sections."""

    def test_short_section_not_split(self, sample_markdown):
        chunks = chunk_text(sample_markdown, chunk_size=5000)

        for chunk in chunks:
            assert len(chunk["content"]) <= 5000

    def test_long_section_respects_chunk_size(self, long_section_markdown):
        chunks = chunk_text(long_section_markdown, chunk_size=200, overlap=50)

        for chunk in chunks:
            assert len(chunk["content"]) <= 250

    def test_overlap_at_sentence_boundary(self):
        sentences = " ".join([f"Sentence {i}." for i in range(30)])
        text = f"# Header\n\n{sentences}"
        chunks = chunk_text(text, chunk_size=150, overlap=50)

        if len(chunks) > 1:
            for i in range(1, len(chunks)):
                prev_content = chunks[i - 1]["content"]
                curr_content = chunks[i]["content"]

                prev_words = set(prev_content.split())
                curr_words = set(curr_content.split())
                overlap_words = prev_words & curr_words

                assert len(overlap_words) > 0

    def test_overlap_never_splits_mid_sentence(self):
        sentences = [f"Long sentence number {i} with extra words. " for i in range(50)]
        text = "# Header\n\n" + "".join(sentences)
        chunks = chunk_text(text, chunk_size=300, overlap=100)

        for chunk in chunks:
            content = chunk["content"].strip()
            if content:
                ends_cleanly = (
                    content.endswith(".")
                    or content.endswith("?")
                    or content.endswith("\n")
                )
                assert ends_cleanly


class TestChunkingIntegration:
    def test_full_pipeline(self, sample_markdown):
        chunks = chunk_text(sample_markdown, chunk_size=500, overlap=100)

        assert len(chunks) > 0
        for chunk in chunks:
            assert len(chunk["content"]) > 0
            assert chunk["start_char"] < chunk["end_char"]


@pytest.mark.integration
class TestIntegration:
    def test_fetch_real_url(self):
        result = fetch_and_convert_to_markdown("https://example.com")

        assert isinstance(result, str)
        assert len(result) > 0
