# Spec 11 — Hypothesis Pipeline Generalisation

## Context

The v0.1 hypothesis pipeline is real but narrow:

- The only worked example is
  [`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](../crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs).
- `nidus hypothesis-report` (in
  [`crates/nidus-cli/src/main.rs:437-596`](../crates/nidus-cli/src/main.rs))
  hard-codes the placental gas exchange model — audit item 124.
- Experiment-design suggestions only exist for placental gas
  exchange — audit item 125.
- The divergence detector
  ([`crates/nidus-hypothesis/src/divergence.rs`](../crates/nidus-hypothesis/src/divergence.rs))
  only handles scalar outcomes — audit item 126.
- Unknown-channel supporting and questioning citations are empty
  vectors — audit items 45–46.

For a researcher to use the pipeline on the questions they actually
have, the engine needs to address any modelled quantity, propagate
unknown channels with real citation evidence, and rank experiments
across modalities. This spec broadens it.

## Deliverables

- `HypothesisModel` trait so any module can plug into the pipeline.
- Generic `nidus hypothesis-report --target <quantity>` working
  for every modelled quantity emitted by the system.
- Populated unknown-channel citation lists.
- Multivariate divergence detection.
- New experiment-design models for placental glucose flux, fetal
  growth, fetal cardiac output, maternal cardiovascular response.

## Dependencies

Requires Spec 01 (parameters), Spec 02 (modules), and Spec 06
(progress bars during long ensembles).

## Numbered prompts

### Prompt 11.1 — `HypothesisModel` trait

File: new
[`crates/nidus-hypothesis/src/model.rs`](../crates/nidus-hypothesis/src/model.rs).

```rust
pub trait HypothesisModel {
    fn id(&self) -> &str;
    fn name(&self) -> &str;
    fn parameters(&self) -> Vec<HypothesisParameter>;  // those that can be perturbed
    fn outcomes(&self) -> Vec<HypothesisOutcome>;       // measurable outputs
    fn run(&self, draw: &ParameterDraw, scenario: &Scenario) -> Vec<f64>;
    fn unknown_channels(&self) -> Vec<ChannelId>;       // upstream uncertainty
}
```

The existing placental gas exchange becomes one impl. Add impls for:
- `PlacentalGlucoseFluxModel`
- `MaternalCardioResponseModel`
- `FetalGrowthAtTermModel`
- `FetalCardiacOutputAtTermModel`

### Prompt 11.2 — CLI `--target` and `--model`

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs)
(specifically lines 437–596 currently hard-wired to placental gas
exchange).

Refactor `nidus hypothesis-report` to take `--model <id>` or
`--target <quantity>` (which resolves to the smallest set of models
that emit it) and `--n <samples>`. Dispatches into the trait from
11.1.

Verification: `nidus hypothesis-report --model
maternal_cardio_response --n 256 --format json` produces a ranked
list of parameters for maternal cardio.

### Prompt 11.3 — Multivariate divergence

File:
[`crates/nidus-hypothesis/src/divergence.rs`](../crates/nidus-hypothesis/src/divergence.rs).

Replace 1-D k-means with a configurable detector: k-means in N-D
with Mahalanobis distance, plus an alternative GMM detector with
BIC selection of cluster count. Document trade-offs in the module
doc.

Verification: a synthetic bimodal 3-D distribution is correctly
separated; the existing 1-D test still passes.

### Prompt 11.4 — Populate unknown-channel citations

File:
[`crates/nidus-unknown/src/registry.rs:260-326`](../crates/nidus-unknown/src/registry.rs).

For each of the four standard channels shipped today (and any new
ones added in Spec 02), populate the `supporting_citations` and
`questioning_citations` lists with real citation ids from
`data/citations/index.toml`. A channel with empty citation lists is
not a useful channel.

Verification: `nidus list channels --json` shows ≥ 2 supporting
and ≥ 1 questioning citation per channel; all ids resolve.

### Prompt 11.5 — Experiment-design across models

File:
[`crates/nidus-hypothesis/src/experiment_design.rs`](../crates/nidus-hypothesis/src/experiment_design.rs).

Generalise the ranking logic to be model-agnostic: input is a Sobol
ranking (total-effect indices) plus a measurability prior
(per-parameter cost-to-measure + ease-of-recruitment annotations
added to the database). Output is a ranked list with each entry
showing the parameter, current tier, expected reduction in target-
quantity variance, and the most-promising experimental modality.

Add the measurability prior as an optional field on
`ParameterEntry` (Spec 01 schema extension), defaulting to
"unknown."

Verification: the hypothesis report output now lists per-parameter
rationale that references the measurability prior.

### Prompt 11.6 — Cross-model hypothesis ranking

File:
[`crates/nidus-hypothesis/src/cross_model.rs`](../crates/nidus-hypothesis/src/cross_model.rs)
(new).

Given a research goal expressed as a target outcome
("reduce uncertainty in 36-wk fetal weight"), aggregate Sobol
rankings across every model whose outcome set includes that
quantity, weighted by tier confidence. Returns a single ranked list.

`nidus hypothesis-report --target fetal.growth.weight_g_at_36w`
uses this.

### Prompt 11.7 — Hypothesis report rendering

File:
[`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs).

Extend the Markdown form to include:
- Target outcome and its current tier.
- Top-K parameters by total-effect index, with each parameter's
  current tier, expected variance reduction, and recommended
  experimental modality.
- Linked unknown channels and their citation evidence.
- A JSON schema sibling (`docs/hypothesis-report-schema.md`).

### Prompt 11.8 — Python hypothesis API

File: [`crates/nidus-py/src/hypothesis.rs`](../crates/nidus-py/src/hypothesis.rs)
(already created in Spec 04).

Surface the trait: `nidus.hypothesis.models()` lists available
models; `nidus.hypothesis.report(target=..., n=...)` returns a
dataframe with the ranking.

### Prompt 11.9 — Worked examples

File: new
[`crates/nidus-hypothesis/examples/sensitivity_fetal_growth.rs`](../crates/nidus-hypothesis/examples/sensitivity_fetal_growth.rs)
and
[`crates/nidus-hypothesis/examples/sensitivity_maternal_cardio.rs`](../crates/nidus-hypothesis/examples/sensitivity_maternal_cardio.rs).

Mirror the structure of the placental gas exchange example but for
two new models.

### Prompt 11.10 — Hypothesis workflow tutorial refresh

File: [`docs/tutorials/hypothesis_workflow.md`](../docs/tutorials/hypothesis_workflow.md).

Update to reflect the generalised pipeline: how to pick a target,
how to interpret the ranking, how the unknown channels and
measurability prior shape recommendations.

## Acceptance for Spec 11

- [ ] `HypothesisModel` trait defined; ≥ 5 impls.
- [ ] `nidus hypothesis-report --target <quantity>` works for every
  modelled quantity emitted in the bundled scenarios.
- [ ] Multivariate divergence detector available, with tests.
- [ ] Every standard unknown channel has ≥ 2 supporting and ≥ 1
  questioning citation.
- [ ] Experiment-design output cites measurability prior.
- [ ] Python `hypothesis.report` returns a dataframe with rankings.
- [ ] Refreshed tutorial executes verbatim.
