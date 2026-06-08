"""Retrieve relevant passages from the Chroma vector store."""
from __future__ import annotations

from functools import lru_cache

from ..config import settings


@lru_cache(maxsize=1)
def _get_store():
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        collection_name="mediagent_knowledge",
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,
    )


def retrieve(query: str, k: int = 4) -> list[str]:
    store = _get_store()
    results = store.similarity_search(query, k=k)
    return [d.page_content for d in results]
