"""Test that the agent graph compiles and has the expected structure.

Does not call any LLM, so no API key is required.
"""
from mediagent.graph import build_graph


def test_graph_compiles():
    graph = build_graph()
    assert graph is not None


def test_graph_has_nodes():
    graph = build_graph()
    node_names = set(graph.get_graph().nodes.keys())
    for expected in {"triage", "symptoms", "knowledge", "drug", "differential", "report"}:
        assert expected in node_names
