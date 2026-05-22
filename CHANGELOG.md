# Nidus Changelog

This changelog covers the Python package, dashboard, and tooling. The
dataset has its own changelog at [`dataset/CHANGELOG.md`](dataset/CHANGELOG.md).

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Two new Phase A submodels** with full export support (SBML L3v2 +
  CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the registry to
  **13 submodels**:
  - `gfr_logistic_trajectory` — logistic maternal GFR rise from
    baseline (~100 mL/min) to plateau (~150 mL/min). Inputs from the
    Phase 1 maternal_renal expansion (baseline_gfr, gfr_ml_per_min,
    gfr_peak_week, gfr_logistic_rate). Conrad 2001 mechanistic
    citation.
  - `amniotic_fluid_volume_trajectory` — Gaussian-bump approximation
    to the Brace & Wolf 1989 (PMID 2782359) curve. Inputs from the
    new `amniotic_fluid` subsystem (peak, peak week, plus two added
    parameters: early baseline and Gaussian spread). Worst-input
    tier is C (the spread parameter); the submodel inherits Tier C
    in exported annotations.
- Reference-kernel functions `maternal_gfr_logistic` and
  `amniotic_fluid_volume` in `nidus.export.reference`, parametrised
  unit tests covering endpoint values and the Gaussian peak.
- Parametrised SBML + CellML test coverage extended to the two new
  submodels; `test_write_sbml_produces_all_files` and
  `test_write_cellml_both_versions` updated to assert ≥13 outputs.


- **Phase 1 + partial Phase 2 dataset expansion:** 70 → **138 parameters**
  across 13 subsystems (was 10). Three new subsystems land additively
  in the schema enum: `maternal_endocrine`, `placental_endocrine`,
  `amniotic_fluid`.
  - Fetal growth: full multi-week Hadlock/Buck Louis biometry — BPD,
    HC, AC, FL at 16/20/24/28/32/36/40w; EFW at 16/24/32w (+29 params).
  - Maternal cardiovascular: HR baseline + peak excess; stroke volume
    baseline + peak excess; SVR baseline + term (+6 params, but 4 net
    after de-duplication against shipped entries).
  - Maternal renal: baseline GFR, GFR peak week + logistic rate, RPF
    baseline/peak/peak-week, filtration fraction, osmolality + sodium
    drops, BUN at term (+10 params).
  - Maternal respiratory: baseline VT, baseline + term RR, baseline
    PaO₂, baseline arterial pH (+5 params).
  - **New `maternal_endocrine`:** cortisol baseline + term, free T4
    term, TSH T1 + term, prolactin, aldosterone, HOMA-IR baseline +
    term (+9 params).
  - **New `placental_endocrine`:** hCG peak + week + term, hPL term,
    progesterone term, estradiol term, estriol term (+7 params).
  - **New `amniotic_fluid`:** AFV peak + peak week + term + 20w
    anchor (+4 params).
- **18 new peer-reviewed citations** spanning the Phase 1 + 2 expansion
  (Conrad 2001, Dunlop 1981, Davison 1981, Pitkin 1979, Kline 2005,
  Larsson 2008, Carr 1981, Glinoer 1997, Tyson 1972, Wilson 1980,
  Catalano 1991, Cole 2010, Tulchinsky 1972, Handwerger 1991, Brace
  1989, Kiserud 2000, Rudolph 1985, Pildner von Steinburg 2013,
  Templeton & Kelman 1976). Total citations 33 → 51.
- **New spec `docs/specs/v0.4/04-exhaustive-parameter-catalog.md`:**
  the project's ceiling. Every parameter the project could honestly
  include given the literature within the declared scope (8–40 week
  human singleton, normal physiology), indexed by subsystem with
  status (`shipped` / `phase1` / `phase2` / `phase3`) and primary
  citation. ~210 parameters at saturation.
- **README rewrite:** adds a narrative on the three-genome negotiation
  in pregnancy (maternal/paternal/fetal evolutionary-conflict framing),
  the clinical consequences when it fails (PE, FGR, GDM, VTE, PPH),
  and why a calibrated parameter dataset is the load-bearing piece.
  Subsystems table extended to 13; submodel table extended with the
  five trajectories described in spec 03 (Phase A submodels remain
  catalogued; SBML/CellML builders are follow-on work tracked in
  [`docs/specs/v0.4/03-submodel-expansion-catalog.md`](docs/specs/v0.4/03-submodel-expansion-catalog.md)).
- `scripts/expand_v04.py` — one-shot, idempotent expansion script that
  produced this batch. Future Phase 2/3 batches follow the same
  pattern.

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
