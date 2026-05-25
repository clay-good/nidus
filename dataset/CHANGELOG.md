# Nidus Dataset Changelog

The dataset uses semantic versioning, independent of the code.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Phase 1 saturation completion (spec 04): 5 new parameters across 4
  subsystems, 2 new citations. Brings the dataset to **204 parameters
  / 60 citations** and closes out the spec-04 Phase 1 column.
  - `maternal_cardiovascular.heart_rate_peak_week` (Mahendru 2014).
  - `maternal_blood.d_dimer_term_ug_per_ml` (Kline 2005).
  - `maternal_renal.cumulative_sodium_retention_g` (Cheung 2013).
  - `placental_structure.placental_thickness_term_cm` (Hoddick 1985,
    new citation).
  - `placental_structure.cord_length_term_cm` (Naeye 1985, new
    citation).
- Initial scaffold for the v0.3.0 dataset-first release.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `schema/`.
- Tier definitions in `tiers/tiers.json`.

### In progress
- Migration of curated parameters from the legacy `data/parameters/*.toml`
  files to schema-valid JSON under `parameters/`.
- Migration of citation index from the legacy `data/citations/` files
  to `citations/citations.json`.
