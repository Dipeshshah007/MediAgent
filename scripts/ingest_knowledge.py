"""Build the RAG vector store from the knowledge corpus.

Usage:
    python -m scripts.ingest_knowledge
"""
from mediagent.config import settings
from mediagent.rag.ingest import build_index

if __name__ == "__main__":
    count = build_index()
    print(f"\u2705 Indexed {count} chunks into {settings.chroma_dir}")
