"""Symptom Analysis Agent.

Turns the free-text case description into a structured representation
(symptoms, onset, severity, duration) that downstream agents can reason over.
"""
from __future__ import annotations

from ..llm import get_llm
from ..state import ClinicalState
from ..utils import call_llm, extract_json

SYSTEM = """You extract structured clinical features from a case description.
This is an EDUCATIONAL demo, not medical advice.

Return ONLY a JSON object:
- "chief_complaint": short phrase
- "symptoms": list of strings
- "duration": string or "unknown"
- "severity": "mild" | "moderate" | "severe" | "unknown"
- "relevant_history": list of strings (may be empty)"""


def symptom_node(state: ClinicalState) -> dict:
    user = (
        f"Age: {state.get('age', 'unknown')}, Sex: {state.get('sex', 'unknown')}\n"
        f"Description: {state.get('patient_input', '')}"
    )
    raw = call_llm(get_llm(), SYSTEM, user)
    data = extract_json(raw) or {
        "chief_complaint": "unknown",
        "symptoms": [],
        "duration": "unknown",
        "severity": "unknown",
        "relevant_history": [],
    }
    return {"symptoms": data}
