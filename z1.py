import sys

from app.services.rag.ingestion import ingest_url


def main():
    if len(sys.argv) != 2:
        print("Usage: python z1.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    result = ingest_url(url)
    print(result)


if __name__ == "__main__":
    main()
