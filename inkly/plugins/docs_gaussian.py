from __future__ import annotations

import json
from pathlib import Path

from inkly.plugins.common import format_plugin_output, validate_plugin_meta
from inkly.plugins.docs_data import DOC_SNIPPETS

# Path where the scraper saves its output.
SCRAPED_DOCS_PATH = Path.home() / ".inkly" / "gaussian_docs.json"

PLUGIN_META = {
    "name": "docs_gaussian",
    "description": (
        "Provides documentation snippets and usage guidance for Gaussian and related "
        "cluster software workflows, including scheduler-oriented usage notes."
    ),
    "category": "documentation",
    "example_queries": [
        "How do I run Gaussian on this cluster?",
        "Show me Gaussian job examples.",
        "What documentation exists for Gaussian jobs?",
        "How should I request resources for Gaussian?",
    ],
}

validate_plugin_meta(PLUGIN_META)


def _load_scraped_passages() -> list[str]:
    """
    Load passages from the scraped JSON file if it exists.

    Returns a flat list of passage strings across all scraped sources,
    or an empty list if the file is missing or unreadable.
    """
    if not SCRAPED_DOCS_PATH.exists():
        return []

    try:
        data = json.loads(SCRAPED_DOCS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    passages = []
    for source in data:
        label = source.get("label", "Unknown source")
        source_passages = source.get("passages", [])
        if source_passages:
            # Prefix the first passage with the source label so the LLM
            # knows where the information came from.
            passages.append(f"[{label}]")
            passages.extend(source_passages)

    return passages


def run() -> str:
    """
    Entry point for the Gaussian documentation plugin.

    Load order:
    1. Try scraped data from ~/.inkly/gaussian_docs.json
    2. Fall back to static snippets in docs_data.py
    3. If neither has content, return a fallback message
    """
    # Try scraped data first — richer and more up to date.
    passages = _load_scraped_passages()

    if passages:
        return format_plugin_output("Gaussian Documentation", passages)

    # Fall back to the static snippets shipped with the project.
    lines = DOC_SNIPPETS.get("gaussian", [])

    if not lines:
        return format_plugin_output(
            "Gaussian Documentation Snippets",
            ["Gaussian documentation snippets are unavailable."],
        )

    title = lines[0]
    body = lines[1:]
    return format_plugin_output(title, body)
