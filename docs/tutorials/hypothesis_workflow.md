# Tutorial: Hypothesis-Generation Workflow

End-to-end walkthrough of the hypothesis-generation layer described in
SPEC.md §10. The pipeline:

```
question → scenario → ensemble run → sensitivity analysis
                                   → divergence detection
                                   → experiment-design suggestions
```

The worked example is the one already shipping in the repository:
[`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](../../crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs).
Run it with:

```sh
cargo run --release -p nidus-hypothesis \
    --example sensitivity_placental_gas_exchange
```

This tutorial steps through what the example does and what each stage
of the pipeline produces.

## 1. The research question

"For fetal umbilical-vein PO₂ at term, which placental-transport
parameter — surface area, half-saturation surface area, or maximum
equilibration coefficient — would I most want to measure next?"

Three parameters, one outcome. Surface area sits at Tier B (mechanism
clear, magnitude uncertain); the other two are Tier C (the functional
form is a v0.1.0 modelling choice rather than a measured equation, so
the coefficients have no published value yet).

## 2. Defining the parameter specs

Each parameter becomes a [`ParameterSpec`](../../crates/nidus-hypothesis/src/ensemble.rs)
with a tier and a sampling strategy. Tier C parameters use
`Uniform` over their full plausible range; Tier B uses `Uniform`
narrowed to the measured uncertainty (or `Normal` if a measured
standard deviation is available).

```rust
use nidus_hypothesis::{ParameterSpec, SamplingStrategy};
use nidus_core::tier::ConfidenceTier;

let specs = vec![
    ParameterSpec::new(
        "surface_area_m2",
        ConfidenceTier::B,
        SamplingStrategy::Uniform { low: 9.0, high: 15.0 },
    ),
    ParameterSpec::new(
        "half_saturation_area_m2",
        ConfidenceTier::C,
        SamplingStrategy::Uniform { low: 1.5, high: 4.5 },
    ),
    ParameterSpec::new(
        "max_equilibration",
        ConfidenceTier::C,
        SamplingStrategy::Uniform { low: 0.20, high: 0.40 },
    ),
];
```

## 3. Sensitivity analysis

The [`SensitivityAnalyser`](../../crates/nidus-hypothesis/src/sensitivity.rs)
implements the Saltelli (2010) Sobol estimator. `N · (k + 2)` model
evaluations produce first-order and total-order indices per parameter
and the total outcome variance.

For the example model, running with `N = 4000` (≈ 20 000 evaluations)
takes <1 s on a laptop and produces results around:

| parameter                | tier | S_first | S_total |
| ------------------------ | ---- | ------- | ------- |
| `max_equilibration`      | C    | ≈ 0.55  | ≈ 0.92  |
| `half_saturation_area_m2`| C    | ≈ 0.03  | ≈ 0.09  |
| `surface_area_m2`        | B    | ≈ -0.03 | ≈ 0.02  |

`max_equilibration` drives almost all the outcome variance. The
`S_total − S_first` gap of about 0.37 means roughly a third of its
influence is via interactions with the other parameters.
`surface_area_m2`'s small total-order index reflects the fact that
the equilibration coefficient saturates well below the sampled
surface-area range — most movement happens in the small-area regime,
which the scenario's sampling window does not visit.

## 4. Divergence detection

If outcomes cluster into qualitatively different regimes,
[`DivergenceDetector`](../../crates/nidus-hypothesis/src/divergence.rs)
reports them. For the gas-exchange model this is not the case (the
output is unimodal across the sampled space), but the detector is
the right tool when the scenario is suspected to cross a regime
boundary — preeclampsia is a canonical example, where small changes
in placental physiology produce qualitatively different outcomes.

```rust
use nidus_hypothesis::{DivergenceDetector, EnsembleRunner};

let runner = EnsembleRunner::new(specs.clone(), 1000, 7);
let ensemble = runner.run(|s| { /* same model fn */ });
let divergence = DivergenceDetector::new().detect(&ensemble);
if divergence.is_multimodal {
    println!("multimodal: {} modes, separation {:.2}",
             divergence.modes.len(), divergence.separation_score);
}
```

Each detected mode carries a `parameter_signature`: the mean of every
input parameter inside that cluster. The signature is what surfaces
"this parameter is the switch."

## 5. Experiment-design suggestions

[`ExperimentDesignSuggester`](../../crates/nidus-hypothesis/src/experiment_design.rs)
turns the sensitivity result into a ranked list of suggestions.
Ranking key: descending `total_order · Var(Y)` (expected variance
reduction from measuring the parameter exactly), with ties broken so
less-confident tiers (D, then C) surface first.

For the gas-exchange model, the example prints:

```
Ranked experiment-design suggestions:
  1. max_equilibration [tier C] yield=13.87 current=0.28±0.10
  2. half_saturation_area_m2 [tier C] yield=1.28 current=3.0±1.5
  3. surface_area_m2 [tier B] yield=0.32 current=12.0±3.0
```

The output is intentionally not prescriptive. A researcher reads it
as: "constraining the maximum equilibration coefficient would buy
the most outcome-variance reduction; here is the parameter's current
estimate and the measurement techniques that exist for it." The
choice of which experiment to actually run depends on resources,
expertise, and broader scientific context that the suggester cannot
know.

## 6. Closing the loop

Once the experiment is run and the measurement is published, the
new value (and its citation) is contributed back to the parameter
database via the pull-request workflow in
[CONTRIBUTING.md](../../CONTRIBUTING.md) and
[`docs/contributing/parameter-pull-requests.md`](../contributing/parameter-pull-requests.md).
The next sensitivity-analysis run on the same scenario will see the
parameter as better-constrained and rank a different parameter as
the next most valuable measurement. This is the closing-the-loop
property described in SPEC.md §10.
