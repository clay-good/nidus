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
    Submodel(
        id="placental_glucose_glut3",
        name="Placental glucose transport, GLUT3 (Michaelis-Menten)",
        description=(
            "Michaelis-Menten flux for GLUT3-mediated placental glucose "
            "transport on the syncytial microvillous membrane: "
            "V = Vmax*[S]/(Km+[S]). GLUT3 is the higher-affinity (lower "
            "Km) isoform and dominates uptake early in gestation."
        ),
        sbo_term="SBO:0000028",
        parameter_ids=(
            "placental_glucose.glucose_glut3_km_mmol_per_l",
            "placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2",
        ),
        independent_variable="substrate_mmol_per_l",
        output_units="mmol/min/m^2",
    ),
    Submodel(
        id="maternal_cardiac_output_trajectory",
        name="Maternal cardiac output trajectory (Gaussian)",
        description=(
            "Gaussian-bump trajectory for cardiac output across "
            "gestation: CO(t) = baseline + peak_excess * "
            "exp(-((t - peak_week)/spread)^2 / 2). Fit to Mahendru 2014 "
            "longitudinal cohort + Sanghavi 2014 review."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_cardiac_output_l_per_min",
            "maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
            "maternal_cardiovascular.cardiac_output_peak_week",
            "maternal_cardiovascular.cardiac_output_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="L/min",
    ),
    Submodel(
        id="maternal_map_trajectory",
        name="Maternal MAP trajectory (Gaussian nadir)",
        description=(
            "Gaussian-nadir trajectory for mean arterial pressure: "
            "MAP(t) = baseline - nadir_drop * exp(-((t - nadir_week)/"
            "spread)^2 / 2). The mid-pregnancy dip reflects systemic "
            "vasodilation; pressure recovers toward term."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_map_mmhg",
            "maternal_cardiovascular.map_nadir_drop_mmhg",
            "maternal_cardiovascular.map_nadir_week",
            "maternal_cardiovascular.map_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="mmHg",
    ),
    Submodel(
        id="uterine_artery_flow_logistic",
        name="Uterine-artery flow logistic growth",
        description=(
            "Logistic growth of bilateral uterine-artery flow across "
            "gestation: Q(t) = baseline + (term - baseline) / "
            "(1 + exp(-r*(t - 24))). The mid-pregnancy reference week "
            "(24) is the inflection point of the curve fit to Thaler "
            "1990 Doppler-cohort means."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_cardiovascular.baseline_uterine_flow_ml_per_min",
            "maternal_cardiovascular.term_uterine_flow_ml_per_min",
            "maternal_cardiovascular.uterine_flow_growth_rate_per_week",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="placental_o2_equilibrator",
        name="Placental O2 venous-equilibrator (algebraic)",
        description=(
            "Algebraic equilibrium between maternal intervillous PO2 "
            "and umbilical vein PO2 across the syncytiotrophoblast "
            "barrier. Umbilical vein PO2 = intervillous PO2 * "
            "max_equilibration (typically ~60-80% of the maternal-side "
            "PO2 in a healthy term placenta)."
        ),
        sbo_term=None,
        parameter_ids=(
            "placental_gas_exchange.maternal_intervillous_po2_mmhg",
            "placental_gas_exchange.gas_max_equilibration",
        ),
        independent_variable="maternal_intervillous_po2_mmhg",
        output_units="mmHg",
    ),
    Submodel(
        id="plasma_volume_expansion",
        name="Maternal plasma volume across gestation (algebraic)",
        description=(
            "Sigmoidal plasma-volume expansion across gestation: "
            "PV(t) = early + (term - early) / (1 + exp(-0.2*(t - 22))). "
            "Fit to de Haas 2017 (PMID 28169502) meta-analysis pooled "
            "trajectory + Bernstein 2001 (PMID 11339913) early "
            "first-trimester anchor."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_blood.plasma_volume_early_l",
            "maternal_blood.plasma_volume_l",
        ),
        independent_variable="t_weeks",
        output_units="L",
    ),
    Submodel(
        id="gfr_logistic_trajectory",
        name="Maternal GFR logistic trajectory",
        description=(
            "Logistic-rise trajectory for maternal glomerular "
            "filtration rate across gestation: GFR(t) = baseline + "
            "(peak - baseline) / (1 + exp(-r*(t - t_peak))). Anchored "
            "to Conrad 2001 (PMID 11489744) review of relaxin-mediated "
            "renal vasodilation and the ~50% rise above non-pregnant "
            "baseline. Logistic is an approximation; the true curve "
            "plateaus and declines slightly toward term."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_renal.baseline_gfr_ml_per_min",
            "maternal_renal.gfr_ml_per_min",
            "maternal_renal.gfr_logistic_rate_per_week",
            "maternal_renal.gfr_peak_week",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="amniotic_fluid_volume_trajectory",
        name="Amniotic fluid volume trajectory (Gaussian-bump approximation)",
        description=(
            "Gaussian-bump approximation to the Brace & Wolf 1989 "
            "(PMID 2782359) amniotic-fluid-volume curve: AFV(t) = "
            "baseline + amplitude * exp(-((t - t_peak)/sigma)^2 / 2), "
            "where amplitude = peak - baseline. Peaks at ~33 weeks "
            "(~800 mL) and declines symmetrically. The published "
            "reference is piecewise; this Gaussian approximation "
            "carries the worst-input Tier C from the empirical spread."
        ),
        sbo_term=None,
        parameter_ids=(
            "amniotic_fluid.afv_early_baseline_ml",
            "amniotic_fluid.afv_peak_ml",
            "amniotic_fluid.afv_peak_week",
            "amniotic_fluid.afv_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="mL",
    ),
    Submodel(
        id="hadlock_fetal_weight",
        name="Hadlock IV fetal weight from biometry",
        description=(
            "Hadlock 1991 (PMID 1887021) four-parameter sonographic "
            "fetal-weight regression: log10(EFW) = 1.3596 + 0.0064*HC "
            "+ 0.0424*AC + 0.174*FL + 0.00061*BPD*AC - 0.00386*AC*FL. "
            "Validated against n=1771 fetuses with 3.3% mean absolute "
            "error."
        ),
        sbo_term=None,
        parameter_ids=("fetal_growth.hadlock_coefficient",),
        independent_variable="biometry_mm",
        output_units="g",
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
