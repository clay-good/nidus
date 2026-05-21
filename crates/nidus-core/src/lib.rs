//! Deterministic simulation engine for Nidus.
//!
//! `nidus-core` provides the substrate on which the biological model layer
//! is built: confidence tiers, citations, tiered values, the hierarchical
//! tick clock, the seeded RNG service, the subscriber dispatcher, and the
//! snapshot mechanism. The crate is intentionally biology-free; it knows
//! about ticks, state, randomness, and observers, but not about placentas
//! or fetuses (see SPEC.md §7).
//!
//! The two most important commitments encoded here are:
//!
//! - **Tier propagation.** Every modelled quantity carries an explicit
//!   confidence tier, and derived quantities cannot be more confident than
//!   their least-confident input (SPEC.md §3).
//! - **Bit-exact reproducibility.** The same scenario with the same seed
//!   produces identical output on every run, with snapshot-and-resume
//!   yielding identical trajectories to continuous simulation (SPEC.md §6).

#![cfg_attr(not(test), warn(missing_docs))]

pub mod citation;
pub mod clock;
pub mod dispatcher;
pub mod numerics;
pub mod rng;
pub mod snapshot;
pub mod subscriber;
pub mod tier;
pub mod tiered;

pub use citation::{Citation, CitationId};
pub use clock::{GestationalAge, TickClock, TickTier};
pub use dispatcher::Dispatcher;
pub use numerics::{Concentration, Duration, Fixed, Mass, OverflowError, Pressure, Ratio, Volume};
pub use rng::{ChildRng, RngService, RngStreamId};
pub use snapshot::Snapshot;
pub use subscriber::{Subscriber, SubscriberId};
pub use tier::ConfidenceTier;
pub use tiered::Tiered;
