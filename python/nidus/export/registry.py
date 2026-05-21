"""Registry of exportable submodels and the nidus parameters that feed them.

Each submodel has:
- a stable `id` string used as the filename stem in exports/,
- a human-readable `name`,
- a `tier` (worst-input tier across its parameters, recomputed at
  export time),
- a `parameter_ids` list — the nidus dataset parameter ids that supply
  the submodel's numerical inputs,
- a `description` paragraph for the model's annotation block.

The registry is data, not code — generators in sbml.py / cellml.py /
physiocell.py consume it directly so adding a new submodel doesn't
require duplicate code per format.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Submodel:
    id: str
    name: str
    description: str
    sbo_term: str | None  # systems-biology ontology, where applicable
    parameter_ids: tuple[str, ...]
    independent_variable: str | None = None  # e.g. "t" (weeks), "PO2" (mmHg)
    output_units: str = "dimensionless"


SUBMODELS: tuple[Submodel, ...] = (
    Submodel(
        id="placental_villous_growth",
        name="Placental villous-surface-area growth (logistic)",
        description=(
            "Logistic ODE for the expansion of placental villous "
            "surface area across gestation. A(t) = A0 + (Aterm-A0) / "
            "(1 + exp(-r*(t-t_mid)))."
        ),
        sbo_term="SBO:0000295",  # logistic equation
        parameter_ids=(
            "placental_structure.initial_area_m2",
            "placental_structure.term_area_m2",
            "placental_structure.growth_rate_per_week",
            "placental_structure.midpoint_week",
        ),
        independent_variable="t_weeks",
        output_units="m^2",
    ),
    Submodel(
        id="o2hb_dissociation_adult",
        name="Adult O2-Hb dissociation (Severinghaus 1979)",
        description=(
            "Severinghaus 1979 (PMID 35496) equation 1 for adult human "
            "O2-Hb saturation: S = ((PO2^3 + 150*PO2)^-1 * 23400 + 1)^-1. "
            "Implicit P50=26.6 mmHg and Hill coefficient ~2.7."
        ),
        sbo_term="SBO:0000192",  # Hill function
        parameter_ids=(
            "maternal_blood.o2_hb_p50_maternal",
            "maternal_blood.o2_hb_hill_coefficient_maternal",
        ),
        independent_variable="po2_mmhg",
        output_units="dimensionless (fractional saturation)",
    ),
    Submodel(
        id="o2hb_dissociation_fetal",
        name="Fetal O2-Hb dissociation (HbF)",
        description=(
            "Hill-form dissociation for fetal HbF with P50 ~19.5 mmHg "
            "(Bauer 1969, PMID 4980905). The leftward P50 shift enables "
            "fetal extraction of O2 from low-PO2 intervillous blood."
        ),
        sbo_term="SBO:0000192",  # Hill function
        parameter_ids=("fetal_metabolism.fetal_p50_mmhg",),
        independent_variable="po2_mmhg",
        output_units="dimensionless (fractional saturation)",
    ),
    Submodel(
        id="placental_glucose_glut1",
        name="Placental glucose transport, GLUT1 (Michaelis-Menten)",
        description=(
            "Michaelis-Menten flux for GLUT1-mediated placental glucose "
            "transport on the syncytiotrophoblast: V = Vmax*[S]/(Km+[S])."
        ),
        sbo_term="SBO:0000028",  # irreversible Michaelis-Menten
        parameter_ids=(
            "placental_glucose.glucose_glut1_km_mmol_per_l",
            "placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2",
        ),
        independent_variable="substrate_mmol_per_l",
        output_units="mmol/min/m^2",
    ),
)


def list_submodels() -> list[dict[str, object]]:
    """Return a JSON-serialisable list of submodel summaries."""
    return [
        {
            "id": sm.id,
            "name": sm.name,
            "sbo_term": sm.sbo_term,
            "n_parameters": len(sm.parameter_ids),
            "parameter_ids": list(sm.parameter_ids),
            "output_units": sm.output_units,
        }
        for sm in SUBMODELS
    ]
