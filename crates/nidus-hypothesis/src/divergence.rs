//! Outcome divergence detector.
//!
//! Some of the most interesting parameters in physiology are not those
//! with the largest average effect but those that act as switches
//! between qualitatively different regimes (SPEC.md §10 and §13
//! prompt 11). For an ensemble of scalar outputs, this module asks: do
//! the outputs concentrate around a single value, or do they fall into
//! two (or more) well-separated regimes — and if so, which parameter
//! values are associated with each regime?
//!
//! The implementation is deliberately small for v0.1.0. It runs a
//! deterministic 1D k-means with `k = 2`, measures cluster separation
//! against pooled within-cluster spread, and reports the input
//! parameter means inside each cluster so callers can see at a glance
//! which knobs distinguish the regimes. Higher-dimensional clustering
//! (Gaussian mixture models, hierarchical methods) is reserved for a
//! later prompt.

use std::collections::BTreeMap;

use crate::ensemble::EnsembleResult;

/// One detected outcome regime.
#[derive(Debug, Clone, PartialEq)]
pub struct Mode {
    /// Mean of the cluster's output values.
    pub centroid: f64,
    /// Population standard deviation within the cluster.
    pub spread: f64,
    /// Number of ensemble samples assigned to the cluster.
    pub count: usize,
    /// Mean of each input parameter across the samples in this
    /// cluster, indexed by parameter name. Used by downstream layers to
    /// surface which parameters distinguish the regimes.
    pub parameter_signature: BTreeMap<String, f64>,
}

/// Result of running [`DivergenceDetector::detect`].
#[derive(Debug, Clone, PartialEq)]
pub struct DivergenceResult {
    /// Detected modes, sorted by `centroid` ascending. Always at least
    /// one entry; two entries when the separation threshold is met.
    pub modes: Vec<Mode>,
    /// Cluster-separation score: `|μ₁ − μ₂| / pooled within-cluster sd`.
    /// `0.0` for a single-mode result.
    pub separation_score: f64,
    /// `true` iff `separation_score ≥ threshold` *and* the smaller
    /// cluster holds at least `min_cluster_fraction` of the samples.
    /// A scenario whose ensemble is one tight blob plus a single
    /// outlier should not be reported as bimodal, and the
    /// minimum-cluster check is what prevents that.
    pub is_multimodal: bool,
}

/// Detector configuration.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct DivergenceDetector {
    /// Minimum cluster separation (in units of pooled within-cluster
    /// standard deviation) for an ensemble to be reported as
    /// multimodal. Standard rule of thumb in the bimodality literature
    /// is `≥ 2.0`.
    pub separation_threshold: f64,
    /// Minimum fraction of the ensemble that must be assigned to the
    /// smaller cluster for the result to count as multimodal.
    pub min_cluster_fraction: f64,
    /// Maximum number of Lloyd iterations to run before declaring the
    /// k-means assignment converged. The default is generous; 1D
    /// k-means converges in only a handful of iterations even when
    /// initial centroids are pessimally placed.
    pub max_iterations: usize,
}

impl Default for DivergenceDetector {
    fn default() -> Self {
        // The separation score implemented here is `|μ₁ − μ₂|` measured
        // in units of pooled within-cluster SD — equivalent to
        // Ashman's `D` for equal-variance clusters. Splitting a single
        // Gaussian with k-means produces `D ≈ 2.65` even though the
        // underlying distribution is unimodal; using `3.0` as the
        // threshold keeps the detector from false-positive on
        // single-Gaussian outputs while still firing for the
        // step-function regime switches that motivate this analyser.
        Self {
            separation_threshold: 3.0,
            min_cluster_fraction: 0.10,
            max_iterations: 100,
        }
    }
}

impl DivergenceDetector {
    /// Construct with default thresholds.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Detect divergence in an ensemble whose outputs are scalar
    /// `f64` values.
    #[allow(
        clippy::cast_precision_loss,
        clippy::cast_possible_truncation,
        clippy::cast_sign_loss
    )]
    pub fn detect(&self, ensemble: &EnsembleResult<f64>) -> DivergenceResult {
        assert_eq!(
            ensemble.samples.len(),
            ensemble.outputs.len(),
            "ensemble samples and outputs must agree in length"
        );
        let n = ensemble.outputs.len();
        if n == 0 {
            return DivergenceResult {
                modes: Vec::new(),
                separation_score: 0.0,
                is_multimodal: false,
            };
        }
        if n == 1 {
            return DivergenceResult {
                modes: vec![single_mode_from(ensemble, &[0])],
                separation_score: 0.0,
                is_multimodal: false,
            };
        }

        // Initialise the two centroids at the extremes of the output
        // range. With 1D data this is the standard k-means++ collapse
        // and converges to the global optimum in a handful of
        // iterations.
        let (mut lo, mut hi) = output_extremes(&ensemble.outputs);
        if (hi - lo).abs() < f64::EPSILON {
            // Degenerate: all outputs identical. One mode.
            let assignments: Vec<usize> = (0..n).collect();
            return DivergenceResult {
                modes: vec![single_mode_from(ensemble, &assignments)],
                separation_score: 0.0,
                is_multimodal: false,
            };
        }

        let mut assignments = vec![0usize; n];
        for _ in 0..self.max_iterations {
            let mut changed = false;
            for (i, &y) in ensemble.outputs.iter().enumerate() {
                let new = usize::from((y - lo).abs() > (y - hi).abs());
                if new != assignments[i] {
                    assignments[i] = new;
                    changed = true;
                }
            }
            let (new_lo, new_hi) = recompute_centroids(&ensemble.outputs, &assignments);
            lo = new_lo;
            hi = new_hi;
            if !changed {
                break;
            }
        }

        let mut cluster_a: Vec<usize> = Vec::new();
        let mut cluster_b: Vec<usize> = Vec::new();
        for (i, &a) in assignments.iter().enumerate() {
            if a == 0 {
                cluster_a.push(i);
            } else {
                cluster_b.push(i);
            }
        }

        // If one cluster is empty, this is unimodal regardless of
        // threshold settings.
        if cluster_a.is_empty() || cluster_b.is_empty() {
            let used = if cluster_a.is_empty() {
                cluster_b
            } else {
                cluster_a
            };
            return DivergenceResult {
                modes: vec![single_mode_from(ensemble, &used)],
                separation_score: 0.0,
                is_multimodal: false,
            };
        }

        let mode_a = mode_from(ensemble, &cluster_a);
        let mode_b = mode_from(ensemble, &cluster_b);
        let pooled_sd = pooled_within_cluster_sd(
            &ensemble.outputs,
            &assignments,
            mode_a.centroid,
            mode_b.centroid,
        );
        let separation = if pooled_sd > 0.0 {
            (mode_a.centroid - mode_b.centroid).abs() / pooled_sd
        } else {
            f64::INFINITY
        };

        let smaller = mode_a.count.min(mode_b.count);
        let min_count = (self.min_cluster_fraction * n as f64).ceil() as usize;
        let is_multimodal = separation >= self.separation_threshold && smaller >= min_count;

        let mut modes = vec![mode_a, mode_b];
        modes.sort_by(|a, b| {
            a.centroid
                .partial_cmp(&b.centroid)
                .unwrap_or(core::cmp::Ordering::Equal)
        });

        DivergenceResult {
            modes,
            separation_score: separation,
            is_multimodal,
        }
    }
}

fn output_extremes(values: &[f64]) -> (f64, f64) {
    let mut lo = f64::INFINITY;
    let mut hi = f64::NEG_INFINITY;
    for &v in values {
        if v < lo {
            lo = v;
        }
        if v > hi {
            hi = v;
        }
    }
    (lo, hi)
}

#[allow(clippy::cast_precision_loss)]
fn recompute_centroids(outputs: &[f64], assignments: &[usize]) -> (f64, f64) {
    let mut sum0 = 0.0;
    let mut n0 = 0usize;
    let mut sum1 = 0.0;
    let mut n1 = 0usize;
    for (i, &y) in outputs.iter().enumerate() {
        if assignments[i] == 0 {
            sum0 += y;
            n0 += 1;
        } else {
            sum1 += y;
            n1 += 1;
        }
    }
    let c0 = if n0 > 0 { sum0 / n0 as f64 } else { 0.0 };
    let c1 = if n1 > 0 { sum1 / n1 as f64 } else { 0.0 };
    (c0, c1)
}

#[allow(clippy::cast_precision_loss)]
fn pooled_within_cluster_sd(
    outputs: &[f64],
    assignments: &[usize],
    centroid_0: f64,
    centroid_1: f64,
) -> f64 {
    let mut ss = 0.0;
    for (i, &y) in outputs.iter().enumerate() {
        let c = if assignments[i] == 0 {
            centroid_0
        } else {
            centroid_1
        };
        ss += (y - c).powi(2);
    }
    (ss / outputs.len() as f64).sqrt()
}

#[allow(clippy::cast_precision_loss)]
fn mode_from(ensemble: &EnsembleResult<f64>, indices: &[usize]) -> Mode {
    let n = indices.len() as f64;
    let centroid: f64 = indices.iter().map(|&i| ensemble.outputs[i]).sum::<f64>() / n;
    let variance: f64 = indices
        .iter()
        .map(|&i| (ensemble.outputs[i] - centroid).powi(2))
        .sum::<f64>()
        / n;
    let mut signature: BTreeMap<String, f64> = BTreeMap::new();
    if let Some(first) = indices.first() {
        for key in ensemble.samples[*first].keys() {
            let sum: f64 = indices.iter().map(|&i| ensemble.samples[i][key]).sum();
            signature.insert(key.clone(), sum / n);
        }
    }
    Mode {
        centroid,
        spread: variance.sqrt(),
        count: indices.len(),
        parameter_signature: signature,
    }
}

fn single_mode_from(ensemble: &EnsembleResult<f64>, indices: &[usize]) -> Mode {
    mode_from(ensemble, indices)
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use crate::ensemble::{EnsembleRunner, ParameterSpec, SamplingStrategy};
    use nidus_core::tier::ConfidenceTier;

    fn unit(name: &str) -> ParameterSpec {
        ParameterSpec::new(
            name,
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 0.0,
                high: 1.0,
            },
        )
    }

    #[test]
    fn unimodal_gaussian_is_not_flagged_multimodal() {
        // Identity model on a Gaussian-sampled parameter gives a
        // single-Gaussian output distribution. k-means with k=2 on a
        // single Gaussian splits the sample, but the separation
        // between cluster means is only ~1.6 within-cluster SDs —
        // below the multimodality threshold of 2.0.
        let specs = vec![ParameterSpec::new(
            "x",
            ConfidenceTier::C,
            SamplingStrategy::Normal { mean: 5.0, sd: 1.0 },
        )];
        let runner = EnsembleRunner::new(specs, 800, 1);
        let ensemble = runner.run(|s| s["x"]);
        let res = DivergenceDetector::new().detect(&ensemble);
        assert!(
            !res.is_multimodal,
            "unimodal but reported multimodal (score={}): {res:?}",
            res.separation_score
        );
    }

    #[test]
    fn well_separated_bimodal_is_detected() {
        let specs = vec![unit("switch")];
        let runner = EnsembleRunner::new(specs, 800, 2);
        // Step function: outputs cluster around 0 vs 10 depending on
        // whether the parameter is above or below 0.5.
        let ensemble = runner.run(|s| if s["switch"] < 0.5 { 0.0 } else { 10.0 });
        let res = DivergenceDetector::new().detect(&ensemble);
        assert!(res.is_multimodal, "expected multimodal: {res:?}");
        assert_eq!(res.modes.len(), 2);
        // Centroids should be near 0 and 10.
        assert!((res.modes[0].centroid).abs() < 0.5);
        assert!((res.modes[1].centroid - 10.0).abs() < 0.5);
    }

    #[test]
    fn parameter_signatures_identify_the_switch_parameter() {
        let specs = vec![unit("switch"), unit("noise")];
        let runner = EnsembleRunner::new(specs, 800, 3);
        let ensemble = runner.run(|s| if s["switch"] < 0.5 { 0.0 } else { 10.0 });
        let res = DivergenceDetector::new().detect(&ensemble);
        assert!(res.is_multimodal);
        // The low-output cluster should have mean switch around 0.25;
        // the high-output cluster should have mean switch around 0.75.
        let low = &res.modes[0];
        let high = &res.modes[1];
        assert!(
            low.parameter_signature["switch"] < 0.4,
            "low cluster switch mean too high: {}",
            low.parameter_signature["switch"]
        );
        assert!(
            high.parameter_signature["switch"] > 0.6,
            "high cluster switch mean too low: {}",
            high.parameter_signature["switch"]
        );
        // The noise parameter should be approximately balanced — its
        // mean inside each cluster should be near 0.5.
        assert!(
            (low.parameter_signature["noise"] - 0.5).abs() < 0.10,
            "noise mean drifted in low cluster: {}",
            low.parameter_signature["noise"]
        );
    }

    #[test]
    fn outlier_does_not_count_as_a_second_mode() {
        // 999 samples clustered near 0, one at 100. Separation is
        // huge but the second "cluster" holds < 10% of the ensemble.
        let mut ensemble = EnsembleResult {
            samples: Vec::new(),
            outputs: Vec::new(),
        };
        for _ in 0..999 {
            let mut sample = BTreeMap::new();
            sample.insert("x".to_owned(), 0.0);
            ensemble.samples.push(sample);
            ensemble.outputs.push(0.0);
        }
        let mut outlier = BTreeMap::new();
        outlier.insert("x".to_owned(), 1.0);
        ensemble.samples.push(outlier);
        ensemble.outputs.push(100.0);
        let res = DivergenceDetector::new().detect(&ensemble);
        assert!(
            !res.is_multimodal,
            "outlier should not count as second mode"
        );
    }

    #[test]
    fn empty_and_singleton_ensembles_do_not_panic() {
        let empty = EnsembleResult::<f64> {
            samples: Vec::new(),
            outputs: Vec::new(),
        };
        let res = DivergenceDetector::new().detect(&empty);
        assert!(!res.is_multimodal);
        assert_eq!(res.modes.len(), 0);

        let one = EnsembleResult {
            samples: vec![{
                let mut s = BTreeMap::new();
                s.insert("x".to_owned(), 1.0);
                s
            }],
            outputs: vec![3.0],
        };
        let res = DivergenceDetector::new().detect(&one);
        assert!(!res.is_multimodal);
        assert_eq!(res.modes.len(), 1);
    }
}
