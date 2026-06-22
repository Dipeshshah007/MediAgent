# 🩺 MediAgent — Multi-Agent Clinical Decision-Support System

A multi-agent LLM system that takes a free-text case description and walks it
through a pipeline of specialised agents — triage, symptom structuring,
knowledge retrieval (RAG), medication review, and differential reasoning 
to produce a structured, source-grounded summary.

---

## ✨ Highlights

- **6 cooperating agents** orchestrated as a stateful graph with conditional routing.
- **Provider-agnostic LLM layer** — switch Groq / Gemini / Ollama with one env var. Stays on free tiers.
- **RAG grounding** with a local Chroma vector store and free local embeddings (no API key for retrieval).
- **Safety-first**: deterministic emergency red-flag detection short-circuits the pipeline; disclaimers everywhere.
- **Three interfaces**: Streamlit UI, FastAPI REST API (with Swagger), and a CLI.
- **Tested + Dockerised**, clean package layout.

---

## 🧰 Tech stack
LangGraph · LangChain · Groq / Gemini / Ollama · Chroma · sentence-transformers ·
FastAPI · Streamlit · Pydantic · pytest · Docker

## 🚀 Setup & Run the Project: 

### 1. Clone & create a virtual environment
```bash
git clone https://github.com/YOUR_USERNAME/mediagent.git
cd mediagent
code .
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
1. Sign up at https://console.groq.com and create an API key.
2. Set `LLM_PROVIDER=groq` and paste the key into `GROQ_API_KEY`.
```

### 4. Build the knowledge index (RAG)
```bash
python -m scripts.ingest_knowledge
```
This embeds the sample documents in `data/medical_knowledge/` into a local
Chroma store. The first run downloads the embedding model (~90 MB) once.

### 5. Run it — pick any interface

**Streamlit UI:**
```bash
streamlit run app/streamlit_app.py
```
