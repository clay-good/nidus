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

<!-- Empty: the scaffold ships only template parameters; verified Tier A
entries are the human-contributor follow-up per CONTRIBUTING.md. -->

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
