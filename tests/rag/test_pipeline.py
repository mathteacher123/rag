from unittest.mock import patch

from app.services.rag.chunking import chunk_html
from app.services.rag.scraping import fetch_html


class TestScraping:
    @patch("app.services.rag.scraping.trafilatura")
    def test_fetch_html_returns_raw_html(
        self, mock_trafilatura, sample_html_for_scraping
    ):
        mock_trafilatura.fetch_url.return_value = sample_html_for_scraping
        mock_trafilatura.extract.return_value = sample_html_for_scraping

        result = fetch_html("https://example.com")

        assert isinstance(result, str)
        assert len(result) > 0
        assert "<html>" in result

    @patch("app.services.rag.scraping.trafilatura")
    def test_fetch_html_returns_empty_on_none(self, mock_trafilatura):
        mock_trafilatura.fetch_url.return_value = None

        result = fetch_html("https://invalid.url")

        assert result == ""


class TestChunkHtmlBasic:
    def test_returns_list_of_documents(self, sample_html):
        chunks = chunk_html(sample_html)

        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_empty_html_returns_empty(self):
        chunks = chunk_html("")
        assert chunks == []

    def test_whitespace_only_returns_empty(self):
        chunks = chunk_html("   \n\n  ")
        assert chunks == []


class TestChunkHtmlMetadata:
    def test_title_extracted(self, sample_html):
        chunks = chunk_html(sample_html)

        assert chunks[0].metadata["title"] == "Test Page"

    def test_title_missing(self, html_no_title):
        chunks = chunk_html(html_no_title)

        assert chunks[0].metadata["title"] is None

    def test_chunk_index_sequential(self, sample_html):
        chunks = chunk_html(sample_html)

        for i, chunk in enumerate(chunks):
            assert chunk.metadata["chunk_index"] == i

    def test_heading_metadata(self, html_with_headings):
        chunks = chunk_html(html_with_headings)

        heading_paths = [c.metadata["heading_path"] for c in chunks]
        assert "Introduction" in heading_paths[0]
        assert "Background" in heading_paths[1]

    def test_heading_hierarchy_nesting(self, html_with_headings):
        chunks = chunk_html(html_with_headings)

        path = "Introduction > Background > Specifics"
        specifics = [c for c in chunks if "Specifics" in c.metadata["heading_path"]]
        assert len(specifics) == 1
        assert path == specifics[0].metadata["heading_path"]


class TestChunkHtmlContentType:
    def test_content_type_prose(self, sample_html):
        chunks = chunk_html(sample_html)

        content_types = [c.metadata["content_type"] for c in chunks]
        assert "prose" in content_types

    def test_content_type_table(self, html_with_table):
        chunks = chunk_html(html_with_table)

        content_types = [c.metadata["content_type"] for c in chunks]
        assert "table" in content_types

    def test_content_type_list(self, html_with_list):
        chunks = chunk_html(html_with_list)

        content_types = [c.metadata["content_type"] for c in chunks]
        assert "list" in content_types

    def test_content_type_blockquote(self, html_with_blockquote):
        chunks = chunk_html(html_with_blockquote)

        content_types = [c.metadata["content_type"] for c in chunks]
        assert "blockquote" in content_types


class TestChunkHtmlSplitting:
    def test_long_prose_is_split(self, long_html):
        chunks = chunk_html(long_html, chunk_size=200, chunk_overlap=50)

        assert len(chunks) > 1

    def test_table_stays_intact(self, html_with_table):
        chunks = chunk_html(html_with_table)

        table_chunks = [c for c in chunks if c.metadata["content_type"] == "table"]
        assert len(table_chunks) == 1

    def test_list_stays_intact(self, html_with_list):
        chunks = chunk_html(html_with_list)

        list_chunks = [c for c in chunks if c.metadata["content_type"] == "list"]
        assert len(list_chunks) == 1

    def test_blockquote_stays_intact(self, html_with_blockquote):
        chunks = chunk_html(html_with_blockquote)

        bq = [c for c in chunks if c.metadata["content_type"] == "blockquote"]
        assert len(bq) == 1
