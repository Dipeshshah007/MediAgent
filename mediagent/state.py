"""Shared state passed between agents in the LangGraph pipeline.

Each agent reads the fields it needs and writes back a partial update. Using a
single typed state object (instead of ad-hoc function arguments) is what makes
the system easy to extend: add a field, add a node, wire one edge.
"""
from __future__ import annotations

from typing import Any, TypedDict


class ClinicalState(TypedDict, total=False):
    # ----- Inputs -----
    patient_input: str          # free-text description of the case
    age: int | None
    sex: str | None
    medications: list[str]      # current medications, by name

    # ----- Agent outputs -----
    triage: dict[str, Any]              # urgency level + reasoning
    is_emergency: bool                  # set by triage / red-flag check
    symptoms: dict[str, Any]            # structured symptom list
    retrieved_knowledge: str            # RAG context from guideline corpus
    drug_interactions: dict[str, Any]   # potential interaction notes
    differential: dict[str, Any]        # candidate conditions + confidence
    final_report: str                   # synthesised, disclaimer-wrapped report
