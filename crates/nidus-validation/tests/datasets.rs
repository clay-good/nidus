//! Cross-crate test: every bundled reference dataset's `citation_id`
//! resolves against the shipping citation index.

use std::path::PathBuf;

use nidus_data::ParameterDatabase;
use nidus_validation::datasets;

fn workspace_root() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest.parent().unwrap().parent().unwrap().to_path_buf()
}

#[test]
fn maternal_hemodynamics_citation_resolves() {
    let root = workspace_root();
    let parameter_files: [PathBuf; 0] = [];
    let citation_files = [root.join("data/citations/index.toml")];
    let db = ParameterDatabase::from_paths(&parameter_files, &citation_files)
        .expect("citation index loads");
    let ds = datasets::maternal_hemodynamics::dataset();
    let cited = db
        .citation(ds.citation_id.as_str())
        .unwrap_or_else(|| panic!("citation `{}` not found", ds.citation_id.as_str()));
    assert_eq!(cited.year, 2014);
}
