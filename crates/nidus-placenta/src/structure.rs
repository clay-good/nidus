//! Placental structural development: surface area as a function of
//! gestational age.
//!
//! The exchange surface area of the villous tree grows substantially
//! across gestation, from a few square metres at the start of the
//! second trimester to roughly twelve to fourteen square metres at
//! term. The trajectory is well-approximated by a logistic curve. The
//! coefficients here are scaffolding values pending integration with
//! the parameter database; they place the trajectory in the textbook
//! range but are not yet citation-resolved.

use nidus_core::clock::{GestationalAge, DAYS_PER_WEEK, SECONDS_PER_DAY};
use nidus_data::{DatabaseError, ParameterDatabase};

/// Database ids consumed by [`StructureParams::from_database`].
pub mod param_ids {
    /// Early-pregnancy villous surface area (m²).
    pub const INITIAL_AREA: &str = "placenta-structure-initial-area-m2";
    /// Term villous surface area (m²).
    pub const TERM_AREA: &str = "placenta-structure-term-area-m2";
    /// Gestational week of logistic-growth midpoint.
    pub const MIDPOINT_WEEK: &str = "placenta-structure-midpoint-week";
    /// Logistic growth-rate coefficient (1/week).
    pub const GROWTH_RATE: &str = "placenta-structure-growth-rate-per-week";
}

/// Coefficients describing the logistic surface-area trajectory.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct StructureParams {
    /// Surface area at week 0 (LMP-based), m². Small but non-zero so
    /// transport calculations remain numerically well-behaved at the
    /// extreme early end of the simulator's supported range.
    pub initial_area_m2: f64,
    /// Asymptotic term-pregnancy surface area, m².
    pub term_area_m2: f64,
    /// Gestational week at which the logistic curve crosses its
    /// midpoint.
    pub midpoint_week: f64,
    /// Steepness of the logistic curve at its midpoint.
    pub growth_rate_per_week: f64,
}

impl Default for StructureParams {
    fn default() -> Self {
        // Scaffolding constants. Each must be replaced with a
        // database-resolved citation-bearing parameter before
        // publication; see SPEC.md §9 and CONTRIBUTING.md.
        Self {
            initial_area_m2: 0.5,
            term_area_m2: 12.0,
            midpoint_week: 22.0,
            growth_rate_per_week: 0.20,
        }
    }
}

impl StructureParams {
    /// Construct from point-estimate values resolved against a loaded
    /// [`ParameterDatabase`].
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> {
        Ok(Self {
            initial_area_m2: db.point_estimate(param_ids::INITIAL_AREA)?,
            term_area_m2: db.point_estimate(param_ids::TERM_AREA)?,
            midpoint_week: db.point_estimate(param_ids::MIDPOINT_WEEK)?,
            growth_rate_per_week: db.point_estimate(param_ids::GROWTH_RATE)?,
        })
    }
}

/// Effective placental exchange surface area at gestational age `age`,
/// in square metres.
#[must_use]
pub fn placental_surface_area_m2(params: &StructureParams, age: GestationalAge) -> f64 {
    let w = age_in_weeks_f64(age);
    let z = -params.growth_rate_per_week * (w - params.midpoint_week);
    let frac = 1.0 / (1.0 + z.exp());
    params.initial_area_m2 + (params.term_area_m2 - params.initial_area_m2) * frac
}

#[allow(clippy::cast_precision_loss)]
fn age_in_weeks_f64(age: GestationalAge) -> f64 {
    let seconds_per_week = (DAYS_PER_WEEK * SECONDS_PER_DAY) as f64;
    (age.seconds as f64) / seconds_per_week
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn surface_area_is_monotonic_and_bounded() {
        let p = StructureParams::default();
        let mut prev = -f64::INFINITY;
        for w in [8u64, 16, 22, 28, 36, 40] {
            let a = placental_surface_area_m2(&p, GestationalAge::from_weeks(w));
            assert!(
                a > prev,
                "expected monotonic growth; w={w} a={a} prev={prev}"
            );
            prev = a;
            assert!(a >= p.initial_area_m2);
            assert!(a <= p.term_area_m2);
        }
    }

    #[test]
    fn term_value_is_near_textbook_range() {
        let p = StructureParams::default();
        let a40 = placental_surface_area_m2(&p, GestationalAge::from_weeks(40));
        // Textbook range for term placental exchange area is roughly
        // 10–15 m²; the scaffold lands inside this window.
        assert!((9.0..15.0).contains(&a40), "term area out of range: {a40}");
    }
}
