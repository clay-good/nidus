//! Cross-crate integration test: load the on-disk `data/` tree and
//! confirm every shipping `Params::from_database` constructor resolves
//! its ids without falling back to scaffold defaults.

use std::path::PathBuf;

use nidus_data::ParameterDatabase;
use nidus_fetal::FetalCirculationParams;
use nidus_maternal::MaternalCardioParams;
use nidus_placenta::structure::StructureParams;
use nidus_placenta::transport::{GasExchangeParams, GlucoseTransportParams};

fn workspace_root() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest.parent().unwrap().parent().unwrap().to_path_buf()
}

#[test]
fn from_database_constructors_resolve_against_shipping_data() {
    let root = workspace_root();
    let citations = vec![root.join("data/citations/index.toml")];
    let parameter_files = vec![
        root.join("data/parameters/maternal/blood.toml"),
        root.join("data/parameters/maternal/cardio.toml"),
        root.join("data/parameters/maternal/respiratory.toml"),
        root.join("data/parameters/maternal/renal.toml"),
        root.join("data/parameters/placenta/structure.toml"),
        root.join("data/parameters/placenta/gas_transport.toml"),
        root.join("data/parameters/placenta/glucose_transport.toml"),
        root.join("data/parameters/fetal/circulation.toml"),
        root.join("data/parameters/fetal/growth.toml"),
        root.join("data/parameters/fetal/metabolism.toml"),
    ];
    let db = ParameterDatabase::from_paths(&parameter_files, &citations)
        .expect("shipping data tree loads");

    let cardio = MaternalCardioParams::from_database(&db).expect("maternal cardio resolved");
    assert!(cardio.baseline_cardiac_output_l_per_min > 3.0);
    assert!(cardio.term_uterine_flow_ml_per_min > 100.0);

    let structure = StructureParams::from_database(&db).expect("placenta structure resolved");
    assert!(structure.initial_area_m2 < structure.term_area_m2);

    let gas = GasExchangeParams::from_database(&db).expect("placenta gas resolved");
    assert!((0.0..1.0).contains(&gas.max_equilibration));

    let glucose = GlucoseTransportParams::from_database(&db).expect("placenta glucose resolved");
    assert!(glucose.km_mmol_per_l > 0.0);
    assert!(glucose.vmax_per_area_mmol_per_min_per_m2 > 0.0);

    let fetal = FetalCirculationParams::from_database(&db).expect("fetal circulation resolved");
    assert!(fetal.foramen_ovale_streamline_preference > 0.5);
    assert!(fetal.ductus_arteriosus_share > 0.5);
}
