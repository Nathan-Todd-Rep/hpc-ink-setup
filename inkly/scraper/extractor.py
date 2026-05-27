from __future__ import annotations

from inkly.scraper.sources import GAUSSIAN_KEYWORDS

# Maximum number of passages to keep from a single page.
# Keeps stored snippets focused and avoids flooding the plugin context.
MAX_PASSAGES_PER_SOURCE = 10

# Minimum number of characters a passage must have to be worth keeping.
# Filters out single-word headings and empty lines.
MIN_PASSAGE_LENGTH = 40


def extract_relevant_passages(text: str, keywords: list[str] | None = None) -> list[str]:
    """
    Extract passages from raw page text that contain at least one keyword.

    A passage is one line of text from the fetched page. Lines are kept if:
    - they are long enough to be meaningful
    - they contain at least one keyword (case-insensitive)

    Args:
        text: Raw text returned by fetch_page_text().
        keywords: List of keywords to filter by. Defaults to GAUSSIAN_KEYWORDS.

    Returns:
        A list of relevant passage strings, capped at MAX_PASSAGES_PER_SOURCE.
    """
    if keywords is None:
        keywords = GAUSSIAN_KEYWORDS

    lower_keywords = [kw.lower() for kw in keywords]
    passages = []

    for line in text.splitlines():
        stripped = line.strip()

        if len(stripped) < MIN_PASSAGE_LENGTH:
            continue

        lower_line = stripped.lower()
        if any(kw in lower_line for kw in lower_keywords):
            passages.append(stripped)

        if len(passages) >= MAX_PASSAGES_PER_SOURCE:
            break

    return passages
