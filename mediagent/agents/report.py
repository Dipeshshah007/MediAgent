"""Report Agent.

Final node. Synthesises every prior agent's output into a single readable
clinician-style summary, then wraps it in the mandatory safety disclaimer.
"""
from __future__ import annotations

from ..llm import get_llm
from ..safety import DISCLAIMER
from ..state import ClinicalState
from ..utils import call_llm

SYSTEM = """You write a concise, structured summary report for an EDUCATIONAL
demo. Use clear headings: Triage, Symptom Summary, Possible Explanations,
Medication Notes, Suggested Next Steps. Be measured and avoid definitive
claims. This is not medical advice."""


def report_node(state: ClinicalState) -> dict:
    user = (
        f"Triage: {state.get('triage')}\n"
        f"Symptoms: {state.get('symptoms')}\n"
        f"Differential: {state.get('differential')}\n"
        f"Drug interactions: {state.get('drug_interactions')}\n"
        f"Reference context used: {state.get('retrieved_knowledge', '')[:1500]}"
    )
    body = call_llm(get_llm(), SYSTEM, user)
    report = f"{body}\n\n{'-' * 60}\n{DISCLAIMER}"
    return {"final_report": report}
