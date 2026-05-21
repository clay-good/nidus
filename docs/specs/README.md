# Nidus Specifications

## Current direction (ACTIVE)

The current direction is captured in [`v0.3/`](v0.3/).

| Spec | File                                                                | Status                                                                |
| ---- | ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 00   | [`v0.3/00-overview.md`](v0.3/00-overview.md)            | **READ FIRST.** What we are doing and why.                            |
| 01   | [`v0.3/01-dataset-and-dashboard.md`](v0.3/01-dataset-and-dashboard.md) | **Active.** Dataset + Python package + Streamlit dashboard. Primary work. |
| 02   | [`v0.3/02-sbml-cellml-export.md`](v0.3/02-sbml-cellml-export.md)       | **Conditional.** Only if Spec 01 sees adoption signal.                |
| 03   | [`v0.3/03-outreach-and-essay.md`](v0.3/03-outreach-and-essay.md)       | **Active.** Blog essay on claygood.com + Zenodo deposit.              |

## Superseded (deprecation stubs)

The following specs were written during the earlier Rust-prototype phase and are superseded by the v0.3 design. Each file is a one-paragraph deprecation stub pointing here. Original content lives in git history (`git log -- docs/specs/<filename>`).

| File                                                                  | Original intent                              |
| --------------------------------------------------------------------- | -------------------------------------------- |
| [`SPEC.md`](SPEC.md)                                                  | Original Rust simulator design.              |
| [`SPEC_V0.2.md`](SPEC_V0.2.md)                                        | v0.2 simulator roadmap.                      |
| [`01-parameter-database.md`](01-parameter-database.md)                | Simulator parameter database work stream.    |
| [`02-subsystem-completion.md`](02-subsystem-completion.md)            | Simulator subsystem completion.              |
| [`03-validation-suite.md`](03-validation-suite.md)                    | Simulator validation suite.                  |
| [`04-python-bindings.md`](04-python-bindings.md)                      | PyO3 bindings to Rust kernel.                |
| [`05-dashboard.md`](05-dashboard.md)                                  | Simulator-era dashboard.                     |
| [`06-cli-and-reproducibility.md`](06-cli-and-reproducibility.md)      | `nidus run` Rust CLI.                        |
| [`07-examples-and-tutorials.md`](07-examples-and-tutorials.md)        | Simulator examples/tutorials.                |
| [`08-distribution.md`](08-distribution.md)                            | Simulator distribution / release.            |
| [`09-testing-and-ci.md`](09-testing-and-ci.md)                        | Simulator-era testing/CI.                    |
| [`10-population-modeling.md`](10-population-modeling.md)              | Cohort sampling in the simulator.            |
| [`11-hypothesis-generalization.md`](11-hypothesis-generalization.md)  | Hypothesis pipeline generalisation.          |
| [`12-code-hygiene.md`](12-code-hygiene.md)                            | Rust code hygiene.                           |

These were written when nidus was conceived as a Rust simulator of coupled maternal-placental-fetal physiology. That direction was determined to be misaligned with both the audience (perinatal researchers, almost all Python/R users) and the impact pathway (existing mechanistic modelling is well-served by CellML, COPASI, PhysioCell). See [`v0.3/00-overview.md`](v0.3/00-overview.md) for the full reasoning.
