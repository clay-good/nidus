//! Exports.
//!
//! NDJSON (newline-delimited JSON) is the v0.1.0 export format: one
//! [`crate::telemetry::TelemetryEvent`] per line, streamable, easy to
//! consume from Python (`pandas.read_json(..., lines=True)`) or from a
//! browser-side dashboard. The format is intentionally boring so that
//! downstream tools do not need to track a Nidus-specific schema
//! beyond the event record.

use std::io::Write;
use std::path::Path;

use thiserror::Error;

use crate::telemetry::TelemetryBus;

/// Errors raised by the NDJSON writer.
#[derive(Debug, Error)]
pub enum ExportError {
    /// I/O error from the underlying writer.
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    /// Serde JSON serialisation error.
    #[error("JSON serialisation error: {0}")]
    Json(#[from] serde_json::Error),
}

/// Workaround for `thiserror` not depending on `serde_json` in the
/// workspace's locked feature set; we accept `serde_json::Error` via
/// `From` above explicitly.
const _: () = ();

/// Write every event on the bus as a JSON object on its own line.
pub fn write_ndjson<W: Write>(bus: &TelemetryBus, writer: &mut W) -> Result<(), ExportError> {
    for event in bus.events() {
        let line = serde_json::to_string(event)?;
        writer.write_all(line.as_bytes())?;
        writer.write_all(b"\n")?;
    }
    writer.flush()?;
    Ok(())
}

/// Convenience helper: open `path` for writing and stream NDJSON into
/// it. Overwrites the file if it exists.
pub fn write_ndjson_to_path(bus: &TelemetryBus, path: &Path) -> Result<(), ExportError> {
    let mut f = std::fs::File::create(path)?;
    write_ndjson(bus, &mut f)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::telemetry::{TelemetryBus, TelemetryEvent};
    use nidus_core::clock::GestationalAge;
    use nidus_core::tier::ConfidenceTier;

    fn fixture_bus() -> TelemetryBus {
        let mut bus = TelemetryBus::new();
        for (i, val) in [1.0_f64, 2.5, 3.75].iter().enumerate() {
            bus.record(TelemetryEvent::numeric(
                "test",
                (i as u64) * 60,
                GestationalAge::from_weeks(20 + i as u64),
                "po2",
                *val,
                "mmHg",
                ConfidenceTier::B,
            ));
        }
        bus
    }

    #[test]
    fn ndjson_writes_one_event_per_line() {
        let bus = fixture_bus();
        let mut buf: Vec<u8> = Vec::new();
        write_ndjson(&bus, &mut buf).unwrap();
        let text = String::from_utf8(buf).unwrap();
        let lines: Vec<_> = text.lines().collect();
        assert_eq!(lines.len(), 3);
        for line in lines {
            // Each line is independently parseable as JSON.
            let _: serde_json::Value = serde_json::from_str(line).unwrap();
        }
    }

    #[test]
    fn ndjson_round_trips_through_serde() {
        let bus = fixture_bus();
        let mut buf: Vec<u8> = Vec::new();
        write_ndjson(&bus, &mut buf).unwrap();
        let text = String::from_utf8(buf).unwrap();
        let parsed: Vec<TelemetryEvent> = text
            .lines()
            .map(|l| serde_json::from_str(l).unwrap())
            .collect();
        assert_eq!(parsed.len(), 3);
        assert_eq!(&parsed[0], &bus.events()[0]);
    }
}
