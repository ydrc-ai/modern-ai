"""Text extraction helpers for notes content."""

from __future__ import annotations

import re

HASHTAG_RE = re.compile(r"(?<!\w)#([A-Za-z][\w-]*)")
CHECKBOX_RE = re.compile(r"^[-*]\s+\[\s*\]\s+(.+)$")


def extract_hashtags(text: str) -> list[str]:
    """Return unique hashtags (without #), preserving first-seen order."""
    seen: set[str] = set()
    tags: list[str] = []
    for match in HASHTAG_RE.finditer(text or ""):
        tag = match.group(1).lower()
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def extract_action_items(text: str) -> list[str]:
    """
    Extract actionable lines from note text.

    Recognizes:
    - Markdown checkboxes: `- [ ] task text`
    - Legacy markers: lines starting with `TODO:` or ending with `!`
    """
    items: list[str] = []
    seen: set[str] = set()

    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue

        checkbox = CHECKBOX_RE.match(line)
        if checkbox:
            desc = checkbox.group(1).strip()
            if desc and desc not in seen:
                seen.add(desc)
                items.append(desc)
            continue

        stripped = re.sub(r"^[-*]\s+", "", line).strip()
        if stripped.lower().startswith("todo:"):
            if stripped not in seen:
                seen.add(stripped)
                items.append(stripped)
            continue

        if stripped.endswith("!") and not stripped.startswith("#"):
            if stripped not in seen:
                seen.add(stripped)
                items.append(stripped)

    return items
