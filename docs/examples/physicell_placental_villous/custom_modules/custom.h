// Custom-module header for the nidus placental-villous slice example.
//
// All Km/Vmax/P50 constants used by `custom.cpp` are looked up by
// nidus parameter id via PhysiCell's parameter accessor, so reviewers
// can audit provenance from PhysiCell_settings.xml alone.

#ifndef __nidus_placental_villous_custom__
#define __nidus_placental_villous_custom__

#include "../core/PhysiCell.h"
#include "../modules/PhysiCell_standard_modules.h"

using namespace BioFVM;
using namespace PhysiCell;

void create_cell_types(void);
void setup_tissue(void);
void setup_microenvironment(void);

void trophoblast_phenotype_update(Cell* pCell, Phenotype& phenotype, double dt);

double glut1_flux_mmol_per_min_per_m2(double substrate_mmol_per_l);
double glut3_flux_mmol_per_min_per_m2(double substrate_mmol_per_l);

#endif
