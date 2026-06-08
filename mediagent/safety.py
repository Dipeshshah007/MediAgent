"""Safety guardrails.

This project is an EDUCATIONAL demonstration of multi-agent orchestration.
It is NOT a medical device and must never be used to make real clinical
decisions. This module centralises the disclaimers and the red-flag check
that the orchestrator uses to short-circuit obviously urgent cases.
"""
from __future__ import annotations

DISCLAIMER = (
    "\u26a0\ufe0f  EDUCATIONAL DEMO ONLY \u2014 NOT MEDICAL ADVICE.\n"
    "MediAgent is a software-engineering portfolio project that demonstrates "
    "multi-agent LLM orchestration. Its output is illustrative, may be wrong, "
    "and must never be used to diagnose, treat, or make decisions about any "
    "real person. Always consult a qualified healthcare professional. "
    "In an emergency, contact your local emergency services immediately."
)

# Plain-language phrases that should trigger an immediate "seek emergency care"
# response rather than a full differential-diagnosis run.
RED_FLAG_TERMS = [
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "unconscious",
    "not breathing",
    "severe bleeding",
    "stroke",
    "face drooping",
    "slurred speech",
    "suicidal",
    "want to die",
    "overdose",
    "anaphylaxis",
    "severe allergic reaction",
    "seizure",
    "blue lips",
]


def detect_red_flags(text: str) -> list[str]:
    """Return any emergency red-flag phrases found in the input text."""
    lowered = (text or "").lower()
    return [term for term in RED_FLAG_TERMS if term in lowered]


def emergency_message(flags: list[str]) -> str:
    return (
        "\U0001f6a8 POSSIBLE EMERGENCY DETECTED\n\n"
        f"The input mentioned: {', '.join(flags)}.\n"
        "This may indicate a medical emergency. Stop using this demo and seek "
        "immediate help from a real healthcare professional or your local "
        "emergency number now.\n\n" + DISCLAIMER
    )
