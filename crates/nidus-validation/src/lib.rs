//! Validation suite.
//!
//! Validation is what makes Nidus credible as a scientific instrument
//! (SPEC.md §11). This crate provides the framework: types for
//! reference datasets, validation cases, agreement metrics, and a
//! report renderer. It also provides one end-to-end demonstration that
//! exercises every layer against the maternal cardiovascular model.
//!
//! Three levels of granularity are supported, matching the prose
//! specification:
//!
//! - **Component-level cases** check one model component against one
//!   published reference. Most cases live at this level.
//! - **Integration-level cases** check coupled subsystems against
//!   clinical observations (e.g. response to placental insufficiency).
//! - **Outcome-level cases** check ensemble distributions of outcomes
//!   against population-level distributions (e.g. birth-weight
//!   distribution).
//!
//! For v0.1.0 the component-level path is fully implemented; the other
//! two share the framework and will be wired in by later prompts.
//!
//! ### What this crate does not do
//!
//! The published reference datasets named in SPEC.md §13 prompt 13 —
//! NICHD Fetal Growth Studies, published placental Doppler flow
//! ranges, published fetal cardiovascular developmental data — are
//! not bundled with this crate. Including them with verified citations
//! is the human-contributor half of Prompt 13, parallel to the
//! parameter-authoring half of Prompt 5. The integration test in
//! `tests/maternal_cardio.rs` demonstrates the framework on a
//! synthetic reference dataset so contributors have a working example
//! to extend.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod builtin;
pub mod datasets;
pub mod report;
pub mod suite;

pub use builtin::{built_in_cases, maternal_cardio_scaffold_case};
pub use datasets::{load_from_str, Dataset, DatasetError, DatasetRow};
pub use report::{Agreement, ValidationReport, ValidationResult};
pub use suite::{
    ComponentLevel, ReferenceDataset, ReferencePoint, ValidationCase, ValidationSuite,
};
