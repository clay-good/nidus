//! Tick dispatcher.
//!
//! The dispatcher owns the [`TickClock`], the [`RngService`], and the
//! set of registered subscribers, and it is the single entry point for
//! advancing the simulation forward. Each call to [`Dispatcher::step`]
//! advances the clock by one engine second and invokes every subscriber
//! whose tier has a boundary at the new tick — in fine-to-coarse order
//! (`Second` → `Minute` → `Hour` → `Day`), matching the accumulation
//! diagram in SPEC.md §6.
//!
//! Subscribers are stored in a [`BTreeMap`] keyed by [`SubscriberId`],
//! which gives the dispatcher a deterministic iteration order
//! independent of registration sequence. Combined with the RNG service's
//! per-(subscriber, tick) keying, this is what makes the engine
//! reordering-stable: adding a new subscriber, or registering existing
//! ones in a different order, does not perturb the random numbers any
//! other subscriber observes.

use alloc::collections::BTreeMap;

use crate::clock::{GestationalAge, TickClock, TickTier};
use crate::rng::RngService;
use crate::snapshot::Snapshot;
use crate::subscriber::{Subscriber, SubscriberId, TickContext};

extern crate alloc;

/// Owns the clock, the RNG service, and all registered subscribers.
pub struct Dispatcher {
    clock: TickClock,
    rng: RngService,
    subscribers: BTreeMap<SubscriberId, Box<dyn Subscriber>>,
}

impl Dispatcher {
    /// Construct a dispatcher with no subscribers.
    pub fn new(start_age: GestationalAge, rng: RngService) -> Self {
        Self {
            clock: TickClock::new(start_age),
            rng,
            subscribers: BTreeMap::new(),
        }
    }

    /// Restore a dispatcher from a snapshot. No subscribers are
    /// registered automatically; the caller is responsible for
    /// re-attaching them in the same configuration they had before the
    /// snapshot was taken.
    pub fn from_snapshot(snapshot: Snapshot) -> Self {
        Self {
            clock: TickClock {
                start_age: snapshot.start_age,
                tick: snapshot.tick,
            },
            rng: RngService::new(snapshot.master_seed),
            subscribers: BTreeMap::new(),
        }
    }

    /// Register a subscriber. Replaces any existing subscriber with the
    /// same identifier and returns the displaced one if there was one.
    pub fn register(&mut self, subscriber: Box<dyn Subscriber>) -> Option<Box<dyn Subscriber>> {
        let id = subscriber.id().clone();
        self.subscribers.insert(id, subscriber)
    }

    /// Number of registered subscribers.
    #[must_use]
    pub fn subscriber_count(&self) -> usize {
        self.subscribers.len()
    }

    /// Current engine tick (seconds since simulation start).
    #[must_use]
    pub fn tick(&self) -> u64 {
        self.clock.tick
    }

    /// Current gestational age.
    #[must_use]
    pub fn current_age(&self) -> GestationalAge {
        self.clock.current_age()
    }

    /// Borrow the RNG service.
    #[must_use]
    pub fn rng(&self) -> &RngService {
        &self.rng
    }

    /// Capture engine state as a snapshot. The result is suitable for
    /// serialisation, transport to another machine, and later restoration
    /// via [`Dispatcher::from_snapshot`].
    #[must_use]
    pub fn snapshot(&self) -> Snapshot {
        Snapshot {
            start_age: self.clock.start_age,
            tick: self.clock.tick,
            master_seed: *self.rng.master_seed(),
        }
    }

    /// Advance the clock by one engine second and dispatch every
    /// subscriber whose tier boundary is crossed by the new tick.
    pub fn step(&mut self) {
        self.clock.step();
        let tick = self.clock.tick;
        let age = self.clock.current_age();

        for tier in TickTier::all_fine_to_coarse() {
            if !tier.is_boundary(tick) {
                continue;
            }
            for (id, sub) in &mut self.subscribers {
                if sub.tier() != tier {
                    continue;
                }
                let mut rng = self.rng.child_for(id, tick);
                let mut ctx = TickContext {
                    age,
                    tier,
                    tick,
                    rng: &mut rng,
                };
                sub.on_tick(&mut ctx);
            }
        }
    }

    /// Advance the clock by `seconds` engine seconds, stepping once per
    /// engine second. This is the right level of abstraction for callers
    /// running real scenarios; for advancing by physiological durations
    /// (a day, a week), multiply at the call site to keep the unit
    /// conversion explicit.
    pub fn advance_seconds(&mut self, seconds: u64) {
        for _ in 0..seconds {
            self.step();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::clock::{SECONDS_PER_DAY, SECONDS_PER_HOUR, SECONDS_PER_MINUTE};
    use core::cell::RefCell;
    use std::rc::Rc;

    /// Test subscriber that records (tier, tick, first RNG u64) on every
    /// invocation. The shared log lets two dispatchers compare their
    /// histories directly.
    struct Recorder {
        id: SubscriberId,
        tier: TickTier,
        log: SharedLog,
    }

    impl Subscriber for Recorder {
        fn id(&self) -> &SubscriberId {
            &self.id
        }
        fn tier(&self) -> TickTier {
            self.tier
        }
        fn on_tick(&mut self, ctx: &mut TickContext<'_>) {
            let r = ctx.rng.next_u64();
            self.log.borrow_mut().push((ctx.tier, ctx.tick, r));
        }
    }

    type LogEntry = (TickTier, u64, u64);
    type SharedLog = Rc<RefCell<Vec<LogEntry>>>;

    fn make_dispatcher(seed: u64) -> (Dispatcher, SharedLog) {
        let log = Rc::new(RefCell::new(Vec::new()));
        let mut disp = Dispatcher::new(GestationalAge::from_weeks(8), RngService::from_u64(seed));
        for (id, tier) in [
            ("alpha", TickTier::Second),
            ("beta", TickTier::Minute),
            ("gamma", TickTier::Hour),
            ("delta", TickTier::Day),
        ] {
            disp.register(Box::new(Recorder {
                id: SubscriberId::new(id),
                tier,
                log: log.clone(),
            }));
        }
        (disp, log)
    }

    #[test]
    fn same_seed_produces_identical_trajectory() {
        let (mut d1, log1) = make_dispatcher(123);
        let (mut d2, log2) = make_dispatcher(123);
        d1.advance_seconds(SECONDS_PER_DAY + 5);
        d2.advance_seconds(SECONDS_PER_DAY + 5);
        assert_eq!(*log1.borrow(), *log2.borrow());
        assert!(!log1.borrow().is_empty());
    }

    #[test]
    fn different_seeds_diverge() {
        let (mut d1, log1) = make_dispatcher(1);
        let (mut d2, log2) = make_dispatcher(2);
        d1.advance_seconds(120);
        d2.advance_seconds(120);
        assert_ne!(*log1.borrow(), *log2.borrow());
    }

    #[test]
    fn snapshot_and_resume_matches_continuous_run() {
        // Continuous run.
        let (mut cont, cont_log) = make_dispatcher(7);
        cont.advance_seconds(SECONDS_PER_HOUR + 100);

        // Run-snapshot-resume run.
        let (mut split, split_log) = make_dispatcher(7);
        split.advance_seconds(SECONDS_PER_MINUTE * 30);
        let snap = split.snapshot();
        let len_before = split_log.borrow().len();

        // Resume into a fresh dispatcher; re-register subscribers in a
        // *different* order to confirm reordering independence.
        let mut resumed = Dispatcher::from_snapshot(snap);
        let resumed_log = split_log.clone();
        for (id, tier) in [
            ("delta", TickTier::Day),
            ("gamma", TickTier::Hour),
            ("beta", TickTier::Minute),
            ("alpha", TickTier::Second),
        ] {
            resumed.register(Box::new(Recorder {
                id: SubscriberId::new(id),
                tier,
                log: resumed_log.clone(),
            }));
        }
        let remaining = SECONDS_PER_HOUR + 100 - SECONDS_PER_MINUTE * 30;
        resumed.advance_seconds(remaining);

        assert_eq!(*cont_log.borrow(), *split_log.borrow());
        // Sanity check that the split actually happened mid-run.
        assert!(len_before > 0 && len_before < cont_log.borrow().len());
    }

    #[test]
    fn fine_subscribers_fire_before_coarse_at_shared_boundary() {
        // At tick == SECONDS_PER_DAY all four tiers fire on the same step.
        let (mut disp, log) = make_dispatcher(0);
        disp.advance_seconds(SECONDS_PER_DAY);
        let final_step: Vec<_> = log
            .borrow()
            .iter()
            .filter(|(_, t, _)| *t == SECONDS_PER_DAY)
            .map(|(tier, _, _)| *tier)
            .collect();
        assert_eq!(
            final_step,
            vec![
                TickTier::Second,
                TickTier::Minute,
                TickTier::Hour,
                TickTier::Day,
            ]
        );
    }
}
