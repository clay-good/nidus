# Nidus Dataset Changelog

The dataset uses semantic versioning, independent of the code.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Initial scaffold for the v0.3.0 dataset-first release.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `schema/`.
- Tier definitions in `tiers/tiers.json`.

### In progress
- Migration of curated parameters from the legacy `data/parameters/*.toml`
  files to schema-valid JSON under `parameters/`.
- Migration of citation index from the legacy `data/citations/` files
  to `citations/citations.json`.
