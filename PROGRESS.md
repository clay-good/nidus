# Implementation Progress

This file tracks which of the implementation prompts in
[SPEC.md §13](docs/specs/SPEC.md) have been completed. Each prompt becomes a
checkbox here; when starting a new working session, look for the first
unchecked item.

## Status

- [x] **Prompt 1 — Workspace initialisation.**
  Cargo workspace with the full crate layout from SPEC.md §12, strict
  workspace-level lints (`unsafe_code = forbid`, clippy `all` and
  `pedantic`), MIT licence, README drawn from SPEC.md §§1–2,
  CONTRIBUTING explaining the confidence tier system, and CODE_OF_CONDUCT.
  Build is clean; clippy is clean with `-D warnings`.
- [x] **Prompt 2 — Confidence tier infrastructure.**
  Implemented in `nidus-core`:
  - [`tier::ConfidenceTier`](crates/nidus-core/src/tier.rs) — A/B/C/D
    enum with `combine` propagation rule.
  - [`citation::Citation`](crates/nidus-core/src/citation.rs) and
    `CitationId` — full bibliographic record + stable slug.
  - [`tiered::Tiered<T>`](crates/nidus-core/src/tiered.rs) — generic
    wrapper with `Add`/`Sub`/`Mul`/`Div`/`Neg` that propagate the
    less-confident tier and union the citation lists.
  Tests cover tier propagation under arithmetic, citation merging, and
  chained operations.
- [x] **Prompt 3 — Tick hierarchy and runtime.**
  Implemented in `nidus-core`:
  - [`clock`](crates/nidus-core/src/clock.rs) — `GestationalAge`,
    `TickTier` (Second/Minute/Hour/Day), `TickClock` with integer-second
    advancement.
  - [`rng`](crates/nidus-core/src/rng.rs) — `RngService` keyed by
    `(SubscriberId, tick)` using a two-pass ChaCha20 seed derivation;
    `ChildRng` exposing `next_u64`/`next_u32`/`fill_bytes`/`next_f64_unit`.
  - [`subscriber`](crates/nidus-core/src/subscriber.rs) — `Subscriber`
    trait, `SubscriberId`, and `TickContext`.
  - [`dispatcher`](crates/nidus-core/src/dispatcher.rs) — `Dispatcher`
    storing subscribers in a `BTreeMap` for deterministic ordering;
    fires fine-to-coarse at each shared boundary.
  - [`snapshot`](crates/nidus-core/src/snapshot.rs) — engine-state
    snapshot (`start_age`, `tick`, `master_seed`); no RNG state needs
    serialisation because streams are re-derived per tick.
  Tests cover bit-identical reproducibility under the same seed,
  divergence under different seeds, snapshot-and-resume matching a
  continuous run (with subscribers re-registered in a different order
  to exercise reordering independence), and fine-to-coarse dispatch
  ordering at shared boundaries.

- [x] **Prompt 4 — Fixed-point numerics.**
  Implemented in [`nidus-core::numerics`](crates/nidus-core/src/numerics/):
  - [`fixed`](crates/nidus-core/src/numerics/fixed.rs) — Q32.32 `Fixed`
    type with checked add/sub/mul/div, `OverflowError`, and explicit
    truncation-toward-negative-infinity rounding so arithmetic is
    bit-identical across architectures.
  - [`quantities`](crates/nidus-core/src/numerics/quantities.rs) — six
    typed wrappers (`Mass`, `Pressure`, `Volume`, `Concentration`,
    `Duration`, `Ratio`) generated via a macro, with same-unit
    arithmetic and `Ratio`-based scaling. Cross-unit arithmetic is a
    compile-time error by construction.
  Tests cover f64 round-tripping, non-finite/out-of-range rejection,
  overflow detection across +/-/×/÷, and unit-preserving scaling.
- [x] **Prompt 5 — Parameter database.**
  Implemented in [`nidus-data`](crates/nidus-data/):
  - [`schema`](crates/nidus-data/src/schema.rs) — serde-derived
    `ParameterEntry`, `CitationEntry`, `ValueSpec` (point / uniform /
    normal / lognormal), `AgeRange`, with `deny_unknown_fields` so
    typos fail loudly.
  - [`database`](crates/nidus-data/src/database.rs) — `ParameterDatabase`
    loader and query API, with typed `DatabaseError` covering I/O,
    parse, duplicate ids, dangling citation references, and invalid
    age ranges.
  - [Repository data tree](data/) with [`README.md`](data/README.md),
    [`citations/index.toml`](data/citations/index.toml), and
    [`parameters/maternal/blood.toml`](data/parameters/maternal/blood.toml)
    as a working scaffold. Per CONTRIBUTING.md, the parameter-authoring
    half of this prompt — verified Tier A entries covering maternal
    blood, O₂–Hb dissociation, placental gas diffusion, and GLUT1/GLUT3
    kinetics — is a human contribution that must verify each citation
    against its original; the scaffold gives them a working template
    to extend.
  Tests cover successful loading, schema rejection of unknown fields,
  duplicate-id detection, dangling-citation detection, age-range
  validation, tier-filtered iteration, and a workspace integration
  test that loads the actual `data/` tree.

- [x] **Prompt 6 — Maternal cardiovascular model.**
  Implemented in [`nidus-maternal`](crates/nidus-maternal/):
  - [`cardio`](crates/nidus-maternal/src/cardio.rs) — `MaternalCardio`
    subscriber producing cardiac output, MAP, and uterine artery flow
    as functions of gestational age, with per-individual stochastic
    offsets sampled once from the seeded RNG via Box–Muller.
    Trajectory coefficients live in `MaternalCardioParams` (default
    values land in textbook ranges; flagged as scaffolding pending
    database integration).
  Tests cover: cardiac-output rise-then-decline through the third
  trimester, mid-pregnancy MAP nadir, monotonic uterine-flow rise,
  same-seed reproducibility, seed divergence, and dispatcher wiring.
- [x] **Prompt 7 — Placental transport model.**
  Implemented in [`nidus-placenta`](crates/nidus-placenta/):
  - [`structure`](crates/nidus-placenta/src/structure.rs) — logistic
    placental surface-area trajectory (initial ≈ 0.5 m², term ≈ 12 m²).
  - [`transport`](crates/nidus-placenta/src/transport.rs) —
    `gas_exchange` (venous-equilibrator weighted average with
    saturation-capped equilibration coefficient) and
    `glucose_flux_mmol_per_min` (net Michaelis–Menten facilitated
    diffusion).
  - [`subscriber`](crates/nidus-placenta/src/subscriber.rs) — `Placenta`
    subscriber tracking surface area and last-computed UV PO₂.
  Tests cover: surface-area monotonicity and textbook term value, UV
  PO₂ inside the published 25–40 mmHg window at term, growth-restriction
  pattern under reduced surface area, asymptote below maternal arterial
  PO₂, glucose flux direction and gradient reversal, and Michaelis–
  Menten saturation.
- [x] **Prompt 8 — Fetal cardiovascular special circulation.**
  Implemented in [`nidus-fetal`](crates/nidus-fetal/):
  - [`special_circulation`](crates/nidus-fetal/src/special_circulation.rs)
    — `FetalSpecialCirculation::route` maps UV PO₂ to cerebral,
    descending aortic, and umbilical-artery (return) PO₂ via a
    streamline-preference weighted average, encoding the foramen-ovale
    and ductus-arteriosus routing.
  - [`subscriber`](crates/nidus-fetal/src/subscriber.rs) — `Fetal`
    subscriber that picks up the placenta's umbilical-vein output
    between ticks and closes the loop by publishing umbilical-artery
    PO₂ for the placenta to consume.
  Tests cover: cerebral PO₂ structurally higher than descending aortic,
  UA between descending and cerebral, sensitivity to UV PO₂, the
  collapse case where eliminating streamline preference removes the
  cerebral advantage, and cerebral PO₂ landing in the textbook range
  at default term conditions.

- [x] **Prompt 9 — Unknown channels registry.**
  Implemented in [`nidus-unknown`](crates/nidus-unknown/):
  - [`registry`](crates/nidus-unknown/src/registry.rs) — `UnknownChannel`
    metadata (id, name, hypothesised mechanism, supporting/questioning
    citations, parameter range with units, downstream effects, tier),
    `ChannelMode` (`Disabled` / `Fixed(v)` / `Sample`), `ChannelRegistry`
    keyed by `BTreeMap` for deterministic order.
  - `ChannelRegistry::standard_v0_1` ships the four channels named in
    SPEC.md §13 prompt 9: maternal exosomal microRNA transfer
    (Tier D), cellular microchimerism (Tier C), the maternal-cortisol
    diurnal influence on fetal HPA-axis development (Tier C), and IgG
    transfer dynamics (Tier C). All ship in `Disabled` mode for a
    minimal-model baseline.
  Tests cover: tier-A/B rejection, tier-C/D acceptance, duplicate-id
  rejection, all three modes resolving to the right values, sample-mode
  stays within range, the standard registry contains all named
  channels, deterministic iteration order, unknown-id rejection on
  `set_mode`, and a baseline-versus-sampled divergence test.
- [x] **Prompt 10 — Ensemble runner + sensitivity analyser.**
  Implemented in [`nidus-hypothesis`](crates/nidus-hypothesis/):
  - [`ensemble`](crates/nidus-hypothesis/src/ensemble.rs) — tier-aware
    `EnsembleRunner` over `ParameterSpec` entries with three
    `SamplingStrategy` variants (`Uniform` for Tier C/D ranges,
    `Normal` for Tier A/B measured uncertainty, `Fixed` for held-out
    parameters). Per-sample RNG keying via `(seed, sample_index)` makes
    runs bit-identical and trivially reproducible.
  - [`sensitivity`](crates/nidus-hypothesis/src/sensitivity.rs) —
    `SensitivityAnalyser` implementing Saltelli (2010) Sobol first-
    order and total-order estimators with the `A`/`B`/`A_B(i)` matrix
    scheme; `N·(k+2)` model evaluations. Results sorted by
    total-order descending with deterministic name-based tie break.
  Tests cover: uniform draws bounded, fixed strategy constant,
  same-seed reproducibility, seed divergence, normal-sampling moments,
  the linear-additive `y = x₁ + 2x₂` case producing analytical
  `S₁ ≈ 0.2`, `S₂ ≈ 0.8` with `S_T = S` (additivity), total-order
  ordering correctness, multiplicative-interaction `y = x₁·x₂`
  producing `S_T > S_first`, constant-model zero-variance edge case,
  and same-seed reproducibility of full results.

- [x] **Prompt 11 — Outcome divergence detector.**
  Implemented in
  [`nidus-hypothesis::divergence`](crates/nidus-hypothesis/src/divergence.rs):
  deterministic 1D k-means with `k = 2`, separation score
  `|μ₁ − μ₂| / pooled within-cluster SD` (≡ Ashman's `D` for
  equal-variance clusters), default threshold `3.0` (chosen so
  splitting a single Gaussian — which gives `D ≈ 2.65` — is not
  false-flagged), and a `min_cluster_fraction` guard so a lone outlier
  does not count as a second mode. Each detected `Mode` carries a
  parameter signature: the mean of each input parameter inside that
  cluster, which is what surfaces "this parameter is the switch."
  Tests cover: unimodal Gaussian not flagged, step-function bimodality
  flagged with cluster centroids near the regime values, parameter
  signatures correctly identifying the switch parameter (and not
  drifting on irrelevant ones), outlier rejection, and empty/singleton
  edge cases.
- [x] **Prompt 12 — Experiment design suggester.**
  Implemented in
  [`nidus-hypothesis::experiment_design`](crates/nidus-hypothesis/src/experiment_design.rs):
  `ExperimentDesignSuggester` takes a `SensitivityResult` plus optional
  `SuggesterParameterInfo` per parameter (current estimate,
  uncertainty, affected outcomes, available techniques) and emits a
  ranked `Vec<ExperimentSuggestion>`. Ranking: descending
  `expected_information_yield = total_order_index · Var(Y)`, with ties
  broken so less-confident tiers (D, then C) surface first.
  Tests cover: descending ordering by yield, tier tie-breaking, info
  threading through to the suggestion, missing-info parameters still
  included with NaN sentinels, and the yield-formula contract.
- [x] **Prompt 13 — Validation suite.**
  Implemented in [`nidus-validation`](crates/nidus-validation/):
  - [`suite`](crates/nidus-validation/src/suite.rs) — `ReferencePoint`,
    `ReferenceDataset` (carries `CitationId`), `ValidationCase`
    (tier + `ComponentLevel::{Component, Integration, Outcome}`),
    `ValidationSuite::run` orchestrating a simulator probe across
    every case.
  - [`report`](crates/nidus-validation/src/report.rs) — four-bucket
    `Agreement` classifier (`Excellent` / `Adequate` / `Divergent` /
    `Unvalidatable`) that recognises Tier C/D cases as unvalidatable
    by definition, RMS residual, in-range counts, and a Markdown
    renderer.
  - Integration test
    [`tests/maternal_cardio.rs`](crates/nidus-validation/tests/maternal_cardio.rs)
    exercises the full pipeline against the maternal cardio module
    with a scaffold reference dataset.
  As with Prompt 5, the *parameter-authoring* half — wiring in the
  NICHD Fetal Growth Studies, placental Doppler flow ranges, and
  fetal cardiovascular developmental data with verified citations —
  is a human contribution and is flagged in the crate documentation
  and in this file.

- [x] **Prompt 14 — Scenario orchestrator + CLI.**
  Implemented in [`nidus-scenarios`](crates/nidus-scenarios/) and
  [`nidus-cli`](crates/nidus-cli/):
  - [`spec`](crates/nidus-scenarios/src/spec.rs) — `ScenarioSpec` TOML
    schema with `deny_unknown_fields`, validator (8 ≤ start < end ≤ 40,
    known subscribers only), and string/path loaders.
  - [`orchestrator`](crates/nidus-scenarios/src/orchestrator.rs) —
    `ScenarioOrchestrator::run` wires maternal/placenta/fetal
    subscribers together, advances a `TickClock`, and emits a
    `ScenarioReport` of `ScenarioSample` records at the scenario's
    recording cadence.
  - [`builtin::NORMAL_TERM_PREGNANCY`](crates/nidus-scenarios/src/builtin.rs)
    compiled-in scaffold; same content on disk at
    [`scenarios/normal_term_pregnancy.toml`](scenarios/normal_term_pregnancy.toml).
  - [`nidus-cli`](crates/nidus-cli/src/main.rs) — clap-based subcommands:
    `run` (executes a scenario file or the built-in scaffold; emits
    pretty JSON), `list parameters`, `list channels`,
    `validate-config`. All four subcommands smoke-tested end-to-end.
  Tests cover scenario load/validation (start-age floor, end-before-start,
  unknown subscriber, unknown field), full-run sample count and
  endpoint, and subscriber gating.
- [x] **Prompt 15 — Observability (partial: telemetry + export).**
  Implemented in
  [`nidus-observability`](crates/nidus-observability/):
  - [`telemetry`](crates/nidus-observability/src/telemetry.rs) —
    `TelemetryEvent` carrying source, tick, age, quantity name,
    `TelemetryValue` (number or text), unit, tier, and citation list.
    `TelemetryBus` is the v0.1.0 in-memory append-only collector.
  - [`export`](crates/nidus-observability/src/export.rs) — NDJSON
    writer (`write_ndjson`, `write_ndjson_to_path`); one event per
    line so Python and browser consumers can stream directly.
  The interactive **web dashboard** described in SPEC.md §13 prompt 15
  is intentionally **deferred to v0.2** — it is a separate frontend
  deliverable with its own UX surface. What ships in v0.1.0 is the
  data pipeline the dashboard will consume.
- [x] **Prompt 16 — Empirical-result integration workflow.**
  - [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)
    with structured sections for parameter contributions, unknown
    channel contributions, validation case contributions, and plain
    code changes; plus a build/test/clippy checklist.
  - [`CHANGELOG.md`](CHANGELOG.md) with the per-release subheading
    convention (Engine, Parameters, Unknown channels, Validation
    cases) so tier promotions and citation updates are visible.
  - [`docs/contributing/parameter-pull-requests.md`](docs/contributing/parameter-pull-requests.md)
    documents the review checklist (citation verification, tier
    assignment, population description, age-range alignment,
    validation suite still passing) and the tier-promotion record.
- [x] **Prompt 17 — Documentation and example library.**
  - [`docs/README.md`](docs/README.md) indexes the doc tree.
  - [`docs/architecture/overview.md`](docs/architecture/overview.md)
    summarises subsystem topology, the determinism contract, tier
    propagation, and the tick hierarchy.
  - [`docs/tutorials/README.md`](docs/tutorials/README.md) covers the
    quickstart, custom-scenario authoring, and the sensitivity-analysis
    walkthrough; outlines the unknown-channel-exploration,
    hypothesis-generation, and parameter-update tutorials that are
    planned.
  - Working example
    [`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs)
    runs end-to-end (`cargo run -p nidus-hypothesis --example
    sensitivity_placental_gas_exchange`) — Saltelli Sobol estimation
    on a placental gas-exchange model, then ranked
    experiment-design suggestions.

## Post-v0.1.0 follow-up (in repo, beyond the 17 prompts)

- **Scenario parameter overrides.** `ScenarioSpec` now carries an
  `[overrides]` section with typed override blocks for the maternal
  cardio, placental structure, placental gas, and fetal circulation
  parameter structs. The orchestrator overlays them on the model
  defaults before running. Wired through
  [`crates/nidus-scenarios/src/spec.rs`](crates/nidus-scenarios/src/spec.rs)
  and [`crates/nidus-scenarios/src/orchestrator.rs`](crates/nidus-scenarios/src/orchestrator.rs);
  tests cover the placental-insufficiency and elevated-MAP cases.
- **Pathology scenarios.** Two new scenarios named in SPEC.md §7,
  expressed as parameter perturbations of the normal trajectory:
  [`scenarios/placental_insufficiency.toml`](scenarios/placental_insufficiency.toml)
  and [`scenarios/mild_preeclampsia.toml`](scenarios/mild_preeclampsia.toml).
  Same content also available as `nidus_scenarios::builtin`
  constants `PLACENTAL_INSUFFICIENCY` and `MILD_PREECLAMPSIA`.
- **Tutorials.** The three planned tutorials in
  [`docs/tutorials/`](docs/tutorials/) are now written:
  [`unknown_channels.md`](docs/tutorials/unknown_channels.md),
  [`hypothesis_workflow.md`](docs/tutorials/hypothesis_workflow.md),
  [`contributing_parameter.md`](docs/tutorials/contributing_parameter.md).
- **CLI deferred subcommands landed.** The three items flagged as
  deferred in the v0.1 CLI docstring are now implemented:
  - `nidus validate` runs the built-in validation suite (wired through
    a new `nidus_validation::builtin` module so the scaffold maternal
    cardio case is shared between tests and the CLI) and emits a
    Markdown or JSON report.
  - `nidus hypothesis-report` runs ensemble + Sobol sensitivity +
    experiment-design on the placental gas-exchange model and emits
    ranked, structured suggestions (Markdown or JSON).
  - `nidus list parameters` gained `--tier`, `--search` (case-insensitive
    substring on id/name/unit), and `--json` filters.
  The only remaining v0.2 CLI surface is the interactive dashboard.

## v0.2.0 — Researcher-ready

Tracking the prompts from [SPEC_V0.2.md](docs/specs/SPEC_V0.2.md) and the detailed
specs under [docs/specs/](docs/specs/). Tick boxes as prompts land; partial
landings record what is done and what remains.

### Stream A — Parameter database

- [x] **Prompt A1 — Citation index population.**
  [`data/citations/index.toml`](data/citations/index.toml) reset with
  28 verified entries covering O2-Hb dissociation (Severinghaus 1979,
  Dash & Bassingthwaighte 2010, Kelman 1966), maternal haematology
  (Hytten & Chamberlain 1980, Bernstein 2001, de Haas 2017),
  maternal cardio (Mahendru 2014, Hunter & Robson 1992, Sanghavi &
  Rutherford 2014, Thaler 1990), respiratory (LoMauro & Aliverti 2015,
  Crapo 1996), renal (Cheung & Lafayette 2013, Davison & Hytten 1974),
  placental morphometry and transport (Mayhew 2014, Carter 2009,
  Burton 2015, Mayhew 1986, Carter & Pijnenborg 2011, Illsley 2000,
  Baumann 2002, Brown 2011, Cleal & Lewis 2008), fetal growth (Buck
  Louis 2015 NICHD, Grewal 2018 NICHD, Hadlock 1991), fetal circulation
  (Rudolph 1985, Kiserud 2000, Sutton 1991), and metabolism / organ
  maturation (Battaglia & Meschia 1986, Avery & Mead 1959, Burri 2006).
  Removed the `scaffold-template-source` placeholder; the two source
  references (validation `builtin.rs` and `tests/maternal_cardio.rs`)
  now point at `mahendru-2014-cardiac-output`. Added
  [`data/citations/README.md`](data/citations/README.md) documenting
  the citation-add and verification workflow.

- [x] **Prompt A2 — Maternal parameter coverage.**
  - `data/parameters/maternal/blood.toml` expanded to 8 entries
    (O2-Hb, Bohr coefficient, blood volume, plasma volume — term and
    early, red-cell mass, haematocrit, haemoglobin).
  - `data/parameters/maternal/cardio.toml` (new): 14 entries mapping
    one-to-one onto the hard-coded constants in
    [`crates/nidus-maternal/src/cardio.rs`](crates/nidus-maternal/src/cardio.rs).
  - `data/parameters/maternal/respiratory.toml` (new): minute
    ventilation, tidal volume, PaCO2, PaO2, P50 shift.
  - `data/parameters/maternal/renal.toml` (new): GFR (term and first
    trimester), plasma creatinine.
  - `MaternalCardioParams::from_database` (Spec 01, Prompt 01.4) is
    landed; the constructor and its `param_ids` audit module live in
    [`crates/nidus-maternal/src/cardio.rs`](crates/nidus-maternal/src/cardio.rs).
    Default scaffold values are kept as a test- and override-only
    helper. The blood / respiratory / renal entries are the source
    of truth for future subscribers that consume those subsystems
    (no Rust subscribers read them yet).

- [x] **Prompt A3 — Placental and fetal parameter coverage.**
  - `data/parameters/placenta/structure.toml`: 5 entries (initial /
    term villous area, growth midpoint and rate, membrane thickness).
  - `data/parameters/placenta/gas_transport.toml`: 2 entries
    (half-saturation area, max equilibration).
  - `data/parameters/placenta/glucose_transport.toml`: 4 entries
    (GLUT1 / GLUT3 Km and Vmax-per-area).
  - `data/parameters/fetal/circulation.toml`: 3 entries replacing the
    hard-coded foramen-ovale, ductus-arteriosus, and systemic-venous
    PO2 constants in
    [`crates/nidus-fetal/src/special_circulation.rs`](crates/nidus-fetal/src/special_circulation.rs).
  - `data/parameters/fetal/growth.toml`: 7 NICHD- and Hadlock-cited
    entries (EFW at 20/28/36/40 weeks, BPD/FL at 28 weeks, Hadlock
    coefficient).
  - `data/parameters/fetal/metabolism.toml`: O2 consumption and
    glucose utilisation per kg.
  - `StructureParams::from_database`, `GasExchangeParams::from_database`,
    `GlucoseTransportParams::from_database` (Spec 01, Prompt 01.6), and
    `FetalCirculationParams::from_database` (Spec 01, Prompt 01.7) are
    landed; each constructor's `param_ids` audit module lives next to
    the struct definition. A cross-crate integration test —
    [`crates/nidus-scenarios/tests/database_constructors.rs`](crates/nidus-scenarios/tests/database_constructors.rs)
    — loads the on-disk `data/` tree and verifies all five constructors
    resolve and produce sane values.
  - Two TOML/struct unit corrections shipped with the wiring:
    `maternal-cardio-cardiac-output-individual-sigma` retyped from
    `L/min` to `fraction` (matching the model's fractional sigma),
    and `fetal-circulation-foramen-ovale-streamline-preference`
    retyped from 0.55 to 0.80 to match the model's
    weighted-average semantics and Rudolph 1985's ~75–80% number.

### Streams B–F

- [~] **Prompt B1 — Reference dataset adapters** *(scaffold landed; per-dataset
  rollouts continue under B2).*
  - New [`crates/nidus-validation/src/datasets/`](crates/nidus-validation/src/datasets/)
    module with shared `Dataset` / `DatasetRow` types and a `deny_unknown_fields`
    TOML loader (`load_from_str`, `cached`).
  - First working adapter:
    [`maternal_hemodynamics`](crates/nidus-validation/src/datasets/maternal_hemodynamics.rs),
    bundling [`data/validation/maternal_hemodynamics.toml`](data/validation/maternal_hemodynamics.toml)
    (Mahendru 2014 longitudinal cardiac-output trajectory; 7 rows across
    8–40 weeks). Loaded via `include_str!` and cached behind a
    `OnceLock`.
  - Cross-crate test
    [`crates/nidus-validation/tests/datasets.rs`](crates/nidus-validation/tests/datasets.rs)
    confirms the dataset's `citation_id` resolves against the shipping
    citation index.
  - The NICHD growth, Doppler flow, and fetal cardiac adapters
    (Prompts 03.2/03.3/03.4) follow the same shape; they are deferred
    until the per-dataset TOMLs are authored by a human contributor.
- [ ] **Prompt B2** — Validation cases (NICHD, placental Doppler,
  fetal cardiac).
- [x] **Prompt B3 — Validation documentation.**
  Populated [`docs/validation/`](docs/validation/) with:
  [`overview.md`](docs/validation/overview.md) (what the suite covers,
  the tier-aware agreement classifier, and how to run it),
  [`extending.md`](docs/validation/extending.md) (the four-part workflow
  for adding a case: dataset TOML → adapter → `ValidationCase` →
  case doc),
  [`report-schema.md`](docs/validation/report-schema.md) (stable JSON
  schema for `nidus validate --format json`), and
  [`case-maternal-cardiac-output.md`](docs/validation/case-maternal-cardiac-output.md)
  documenting the single shipped case. Linked from
  [`docs/README.md`](docs/README.md). Per-case docs for the
  NICHD/Doppler/fetal-cardiac cases land alongside their respective
  TOMLs under B2.
- [ ] **Prompt C1** — PyO3 + maturin bindings for `nidus-py`.
- [ ] **Prompt C2** — Jupyter quickstart notebook.
- [ ] **Prompt C3** — Hypothesis / sensitivity in Python.
- [ ] **Prompt D1** — Interactive dashboard.
- [ ] **Prompt D2** — End-to-end researcher tutorials.
- [ ] **Prompt D3** — CLI polish: `nidus run`, `nidus doctor`,
  `--seed`, `--age-range`.
- [ ] **Prompt E1** — Release artefacts workflow.
- [ ] **Prompt E2** — Software citation (`CITATION.cff`, Zenodo).
- [ ] **Prompt E3** — Reproducibility manifest and `nidus reproduce`.
- [ ] **Prompt F1** — Examples directory.
- [~] **Prompt F2 — Contributor onboarding refresh and issue templates**
  *(issue templates landed; contributing-doc end-to-end refresh
  continues as Streams B/C/D fill in the validation/Python/CLI surfaces
  they reference).*
  Added three GitHub Issue templates under
  [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/):
  `parameter-request.yml`, `bug-report.yml`, and
  `hypothesis-proposal.yml`, plus a `config.yml` that disables blank
  issues and directs open-ended questions to GitHub Discussions.
  [`CONTRIBUTING.md`](CONTRIBUTING.md) gained a "Filing an issue"
  section pointing at the templates, and the dead `SPEC.md` pointer at
  the repo root was retargeted to `docs/specs/SPEC.md` (matching the
  v0.2 spec relocation).
- [ ] **Prompt F3** — CI completeness (maturin, validation gate).
- [ ] **Prompt F4** — Final PROGRESS / CHANGELOG sweep.

## Up next

All seventeen SPEC.md §13 prompts have at least their v0.1.0 scope
landed. The remaining work for v0.2 falls into three streams:

- **Parameter authoring (human-contributor task).** Populate
  `data/parameters/` and `data/citations/` with verified entries for
  the Tier A and B parameters named in SPEC.md §13 prompt 5
  (maternal blood properties, O₂–Hb dissociation, gas diffusion,
  GLUT1/3 kinetics). See
  [`docs/contributing/parameter-pull-requests.md`](docs/contributing/parameter-pull-requests.md).
- **Reference-dataset integration (human-contributor task).** Add
  validation cases against the NICHD Fetal Growth Studies, published
  placental Doppler flow ranges, and fetal cardiovascular
  developmental data, with citation-bearing dataset entries.
- **Interactive dashboard.** The web frontend deferred from Prompt 15.
  Consumes the NDJSON exports already produced by
  `nidus-observability`.

## How to verify what is done

```sh
cargo build --workspace          # clean build
cargo test --workspace           # 114 across all v0.1.0 crates
cargo clippy --workspace --all-targets -- -D warnings   # clean
```
