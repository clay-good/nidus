# Tutorials

The tutorials below mirror SPEC.md §13 prompt 17 and are the
researcher-facing entry points to the simulator. The first three are
working v0.1.0 walkthroughs; the rest are planned and will be filled in
as the underlying components mature.

## Quickstart: run the built-in scaffold scenario

```sh
cargo run -p nidus-cli -- run > out.json
```

The output is a JSON document with one `samples` entry per recording
boundary (default: one per day, from week 8 through week 40). Every
recorded quantity is in textbook units. The scaffold scenario uses
constants that are inside textbook ranges but are not yet
citation-resolved; see [CONTRIBUTING.md](../../CONTRIBUTING.md) for
how parameter authoring works.

## Author a custom scenario

Copy `scenarios/normal_term_pregnancy.toml` and edit:

- `start_age_weeks`, `end_age_weeks` — pregnancy window (8 ≤ start <
  end ≤ 40).
- `seed` — master RNG seed.
- `record_every_seconds` — recording cadence; smaller values give
  finer-grained reports.
- `subscribers` — any subset of `["maternal-cardio", "placenta",
  "fetal"]`.

Validate before running:

```sh
cargo run -p nidus-cli -- validate-config path/to/scenario.toml
```

## Sensitivity analysis on the placental gas-exchange model

The `nidus-hypothesis` crate exposes the ensemble runner and the
Saltelli Sobol estimator. See the worked example in
[`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](../../crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs):
parameters are placental surface area, the half-saturation area, and
the max equilibration coefficient; the analysed outcome is the fetal
umbilical-vein PO₂ at term. The example demonstrates the full path
from `ParameterSpec`-list → `SensitivityResult` → ranked
`ExperimentSuggestion`s.

## Unknown channel exploration

See [`unknown_channels.md`](unknown_channels.md). Demonstrates the
three modes — `Disabled`, `Fixed`, `Sample` — against the four
standard channels in `ChannelRegistry::standard_v0_1`, and explains
which mode is the right tool for which research question.

## Hypothesis-generation workflow

See [`hypothesis_workflow.md`](hypothesis_workflow.md). End to end:
define a scenario, run an ensemble, run sensitivity analysis, run
divergence detection, read the experiment-design suggestions, design
a measurement. Uses the bundled placental gas-exchange example.

## Contributing a parameter update

See [`contributing_parameter.md`](contributing_parameter.md). Worked
walkthrough of the pull-request workflow: adding the citation,
adding (or updating) the parameter, choosing the tier, updating the
changelog, and closing the loop with the next sensitivity-analysis
run.
