"""FastAPI backend for MediAgent.

Run with:
    uvicorn api.main:app --reload

Then open http://localhost:8000/docs for interactive Swagger docs.
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from mediagent.graph import run_case
from mediagent.safety import DISCLAIMER

app = FastAPI(
    title="MediAgent API",
    description="Educational multi-agent clinical decision-support demo. NOT medical advice.",
    version="1.0.0",
)


class CaseRequest(BaseModel):
    patient_input: str = Field(..., description="Free-text case description")
    age: int | None = None
    sex: str | None = None
    medications: list[str] = Field(default_factory=list)


class CaseResponse(BaseModel):
    triage: dict | None = None
    is_emergency: bool = False
    symptoms: dict | None = None
    drug_interactions: dict | None = None
    differential: dict | None = None
    final_report: str
    disclaimer: str = DISCLAIMER


@app.get("/")
def root():
    return {"service": "MediAgent", "status": "ok", "disclaimer": DISCLAIMER}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=CaseResponse)
def analyze(req: CaseRequest):
    state = run_case(
        patient_input=req.patient_input,
        age=req.age,
        sex=req.sex,
        medications=req.medications,
    )
    return CaseResponse(
        triage=state.get("triage"),
        is_emergency=state.get("is_emergency", False),
        symptoms=state.get("symptoms"),
        drug_interactions=state.get("drug_interactions"),
        differential=state.get("differential"),
        final_report=state.get("final_report", ""),
    )
