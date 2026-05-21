# Nidus Changelog

This changelog covers the Python package, dashboard, and tooling. The
dataset has its own changelog at [`dataset/CHANGELOG.md`](dataset/CHANGELOG.md).

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- **Major direction change.** Nidus has pivoted from a Rust simulator
  of coupled maternal-placental-fetal physiology to a dataset-first
  form: a curated JSON dataset distributed as a `pip install nidus`
  Python package with a Streamlit dashboard. See
  [`docs/specs/v0.3-pivot/00-overview.md`](docs/specs/v0.3-pivot/00-overview.md)
  for the rationale.

### Removed
- Rust simulator (`crates/`, `Cargo.toml`, `Cargo.lock`, `target/`),
  simulator-era scenario configurations (`scenarios/`), examples
  (`examples/`), output artefacts (`out/`), and the
  implementation-progress tracker (`PROGRESS.md`). All recoverable from
  the `v0.2-archive` git tag.

### Added
- Repository scaffold for the dataset-first pivot: `dataset/`,
  `python/`, `dashboard/`, `notebooks/`.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `dataset/schema/`.
- `CITATION.cff` and `LICENSE-DATASET` (CC-BY-4.0).
- `CLAUDE.md` at repo root to orient fresh Claude Code sessions.
