# Project orientation for Claude Code

**Read [docs/specs/v0.3/00-overview.md](docs/specs/v0.3/00-overview.md) first.** It captures the v0.3 design in one page.

## What nidus is

A **curated, citation-backed, confidence-tier-annotated JSON dataset** of human gestational physiology parameters, distributed as a pure-Python package (`pip install nidus`) and browsable via a Streamlit dashboard.

The dataset is the centerpiece. Everything else (Python package, dashboard, optional SBML/CellML export) is a presentation layer.

## Scope decisions (locked in)

- **Pure Python.** No Rust, no PyO3, no compiled extensions. NumPy/SciPy is sufficient for everything the dashboard needs.
- **GitHub + PyPI + Streamlit Cloud are the canonical URLs.** No custom domain.
- **An essay in the repository** is the outreach vehicle. No academic methods paper.
- **Dataset-only scope.** No new mechanistic biology beyond the curated parameters.
- **The earlier Rust prototype is archived,** not deleted: see the `v0.2-archive` git tag.
- **The pre-v0.3 spec files** (`docs/specs/01-*.md` through `12-*.md`, `SPEC.md`, `SPEC_V0.2.md`) are one-paragraph deprecation stubs pointing to the v0.3 design. Their original content lives in git history.

## Where the work lives

| Path                                          | Status                                                              |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `docs/specs/v0.3/00-overview.md`              | **READ FIRST.** v0.3 design and rationale.                          |
| `docs/specs/v0.3/01-dataset-and-dashboard.md` | **Active.** Dataset + Python package + dashboard. Primary work.     |
| `docs/specs/v0.3/02-sbml-cellml-export.md`    | **Conditional.** SBML/CellML export — execute only on adoption.     |
| `docs/specs/v0.3/03-outreach-and-essay.md`    | **Active.** Blog essay outreach.                                    |
| `docs/specs/01-*.md` … `12-*.md`              | **Superseded.** Deprecation stubs pointing to the v0.3 design.      |
| `docs/specs/SPEC.md`, `SPEC_V0.2.md`          | **Superseded.** Deprecation stubs.                                  |
| `dataset/`                                    | The curated dataset. JSON, schema-validated, FAIR-compliant.        |
| `python/`                                     | The `nidus` package source. Pure Python.                            |
| `dashboard/`                                  | The Streamlit dashboard (scaffolded; pages land incrementally).     |
| `notebooks/`                                  | Reference notebooks (land alongside the dashboard).                 |
| `scripts/`                                    | One-off migration + maintenance scripts.                            |

## Audience and ethos

- Audience: ~hundreds of perinatal researchers globally. Almost all Python/R users.
- Solo maintainer. Scope matches.
- MIT for code, CC-BY-4.0 for the dataset. Forever free. No commercial intent.
- Be honest about scope and limits. Dishonesty about uncertainty turns a useful tool into a misleading one.
- Realistic best case: a handful of researchers cite the dataset; one publishes a hypothesis informed by it. That is success.

## When in doubt

- The dataset is the centerpiece.
- The audience wants something they can use today, not a heroic simulator.
- Honest scope > ambitious scope.
