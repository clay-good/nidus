//! Experiment design suggester.
//!
//! Takes the output of the sensitivity analyser and a small amount of
//! per-parameter context (current best estimate, current uncertainty,
//! affected outcomes, available measurement techniques) and produces a
//! ranked list of structured suggestions for what to measure next. The
//! ranking metric is the **expected variance reduction** in the
//! analysed outcome that would follow from learning the parameter
//! exactly: under the standard Sobol decomposition,
//!
//! ```text
//!     E[ΔVar | measure i] = S_T_i · Var(Y)
//! ```
//!
//! where `S_T_i` is the parameter's total-order Sobol index and
//! `Var(Y)` is the analysed outcome's total variance. The suggestion
//! list is sorted by this quantity in descending order so the parameter
//! whose measurement would buy the most uncertainty reduction comes
//! first.
//!
//! The suggester is intentionally not prescriptive: it does not tell
//! researchers what experiment to run, because that choice depends on
//! their resources, expertise, and broader scientific context. It
//! provides the information a researcher needs to make that choice
//! well (SPEC.md §10).

use std::collections::BTreeMap;

use nidus_core::tier::ConfidenceTier;

use crate::sensitivity::SensitivityResult;

/// Per-parameter context the suggester consumes alongside the
/// sensitivity result. The suggester does not invent these values; the
/// caller assembles them from the parameter database and from
/// scenario-specific knowledge of which outcomes the researcher cares
/// about.
#[derive(Debug, Clone, PartialEq)]
pub struct SuggesterParameterInfo {
    /// Current best estimate of the parameter (e.g. mean of the
    /// posterior distribution under the current literature).
    pub current_estimate: f64,
    /// Current symmetric uncertainty (e.g. one-sigma SD or half-width
    /// of a uniform plausible range). Used in the rendered suggestion;
    /// the ranking itself uses the sensitivity index, not the
    /// uncertainty.
    pub current_uncertainty: f64,
    /// Outcomes whose simulator uncertainty depends on this parameter.
    /// Free-form for v0.1.0; typed linkage arrives in a later prompt.
    pub outcomes_affected: Vec<String>,
    /// Measurement techniques currently available for measuring the
    /// parameter, with known limitations noted. Free-form text.
    pub available_techniques: Vec<String>,
}

/// One structured experiment-design suggestion.
#[derive(Debug, Clone, PartialEq)]
pub struct ExperimentSuggestion {
    /// Parameter being proposed for measurement.
    pub parameter_name: String,
    /// Parameter's confidence tier, carried through from the
    /// sensitivity result.
    pub tier: ConfidenceTier,
    /// Total-order Sobol index of this parameter on the analysed
    /// outcome.
    pub total_order_index: f64,
    /// First-order Sobol index of this parameter on the analysed
    /// outcome. The gap `total_order − first_order` indicates
    /// interaction with other parameters; large gaps are worth
    /// highlighting to researchers.
    pub first_order_index: f64,
    /// Expected reduction in outcome variance from measuring this
    /// parameter exactly (`total_order_index · Var(Y)`). The ranking
    /// metric.
    pub expected_information_yield: f64,
    /// Current best estimate (copied from `SuggesterParameterInfo`).
    pub current_estimate: f64,
    /// Current symmetric uncertainty (copied through).
    pub current_uncertainty: f64,
    /// Outcomes whose uncertainty depends on this parameter (copied
    /// through).
    pub outcomes_affected: Vec<String>,
    /// Available measurement techniques (copied through).
    pub available_techniques: Vec<String>,
}

/// Experiment design suggester.
#[derive(Debug, Clone, Default)]
pub struct ExperimentDesignSuggester {
    /// Per-parameter context, keyed by parameter name. Parameters
    /// absent from this map still appear in the output but with empty
    /// lists and `NaN` estimates, so the suggester remains useful
    /// even when full context is not yet available.
    pub parameter_info: BTreeMap<String, SuggesterParameterInfo>,
}

impl ExperimentDesignSuggester {
    /// Construct an empty suggester. Populate `parameter_info` via
    /// [`Self::with_info`] or by direct field access.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Add (or replace) per-parameter context for one parameter.
    #[must_use]
    pub fn with_info(mut self, name: impl Into<String>, info: SuggesterParameterInfo) -> Self {
        self.parameter_info.insert(name.into(), info);
        self
    }

    /// Produce ranked suggestions from a sensitivity result.
    ///
    /// Order: descending expected information yield, with ties broken
    /// by tier (less confident first — Tier D before Tier C before
    /// Tier B before Tier A) and then by parameter name for full
    /// determinism. Parameters at Tier A or B are still included
    /// (so callers can see the full picture), but the tie-break rule
    /// ensures that two parameters with the same yield surface in
    /// the order most useful to a researcher: less-confident first.
    #[must_use]
    pub fn suggest(&self, sensitivity: &SensitivityResult) -> Vec<ExperimentSuggestion> {
        let variance = sensitivity.variance;
        let mut out: Vec<ExperimentSuggestion> = sensitivity
            .indices
            .iter()
            .map(|(name, idx)| {
                let info = self.parameter_info.get(name).cloned();
                ExperimentSuggestion {
                    parameter_name: name.clone(),
                    tier: idx.tier,
                    total_order_index: idx.total_order,
                    first_order_index: idx.first_order,
                    expected_information_yield: idx.total_order * variance,
                    current_estimate: info.as_ref().map_or(f64::NAN, |i| i.current_estimate),
                    current_uncertainty: info.as_ref().map_or(f64::NAN, |i| i.current_uncertainty),
                    outcomes_affected: info
                        .as_ref()
                        .map(|i| i.outcomes_affected.clone())
                        .unwrap_or_default(),
                    available_techniques: info.map(|i| i.available_techniques).unwrap_or_default(),
                }
            })
            .collect();
        out.sort_by(|a, b| {
            b.expected_information_yield
                .partial_cmp(&a.expected_information_yield)
                .unwrap_or(core::cmp::Ordering::Equal)
                .then_with(|| b.tier.cmp(&a.tier)) // larger tier value (D) first
                .then_with(|| a.parameter_name.cmp(&b.parameter_name))
        });
        out
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use crate::sensitivity::SensitivityIndex;

    fn sensitivity_with(entries: Vec<(&str, ConfidenceTier, f64, f64)>) -> SensitivityResult {
        let mut indices: Vec<_> = entries
            .into_iter()
            .map(|(name, tier, s_first, s_total)| {
                (
                    name.to_owned(),
                    SensitivityIndex {
                        first_order: s_first,
                        total_order: s_total,
                        tier,
                    },
                )
            })
            .collect();
        indices.sort_by(|a, b| b.1.total_order.partial_cmp(&a.1.total_order).unwrap());
        SensitivityResult {
            indices,
            variance: 1.0,
        }
    }

    #[test]
    fn ordered_by_expected_information_yield_descending() {
        let sens = sensitivity_with(vec![
            ("low", ConfidenceTier::C, 0.05, 0.10),
            ("high", ConfidenceTier::C, 0.50, 0.80),
            ("mid", ConfidenceTier::C, 0.20, 0.40),
        ]);
        let s = ExperimentDesignSuggester::new().suggest(&sens);
        let names: Vec<_> = s.iter().map(|x| x.parameter_name.clone()).collect();
        assert_eq!(names, vec!["high", "mid", "low"]);
    }

    #[test]
    fn tier_d_breaks_ties_above_tier_b() {
        let sens = sensitivity_with(vec![
            ("tier_b_param", ConfidenceTier::B, 0.10, 0.30),
            ("tier_d_param", ConfidenceTier::D, 0.10, 0.30),
        ]);
        let s = ExperimentDesignSuggester::new().suggest(&sens);
        assert_eq!(s[0].parameter_name, "tier_d_param");
        assert_eq!(s[1].parameter_name, "tier_b_param");
    }

    #[test]
    fn parameter_info_is_threaded_through() {
        let sens = sensitivity_with(vec![("x", ConfidenceTier::C, 0.1, 0.2)]);
        let suggester = ExperimentDesignSuggester::new().with_info(
            "x",
            SuggesterParameterInfo {
                current_estimate: 1.5,
                current_uncertainty: 0.5,
                outcomes_affected: vec!["fetal-growth".to_owned()],
                available_techniques: vec!["technique A".to_owned()],
            },
        );
        let s = suggester.suggest(&sens);
        assert_eq!(s[0].current_estimate, 1.5);
        assert_eq!(s[0].current_uncertainty, 0.5);
        assert_eq!(s[0].outcomes_affected, vec!["fetal-growth"]);
        assert_eq!(s[0].available_techniques, vec!["technique A"]);
    }

    #[test]
    fn missing_info_does_not_drop_the_parameter() {
        let sens = sensitivity_with(vec![("x", ConfidenceTier::D, 0.5, 0.6)]);
        let s = ExperimentDesignSuggester::new().suggest(&sens);
        assert_eq!(s.len(), 1);
        assert!(s[0].current_estimate.is_nan());
        assert!(s[0].outcomes_affected.is_empty());
    }

    #[test]
    fn expected_information_yield_equals_total_order_times_variance() {
        let mut sens = sensitivity_with(vec![("x", ConfidenceTier::C, 0.1, 0.4)]);
        sens.variance = 2.5;
        let s = ExperimentDesignSuggester::new().suggest(&sens);
        assert!((s[0].expected_information_yield - 1.0).abs() < 1e-12);
    }
}
