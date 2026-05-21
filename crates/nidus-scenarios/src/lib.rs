//! Scenario configuration and orchestration.
//!
//! A scenario is the declarative description of a simulation run:
//! starting and ending gestational age, the RNG seed, the recording
//! cadence, and the set of subscribers to register. Scenarios are
//! written as TOML files so researchers can compose custom runs by
//! editing parameters or inheriting from a built-in scenario without
//! recompiling.
//!
//! Version 0.1.0 ships:
//!
//! - [`spec::ScenarioSpec`] — the in-memory representation of a
//!   scenario file, with TOML serde derived.
//! - [`spec::load_scenario_from_str`] / [`spec::load_scenario_from_path`]
//!   loaders.
//! - [`orchestrator::ScenarioOrchestrator`] — wires the maternal,
//!   placenta, and fetal subscribers into a [`nidus_core::Dispatcher`]
//!   and advances it to the scenario's end.
//! - [`builtin::NORMAL_TERM_PREGNANCY`], a pre-built scenario string
//!   suitable for `cargo test` and for the CLI's `--scenario` argument.
//!
//! The full library of built-in scenarios named in SPEC.md §7 (normal,
//! gestational diabetes, preeclampsia, IUGR, extremes of maternal age)
//! is the human-contributor follow-up; the loader and orchestrator do
//! not depend on it.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod builtin;
pub mod orchestrator;
pub mod spec;

pub use orchestrator::{ScenarioOrchestrator, ScenarioReport};
pub use spec::{
    load_scenario_from_path, load_scenario_from_str, FetalCirculationOverrides,
    MaternalCardioOverrides, Overrides, PlacentaGasOverrides, PlacentaStructureOverrides,
    ScenarioError, ScenarioSpec,
};
