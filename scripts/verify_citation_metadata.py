#!/usr/bin/env python3
"""Verify citation metadata in ``dataset/citations/citations.json`` against
authoritative publisher records (Crossref for DOIs, PubMed E-utilities
for PMID-only entries).

What this script does
---------------------

* Fetches the Crossref record for every citation with a ``doi`` field.
* For citations with a ``pmid`` but no ``doi``, fetches the PubMed
  E-utilities summary.
* Compares the local ``title``, ``authors`` (first-author family name),
  ``year``, and ``journal`` against the publisher record.
* Prints a per-citation report with any discrepancies.
* With ``--apply-safe-fixes``, applies trivially-safe corrections to
  ``citations.json``: matched-but-different-capitalisation titles and
  journals, trailing-period normalisation. Non-trivial mismatches are
  always flagged for human review, never auto-applied.

What this script does NOT do
----------------------------

This script verifies that the *bibliographic record* matches the
publisher. It does NOT verify that the *parameter value* a record
supports matches what the paper actually reports. That requires a
human reading the paper PDF; see ``docs/contributing/verification.md``.

A clean run of this script is necessary but not sufficient for tier
A/B promotion.

Run
---

    python scripts/verify_citation_metadata.py             # report only
    python scripts/verify_citation_metadata.py --apply-safe-fixes

Exit code 0 = no metadata discrepancies; non-zero = flagged for review.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).parent.parent
CITATIONS = REPO / "dataset" / "citations" / "citations.json"

CROSSREF_BASE = "https://api.crossref.org/works"
PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
USER_AGENT = (
    "nidus-citation-verifier/0.3 "
    "(+https://github.com/clay-good/nidus; mailto:hi@claygood.com)"
)
TIMEOUT_SECONDS = 25
SLEEP_BETWEEN_CALLS = 0.25  # polite-pool friendly


# ---- API calls ------------------------------------------------------


def fetch_crossref(doi: str) -> dict[str, Any] | None:
    try:
        r = requests.get(
            f"{CROSSREF_BASE}/{doi}",
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as e:
        return {"_error": f"network: {e}"}
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        return {"_error": f"HTTP {r.status_code}"}
    try:
        return r.json()["message"]
    except (ValueError, KeyError) as e:
        return {"_error": f"parse: {e}"}


def fetch_pubmed(pmid: str) -> dict[str, Any] | None:
    try:
        r = requests.get(
            PUBMED_BASE,
            params={"db": "pubmed", "id": str(pmid), "retmode": "json"},
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as e:
        return {"_error": f"network: {e}"}
    if r.status_code != 200:
        return {"_error": f"HTTP {r.status_code}"}
    try:
        data = r.json()
    except ValueError as e:
        return {"_error": f"parse: {e}"}
    item = data.get("result", {}).get(str(pmid))
    if not item or "error" in item:
        return None
    return item


# ---- Normalisation --------------------------------------------------


_WS = re.compile(r"\s+")


def normalise(text: str) -> str:
    """Lowercase + collapse whitespace + strip trailing punctuation.

    Also decodes HTML entities (Crossref returns ``&amp;`` for ``&``) and
    canonicalises en-dash/em-dash to ASCII hyphen, since those are
    common cosmetic differences that should not surface as discrepancies.
    """
    if not text:
        return ""
    out = html.unescape(text).lower()
    out = out.replace("–", "-").replace("—", "-")  # en/em dash -> hyphen
    out = _WS.sub(" ", out).strip()
    return out.rstrip(".,;:")


def family_name(author_str: str) -> str:
    """Best-effort family-name extraction from an 'Family GI' style string.

    Handles compound surnames separated by spaces (e.g. "Buck Louis GM" or
    "de Haas S") by greedily consuming title-cased / lowercase tokens
    until an all-caps initials token is reached.
    """
    s = author_str.strip().rstrip(",")
    if not s:
        return ""
    if "," in s:
        return _WS.sub(" ", s.split(",", 1)[0].strip()).lower()
    tokens = s.split()
    family_tokens: list[str] = []
    for tok in tokens:
        # If a token is short uppercase (e.g. "AA", "GM"), treat as initials.
        if len(tok) <= 3 and tok.isupper():
            break
        family_tokens.append(tok)
    return " ".join(family_tokens).lower() or tokens[0].lower()


# ---- Comparison -----------------------------------------------------


def compare_crossref(
    local: dict[str, Any], cr: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    """Compare local record against Crossref. Return (issues, safe_fixes)."""
    issues: list[str] = []
    fixes: dict[str, str] = {}

    # Title
    cr_titles = cr.get("title") or [""]
    cr_title = cr_titles[0] if cr_titles else ""
    if cr_title and normalise(local["title"]) != normalise(cr_title):
        issues.append(
            f"title differs:\n      local:    {local['title']!r}\n      crossref: {cr_title!r}"
        )
    elif cr_title and local["title"] != cr_title:
        # Same when normalised; differs only in casing/punctuation. Safe fix.
        fixes["title"] = cr_title

    # Year
    cr_year = None
    for k in ("published-print", "published-online", "issued", "created"):
        d = (cr.get(k) or {}).get("date-parts") or []
        if d and d[0]:
            cr_year = int(d[0][0])
            break
    if cr_year is not None and int(local["year"]) != cr_year:
        issues.append(f"year differs: local={local['year']}, crossref={cr_year}")

    # First-author family name
    if local.get("authors"):
        local_first = family_name(local["authors"][0])
        cr_authors = cr.get("author", [])
        if cr_authors:
            cr_first_raw = cr_authors[0].get("family") or ""
            cr_first = _WS.sub(" ", cr_first_raw).lower().strip()
            if local_first and cr_first and local_first != cr_first:
                cr_given = cr_authors[0].get("given") or ""
                issues.append(
                    f"first author differs: local={local['authors'][0]!r}, "
                    f"crossref={cr_authors[0].get('family')!r} {cr_given!r}"
                )

    # Journal / container-title
    cr_journal = (
        (cr.get("container-title") or [""])[0] if cr.get("container-title") else ""
    )
    if local.get("journal") and cr_journal:
        if normalise(local["journal"]) != normalise(cr_journal):
            issues.append(
                f"journal differs:\n      local:    {local['journal']!r}\n"
                f"      crossref: {cr_journal!r}"
            )
        elif local["journal"] != cr_journal:
            fixes["journal"] = cr_journal

    return issues, fixes


def compare_pubmed(
    local: dict[str, Any], pm: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    issues: list[str] = []
    fixes: dict[str, str] = {}

    pm_title = (pm.get("title") or "").rstrip(".")
    if pm_title and normalise(local["title"]) != normalise(pm_title):
        issues.append(
            f"title differs:\n      local:   {local['title']!r}\n      pubmed:  {pm_title!r}"
        )

    pm_year = None
    pubdate = pm.get("pubdate") or ""
    m = re.match(r"^(\d{4})", pubdate)
    if m:
        pm_year = int(m.group(1))
    if pm_year and int(local["year"]) != pm_year:
        issues.append(f"year differs: local={local['year']}, pubmed={pm_year}")

    pm_authors = pm.get("authors") or []
    if local.get("authors") and pm_authors:
        local_first = family_name(local["authors"][0])
        pm_first = (pm_authors[0].get("name") or "").split()[0].lower()
        if local_first and pm_first and local_first != pm_first:
            issues.append(
                f"first author differs: local={local['authors'][0]!r}, "
                f"pubmed={pm_authors[0].get('name')!r}"
            )

    return issues, fixes


# ---- Main -----------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument(
        "--apply-safe-fixes",
        action="store_true",
        help="Apply trivially-safe corrections (capitalisation, punctuation) to citations.json",
    )
    args = p.parse_args()

    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))
    keys = sorted(citations.keys())

    n_checked = 0
    n_skipped = 0
    n_ok = 0
    n_issues = 0
    n_unresolved = 0
    total_fixes: dict[str, dict[str, str]] = {}

    for key in keys:
        c = citations[key]
        if c.get("doi"):
            cr = fetch_crossref(c["doi"])
            time.sleep(SLEEP_BETWEEN_CALLS)
            source = "Crossref"
        elif c.get("pmid"):
            cr = fetch_pubmed(str(c["pmid"]))
            time.sleep(SLEEP_BETWEEN_CALLS)
            source = "PubMed"
        else:
            n_skipped += 1
            print(f"SKIP {key}  no DOI/PMID  type={c.get('type', '?')}")
            continue

        n_checked += 1

        if cr is None:
            n_unresolved += 1
            ident = c.get("doi") or f"PMID:{c.get('pmid')}"
            print(f"FAIL {key}  {source} did not resolve ({ident})")
            continue
        if "_error" in cr:
            n_unresolved += 1
            print(f"FAIL {key}  {source} error: {cr['_error']}")
            continue

        if source == "Crossref":
            issues, fixes = compare_crossref(c, cr)
        else:
            issues, fixes = compare_pubmed(c, cr)

        if not issues and not fixes:
            n_ok += 1
            print(f"OK   {key}  ({source})")
        elif not issues and fixes:
            print(f"OK*  {key}  ({source}, {len(fixes)} safe fix(es) available)")
            n_ok += 1
            total_fixes[key] = fixes
        else:
            n_issues += 1
            print(f"FLAG {key}  ({source})")
            for issue in issues:
                print(f"  - {issue}")
            if fixes:
                print(f"  + {len(fixes)} safe fix(es) also available")
                total_fixes[key] = fixes

    # Summary
    print()
    print("=" * 60)
    print(f"Total citations:       {len(citations)}")
    print(f"  with DOI/PMID:       {n_checked}")
    print(f"  without identifier:  {n_skipped}")
    print(f"  OK against record:   {n_ok}")
    print(f"  flagged for review:  {n_issues}")
    print(f"  unresolved:          {n_unresolved}")
    print(f"  safe fixes pending:  {sum(len(v) for v in total_fixes.values())}")

    # Apply fixes if requested
    if args.apply_safe_fixes and total_fixes:
        for key, fixes in total_fixes.items():
            for field, value in fixes.items():
                citations[key][field] = value
        CITATIONS.write_text(
            json.dumps(citations, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print()
        print(
            f"Applied {sum(len(v) for v in total_fixes.values())} safe fix(es) "
            f"to {len(total_fixes)} citation(s) in {CITATIONS.relative_to(REPO)}"
        )
    elif total_fixes and not args.apply_safe_fixes:
        print()
        print("Re-run with --apply-safe-fixes to write the safe fixes above.")

    return 0 if (n_issues + n_unresolved) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
