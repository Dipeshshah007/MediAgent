"""LLM provider abstraction.

Lets you switch between free backends (Groq, Gemini, or local Ollama) by
changing a single environment variable. Every agent calls `get_llm()` so the
rest of the codebase never cares which provider is active.
"""
from __future__ import annotations

from functools import lru_cache

from .config import settings


@lru_cache(maxsize=4)
def get_llm(temperature: float | None = None):
    """Return a LangChain chat model for the configured provider.

    The returned object exposes a uniform `.invoke(messages)` interface, so the
    agents are completely decoupled from the underlying provider.
    """
    temp = settings.temperature if temperature is None else temperature
    provider = settings.llm_provider.lower().strip()

    if provider == "groq":
        from langchain_groq import ChatGroq

        if not settings.groq_api_key:
            raise RuntimeError(
                "LLM_PROVIDER=groq but GROQ_API_KEY is empty. "
                "Get a free key at https://console.groq.com"
            )
        return ChatGroq(
            model=settings.groq_model,
            temperature=temp,
            api_key=settings.groq_api_key,
        )

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        if not settings.gemini_api_key:
            raise RuntimeError(
                "LLM_PROVIDER=gemini but GEMINI_API_KEY is empty. "
                "Get a free key at https://aistudio.google.com"
            )
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=temp,
            google_api_key=settings.gemini_api_key,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=temp,
        )

    raise ValueError(
        f"Unknown LLM_PROVIDER '{settings.llm_provider}'. "
        "Use one of: groq, gemini, ollama."
    )
