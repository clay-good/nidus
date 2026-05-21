//! Maternal haemodynamics adapter: Mahendru 2014 cardiac-output
//! trajectory.
//!
//! Bundles `data/validation/maternal_hemodynamics.toml` via
//! `include_str!` and parses it on first access. The cohort is a
//! healthy-nulliparous longitudinal study (Mahendru AA et al.,
//! J Hypertens 2014;32(4):849-856).

use std::sync::OnceLock;

use super::{cached, Dataset};

const RAW: &str = include_str!("../../../../data/validation/maternal_hemodynamics.toml");

/// Mahendru 2014 longitudinal cardiac-output trajectory.
///
/// The returned reference is cached for the lifetime of the process;
/// subsequent calls re-use the parsed value.
pub fn dataset() -> &'static Dataset {
    static CELL: OnceLock<Dataset> = OnceLock::new();
    cached("maternal_hemodynamics", RAW, &CELL)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn loads_and_caches_bundled_toml() {
        let d = dataset();
        assert_eq!(d.unit, "L/min");
        assert!(!d.rows.is_empty());
        // Mahendru's CO trajectory: monotone rise into the early
        // third trimester, then modest decline toward term.
        let early = d
            .rows
            .iter()
            .find(|r| (r.age_weeks - 12.0).abs() < 1e-9)
            .unwrap();
        let peak = d
            .rows
            .iter()
            .find(|r| (r.age_weeks - 32.0).abs() < 1e-9)
            .unwrap();
        let term = d
            .rows
            .iter()
            .find(|r| (r.age_weeks - 40.0).abs() < 1e-9)
            .unwrap();
        assert!(peak.mean > early.mean);
        assert!(peak.mean > term.mean);
    }

    #[test]
    fn second_call_returns_same_pointer() {
        let a = dataset() as *const Dataset;
        let b = dataset() as *const Dataset;
        assert_eq!(a, b, "cached references must reuse the same allocation");
    }
}
