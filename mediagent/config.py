"""Central configuration for MediAgent.

All settings are read from environment variables (or a local .env file).
Copy .env.example to .env and fill in ONE free provider's key to get started.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ----- Which LLM backend to use: "groq" | "gemini" | "ollama" -----
    # groq   -> free hosted Llama models (fast, recommended to start)
    # gemini -> free Google AI Studio tier
    # ollama -> fully local & offline, no API key needed
    llm_provider: str = "groq"

    # Groq (https://console.groq.com  -> free API key)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Google Gemini (https://aistudio.google.com -> free API key)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # Ollama (https://ollama.com -> run `ollama pull llama3.1`)
    ollama_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434"

    # ----- Embeddings (runs locally, free, no API key) -----
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ----- Storage paths -----
    chroma_dir: str = "./data/chroma"
    knowledge_dir: str = "./data/medical_knowledge"

    # Generation
    temperature: float = 0.2


settings = Settings()
