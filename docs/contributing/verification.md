# The verification standard

Every Tier A and Tier B parameter in nidus must link to at least one citation with a DOI or PMID, and the citation must be **verified against the original paper by a human** — not by an LLM, not from a downstream review article, not from a Wikipedia summary.

This is the single most important rule in the project.

## What "verified" means

- The cited paper actually reports the claimed value (or its uncertainty range).
- The cohort, gestational window, and units match the claim.
- The extraction method is documented (`extraction.method`): which table, which figure, which column, which row.
- A human has read the relevant section of the paper.

If any of these are not true, the record stays `unverified` (or
`pending_human_review`) until they are.

## The four review states

| `review_status` | Meaning |
| --------------- | ------- |
| `unverified` | Illustrative central value from the literature; the source has not been confirmed against the entry. |
| `pending_human_review` | Automated review located the stored value in a real source and attached a verbatim quote (`extraction.source_check`), but **no human has signed off**. Sourced, not verified. |
| `verified` | A human read the source and confirmed the value. Only a human sets this. |
| `contested` | Flagged for investigation — e.g. the source appears to disagree with the stored value. |

`pending_human_review` exists so a machine can fill records from real sources
without ever claiming human verification. Promoting one to `verified` is the
fast path: the quote is already on the record (and ranked in the
[review queue](https://github.com/clay-good/nidus/blob/main/data/validation/REVIEW_QUEUE.md))
— you just confirm it against the source.

## Where to start: the machine pre-verification queue

You do not have to start from a blank page. The repository ships a
**machine pre-verification** layer at [`data/validation/`](https://github.com/clay-good/nidus/tree/main/data/validation)
that has already fetched each parameter's source (open-access full text where
available, otherwise the abstract) and compared it to the stored value, with a
verbatim supporting quote.

Open [`data/validation/REVIEW_QUEUE.md`](https://github.com/clay-good/nidus/blob/main/data/validation/REVIEW_QUEUE.md)
and work top-down: parameters the machine flagged as a likely **mismatch**
(a wrong value is worse than an unverified one), then the `close` and `match`
candidates where a quote already supports the value, then the `not_found` /
`source_unavailable` ones that need the full PDF or a library copy.

This is a worklist, not a verdict — the machine never sets `review_status`.
You still read the source and make the call. See
[`data/validation/README.md`](https://github.com/clay-good/nidus/blob/main/data/validation/README.md)
for how the layer is built and what each verdict means.

## The verification workflow

1. Pick a parameter currently marked `extraction.review_status: "unverified"` (the [review queue](https://github.com/clay-good/nidus/blob/main/data/validation/REVIEW_QUEUE.md) ranks these for you).
2. Open the cited paper. Try the DOI first; fall back to the PMID; fall back to the author–title–year lookup if neither resolves.
3. Find the value in the paper.
4. Cross-check:

      - Units match what the dataset records.
      - Cohort matches what `applicability.population` says (or update `applicability.population` to match).
      - Gestational window matches.
      - Distribution type makes sense for what the paper reports (mean ± SD ⇒ `normal`; geometric mean ⇒ `lognormal`; etc.).
      - `value.central` is what the paper reports.
      - `value.low` / `value.high` correspond to the right CI level (`ci` field) — most v0.3 entries use 1σ.

5. Update the record:

      - Set `extraction.review_status` to `"verified"`.
      - Set `extraction.reviewer` to your name / handle.
      - Set `extraction.date` to today (ISO format).
      - Fix any extraction inaccuracies you find (this is half the point of verification).
      - Rewrite `tier_rationale` if the placeholder no longer reflects the evidence base.

6. Run `nidus.validate()` and `pytest python/tests/`. Open a PR.

## Citation-only contributions

A useful smaller contribution: add a new citation to `dataset/citations/citations.json` even before any parameter uses it. The schema accepts orphan citations; they become available for future parameter PRs to reference without re-typing the bibliographic metadata.

## When verification finds a discrepancy

If you read the cited paper and find the dataset value is wrong:

- **Small numerical correction** (typo, rounding): fix it in the same PR.
- **Larger disagreement** (the paper doesn't actually support the claim): open an issue with the citation, the dataset record, and a quote from the paper. Mark the record `extraction.review_status: "contested"` while the issue is open. Tier deflation usually follows.

Contested entries stay in the dataset (documented dissent is more useful than hidden silence) but with an honest status flag.

## What we will not accept

- "I read a review article that said this." Read the primary source.
- "An LLM extracted this for me." Tools can help find a paper; humans verify the value.
- "It's in the Wikipedia article on pregnancy physiology." That's not a primary source.
- Values from preprints unless you flag them as preprints and tier them conservatively.

## Why this matters

The tier system is the most rare and intellectually honest thing about nidus. It is also fragile: a single Tier-A parameter that turns out to be unverified poisons the credibility of every downstream computation that uses it.

If verification feels slow, it should. That is the standard.
