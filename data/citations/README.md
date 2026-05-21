# Citation Index

This directory holds the canonical citation index for the Nidus
parameter database. Every Tier A or Tier B parameter shipped under
[`data/parameters/`](../parameters/) must reference an `id` that
resolves here.

## What a citation entry looks like

```toml
[[citation]]
id = "author-year-shortlabel"
authors = "Author Family I, Coauthor F"
title = "The exact title as published"
venue = "Journal or book"
year = 2014
doi = "10.xxxx/xxxx"      # one of doi or pmid is required for tier A/B
pmid = "12345678"
notes = "What this is used for. Dependents: list of parameter files."
```

The `id` is the stable handle. It is `kebab-case` and conventionally
encodes `<first-author>-<year>-<short-topic>`. The schema is enforced
by [`crates/nidus-data/src/schema.rs`](../../crates/nidus-data/src/schema.rs);
unknown fields are rejected.

## Adding a citation

1. **Read the source.** You must have personally read the paper or the
   relevant section of the book. Tier A/B citations require a verified
   numeric extraction; you may not cite a source that you only know from
   a secondary review.
2. **Record a stable identifier.** Use the PubMed `pmid` or the DOI.
   At least one is required for any citation that backs a Tier A or
   Tier B parameter.
3. **Write the `notes` field** to record which parameter files depend on
   this source. When a parameter graduates from one citation to a better
   one, this field is how reviewers find every dependent.
4. **Open a PR.** The PR template at
   [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)
   includes a citation checklist.

## How a reviewer verifies an entry

For each new citation:

1. Open the PDF or print of the original source.
2. For every parameter listed in the `notes` field, locate the
   numeric value in the source and confirm it matches the value used
   in the dependent TOML — within the source's own reported precision.
3. Confirm the population, technique, and age range stated in the
   parameter entry are consistent with the source.
4. Initial the PR review comment with `verified-by: <github-handle>`.

A citation is considered verified once the PR carries at least one
such initialled review comment.

## Tier-promotion record

When a parameter changes tier (e.g. a Tier C scaffold value is replaced
by a Tier B literature-derived value), the PR description must:

- State the previous tier and the new tier.
- Cite the new source.
- Reference any validation cases that exercise the parameter.
- Be reviewed by at least one reviewer other than the author.

The tier-promotion log lives at
[`docs/contributing/parameter-pull-requests.md`](../../docs/contributing/parameter-pull-requests.md);
add an entry there as part of any promotion PR.
