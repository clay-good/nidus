# Nidus Changelog

This changelog covers the Python package, dashboard, and tooling. The
dataset has its own changelog at [`dataset/CHANGELOG.md`](dataset/CHANGELOG.md).

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- **v0.3 reframes nidus around its durable contribution.** Earlier
  Rust-prototype work (preserved at the `v0.2-archive` git tag)
  explored a coupled maternal-placental-fetal physiology engine. v0.3
  distils that exploration into the artefact that is actually
  transferable: a citation-verified, tier-annotated parameter dataset,
  distributed as `pip install nidus` with a Streamlit dashboard. The
  form factor matches the audience (biomedical researchers, almost all
  Python/R users); the maintenance scope matches what one person can
  sustain. See
  [`docs/specs/v0.3/00-overview.md`](docs/specs/v0.3/00-overview.md)
  for the design rationale.

### Removed
- The Rust prototype: `crates/`, `Cargo.toml`, `Cargo.lock`, `target/`,
  scenario configurations (`scenarios/`), examples (`examples/`),
  output artefacts (`out/`), and the implementation-progress tracker
  (`PROGRESS.md`). All recoverable from the `v0.2-archive` tag.

### Added
- Repository scaffold for the v0.3 design: `dataset/`, `python/`,
  `dashboard/`, `notebooks/`, `scripts/`.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `dataset/schema/`. JSON-LD context for FAIR linked-data consumption.
- Pure-Python `nidus` package: `nidus.load()`, `nidus.validate()`,
  dataclass models, schema validation, citation resolution, multi-axis
  filtering. Test suite of 36 cases covering load, filter, citations,
  and validation.
- 54 parameters across 10 subsystems, 32 citations migrated from the
  v0.2 curation into schema-valid JSON.
- GitHub Actions CI: lint (`ruff`), typecheck (`mypy --strict`), test
  matrix (Python 3.10/3.11/3.12), dataset validation, wheel + sdist
  build with smoke test of the installed wheel.
- Weekly citation-reachability cron with automated issue creation on
  failures.
- Release pipeline (PyPI Trusted Publishing + GitHub Releases) wired
  for tag-driven publishing.
- `CITATION.cff` and `LICENSE-DATASET` (CC-BY-4.0).
- `CLAUDE.md` at repo root to orient fresh Claude Code sessions.
