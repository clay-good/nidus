//! Reference-dataset adapters.
//!
//! Validation cases compare simulator output against published
//! reference data. Each dataset lives in `data/validation/` as a TOML
//! file with a stable schema, and is exposed to Rust code through a
//! per-dataset adapter module in this directory.
//!
//! ### Schema
//!
//! Every TOML file declares a single `[dataset]` table with
//! `name`, `quantity`, `unit`, and `citation_id`, followed by a list
//! of `[[row]]` entries. Percentile columns are optional; cohort
//! studies (NICHD) populate them, while longitudinal-cohort studies
//! (Mahendru, Acharya) typically report only `mean` and `sd`.
//!
//! ### Adapter contract
//!
//! Each adapter is a `pub fn name() -> &'static Dataset` returning a
//! cached parse of the bundled TOML. Bundling uses `include_str!` so
//! the binary is self-contained — no filesystem access at runtime.
//!
//! ### Citation hygiene
//!
//! Every dataset's `citation_id` must resolve against the project's
//! shared `data/citations/index.toml`. A workspace integration test
//! checks this; the loader itself only validates the schema.

use std::sync::OnceLock;

use serde::Deserialize;
use thiserror::Error;

use nidus_core::citation::CitationId;

pub mod maternal_hemodynamics;

/// One reference dataset: a series of measurements at varying
/// gestational ages, plus the citation backing them.
#[derive(Debug, Clone, PartialEq)]
pub struct Dataset {
    /// Stable identifier (kebab-case).
    pub id: String,
    /// Human-readable name.
    pub name: String,
    /// Citation backing every row.
    pub citation_id: CitationId,
    /// Quantity measured (e.g. `"cardiac-output"`).
    pub quantity: String,
    /// Display unit (e.g. `"L/min"`).
    pub unit: String,
    /// Reference rows, in order of gestational age.
    pub rows: Vec<DatasetRow>,
}

/// One row of a reference dataset.
///
/// Cohort percentile studies populate the `percentile_*` fields;
/// longitudinal-cohort summary studies leave them `None` and report
/// only `mean` and `sd`.
#[derive(Debug, Clone, PartialEq)]
pub struct DatasetRow {
    /// Gestational age in completed weeks.
    pub age_weeks: f64,
    /// Sample or population mean.
    pub mean: f64,
    /// Sample or population standard deviation.
    pub sd: f64,
    /// 5th percentile, if reported.
    pub percentile_5: Option<f64>,
    /// 50th percentile (median), if reported.
    pub percentile_50: Option<f64>,
    /// 95th percentile, if reported.
    pub percentile_95: Option<f64>,
}

/// Errors that can arise loading a dataset TOML file.
#[derive(Debug, Error)]
pub enum DatasetError {
    /// TOML failed to parse against the expected schema.
    #[error("failed to parse dataset TOML for `{dataset}`: {source}")]
    Parse {
        /// Dataset id (or filename stem) being loaded.
        dataset: String,
        /// Underlying decode error.
        #[source]
        source: toml::de::Error,
    },
}

/// Parse a `Dataset` from a TOML string. The string is the full
/// contents of a `data/validation/<name>.toml` file.
pub fn load_from_str(label: &str, toml_str: &str) -> Result<Dataset, DatasetError> {
    let parsed: DatasetFile = toml::from_str(toml_str).map_err(|source| DatasetError::Parse {
        dataset: label.to_owned(),
        source,
    })?;
    let rows = parsed
        .row
        .into_iter()
        .map(|r| DatasetRow {
            age_weeks: r.age_weeks,
            mean: r.mean,
            sd: r.sd,
            percentile_5: r.percentile_5,
            percentile_50: r.percentile_50,
            percentile_95: r.percentile_95,
        })
        .collect();
    Ok(Dataset {
        id: parsed.dataset.id,
        name: parsed.dataset.name,
        citation_id: CitationId::new(&parsed.dataset.citation_id),
        quantity: parsed.dataset.quantity,
        unit: parsed.dataset.unit,
        rows,
    })
}

/// Helper used by adapters: parse the bundled TOML once and cache it
/// in the supplied `OnceLock`.
pub fn cached(
    label: &'static str,
    toml_str: &'static str,
    cell: &'static OnceLock<Dataset>,
) -> &'static Dataset {
    cell.get_or_init(|| {
        load_from_str(label, toml_str)
            .unwrap_or_else(|e| panic!("bundled dataset `{label}` failed to parse: {e}"))
    })
}

// -------- TOML schema (private) --------

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct DatasetFile {
    dataset: DatasetMeta,
    #[serde(default)]
    row: Vec<DatasetRowTable>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct DatasetMeta {
    id: String,
    name: String,
    citation_id: String,
    quantity: String,
    unit: String,
    #[serde(default)]
    #[allow(dead_code)]
    notes: Option<String>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct DatasetRowTable {
    age_weeks: f64,
    mean: f64,
    sd: f64,
    #[serde(default)]
    percentile_5: Option<f64>,
    #[serde(default)]
    percentile_50: Option<f64>,
    #[serde(default)]
    percentile_95: Option<f64>,
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    const SAMPLE: &str = r#"
[dataset]
id = "demo"
name = "Demo"
citation_id = "demo-source"
quantity = "cardiac-output"
unit = "L/min"

[[row]]
age_weeks = 12.0
mean = 5.5
sd = 0.8

[[row]]
age_weeks = 28.0
mean = 7.0
sd = 1.0
percentile_50 = 7.0
"#;

    #[test]
    fn round_trip_parses_sample() {
        let ds = load_from_str("demo", SAMPLE).expect("parses");
        assert_eq!(ds.id, "demo");
        assert_eq!(ds.unit, "L/min");
        assert_eq!(ds.rows.len(), 2);
        assert_eq!(ds.rows[0].age_weeks, 12.0);
        assert_eq!(ds.rows[1].percentile_50, Some(7.0));
        assert_eq!(ds.rows[0].percentile_50, None);
    }

    #[test]
    fn unknown_fields_are_rejected() {
        let toml_str = r#"
[dataset]
id = "demo"
name = "Demo"
citation_id = "demo-source"
quantity = "x"
unit = "y"
unexpected = "fail"

[[row]]
age_weeks = 12.0
mean = 1.0
sd = 0.1
"#;
        let err = load_from_str("demo", toml_str).expect_err("schema rejects unknown field");
        assert!(matches!(err, DatasetError::Parse { .. }));
    }
}
