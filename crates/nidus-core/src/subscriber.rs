//! Subscribers: the protocol by which biological model components plug
//! into the engine's tick loop.
//!
//! A subscriber is anything that wants to be notified at the boundaries
//! of a particular [`TickTier`]. The engine knows nothing about what a
//! subscriber actually does; it only guarantees that subscribers are
//! invoked in a deterministic order at every tick boundary they care
//! about, with access to an independent RNG stream and the current
//! gestational age (SPEC.md §7).

use crate::clock::{GestationalAge, TickTier};
use crate::rng::ChildRng;

/// Stable identifier for a subscriber.
///
/// Subscriber identifiers are part of the engine's reproducibility
/// contract: the RNG service derives streams keyed by `SubscriberId`,
/// so two scenarios that register the same subscriber under the same ID
/// will see the same RNG output for that subscriber even if registration
/// order differs. Identifiers should be stable across releases, ideally
/// matching the crate and module path: e.g. `"nidus-maternal:cardio"`.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct SubscriberId(String);

impl SubscriberId {
    /// Construct a subscriber id from any string-like value.
    pub fn new(id: impl Into<String>) -> Self {
        Self(id.into())
    }

    /// Borrow the id as a string slice.
    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// Borrow the id as raw bytes (used by the RNG seed derivation).
    #[must_use]
    pub fn as_bytes(&self) -> &[u8] {
        self.0.as_bytes()
    }
}

impl From<&str> for SubscriberId {
    fn from(value: &str) -> Self {
        Self(value.to_owned())
    }
}

impl From<String> for SubscriberId {
    fn from(value: String) -> Self {
        Self(value)
    }
}

/// Context passed to a subscriber for the duration of a single
/// `on_tick` invocation.
pub struct TickContext<'a> {
    /// Current gestational age at the moment this tick fires.
    pub age: GestationalAge,
    /// Tier whose boundary this dispatch corresponds to.
    pub tier: TickTier,
    /// Engine tick counter in seconds (since simulation start).
    pub tick: u64,
    /// RNG stream owned by this subscriber for this tick.
    pub rng: &'a mut ChildRng,
}

/// The protocol a model component implements to receive tick callbacks.
///
/// Implementations should be free of hidden global state. Any random
/// draws they need should go through the provided [`ChildRng`]; any
/// time-dependent computation should consult `ctx.age`. These
/// constraints are what make the dispatcher's output bit-exact
/// reproducible across runs.
pub trait Subscriber {
    /// Stable identifier; must not change for the life of the simulation.
    fn id(&self) -> &SubscriberId;

    /// Tier at whose boundaries this subscriber wishes to be invoked.
    fn tier(&self) -> TickTier;

    /// Called at every boundary of [`Subscriber::tier`].
    fn on_tick(&mut self, ctx: &mut TickContext<'_>);
}
