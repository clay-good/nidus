#!/usr/bin/env python3
"""Repair wrong DOI / PMID identifiers in ``citations.json``.

Background
----------

A metadata audit (``verify_citation_metadata.py``) found that the
majority of citations in the v0.2 corpus carry DOI/PMID identifiers
that resolve to *different papers* than what the title and authors
describe. The titles and author lists themselves look correct (they
are descriptive, human-written), so the strategy is to search Crossref
by ``title + first-author family + year``, pick the highest-title-
similarity match, and propose it as the corrected DOI.

This script:

* For each citation whose stored DOI/PMID disagrees with the title,
  searches Crossref by ``query.bibliographic`` + ``query.author`` +
  publication-year filter.
* Scores each candidate by Jaccard similarity over title word-sets.
* Proposes the highest-scoring candidate above a configurable threshold.
* With ``--apply``, writes the proposed corrections back to
  ``citations.json`` (DOI replaced, stale PMID cleared if it disagreed,
  and the matched title used to canonicalise capitalisation).

Run
---

    python scripts/repair_citation_identifiers.py                  # dry-run
    python scripts/repair_citation_identifiers.py --apply           # write changes
    python scripts/repair_citation_identifiers.py --apply --threshold 0.55
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).parent.parent
CITATIONS = REPO / "dataset" / "citations" / "citations.json"

CROSSREF_BASE = "https://api.crossref.org/works"
USER_AGENT = (
    "nidus-citation-verifier/0.3 "
    "(+https://github.com/claygood/nidus; mailto:hi@claygood.com)"
)
TIMEOUT_SECONDS = 25
SLEEP_BETWEEN_CALLS = 0.3
SEARCH_ROWS = 8


_WS = re.compile(r"\s+")


def normalise(s: str) -> str:
    return _WS.sub(" ", (s or "").lower()).strip().rstrip(".,;:")


def family_name(author_str: str) -> str:
    s = (author_str or "").strip().rstrip(",")
    if not s:
        return ""
    if "," in s:
        return s.split(",", 1)[0].strip().lower()
    return s.split()[0].lower()


def jaccard(a: str, b: str) -> float:
    aw = set(normalise(a).split())
    bw = set(normalise(b).split())
    if not aw or not bw:
        return 0.0
    return len(aw & bw) / len(aw | bw)


def fetch_crossref_doi(doi: str) -> dict[str, Any] | None:
    try:
        r = requests.get(
            f"{CROSSREF_BASE}/{doi}",
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    try:
        return r.json().get("message")
    except ValueError:
        return None


def search_crossref(title: str, first_author: str, year: int) -> list[dict[str, Any]]:
    fam = family_name(first_author)
    params = {
        "query.bibliographic": title,
        "rows": SEARCH_ROWS,
        "filter": f"from-pub-date:{year - 1},until-pub-date:{year + 1}",
    }
    if fam:
        params["query.author"] = fam
    try:
        r = requests.get(
            CROSSREF_BASE,
            params=params,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException:
        return []
    if r.status_code != 200:
        return []
    try:
        return r.json().get("message", {}).get("items", [])
    except ValueError:
        return []


def current_doi_matches(citation: dict[str, Any]) -> bool:
    """Check whether the citation's current DOI resolves to a record whose
    title matches the citation's stored title (Jaccard >= 0.7)."""
    doi = citation.get("doi")
    if not doi:
        return False
    record = fetch_crossref_doi(doi)
    time.sleep(SLEEP_BETWEEN_CALLS)
    if not record:
        return False
    title_list = record.get("title") or [""]
    crossref_title = title_list[0] if title_list else ""
    return jaccard(citation["title"], crossref_title) >= 0.7


def best_candidate(citation: dict[str, Any], threshold: float) -> dict[str, Any] | None:
    title = citation["title"]
    first_author = citation["authors"][0] if citation.get("authors") else ""
    year = int(citation["year"])
    candidates = search_crossref(title, first_author, year)
    time.sleep(SLEEP_BETWEEN_CALLS)

    best: tuple[float, dict[str, Any]] | None = None
    for item in candidates:
        item_title = (item.get("title") or [""])[0] if item.get("title") else ""
        if not item_title:
            continue
        score = jaccard(title, item_title)
        if best is None or score > best[0]:
            best = (score, item)

    if best is None or best[0] < threshold:
        return None

    score, item = best
    issued = (item.get("issued") or {}).get("date-parts") or [[None]]
    cand_year = issued[0][0] if issued and issued[0] else None
    return {
        "doi": item.get("DOI"),
        "title": (item.get("title") or [""])[0],
        "year": cand_year,
        "journal": (item.get("container-title") or [""])[0]
        if item.get("container-title")
        else None,
        "authors": [
            f"{a.get('family', '')} {a.get('given', '') and a.get('given', '')[0]}".strip()
            for a in (item.get("author") or [])[:5]
        ],
        "score": score,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--apply", action="store_true", help="Write fixes to citations.json")
    p.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Minimum title Jaccard similarity to accept a candidate (default 0.5)",
    )
    p.add_argument(
        "--keys",
        nargs="*",
        default=None,
        help="Restrict to these citation keys (default: all)",
    )
    args = p.parse_args()

    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))
    selected_keys = sorted(args.keys) if args.keys else sorted(citations.keys())

    proposed: dict[str, dict[str, Any]] = {}
    no_candidate: list[str] = []
    already_correct: list[str] = []
    skipped_no_doi: list[str] = []

    for key in selected_keys:
        if key not in citations:
            print(f"WARN unknown citation key: {key}")
            continue
        c = citations[key]
        print(f"=== {key} ===")
        print(f"  stored title:  {c['title']!r}")
        print(f"  stored DOI:    {c.get('doi') or '(none)'}")
        print(f"  stored PMID:   {c.get('pmid') or '(none)'}")

        if not c.get("doi") and not c.get("pmid"):
            print("  SKIP — no DOI or PMID stored (book or pre-DOI reference)")
            skipped_no_doi.append(key)
            print()
            continue

        if c.get("doi") and current_doi_matches(c):
            print("  OK — current DOI resolves to a title that matches")
            already_correct.append(key)
            print()
            continue

        candidate = best_candidate(c, threshold=args.threshold)
        if candidate is None:
            print(f"  NO CANDIDATE found above Jaccard {args.threshold}")
            no_candidate.append(key)
        else:
            print(f"  PROPOSED:")
            print(f"    DOI:     {candidate['doi']}")
            print(f"    title:   {candidate['title']!r}")
            print(f"    year:    {candidate['year']}")
            print(f"    journal: {candidate['journal']}")
            print(f"    authors: {', '.join(candidate['authors'])}")
            print(f"    score:   {candidate['score']:.2f}")
            proposed[key] = candidate
        print()

    print("=" * 60)
    print(f"Selected:           {len(selected_keys)}")
    print(f"  already correct:  {len(already_correct)}")
    print(f"  no DOI/PMID:      {len(skipped_no_doi)}")
    print(f"  repair proposed:  {len(proposed)}")
    print(f"  no candidate:     {len(no_candidate)}")
    if no_candidate:
        print("\nCitations that need manual investigation:")
        for k in no_candidate:
            print(f"  - {k}")

    if args.apply and proposed:
        for key, cand in proposed.items():
            c = citations[key]
            c["doi"] = cand["doi"]
            # If the candidate match disagrees with the stored PMID,
            # clear the PMID — it likely also pointed to the wrong paper.
            if c.get("pmid"):
                del c["pmid"]
            # Use Crossref's canonical title (handles capitalisation).
            if cand["title"]:
                c["title"] = cand["title"]
            # Use Crossref's canonical journal (publishers normalise &amp; etc., undo it).
            if cand["journal"]:
                c["journal"] = cand["journal"].replace("&amp;", "&")
        CITATIONS.write_text(
            json.dumps(citations, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"\nApplied {len(proposed)} repair(s) to {CITATIONS.relative_to(REPO)}")

    return 0 if not no_candidate else 1


if __name__ == "__main__":
    raise SystemExit(main())
