//! Telemetry bus and event record.
//!
//! Every observable quantity emitted by the simulator becomes a
//! [`TelemetryEvent`] with its source subscriber, the engine tick at
//! which it was observed, the value, the unit, the confidence tier,
//! and a list of supporting citation ids. This is the substrate the
//! confidence-tier-aware visualisation layer (and any downstream
//! exporter) consumes.

use serde::{Deserialize, Serialize};

use nidus_core::citation::CitationId;
use nidus_core::clock::GestationalAge;
use nidus_core::tier::ConfidenceTier;

/// Numeric or string-valued observation.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum TelemetryValue {
    /// A real-valued observation.
    Number(f64),
    /// A categorical observation (e.g. regime label).
    Text(String),
}

impl From<f64> for TelemetryValue {
    fn from(value: f64) -> Self {
        Self::Number(value)
    }
}

impl From<&str> for TelemetryValue {
    fn from(value: &str) -> Self {
        Self::Text(value.to_owned())
    }
}

impl From<String> for TelemetryValue {
    fn from(value: String) -> Self {
        Self::Text(value)
    }
}

/// One observation in the telemetry stream.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TelemetryEvent {
    /// Subscriber or scenario identifier that produced the observation.
    pub source: String,
    /// Engine tick (seconds since simulation start) at observation time.
    pub tick_seconds: u64,
    /// Gestational age at observation time.
    pub gestational_age: GestationalAge,
    /// Quantity name (e.g. `"maternal-cardiac-output"`).
    pub quantity: String,
    /// Value of the observation.
    pub value: TelemetryValue,
    /// Unit string (free-form, mirrors the parameter database).
    pub unit: String,
    /// Confidence tier of the observation.
    pub tier: ConfidenceTier,
    /// Citation ids supporting the observation, in declaration order.
    /// Empty for engine-internal computations that have no published
    /// source.
    pub citations: Vec<CitationId>,
}

impl TelemetryEvent {
    /// Convenience constructor for a numeric observation with no
    /// citations.
    pub fn numeric(
        source: impl Into<String>,
        tick_seconds: u64,
        age: GestationalAge,
        quantity: impl Into<String>,
        value: f64,
        unit: impl Into<String>,
        tier: ConfidenceTier,
    ) -> Self {
        Self {
            source: source.into(),
            tick_seconds,
            gestational_age: age,
            quantity: quantity.into(),
            value: TelemetryValue::Number(value),
            unit: unit.into(),
            tier,
            citations: Vec::new(),
        }
    }
}

/// Simple in-memory telemetry bus.
///
/// Designed for v0.1.0's needs: it is a `Vec` with a small façade. A
/// later prompt will introduce a publish-subscribe API and a streaming
/// variant; the on-disk NDJSON format produced by
/// [`crate::export::write_ndjson`] is stable enough now that those
/// changes will not break consumers.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct TelemetryBus {
    events: Vec<TelemetryEvent>,
}

impl TelemetryBus {
    /// Construct an empty bus.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Append an event.
    pub fn record(&mut self, event: TelemetryEvent) {
        self.events.push(event);
    }

    /// Borrow the event stream in insertion order.
    #[must_use]
    pub fn events(&self) -> &[TelemetryEvent] {
        &self.events
    }

    /// `true` iff no events have been recorded.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.events.is_empty()
    }

    /// Number of recorded events.
    #[must_use]
    pub fn len(&self) -> usize {
        self.events.len()
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn records_and_iterates_events_in_order() {
        let mut bus = TelemetryBus::new();
        bus.record(TelemetryEvent::numeric(
            "test",
            0,
            GestationalAge::from_weeks(20),
            "x",
            1.0,
            "u",
            ConfidenceTier::B,
        ));
        bus.record(TelemetryEvent::numeric(
            "test",
            60,
            GestationalAge::from_weeks(20),
            "x",
            2.0,
            "u",
            ConfidenceTier::B,
        ));
        assert_eq!(bus.len(), 2);
        match &bus.events()[0].value {
            TelemetryValue::Number(v) => assert_eq!(*v, 1.0),
            TelemetryValue::Text(_) => panic!("expected numeric value"),
        }
    }

    #[test]
    fn json_round_trip_preserves_event_fields() {
        let original = TelemetryEvent {
            source: "src".into(),
            tick_seconds: 99,
            gestational_age: GestationalAge::from_weeks(28),
            quantity: "po2".into(),
            value: TelemetryValue::Number(33.3),
            unit: "mmHg".into(),
            tier: ConfidenceTier::B,
            citations: vec![CitationId::new("a"), CitationId::new("b")],
        };
        let s = serde_json::to_string(&original).unwrap();
        let back: TelemetryEvent = serde_json::from_str(&s).unwrap();
        assert_eq!(back, original);
    }
}
