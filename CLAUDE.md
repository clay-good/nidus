# Project orientation for Claude Code

**Read [docs/specs/v0.3-pivot/00-overview.md](docs/specs/v0.3-pivot/00-overview.md) first.** It captures the current direction in one page.

## What nidus is being pivoted into

A **curated, citation-backed, confidence-tier-annotated JSON dataset** of human gestational physiology parameters, distributed as a Python package (`pip install nidus`) with a Streamlit dashboard on top.

The dataset is the centerpiece. Everything else is a presentation layer.

## What is NOT being done (locked-in decisions)

- **The Rust simulator is being deleted, not maintained.** `crates/`, `Cargo.toml`, `Cargo.lock`, `target/` are removed in step 1 of the pivot. Git history preserves them; no archive branch.
- **No PyO3 kernel.** NumPy/SciPy handles everything the dashboard needs.
- **No custom domain.** GitHub + PyPI + Streamlit Cloud are the canonical URLs.
- **No academic methods paper.** A blog essay on claygood.com replaces it.
- **No new biology beyond the existing curated parameters.** Dataset-only scope.
- **The old specs are deprecated.** Files `docs/specs/01-*.md` through `docs/specs/12-*.md`, `docs/specs/SPEC.md`, and `docs/specs/SPEC_V0.2.md` are deprecation stubs. Original content is in git history.

## Where the work lives

| Path                                  | Status                                                                |
| ------------------------------------- | --------------------------------------------------------------------- |
| `docs/specs/v0.3-pivot/00-overview.md`| **READ FIRST.** Current direction and rationale.                      |
| `docs/specs/v0.3-pivot/01-...md`      | **Active.** Dataset + Python package + dashboard. The primary work.   |
| `docs/specs/v0.3-pivot/02-...md`      | **Conditional.** SBML/CellML export — only if Spec 01 sees adoption.  |
| `docs/specs/v0.3-pivot/03-...md`      | **Active.** Blog essay outreach.                                      |
| `docs/specs/01-*.md` ... `12-*.md`    | **NOT DOING.** Deprecation stubs.                                     |
| `docs/specs/SPEC.md`, `SPEC_V0.2.md`  | **NOT DOING.** Deprecation stubs.                                     |
| `crates/`, `Cargo.*`, `target/`       | **TO BE DELETED.** Pending pivot step 1.                              |

## Audience and ethos

- Audience: ~hundreds of perinatal researchers globally. Almost all Python/R users.
- Solo maintainer. Scope must match.
- MIT for code, CC-BY-4.0 for the dataset. Forever free. No commercial intent.
- Be honest about scope and limits. Dishonesty about uncertainty turns a useful tool into a misleading one.

## When in doubt

- The dataset is the centerpiece.
- The audience wants a tool they can use today, not a heroic simulator.
- Realistic best case: a handful of researchers cite the dataset; one publishes a hypothesis informed by it. That is success.
