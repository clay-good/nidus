//! Hypothesis-generation layer.
//!
//! Version 0.1.0 ships the ensemble runner and the Sobol-based
//! sensitivity analyser described in SPEC.md §10 and §13 prompt 10.
//! The outcome-divergence detector and the experiment-design suggester
//! (§13 prompts 11 and 12) are deferred to later prompts.
//!
//! ### Ensemble runs
//!
//! [`ensemble::EnsembleRunner`] takes a vector of [`ensemble::ParameterSpec`]
//! entries — each pinning a parameter to a confidence tier and a
//! sampling strategy — plus a model closure that takes the sampled
//! parameter values and returns one or more outputs of interest. It
//! returns an [`ensemble::EnsembleResult`] holding every sample's
//! parameter draw and the model's output for that draw. The runner is
//! tier-aware: by convention, Tier C and D parameters use [`Uniform`]
//! sampling across their full plausible range, while Tier A and B
//! parameters use [`Normal`] sampling around their measured mean with
//! the measured standard deviation. The runner does not impose this
//! convention — it merely passes the strategy through — but the
//! convention is the one SPEC.md §10 names.
//!
//! [`Uniform`]: ensemble::SamplingStrategy::Uniform
//! [`Normal`]: ensemble::SamplingStrategy::Normal
//!
//! ### Sensitivity analysis
//!
//! [`sensitivity::SensitivityAnalyser`] implements Sobol first-order
//! and total-order variance-decomposition indices via the Saltelli
//! sampling estimator. Parameters whose total-order index is large
//! drive a substantial fraction of outcome variance; parameters whose
//! total-order index minus first-order index is large drive variance
//! through interactions with other parameters. The analyser returns
//! results ordered by total-order index so that the most influential
//! uncertain quantities surface first.
//!
//! These two components together form the data path the
//! experiment-design suggester (§13 prompt 12) will eventually consume:
//! large-total-order Tier C/D parameters are the natural candidates for
//! experimental investigation, because measuring them reduces both
//! uncertainty and consequence.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod divergence;
pub mod ensemble;
pub mod experiment_design;
pub mod sensitivity;

pub use divergence::{DivergenceDetector, DivergenceResult, Mode};
pub use ensemble::{
    EnsembleResult, EnsembleRunner, ParameterSample, ParameterSpec, SamplingStrategy,
};
pub use experiment_design::{
    ExperimentDesignSuggester, ExperimentSuggestion, SuggesterParameterInfo,
};
pub use sensitivity::{SensitivityAnalyser, SensitivityIndex, SensitivityResult};
