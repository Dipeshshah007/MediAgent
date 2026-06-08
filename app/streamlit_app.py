"""Streamlit UI for MediAgent.

Run with:
    streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make the project root importable when Streamlit runs this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

from mediagent.config import settings  # noqa: E402
from mediagent.graph import run_case  # noqa: E402
from mediagent.safety import DISCLAIMER  # noqa: E402

st.set_page_config(page_title="MediAgent (Demo)", page_icon="\U0001fa7a", layout="centered")

st.title("\U0001fa7a MediAgent")
st.caption("Multi-Agent Clinical Decision-Support \u2014 educational demonstration")
st.error(DISCLAIMER)

with st.sidebar:
    st.subheader("Configuration")
    st.write(f"**LLM provider:** `{settings.llm_provider}`")
    st.write(f"**Embeddings:** `{settings.embedding_model}`")
    st.info(
        "Switch provider by editing `.env` (LLM_PROVIDER = groq | gemini | ollama). "
        "All three have free options."
    )

st.subheader("Describe the case")
patient_input = st.text_area(
    "Case description",
    placeholder="e.g. 34-year-old with 3 days of sore throat, mild fever, and fatigue.",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
with col2:
    sex = st.selectbox("Sex", ["unknown", "female", "male", "other"])

meds_raw = st.text_input("Current medications (comma-separated)", placeholder="ibuprofen, warfarin")
medications = [m.strip() for m in meds_raw.split(",") if m.strip()]

if st.button("Run analysis", type="primary"):
    if not patient_input.strip():
        st.warning("Please enter a case description.")
    else:
        with st.spinner("Agents working\u2026"):
            state = run_case(
                patient_input=patient_input,
                age=int(age),
                sex=None if sex == "unknown" else sex,
                medications=medications,
            )

        if state.get("is_emergency"):
            st.error(state.get("final_report"))
        else:
            st.success("Analysis complete")

            with st.expander("1. Triage", expanded=True):
                st.json(state.get("triage", {}))
            with st.expander("2. Structured symptoms"):
                st.json(state.get("symptoms", {}))
            with st.expander("3. Medication interaction notes"):
                st.json(state.get("drug_interactions", {}))
            with st.expander("4. Differential reasoning"):
                st.json(state.get("differential", {}))

            st.subheader("Summary report")
            st.markdown(state.get("final_report", ""))
