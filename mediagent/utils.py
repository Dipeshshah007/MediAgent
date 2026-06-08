"""Small, dependency-free utilities shared across agents."""
from __future__ import annotations

import json
import re
from typing import Any


def call_llm(llm, system: str, user: str) -> str:
    """Invoke a chat model with a system + user message and return plain text."""
    messages = [
        ("system", system),
        ("human", user),
    ]
    response = llm.invoke(messages)
    # LangChain chat models return an AIMessage with `.content`
    return getattr(response, "content", str(response)).strip()


def extract_json(text: str) -> dict[str, Any]:
    """Best-effort extraction of a JSON object from an LLM response.

    Smaller free models sometimes wrap JSON in markdown fences or add prose.
    This pulls out the first balanced {...} block and parses it, returning an
    empty dict on failure so a single bad response never crashes the pipeline.
    """
    if not text:
        return {}

    # Strip ```json ... ``` fences if present.
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text

    # Grab the outermost JSON object.
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end < start:
        return {}

    snippet = candidate[start : end + 1]
    try:
        return json.loads(snippet)
    except json.JSONDecodeError:
        # Last resort: remove trailing commas, then retry.
        cleaned = re.sub(r",\s*([}\]])", r"\1", snippet)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {}
