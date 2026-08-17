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
def html_with_headings() -> str:
    return """
    <html>
    <head><title>Heading Test</title></head>
    <body>
        <h1>Introduction</h1>
        <p>Intro content here.</p>
        <h2>Background</h2>
        <p>Background details.</p>
        <h3>Specifics</h3>
        <p>Specific information.</p>
        <h2>Methods</h2>
        <p>Methodology description.</p>
    </body>
    </html>
    """


@pytest.fixture
def html_with_table() -> str:
    return """
    <html>
    <head><title>Table Test</title></head>
    <body>
        <h1>Data</h1>
        <table>
            <tr><th>Name</th><th>Value</th></tr>
            <tr><td>Alpha</td><td>100</td></tr>
            <tr><td>Beta</td><td>200</td></tr>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def html_with_list() -> str:
    return """
    <html>
    <head><title>List Test</title></head>
    <body>
        <h1>Items</h1>
        <ul>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ul>
    </body>
    </html>
    """


@pytest.fixture
def html_with_blockquote() -> str:
    return """
    <html>
    <head><title>Quote Test</title></head>
    <body>
        <h1>References</h1>
        <blockquote>This is an important quote from a source.</blockquote>
    </body>
    </html>
    """


@pytest.fixture
def html_no_title() -> str:
    return """
    <html>
    <body>
        <h1>No Title Page</h1>
        <p>Content without a title tag.</p>
    </body>
    </html>
    """


@pytest.fixture
def long_html() -> str:
    sentences = " ".join([f"This is sentence number {i}." for i in range(100)])
    return f"""
    <html>
    <head><title>Long Content</title></head>
    <body>
        <h1>Long Section</h1>
        <p>{sentences}</p>
    </body>
    </html>
    """


@pytest.fixture
def sample_html_for_scraping() -> str:
    return """
    <html>
    <head><title>Scraped Page</title></head>
    <body>
        <h1>Scraped Content</h1>
        <p>This content was fetched from a URL.</p>
    </body>
    </html>
    """
