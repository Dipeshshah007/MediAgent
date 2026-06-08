"""Triage Agent.

First in the pipeline. Assesses urgency and decides whether the case looks
like an emergency. Combines a deterministic red-flag check (fast, reliable)
with an LLM assessment (nuanced).
"""
from __future__ import annotations

from ..llm import get_llm
from ..safety import detect_red_flags
from ..state import ClinicalState
from ..utils import call_llm, extract_json

SYSTEM = """You are a clinical triage assistant in an EDUCATIONAL demo.
Classify the urgency of a described case. You are NOT giving medical advice.

Return ONLY a JSON object with these keys:
- "level": one of "EMERGENCY", "URGENT", "ROUTINE"
- "reason": one short sentence explaining the classification
- "recommended_setting": e.g. "emergency department", "same-day GP", "self-care / pharmacy"

Be conservative: if there is any doubt about a life-threatening sign, choose EMERGENCY."""


def triage_node(state: ClinicalState) -> dict:
    text = state.get("patient_input", "")
    flags = detect_red_flags(text)

    user = (
        f"Patient age: {state.get('age', 'unknown')}\n"
        f"Patient sex: {state.get('sex', 'unknown')}\n"
        f"Case description: {text}"
    )
    raw = call_llm(get_llm(), SYSTEM, user)
    data = extract_json(raw) or {
        "level": "ROUTINE",
        "reason": "Model output could not be parsed; defaulting to routine.",
        "recommended_setting": "consult a healthcare professional",
    }

    # Red flags override the model toward EMERGENCY.
    is_emergency = bool(flags) or data.get("level") == "EMERGENCY"
    if flags:
        data["level"] = "EMERGENCY"
        data["red_flags"] = flags

    return {"triage": data, "is_emergency": is_emergency}
