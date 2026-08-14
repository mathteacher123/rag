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
def mock_fetch_response():
    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content
            self.status_code = status_code

    return MockResponse
