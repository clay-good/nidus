//! Seeded RNG service.
//!
//! The engine is deterministic given a seed and a scenario: the same seed
//! produces the same trajectory, run-to-run and across architectures
//! (SPEC.md §7). The RNG service achieves this by holding a single
//! 32-byte master seed and deriving an independent `ChaCha20` child stream
//! for every (subscriber, tick) pair.
//!
//! Per-(subscriber, tick) derivation has two useful properties:
//!
//! 1. **Reordering independence.** Two subscribers' streams do not share
//!    state, so re-ordering subscribers (or adding new ones) does not
//!    perturb the random numbers an existing subscriber sees.
//! 2. **Trivial snapshotting.** No RNG state has to be serialised: a
//!    snapshot of (master seed, current tick) is sufficient to resume
//!    with bit-identical output.
//!
//! The seed-derivation function mixes the master seed with the
//! subscriber identifier and the tick counter through two `ChaCha20`
//! invocations. It is not a cryptographic KDF — it does not need to be —
//! but the output streams are independent for distinct
//! (subscriber, tick) pairs with overwhelming probability.

use rand_chacha::ChaCha20Rng;
use rand_core::{RngCore, SeedableRng};

use crate::subscriber::SubscriberId;

/// Identifies a derived RNG stream.
///
/// Streams are scoped to a `(SubscriberId, tick)` pair so that each
/// subscriber sees an independent random sequence at every tick boundary
/// it fires on.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct RngStreamId {
    /// Subscriber owning this stream.
    pub subscriber: SubscriberId,
    /// Engine tick (in seconds) at which the stream was derived.
    pub tick: u64,
}

/// A child RNG owned by a specific subscriber for the duration of one
/// tick. Calling code obtains one from [`RngService::child_for`] and
/// uses it for any random draws required by that tick's update.
pub struct ChildRng(ChaCha20Rng);

impl ChildRng {
    /// Return the next 64-bit value from the stream.
    pub fn next_u64(&mut self) -> u64 {
        self.0.next_u64()
    }

    /// Return the next 32-bit value from the stream.
    pub fn next_u32(&mut self) -> u32 {
        self.0.next_u32()
    }

    /// Fill the provided buffer with bytes from the stream.
    pub fn fill_bytes(&mut self, dest: &mut [u8]) {
        self.0.fill_bytes(dest);
    }

    /// Sample a uniform `f64` in `[0, 1)` using 53 bits of entropy.
    ///
    /// The construction follows the standard "bit-fiddle 64 random bits
    /// into a double in `[0, 1)`" pattern, kept explicit here so the
    /// output is reproducible across platforms regardless of the
    /// `rand` distribution machinery.
    #[allow(clippy::cast_precision_loss)]
    pub fn next_f64_unit(&mut self) -> f64 {
        // Take 53 high bits and divide by 2^53; both numerator and
        // denominator fit exactly in an f64 mantissa, so the result is
        // a bit-stable uniform draw in [0, 1).
        let bits = self.0.next_u64() >> 11;
        (bits as f64) / ((1_u64 << 53) as f64)
    }
}

/// Seeded RNG service for the simulation engine.
///
/// Holds the master seed and produces child generators on demand. The
/// service itself is stateless beyond the master seed, which makes
/// snapshot and resume trivial.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct RngService {
    /// 32-byte master seed.
    pub master_seed: [u8; 32],
}

impl RngService {
    /// Construct a service from a raw 32-byte seed.
    #[must_use]
    pub const fn new(master_seed: [u8; 32]) -> Self {
        Self { master_seed }
    }

    /// Construct a service from a `u64` seed, padded into 32 bytes.
    ///
    /// Convenient for tests and short scenario specifications. Production
    /// scenarios should provide an explicit 32-byte seed for full
    /// reproducibility across implementations.
    #[must_use]
    pub fn from_u64(seed: u64) -> Self {
        let mut master = [0u8; 32];
        master[..8].copy_from_slice(&seed.to_le_bytes());
        Self::new(master)
    }

    /// Borrow the master seed bytes.
    #[must_use]
    pub const fn master_seed(&self) -> &[u8; 32] {
        &self.master_seed
    }

    /// Derive a child RNG for the given (subscriber, tick) pair.
    ///
    /// Two calls with the same inputs return generators that produce
    /// identical sequences. Different inputs produce independent streams.
    pub fn child_for(&self, subscriber: &SubscriberId, tick: u64) -> ChildRng {
        ChildRng(ChaCha20Rng::from_seed(derive_seed(
            &self.master_seed,
            subscriber.as_bytes(),
            tick,
        )))
    }
}

/// Two-pass `ChaCha20`-based seed derivation.
///
/// Pass one keys `ChaCha20` with the master seed and produces a 32-byte
/// block to start with. Pass two folds the subscriber identifier and
/// tick counter into that block and re-keys `ChaCha20` to produce the
/// final child seed. The construction is deterministic, branch-free on
/// the inputs, and produces well-distributed output for distinct inputs.
fn derive_seed(master: &[u8; 32], subscriber_id: &[u8], tick: u64) -> [u8; 32] {
    let mut buf = [0u8; 32];
    {
        let mut rng = ChaCha20Rng::from_seed(*master);
        rng.fill_bytes(&mut buf);
    }
    for (i, b) in subscriber_id.iter().enumerate() {
        buf[i % 32] ^= *b;
    }
    let tick_bytes = tick.to_le_bytes();
    for (i, b) in tick_bytes.iter().enumerate() {
        buf[i] ^= *b;
    }
    // Length-prefix the subscriber id so that ids "abc" and "ab" + "c"
    // (impossible here but conceptually) cannot collide.
    let len_bytes = (subscriber_id.len() as u64).to_le_bytes();
    for (i, b) in len_bytes.iter().enumerate() {
        buf[(i + 8) % 32] ^= *b;
    }
    let mut out = [0u8; 32];
    let mut rng = ChaCha20Rng::from_seed(buf);
    rng.fill_bytes(&mut out);
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sub(id: &str) -> SubscriberId {
        SubscriberId::new(id)
    }

    #[test]
    fn same_seed_and_inputs_produce_identical_output() {
        let svc = RngService::from_u64(42);
        let mut a = svc.child_for(&sub("alpha"), 7);
        let mut b = svc.child_for(&sub("alpha"), 7);
        assert_eq!(a.next_u64(), b.next_u64());
        assert_eq!(a.next_u64(), b.next_u64());
    }

    #[test]
    fn different_subscribers_get_independent_streams() {
        let svc = RngService::from_u64(42);
        let mut a = svc.child_for(&sub("alpha"), 0);
        let mut b = svc.child_for(&sub("beta"), 0);
        assert_ne!(a.next_u64(), b.next_u64());
    }

    #[test]
    fn different_ticks_for_same_subscriber_get_independent_streams() {
        let svc = RngService::from_u64(42);
        let mut a = svc.child_for(&sub("alpha"), 0);
        let mut b = svc.child_for(&sub("alpha"), 1);
        assert_ne!(a.next_u64(), b.next_u64());
    }

    #[test]
    fn different_master_seeds_diverge() {
        let mut a = RngService::from_u64(1).child_for(&sub("x"), 0);
        let mut b = RngService::from_u64(2).child_for(&sub("x"), 0);
        assert_ne!(a.next_u64(), b.next_u64());
    }

    #[test]
    fn f64_unit_in_range() {
        let svc = RngService::from_u64(99);
        let mut rng = svc.child_for(&sub("u"), 0);
        for _ in 0..1024 {
            let x = rng.next_f64_unit();
            assert!((0.0..1.0).contains(&x));
        }
    }
}
