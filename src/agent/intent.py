# src/agent/intent.py
from typing import Dict
from src.agent.commands import COMMANDS


def interpret_intent(text: str) -> Dict:
    """
    Match user text against COMMANDS examples.
    Returns best intent with confidence.
    """
    text = text.lower().strip()

    best_match = None
    best_score = 0.0

    for command, meta in COMMANDS.items():
        examples = meta.get("examples", [])
        if not examples:
            continue

        for example in examples:
            example = example.lower()

            score = _similarity(text, example)

            if score > best_score:
                best_score = score
                best_match = command

    if best_match and best_score >= 0.5:
        return {
            "intent": best_match,
            "confidence": round(best_score, 2),
            "message": f"I think you want to run `{best_match}`",
            "alternatives": [],
        }

    return {
        "intent": None,
        "confidence": 0.0,
    }


def _similarity(a: str, b: str) -> float:
    """
    Very lightweight _similarity score (token overlap).
    """

    a_tokens = set(a.split())
    b_tokens = set(b.split())

    if not a_tokens or not b_tokens:
        return 0.0

    overlap = a_tokens & b_tokens
    return len(overlap) / max(len(a_tokens), len(b_tokens))
