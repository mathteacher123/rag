import pytest


@pytest.fixture
def sample_html() -> str:
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Hello World</h1>
        <p>This is a test paragraph with some content.</p>
        <p>This is another paragraph with more text.</p>
    </body>
    </html>
    """


@pytest.fixture
def sample_text() -> str:
    return "This is sample text for chunking tests. " * 50


@pytest.fixture
def sample_markdown() -> str:
    return """# Introduction

This is the introduction section.

## Background

The background section contains important context.

## Methods

Our methodology involves several steps.

### Data Collection

We gathered data from multiple sources.

### Analysis

The analysis phase involved statistical testing.

## Results

The results show significant improvement.

## Conclusion

In summary this study demonstrates our approach."""


@pytest.fixture
def long_section_markdown() -> str:
    sentences = [f"This is sentence number {i}. " for i in range(200)]
    return "# Long Section\n\n" + "".join(sentences)


@pytest.fixture
def multi_header_markdown() -> str:
    return """# First Header

Content under first header.

## Second Header

Content under second header.

### Third Header

Content under third header.

## Another Second Header

More content here."""


@pytest.fixture
def mock_fetch_response():
    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content
            self.status_code = status_code

    return MockResponse
