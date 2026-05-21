//! Engine-level snapshot.
//!
//! A [`Snapshot`] captures the engine's reproducibility-relevant state at
//! a tick boundary: the gestational age the simulation started at, the
//! current engine tick, and the RNG master seed. Because the engine
//! derives RNG streams from `(master_seed, subscriber_id, tick)` rather
//! than maintaining incremental RNG state, no additional state is needed
//! to resume bit-identically (see [`crate::rng`] for the design rationale
//! and [`crate::dispatcher`] for the round-trip test).
//!
//! Biological state owned by individual subscribers is not part of the
//! engine-level snapshot; those snapshots are the subscribers' own
//! responsibility, layered on top of this one.

use crate::clock::GestationalAge;

/// Engine state snapshot.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Snapshot {
    /// Gestational age at the moment the simulation started (`tick == 0`).
    pub start_age: GestationalAge,
    /// Engine tick (seconds since simulation start) at the moment of
    /// capture.
    pub tick: u64,
    /// 32-byte master seed used by the RNG service.
    pub master_seed: [u8; 32],
}
