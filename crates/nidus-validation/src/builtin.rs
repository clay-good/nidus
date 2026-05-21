//! Built-in validation cases.
//!
//! v0.1.0 shipped exactly one case — the maternal cardiac-output
//! trajectory against a textbook-shaped reference — so the `nidus
//! validate` CLI has something to run end-to-end out of the box.
//! Populating the suite with additional verified citations against
//! NICHD Fetal Growth Studies, placental Doppler flow ranges, and fetal
//! cardiovascular developmental data is the human-contributor follow-up
//! named in SPEC.md §13 prompt 13. See [`crate`] documentation for the
//! contract.

use nidus_core::citation::CitationId;
use nidus_core::tier::ConfidenceTier;

use crate::suite::{ComponentLevel, ReferenceDataset, ReferencePoint, ValidationCase};

/// Build the maternal cardiac-output scaffold case.
///
/// The trajectory points (12–40 weeks) sit in the textbook range the
/// `nidus-maternal` cardio module is calibrated to; the case is tagged
/// Tier B because the longitudinal CO trajectory shape is
/// well-characterised in the literature (Mahendru 2014) even though
/// individual reference points are summary values rather than
/// point-by-point reproductions of any single cohort.
#[must_use]
pub fn maternal_cardio_scaffold_case() -> ValidationCase {
    let points = vec![
        ReferencePoint::interval(12.0, 5.5, 1.0),
        ReferencePoint::interval(20.0, 6.5, 1.0),
        ReferencePoint::interval(28.0, 7.3, 1.0),
        ReferencePoint::interval(32.0, 7.5, 1.0),
        ReferencePoint::interval(36.0, 7.2, 1.0),
        ReferencePoint::interval(40.0, 6.8, 1.0),
    ];
    let reference = ReferenceDataset {
        id: "maternal-cardiac-output-trajectory".to_owned(),
        name: "Maternal cardiac output trajectory".to_owned(),
        citation: CitationId::new("mahendru-2014-cardiac-output"),
        units: "L/min".to_owned(),
        points,
    };
    ValidationCase {
        id: "case:maternal-cardio:cardiac-output".to_owned(),
        description: "Population-mean maternal cardiac output across pregnancy matches the \
                      reference trajectory within ±1 L/min."
            .to_owned(),
        component: "nidus-maternal:cardio".to_owned(),
        tier: ConfidenceTier::B,
        level: ComponentLevel::Component,
        reference,
        default_tolerance: 1.0,
    }
}

/// All built-in validation cases shipped with the crate.
#[must_use]
pub fn built_in_cases() -> Vec<ValidationCase> {
    vec![maternal_cardio_scaffold_case()]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn built_in_suite_is_non_empty() {
        let cases = built_in_cases();
        assert!(!cases.is_empty());
        assert!(cases.iter().any(|c| c.component.contains("maternal")));
    }
}
