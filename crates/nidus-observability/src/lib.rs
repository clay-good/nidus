//! Telemetry, confidence-tier tracking, and data export for Nidus.
//!
//! The most important responsibility of the observability layer is the
//! visualisation of confidence tiers and uncertainty bands: charts
//! always show the tier of displayed quantities, always include
//! uncertainty intervals where applicable, and always allow the user
//! to trace any displayed value back to its underlying parameters and
//! citations (SPEC.md §7).
//!
//! Version 0.1.0 ships the *substrate* for that visualisation —
//! [`telemetry::TelemetryBus`], the [`telemetry::TelemetryEvent`]
//! record, and an NDJSON [`export::write_ndjson`] writer that turns a
//! bus into a streamable file. The interactive web dashboard
//! described in SPEC.md §13 prompt 15 is a separate frontend
//! deliverable explicitly deferred to v0.2; what's here is the data
//! pipeline that any frontend (browser, notebook, terminal) will
//! consume.
//!
//! ### Why a separate bus rather than direct dispatcher state
//!
//! The engine deliberately does not expose subscriber state to the
//! dispatcher (see `nidus-core::dispatcher`); subscribers own their
//! state. The telemetry bus is what subscribers, or the scenario
//! orchestrator on their behalf, push observations into so that the
//! observability layer can consume them without needing to reach into
//! subscriber internals.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod export;
pub mod telemetry;

pub use export::{write_ndjson, ExportError};
pub use telemetry::{TelemetryBus, TelemetryEvent, TelemetryValue};
