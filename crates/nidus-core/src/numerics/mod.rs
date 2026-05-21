//! Fixed-point numerics for biological quantities.
//!
//! Bit-exact reproducibility across architectures (x86, ARM, WebAssembly)
//! requires that the simulation engine avoid floating-point arithmetic in
//! its core (SPEC.md §6). This module supplies a single underlying
//! [`Fixed`] type — signed 64-bit with 32 fractional bits ("Q32.32") —
//! and a family of typed newtype wrappers (`Mass`, `Pressure`,
//! `Volume`, `Concentration`, `Duration`, `Ratio`) that prevent
//! accidental cross-unit arithmetic at the type level.
//!
//! Conversions between fixed-point and floating-point are deliberately
//! restricted to the user-facing boundary: scenarios load their inputs
//! through `from_f64`, simulation steps are executed entirely in
//! fixed-point, and outputs are converted to `f64` only at observation
//! time. All internal arithmetic uses checked integer operations with
//! arithmetic-shift rounding (truncation toward negative infinity), so
//! every operation produces a bit-identical result regardless of host.
//!
//! Out-of-range inputs and overflowing operations return
//! [`OverflowError`] rather than silently wrapping; callers must decide
//! whether to saturate, panic, or propagate.

mod fixed;
mod quantities;

pub use fixed::{Fixed, OverflowError, FRAC_BITS};
pub use quantities::{Concentration, Duration, Mass, Pressure, Ratio, Volume};
