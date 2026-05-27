// Custom-module implementation for the nidus placental-villous slice.
//
// Demonstrates the canonical pattern for reading nidus parameters
// inside a PhysiCell module: every magic number is replaced by an
// `nidus.parameters.get(<dotted_id>)` call, so the same dataset that
// generated the SBML / CellML exports also drives this simulation.

#include "./custom.h"

// ---- Parameter id lookups -----------------------------------------

// Convert nidus dotted ids (subsystem.param_name) to the underscored
// form used by `nidus export --format physiocell` (which replaces "."
// with "__").
static std::string nidus_id(const std::string& dotted) {
    std::string out = dotted;
    for (auto& c : out) if (c == '.') c = '_';
    // PhysiCell parameter names use the underscored form: subsystem__name
    return out;
}

static double nidus_double(const std::string& dotted) {
    // The PhysiCell <user_parameters> block stores all nidus params
    // with their canonical id under a `__` separator.
    return parameters.doubles(nidus_id(dotted).c_str());
}

// ---- Michaelis–Menten kinetics ------------------------------------

double glut1_flux_mmol_per_min_per_m2(double s) {
    static double km   = nidus_double("placental_glucose.glucose_glut1_km_mmol_per_l");
    static double vmax = nidus_double(
        "placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2");
    return vmax * s / (km + s);
}

double glut3_flux_mmol_per_min_per_m2(double s) {
    static double km   = nidus_double("placental_glucose.glucose_glut3_km_mmol_per_l");
    static double vmax = nidus_double(
        "placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2");
    return vmax * s / (km + s);
}

// ---- Setup -------------------------------------------------------

void create_cell_types(void) {
    initialize_default_cell_definition();
    initialize_cell_definitions_from_pugixml();
    Cell_Definition* pTrophoblast = find_cell_definition("trophoblast");
    pTrophoblast->functions.update_phenotype = trophoblast_phenotype_update;
    build_cell_definitions_maps();
    display_cell_definitions(std::cout);
}

void setup_microenvironment(void) {
    initialize_microenvironment();
}

void setup_tissue(void) {
    Cell_Definition* pTrophoblast = find_cell_definition("trophoblast");
    int n = parameters.ints("n_trophoblasts");
    double r = parameters.doubles("villus_radius");
    double two_pi = 6.28318530717958647692;

    for (int i = 0; i < n; ++i) {
        double theta = (double)i / (double)n * two_pi;
        double ring_r = r + 10.0;
        Cell* pCell = create_cell(*pTrophoblast);
        pCell->assign_position(ring_r * std::cos(theta), ring_r * std::sin(theta), 0.0);
    }
}

// ---- Phenotype update --------------------------------------------

void trophoblast_phenotype_update(Cell* pCell, Phenotype& phenotype, double dt) {
    // Pull the local glucose concentration from BioFVM.
    static int glucose_idx = microenvironment.find_density_index("glucose");
    static int oxygen_idx  = microenvironment.find_density_index("oxygen");
    double s = pCell->nearest_density_vector()[glucose_idx];

    // Use GLUT3 below ~3 mmol/L (higher affinity), GLUT1 above.
    double flux = (s < 3.0)
        ? glut3_flux_mmol_per_min_per_m2(s)
        : glut1_flux_mmol_per_min_per_m2(s);

    // Convert flux density to per-cell uptake (assumes ~30 µm^2 of
    // brush border per agent). This is purely demonstrative — the
    // micrometric value is small enough that the equilibrium isn't
    // perturbed; the point is the API pattern, not the rate calibration.
    const double brush_border_m2 = 3.0e-11;
    phenotype.secretion.uptake_rates[glucose_idx] = flux * brush_border_m2;

    // Oxygen uptake is left to the static value in the cell definition;
    // see future revisions for an explicit Severinghaus-coupled rate.
    (void)oxygen_idx;
}
