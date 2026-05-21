# Spec 10 — Population Modelling

## Context

SPEC.md §§3, 8 describe Nidus as producing distributions, not point
estimates, with explicit per-individual variability and explicit
between-individual variability drawn from population distributions.
The v0.1 reality (audit items 121–123):

- `ScenarioSpec` uses point values; there is no support for sampling
  individual parameter draws from the database's `ValueSpec`
  distributions.
- The orchestrator runs a single individual per invocation.
- Per-individual offsets in
  [`crates/nidus-maternal/src/cardio.rs:142-145`](../crates/nidus-maternal/src/cardio.rs)
  exist but the sigma values are scaffolded constants, not drawn from
  population SDs in the database.

A researcher who wants to ask "what fraction of pregnancies with
elevated MAP develop fetal growth restriction?" needs ensemble
population sampling. This spec adds it.

## Deliverables

- `nidus_scenarios::Population` type: a Scenario with an ensemble
  draw plan.
- Per-parameter sampling from the database's `ValueSpec` distribution.
- `nidus run --n-individuals N` produces N-individual NDJSON and a
  population summary table.
- Stratification: cohorts (subgroups) drawn from named subsets of
  the database.
- Population-level validation cases (Spec 03 references this).
- Documentation and a worked example.

## Dependencies

Requires Spec 01 (database `ValueSpec` distributions) and Spec 02
(modules whose parameters are sampled).

## Numbered prompts

### Prompt 10.1 — Population draw plan

File: new
[`crates/nidus-scenarios/src/population.rs`](../crates/nidus-scenarios/src/population.rs).

`PopulationPlan`:

```rust
pub struct PopulationPlan {
    pub n_individuals: u32,
    pub sample_from_database: bool,  // if true, draw each individual's
                                     // params from the ValueSpec distribution
                                     // for that id
    pub fixed_seeds: Option<Vec<u64>>,  // for deterministic replay
    pub stratify_by: Option<Stratification>,
}
pub enum Stratification {
    None,
    Categorical { variable: String, levels: Vec<(String, f64)> },
    Continuous  { variable: String, samples: Vec<f64> },
}
```

Wired into `ScenarioSpec` as an optional `[population]` table.

### Prompt 10.2 — Per-individual parameter sampling

File: same as 10.1, plus
[`crates/nidus-data/src/sampling.rs`](../crates/nidus-data/src/sampling.rs)
(new).

For each `ParameterEntry` flagged as population-sampled, draw one
value from its `ValueSpec` (uniform, normal, lognormal) using a
deterministically-keyed child RNG so two runs with the same seed
draw identical individuals.

Verification: same seed + same plan ⇒ byte-identical draws across
machines; sample mean and variance over N=1000 individuals match
the `ValueSpec` parameters within Monte Carlo error.

### Prompt 10.3 — Orchestrator ensemble loop

File: [`crates/nidus-scenarios/src/orchestrator.rs`](../crates/nidus-scenarios/src/orchestrator.rs).

Extend the orchestrator to run N individuals serially (parallel via
`rayon` behind `--jobs <n>` after correctness is established). Each
individual gets its own `RngService` seeded from the master seed +
individual index. Telemetry is tagged with an `individual_id` column.

Verification: `nidus run normal_term --n-individuals 100 --out
/tmp/p` produces telemetry with 100 distinct `individual_id`s.

### Prompt 10.4 — Population summary report

File: [`crates/nidus-cli/src/run.rs`](../crates/nidus-cli/src/run.rs).

`summary.md` (already produced by Spec 06 Prompt 06.1) gains a
population section when `--n-individuals > 1`: per-quantity per-age
sample mean, SD, 5/50/95 percentiles. A companion
`population_summary.csv` is written for downstream analysis.

### Prompt 10.5 — Cohort definitions

File: new
[`data/cohorts/`](../data/cohorts/) plus a TOML schema.

Pre-defined cohorts: `nulliparous_low_risk`, `parous`,
`advanced_maternal_age`, `prior_preeclampsia`. Each cohort is a TOML
file overriding specific parameter distributions with subgroup-
specific values (citations required).

`ScenarioSpec` can reference a cohort by name in the `[population]`
table.

### Prompt 10.6 — Population validation cases

File: [`crates/nidus-validation/src/builtin.rs`](../crates/nidus-validation/src/builtin.rs).

Add cases verifying:
- The fraction of `normal_term` individuals whose 36-wk fetal weight
  falls inside the NICHD 10–90th band is ≥ 80 % (population-level
  calibration).
- The variance ratio at 28 wk between simulator and NICHD matches
  within a factor of 1.5.

These complement the integration case in Spec 03 Prompt 03.9.

### Prompt 10.7 — Stratified analysis API

File: [`crates/nidus-py/src/population.rs`](../crates/nidus-py/src/population.rs) (new).

Python helpers: `nidus.Population.from_scenario(scenario, n=200)`,
`.stratify('maternal.cardio.baseline_map_mmhg', levels=[80, 90, 100])`,
`.run() -> PopulationResult`,
`PopulationResult.outcome_by_stratum(quantity, at_age_weeks)` returns
a dataframe.

### Prompt 10.8 — Worked example: MAP → growth restriction

File: new [`examples/map_to_growth_restriction.ipynb`](../examples/map_to_growth_restriction.ipynb).

Stratifies maternal MAP across population, runs 500 individuals per
stratum, plots the fraction of growth-restricted fetuses (< 10th
percentile at 36 wk) vs maternal MAP. The point of the example is to
show how Nidus produces population-level inferences with explicit
tier propagation.

### Prompt 10.9 — Documentation

File: new
[`docs/tutorials/population_modeling.md`](../docs/tutorials/population_modeling.md).

Covers: when to use point vs population scenarios, how draws are
made, the determinism contract for ensembles, the cohort system,
and the stratified-analysis API.

## Acceptance for Spec 10

- [ ] `nidus run --n-individuals 100` produces a population summary.
- [ ] Same seed produces byte-identical population draws on Linux
  and macOS.
- [ ] At least two population-level validation cases pass.
- [ ] Cohort files for four standard subgroups exist with cited
  parameter overrides.
- [ ] Python ergonomic helpers exist.
- [ ] Documentation links from `docs/README.md`.
