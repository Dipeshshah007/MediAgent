"""Ingest the local medical-knowledge corpus into a Chroma vector store.

Run once (or whenever you add documents):
    python -m scripts.ingest_knowledge

Embeddings run locally with sentence-transformers, so this step is free and
needs no API key.
"""
from __future__ import annotations

import glob
import os

from ..config import settings


def _load_documents() -> list[str]:
    paths = glob.glob(os.path.join(settings.knowledge_dir, "**", "*.md"), recursive=True)
    paths += glob.glob(os.path.join(settings.knowledge_dir, "**", "*.txt"), recursive=True)
    docs: list[str] = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            docs.append(f.read())
    return docs


def _chunk(text: str, size: int = 800, overlap: int = 120) -> list[str]:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return [c for c in chunks if c.strip()]


def build_index() -> int:
    """Build/refresh the vector store. Returns the number of chunks indexed."""
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    raw_docs = _load_documents()
    if not raw_docs:
        raise FileNotFoundError(
            f"No .md/.txt files found in {settings.knowledge_dir}. "
            "Add guideline documents there first."
        )

    chunks: list[str] = []
    for doc in raw_docs:
        chunks.extend(_chunk(doc))

    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    store = Chroma(
        collection_name="mediagent_knowledge",
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,
    )
    # Reset collection so re-running is idempotent.
    try:
        store.delete_collection()
    except Exception:
        pass
    store = Chroma(
        collection_name="mediagent_knowledge",
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,
    )
    store.add_texts(chunks)
    return len(chunks)


if __name__ == "__main__":
    n = build_index()
    print(f"Indexed {n} chunks into {settings.chroma_dir}")
