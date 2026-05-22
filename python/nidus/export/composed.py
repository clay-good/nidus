"""Composed top-level pregnancy model.

Builds a single SBML L3v2 document that wires every submodel into one
self-contained model. This is the "researcher's starting point" — load
it in COPASI, tellurium, libRoadRunner, etc. and you get the whole
nidus submodel collection in one file, with cross-submodel parameter
sharing where appropriate (e.g. gestational time `t_weeks` is shared
across the four time-driven submodels).

Design choices:
- A single flat SBML model rather than the `comp` package. The `comp`
  package gives nicer modularity but has uneven tool support; a flat
  model with prefixed parameter ids works everywhere.
- Each submodel becomes a group of parameters + one assignment rule on
  a clearly-named output variable. Submodel grouping is preserved via
  SBML `<groups>` annotations (libSBML's "groups" package) and via
  nidus-specific RDF blocks.
- Cross-cutting `t_weeks` (gestational age, in weeks) is a single
  shared parameter. Each time-driven submodel's output is `<id>__out`.
"""

from __future__ import annotations

from pathlib import Path

import libsbml  # type: ignore[import-untyped]

from nidus.export.annotate import (
    parameter_id_to_sbml,
    parameter_miriam_block,
    worst_tier,
)
from nidus.export.registry import SUBMODELS
from nidus.load import Dataset
from nidus.models import Parameter

MODEL_ID = "nidus_pregnancy_composed"
MODEL_NAME = "Nidus composed pregnancy physiology model"


def _add_units(model: libsbml.Model) -> None:
    for name, (kind, exp, scale, mult) in {
        "per_week": ("second", -1, 0, 1.0 / (60 * 60 * 24 * 7)),
        "mmHg": ("pascal", 1, 0, 133.322),
        "m_squared": ("metre", 2, 0, 1.0),
    }.items():
        ud = model.createUnitDefinition()
        ud.setId(name)
        u = ud.createUnit()
        u.setKind(getattr(libsbml, f"UNIT_KIND_{kind.upper()}"))
        u.setExponent(exp)
        u.setScale(scale)
        u.setMultiplier(mult)


def _add_param(
    model: libsbml.Model,
    pid: str,
    value: float,
    units: str = "dimensionless",
    constant: bool = True,
) -> libsbml.Parameter:
    p = model.createParameter()
    p.setId(pid)
    p.setValue(value)
    p.setConstant(constant)
    p.setUnits(units)
    return p


def _add_annotated_param(model: libsbml.Model, ds_param: Parameter) -> libsbml.Parameter:
    p = _add_param(model, parameter_id_to_sbml(ds_param.id), ds_param.value.central)
    rdf = parameter_miriam_block(ds_param, indent="    ")
    p.setAnnotation(f"<annotation>\n{rdf}\n</annotation>")
    return p


def _assign(model: libsbml.Model, target: str, formula: str) -> None:
    r = model.createAssignmentRule()
    r.setVariable(target)
    r.setMath(libsbml.parseL3Formula(formula))


def build_composed_sbml(ds: Dataset) -> str:
    """Build the single composed SBML document and return its XML."""
    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(MODEL_ID)
    model.setName(MODEL_NAME)
    _add_units(model)

    # Shared time axis.
    _add_param(model, "t_weeks", 20.0, constant=False)

    # Add every dataset parameter referenced by any submodel exactly once.
    seen: set[str] = set()
    for sm in SUBMODELS:
        for pid in sm.parameter_ids:
            if pid in seen:
                continue
            seen.add(pid)
            _add_annotated_param(model, ds[pid])

    # --- Submodel outputs + assignment rules ---

    # 1. Placental villous growth
    A0 = parameter_id_to_sbml("placental_structure.initial_area_m2")
    K = parameter_id_to_sbml("placental_structure.term_area_m2")
    rA = parameter_id_to_sbml("placental_structure.growth_rate_per_week")
    tmid = parameter_id_to_sbml("placental_structure.midpoint_week")
    _add_param(model, "placental_area_m2", 0.0, units="m_squared", constant=False)
    _assign(
        model,
        "placental_area_m2",
        f"{A0} + ({K} - {A0}) / (1 + exp(-{rA} * (t_weeks - {tmid})))",
    )

    # 2. Cardiac output trajectory
    co_base = parameter_id_to_sbml("maternal_cardiovascular.baseline_cardiac_output_l_per_min")
    co_peak = parameter_id_to_sbml("maternal_cardiovascular.peak_excess_cardiac_output_l_per_min")
    co_pw = parameter_id_to_sbml("maternal_cardiovascular.cardiac_output_peak_week")
    co_sp = parameter_id_to_sbml("maternal_cardiovascular.cardiac_output_spread_weeks")
    _add_param(model, "cardiac_output_l_per_min", 0.0, constant=False)
    _assign(
        model,
        "cardiac_output_l_per_min",
        f"{co_base} + {co_peak} * exp(-((t_weeks - {co_pw}) / {co_sp})^2 / 2)",
    )

    # 3. MAP trajectory
    map_b = parameter_id_to_sbml("maternal_cardiovascular.baseline_map_mmhg")
    map_n = parameter_id_to_sbml("maternal_cardiovascular.map_nadir_drop_mmhg")
    map_nw = parameter_id_to_sbml("maternal_cardiovascular.map_nadir_week")
    map_sp = parameter_id_to_sbml("maternal_cardiovascular.map_spread_weeks")
    _add_param(model, "map_mmhg", 0.0, constant=False)
    _assign(
        model,
        "map_mmhg",
        f"{map_b} - {map_n} * exp(-((t_weeks - {map_nw}) / {map_sp})^2 / 2)",
    )

    # 4. Uterine artery flow logistic
    ua_b = parameter_id_to_sbml("maternal_cardiovascular.baseline_uterine_flow_ml_per_min")
    ua_t = parameter_id_to_sbml("maternal_cardiovascular.term_uterine_flow_ml_per_min")
    ua_r = parameter_id_to_sbml("maternal_cardiovascular.uterine_flow_growth_rate_per_week")
    _add_param(model, "uterine_flow_ml_per_min", 0.0, constant=False)
    _assign(
        model,
        "uterine_flow_ml_per_min",
        f"{ua_b} + ({ua_t} - {ua_b}) / (1 + exp(-{ua_r} * (t_weeks - 24)))",
    )

    # 5. Plasma volume expansion
    pv_e = parameter_id_to_sbml("maternal_blood.plasma_volume_early_l")
    pv_t = parameter_id_to_sbml("maternal_blood.plasma_volume_l")
    _add_param(model, "plasma_volume_l", 0.0, constant=False)
    _assign(
        model,
        "plasma_volume_l",
        f"{pv_e} + ({pv_t} - {pv_e}) / (1 + exp(-0.2 * (t_weeks - 22)))",
    )

    # 6. Adult HbA saturation at maternal intervillous PO2
    mat_po2_id = parameter_id_to_sbml("placental_gas_exchange.maternal_intervillous_po2_mmhg")
    _add_param(model, "maternal_sat", 0.0, constant=False)
    _assign(
        model,
        "maternal_sat",
        f"1 / ((({mat_po2_id})^3 + 150*{mat_po2_id})^-1 * 23400 + 1)",
    )

    # 7. Umbilical vein PO2 from equilibrator
    f_eq = parameter_id_to_sbml("placental_gas_exchange.gas_max_equilibration")
    _add_param(model, "umbilical_vein_po2_mmhg", 0.0, constant=False)
    _assign(model, "umbilical_vein_po2_mmhg", f"{mat_po2_id} * {f_eq}")

    # 8. Fetal HbF saturation at umbilical vein PO2
    p50f = parameter_id_to_sbml("fetal_metabolism.fetal_p50_mmhg")
    _add_param(model, "fetal_sat", 0.0, constant=False)
    _add_param(model, "hill_coefficient_hbf", 2.85)
    _assign(
        model,
        "fetal_sat",
        f"(umbilical_vein_po2_mmhg / {p50f})^hill_coefficient_hbf "
        f"/ (1 + (umbilical_vein_po2_mmhg / {p50f})^hill_coefficient_hbf)",
    )

    # 9. GLUT1/GLUT3 flux at standard maternal glucose (5 mmol/L)
    km1 = parameter_id_to_sbml("placental_glucose.glucose_glut1_km_mmol_per_l")
    vm1 = parameter_id_to_sbml("placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2")
    km3 = parameter_id_to_sbml("placental_glucose.glucose_glut3_km_mmol_per_l")
    vm3 = parameter_id_to_sbml("placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2")
    _add_param(model, "maternal_glucose_mmol_per_l", 5.0, constant=False)
    _add_param(model, "glut1_flux", 0.0, constant=False)
    _add_param(model, "glut3_flux", 0.0, constant=False)
    _assign(
        model,
        "glut1_flux",
        f"{vm1} * maternal_glucose_mmol_per_l / ({km1} + maternal_glucose_mmol_per_l)",
    )
    _assign(
        model,
        "glut3_flux",
        f"{vm3} * maternal_glucose_mmol_per_l / ({km3} + maternal_glucose_mmol_per_l)",
    )

    # 10. Hadlock fetal weight
    coef = parameter_id_to_sbml("fetal_growth.hadlock_coefficient")
    _add_param(model, "bpd_mm", 80.0, constant=False)
    _add_param(model, "hc_mm", 300.0, constant=False)
    _add_param(model, "ac_mm", 300.0, constant=False)
    _add_param(model, "fl_mm", 60.0, constant=False)
    _add_param(model, "efw_g", 0.0, constant=False)
    _assign(
        model,
        "efw_g",
        f"10^({coef}"
        " + 0.0064 * (hc_mm / 10)"
        " + 0.0424 * (ac_mm / 10)"
        " + 0.174 * (fl_mm / 10)"
        " + 0.00061 * (bpd_mm / 10) * (ac_mm / 10)"
        " - 0.00386 * (ac_mm / 10) * (fl_mm / 10))",
    )

    # Top-level model annotation
    tier = worst_tier(*(ds[pid].tier for sm in SUBMODELS for pid in sm.parameter_ids))
    model.setAnnotation(
        "<annotation>\n"
        '  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        '           xmlns:nidus="https://github.com/clay-good/nidus/ontology#">\n'
        f'    <rdf:Description rdf:about="#{MODEL_ID}">\n'
        f"      <nidus:worstInputTier>{tier}</nidus:worstInputTier>\n"
        "      <nidus:datasetVersion>0.4.0.dev0</nidus:datasetVersion>\n"
        "      <nidus:submodelCount>11</nidus:submodelCount>\n"
        "      <nidus:couplingType>flat-composition</nidus:couplingType>\n"
        "    </rdf:Description>\n"
        "  </rdf:RDF>\n"
        "</annotation>"
    )
    model.setNotes(
        '<notes><body xmlns="http://www.w3.org/1999/xhtml">'
        "<p>Composed nidus pregnancy model: 11 submodels wired together "
        "with shared gestational time and gas-exchange coupling. See "
        "docs/specs/v0.4/ for the design and parameter provenance.</p>"
        "</body></notes>"
    )

    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_MODELING_PRACTICE, False)
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, False)
    n = doc.checkConsistency()
    errors = [
        doc.getError(i)
        for i in range(n)
        if doc.getError(i).getSeverity() >= libsbml.LIBSBML_SEV_ERROR
    ]
    if errors:
        msg = "\n".join(e.getMessage() for e in errors[:5])
        raise RuntimeError(f"Composed model failed SBML consistency:\n{msg}")

    xml: str = libsbml.writeSBMLToString(doc)
    return xml


def write_composed_sbml(ds: Dataset, output_dir: str | Path) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{MODEL_ID}.xml"
    path.write_text(build_composed_sbml(ds), encoding="utf-8")
    return path
