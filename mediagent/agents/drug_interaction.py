"""Drug Interaction Agent.

Reviews the patient's listed medications for potential interactions. In a real
system this would query a curated database (e.g. an RxNorm / DrugBank-style
source); here it uses the LLM as a stand-in and is clearly flagged as
illustrative only.
"""
from __future__ import annotations

from ..llm import get_llm
from ..state import ClinicalState
from ..utils import call_llm, extract_json

SYSTEM = """You review a medication list for POTENTIAL interactions in an
EDUCATIONAL demo. This is not medical advice and may be incomplete or wrong.

Return ONLY a JSON object:
- "interactions": list of objects, each {"pair": "drugA + drugB", "concern": "short note", "severity": "low|moderate|high"}
- "notes": short overall caveat string
If fewer than two medications are given, return an empty interactions list."""


def drug_node(state: ClinicalState) -> dict:
    meds = state.get("medications") or []
    if len(meds) < 2:
        return {
            "drug_interactions": {
                "interactions": [],
                "notes": "Fewer than two medications provided; no pairwise check performed.",
            }
        }

    user = "Medications: " + ", ".join(meds)
    raw = call_llm(get_llm(), SYSTEM, user)
    data = extract_json(raw) or {"interactions": [], "notes": "Could not parse model output."}
    return {"drug_interactions": data}
