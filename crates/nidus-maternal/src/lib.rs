//! Maternal subsystem.
//!
//! This crate models the pregnant person as a coupled cardiovascular,
//! metabolic, endocrine, and immune system that adapts across pregnancy
//! (SPEC.md §7). Version 0.1.0 ships the cardiovascular component; the
//! metabolic, endocrine, and immune components are deferred to later
//! prompts.
//!
//! ### Cardiovascular state
//!
//! [`cardio::MaternalCardio`] produces maternal cardiac output, mean
//! arterial pressure, and uterine artery blood flow as functions of
//! gestational age, with per-individual stochastic offsets drawn from
//! the engine's seeded RNG. The trajectory shapes follow the canonical
//! pattern documented in maternal-fetal physiology textbooks:
//!
//! - **Cardiac output** rises from a non-pregnant baseline of about
//!   5 L/min, peaks at roughly 7–8 L/min near the start of the third
//!   trimester, then declines slightly toward term.
//! - **Mean arterial pressure** falls through the first half of
//!   pregnancy (the "mid-pregnancy nadir"), reaching its lowest values
//!   around 20–24 weeks, then rises gradually back toward non-pregnant
//!   values at term.
//! - **Uterine artery flow** rises monotonically from a small fraction
//!   of cardiac output at early gestation to several hundred mL/min at
//!   term.
//!
//! All trajectory constants in [`cardio`] are flagged scaffolding values
//! pending integration with the parameter database (`nidus-data`); the
//! ranges they produce are consistent with the literature, but they
//! must be replaced with database-resolved, citation-bearing values
//! before the model is used for published simulator output. See
//! CONTRIBUTING.md and SPEC.md §9.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod cardio;

pub use cardio::{MaternalCardio, MaternalCardioParams, MaternalCardioState};
