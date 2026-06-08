# 🩺 MediAgent — Multi-Agent Clinical Decision-Support System

A multi-agent LLM system that takes a free-text case description and walks it
through a pipeline of specialised agents — triage, symptom structuring,
knowledge retrieval (RAG), medication review, and differential reasoning —
to produce a structured, source-grounded summary.

Built with **LangGraph**, runs entirely on **free** model providers
(Groq / Google Gemini / local Ollama), and ships with a Streamlit UI, a
FastAPI service, and a CLI.

> ## ⚠️ Important disclaimer
> **MediAgent is an EDUCATIONAL software-engineering demonstration. It is NOT a
> medical device, NOT a diagnostic tool, and NOT medical advice.** Its output
> is illustrative and may be wrong. Never use it to diagnose, treat, or make
> decisions about any real person. Always consult a qualified healthcare
> professional. This project exists to demonstrate multi-agent orchestration,
> RAG, and responsible-AI patterns — nothing more.

---

## ✨ Highlights

- **6 cooperating agents** orchestrated as a stateful graph with conditional routing.
- **Provider-agnostic LLM layer** — switch Groq / Gemini / Ollama with one env var. Stays on free tiers.
- **RAG grounding** with a local Chroma vector store and free local embeddings (no API key for retrieval).
- **Safety-first**: deterministic emergency red-flag detection short-circuits the pipeline; disclaimers everywhere.
- **Three interfaces**: Streamlit UI, FastAPI REST API (with Swagger), and a CLI.
- **Tested + Dockerised**, clean package layout.

---

## 🏗️ Architecture

See [`docs/architecture.md`](docs/architecture.md) for full diagrams. In short:

```
triage ──(emergency)────────────────────────────► emergency report
   │
   └─(continue)─► symptoms ─► knowledge(RAG) ─► drug ─► differential ─► report
```

Each agent reads from and writes to a shared typed `ClinicalState`, so adding a
new capability is: add a field, add a node, wire one edge.

---

## 🚀 Quickstart

### 0. Prerequisites
- Python 3.10+ and VS Code (the project is plain Python — works anywhere).
- A free API key from **one** provider (or Ollama for fully-offline use).

### 1. Clone & create a virtual environment
```bash
git clone <your-repo-url> mediagent
cd mediagent
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure a free provider
```bash
cp .env.example .env     # Windows: copy .env.example .env
```
Then edit `.env`. **Easiest path — Groq (free & fast):**
1. Sign up at https://console.groq.com and create an API key.
2. Set `LLM_PROVIDER=groq` and paste the key into `GROQ_API_KEY`.

(Alternatives: `LLM_PROVIDER=gemini` with a free key from
https://aistudio.google.com, or `LLM_PROVIDER=ollama` for fully-local —
install Ollama, then `ollama pull llama3.1`.)

### 4. Build the knowledge index (RAG)
```bash
python -m scripts.ingest_knowledge
```
This embeds the sample documents in `data/medical_knowledge/` into a local
Chroma store. The first run downloads the embedding model (~90 MB) once.

### 5. Run it — pick any interface

**Streamlit UI (recommended for demos):**
```bash
streamlit run app/streamlit_app.py
```

**REST API + Swagger docs:**
```bash
uvicorn api.main:app --reload
# open http://localhost:8000/docs
```

**Command line:**
```bash
python -m scripts.run_cli "34-year-old with sore throat and mild fever for 3 days"
```

### 6. Run the tests
```bash
pytest
```
(Tests for safety, JSON parsing, and graph structure need no API key.)

---

## 📁 Project structure
```
mediagent/
├── mediagent/              # core package
│   ├── config.py           # env-driven settings
│   ├── llm.py              # Groq/Gemini/Ollama abstraction
│   ├── state.py            # shared ClinicalState schema
│   ├── safety.py           # disclaimers + red-flag guardrails
│   ├── utils.py            # LLM call helper + robust JSON parsing
│   ├── graph.py            # LangGraph orchestration
│   ├── agents/             # the six agents
│   └── rag/                # ingestion + retrieval
├── app/streamlit_app.py    # UI
├── api/main.py             # FastAPI service
├── scripts/                # ingest + CLI entrypoints
├── tests/                  # pytest suite
├── data/medical_knowledge/ # sample corpus (replace for real use)
└── docs/architecture.md    # diagrams
```

---

## 📌 Project rationale

### 1. What real-world problem does it address?
Clinicians and triage staff face information overload: scattered guidelines,
long medication lists, and time pressure. Early-stage information *triage and
organisation* — not decision-making — is a genuine pain point. MediAgent
demonstrates how a multi-agent system could *organise and summarise* case
information to support (never replace) a professional. As a portfolio piece it
shows you can model a messy, high-stakes workflow as a clean, safe pipeline.

### 2. What is the solution?
A coordinated team of narrow agents, each doing one job well, orchestrated by a
LangGraph state machine. Reasoning is grounded in a retrieved knowledge corpus
(RAG) rather than raw model memory, and a deterministic safety layer routes
apparent emergencies straight to a "seek immediate care" response. The output
is an organised summary with explicit confidence levels and caveats.

### 3. Who are the end users?
In this **educational framing**, the audience is *developers and recruiters*
evaluating multi-agent / RAG / responsible-AI skills. The *simulated* domain
users it models are healthcare staff who might use decision-*support* tooling —
but the project is explicitly not built or validated for real clinical users.

### 4. How scalable is it?
- **Stateless core** — each request is independent, so the FastAPI service
  scales horizontally behind a load balancer.
- **Pluggable models** — swap to higher-throughput hosted models without code
  changes via the provider abstraction.
- **Vector store** — Chroma for the demo; the retriever interface can be
  repointed at a managed vector DB (pgvector, Pinecone, etc.) for scale.
- **Agents are independent nodes** — parallelisable and individually replaceable.

### 5. Is it cost-effective, and what's the future scope?
**Cost:** runs at **$0** on free tiers — Groq/Gemini free APIs plus local
embeddings, so retrieval and the UI cost nothing. Ollama makes it fully
offline.
**Future scope:** real curated guideline corpus, a proper drug-interaction
database, citation/traceability for every claim, evaluation harness with
clinical QA, structured FHIR input, human-in-the-loop review, and
observability (LangSmith/tracing). Each is a natural next commit you can show.

---

## 🧰 Tech stack
LangGraph · LangChain · Groq / Gemini / Ollama · Chroma · sentence-transformers ·
FastAPI · Streamlit · Pydantic · pytest · Docker

## 📜 License
MIT (see [`LICENSE`](LICENSE)). Educational demo only — not a medical device.
