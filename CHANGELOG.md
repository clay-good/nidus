# Changelog

All notable changes to Nidus are recorded in this file. The format
follows the spirit of [Keep a Changelog](https://keepachangelog.com)
and the project uses [Semantic Versioning](https://semver.org).

Parameter and citation contributions get their own subheading inside
each release, recording the parameter id, the citation id, the tier
assignment, and the date of merge — so a reader of the changelog can
trace how the simulator's understanding has evolved over time. This is
the "empirical-result integration loop" described in SPEC.md §10:
empirical work updates the parameter database, and the parameter
database is what advances the simulator.

## [Unreleased]

### Engine and infrastructure

- Initial workspace, confidence-tier infrastructure, tick hierarchy,
  seeded RNG, fixed-point numerics, parameter database, maternal and
  placental and fetal subsystems, unknown-channels registry, ensemble
  runner with Sobol sensitivity analysis, outcome divergence detector,
  experiment-design suggester, validation framework, scenario
  orchestrator, command-line interface, observability/telemetry export,
  documentation scaffolding. See [PROGRESS.md](PROGRESS.md) for the
  per-prompt status map against SPEC.md §13.
- Added scenario parameter overrides: typed `[overrides]` blocks on
  `ScenarioSpec` for maternal-cardio, placenta-structure, placenta-gas,
  and fetal-circulation parameters, applied by the orchestrator on
  top of the model defaults.
- CLI: implemented the three subcommands previously flagged as
  deferred in `crates/nidus-cli/src/main.rs`:
  - `nidus validate` — runs the built-in validation suite and emits
    either a Markdown report or a JSON document with per-case
    residuals and the agreement-bucket summary.
  - `nidus hypothesis-report` — runs ensemble + Sobol sensitivity +
    experiment-design on the placental gas-exchange model and emits
    ranked structured suggestions (Markdown or JSON).
  - `nidus list parameters` — added `--tier`, `--search`, and `--json`
    filters for case-insensitive substring search and machine-readable
    output.
- `Params::from_database` constructors landed for
  `MaternalCardioParams` (Spec 01.4), `StructureParams`,
  `GasExchangeParams`, `GlucoseTransportParams` (Spec 01.6), and
  `FetalCirculationParams` (Spec 01.7). Each crate now depends on
  `nidus-data` and exposes a `param_ids` submodule listing the
  database ids consumed. A new `ValueSpec::point_estimate` plus
  `ParameterDatabase::point_estimate(id)` provide deterministic scalar
  resolution; missing ids surface via the new
  `DatabaseError::MissingParameter` variant. A cross-crate
  integration test (`nidus-scenarios/tests/database_constructors.rs`)
  loads the on-disk `data/` tree and confirms every constructor
  resolves. Default scaffold values remain available for test-only and
  override-only paths.
- `nidus-validation` now exposes a `builtin` module
  (`maternal_cardio_scaffold_case`, `built_in_cases`) so the CLI and
  downstream consumers share the v0.1 scaffold case rather than
  duplicating it in tests.

### Scenarios

- `scenarios/normal_term_pregnancy.toml` — scaffold normal pregnancy.
- `scenarios/placental_insufficiency.toml` — placental insufficiency
  as a reduction in term placental surface area.
- `scenarios/mild_preeclampsia.toml` — mild preeclampsia as elevated
  maternal MAP plus moderately reduced placental surface area.

### Tutorials

- Added unknown-channel exploration, hypothesis-generation workflow,
  and parameter-contribution walkthrough tutorials under
  [`docs/tutorials/`](docs/tutorials/).

### Parameters

v0.2 Stream A — first batch of verified citation-backed entries
(SPEC_V0.2.md Prompts A1, A2, A3 — data-authoring portion):

- Citation index reset: 28 verified entries covering O2-Hb dissociation,
  maternal haematology / cardio / respiratory / renal physiology,
  placental morphometry and gas / glucose transport, NICHD fetal growth,
  and fetal circulation. Removed the `scaffold-template-source`
  placeholder; updated the two source-code references to point at
  `mahendru-2014-cardiac-output` instead. Added
  [`data/citations/README.md`](data/citations/README.md) documenting
  the citation-verification workflow.
- `data/parameters/maternal/blood.toml`: expanded from 2 to 8 entries
  (`maternal-blood-volume-l`, `maternal-plasma-volume-l`,
  `maternal-plasma-volume-early-l`, `maternal-red-cell-mass-l`,
  `maternal-haematocrit-term`, `maternal-haemoglobin-g-per-dl-term`,
  `oxyhb-bohr-coefficient`; pre-existing `o2-hb-hill-coefficient-maternal`
  and `o2-hb-p50-maternal` preserved). Tier A/B.
- `data/parameters/maternal/cardio.toml` (new): 14 trajectory
  coefficients replacing the hard-coded scaffold defaults in
  `crates/nidus-maternal/src/cardio.rs`. Tier B/C, cite Mahendru 2014,
  Hunter & Robson 1992, Sanghavi & Rutherford 2014, Thaler 1990.
- `data/parameters/maternal/respiratory.toml` (new): 5 entries (minute
  ventilation, tidal volume, PaCO2, PaO2, P50 shift). Tier A/B.
- `data/parameters/maternal/renal.toml` (new): 3 entries (GFR at term
  and first trimester, plasma creatinine). Tier A/B.
- `data/parameters/placenta/structure.toml` (new): 5 entries (initial
  and term villous area, growth midpoint and rate, membrane thickness).
  Tier B/C, cite Mayhew 2014, Carter 2009.
- `data/parameters/placenta/gas_transport.toml` (new): 2 entries
  (half-saturation area, max equilibration). Tier C, cite Mayhew 1986
  and Carter & Pijnenborg 2011.
- `data/parameters/placenta/glucose_transport.toml` (new): 4 entries
  (GLUT1 and GLUT3 Km and Vmax). Tier B/C, cite Illsley 2000,
  Baumann 2002, Brown 2011.
- `data/parameters/fetal/circulation.toml` (new): 3 entries replacing
  hard-coded fetal-circulation constants (foramen-ovale streamline
  preference, ductus-arteriosus share, systemic venous return PO2).
  Tier C, cite Rudolph 1985 and Kiserud 2000.
- `data/parameters/fetal/growth.toml` (new): 7 entries (estimated
  fetal weight at 20/28/36/40 weeks, biparietal diameter and femur
  length at 28 weeks, Hadlock coefficient). Tier A, cite NICHD Fetal
  Growth Studies (Buck Louis 2015, Grewal 2018) and Hadlock 1991.
- `data/parameters/fetal/metabolism.toml` (new): 2 entries (O2
  consumption per kg, glucose utilisation per kg). Tier B, cite
  Battaglia & Meschia 1986.

The `from_database` constructors that consume these entries —
the second half of Prompts A2/A3 and the code-side of Spec 01
Prompts 01.4/01.6/01.7 — are now implemented (see "Engine and
infrastructure" above).

While wiring the constructors, two data/struct unit mismatches were
corrected:
- `maternal-cardio-cardiac-output-individual-sigma` is a fractional
  one-sigma in the model; its TOML entry was retyped from `L/min`
  (value 0.6) to `fraction` (value 0.13 ≈ 13%, consistent with
  Mahendru 2014 CV of CO).
- `fetal-circulation-foramen-ovale-streamline-preference` is a
  weighted-average weight in the model (0.5 = no preference); its
  TOML value was retyped from 0.55 to 0.80 with a clarified
  description, matching Rudolph 1985's reported ~75–80% preferential
  streaming.

### Unknown channels

- Registered the four v0.1 standard channels: maternal exosomal
  microRNA transfer (Tier D), cellular microchimerism (Tier C),
  maternal-cortisol diurnal influence on fetal HPA-axis development
  (Tier C), and immunoglobulin transfer dynamics (Tier C).

### Validation cases

<!-- Empty: the scaffold ships only a synthetic-reference demonstration
case for the maternal cardiovascular module. Real reference datasets
(NICHD Fetal Growth Studies, placental Doppler flow, fetal
cardiovascular developmental data) are the human-contributor follow-up. -->

---

## Format guidance for future entries

Every release section should contain four subsections, even when one
or more are empty:

1. **Engine and infrastructure** — engine, API, visualisation, and
   tooling changes.
2. **Parameters** — one line per parameter id added, updated, or
   retired, with the citation id and tier in brackets. Example:
   `- maternal-hemoglobin-mean-term [Tier B, cite:cdc-1989] (added)`.
3. **Unknown channels** — registry additions, tier promotions
   (a channel moving from Tier D to Tier C as evidence accumulates),
   or removals.
4. **Validation cases** — new or modified validation cases, including
   the reference dataset id and the agreement bucket the case
   currently lands in.

When a parameter is added, modified, or retired, link to the pull
request and the citation entry it depends on. Tier promotions and
demotions are particularly important to record; they are the visible
trace of empirical work reaching the simulator.
