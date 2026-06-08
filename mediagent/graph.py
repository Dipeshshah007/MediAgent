"""LangGraph orchestration.

Wires the agents into a directed graph with state passed between nodes.
The interesting bit is the conditional edge after triage: if the case looks
like an emergency, we skip the diagnostic reasoning entirely and route
straight to an emergency report. That is exactly the kind of control flow
LangGraph is built for, and it doubles as a safety guardrail.

Flow:
    triage ──(emergency)──────────────► report
       │
       └─(not emergency)─► symptoms ─► knowledge ─► drug ─► differential ─► report
"""
from __future__ import annotations

from langgraph.graph import END, StateGraph

from .agents import (
    differential_node,
    drug_node,
    knowledge_node,
    report_node,
    symptom_node,
    triage_node,
)
from .safety import emergency_message
from .state import ClinicalState


def _emergency_report_node(state: ClinicalState) -> dict:
    flags = state.get("triage", {}).get("red_flags", []) or ["urgent presentation"]
    return {"final_report": emergency_message(flags)}


def _route_after_triage(state: ClinicalState) -> str:
    return "emergency" if state.get("is_emergency") else "continue"


def build_graph():
    """Compile and return the runnable MediAgent graph."""
    g = StateGraph(ClinicalState)

    g.add_node("triage", triage_node)
    g.add_node("symptoms", symptom_node)
    g.add_node("knowledge", knowledge_node)
    g.add_node("drug", drug_node)
    g.add_node("differential", differential_node)
    g.add_node("report", report_node)
    g.add_node("emergency_report", _emergency_report_node)

    g.set_entry_point("triage")

    g.add_conditional_edges(
        "triage",
        _route_after_triage,
        {"emergency": "emergency_report", "continue": "symptoms"},
    )

    # Normal diagnostic path (linear, but each node is independent).
    g.add_edge("symptoms", "knowledge")
    g.add_edge("knowledge", "drug")
    g.add_edge("drug", "differential")
    g.add_edge("differential", "report")

    g.add_edge("report", END)
    g.add_edge("emergency_report", END)

    return g.compile()


# Build once at import time so the API/UI can reuse it.
GRAPH = build_graph()


def run_case(
    patient_input: str,
    age: int | None = None,
    sex: str | None = None,
    medications: list[str] | None = None,
) -> ClinicalState:
    """Convenience wrapper: run a single case end-to-end and return final state."""
    initial: ClinicalState = {
        "patient_input": patient_input,
        "age": age,
        "sex": sex,
        "medications": medications or [],
    }
    return GRAPH.invoke(initial)
