//! Variance-based sensitivity analysis via Sobol indices.
//!
//! The analyser uses the Saltelli sampling scheme to estimate two
//! quantities per parameter:
//!
//! - **First-order Sobol index** `S_i`. Fraction of total output
//!   variance attributable to parameter `i` *alone* (no interactions).
//! - **Total-order Sobol index** `S_Ti`. Fraction of total output
//!   variance involving parameter `i` (alone or in interaction with any
//!   other parameter).
//!
//! For a model whose response decomposes additively in its inputs, the
//! two are equal; gaps between them indicate interactions. The
//! estimator implemented here is the Saltelli (2010) form:
//!
//! ```text
//!   S_i  ≈ (1/N)   Σ_j  y_B_j · (y_AB_i_j  - y_A_j)   / Var(Y)
//!   S_Ti ≈ (1/2N) Σ_j  (y_A_j   - y_AB_i_j)²        / Var(Y)
//! ```
//!
//! where `A` and `B` are two independent `N × k` parameter sample
//! matrices and `A_B(i)` is `A` with column `i` replaced by `B`'s
//! column `i`. The total number of model evaluations is `N · (k + 2)`.

use crate::ensemble::{ParameterSample, ParameterSpec};
use nidus_core::rng::{ChildRng, RngService};
use nidus_core::subscriber::SubscriberId;
use nidus_core::tier::ConfidenceTier;

/// Sobol indices for one parameter.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SensitivityIndex {
    /// First-order Sobol index `S_i`.
    pub first_order: f64,
    /// Total-order Sobol index `S_Ti`.
    pub total_order: f64,
    /// Tier of the parameter, carried through from the input spec so
    /// callers can rank by tier as well as by index magnitude.
    pub tier: ConfidenceTier,
}

/// Result of running the sensitivity analyser.
#[derive(Debug, Clone, PartialEq)]
pub struct SensitivityResult {
    /// One `(parameter name, indices)` pair per spec, ordered by
    /// total-order index descending. Ties are broken by lexicographic
    /// parameter name so the order is deterministic.
    pub indices: Vec<(String, SensitivityIndex)>,
    /// Total output variance estimated from the union of `y_A` and
    /// `y_B`. Reported so callers can sanity-check that the response
    /// has non-trivial variance over the sampled region.
    pub variance: f64,
}

/// Sobol sensitivity analyser.
#[derive(Debug, Clone)]
pub struct SensitivityAnalyser {
    /// Parameters to analyse.
    pub specs: Vec<ParameterSpec>,
    /// `N` in the Saltelli formula above. Total model evaluations are
    /// `N · (k + 2)` where `k = specs.len()`.
    pub n_base: usize,
    /// Master seed.
    pub seed: u64,
}

impl SensitivityAnalyser {
    /// Construct an analyser.
    #[must_use]
    pub fn new(specs: Vec<ParameterSpec>, n_base: usize, seed: u64) -> Self {
        Self {
            specs,
            n_base,
            seed,
        }
    }

    /// Run the model `N · (k + 2)` times and estimate Sobol indices.
    pub fn analyse<F>(&self, mut model: F) -> SensitivityResult
    where
        F: FnMut(&ParameterSample) -> f64,
    {
        let k = self.specs.len();
        let n = self.n_base;
        let rng_service = RngService::from_u64(self.seed);
        let stream_a = SubscriberId::new("nidus-hypothesis:sensitivity:A");
        let stream_b = SubscriberId::new("nidus-hypothesis:sensitivity:B");

        // Draw the two N×k matrices as flat row-major Vec<Vec<f64>>.
        let mut matrix_a: Vec<Vec<f64>> = Vec::with_capacity(n);
        let mut matrix_b: Vec<Vec<f64>> = Vec::with_capacity(n);
        for j in 0..n {
            let mut rng_a = rng_service.child_for(&stream_a, j as u64);
            let mut rng_b = rng_service.child_for(&stream_b, j as u64);
            matrix_a.push(self.draw_row(&mut rng_a));
            matrix_b.push(self.draw_row(&mut rng_b));
        }

        // Evaluate y_A and y_B.
        let y_a: Vec<f64> = matrix_a
            .iter()
            .map(|row| model(&row_to_sample(&self.specs, row)))
            .collect();
        let y_b: Vec<f64> = matrix_b
            .iter()
            .map(|row| model(&row_to_sample(&self.specs, row)))
            .collect();

        // Total variance estimated from the pooled y_A ∪ y_B.
        let variance = pooled_variance(&y_a, &y_b);
        // Defensive: if the model is effectively constant, Sobol
        // indices are undefined. Return zeros and let callers notice
        // via `variance ≈ 0`.
        let denom = if variance > 0.0 { variance } else { 1.0 };

        // For each parameter i, build A_B(i) and evaluate.
        let mut entries: Vec<(String, SensitivityIndex)> = Vec::with_capacity(k);
        for (i, spec) in self.specs.iter().enumerate() {
            let mut y_ab_i: Vec<f64> = Vec::with_capacity(n);
            for j in 0..n {
                let mut row = matrix_a[j].clone();
                row[i] = matrix_b[j][i];
                y_ab_i.push(model(&row_to_sample(&self.specs, &row)));
            }

            // Saltelli (2010) first-order estimator.
            #[allow(clippy::cast_precision_loss)]
            let n_f = n as f64;
            let mut s_i = 0.0;
            for j in 0..n {
                s_i += y_b[j] * (y_ab_i[j] - y_a[j]);
            }
            s_i /= n_f * denom;

            // Saltelli total-order estimator.
            let mut s_t = 0.0;
            for j in 0..n {
                let d = y_a[j] - y_ab_i[j];
                s_t += d * d;
            }
            s_t /= 2.0 * n_f * denom;

            entries.push((
                spec.name.clone(),
                SensitivityIndex {
                    first_order: s_i,
                    total_order: s_t,
                    tier: spec.tier,
                },
            ));
        }

        entries.sort_by(|a, b| {
            b.1.total_order
                .partial_cmp(&a.1.total_order)
                .unwrap_or(core::cmp::Ordering::Equal)
                .then_with(|| a.0.cmp(&b.0))
        });

        SensitivityResult {
            indices: entries,
            variance,
        }
    }

    fn draw_row(&self, rng: &mut ChildRng) -> Vec<f64> {
        self.specs.iter().map(|s| s.sampling.sample(rng)).collect()
    }
}

fn row_to_sample(specs: &[ParameterSpec], row: &[f64]) -> ParameterSample {
    let mut sample = ParameterSample::new();
    for (spec, &v) in specs.iter().zip(row) {
        sample.insert(spec.name.clone(), v);
    }
    sample
}

#[allow(clippy::cast_precision_loss)]
fn pooled_variance(a: &[f64], b: &[f64]) -> f64 {
    let n = (a.len() + b.len()) as f64;
    if n < 2.0 {
        return 0.0;
    }
    let sum: f64 = a.iter().chain(b.iter()).sum();
    let mean = sum / n;
    let ss: f64 = a.iter().chain(b.iter()).map(|v| (v - mean).powi(2)).sum();
    ss / n
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use crate::ensemble::SamplingStrategy;

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
    fn additive_linear_model_indices_match_analytical_form() {
        // y = a*x1 + b*x2 with x1, x2 ~ U(0,1), a=1, b=2.
        // Var(Y) = a²/12 + b²/12 = 5/12.
        // S_1 = 1/5 = 0.20, S_2 = 4/5 = 0.80.
        // Additive ⇒ S_T_i = S_i.
        let specs = vec![unit("x1"), unit("x2")];
        let analyser = SensitivityAnalyser::new(specs, 16_000, 42);
        let result = analyser.analyse(|s| s["x1"] + 2.0 * s["x2"]);
        // Pull out indices by name.
        let map: std::collections::HashMap<_, _> = result.indices.iter().cloned().collect();
        let s1 = map["x1"];
        let s2 = map["x2"];
        // Monte-Carlo tolerance at N=16k; Sobol estimator standard
        // error scales as 1/sqrt(N). With seeded RNG the values are
        // deterministic across runs.
        assert!(
            (s1.first_order - 0.20).abs() < 0.05,
            "S1 first_order: {}",
            s1.first_order
        );
        assert!(
            (s2.first_order - 0.80).abs() < 0.05,
            "S2 first_order: {}",
            s2.first_order
        );
        assert!(
            (s1.total_order - s1.first_order).abs() < 0.08,
            "S1 additive ⇒ total ≈ first; got first={} total={}",
            s1.first_order,
            s1.total_order
        );
        assert!(
            (s2.total_order - s2.first_order).abs() < 0.08,
            "S2 additive ⇒ total ≈ first; got first={} total={}",
            s2.first_order,
            s2.total_order
        );
    }

    #[test]
    fn ranking_orders_by_total_order_descending() {
        let specs = vec![unit("low"), unit("high")];
        let analyser = SensitivityAnalyser::new(specs, 1500, 11);
        let result = analyser.analyse(|s| s["low"] + 10.0 * s["high"]);
        assert_eq!(result.indices[0].0, "high");
        assert_eq!(result.indices[1].0, "low");
        assert!(result.indices[0].1.total_order > result.indices[1].1.total_order);
    }

    #[test]
    fn interaction_term_shows_in_total_minus_first_order() {
        // y = x1 * x2 (pure interaction, no main effects in the
        // additive decomposition over U(0,1)²). S_i is small;
        // S_T_i should be substantially larger.
        let specs = vec![unit("x1"), unit("x2")];
        let analyser = SensitivityAnalyser::new(specs, 4000, 7);
        let result = analyser.analyse(|s| s["x1"] * s["x2"]);
        for (_, idx) in &result.indices {
            assert!(
                idx.total_order > idx.first_order,
                "expected total > first for interaction-driven model; got first={} total={}",
                idx.first_order,
                idx.total_order
            );
        }
    }

    #[test]
    fn constant_model_yields_zero_variance() {
        let specs = vec![unit("x")];
        let analyser = SensitivityAnalyser::new(specs, 200, 5);
        let result = analyser.analyse(|_| 42.0);
        assert!(result.variance.abs() < 1e-12);
        // With zero variance, indices are undefined but the analyser
        // must not panic; values are reported as zero.
        for (_, idx) in &result.indices {
            assert_eq!(idx.first_order, 0.0);
            assert_eq!(idx.total_order, 0.0);
        }
    }

    #[test]
    fn same_seed_produces_identical_indices() {
        let specs = vec![unit("a"), unit("b")];
        let a = SensitivityAnalyser::new(specs.clone(), 500, 99).analyse(|s| s["a"] + s["b"]);
        let b = SensitivityAnalyser::new(specs, 500, 99).analyse(|s| s["a"] + s["b"]);
        assert_eq!(a, b);
    }
}
