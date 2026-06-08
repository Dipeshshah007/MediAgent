"""Knowledge Retrieval Agent (RAG).

Queries the local vector store of medical guideline documents and returns the
most relevant passages as grounding context for the differential agent. This
is what keeps the system's reasoning anchored to a curated corpus rather than
relying purely on the LLM's parametric memory.
"""
from __future__ import annotations

from ..rag.retriever import retrieve
from ..state import ClinicalState


def knowledge_node(state: ClinicalState) -> dict:
    symptoms = state.get("symptoms", {})
    query_parts = [symptoms.get("chief_complaint", "")]
    query_parts += symptoms.get("symptoms", []) or []
    query = " ".join(p for p in query_parts if p) or state.get("patient_input", "")

    try:
        passages = retrieve(query, k=4)
        context = "\n\n---\n\n".join(passages) if passages else ""
    except Exception as exc:  # vector store not built yet, etc.
        context = f"[knowledge base unavailable: {exc}]"

    return {"retrieved_knowledge": context}
