"""Tests for pure utility and safety functions.

These run without any API key or model, so they work in CI out of the box.
"""
from mediagent.safety import detect_red_flags, emergency_message, DISCLAIMER
from mediagent.utils import extract_json


def test_extract_json_plain():
    assert extract_json('{"level": "ROUTINE"}') == {"level": "ROUTINE"}


def test_extract_json_fenced():
    text = 'Here you go:\n```json\n{"a": 1, "b": [2, 3]}\n```\nThanks!'
    assert extract_json(text) == {"a": 1, "b": [2, 3]}


def test_extract_json_trailing_comma():
    assert extract_json('{"x": 1,}') == {"x": 1}


def test_extract_json_garbage_returns_empty():
    assert extract_json("no json here") == {}


def test_red_flags_detected():
    flags = detect_red_flags("Patient reports sudden chest pain and shortness of breath")
    assert "chest pain" in flags
    assert "shortness of breath" in flags


def test_red_flags_none():
    assert detect_red_flags("mild sore throat for two days") == []


def test_emergency_message_includes_disclaimer():
    msg = emergency_message(["chest pain"])
    assert "EMERGENCY" in msg
    assert DISCLAIMER in msg
