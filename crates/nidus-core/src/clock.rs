//! Gestational time and the tick tier hierarchy.
//!
//! Gestational age is measured from the first day of the last menstrual
//! period (LMP), which is the clinical convention. The engine advances
//! time in whole seconds and reports gestational age in days, weeks, or
//! hours as required by callers. Storing time as integer seconds is what
//! makes the engine bit-exact reproducible across hardware (SPEC.md §6).

use core::fmt;

/// One day in seconds.
pub const SECONDS_PER_DAY: u64 = 86_400;
/// One hour in seconds.
pub const SECONDS_PER_HOUR: u64 = 3_600;
/// One minute in seconds.
pub const SECONDS_PER_MINUTE: u64 = 60;
/// Days per gestational week.
pub const DAYS_PER_WEEK: u64 = 7;

/// Gestational age measured in whole seconds from the start of gestation.
///
/// "Start of gestation" follows the LMP-based clinical convention: a
/// pregnancy at 0 weeks 0 days has age zero, and term is at 40 weeks.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct GestationalAge {
    /// Seconds elapsed since the LMP-based start of gestation.
    pub seconds: u64,
}

impl GestationalAge {
    /// Construct an age from whole seconds.
    #[must_use]
    pub const fn from_seconds(seconds: u64) -> Self {
        Self { seconds }
    }

    /// Construct an age from a number of completed gestational weeks.
    #[must_use]
    pub const fn from_weeks(weeks: u64) -> Self {
        Self {
            seconds: weeks * DAYS_PER_WEEK * SECONDS_PER_DAY,
        }
    }

    /// Construct an age from completed weeks and additional days.
    #[must_use]
    pub const fn from_weeks_and_days(weeks: u64, days: u64) -> Self {
        Self {
            seconds: (weeks * DAYS_PER_WEEK + days) * SECONDS_PER_DAY,
        }
    }

    /// Completed gestational weeks.
    #[must_use]
    pub const fn completed_weeks(self) -> u64 {
        self.seconds / (DAYS_PER_WEEK * SECONDS_PER_DAY)
    }

    /// Completed gestational days.
    #[must_use]
    pub const fn completed_days(self) -> u64 {
        self.seconds / SECONDS_PER_DAY
    }

    /// Add a duration in seconds, saturating at `u64::MAX` rather than
    /// wrapping. Simulations never approach this bound in practice.
    #[must_use]
    pub const fn add_seconds(self, delta: u64) -> Self {
        Self {
            seconds: self.seconds.saturating_add(delta),
        }
    }
}

impl fmt::Display for GestationalAge {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let weeks = self.completed_weeks();
        let days = (self.seconds / SECONDS_PER_DAY) % DAYS_PER_WEEK;
        write!(f, "{weeks}w{days}d")
    }
}

/// The four tiers of the hierarchical tick architecture.
///
/// Each tier corresponds to a characteristic physiological timescale and
/// fires at a fixed period in engine seconds. The full mapping from
/// physiology to tier is described in SPEC.md §6.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum TickTier {
    /// Fires every simulated second. Cardiac dynamics, fast transport.
    Second,
    /// Fires every simulated minute. Metabolic adjustments, fast feedback.
    Minute,
    /// Fires every simulated hour. Hormonal shifts, perfusion changes.
    Hour,
    /// Fires every simulated day. Growth, developmental milestones.
    Day,
}

impl TickTier {
    /// Period of this tier in engine seconds.
    #[must_use]
    pub const fn period_seconds(self) -> u64 {
        match self {
            Self::Second => 1,
            Self::Minute => SECONDS_PER_MINUTE,
            Self::Hour => SECONDS_PER_HOUR,
            Self::Day => SECONDS_PER_DAY,
        }
    }

    /// Whether the given tick count (in engine seconds) is a boundary for
    /// this tier — i.e. whether subscribers at this tier should fire.
    #[must_use]
    pub const fn is_boundary(self, tick: u64) -> bool {
        tick % self.period_seconds() == 0
    }

    /// Iteration order from finest to coarsest. The dispatcher fires
    /// subscribers in this order at every step so that finer-grained
    /// dynamics accumulate into the state visible to coarser tiers.
    #[must_use]
    pub const fn all_fine_to_coarse() -> [Self; 4] {
        [Self::Second, Self::Minute, Self::Hour, Self::Day]
    }
}

/// Engine clock: gestational-age reference plus an integer tick counter.
///
/// The tick counter measures simulated seconds since the engine's start
/// (not since the LMP). `tick == 0` is the moment the simulation began;
/// the initial gestational age (e.g. 8 weeks) is recorded in `start_age`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct TickClock {
    /// Gestational age at the moment `tick == 0`.
    pub start_age: GestationalAge,
    /// Engine seconds elapsed since the start of the simulation.
    pub tick: u64,
}

impl TickClock {
    /// Construct a clock that begins at the given gestational age.
    #[must_use]
    pub const fn new(start_age: GestationalAge) -> Self {
        Self { start_age, tick: 0 }
    }

    /// Current gestational age (start age plus elapsed ticks).
    #[must_use]
    pub const fn current_age(&self) -> GestationalAge {
        self.start_age.add_seconds(self.tick)
    }

    /// Advance the clock by one engine second.
    pub fn step(&mut self) {
        self.tick = self.tick.saturating_add(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn gestational_age_round_trips_weeks_and_days() {
        let age = GestationalAge::from_weeks_and_days(28, 3);
        assert_eq!(age.completed_weeks(), 28);
        assert_eq!(age.completed_days(), 28 * 7 + 3);
        assert_eq!(format!("{age}"), "28w3d");
    }

    #[test]
    fn tier_boundaries_align_with_period() {
        assert!(TickTier::Second.is_boundary(0));
        assert!(TickTier::Second.is_boundary(1));
        assert!(TickTier::Minute.is_boundary(0));
        assert!(TickTier::Minute.is_boundary(60));
        assert!(!TickTier::Minute.is_boundary(59));
        assert!(TickTier::Day.is_boundary(SECONDS_PER_DAY));
        assert!(!TickTier::Day.is_boundary(SECONDS_PER_DAY - 1));
    }

    #[test]
    fn clock_advances_one_second_per_step() {
        let mut clock = TickClock::new(GestationalAge::from_weeks(8));
        let start = clock.current_age();
        clock.step();
        assert_eq!(clock.tick, 1);
        assert_eq!(clock.current_age().seconds, start.seconds + 1);
    }
}
