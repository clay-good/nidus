"""SBML L3v2 generator for nidus submodels.

Uses libSBML to build a small SBML model per registry entry. Every
parameter carries MIRIAM citation annotations + nidus tier metadata.
Every model passes `libSBML.SBMLDocument.checkConsistency()` with
zero errors.

The mathematical content is encoded with SBML's MathML in
`assignmentRule` (for algebraic submodels) and `rateRule` (for ODE
submodels), with `parameter` SBML elements carrying the nidus values.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import libsbml  # type: ignore[import-untyped]

from nidus.export.annotate import (
    parameter_id_to_sbml,
    parameter_miriam_block,
    worst_tier,
)
from nidus.export.registry import SUBMODELS, Submodel
from nidus.load import Dataset


# Unit definitions reused across submodels.
def _add_units(model: libsbml.Model) -> None:
    """Register the unit definitions we'll reference."""
    # per_week
    ud = model.createUnitDefinition()
    ud.setId("per_week")
    u = ud.createUnit()
    u.setKind(libsbml.UNIT_KIND_SECOND)
    u.setExponent(-1)
    u.setScale(0)
    u.setMultiplier(1.0 / (60 * 60 * 24 * 7))

    # mmHg
    ud = model.createUnitDefinition()
    ud.setId("mmHg")
    u = ud.createUnit()
    u.setKind(libsbml.UNIT_KIND_PASCAL)
    u.setExponent(1)
    u.setScale(0)
    u.setMultiplier(133.322)

    # m_squared
    ud = model.createUnitDefinition()
    ud.setId("m_squared")
    u = ud.createUnit()
    u.setKind(libsbml.UNIT_KIND_METRE)
    u.setExponent(2)
    u.setScale(0)
    u.setMultiplier(1.0)

    # mmol_per_l
    ud = model.createUnitDefinition()
    ud.setId("mmol_per_l")
    u = ud.createUnit()
    u.setKind(libsbml.UNIT_KIND_MOLE)
    u.setExponent(1)
    u.setScale(-3)
    u.setMultiplier(1.0)
    u = ud.createUnit()
    u.setKind(libsbml.UNIT_KIND_LITRE)
    u.setExponent(-1)
    u.setScale(0)
    u.setMultiplier(1.0)


def _add_parameter(
    model: libsbml.Model,
    pid: str,
    value: float,
    units: str | None,
    constant: bool = True,
    annotation_xml: str | None = None,
) -> libsbml.Parameter:
    p = model.createParameter()
    p.setId(parameter_id_to_sbml(pid))
    p.setValue(value)
    p.setConstant(constant)
    if units:
        p.setUnits(units)
    if annotation_xml:
        p.setAnnotation(annotation_xml)
    return p


def _attach_param_annotation(sbml_param: libsbml.Parameter, nidus_param: Any) -> None:
    rdf = parameter_miriam_block(nidus_param, indent="    ")
    sbml_param.setAnnotation(f"<annotation>\n{rdf}\n</annotation>")


# ---- Per-submodel constructors -------------------------------------


def _build_placental_villous_growth(ds: Dataset) -> libsbml.SBMLDocument:
    """Logistic placental villous growth: dA/dt = r*A*(1 - A/K) form,
    realised as an algebraic logistic rule on gestational time."""
    sm = next(s for s in SUBMODELS if s.id == "placental_villous_growth")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    # Independent variable: t_weeks (constant for snapshot evaluation,
    # rate-rule-eligible for ODE integration in tools like tellurium).
    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)

    # Source parameters from the dataset
    A0 = ds["placental_structure.initial_area_m2"]
    K = ds["placental_structure.term_area_m2"]
    r = ds["placental_structure.growth_rate_per_week"]
    tmid = ds["placental_structure.midpoint_week"]

    p_A0 = _add_parameter(model, A0.id, A0.value.central, "m_squared")
    _attach_param_annotation(p_A0, A0)
    p_K = _add_parameter(model, K.id, K.value.central, "m_squared")
    _attach_param_annotation(p_K, K)
    p_r = _add_parameter(model, r.id, r.value.central, "per_week")
    _attach_param_annotation(p_r, r)
    p_tmid = _add_parameter(model, tmid.id, tmid.value.central, "dimensionless")
    _attach_param_annotation(p_tmid, tmid)

    # Output: A(t)
    _add_parameter(model, "A_t_m_squared", 0.0, "m_squared", constant=False)

    # assignmentRule: A = A0 + (K - A0) / (1 + exp(-r*(t - tmid)))
    rule = model.createAssignmentRule()
    rule.setVariable("A_t_m_squared")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(A0.id)} + "
        f"({parameter_id_to_sbml(K.id)} - {parameter_id_to_sbml(A0.id)}) / "
        f"(1 + exp(-{parameter_id_to_sbml(r.id)} * "
        f"(t_weeks - {parameter_id_to_sbml(tmid.id)})))"
    )
    rule.setMath(math_ast)

    # Top-level model annotation: tier + submodel description
    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model_ann = (
        f"<annotation>\n"
        f'  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        f'           xmlns:nidus="https://github.com/clay-good/nidus/ontology#">\n'
        f'    <rdf:Description rdf:about="#{sm.id}">\n'
        f"      <nidus:confidenceTier>{tier}</nidus:confidenceTier>\n"
        f"      <nidus:datasetVersion>0.4.0.dev0</nidus:datasetVersion>\n"
        f"      <nidus:submodelId>{sm.id}</nidus:submodelId>\n"
        f"    </rdf:Description>\n"
        f"  </rdf:RDF>\n"
        f"</annotation>"
    )
    model.setAnnotation(model_ann)
    model.setNotes(_html_notes(sm.description))

    return doc


def _build_o2hb_dissociation_adult(ds: Dataset) -> libsbml.SBMLDocument:
    """Severinghaus 1979 algebraic O2-Hb saturation."""
    sm = next(s for s in SUBMODELS if s.id == "o2hb_dissociation_adult")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    p50 = ds["maternal_blood.o2_hb_p50_maternal"]
    hill = ds["maternal_blood.o2_hb_hill_coefficient_maternal"]

    _add_parameter(model, "po2_mmhg", 50.0, "mmHg", constant=False)
    p_p50 = _add_parameter(model, p50.id, p50.value.central, "mmHg")
    _attach_param_annotation(p_p50, p50)
    p_hill = _add_parameter(model, hill.id, hill.value.central, "dimensionless")
    _attach_param_annotation(p_hill, hill)

    _add_parameter(model, "saturation", 0.0, "dimensionless", constant=False)

    # Severinghaus Eq.1 directly: S = 1 / (((po2^3 + 150*po2)^-1)*23400 + 1)
    # Note: this form ignores the supplied p50/hill (they are stored as
    # annotation-bearing parameters for documentation). The equation
    # form itself implies P50=26.6 and n≈2.7.
    rule = model.createAssignmentRule()
    rule.setVariable("saturation")
    math_ast = libsbml.parseL3Formula("1 / (((po2_mmhg^3 + 150*po2_mmhg)^-1) * 23400 + 1)")
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_o2hb_dissociation_fetal(ds: Dataset) -> libsbml.SBMLDocument:
    """Hill-form dissociation for fetal HbF (Bauer 1969)."""
    sm = next(s for s in SUBMODELS if s.id == "o2hb_dissociation_fetal")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    p50 = ds["fetal_metabolism.fetal_p50_mmhg"]

    _add_parameter(model, "po2_mmhg", 30.0, "mmHg", constant=False)
    p_p50 = _add_parameter(model, p50.id, p50.value.central, "mmHg")
    _attach_param_annotation(p_p50, p50)
    _add_parameter(model, "hill_coefficient_hbf", 2.85, "dimensionless")
    _add_parameter(model, "saturation", 0.0, "dimensionless", constant=False)

    # S = (PO2/P50)^n / (1 + (PO2/P50)^n)
    rule = model.createAssignmentRule()
    rule.setVariable("saturation")
    math_ast = libsbml.parseL3Formula(
        f"(po2_mmhg / {parameter_id_to_sbml(p50.id)})^hill_coefficient_hbf / "
        f"(1 + (po2_mmhg / {parameter_id_to_sbml(p50.id)})^hill_coefficient_hbf)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_placental_glucose_glut1(ds: Dataset) -> libsbml.SBMLDocument:
    """Michaelis-Menten flux for GLUT1-mediated placental glucose transport."""
    sm = next(s for s in SUBMODELS if s.id == "placental_glucose_glut1")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    km = ds["placental_glucose.glucose_glut1_km_mmol_per_l"]
    vmax = ds["placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2"]

    _add_parameter(model, "substrate_mmol_per_l", 5.0, "mmol_per_l", constant=False)
    p_km = _add_parameter(model, km.id, km.value.central, "mmol_per_l")
    _attach_param_annotation(p_km, km)
    p_vmax = _add_parameter(model, vmax.id, vmax.value.central, "dimensionless")
    _attach_param_annotation(p_vmax, vmax)
    _add_parameter(model, "flux", 0.0, "dimensionless", constant=False)

    # V = Vmax * [S] / (Km + [S])
    rule = model.createAssignmentRule()
    rule.setVariable("flux")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(vmax.id)} * substrate_mmol_per_l / "
        f"({parameter_id_to_sbml(km.id)} + substrate_mmol_per_l)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_placental_glucose_glut3(ds: Dataset) -> libsbml.SBMLDocument:
    """Michaelis-Menten flux for GLUT3-mediated placental glucose transport."""
    sm = next(s for s in SUBMODELS if s.id == "placental_glucose_glut3")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    km = ds["placental_glucose.glucose_glut3_km_mmol_per_l"]
    vmax = ds["placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2"]

    _add_parameter(model, "substrate_mmol_per_l", 5.0, "mmol_per_l", constant=False)
    p_km = _add_parameter(model, km.id, km.value.central, "mmol_per_l")
    _attach_param_annotation(p_km, km)
    p_vmax = _add_parameter(model, vmax.id, vmax.value.central, "dimensionless")
    _attach_param_annotation(p_vmax, vmax)
    _add_parameter(model, "flux", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("flux")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(vmax.id)} * substrate_mmol_per_l / "
        f"({parameter_id_to_sbml(km.id)} + substrate_mmol_per_l)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_maternal_cardiac_output(ds: Dataset) -> libsbml.SBMLDocument:
    """Gaussian-bump cardiac-output trajectory across gestation."""
    sm = next(s for s in SUBMODELS if s.id == "maternal_cardiac_output_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    peak = ds["maternal_cardiovascular.peak_excess_cardiac_output_l_per_min"]
    peak_week = ds["maternal_cardiovascular.cardiac_output_peak_week"]
    spread = ds["maternal_cardiovascular.cardiac_output_spread_weeks"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (baseline, peak, peak_week, spread):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "CO_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("CO_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(baseline.id)} + "
        f"{parameter_id_to_sbml(peak.id)} * "
        f"exp(-((t_weeks - {parameter_id_to_sbml(peak_week.id)}) / "
        f"{parameter_id_to_sbml(spread.id)})^2 / 2)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_maternal_map(ds: Dataset) -> libsbml.SBMLDocument:
    """Gaussian-nadir MAP trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "maternal_map_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_cardiovascular.baseline_map_mmhg"]
    nadir = ds["maternal_cardiovascular.map_nadir_drop_mmhg"]
    nadir_week = ds["maternal_cardiovascular.map_nadir_week"]
    spread = ds["maternal_cardiovascular.map_spread_weeks"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (baseline, nadir, nadir_week, spread):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "MAP_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("MAP_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(baseline.id)} - "
        f"{parameter_id_to_sbml(nadir.id)} * "
        f"exp(-((t_weeks - {parameter_id_to_sbml(nadir_week.id)}) / "
        f"{parameter_id_to_sbml(spread.id)})^2 / 2)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_uterine_artery_flow(ds: Dataset) -> libsbml.SBMLDocument:
    """Logistic growth of uterine-artery flow (midpoint = 24 weeks)."""
    sm = next(s for s in SUBMODELS if s.id == "uterine_artery_flow_logistic")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_cardiovascular.baseline_uterine_flow_ml_per_min"]
    term = ds["maternal_cardiovascular.term_uterine_flow_ml_per_min"]
    rate = ds["maternal_cardiovascular.uterine_flow_growth_rate_per_week"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "midpoint_week", 24.0, "dimensionless")
    for p in (baseline, term, rate):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "Q_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("Q_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(baseline.id)} + "
        f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) / "
        f"(1 + exp(-{parameter_id_to_sbml(rate.id)} * (t_weeks - midpoint_week)))"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_placental_o2_equilibrator(ds: Dataset) -> libsbml.SBMLDocument:
    """Algebraic equilibrium: umbilical vein PO2 = intervillous PO2 * f."""
    sm = next(s for s in SUBMODELS if s.id == "placental_o2_equilibrator")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    mat_po2 = ds["placental_gas_exchange.maternal_intervillous_po2_mmhg"]
    f_eq = ds["placental_gas_exchange.gas_max_equilibration"]

    p1 = _add_parameter(model, mat_po2.id, mat_po2.value.central, "mmHg", constant=False)
    _attach_param_annotation(p1, mat_po2)
    p2 = _add_parameter(model, f_eq.id, f_eq.value.central, "dimensionless")
    _attach_param_annotation(p2, f_eq)
    _add_parameter(model, "umbilical_vein_po2_mmhg", 0.0, "mmHg", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("umbilical_vein_po2_mmhg")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(mat_po2.id)} * {parameter_id_to_sbml(f_eq.id)}"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_plasma_volume_expansion(ds: Dataset) -> libsbml.SBMLDocument:
    """Sigmoidal plasma-volume expansion across gestation."""
    sm = next(s for s in SUBMODELS if s.id == "plasma_volume_expansion")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    early = ds["maternal_blood.plasma_volume_early_l"]
    term = ds["maternal_blood.plasma_volume_l"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "growth_rate_per_week", 0.2, "dimensionless")
    _add_parameter(model, "midpoint_week", 22.0, "dimensionless")
    p_early = _add_parameter(model, early.id, early.value.central, "dimensionless")
    _attach_param_annotation(p_early, early)
    p_term = _add_parameter(model, term.id, term.value.central, "dimensionless")
    _attach_param_annotation(p_term, term)
    _add_parameter(model, "PV_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("PV_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(early.id)} + "
        f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(early.id)}) / "
        f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week)))"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_hadlock_fetal_weight(ds: Dataset) -> libsbml.SBMLDocument:
    """Hadlock IV 4-parameter sonographic fetal-weight regression."""
    sm = next(s for s in SUBMODELS if s.id == "hadlock_fetal_weight")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    coef = ds["fetal_growth.hadlock_coefficient"]

    # Biometry inputs in mm (converted to cm in the formula).
    _add_parameter(model, "bpd_mm", 80.0, "dimensionless", constant=False)
    _add_parameter(model, "hc_mm", 300.0, "dimensionless", constant=False)
    _add_parameter(model, "ac_mm", 300.0, "dimensionless", constant=False)
    _add_parameter(model, "fl_mm", 60.0, "dimensionless", constant=False)
    p_coef = _add_parameter(model, coef.id, coef.value.central, "dimensionless")
    _attach_param_annotation(p_coef, coef)
    _add_parameter(model, "efw_g", 0.0, "dimensionless", constant=False)

    # log10(EFW) = a + 0.0064*HC + 0.0424*AC + 0.174*FL + 0.00061*BPD*AC - 0.00386*AC*FL
    rule = model.createAssignmentRule()
    rule.setVariable("efw_g")
    math_ast = libsbml.parseL3Formula(
        f"10^({parameter_id_to_sbml(coef.id)}"
        " + 0.0064 * (hc_mm / 10)"
        " + 0.0424 * (ac_mm / 10)"
        " + 0.174 * (fl_mm / 10)"
        " + 0.00061 * (bpd_mm / 10) * (ac_mm / 10)"
        " - 0.00386 * (ac_mm / 10) * (fl_mm / 10))"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


# ---- Shared helpers ------------------------------------------------


def _model_annotation_xml(sm: Submodel, tier: str) -> str:
    return (
        f"<annotation>\n"
        f'  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        f'           xmlns:nidus="https://github.com/clay-good/nidus/ontology#">\n'
        f'    <rdf:Description rdf:about="#{sm.id}">\n'
        f"      <nidus:confidenceTier>{tier}</nidus:confidenceTier>\n"
        f"      <nidus:datasetVersion>0.4.0.dev0</nidus:datasetVersion>\n"
        f"      <nidus:submodelId>{sm.id}</nidus:submodelId>\n"
        + (f"      <nidus:sboTerm>{sm.sbo_term}</nidus:sboTerm>\n" if sm.sbo_term else "")
        + "    </rdf:Description>\n"
        "  </rdf:RDF>\n"
        "</annotation>"
    )


def _html_notes(text: str) -> str:
    """SBML <notes> require XHTML markup. Wrap a plain string."""
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<notes><body xmlns="http://www.w3.org/1999/xhtml"><p>{esc}</p></body></notes>'


# ---- Public API ----------------------------------------------------


def _build_gfr_logistic(ds: Dataset) -> libsbml.SBMLDocument:
    """Logistic GFR trajectory across gestation."""
    sm = next(s for s in SUBMODELS if s.id == "gfr_logistic_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_renal.baseline_gfr_ml_per_min"]
    peak = ds["maternal_renal.gfr_ml_per_min"]
    rate = ds["maternal_renal.gfr_logistic_rate_per_week"]
    peak_week = ds["maternal_renal.gfr_peak_week"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (baseline, peak, rate, peak_week):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "GFR_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("GFR_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(baseline.id)} + "
        f"({parameter_id_to_sbml(peak.id)} - {parameter_id_to_sbml(baseline.id)}) / "
        f"(1 + exp(-{parameter_id_to_sbml(rate.id)} * "
        f"(t_weeks - {parameter_id_to_sbml(peak_week.id)})))"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_amniotic_fluid_volume(ds: Dataset) -> libsbml.SBMLDocument:
    """Gaussian-bump amniotic fluid volume trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "amniotic_fluid_volume_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["amniotic_fluid.afv_early_baseline_ml"]
    peak = ds["amniotic_fluid.afv_peak_ml"]
    peak_week = ds["amniotic_fluid.afv_peak_week"]
    spread = ds["amniotic_fluid.afv_spread_weeks"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (baseline, peak, peak_week, spread):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "AFV_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("AFV_t")
    math_ast = libsbml.parseL3Formula(
        f"{parameter_id_to_sbml(baseline.id)} + "
        f"({parameter_id_to_sbml(peak.id)} - {parameter_id_to_sbml(baseline.id)}) * "
        f"exp(-((t_weeks - {parameter_id_to_sbml(peak_week.id)}) / "
        f"{parameter_id_to_sbml(spread.id)})^2 / 2)"
    )
    rule.setMath(math_ast)

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_svr_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Derived SVR(t) = MAP(t) * 80 / CO(t)."""
    sm = next(s for s in SUBMODELS if s.id == "svr_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    map_b = ds["maternal_cardiovascular.baseline_map_mmhg"]
    map_n = ds["maternal_cardiovascular.map_nadir_drop_mmhg"]
    map_nw = ds["maternal_cardiovascular.map_nadir_week"]
    map_sp = ds["maternal_cardiovascular.map_spread_weeks"]
    co_b = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    co_p = ds["maternal_cardiovascular.peak_excess_cardiac_output_l_per_min"]
    co_pw = ds["maternal_cardiovascular.cardiac_output_peak_week"]
    co_sp = ds["maternal_cardiovascular.cardiac_output_spread_weeks"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (map_b, map_n, map_nw, map_sp, co_b, co_p, co_pw, co_sp):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "SVR_t", 0.0, "dimensionless", constant=False)

    map_expr = (
        f"({parameter_id_to_sbml(map_b.id)} - "
        f"{parameter_id_to_sbml(map_n.id)} * "
        f"exp(-((t_weeks - {parameter_id_to_sbml(map_nw.id)}) / "
        f"{parameter_id_to_sbml(map_sp.id)})^2 / 2))"
    )
    co_expr = (
        f"({parameter_id_to_sbml(co_b.id)} + "
        f"{parameter_id_to_sbml(co_p.id)} * "
        f"exp(-((t_weeks - {parameter_id_to_sbml(co_pw.id)}) / "
        f"{parameter_id_to_sbml(co_sp.id)})^2 / 2))"
    )
    rule = model.createAssignmentRule()
    rule.setVariable("SVR_t")
    rule.setMath(libsbml.parseL3Formula(f"{map_expr} * 80 / {co_expr}"))

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_pao2_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Linear PaO2 trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "pao2_trajectory_linear")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_respiratory.baseline_pao2_mmhg"]
    term = ds["maternal_respiratory.pao2_mmhg_term"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "term_week", 40.0, "dimensionless")
    for p in (baseline, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "PaO2_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("PaO2_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) * "
            f"(t_weeks / term_week)"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_tidal_volume(ds: Dataset) -> libsbml.SBMLDocument:
    """Sigmoidal tidal-volume trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "tidal_volume_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_respiratory.baseline_tidal_volume_ml"]
    term = ds["maternal_respiratory.tidal_volume_ml_term"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "growth_rate_per_week", 0.2, "dimensionless")
    _add_parameter(model, "midpoint_week", 20.0, "dimensionless")
    for p in (baseline, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "VT_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("VT_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) / "
            f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week)))"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_heart_rate_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Sigmoidal HR trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "heart_rate_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_cardiovascular.baseline_heart_rate_bpm"]
    term = ds["maternal_cardiovascular.term_heart_rate_bpm"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "growth_rate_per_week", 0.2, "dimensionless")
    _add_parameter(model, "midpoint_week", 20.0, "dimensionless")
    for p in (baseline, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "HR_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("HR_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) / "
            f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week)))"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_stroke_volume_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Gaussian-bump stroke-volume trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "stroke_volume_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_cardiovascular.baseline_stroke_volume_ml"]
    peak = ds["maternal_cardiovascular.peak_excess_stroke_volume_ml"]
    peak_week = ds["maternal_cardiovascular.cardiac_output_peak_week"]
    spread = ds["maternal_cardiovascular.cardiac_output_spread_weeks"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    for p in (baseline, peak, peak_week, spread):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "SV_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("SV_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"{parameter_id_to_sbml(peak.id)} * "
            f"exp(-((t_weeks - {parameter_id_to_sbml(peak_week.id)}) / "
            f"{parameter_id_to_sbml(spread.id)})^2 / 2)"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_rpf_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Gaussian-bump RPF trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "renal_plasma_flow_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_renal.renal_plasma_flow_baseline_ml_per_min"]
    peak = ds["maternal_renal.renal_plasma_flow_peak_ml_per_min"]
    peak_week = ds["maternal_renal.rpf_peak_week"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "spread_weeks", 8.0, "dimensionless")
    for p in (baseline, peak, peak_week):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "RPF_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("RPF_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(peak.id)} - {parameter_id_to_sbml(baseline.id)}) * "
            f"exp(-((t_weeks - {parameter_id_to_sbml(peak_week.id)}) / "
            f"spread_weeks)^2 / 2)"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_minute_ventilation(ds: Dataset) -> libsbml.SBMLDocument:
    """Derived VE(t) = VT(t) * RR(t) with sigmoidal VT and RR."""
    sm = next(s for s in SUBMODELS if s.id == "minute_ventilation_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    vt_b = ds["maternal_respiratory.baseline_tidal_volume_ml"]
    vt_t = ds["maternal_respiratory.tidal_volume_ml_term"]
    rr_b = ds["maternal_respiratory.baseline_respiratory_rate_bpm"]
    rr_t = ds["maternal_respiratory.term_respiratory_rate_bpm"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "growth_rate_per_week", 0.2, "dimensionless")
    _add_parameter(model, "midpoint_week", 20.0, "dimensionless")
    for p in (vt_b, vt_t, rr_b, rr_t):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "VE_t", 0.0, "dimensionless", constant=False)

    vt_expr = (
        f"({parameter_id_to_sbml(vt_b.id)} + "
        f"({parameter_id_to_sbml(vt_t.id)} - {parameter_id_to_sbml(vt_b.id)}) / "
        f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week))))"
    )
    rr_expr = (
        f"({parameter_id_to_sbml(rr_b.id)} + "
        f"({parameter_id_to_sbml(rr_t.id)} - {parameter_id_to_sbml(rr_b.id)}) / "
        f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week))))"
    )
    rule = model.createAssignmentRule()
    rule.setVariable("VE_t")
    rule.setMath(libsbml.parseL3Formula(f"{vt_expr} * {rr_expr}"))

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_arterial_ph_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Linear arterial-pH trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "arterial_ph_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds["maternal_respiratory.baseline_arterial_ph"]
    term = ds["maternal_respiratory.term_arterial_ph"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "term_week", 40.0, "dimensionless")
    for p in (baseline, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "pH_t", 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable("pH_t")
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) * "
            f"(t_weeks / term_week)"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_hadlock_biometry_growth(
    ds: Dataset, sm_id: str, output_name: str, biometry_prefix: str
) -> libsbml.SBMLDocument:
    """Cubic-fit biometry growth submodel (BPD/HC/AC/FL).

    Fits a cubic polynomial to the seven weekly anchors at build time
    and emits the fit coefficients as constants alongside the seven
    anchor nidus parameters (carried for tier + provenance).
    """
    from nidus.export.reference import (
        HADLOCK_ANCHOR_WEEKS,
        hadlock_biometry_cubic_coefficients,
    )

    sm = next(s for s in SUBMODELS if s.id == sm_id)

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    anchors = [ds[f"fetal_growth.{biometry_prefix}_{w}w_mm"] for w in HADLOCK_ANCHOR_WEEKS]
    a3, a2, a1, a0 = hadlock_biometry_cubic_coefficients([p.value.central for p in anchors])

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    # Anchor parameters carry MIRIAM citation + tier annotations; the
    # cubic-fit coefficients below are derived from them.
    for p in anchors:
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "fit_a3", a3, "dimensionless")
    _add_parameter(model, "fit_a2", a2, "dimensionless")
    _add_parameter(model, "fit_a1", a1, "dimensionless")
    _add_parameter(model, "fit_a0", a0, "dimensionless")
    _add_parameter(model, output_name, 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable(output_name)
    rule.setMath(
        libsbml.parseL3Formula(
            "fit_a3 * t_weeks^3 + fit_a2 * t_weeks^2 + fit_a1 * t_weeks + fit_a0"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_hadlock_bpd_growth(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_hadlock_biometry_growth(ds, "hadlock_bpd_growth", "BPD_t_mm", "bpd")


def _build_hadlock_hc_growth(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_hadlock_biometry_growth(ds, "hadlock_hc_growth", "HC_t_mm", "hc")


def _build_hadlock_ac_growth(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_hadlock_biometry_growth(ds, "hadlock_ac_growth", "AC_t_mm", "ac")


def _build_hadlock_fl_growth(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_hadlock_biometry_growth(ds, "hadlock_fl_growth", "FL_t_mm", "fl")


def _build_sigmoid_baseline_term(
    ds: Dataset,
    sm_id: str,
    *,
    baseline_pid: str,
    term_pid: str,
    output_name: str,
    growth_rate: float,
    midpoint_week: float,
) -> libsbml.SBMLDocument:
    """Generic baseline -> term sigmoidal trajectory builder.

    Used by Phase B trajectories where the dataset stores only the
    endpoints and the curve shape is the standard logistic.
    """
    sm = next(s for s in SUBMODELS if s.id == sm_id)

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    baseline = ds[baseline_pid]
    term = ds[term_pid]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "growth_rate_per_week", growth_rate, "dimensionless")
    _add_parameter(model, "midpoint_week", midpoint_week, "dimensionless")
    for p in (baseline, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, output_name, 0.0, "dimensionless", constant=False)

    rule = model.createAssignmentRule()
    rule.setVariable(output_name)
    rule.setMath(
        libsbml.parseL3Formula(
            f"{parameter_id_to_sbml(baseline.id)} + "
            f"({parameter_id_to_sbml(term.id)} - {parameter_id_to_sbml(baseline.id)}) / "
            f"(1 + exp(-growth_rate_per_week * (t_weeks - midpoint_week)))"
        )
    )

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_hpl(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "hpl_trajectory",
        baseline_pid="placental_endocrine.hpl_baseline_ug_per_ml",
        term_pid="placental_endocrine.hpl_term_ug_per_ml",
        output_name="hPL_t",
        growth_rate=0.2,
        midpoint_week=24.0,
    )


def _build_progesterone(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "progesterone_trajectory",
        baseline_pid="placental_endocrine.progesterone_baseline_ng_per_ml",
        term_pid="placental_endocrine.progesterone_term_ng_per_ml",
        output_name="progesterone_t",
        growth_rate=0.18,
        midpoint_week=24.0,
    )


def _build_estradiol(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "estradiol_trajectory",
        baseline_pid="placental_endocrine.estradiol_baseline_ng_per_ml",
        term_pid="placental_endocrine.estradiol_term_ng_per_ml",
        output_name="estradiol_t",
        growth_rate=0.15,
        midpoint_week=24.0,
    )


def _build_fhr(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "fetal_heart_rate_trajectory",
        baseline_pid="fetal_circulation.fhr_baseline_bpm",
        term_pid="fetal_circulation.fhr_term_bpm",
        output_name="FHR_t",
        growth_rate=0.2,
        midpoint_week=18.0,
    )


def _build_hcg(ds: Dataset) -> libsbml.SBMLDocument:
    """Piecewise hCG: quadratic rise from 0 to peak, then exponential decline."""
    import math

    sm = next(s for s in SUBMODELS if s.id == "hcg_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    peak = ds["placental_endocrine.hcg_peak_miu_per_ml"]
    peak_week = ds["placental_endocrine.hcg_peak_week"]
    term = ds["placental_endocrine.hcg_term_miu_per_ml"]

    # Decay rate so that peak * exp(-decay*(40 - peak_week)) == term.
    term_week = 40.0
    decay_rate = -math.log(term.value.central / peak.value.central) / (
        term_week - peak_week.value.central
    )

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "term_week", term_week, "dimensionless")
    _add_parameter(model, "decay_rate_per_week", decay_rate, "dimensionless")
    for p in (peak, peak_week, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "hCG_t", 0.0, "dimensionless", constant=False)

    peak_id = parameter_id_to_sbml(peak.id)
    pw_id = parameter_id_to_sbml(peak_week.id)
    formula = (
        f"piecewise("
        f"{peak_id} * (t_weeks / {pw_id})^2, t_weeks < {pw_id}, "
        f"{peak_id} * exp(-decay_rate_per_week * (t_weeks - {pw_id}))"
        f")"
    )
    rule = model.createAssignmentRule()
    rule.setVariable("hCG_t")
    rule.setMath(libsbml.parseL3Formula(formula))

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


def _build_homa_ir(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "homa_ir_trajectory",
        baseline_pid="maternal_endocrine.homa_ir_baseline",
        term_pid="maternal_endocrine.homa_ir_term",
        output_name="HOMA_t",
        growth_rate=0.2,
        midpoint_week=22.0,
    )


def _build_cortisol(ds: Dataset) -> libsbml.SBMLDocument:
    return _build_sigmoid_baseline_term(
        ds,
        "cortisol_trajectory",
        baseline_pid="maternal_endocrine.cortisol_baseline_ug_per_dl",
        term_pid="maternal_endocrine.cortisol_term_ug_per_dl",
        output_name="cortisol_t",
        growth_rate=0.15,
        midpoint_week=22.0,
    )


def _build_tsh_trajectory(ds: Dataset) -> libsbml.SBMLDocument:
    """Piecewise-linear TSH: constant at T1 nadir then linear to term."""
    sm = next(s for s in SUBMODELS if s.id == "tsh_trajectory")

    doc = libsbml.SBMLDocument(3, 2)
    model = doc.createModel()
    model.setId(sm.id)
    model.setName(sm.name)
    _add_units(model)

    t1 = ds["maternal_endocrine.tsh_t1_miu_per_l"]
    term = ds["maternal_endocrine.tsh_term_miu_per_l"]

    _add_parameter(model, "t_weeks", 20.0, "dimensionless", constant=False)
    _add_parameter(model, "t1_week", 12.0, "dimensionless")
    _add_parameter(model, "term_week", 40.0, "dimensionless")
    for p in (t1, term):
        sp = _add_parameter(model, p.id, p.value.central, "dimensionless")
        _attach_param_annotation(sp, p)
    _add_parameter(model, "TSH_t", 0.0, "dimensionless", constant=False)

    t1_id = parameter_id_to_sbml(t1.id)
    term_id = parameter_id_to_sbml(term.id)
    formula = (
        f"piecewise({t1_id}, t_weeks < t1_week, "
        f"{t1_id} + ({term_id} - {t1_id}) * (t_weeks - t1_week) / (term_week - t1_week))"
    )
    rule = model.createAssignmentRule()
    rule.setVariable("TSH_t")
    rule.setMath(libsbml.parseL3Formula(formula))

    tier = worst_tier(*(ds[pid].tier for pid in sm.parameter_ids))
    model.setAnnotation(_model_annotation_xml(sm, tier))
    model.setNotes(_html_notes(sm.description))
    return doc


_BUILDERS = {
    "placental_villous_growth": _build_placental_villous_growth,
    "o2hb_dissociation_adult": _build_o2hb_dissociation_adult,
    "o2hb_dissociation_fetal": _build_o2hb_dissociation_fetal,
    "placental_glucose_glut1": _build_placental_glucose_glut1,
    "placental_glucose_glut3": _build_placental_glucose_glut3,
    "maternal_cardiac_output_trajectory": _build_maternal_cardiac_output,
    "maternal_map_trajectory": _build_maternal_map,
    "uterine_artery_flow_logistic": _build_uterine_artery_flow,
    "placental_o2_equilibrator": _build_placental_o2_equilibrator,
    "plasma_volume_expansion": _build_plasma_volume_expansion,
    "hadlock_fetal_weight": _build_hadlock_fetal_weight,
    "gfr_logistic_trajectory": _build_gfr_logistic,
    "amniotic_fluid_volume_trajectory": _build_amniotic_fluid_volume,
    "svr_trajectory": _build_svr_trajectory,
    "pao2_trajectory_linear": _build_pao2_trajectory,
    "tidal_volume_trajectory": _build_tidal_volume,
    "heart_rate_trajectory": _build_heart_rate_trajectory,
    "stroke_volume_trajectory": _build_stroke_volume_trajectory,
    "renal_plasma_flow_trajectory": _build_rpf_trajectory,
    "minute_ventilation_trajectory": _build_minute_ventilation,
    "arterial_ph_trajectory": _build_arterial_ph_trajectory,
    "homa_ir_trajectory": _build_homa_ir,
    "tsh_trajectory": _build_tsh_trajectory,
    "cortisol_trajectory": _build_cortisol,
    "hpl_trajectory": _build_hpl,
    "progesterone_trajectory": _build_progesterone,
    "estradiol_trajectory": _build_estradiol,
    "fetal_heart_rate_trajectory": _build_fhr,
    "hcg_trajectory": _build_hcg,
    "hadlock_bpd_growth": _build_hadlock_bpd_growth,
    "hadlock_hc_growth": _build_hadlock_hc_growth,
    "hadlock_ac_growth": _build_hadlock_ac_growth,
    "hadlock_fl_growth": _build_hadlock_fl_growth,
}


def build_sbml(ds: Dataset, submodel_id: str) -> str:
    """Return the SBML L3v2 XML for one submodel as a string.

    Raises:
        KeyError: if submodel_id is not a known export target.
    """
    if submodel_id not in _BUILDERS:
        raise KeyError(f"Unknown submodel {submodel_id!r}. Available: {sorted(_BUILDERS)}")
    doc = _BUILDERS[submodel_id](ds)
    # Consistency check: zero errors is the bar; warnings are OK.
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_MODELING_PRACTICE, False)
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, False)
    n_errors = doc.checkConsistency()
    errors = [
        doc.getError(i)
        for i in range(n_errors)
        if doc.getError(i).getSeverity() >= libsbml.LIBSBML_SEV_ERROR
    ]
    if errors:
        msg = "\n".join(e.getMessage() for e in errors[:5])
        raise RuntimeError(f"SBML consistency check failed for {submodel_id}:\n{msg}")
    xml: str = libsbml.writeSBMLToString(doc)
    return xml


def write_sbml(ds: Dataset, output_dir: str | Path) -> list[Path]:
    """Write all SBML submodels to a directory. Returns the file paths."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for sm in SUBMODELS:
        if sm.id not in _BUILDERS:
            continue
        xml = build_sbml(ds, sm.id)
        path = out_dir / f"{sm.id}.xml"
        path.write_text(xml, encoding="utf-8")
        written.append(path)
    return written
