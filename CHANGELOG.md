# Nidus Changelog

This changelog covers the Python package, dashboard, and tooling. The
dataset has its own changelog at [`dataset/CHANGELOG.md`](dataset/CHANGELOG.md).

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Three more Phase B submodels** (fetal Doppler PI cluster),
  bringing the registry to **36 submodels** and Phase B to **9 of 10**:
  - `umbilical_artery_pi_trajectory` — sigmoidal UA-PI fall from
    ~1.5 at 16 weeks to ~0.85 at term as placental vascular
    resistance drops (Acharya 2005, PMID 15776417).
  - `mca_pi_trajectory` — Gaussian bell with mid-pregnancy peak
    (~2.0 at ~28 weeks), reflecting fetal cerebral vasodilation
    dynamics (Mari 1995, PMID 7900181). Peak week + spread are
    hardcoded.
  - `cerebroplacental_ratio` — derived CPR(t) = MCA-PI(t) / UA-PI(t).
    Normal pregnancies: CPR > 1; CPR < 1 flags fetal compromise
    (Baschat 2003). Reuses the four PI parameters above.
- **Four new dataset parameters** (146 → **150 parameters**), all
  in `fetal_circulation`:
  - `ua_pi_baseline` (Tier A, Acharya 2005)
  - `ua_pi_term` (Tier A, Acharya 2005)
  - `mca_pi_baseline` (Tier B, Mari 1995)
  - `mca_pi_peak` (Tier B, Mari 1995)
- Two new citations in `citations.json`: `acharya-2005-umbilical-pi`,
  `mari-1995-mca-pi`. Citation count 51 → 53.
- Reference kernels `umbilical_artery_pi`, `mca_pi`,
  `cerebroplacental_ratio` with endpoint + shape sanity tests. The
  CPR test asserts CPR > 1 across normal-pregnancy timepoints.

- **Three more Phase B submodels**, bringing the registry to
  **33 submodels** and Phase B to **8 of 10**:
  - `estradiol_trajectory` — sigmoidal estradiol rise from mid-luteal
    baseline (~0.1 ng/mL) to term (~14 ng/mL); ~100x rise driven by
    placental aromatisation. Tulchinsky 1972 / O'Leary 1991.
  - `fetal_heart_rate_trajectory` — sigmoidal FHR fall from T1 peak
    (~170 bpm) to term (~140 bpm) as parasympathetic tone develops.
    The same baseline → term sigmoid form encodes the fall because
    `(term - baseline)` is negative. Pildner von Steinburg 2013
    (PMID 23740338).
  - `hcg_trajectory` — first non-sigmoidal Phase B submodel:
    piecewise quadratic rise from zero to peak by `hcg_peak_week`,
    then exponential decline to `hcg_term` at week 40. The decline
    rate is fit at build time so the curve passes exactly through
    the curated peak and term values. Cole 2010 (PMID 20089136).
- **Three new dataset parameters** (143 → **146 parameters**), all
  Tier A or B:
  - `placental_endocrine.estradiol_baseline_ng_per_ml` (Tier B)
  - `fetal_circulation.fhr_baseline_bpm` (Tier B)
  - `fetal_circulation.fhr_term_bpm` (Tier A — NICHD definitions)
- Reference kernels `maternal_estradiol`, `fetal_heart_rate`,
  `maternal_hcg` with endpoint + shape sanity tests. The hCG test
  asserts exact pass-through of the (peak_week, peak) anchor and the
  (40w, term) anchor, validating the build-time decay-rate fit.

- **Two more Phase B submodels** (placental endocrine), bringing the
  registry to **30 submodels** and Phase B to **5 of 10**:
  - `hpl_trajectory` — sigmoidal hPL rise from undetectable
    non-pregnant baseline to ~7 ug/mL at term (Handwerger 2010 /
    Handwerger 1991). hPL is a major driver of maternal insulin
    resistance.
  - `progesterone_trajectory` — sigmoidal progesterone rise from the
    mid-luteal pre-pregnancy baseline (~10 ng/mL) to term
    (~150 ng/mL); 10-20x rise. A single sigmoid simplifies the
    actual two-source kinetics (corpus luteum then placental
    takeover at ~8 weeks). Tulchinsky 1972.
- **Two new dataset parameters** (141 → **143 parameters**), both
  Tier B, in `placental_endocrine`:
  - `hpl_baseline_ug_per_ml` — ~0 (below assay sensitivity).
  - `progesterone_baseline_ng_per_ml` — ~10 ng/mL (mid-luteal pre-
    pregnancy reference).
- Reference kernels `maternal_hpl` and `maternal_progesterone` with
  endpoint + magnitude sanity tests (the progesterone test asserts
  the canonical >10x rise).

- **First three Phase B submodels** with full export support, bringing
  the registry to **28 submodels** and opening Phase B (3 of 10 shipped):
  - `homa_ir_trajectory` — sigmoidal insulin resistance rise across
    gestation using existing `maternal_endocrine.homa_ir_baseline` /
    `homa_ir_term` (Catalano 1991, PMID 1957840; Sonagra 2014).
  - `tsh_trajectory` — piecewise-linear: constant at the T1 hCG-
    suppressed nadir before week 12, then linear toward term recovery
    using existing `tsh_t1_miu_per_l` / `tsh_term_miu_per_l` (Glinoer
    1997, Korevaar 2014). The full Hill-form coupling to hCG (catalog
    item 3.4) is deferred until a coupling-coefficient parameter
    lands.
  - `cortisol_trajectory` — sigmoidal total cortisol rise using
    existing `cortisol_baseline_ug_per_dl` / `cortisol_term_ug_per_dl`
    (Allolio 1990, Jung 2011). The diurnal-rhythm overlay (catalog
    item 3.3) needs a separate amplitude parameter and is deferred.
- Reference kernels `maternal_homa_ir`, `maternal_tsh`,
  `maternal_cortisol` in `nidus.export.reference`, with endpoint +
  midpoint sanity tests. A new `_build_sigmoid_baseline_term` helper
  in `sbml.py` (and matching CellML form) consolidates the standard
  baseline → term logistic emission, reused by all three.
- Generators learned the SBML/MathML `piecewise` construct (TSH is
  the first piecewise submodel in the registry).

- **Four Hadlock biometry growth submodels** — `hadlock_bpd_growth`,
  `hadlock_hc_growth`, `hadlock_ac_growth`, `hadlock_fl_growth` —
  closing out Phase A of the submodel-expansion catalog (12/12 shipped).
  Registry now stands at **25 submodels**. Each fits a cubic
  polynomial at build time to the seven weekly Hadlock 1982
  (PMID 7058748) anchors already in the dataset (16w-40w in 4-week
  steps). Fit residuals: BPD <1 mm, HC ~2.4 mm, AC ~1.4 mm, FL <0.5 mm
  — well inside published longitudinal scatter. The seven anchors
  are carried as nidus parameters in the SBML/CellML output so the
  Hadlock 1982 citation + Tier A annotations propagate cleanly; the
  fit coefficients themselves are derived constants embedded in the
  assignment rule.
- `hadlock_biometry_cubic` and `hadlock_biometry_cubic_coefficients`
  helpers in `nidus.export.reference`; a parametrised fit-residual
  test asserts the cubic reproduces all four biometries within
  per-biometry tolerance, plus a monotonicity check across 16-40w.

- **Two more Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **21 submodels**:
  - `minute_ventilation_trajectory` — derived VE(t) = VT(t) · RR(t)
    using existing maternal_respiratory tidal-volume and respiratory-
    rate baseline/term parameters. The product reproduces the ~30-50%
    pregnancy VE rise (LoMauro 2015, PMID 25624458; Hegewald 2011).
  - `arterial_ph_trajectory` — linear pH rise from non-pregnant
    baseline (~7.40) to term (~7.44) reflecting compensated
    respiratory alkalosis (Templeton & Kelman 1976, PMID 1247088).
- **One new dataset parameter** (140 → **141 parameters**):
  - `maternal_respiratory.term_arterial_ph` — pH at term, Tier B from
    Templeton & Kelman 1976 / LoMauro 2015 convergence. Citation list
    unchanged (existing entries cover the new parameter).
- Reference kernels `maternal_minute_ventilation` and
  `maternal_arterial_ph` with endpoint sanity tests; CellML factor-
  out helper `_sigmoid_baseline_term` consolidates the common
  baseline→term sigmoid MathML.

- **Three more Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **19 submodels**:
  - `heart_rate_trajectory` — sigmoidal HR rise from non-pregnant
    baseline to term using existing `baseline_heart_rate_bpm` and
    `term_heart_rate_bpm` (Mahendru 2014, PMID 25053730).
  - `stroke_volume_trajectory` — Gaussian-bump SV trajectory sharing
    peak week and spread with the CO submodel, using existing
    `baseline_stroke_volume_ml` and `peak_excess_stroke_volume_ml`.
    SV is the larger driver of the CO peak (Mahendru 2014); the
    product SV(t) * HR(t) reconstructs the CO bump.
  - `renal_plasma_flow_trajectory` — Gaussian bell-shape RPF
    trajectory with fixed 8-week spread, using existing
    `renal_plasma_flow_baseline_ml_per_min`, `_peak_ml_per_min`, and
    `rpf_peak_week` (Dunlop 1981, PMID 7259294).
- Reference kernels `maternal_heart_rate`, `maternal_stroke_volume`,
  and `renal_plasma_flow` with endpoint + peak sanity tests. No new
  dataset parameters required for any of the three.

- **Three additional Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **16 submodels**:
  - `svr_trajectory` — derived systemic vascular resistance
    SVR(t) = MAP(t)·80 / CO(t), the conventional CGS form used in
    obstetric haemodynamics. All inputs are the four MAP and four CO
    Gaussian-trajectory parameters already in the dataset; no new
    dataset parameters required. Sanghavi 2014 (PMC4172642) reference.
  - `pao2_trajectory_linear` — linear PaO₂ rise from non-pregnant
    baseline to term reflecting hyperventilation-induced respiratory
    alkalosis. Uses existing
    `maternal_respiratory.baseline_pao2_mmhg` and `pao2_mmhg_term`.
    Templeton & Kelman 1976 (PMID 1247088), Hegewald 2011.
  - `tidal_volume_trajectory` — sigmoidal tidal-volume rise from
    baseline to term. Uses existing
    `maternal_respiratory.baseline_tidal_volume_ml` and
    `tidal_volume_ml_term`. LoMauro 2015 (PMID 25624458),
    Hegewald 2011.
- Reference kernels `maternal_svr_trajectory`,
  `maternal_pao2_linear`, and `maternal_tidal_volume` in
  `nidus.export.reference`, with endpoint + physiological-shape
  sanity tests. The SVR test confirms the mid-pregnancy drop and
  late-pregnancy recovery characteristic of normal haemodynamic
  adaptation.
- Parametrised SBML + CellML test coverage extended to the three new
  submodels; `test_write_sbml_produces_all_files` /
  `test_write_cellml_both_versions` floor lifted from 13 → 16.

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
