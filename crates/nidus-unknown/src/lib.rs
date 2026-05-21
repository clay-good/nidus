//! Unknown-channels registry.
//!
//! Every Tier C or Tier D channel in Nidus is a first-class entity
//! (SPEC.md §7). A channel records the hypothesised mechanism by which
//! a poorly characterised input might affect downstream physiology, the
//! citations that support or question the hypothesis, the parameter
//! range over which the channel could plausibly operate, and the
//! downstream effects it might produce. Every channel can be run in one
//! of three modes — disabled (the minimal-model baseline), fixed at a
//! particular hypothesised value, or sampled across its range as part
//! of an ensemble — so a single scenario can probe a hypothesis without
//! conflating it with everything else the model represents.
//!
//! This crate provides the [`UnknownChannel`] type, the
//! [`ChannelRegistry`] that holds them, and a built-in
//! [`ChannelRegistry::standard_v0_1`] populated with the four initial
//! channels named in SPEC.md §13 prompt 9: maternal exosomal microRNA
//! transfer, cellular microchimerism, the maternal-cortisol diurnal
//! influence on fetal HPA-axis development, and immunoglobulin transfer
//! dynamics.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod registry;

pub use registry::{ChannelMode, ChannelRegistry, ParameterRange, RegistryError, UnknownChannel};
