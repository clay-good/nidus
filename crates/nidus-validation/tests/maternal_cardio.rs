//! End-to-end validation demonstration.
//!
//! Exercises the full pipeline — case → probe → report — against the
//! maternal cardiovascular module. The "reference" dataset here is
//! synthetic, sized to match the textbook trajectory the model itself
//! is calibrated to, and clearly tagged as scaffolding pending a
//! human-contributed citation per CONTRIBUTING.md.

use nidus_core::citation::CitationId;
use nidus_core::clock::GestationalAge;
use nidus_core::rng::RngService;
use nidus_core::subscriber::SubscriberId;
use nidus_core::tier::ConfidenceTier;

use nidus_maternal::cardio::{MaternalCardio, SUBSCRIBER_ID};
use nidus_validation::{
    Agreement, ComponentLevel, ReferenceDataset, ReferencePoint, ValidationCase, ValidationSuite,
};

fn scaffold_reference() -> ReferenceDataset {
    // Textbook-style cardiac-output trajectory across pregnancy. Tagged
    // as scaffolding (`scaffold-template-source`); the
    // human-contributor task per SPEC.md §13 prompt 13 is to replace
    // this dataset with an entry citing the NICHD Fetal Growth Studies
    // or similarly verifiable longitudinal cohort.
    let points = vec![
        ReferencePoint::interval(12.0, 5.5, 1.0),
        ReferencePoint::interval(20.0, 6.5, 1.0),
        ReferencePoint::interval(28.0, 7.3, 1.0),
        ReferencePoint::interval(32.0, 7.5, 1.0),
        ReferencePoint::interval(36.0, 7.2, 1.0),
        ReferencePoint::interval(40.0, 6.8, 1.0),
    ];
    ReferenceDataset {
        id: "maternal-cardiac-output-scaffold".to_owned(),
        name: "Maternal cardiac output trajectory (scaffold)".to_owned(),
        citation: CitationId::new("scaffold-template-source"),
        units: "L/min".to_owned(),
        points,
    }
}

fn build_case() -> ValidationCase {
    ValidationCase {
        id: "case:maternal-cardio:cardiac-output".to_owned(),
        description: "Population-mean maternal cardiac output across pregnancy matches the \
             scaffold reference trajectory within ±1 L/min."
            .to_owned(),
        component: "nidus-maternal:cardio".to_owned(),
        tier: ConfidenceTier::B,
        level: ComponentLevel::Component,
        reference: scaffold_reference(),
        default_tolerance: 1.0,
    }
}

#[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
fn at_week(cardio: &MaternalCardio, week: f64) -> f64 {
    cardio
        .evaluate(GestationalAge::from_weeks(week as u64))
        .cardiac_output_l_per_min
}

#[test]
fn maternal_cardio_validates_against_scaffold_reference() {
    let mut svc_rng = RngService::from_u64(123).child_for(&SubscriberId::new(SUBSCRIBER_ID), 0);
    let cardio = MaternalCardio::with_default_params(&mut svc_rng);

    let mut suite = ValidationSuite::new();
    suite.push(build_case());

    let report = suite.run(|_, week| at_week(&cardio, week));

    assert_eq!(report.results.len(), 1);
    let r = &report.results[0];
    assert!(
        matches!(r.agreement, Agreement::Excellent | Agreement::Adequate),
        "expected good agreement with scaffold reference; got {:?}",
        r.agreement
    );
    // RMS residual under default scaffold parameters should be well
    // below the ±1 L/min half-width.
    assert!(
        r.rms_residual < 1.0,
        "RMS residual unexpectedly large: {}",
        r.rms_residual
    );
}

#[test]
fn renders_markdown_report() {
    let mut svc_rng = RngService::from_u64(123).child_for(&SubscriberId::new(SUBSCRIBER_ID), 0);
    let cardio = MaternalCardio::with_default_params(&mut svc_rng);
    let mut suite = ValidationSuite::new();
    suite.push(build_case());
    let report = suite.run(|_, week| at_week(&cardio, week));
    let md = report.render_markdown();
    assert!(md.contains("Validation Report"));
    assert!(md.contains("nidus-maternal:cardio"));
}

#[test]
fn tier_c_case_is_marked_unvalidatable() {
    // A Tier C case is included for completeness; the framework must
    // recognise it as unvalidatable rather than passing or failing.
    let mut suite = ValidationSuite::new();
    suite.push(ValidationCase {
        id: "case:unknown:cortisol-hpa".to_owned(),
        description: "Maternal-cortisol diurnal effect on fetal HPA axis".to_owned(),
        component: "nidus-unknown:cortisol-hpa".to_owned(),
        tier: ConfidenceTier::C,
        level: ComponentLevel::Component,
        reference: ReferenceDataset {
            id: "no-such-reference".to_owned(),
            name: "Tier-C placeholder".to_owned(),
            citation: CitationId::new("scaffold-template-source"),
            units: "dimensionless".to_owned(),
            points: vec![ReferencePoint::interval(20.0, 1.0, 0.1)],
        },
        default_tolerance: 0.1,
    });
    let report = suite.run(|_, _| 999.0);
    assert_eq!(report.results[0].agreement, Agreement::Unvalidatable);
}
