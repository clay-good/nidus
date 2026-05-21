# Contributing to Nidus

Nidus is a curated dataset of human gestational physiology parameters,
annotated with confidence tiers and peer-reviewed citations. The most
valuable contributions are **verified parameters drawn from published
empirical work**.

## Project status

The project is currently pivoting from an earlier Rust-simulator
architecture to a dataset-first form. Until `v0.3.0` ships, contribution
workflows are in flux. See
[docs/specs/v0.3-pivot/00-overview.md](docs/specs/v0.3-pivot/00-overview.md)
for the current direction and
[docs/specs/v0.3-pivot/01-dataset-and-dashboard.md](docs/specs/v0.3-pivot/01-dataset-and-dashboard.md)
for the work in progress.

If you want to contribute now, the most useful things are:

1. **Verify an existing citation** in `data/citations/` (or, once
   migrated, `dataset/citations/citations.json`) against the original
   paper.
2. **Identify a parameter** in the literature that fits the schema and
   is well-supported (Tier A or B), and propose it via an issue.
3. **Surface a Tier D candidate** — a hypothesised mechanism or channel
   that lacks quantitative literature.

## Confidence tiers

Every parameter carries one of four tiers:

| Tier | Meaning                                                                                  |
| ---- | ---------------------------------------------------------------------------------------- |
| A    | Well-established. 3+ independent studies, overlapping CIs, validated across populations. |
| B    | Supported. 1–2 longitudinal studies (n≥100), plausible mechanism.                        |
| C    | Provisional. Single study, or cross-sectional only, or small n.                          |
| D    | Unknown. Hypothesised; no quantitative literature.                                       |

Machine-readable definitions: [`dataset/tiers/tiers.json`](dataset/tiers/tiers.json).

## Verification standard

Every Tier A/B parameter must link to at least one citation with a DOI
or PMID, and the citation must be verified against the original paper
**by a human** (not an LLM). Verification means:

- The cited paper actually reports the claimed value.
- The cohort, gestational window, and units match the claim.
- The extraction is documented (table number, figure, page).

## Licence

- Code (Python package, dashboard, schemas-as-tooling, tests, notebooks):
  **MIT**. See [LICENSE](LICENSE).
- Dataset (parameter JSON, citation JSON, tier JSON, JSON-LD context):
  **CC-BY-4.0**. See [LICENSE-DATASET](LICENSE-DATASET).

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Contributors are expected
to follow it.

## Getting in touch

File an issue on GitHub. Issue templates may be out of date during the
pivot; describe what you have in plain prose and we'll work through it.
