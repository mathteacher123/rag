from bs4 import BeautifulSoup
from llama_index.core import Document
from llama_index.core.node_parser import HTMLNodeParser, SentenceSplitter


def chunk_html(html, chunk_size=600, chunk_overlap=75):
    """
    Chunk HTML for RAG using a structure-aware LlamaIndex pipeline.

    Metadata preserved on every chunk:
        title
        heading_path
        content_type
        chunk_index
    """

    soup = BeautifulSoup(html, "html.parser")

    # ---------------------------------------------------------
    # 1. Document title
    # ---------------------------------------------------------
    title_tag = soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else None

    # ---------------------------------------------------------
    # 2. Extract HTML into structural units
    # ---------------------------------------------------------
    parser = HTMLNodeParser(
        tags=[
            "h1", "h2", "h3", "h4", "h5", "h6",
            "p",
            "li",
            "table",
            "blockquote",
        ]
    )

    document = Document(text=html)
    html_nodes = parser.get_nodes_from_documents([document])

    # ---------------------------------------------------------
    # 3. Walk nodes and maintain heading hierarchy
    # ---------------------------------------------------------
    heading_path = []
    prepared_nodes = []

    for node in html_nodes:
        tag = node.metadata.get("tag", "")
        text = node.text.strip()

        if not text:
            continue

        # -------------------------
        # Heading
        # -------------------------
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:

            level = int(tag[1])

            # Keep only headings above the current level
            heading_path = heading_path[:level - 1]

            heading_path.append(text)

            # IMPORTANT:
            # Do NOT create a chunk for the heading.
            # It becomes metadata for following content.
            continue

        # -------------------------
        # Content type
        # -------------------------
        if tag == "table":
            content_type = "table"

        elif tag == "li":
            content_type = "list"

        elif tag == "blockquote":
            content_type = "blockquote"

        else:
            content_type = "prose"

        prepared_nodes.append({
            "node": node,
            "heading_path": list(heading_path),
            "content_type": content_type,
        })

    # ---------------------------------------------------------
    # 4. Split content
    # ---------------------------------------------------------
    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    final_chunks = []

    for item in prepared_nodes:

        node = item["node"]
        content_type = item["content_type"]

        # ---------------------------------------------
        # Structural content stays together
        # ---------------------------------------------
        if content_type in ["table", "blockquote"]:

            chunks = [node]

        # ---------------------------------------------
        # Lists: keep consecutive list items together
        # ---------------------------------------------
        elif content_type == "list":

            chunks = [node]

        # ---------------------------------------------
        # Prose: sentence-aware chunking
        # ---------------------------------------------
        else:

            chunks = splitter.get_nodes_from_documents([node])

        # ---------------------------------------------
        # Preserve our metadata
        # ---------------------------------------------
        for chunk in chunks:

            chunk.metadata = {
                "title": title,
                "heading_path": " > ".join(item["heading_path"]),
                "content_type": content_type,
            }

            final_chunks.append(chunk)

    # ---------------------------------------------------------
    # 5. Add chunk index
    # ---------------------------------------------------------
    for index, chunk in enumerate(final_chunks):
        chunk.metadata["chunk_index"] = index

    return final_chunks