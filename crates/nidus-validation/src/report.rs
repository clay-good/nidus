//! Validation report types and rendering.
//!
//! The report is intentionally honest: it shows agreement metrics
//! quantitatively and uses three categories — Excellent, Adequate,
//! Divergent — chosen so that "Divergent" is not a synonym for "the
//! simulator is wrong" but for "look here." A Tier B model component
//! whose published reference data is itself noisy may legitimately
//! sit in the Adequate bucket. The renderer never claims a case has
//! passed; it summarises what was observed.

use std::fmt::Write as _;

use nidus_core::tier::ConfidenceTier;

use crate::suite::{ComponentLevel, ReferenceDataset};

/// Qualitative bucket for a validation case's result.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Agreement {
    /// Most or all simulator points lie inside their reference
    /// intervals and the RMS residual is small.
    Excellent,
    /// A majority of simulator points lie inside their reference
    /// intervals, but RMS residual is non-trivial relative to the
    /// dataset's typical interval half-width.
    Adequate,
    /// Most simulator points fall outside their reference intervals.
    Divergent,
    /// The case operates at Tier C or D, for which there is no
    /// reference data to validate against. Recorded distinctly so
    /// the report is honest about what cannot be validated.
    Unvalidatable,
}

impl Agreement {
    /// Classify a case's result from its summary metrics.
    #[allow(clippy::cast_precision_loss)]
    pub fn classify(
        tier: ConfidenceTier,
        in_range: usize,
        total: usize,
        rms_residual: f64,
        reference: &ReferenceDataset,
    ) -> Self {
        if matches!(tier, ConfidenceTier::C | ConfidenceTier::D) {
            return Self::Unvalidatable;
        }
        if total == 0 {
            return Self::Adequate;
        }
        let frac = in_range as f64 / total as f64;
        // Mean half-width of the reference intervals; falls back to 1.0
        // when no points carry uncertainty.
        let mean_half: f64 = {
            let widths: Vec<f64> = reference
                .points
                .iter()
                .filter_map(|p| p.uncertainty)
                .collect();
            if widths.is_empty() {
                1.0
            } else {
                widths.iter().sum::<f64>() / widths.len() as f64
            }
        };
        if frac >= 0.90 && rms_residual <= mean_half {
            Self::Excellent
        } else if frac >= 0.60 {
            Self::Adequate
        } else {
            Self::Divergent
        }
    }

    /// Single-word label for compact rendering.
    #[must_use]
    pub fn label(self) -> &'static str {
        match self {
            Self::Excellent => "Excellent",
            Self::Adequate => "Adequate",
            Self::Divergent => "Divergent",
            Self::Unvalidatable => "Unvalidatable",
        }
    }
}

/// Outcome of one validation case.
#[derive(Debug, Clone, PartialEq)]
pub struct ValidationResult {
    /// Stable case id (echoed from the input).
    pub case_id: String,
    /// Model component or subsystem the case targets.
    pub component: String,
    /// Tier of the case.
    pub tier: ConfidenceTier,
    /// Level of the case.
    pub level: ComponentLevel,
    /// Total reference points checked.
    pub total_points: usize,
    /// Points whose simulator value fell inside the reference
    /// interval (or within `default_tolerance` if no interval was
    /// supplied).
    pub points_in_range: usize,
    /// RMS residual `sqrt(mean((sim − ref)²))` across all points.
    pub rms_residual: f64,
    /// Per-point signed residual `sim − ref`.
    pub residuals: Vec<f64>,
    /// Agreement classification.
    pub agreement: Agreement,
}

/// Full validation report.
#[derive(Debug, Clone, PartialEq, Default)]
pub struct ValidationReport {
    /// One [`ValidationResult`] per case, in suite order.
    pub results: Vec<ValidationResult>,
}

impl ValidationReport {
    /// Count of cases that fell into each agreement bucket.
    #[must_use]
    pub fn summary_counts(&self) -> AgreementCounts {
        let mut c = AgreementCounts::default();
        for r in &self.results {
            match r.agreement {
                Agreement::Excellent => c.excellent += 1,
                Agreement::Adequate => c.adequate += 1,
                Agreement::Divergent => c.divergent += 1,
                Agreement::Unvalidatable => c.unvalidatable += 1,
            }
        }
        c
    }

    /// Render a Markdown-style summary.
    #[must_use]
    pub fn render_markdown(&self) -> String {
        let mut out = String::new();
        let _ = writeln!(out, "# Validation Report");
        let _ = writeln!(out);
        let counts = self.summary_counts();
        let _ = writeln!(out, "| Excellent | Adequate | Divergent | Unvalidatable |");
        let _ = writeln!(out, "| --- | --- | --- | --- |");
        let _ = writeln!(
            out,
            "| {} | {} | {} | {} |",
            counts.excellent, counts.adequate, counts.divergent, counts.unvalidatable
        );
        let _ = writeln!(out);
        let _ = writeln!(
            out,
            "| Case | Component | Tier | Level | Points in range | RMS residual | Agreement |"
        );
        let _ = writeln!(out, "| --- | --- | --- | --- | --- | --- | --- |");
        for r in &self.results {
            let _ = writeln!(
                out,
                "| {} | {} | {} | {:?} | {}/{} | {:.4} | {} |",
                r.case_id,
                r.component,
                r.tier,
                r.level,
                r.points_in_range,
                r.total_points,
                r.rms_residual,
                r.agreement.label(),
            );
        }
        out
    }
}

/// Bucket counts from a [`ValidationReport`].
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct AgreementCounts {
    /// Number of cases classified Excellent.
    pub excellent: usize,
    /// Number of cases classified Adequate.
    pub adequate: usize,
    /// Number of cases classified Divergent.
    pub divergent: usize,
    /// Number of cases classified Unvalidatable.
    pub unvalidatable: usize,
}
