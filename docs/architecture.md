# Architecture

> Educational demonstration. Not a medical device. See the disclaimer in the README.

## 1. High-level system

```mermaid
flowchart LR
    subgraph Client
        UI["Streamlit UI"]
        CLI["CLI"]
        REST["REST client / Swagger"]
    end

    subgraph App["Application layer"]
        API["FastAPI<br/>/analyze"]
    end

    subgraph Core["MediAgent core (LangGraph)"]
        ORCH["Orchestrator graph"]
    end

    subgraph Infra["Infrastructure (all free)"]
        LLM["LLM provider<br/>Groq / Gemini / Ollama"]
        VEC["Chroma vector store"]
        EMB["Local embeddings<br/>sentence-transformers"]
    end

    UI --> ORCH
    CLI --> ORCH
    REST --> API --> ORCH
    ORCH --> LLM
    ORCH --> VEC
    VEC --- EMB
```

## 2. Agent orchestration graph

```mermaid
flowchart TD
    START(["Case input:<br/>text + age + sex + meds"]) --> TRIAGE["🩺 Triage Agent<br/>urgency + red-flag check"]
    TRIAGE -->|EMERGENCY| EMERG["🚨 Emergency Report<br/>seek immediate care"]
    TRIAGE -->|continue| SYMP["📋 Symptom Analysis Agent<br/>structure the case"]
    SYMP --> KNOW["📚 Knowledge Retrieval Agent<br/>RAG over guideline corpus"]
    KNOW --> DRUG["💊 Drug Interaction Agent<br/>medication review"]
    DRUG --> DIFF["🧠 Differential Agent<br/>ranked candidate explanations"]
    DIFF --> REPORT["📝 Report Agent<br/>synthesise + disclaimer"]
    EMERG --> END(["Final output"])
    REPORT --> END
```

## 3. Why this design

| Decision | Reason |
| --- | --- |
| **LangGraph** for orchestration | Explicit state + conditional edges; the emergency short-circuit is a real routing example, not a toy. In demand on AI-engineering job posts. |
| **Provider abstraction** (`llm.py`) | Swap Groq / Gemini / Ollama via one env var. Reviewers see clean dependency inversion; you stay on free tiers. |
| **RAG grounding** | Differential reasoning is anchored to a retrieved corpus instead of raw model memory, reducing hallucination. |
| **Local embeddings** | `sentence-transformers` runs free with no API key, so the RAG layer costs nothing. |
| **Safety module** | Deterministic red-flag detection + disclaimers everywhere. Signals you understand responsible AI in a regulated domain — a hiring differentiator. |
| **Three interfaces** (UI, API, CLI) | Same core, three entry points — demonstrates separation of concerns. |

## 4. Data flow (single request)

1. Client sends case → orchestrator initialises `ClinicalState`.
2. **Triage** runs first; red-flag terms or an EMERGENCY classification route straight to the emergency report (safety guardrail).
3. Otherwise the case flows through symptom structuring → RAG retrieval → drug review → differential reasoning.
4. **Report** agent synthesises all prior outputs and appends the mandatory disclaimer.
5. Final `ClinicalState` returned to the client.
