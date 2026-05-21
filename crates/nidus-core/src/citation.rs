//! Citation records for parameters and unknown-channel hypotheses.
//!
//! Every numerical quantity in Nidus carries a citation back to the source
//! literature so that simulator output is auditable from the result back to
//! the original studies (SPEC.md §9).

/// Stable identifier for a citation entry in the parameter database.
///
/// The string form is a short slug, e.g. `"nichd-fetal-growth-2015"`,
/// chosen to be stable across releases. The full bibliographic record
/// lives in the citation index (`data/citations/`).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct CitationId(pub String);

impl CitationId {
    /// Construct a citation identifier from any string-like value.
    pub fn new(id: impl Into<String>) -> Self {
        Self(id.into())
    }

    /// Borrow the underlying slug.
    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// Full bibliographic record for a cited source.
///
/// Citations are written once into the citation index and referenced
/// elsewhere by [`CitationId`]. The fields are deliberately broad enough
/// to record both peer-reviewed publications and grey-literature sources
/// such as published reference cohort datasets.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Citation {
    /// Stable identifier referenced from parameter entries.
    pub id: CitationId,
    /// Author list in display form (e.g. `"Smith J, Jones K, ..."`).
    pub authors: String,
    /// Title of the work.
    pub title: String,
    /// Containing venue: journal, book, or dataset publisher.
    pub venue: String,
    /// Year of publication.
    pub year: u16,
    /// Digital Object Identifier, if any.
    pub doi: Option<String>,
    /// `PubMed` identifier, if any.
    pub pmid: Option<String>,
    /// Free-text notes (e.g. cohort description, measurement technique).
    pub notes: Option<String>,
}

impl Citation {
    /// Construct a minimal citation; optional identifiers and notes can be
    /// populated by direct field assignment.
    pub fn new(
        id: impl Into<CitationId>,
        authors: impl Into<String>,
        title: impl Into<String>,
        venue: impl Into<String>,
        year: u16,
    ) -> Self {
        Self {
            id: id.into(),
            authors: authors.into(),
            title: title.into(),
            venue: venue.into(),
            year,
            doi: None,
            pmid: None,
            notes: None,
        }
    }
}

impl From<&str> for CitationId {
    fn from(value: &str) -> Self {
        Self(value.to_owned())
    }
}

impl From<String> for CitationId {
    fn from(value: String) -> Self {
        Self(value)
    }
}
