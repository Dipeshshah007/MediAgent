"""Differential Diagnosis Agent.

The reasoning core. Combines the structured symptoms with the retrieved
guideline context to produce a ranked list of candidate explanations, each
with a confidence band and the evidence that supports it. Grounding the prompt
in the RAG context reduces hallucination versus free-form generation.
"""
from __future__ import annotations

from ..llm import get_llm
from ..state import ClinicalState
from ..utils import call_llm, extract_json

SYSTEM = """You are a differential-reasoning assistant in an EDUCATIONAL demo.
Using ONLY the structured symptoms and the provided reference context, list
plausible explanations. This is not a diagnosis and not medical advice.

Return ONLY a JSON object:
- "candidates": list of objects, each
    {"condition": str, "confidence": "low|moderate|high", "supporting": "short evidence from context/symptoms"}
- "recommended_next_steps": list of strings (e.g. tests or specialist referral)
- "caveats": short string noting the limits of this reasoning
Prefer 'low' confidence when context is thin. Never invent reference facts."""


def differential_node(state: ClinicalState) -> dict:
    symptoms = state.get("symptoms", {})
    context = state.get("retrieved_knowledge", "") or "(no reference context retrieved)"

    user = (
        f"Structured symptoms: {symptoms}\n\n"
        f"Reference context:\n{context}"
    )
    raw = call_llm(get_llm(), SYSTEM, user)
    data = extract_json(raw) or {
        "candidates": [],
        "recommended_next_steps": ["Consult a healthcare professional."],
        "caveats": "Model output could not be parsed.",
    }
    return {"differential": data}
