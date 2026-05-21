//! Validation suite: types for reference datasets and validation cases.

use nidus_core::citation::CitationId;
use nidus_core::tier::ConfidenceTier;

/// One reference data point.
#[derive(Debug, Clone, PartialEq)]
pub struct ReferencePoint {
    /// Gestational week at which the reference value was measured.
    pub gestational_week: f64,
    /// Reference value.
    pub value: f64,
    /// Symmetric half-width of the reference interval, if reported.
    /// `None` if the source provides only a point estimate.
    pub uncertainty: Option<f64>,
}

impl ReferencePoint {
    /// Construct a point with no uncertainty.
    #[must_use]
    pub fn point(week: f64, value: f64) -> Self {
        Self {
            gestational_week: week,
            value,
            uncertainty: None,
        }
    }

    /// Construct a point with a symmetric uncertainty half-width.
    #[must_use]
    pub fn interval(week: f64, value: f64, half_width: f64) -> Self {
        Self {
            gestational_week: week,
            value,
            uncertainty: Some(half_width),
        }
    }

    /// `true` iff `simulator_value` lies inside this point's reference
    /// interval. With no uncertainty, the comparison falls back to
    /// `tolerance`-based agreement.
    #[must_use]
    pub fn contains(&self, simulator_value: f64, tolerance: f64) -> bool {
        let half = self.uncertainty.unwrap_or(tolerance);
        (simulator_value - self.value).abs() <= half
    }
}

/// One reference dataset (a series of measurements at varying
/// gestational ages).
#[derive(Debug, Clone, PartialEq)]
pub struct ReferenceDataset {
    /// Stable identifier (kebab-case).
    pub id: String,
    /// Human-readable name.
    pub name: String,
    /// Citation for the published source. References an entry in
    /// `nidus-data`'s citation index.
    pub citation: CitationId,
    /// Free-text units, mirroring the parameter database schema.
    pub units: String,
    /// Reference points in order of gestational week.
    pub points: Vec<ReferencePoint>,
}

/// At what level of the model is this case asserting agreement?
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ComponentLevel {
    /// One model component against one reference dataset.
    Component,
    /// Coupled subsystems against a clinical observation.
    Integration,
    /// Ensemble distribution against a population-level distribution.
    Outcome,
}

/// One validation case.
#[derive(Debug, Clone)]
pub struct ValidationCase {
    /// Stable identifier.
    pub id: String,
    /// Human-readable description of what the case asserts.
    pub description: String,
    /// Module or subsystem the case validates (free-text, e.g.
    /// `"nidus-maternal:cardio"`).
    pub component: String,
    /// Confidence tier the case operates at. Tier C and D content
    /// cannot be validated against reference data by definition; cases
    /// at those tiers are accepted but the framework reports them as
    /// `Unvalidatable` rather than passing or failing.
    pub tier: ConfidenceTier,
    /// Component level.
    pub level: ComponentLevel,
    /// Reference dataset.
    pub reference: ReferenceDataset,
    /// Default tolerance to use when a reference point carries no
    /// `uncertainty` half-width.
    pub default_tolerance: f64,
}

/// Validation suite: a collection of cases plus the orchestration
/// machinery that runs a simulator probe against each one.
#[derive(Debug, Clone, Default)]
pub struct ValidationSuite {
    /// Cases to run.
    pub cases: Vec<ValidationCase>,
}

impl ValidationSuite {
    /// Empty suite.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Add a case.
    pub fn push(&mut self, case: ValidationCase) {
        self.cases.push(case);
    }

    /// Run every case against the supplied simulator probe and return
    /// a [`crate::report::ValidationReport`].
    ///
    /// The probe receives the case being run and the gestational week
    /// at which to evaluate, and returns the simulator's output at
    /// that week in the same units as the reference dataset.
    #[allow(clippy::cast_precision_loss)]
    pub fn run<F>(&self, mut probe: F) -> crate::report::ValidationReport
    where
        F: FnMut(&ValidationCase, f64) -> f64,
    {
        let mut results = Vec::with_capacity(self.cases.len());
        for case in &self.cases {
            let mut residuals = Vec::with_capacity(case.reference.points.len());
            let mut in_range = 0usize;
            for point in &case.reference.points {
                let sim = probe(case, point.gestational_week);
                residuals.push(sim - point.value);
                if point.contains(sim, case.default_tolerance) {
                    in_range += 1;
                }
            }
            let total = residuals.len();
            let rms = if total == 0 {
                0.0
            } else {
                (residuals.iter().map(|r| r * r).sum::<f64>() / total as f64).sqrt()
            };
            let agreement = crate::report::Agreement::classify(
                case.tier,
                in_range,
                total,
                rms,
                &case.reference,
            );
            results.push(crate::report::ValidationResult {
                case_id: case.id.clone(),
                component: case.component.clone(),
                tier: case.tier,
                level: case.level,
                total_points: total,
                points_in_range: in_range,
                rms_residual: rms,
                residuals,
                agreement,
            });
        }
        crate::report::ValidationReport { results }
    }
}
