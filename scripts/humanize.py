"""
Universal Hunter - Dynamic Humanization & Anti-AI Slop Processing Layer
Applies stochastic punctuation relaxation, lowercase capitalization, contraction replacements,
and removes generic solicitation tails to bypass NLP spam classifiers (SimHash/Jaccard).
"""

from __future__ import annotations

import json
import random
import re
import sys

AI_SOLICITATION_PATTERNS = [
    r"(?i)\b(let me know if you (need|have|want)|feel free to (reach out|dm|message|ask)|hope this (helps|helped)|reach out if you|shout if you need|let me know if there)\b.*$",
    r"(?i)\b(if you have any (questions|issues),? (feel free|don't hesitate|let me know))\b.*$",
    r"(?i)\b(happy to help|hope that clears things up|best of luck with)\b.*$",
]

BIO_HOOK_PATTERNS = [
    r"(?i)\b(pinned\s+(a\s+)?(breakdown|guide|checklist|notes|matrix|workflow|sheet)\s+on\s+my\s+profile)\b.*?[.!?]?",
    r"(?i)\b(left\s+(the\s+)?(breakdown|notes|details|checklist|summary)\s+(in|on)\s+my\s+bio)\b.*?[.!?]?",
    r"(?i)\b(check\s+my\s+(bio|profile)\s+for\s+the\s+checklist)\b.*?[.!?]?",
    r"(?i)\b(see\s+(my\s+)?(bio|profile)\s+for\s+link)\b.*?[.!?]?",
]


def strip_ai_solicitation(text: str) -> str:
    """Strip generic corporate AI closing phrases (e.g. 'let me know if you need help')."""
    if not text:
        return ""
    cleaned = text.strip()
    for pattern in AI_SOLICITATION_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned).strip()
    cleaned = re.sub(r"[,;:\-–—\s]+$", "", cleaned).strip()
    return cleaned


def strip_bio_hooks(text: str) -> str:
    """Strip Bio-routing invitations if account's profile bio is not configured."""
    if not text:
        return ""
    cleaned = text
    for pattern in BIO_HOOK_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned).strip()
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def humanize_text(
    text: str,
    lowercase_prob: float = 0.40,
    strip_period_prob: float = 0.55,
    contractions_prob: float = 0.25,
    seed: int | None = None
) -> str:
    """
    Applies humanization rules:
    1. Strip robotic AI solicitation endings.
    2. Lowercase first letter with probability (default 40%).
    3. Strip trailing period with probability (default 55%).
    4. Occasional peer speech contractions (because -> bc, you -> u).
    """
    if not text:
        return ""

    if seed is not None:
        random.seed(seed)

    cleaned = strip_ai_solicitation(text)
    if not cleaned:
        return text

    # Do not perturb markdown headers or links
    first_char = cleaned[0]
    if first_char.isalpha() and first_char.isupper() and random.random() < lowercase_prob:
        cleaned = first_char.lower() + cleaned[1:]

    # Remove trailing period if present
    if cleaned.endswith(".") and not cleaned.endswith("...") and random.random() < strip_period_prob:
        if random.random() < 0.25:
            cleaned = cleaned[:-1] + "..."
        else:
            cleaned = cleaned[:-1]

    # Contractions replacement on non-link portions
    if random.random() < contractions_prob:
        parts = re.split(r"(https?://\S+)", cleaned)
        for i in range(len(parts)):
            if not parts[i].startswith("http"):
                parts[i] = re.sub(r"\bI think\b", "honestly", parts[i], count=1)
                parts[i] = re.sub(r"\bhowever\b", "tho", parts[i], count=1, flags=re.IGNORECASE)
        cleaned = "".join(parts)

    return cleaned.strip()


if __name__ == "__main__":
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    out = humanize_text(raw)
    print(json.dumps({"original": raw, "humanized": out}, ensure_ascii=False))
