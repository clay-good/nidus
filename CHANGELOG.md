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
- `nidus` console-script entry point (`nidus version`, `nidus validate`,
  `nidus info`, `nidus export --format csv|bibtex`).
- Reference notebooks (5) embedded as docs pages via mkdocs-jupyter.
- Auto-generated API reference via mkdocstrings.
- `docs/about/essay.md` — "Confidence tiers for pregnancy physiology",
  ~2,500 words, with three seeded figures committed under
  `docs/assets/essay/`.
- Citation audit + repair tooling:
  `scripts/verify_citation_metadata.py` cross-checks every citation
  against Crossref / PubMed publisher records;
  `scripts/repair_citation_identifiers.py` finds the correct DOI for
  any citation whose stored identifier resolves to the wrong paper.

### Data integrity (this release)

- 22 of 30 citations in the original v0.2 corpus had DOI/PMID
  identifiers pointing to the wrong papers. Crossref-search-and-replace
  repaired all of them; the corpus now passes the metadata audit
  cleanly (30/30 with identifiers; 2 books legitimately have none).
- 23 additional PMIDs added via NCBI IdConverter / EPMC lookups.
- Six papers (the PMC-accessible subset) were read at the abstract or
  table level. Five parameters were promoted to
  `extraction.review_status: "verified"` based on direct confirmation:
  `maternal_blood.plasma_volume_l` (de Haas 2017 meta-analysis pooled
  +1.13 L third-trimester rise), `maternal_blood.plasma_volume_early_l`
  (Bernstein 2001 2.32 L at 12 weeks), `maternal_blood.o2_hb_p50_maternal`
  (Severinghaus 1979 Eq. 4 explicit P50=26.6 mmHg),
  `maternal_respiratory.paco2_mmhg_term` (LoMauro 2015 plateau at 32),
  `maternal_respiratory.pao2_mmhg_term` (LoMauro 2015 third-trimester
  range 101-104).
- One parameter promoted to `contested`:
  `maternal_cardiovascular.baseline_uterine_flow_ml_per_min` —
  Thaler 1990's pre-pregnancy bilateral estimate (~189 mL/min) is
  meaningfully larger than the dataset's stored 50 mL/min, needs
  human investigation.
- Two more parameters carry `notes` flagging discrepancies for human
  re-investigation: `peak_excess_cardiac_output_l_per_min` (Mahendru
  2014 abstract's 0.6 L/min tension with the dataset's 2.7), and the
  four `efw_*_g` records (Hadlock 1991 ±12.7% CV pattern is closer to
  the dataset than Buck Louis 2015's racial-percentile values —
  primary citation may have been mis-attributed in v0.2).
- All 31 placeholder `tier_rationale` fields rewritten with
  substantive evidence from the verified citation abstracts.
- 100% test coverage of `nidus.validate`; total package coverage 95%.
