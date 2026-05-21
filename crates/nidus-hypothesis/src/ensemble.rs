//! Ensemble runner.
//!
//! Given a list of parameter specifications and a model closure, the
//! runner draws independent samples from each parameter's distribution
//! and evaluates the model at every draw. The result is a flat collection
//! of `(parameter draw, output)` pairs that downstream analysers
//! consume — first the sensitivity analyser, then (in future prompts)
//! the outcome-divergence detector and experiment-design suggester.

use std::collections::BTreeMap;

use nidus_core::rng::{ChildRng, RngService};
use nidus_core::subscriber::SubscriberId;
use nidus_core::tier::ConfidenceTier;

/// How a parameter is sampled inside an ensemble run.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SamplingStrategy {
    /// Uniform draw from `[low, high]`. The natural choice for Tier C
    /// and D parameters whose only documented constraint is a plausible
    /// range.
    Uniform {
        /// Lower bound (inclusive).
        low: f64,
        /// Upper bound (inclusive).
        high: f64,
    },
    /// Normal draw with given mean and standard deviation. The natural
    /// choice for Tier A and B parameters with a measured mean and a
    /// measured one-sigma uncertainty.
    Normal {
        /// Distribution mean.
        mean: f64,
        /// Standard deviation.
        sd: f64,
    },
    /// Held at a single value across all samples. Useful for fixing a
    /// parameter while exploring the rest.
    Fixed(f64),
}

impl SamplingStrategy {
    /// Draw one value from the strategy using the supplied RNG.
    pub fn sample(&self, rng: &mut ChildRng) -> f64 {
        match *self {
            Self::Uniform { low, high } => {
                let u = rng.next_f64_unit();
                low + u * (high - low)
            }
            Self::Normal { mean, sd } => mean + sd * standard_normal(rng),
            Self::Fixed(v) => v,
        }
    }
}

/// One parameter's name, confidence tier, and sampling strategy.
#[derive(Debug, Clone, PartialEq)]
pub struct ParameterSpec {
    /// Parameter name, used as the key in the sampled-values map
    /// passed to the model closure.
    pub name: String,
    /// Confidence tier. Recorded so downstream analysers can weight or
    /// rank by tier; the runner itself does not interpret the tier.
    pub tier: ConfidenceTier,
    /// Sampling strategy applied on every draw.
    pub sampling: SamplingStrategy,
}

impl ParameterSpec {
    /// Convenience constructor.
    #[must_use]
    pub fn new(name: impl Into<String>, tier: ConfidenceTier, sampling: SamplingStrategy) -> Self {
        Self {
            name: name.into(),
            tier,
            sampling,
        }
    }
}

/// A single ensemble sample: parameter values keyed by name.
pub type ParameterSample = BTreeMap<String, f64>;

/// Result of running an ensemble: every parameter draw alongside the
/// model's output for that draw.
#[derive(Debug, Clone, PartialEq)]
pub struct EnsembleResult<R> {
    /// One entry per sample; the order matches `outputs`.
    pub samples: Vec<ParameterSample>,
    /// Model outputs for each sample.
    pub outputs: Vec<R>,
}

/// Ensemble runner.
///
/// Given a fixed list of parameter specifications and a sample budget,
/// [`EnsembleRunner::run`] executes the model `n_samples` times,
/// re-keying the RNG with a fresh `(seed, sample_index)` pair on each
/// draw so that results are bit-identical across re-runs and trivially
/// reproducible.
#[derive(Debug, Clone)]
pub struct EnsembleRunner {
    /// Parameters to sample. Order is preserved in the returned
    /// `samples` map keys (though `BTreeMap` makes the on-iteration
    /// order alphabetical regardless of spec order).
    pub specs: Vec<ParameterSpec>,
    /// Number of samples to draw.
    pub n_samples: usize,
    /// Master seed; combined with a per-sample stream id to derive a
    /// fresh `ChildRng` for each sample.
    pub seed: u64,
}

impl EnsembleRunner {
    /// Construct an ensemble runner.
    #[must_use]
    pub fn new(specs: Vec<ParameterSpec>, n_samples: usize, seed: u64) -> Self {
        Self {
            specs,
            n_samples,
            seed,
        }
    }

    /// Run the model across the ensemble. The model closure receives a
    /// borrowed [`ParameterSample`] and returns one output per call.
    pub fn run<F, R>(&self, mut model: F) -> EnsembleResult<R>
    where
        F: FnMut(&ParameterSample) -> R,
    {
        let rng_service = RngService::from_u64(self.seed);
        let stream_id = SubscriberId::new("nidus-hypothesis:ensemble");
        let mut samples = Vec::with_capacity(self.n_samples);
        let mut outputs = Vec::with_capacity(self.n_samples);
        for i in 0..self.n_samples {
            let mut rng = rng_service.child_for(&stream_id, i as u64);
            let mut sample = ParameterSample::new();
            for spec in &self.specs {
                sample.insert(spec.name.clone(), spec.sampling.sample(&mut rng));
            }
            let out = model(&sample);
            samples.push(sample);
            outputs.push(out);
        }
        EnsembleResult { samples, outputs }
    }
}

/// Standard normal sample via Box–Muller. Used by `Normal` sampling.
fn standard_normal(rng: &mut ChildRng) -> f64 {
    let u1 = rng.next_f64_unit().max(f64::MIN_POSITIVE);
    let u2 = rng.next_f64_unit();
    (-2.0 * u1.ln()).sqrt() * (core::f64::consts::TAU * u2).cos()
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn uniform_draws_stay_in_range() {
        let spec = ParameterSpec::new(
            "x",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: -2.0,
                high: 5.0,
            },
        );
        let runner = EnsembleRunner::new(vec![spec], 1000, 1);
        let result = runner.run(|s| s["x"]);
        for &v in &result.outputs {
            assert!((-2.0..=5.0).contains(&v), "out of range: {v}");
        }
    }

    #[test]
    fn fixed_strategy_returns_constant() {
        let spec = ParameterSpec::new("x", ConfidenceTier::A, SamplingStrategy::Fixed(7.5));
        let result = EnsembleRunner::new(vec![spec], 10, 1).run(|s| s["x"]);
        assert!(result.outputs.iter().all(|v| (*v - 7.5).abs() < 1e-12));
    }

    #[test]
    fn same_seed_produces_identical_ensemble() {
        let specs = vec![ParameterSpec::new(
            "x",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 0.0,
                high: 1.0,
            },
        )];
        let a = EnsembleRunner::new(specs.clone(), 50, 42).run(|s| s["x"]);
        let b = EnsembleRunner::new(specs, 50, 42).run(|s| s["x"]);
        assert_eq!(a.outputs, b.outputs);
    }

    #[test]
    fn different_seeds_diverge() {
        let specs = vec![ParameterSpec::new(
            "x",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 0.0,
                high: 1.0,
            },
        )];
        let a = EnsembleRunner::new(specs.clone(), 50, 1).run(|s| s["x"]);
        let b = EnsembleRunner::new(specs, 50, 2).run(|s| s["x"]);
        assert_ne!(a.outputs, b.outputs);
    }

    #[test]
    fn normal_sampling_has_correct_moments() {
        let spec = ParameterSpec::new(
            "x",
            ConfidenceTier::B,
            SamplingStrategy::Normal {
                mean: 10.0,
                sd: 2.0,
            },
        );
        let runner = EnsembleRunner::new(vec![spec], 4000, 99);
        let result = runner.run(|s| s["x"]);
        #[allow(clippy::cast_precision_loss)]
        let n = result.outputs.len() as f64;
        let mean: f64 = result.outputs.iter().sum::<f64>() / n;
        let var: f64 = result
            .outputs
            .iter()
            .map(|v| (v - mean).powi(2))
            .sum::<f64>()
            / n;
        assert!((mean - 10.0).abs() < 0.15, "mean was {mean}");
        assert!((var.sqrt() - 2.0).abs() < 0.2, "sd was {}", var.sqrt());
    }
}
