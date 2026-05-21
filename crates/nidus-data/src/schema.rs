//! TOML schema for parameter and citation entries.
//!
//! Every parameter file is a list of `[[parameter]]` tables matching
//! [`ParameterEntry`]. Every citation file is a list of `[[citation]]`
//! tables matching [`CitationEntry`]. The fields are intentionally
//! similar to the prose specification in SPEC.md §9 so that contributors
//! can author entries without having to learn a new data model.

use serde::{Deserialize, Serialize};

use nidus_core::tier::ConfidenceTier;

/// One parameter entry as written in a TOML file.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ParameterEntry {
    /// Stable identifier referenced from code; conventionally
    /// `subsystem-name` in kebab case, e.g. `"maternal-hemoglobin-mean"`.
    pub id: String,
    /// Human-readable name.
    pub name: String,
    /// Short description; what the parameter represents and how it is
    /// used in the model.
    pub description: String,
    /// Confidence tier (A, B, C, or D).
    pub tier: ConfidenceTier,
    /// Canonical unit. Free-form for now (e.g. `"g/L"`, `"mmHg"`).
    pub unit: String,
    /// Value, expressed either as a point estimate or as a distribution.
    pub value: ValueSpec,
    /// Identifier of the citation supporting this parameter; must match
    /// an entry in some citation index file.
    pub citation: String,
    /// Population or cohort the parameter was derived from.
    pub population: String,
    /// Gestational-age range over which the value is documented.
    pub age_range: AgeRange,
    /// Measurement technique with known limitations.
    #[serde(default)]
    pub technique: Option<String>,
    /// Caveats about extrapolation outside the studied range.
    #[serde(default)]
    pub caveats: Option<String>,
}

/// Value of a parameter.
///
/// Distributions follow well-known parametric forms. Where the source
/// literature reports a value with uncertainty without specifying a
/// distribution, prefer `point` with `uncertainty` set; reserve the
/// distribution variants for parameters whose sources explicitly fit a
/// distribution.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(tag = "kind", rename_all = "lowercase", deny_unknown_fields)]
pub enum ValueSpec {
    /// A point estimate, optionally with a single-number uncertainty.
    Point {
        /// The point value.
        value: f64,
        /// Standard error or symmetric one-sigma uncertainty, if known.
        #[serde(default)]
        uncertainty: Option<f64>,
    },
    /// A uniform distribution over `[low, high]`.
    Uniform {
        /// Inclusive lower bound.
        low: f64,
        /// Inclusive upper bound.
        high: f64,
    },
    /// A normal distribution with given mean and standard deviation.
    Normal {
        /// Distribution mean.
        mean: f64,
        /// Distribution standard deviation.
        sd: f64,
    },
    /// A lognormal distribution. The parameters are those of the
    /// *underlying normal* distribution on log space (`mu`, `sigma`).
    Lognormal {
        /// Mean of the underlying normal.
        mu: f64,
        /// Standard deviation of the underlying normal.
        sigma: f64,
    },
}

/// Gestational-age range, inclusive on both ends, in completed weeks.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct AgeRange {
    /// Earliest gestational age, in completed weeks, at which the
    /// parameter is documented.
    pub min_weeks: u16,
    /// Latest gestational age, in completed weeks, at which the
    /// parameter is documented.
    pub max_weeks: u16,
}

impl AgeRange {
    /// `true` iff `min_weeks <= max_weeks`.
    #[must_use]
    pub fn is_valid(&self) -> bool {
        self.min_weeks <= self.max_weeks
    }

    /// `true` iff `weeks` falls within `[min_weeks, max_weeks]`.
    #[must_use]
    pub fn contains(&self, weeks: u16) -> bool {
        weeks >= self.min_weeks && weeks <= self.max_weeks
    }
}

/// Top-level structure of a parameter TOML file: an array of entries
/// under the `parameter` key.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ParameterFile {
    /// All parameters declared in this file.
    #[serde(default)]
    pub parameter: Vec<ParameterEntry>,
}

/// One citation as written in the citation index.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct CitationEntry {
    /// Stable identifier referenced from parameter entries.
    pub id: String,
    /// Author list in display form.
    pub authors: String,
    /// Title of the work.
    pub title: String,
    /// Containing journal, book, or dataset publisher.
    pub venue: String,
    /// Year of publication.
    pub year: u16,
    /// Digital Object Identifier, if any.
    #[serde(default)]
    pub doi: Option<String>,
    /// `PubMed` identifier, if any.
    #[serde(default)]
    pub pmid: Option<String>,
    /// Free-text notes (e.g. measurement technique, cohort description).
    #[serde(default)]
    pub notes: Option<String>,
}

/// Top-level structure of a citation TOML file: an array of entries
/// under the `citation` key.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct CitationIndexFile {
    /// All citations declared in this file.
    #[serde(default)]
    pub citation: Vec<CitationEntry>,
}
