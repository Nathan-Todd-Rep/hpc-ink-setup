#!/usr/bin/env python3
"""
Scrape Gaussian documentation from curated HPC sources and save to
~/.inkly/gaussian_docs.json.

Run this script to refresh the data the docs_gaussian plugin uses:

    py scripts/scrape_gaussian_docs.py

The output file is read by inkly/plugins/docs_gaussian.py at runtime.
If this script has never been run, the plugin falls back to the static
snippets in inkly/plugins/docs_data.py.
"""
from __future__ import annotations

import json
from pathlib import Path

from inkly.scraper.extractor import extract_relevant_passages
from inkly.scraper.fetcher import fetch_page_text
from inkly.scraper.sources import GAUSSIAN_SOURCES

OUTPUT_PATH = Path.home() / ".inkly" / "gaussian_docs.json"


def scrape_all_sources() -> list[dict]:
    """
    Scrape all configured sources and return a list of result records.

    Each record contains:
    - label: human-readable name of the source
    - url: the page that was scraped
    - passages: list of relevant text passages extracted from that page
    """
    results = []

    for source in GAUSSIAN_SOURCES:
        label = source["label"]
        url = source["url"]

        print(f"Fetching: {label}")
        print(f"  URL: {url}")

        text = fetch_page_text(url)

        if text is None:
            print(f"  SKIPPED — could not fetch page")
            continue

        passages = extract_relevant_passages(text)

        if not passages:
            print(f"  SKIPPED — no relevant passages found")
            continue

        print(f"  OK — {len(passages)} passages extracted")
        results.append({
            "label": label,
            "url": url,
            "passages": passages,
        })

    return results


def save_results(results: list[dict]) -> None:
    """
    Save scraped results to the output JSON file.
    Creates the ~/.inkly directory if it doesn't exist yet.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )
    print(f"\nSaved {len(results)} sources to {OUTPUT_PATH}")


if __name__ == "__main__":
    print("=== Gaussian Docs Scraper ===\n")
    results = scrape_all_sources()

    if not results:
        print("\nNo results collected. Check network access or source URLs.")
    else:
        save_results(results)
        total_passages = sum(len(r["passages"]) for r in results)
        print(f"Total passages collected: {total_passages}")
