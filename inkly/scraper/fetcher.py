from __future__ import annotations

import requests
from bs4 import BeautifulSoup

# How long to wait for a page to respond before giving up.
REQUEST_TIMEOUT_SEC = 10

# Tags that contain visible documentation content.
# We skip nav, header, footer, and script tags as they contain UI noise.
CONTENT_TAGS = ["p", "li", "pre", "code", "h1", "h2", "h3", "h4"]


def fetch_page_text(url: str) -> str | None:
    """
    Fetch a URL and return its visible text content as a plain string.

    Steps:
    - Make an HTTP GET request with a browser-like User-Agent header
      (some sites block requests that look like bots)
    - Parse the HTML with BeautifulSoup
    - Extract text only from content-bearing tags
    - Return a single string with one line per extracted piece

    Returns None if the request fails or the page returns an error status.
    """
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT_SEC,
            headers={"User-Agent": "Mozilla/5.0 (research documentation scraper)"},
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style tags so their text doesn't pollute the output.
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    lines = []
    for tag in soup.find_all(CONTENT_TAGS):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            lines.append(text)

    return "\n".join(lines) if lines else None
