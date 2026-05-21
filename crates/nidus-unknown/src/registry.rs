//! `ChannelRegistry`: storage and mode-management for unknown channels.

use std::collections::BTreeMap;
use std::fmt;

use nidus_core::citation::CitationId;
use nidus_core::rng::ChildRng;
use nidus_core::tier::ConfidenceTier;

/// Plausible parameter range for an unknown channel.
///
/// The range is a closed interval `[low, high]` whose units are
/// channel-specific (documented in [`UnknownChannel::units`]). Sampling
/// mode draws uniformly across this interval.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ParameterRange {
    /// Inclusive lower bound.
    pub low: f64,
    /// Inclusive upper bound.
    pub high: f64,
}

impl ParameterRange {
    /// Construct a range, panicking if `low > high`. (Sampling mode
    /// callers cannot recover from a malformed range; the panic is
    /// preferable to silently inverting the bounds.)
    #[must_use]
    pub fn new(low: f64, high: f64) -> Self {
        assert!(low <= high, "ParameterRange requires low <= high");
        Self { low, high }
    }

    /// Width of the range.
    #[must_use]
    pub fn width(&self) -> f64 {
        self.high - self.low
    }

    /// Midpoint of the range.
    #[must_use]
    pub fn midpoint(&self) -> f64 {
        0.5 * (self.low + self.high)
    }

    /// `true` iff `value` lies in `[low, high]`.
    #[must_use]
    pub fn contains(&self, value: f64) -> bool {
        value >= self.low && value <= self.high
    }

    /// Uniform draw from the range, using the engine's seeded RNG.
    pub fn sample(&self, rng: &mut ChildRng) -> f64 {
        let u = rng.next_f64_unit();
        self.low + u * self.width()
    }
}

/// Mode an unknown channel runs in for a given scenario.
#[derive(Debug, Default, Clone, Copy, PartialEq)]
pub enum ChannelMode {
    /// Channel produces its no-effect value (typically zero). Yields
    /// the minimal-model baseline.
    #[default]
    Disabled,
    /// Channel is held at a specific hypothesised value.
    Fixed(f64),
    /// Channel is sampled uniformly across its range on every query.
    /// Used by ensemble runs that propagate the range into outcome
    /// uncertainty.
    Sample,
}

/// A single unknown channel: its metadata, its plausible range, and the
/// effects it might produce.
#[derive(Debug, Clone, PartialEq)]
pub struct UnknownChannel {
    /// Stable identifier, kebab-case.
    pub id: String,
    /// Human-readable name.
    pub name: String,
    /// Free-form description of the hypothesised mechanism by which
    /// this channel acts on downstream physiology.
    pub hypothesised_mechanism: String,
    /// Citations supporting the hypothesised mechanism.
    pub supporting_citations: Vec<CitationId>,
    /// Citations questioning the hypothesised mechanism. Tier C and D
    /// channels often have both supporting and questioning literature;
    /// recording both is part of the honesty commitment.
    pub questioning_citations: Vec<CitationId>,
    /// Plausible parameter range.
    pub parameter_range: ParameterRange,
    /// Units associated with `parameter_range`. Free-form for v0.1.0
    /// (e.g. `"copies / mL"`, `"dimensionless"`, `"ng/dL"`).
    pub units: String,
    /// Downstream effects the channel is hypothesised to produce.
    /// Free-form text in v0.1.0; a later prompt will introduce typed
    /// linkage to the affected model subsystem.
    pub downstream_effects: Vec<String>,
    /// Confidence tier — must be `C` or `D`, enforced by the registry.
    pub tier: ConfidenceTier,
}

/// Errors raised by [`ChannelRegistry`] operations.
#[derive(Debug, PartialEq, Eq)]
pub enum RegistryError {
    /// Attempted to register a channel with an id that is already in
    /// the registry.
    DuplicateId(String),
    /// Channel id does not exist in the registry.
    UnknownId(String),
    /// A channel was registered at Tier A or B — not allowed; the
    /// registry is for Tier C and D only.
    InvalidTier {
        /// The channel id whose tier was rejected.
        id: String,
        /// The offending tier.
        tier: ConfidenceTier,
    },
}

impl fmt::Display for RegistryError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateId(id) => write!(f, "duplicate channel id `{id}`"),
            Self::UnknownId(id) => write!(f, "unknown channel id `{id}`"),
            Self::InvalidTier { id, tier } => write!(
                f,
                "channel `{id}` registered at tier {tier}; \
                 unknown-channels registry accepts only tier C or D"
            ),
        }
    }
}

impl std::error::Error for RegistryError {}

/// Storage for unknown channels and their current scenario modes.
///
/// Channels are stored in a [`BTreeMap`] keyed by id for deterministic
/// iteration order, matching the dispatcher's reordering-stability
/// commitment (SPEC.md §7).
#[derive(Debug, Default, Clone)]
pub struct ChannelRegistry {
    channels: BTreeMap<String, UnknownChannel>,
    modes: BTreeMap<String, ChannelMode>,
}

impl ChannelRegistry {
    /// Construct an empty registry.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Add a channel. Returns [`RegistryError::DuplicateId`] if the id
    /// is already present, or [`RegistryError::InvalidTier`] if the
    /// channel's tier is not C or D.
    pub fn register(&mut self, channel: UnknownChannel) -> Result<(), RegistryError> {
        if matches!(channel.tier, ConfidenceTier::A | ConfidenceTier::B) {
            return Err(RegistryError::InvalidTier {
                id: channel.id,
                tier: channel.tier,
            });
        }
        if self.channels.contains_key(&channel.id) {
            return Err(RegistryError::DuplicateId(channel.id));
        }
        self.modes.insert(channel.id.clone(), ChannelMode::Disabled);
        self.channels.insert(channel.id.clone(), channel);
        Ok(())
    }

    /// Set the mode of an existing channel. Returns
    /// [`RegistryError::UnknownId`] if no channel with that id exists.
    pub fn set_mode(&mut self, id: &str, mode: ChannelMode) -> Result<(), RegistryError> {
        if !self.channels.contains_key(id) {
            return Err(RegistryError::UnknownId(id.to_owned()));
        }
        self.modes.insert(id.to_owned(), mode);
        Ok(())
    }

    /// Current mode of the channel, or `None` if no such channel
    /// exists.
    #[must_use]
    pub fn mode(&self, id: &str) -> Option<ChannelMode> {
        self.modes.get(id).copied()
    }

    /// Resolve the channel to a concrete value under its current mode.
    ///
    /// Returns `None` if the channel does not exist. `Disabled` resolves
    /// to `0.0` (the no-effect value); `Fixed(v)` resolves to `v`;
    /// `Sample` returns a fresh uniform draw from the channel's
    /// parameter range, using the supplied RNG. Sampling consumes RNG
    /// state, so callers should pass a stream keyed to make the draws
    /// reproducible.
    pub fn current_value(&self, id: &str, rng: &mut ChildRng) -> Option<f64> {
        let channel = self.channels.get(id)?;
        let mode = self.modes.get(id).copied().unwrap_or_default();
        Some(match mode {
            ChannelMode::Disabled => 0.0,
            ChannelMode::Fixed(v) => v,
            ChannelMode::Sample => channel.parameter_range.sample(rng),
        })
    }

    /// Borrow a channel by id.
    #[must_use]
    pub fn channel(&self, id: &str) -> Option<&UnknownChannel> {
        self.channels.get(id)
    }

    /// Iterate over channels in deterministic id order.
    pub fn channels(&self) -> impl Iterator<Item = &UnknownChannel> {
        self.channels.values()
    }

    /// Number of registered channels.
    #[must_use]
    pub fn len(&self) -> usize {
        self.channels.len()
    }

    /// `true` iff no channels are registered.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.channels.is_empty()
    }

    /// Built-in registry pre-populated with the four channels named in
    /// SPEC.md §13 prompt 9.
    ///
    /// Each channel ships in [`ChannelMode::Disabled`] so the registry
    /// produces a minimal-model baseline by default. Scenarios opt in
    /// to specific hypothesised values or to ensemble sampling by
    /// calling [`ChannelRegistry::set_mode`].
    #[must_use]
    pub fn standard_v0_1() -> Self {
        let mut registry = Self::new();
        for channel in standard_channels() {
            registry
                .register(channel)
                .expect("standard channels must register cleanly");
        }
        registry
    }
}

fn standard_channels() -> Vec<UnknownChannel> {
    vec![
        UnknownChannel {
            id: "maternal-exosomal-mirna-transfer".to_owned(),
            name: "Maternal exosomal microRNA transfer".to_owned(),
            hypothesised_mechanism:
                "Maternal-derived exosomes carrying microRNA cargo cross the placental barrier \
                 and influence fetal gene expression in target tissues. The candidate cargo, \
                 the targets, and the dose–response relationship are all open questions."
                    .to_owned(),
            supporting_citations: Vec::new(),
            questioning_citations: Vec::new(),
            parameter_range: ParameterRange::new(0.0, 1.0),
            units: "dimensionless transfer index".to_owned(),
            downstream_effects: vec![
                "Modulation of fetal hepatic gene expression".to_owned(),
                "Modulation of fetal placental-axis gene expression".to_owned(),
            ],
            tier: ConfidenceTier::D,
        },
        UnknownChannel {
            id: "cellular-microchimerism".to_owned(),
            name: "Maternal-fetal cellular microchimerism".to_owned(),
            hypothesised_mechanism:
                "Maternal cells crossing into fetal compartments (and vice versa) persist long \
                 after pregnancy. The extent of bidirectional transfer, the lineage of \
                 persisting cells, and their functional roles are active research questions."
                    .to_owned(),
            supporting_citations: Vec::new(),
            questioning_citations: Vec::new(),
            parameter_range: ParameterRange::new(0.0, 100.0),
            units: "cells per mL of fetal blood (illustrative scale)".to_owned(),
            downstream_effects: vec![
                "Possible influence on fetal immune development".to_owned(),
                "Possible influence on long-term maternal autoimmune risk \
                 (post-pregnancy effect; not modelled in v0.1.0)"
                    .to_owned(),
            ],
            tier: ConfidenceTier::C,
        },
        UnknownChannel {
            id: "maternal-cortisol-diurnal-fetal-hpa".to_owned(),
            name: "Maternal cortisol diurnal pattern on fetal HPA-axis development".to_owned(),
            hypothesised_mechanism:
                "Maternal cortisol crosses the placenta in proportions modulated by 11β-HSD2 \
                 activity. The diurnal pattern and total exposure are suspected to programme \
                 fetal HPA-axis set points, but the dose-response and developmental-window \
                 specifics remain uncertain."
                    .to_owned(),
            supporting_citations: Vec::new(),
            questioning_citations: Vec::new(),
            parameter_range: ParameterRange::new(0.0, 1.0),
            units: "fractional placental cortisol transfer (dimensionless)".to_owned(),
            downstream_effects: vec![
                "Modulation of fetal HPA-axis set point".to_owned(),
                "Possible influence on offspring stress reactivity".to_owned(),
            ],
            tier: ConfidenceTier::C,
        },
        UnknownChannel {
            id: "immunoglobulin-transfer-dynamics".to_owned(),
            name: "Maternal-to-fetal immunoglobulin (IgG) transfer dynamics".to_owned(),
            hypothesised_mechanism:
                "IgG crosses the placenta via FcRn-mediated transcytosis, accelerating in the \
                 third trimester. The maximal transfer rate, subclass-specific kinetics, and \
                 their modulation by maternal pathology are open quantitative questions."
                    .to_owned(),
            supporting_citations: Vec::new(),
            questioning_citations: Vec::new(),
            parameter_range: ParameterRange::new(0.0, 2.0),
            units: "fetal:maternal IgG concentration ratio".to_owned(),
            downstream_effects: vec![
                "Neonatal passive immunity profile".to_owned(),
                "Modulation of fetal autoimmune signal exposure".to_owned(),
            ],
            tier: ConfidenceTier::C,
        },
    ]
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use nidus_core::rng::RngService;
    use nidus_core::subscriber::SubscriberId;

    fn rng() -> ChildRng {
        RngService::from_u64(42).child_for(&SubscriberId::new("test"), 0)
    }

    fn dummy_channel(id: &str, tier: ConfidenceTier) -> UnknownChannel {
        UnknownChannel {
            id: id.to_owned(),
            name: id.to_owned(),
            hypothesised_mechanism: String::new(),
            supporting_citations: Vec::new(),
            questioning_citations: Vec::new(),
            parameter_range: ParameterRange::new(0.0, 10.0),
            units: "test".to_owned(),
            downstream_effects: Vec::new(),
            tier,
        }
    }

    #[test]
    fn registry_rejects_tier_a_and_b() {
        let mut r = ChannelRegistry::new();
        let err = r
            .register(dummy_channel("a", ConfidenceTier::A))
            .unwrap_err();
        assert!(matches!(err, RegistryError::InvalidTier { .. }));
        let err = r
            .register(dummy_channel("b", ConfidenceTier::B))
            .unwrap_err();
        assert!(matches!(err, RegistryError::InvalidTier { .. }));
    }

    #[test]
    fn registry_accepts_tier_c_and_d() {
        let mut r = ChannelRegistry::new();
        r.register(dummy_channel("c", ConfidenceTier::C)).unwrap();
        r.register(dummy_channel("d", ConfidenceTier::D)).unwrap();
        assert_eq!(r.len(), 2);
    }

    #[test]
    fn duplicate_id_is_rejected() {
        let mut r = ChannelRegistry::new();
        r.register(dummy_channel("c", ConfidenceTier::C)).unwrap();
        let err = r
            .register(dummy_channel("c", ConfidenceTier::D))
            .unwrap_err();
        assert_eq!(err, RegistryError::DuplicateId("c".to_owned()));
    }

    #[test]
    fn disabled_mode_yields_zero() {
        let mut r = ChannelRegistry::new();
        r.register(dummy_channel("c", ConfidenceTier::C)).unwrap();
        let mut g = rng();
        assert_eq!(r.current_value("c", &mut g), Some(0.0));
    }

    #[test]
    fn fixed_mode_yields_specified_value() {
        let mut r = ChannelRegistry::new();
        r.register(dummy_channel("c", ConfidenceTier::C)).unwrap();
        r.set_mode("c", ChannelMode::Fixed(3.5)).unwrap();
        let mut g = rng();
        assert_eq!(r.current_value("c", &mut g), Some(3.5));
    }

    #[test]
    fn sample_mode_stays_in_range() {
        let mut r = ChannelRegistry::new();
        r.register(dummy_channel("c", ConfidenceTier::C)).unwrap();
        r.set_mode("c", ChannelMode::Sample).unwrap();
        let mut g = rng();
        for _ in 0..256 {
            let v = r.current_value("c", &mut g).unwrap();
            assert!((0.0..=10.0).contains(&v), "out of range: {v}");
        }
    }

    #[test]
    fn standard_v0_1_contains_named_channels() {
        let r = ChannelRegistry::standard_v0_1();
        for id in [
            "maternal-exosomal-mirna-transfer",
            "cellular-microchimerism",
            "maternal-cortisol-diurnal-fetal-hpa",
            "immunoglobulin-transfer-dynamics",
        ] {
            assert!(r.channel(id).is_some(), "missing channel: {id}");
        }
        // All four ship in the disabled mode for a minimal-model
        // baseline.
        for ch in r.channels() {
            assert_eq!(r.mode(&ch.id), Some(ChannelMode::Disabled));
        }
    }

    #[test]
    fn iteration_order_is_deterministic() {
        let r = ChannelRegistry::standard_v0_1();
        let a: Vec<_> = r.channels().map(|c| c.id.clone()).collect();
        let b: Vec<_> = r.channels().map(|c| c.id.clone()).collect();
        assert_eq!(a, b);
        // BTreeMap ordering gives lexicographic id order; the test
        // pins the contract by name.
        assert_eq!(
            a,
            vec![
                "cellular-microchimerism",
                "immunoglobulin-transfer-dynamics",
                "maternal-cortisol-diurnal-fetal-hpa",
                "maternal-exosomal-mirna-transfer",
            ]
        );
    }

    #[test]
    fn set_mode_rejects_unknown_id() {
        let mut r = ChannelRegistry::new();
        let err = r
            .set_mode("does-not-exist", ChannelMode::Fixed(1.0))
            .unwrap_err();
        assert_eq!(err, RegistryError::UnknownId("does-not-exist".to_owned()));
    }

    #[test]
    fn ensemble_baseline_versus_sampled_diverges() {
        let baseline = ChannelRegistry::standard_v0_1();
        let mut sampled = ChannelRegistry::standard_v0_1();
        for ch in sampled.channels().map(|c| c.id.clone()).collect::<Vec<_>>() {
            sampled.set_mode(&ch, ChannelMode::Sample).unwrap();
        }
        let mut g1 = rng();
        let mut g2 = rng();
        let mut any_difference = false;
        for ch in baseline
            .channels()
            .map(|c| c.id.clone())
            .collect::<Vec<_>>()
        {
            let b = baseline.current_value(&ch, &mut g1).unwrap();
            let s = sampled.current_value(&ch, &mut g2).unwrap();
            if (b - s).abs() > 0.0 {
                any_difference = true;
            }
        }
        assert!(
            any_difference,
            "sampling all standard channels should produce values different \
             from the disabled baseline (zeros)"
        );
    }
}
