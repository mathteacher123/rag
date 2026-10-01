import sys

from app.services.rag.engine import query_engine
from app.services.rag.ingestion import ingest_url


def ingest(url: str):
    result = ingest_url(url)
    print(result)


def query(question: str):
    response = query_engine.query(question)
    print("=== ANSWER ===")
    print(response)
    print("\n=== SOURCES ===")
    for node in response.source_nodes:
        print(f"- score: {node.score:.4f} | {node.metadata.get('title', 'N/A')}")


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print('  python z1.py 1 "<url>"      (ingest)')
        print('  python z1.py 2 "<question>" (query)')
        sys.exit(1)

    mode = sys.argv[1]
    arg = sys.argv[2]

    if mode == "1":
        ingest(arg)
    elif mode == "2":
        query(arg)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
