from __future__ import annotations

from inkly.scraper import extractor, fetcher
from inkly.scraper.extractor import extract_relevant_passages
from inkly.scraper.fetcher import fetch_page_text


# --- extractor tests ---

def test_extract_returns_passages_containing_keywords():
    text = "\n".join([
        "Load the Gaussian module before submitting your job.",
        "This line has nothing relevant in it at all and is long enough.",
        "Use %mem and %nproc in your Gaussian input file to request resources.",
        "Another irrelevant line that contains no matching keywords whatsoever.",
    ])

    results = extract_relevant_passages(text, keywords=["gaussian", "%mem"])

    assert any("Gaussian" in p for p in results)
    assert any("%mem" in p for p in results)


def test_extract_ignores_short_lines():
    text = "\n".join([
        "Gaussian",              # too short
        "g16",                   # too short
        "Use Gaussian 16 with the appropriate memory settings in your Slurm script.",
    ])

    results = extract_relevant_passages(text, keywords=["gaussian", "g16"])

    assert len(results) == 1
    assert "Use Gaussian 16" in results[0]


def test_extract_returns_empty_when_no_matches():
    text = "\n".join([
        "This documentation page is about a completely unrelated topic.",
        "There are no chemistry keywords anywhere in this passage at all.",
    ])

    results = extract_relevant_passages(text, keywords=["gaussian", "g16"])

    assert results == []


def test_extract_caps_results_at_max_passages(monkeypatch):
    monkeypatch.setattr(extractor, "MAX_PASSAGES_PER_SOURCE", 3)

    # Build more lines than the cap allows.
    lines = [
        f"Use Gaussian with nproc and mem settings for job number {i}."
        for i in range(10)
    ]
    text = "\n".join(lines)

    results = extract_relevant_passages(text, keywords=["gaussian"])

    assert len(results) == 3


# --- fetcher tests ---

def test_fetch_returns_none_on_request_error(monkeypatch):
    import requests

    def fake_get(*args, **kwargs):
        raise requests.RequestException("connection refused")

    monkeypatch.setattr(requests, "get", fake_get)

    result = fetch_page_text("http://fake-url.example.com")

    assert result is None


def test_fetch_returns_none_on_non_200_status(monkeypatch):
    import requests
    from types import SimpleNamespace

    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **kw: SimpleNamespace(status_code=404, text=""),
    )

    result = fetch_page_text("http://fake-url.example.com")

    assert result is None


def test_fetch_extracts_text_from_html(monkeypatch):
    import requests
    from types import SimpleNamespace

    fake_html = """
    <html>
      <body>
        <nav>Skip this nav content</nav>
        <p>Load the Gaussian module before submitting your job.</p>
        <li>Request memory carefully in your Slurm script.</li>
        <footer>Skip this footer</footer>
      </body>
    </html>
    """

    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **kw: SimpleNamespace(status_code=200, text=fake_html),
    )

    result = fetch_page_text("http://fake-url.example.com")

    assert result is not None
    assert "Load the Gaussian module" in result
    assert "Request memory carefully" in result
    assert "Skip this nav content" not in result
    assert "Skip this footer" not in result
