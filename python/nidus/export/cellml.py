"""CellML 2.0 generator for nidus submodels.

Uses libcellml to build a small CellML model per registry entry. The
math is encoded in MathML. Annotations are attached via the CellML
metadata interface (cmeta:id targets carrying RDF blocks).

CellML 1.1 fallback emission is supported via the ``--cellml-version``
arg on the CLI; libcellml emits 2.0 by default and we down-convert by
adjusting the namespace and a few syntactic differences.
"""

from __future__ import annotations

from pathlib import Path

import libcellml  # type: ignore[import-untyped]

from nidus.export.annotate import (
    parameter_id_to_sbml,
)
from nidus.export.registry import SUBMODELS
from nidus.load import Dataset

MATHML_NS = "http://www.w3.org/1998/Math/MathML"


def _mathml(content: str) -> str:
    """Wrap MathML content in the math element with proper namespace."""
    return f'<math xmlns="{MATHML_NS}">\n{content}\n</math>'


def _apply_assign(var: str, rhs_xml: str) -> str:
    """MathML for an assignment `var := rhs`."""
    return f"<apply>\n  <eq/>\n  <ci>{var}</ci>\n{rhs_xml}\n</apply>"


def _add_variable(
    component: libcellml.Component,
    name: str,
    *,
    units: str,
    initial_value: str | None = None,
    interface: str = "public",
) -> libcellml.Variable:
    v = libcellml.Variable()
    v.setName(name)
    v.setUnits(units)
    if initial_value is not None:
        v.setInitialValue(initial_value)
    v.setInterfaceType(interface)
    component.addVariable(v)
    return v


def _ensure_units(model: libcellml.Model) -> None:
    """Register the unit definitions we'll use."""
    for unit_name, _base_kind in [
        ("per_week", None),  # custom
        ("mmHg", None),
        ("m_squared", None),
        ("mmol_per_l", None),
    ]:
        if model.units(unit_name) is not None:
            continue
        u = libcellml.Units(unit_name)
        if unit_name == "per_week":
            u.addUnit("second", 1, -1.0, 1.0 / (60 * 60 * 24 * 7))
        elif unit_name == "mmHg":
            u.addUnit("pascal", 1, 1.0, 133.322)
        elif unit_name == "m_squared":
            u.addUnit("metre", 1, 2.0, 1.0)
        elif unit_name == "mmol_per_l":
            u.addUnit("mole", -3, 1.0, 1.0)
            u.addUnit("litre", 1, -1.0, 1.0)
        model.addUnits(u)


def _ci(name: str) -> str:
    return f"<ci>{name}</ci>"


def _cn(val: str | float, units: str = "dimensionless") -> str:
    return f'<cn cellml:units="{units}">{val}</cn>'


def _apply(op: str, *args: str) -> str:
    inner = "\n".join(args)
    return f"<apply>\n<{op}/>\n{inner}\n</apply>"


# ---- Submodel constructors -----------------------------------------


def _build_placental_villous_growth(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "placental_villous_growth")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    A0 = ds["placental_structure.initial_area_m2"]
    K = ds["placental_structure.term_area_m2"]
    r = ds["placental_structure.growth_rate_per_week"]
    tmid = ds["placental_structure.midpoint_week"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(
        comp, parameter_id_to_sbml(A0.id), units="m_squared", initial_value=str(A0.value.central)
    )
    _add_variable(
        comp, parameter_id_to_sbml(K.id), units="m_squared", initial_value=str(K.value.central)
    )
    _add_variable(
        comp, parameter_id_to_sbml(r.id), units="per_week", initial_value=str(r.value.central)
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(tmid.id),
        units="dimensionless",
        initial_value=str(tmid.value.central),
    )
    _add_variable(comp, "A_t_m_squared", units="m_squared", initial_value="0")

    A0_id = parameter_id_to_sbml(A0.id)
    K_id = parameter_id_to_sbml(K.id)
    r_id = parameter_id_to_sbml(r.id)
    tmid_id = parameter_id_to_sbml(tmid.id)

    rhs = (
        f"<apply>\n"
        f"  <plus/>\n"
        f"  <ci>{A0_id}</ci>\n"
        f"  <apply>\n"
        f"    <divide/>\n"
        f"    <apply>\n"
        f"      <minus/>\n"
        f"      <ci>{K_id}</ci>\n"
        f"      <ci>{A0_id}</ci>\n"
        f"    </apply>\n"
        f"    <apply>\n"
        f"      <plus/>\n"
        f'      <cn cellml:units="dimensionless">1</cn>\n'
        f"      <apply>\n"
        f"        <exp/>\n"
        f"        <apply>\n"
        f"          <minus/>\n"
        f"          <apply>\n"
        f"            <times/>\n"
        f"            <ci>{r_id}</ci>\n"
        f"            <apply>\n"
        f"              <minus/>\n"
        f"              <ci>t_weeks</ci>\n"
        f"              <ci>{tmid_id}</ci>\n"
        f"            </apply>\n"
        f"          </apply>\n"
        f"        </apply>\n"
        f"      </apply>\n"
        f"    </apply>\n"
        f"  </apply>\n"
        f"</apply>"
    )
    comp.setMath(_mathml(_apply_assign("A_t_m_squared", rhs)))
    return model


def _build_o2hb_dissociation_adult(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "o2hb_dissociation_adult")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    p50 = ds["maternal_blood.o2_hb_p50_maternal"]
    hill = ds["maternal_blood.o2_hb_hill_coefficient_maternal"]

    _add_variable(comp, "po2_mmhg", units="mmHg", initial_value="50")
    _add_variable(
        comp, parameter_id_to_sbml(p50.id), units="mmHg", initial_value=str(p50.value.central)
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(hill.id),
        units="dimensionless",
        initial_value=str(hill.value.central),
    )
    _add_variable(comp, "saturation", units="dimensionless", initial_value="0")

    # S = 1 / (1 + (PO2^3 + 150*PO2)^-1 * 23400)
    rhs = (
        "<apply>\n"
        "  <divide/>\n"
        '  <cn cellml:units="dimensionless">1</cn>\n'
        "  <apply>\n"
        "    <plus/>\n"
        "    <apply>\n"
        "      <times/>\n"
        "      <apply>\n"
        "        <divide/>\n"
        '        <cn cellml:units="dimensionless">1</cn>\n'
        "        <apply>\n"
        "          <plus/>\n"
        "          <apply>\n"
        "            <power/>\n"
        "            <ci>po2_mmhg</ci>\n"
        '            <cn cellml:units="dimensionless">3</cn>\n'
        "          </apply>\n"
        "          <apply>\n"
        "            <times/>\n"
        '            <cn cellml:units="dimensionless">150</cn>\n'
        "            <ci>po2_mmhg</ci>\n"
        "          </apply>\n"
        "        </apply>\n"
        "      </apply>\n"
        '      <cn cellml:units="dimensionless">23400</cn>\n'
        "    </apply>\n"
        '    <cn cellml:units="dimensionless">1</cn>\n'
        "  </apply>\n"
        "</apply>"
    )
    comp.setMath(_mathml(_apply_assign("saturation", rhs)))
    return model


def _build_o2hb_dissociation_fetal(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "o2hb_dissociation_fetal")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    p50 = ds["fetal_metabolism.fetal_p50_mmhg"]
    _add_variable(comp, "po2_mmhg", units="mmHg", initial_value="30")
    _add_variable(
        comp, parameter_id_to_sbml(p50.id), units="mmHg", initial_value=str(p50.value.central)
    )
    _add_variable(comp, "hill_coefficient_hbf", units="dimensionless", initial_value="2.85")
    _add_variable(comp, "saturation", units="dimensionless", initial_value="0")

    p50_id = parameter_id_to_sbml(p50.id)
    # S = (PO2/P50)^n / (1 + (PO2/P50)^n)
    rhs = (
        "<apply>\n"
        "  <divide/>\n"
        "  <apply>\n"
        "    <power/>\n"
        "    <apply>\n"
        "      <divide/>\n"
        "      <ci>po2_mmhg</ci>\n"
        f"      <ci>{p50_id}</ci>\n"
        "    </apply>\n"
        "    <ci>hill_coefficient_hbf</ci>\n"
        "  </apply>\n"
        "  <apply>\n"
        "    <plus/>\n"
        '    <cn cellml:units="dimensionless">1</cn>\n'
        "    <apply>\n"
        "      <power/>\n"
        "      <apply>\n"
        "        <divide/>\n"
        "        <ci>po2_mmhg</ci>\n"
        f"        <ci>{p50_id}</ci>\n"
        "      </apply>\n"
        "      <ci>hill_coefficient_hbf</ci>\n"
        "    </apply>\n"
        "  </apply>\n"
        "</apply>"
    )
    comp.setMath(_mathml(_apply_assign("saturation", rhs)))
    return model


def _build_placental_glucose_glut1(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "placental_glucose_glut1")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    km = ds["placental_glucose.glucose_glut1_km_mmol_per_l"]
    vmax = ds["placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2"]

    _add_variable(comp, "substrate_mmol_per_l", units="mmol_per_l", initial_value="5")
    _add_variable(
        comp, parameter_id_to_sbml(km.id), units="mmol_per_l", initial_value=str(km.value.central)
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(vmax.id),
        units="dimensionless",
        initial_value=str(vmax.value.central),
    )
    _add_variable(comp, "flux", units="dimensionless", initial_value="0")

    km_id = parameter_id_to_sbml(km.id)
    vmax_id = parameter_id_to_sbml(vmax.id)
    rhs = (
        "<apply>\n"
        "  <divide/>\n"
        "  <apply>\n"
        "    <times/>\n"
        f"    <ci>{vmax_id}</ci>\n"
        "    <ci>substrate_mmol_per_l</ci>\n"
        "  </apply>\n"
        "  <apply>\n"
        "    <plus/>\n"
        f"    <ci>{km_id}</ci>\n"
        "    <ci>substrate_mmol_per_l</ci>\n"
        "  </apply>\n"
        "</apply>"
    )
    comp.setMath(_mathml(_apply_assign("flux", rhs)))
    return model


def _build_mm_glut(ds: Dataset, sm_id: str, km_pid: str, vmax_pid: str) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == sm_id)
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    km = ds[km_pid]
    vmax = ds[vmax_pid]

    _add_variable(comp, "substrate_mmol_per_l", units="mmol_per_l", initial_value="5")
    _add_variable(
        comp, parameter_id_to_sbml(km.id), units="mmol_per_l", initial_value=str(km.value.central)
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(vmax.id),
        units="dimensionless",
        initial_value=str(vmax.value.central),
    )
    _add_variable(comp, "flux", units="dimensionless", initial_value="0")

    km_id = parameter_id_to_sbml(km.id)
    vmax_id = parameter_id_to_sbml(vmax.id)
    rhs = _apply(
        "divide",
        _apply("times", _ci(vmax_id), _ci("substrate_mmol_per_l")),
        _apply("plus", _ci(km_id), _ci("substrate_mmol_per_l")),
    )
    comp.setMath(_mathml(_apply_assign("flux", rhs)))
    return model


def _build_placental_glucose_glut3(ds: Dataset) -> libcellml.Model:
    return _build_mm_glut(
        ds,
        "placental_glucose_glut3",
        "placental_glucose.glucose_glut3_km_mmol_per_l",
        "placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2",
    )


def _build_gaussian(
    ds: Dataset,
    sm_id: str,
    *,
    baseline_pid: str,
    amplitude_pid: str,
    center_pid: str,
    spread_pid: str,
    output_name: str,
    sign: str,  # "plus" for bump, "minus" for nadir
) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == sm_id)
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds[baseline_pid]
    amp = ds[amplitude_pid]
    center = ds[center_pid]
    spread = ds[spread_pid]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    for p in (baseline, amp, center, spread):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, output_name, units="dimensionless", initial_value="0")

    bid = parameter_id_to_sbml(baseline.id)
    aid = parameter_id_to_sbml(amp.id)
    cid = parameter_id_to_sbml(center.id)
    sid = parameter_id_to_sbml(spread.id)
    # z = (t - center) / spread
    z = _apply("divide", _apply("minus", _ci("t_weeks"), _ci(cid)), _ci(sid))
    # bump = amp * exp(-z^2 / 2)
    bump = _apply(
        "times",
        _ci(aid),
        _apply(
            "exp",
            _apply(
                "divide",
                _apply("minus", _apply("power", z, _cn("2"))),
                _cn("2"),
            ),
        ),
    )
    rhs = _apply(sign, _ci(bid), bump)
    comp.setMath(_mathml(_apply_assign(output_name, rhs)))
    return model


def _build_maternal_cardiac_output(ds: Dataset) -> libcellml.Model:
    return _build_gaussian(
        ds,
        "maternal_cardiac_output_trajectory",
        baseline_pid="maternal_cardiovascular.baseline_cardiac_output_l_per_min",
        amplitude_pid="maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
        center_pid="maternal_cardiovascular.cardiac_output_peak_week",
        spread_pid="maternal_cardiovascular.cardiac_output_spread_weeks",
        output_name="CO_t",
        sign="plus",
    )


def _build_maternal_map(ds: Dataset) -> libcellml.Model:
    return _build_gaussian(
        ds,
        "maternal_map_trajectory",
        baseline_pid="maternal_cardiovascular.baseline_map_mmhg",
        amplitude_pid="maternal_cardiovascular.map_nadir_drop_mmhg",
        center_pid="maternal_cardiovascular.map_nadir_week",
        spread_pid="maternal_cardiovascular.map_spread_weeks",
        output_name="MAP_t",
        sign="minus",
    )


def _build_logistic(
    ds: Dataset,
    sm_id: str,
    *,
    a0_pid: str,
    k_pid: str,
    r_pid: str,
    midpoint: str | float,
    midpoint_pid: str | None,
    output_name: str,
) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == sm_id)
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    A0 = ds[a0_pid]
    K = ds[k_pid]
    r = ds[r_pid]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    for p in (A0, K, r):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    if midpoint_pid is None:
        _add_variable(comp, "midpoint_week", units="dimensionless", initial_value=str(midpoint))
        tmid_ref = "midpoint_week"
    else:
        tmid = ds[midpoint_pid]
        _add_variable(
            comp,
            parameter_id_to_sbml(tmid.id),
            units="dimensionless",
            initial_value=str(tmid.value.central),
        )
        tmid_ref = parameter_id_to_sbml(tmid.id)
    _add_variable(comp, output_name, units="dimensionless", initial_value="0")

    A0_id = parameter_id_to_sbml(A0.id)
    K_id = parameter_id_to_sbml(K.id)
    r_id = parameter_id_to_sbml(r.id)

    # A0 + (K - A0) / (1 + exp(-r * (t - tmid)))
    rhs = _apply(
        "plus",
        _ci(A0_id),
        _apply(
            "divide",
            _apply("minus", _ci(K_id), _ci(A0_id)),
            _apply(
                "plus",
                _cn("1"),
                _apply(
                    "exp",
                    _apply(
                        "minus",
                        _apply(
                            "times",
                            _ci(r_id),
                            _apply("minus", _ci("t_weeks"), _ci(tmid_ref)),
                        ),
                    ),
                ),
            ),
        ),
    )
    comp.setMath(_mathml(_apply_assign(output_name, rhs)))
    return model


def _build_uterine_artery_flow(ds: Dataset) -> libcellml.Model:
    return _build_logistic(
        ds,
        "uterine_artery_flow_logistic",
        a0_pid="maternal_cardiovascular.baseline_uterine_flow_ml_per_min",
        k_pid="maternal_cardiovascular.term_uterine_flow_ml_per_min",
        r_pid="maternal_cardiovascular.uterine_flow_growth_rate_per_week",
        midpoint=24.0,
        midpoint_pid=None,
        output_name="Q_t",
    )


def _build_plasma_volume_expansion(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "plasma_volume_expansion")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    early = ds["maternal_blood.plasma_volume_early_l"]
    term = ds["maternal_blood.plasma_volume_l"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "growth_rate_per_week", units="dimensionless", initial_value="0.2")
    _add_variable(comp, "midpoint_week", units="dimensionless", initial_value="22")
    _add_variable(
        comp,
        parameter_id_to_sbml(early.id),
        units="dimensionless",
        initial_value=str(early.value.central),
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(term.id),
        units="dimensionless",
        initial_value=str(term.value.central),
    )
    _add_variable(comp, "PV_t", units="dimensionless", initial_value="0")

    e_id = parameter_id_to_sbml(early.id)
    t_id = parameter_id_to_sbml(term.id)
    rhs = _apply(
        "plus",
        _ci(e_id),
        _apply(
            "divide",
            _apply("minus", _ci(t_id), _ci(e_id)),
            _apply(
                "plus",
                _cn("1"),
                _apply(
                    "exp",
                    _apply(
                        "minus",
                        _apply(
                            "times",
                            _ci("growth_rate_per_week"),
                            _apply("minus", _ci("t_weeks"), _ci("midpoint_week")),
                        ),
                    ),
                ),
            ),
        ),
    )
    comp.setMath(_mathml(_apply_assign("PV_t", rhs)))
    return model


def _build_placental_o2_equilibrator(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "placental_o2_equilibrator")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    mat = ds["placental_gas_exchange.maternal_intervillous_po2_mmhg"]
    f_eq = ds["placental_gas_exchange.gas_max_equilibration"]
    _add_variable(
        comp, parameter_id_to_sbml(mat.id), units="mmHg", initial_value=str(mat.value.central)
    )
    _add_variable(
        comp,
        parameter_id_to_sbml(f_eq.id),
        units="dimensionless",
        initial_value=str(f_eq.value.central),
    )
    _add_variable(comp, "umbilical_vein_po2_mmhg", units="mmHg", initial_value="0")

    rhs = _apply(
        "times",
        _ci(parameter_id_to_sbml(mat.id)),
        _ci(parameter_id_to_sbml(f_eq.id)),
    )
    comp.setMath(_mathml(_apply_assign("umbilical_vein_po2_mmhg", rhs)))
    return model


def _build_hadlock_fetal_weight(ds: Dataset) -> libcellml.Model:
    sm = next(s for s in SUBMODELS if s.id == "hadlock_fetal_weight")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    coef = ds["fetal_growth.hadlock_coefficient"]
    _add_variable(comp, "bpd_mm", units="dimensionless", initial_value="80")
    _add_variable(comp, "hc_mm", units="dimensionless", initial_value="300")
    _add_variable(comp, "ac_mm", units="dimensionless", initial_value="300")
    _add_variable(comp, "fl_mm", units="dimensionless", initial_value="60")
    _add_variable(
        comp,
        parameter_id_to_sbml(coef.id),
        units="dimensionless",
        initial_value=str(coef.value.central),
    )
    _add_variable(comp, "efw_g", units="dimensionless", initial_value="0")

    coef_id = parameter_id_to_sbml(coef.id)
    # cm values
    hc_cm = _apply("divide", _ci("hc_mm"), _cn("10"))
    ac_cm = _apply("divide", _ci("ac_mm"), _cn("10"))
    fl_cm = _apply("divide", _ci("fl_mm"), _cn("10"))
    bpd_cm = _apply("divide", _ci("bpd_mm"), _cn("10"))

    log_w = _apply(
        "plus",
        _ci(coef_id),
        _apply("times", _cn("0.0064"), hc_cm),
        _apply("times", _cn("0.0424"), ac_cm),
        _apply("times", _cn("0.174"), fl_cm),
        _apply("times", _cn("0.00061"), bpd_cm, ac_cm),
        _apply("times", _cn("-0.00386"), ac_cm, fl_cm),
    )
    rhs = _apply("power", _cn("10"), log_w)
    comp.setMath(_mathml(_apply_assign("efw_g", rhs)))
    return model


def _build_gfr_logistic(ds: Dataset) -> libcellml.Model:
    return _build_logistic(
        ds,
        "gfr_logistic_trajectory",
        a0_pid="maternal_renal.baseline_gfr_ml_per_min",
        k_pid="maternal_renal.gfr_ml_per_min",
        r_pid="maternal_renal.gfr_logistic_rate_per_week",
        midpoint=16.0,
        midpoint_pid="maternal_renal.gfr_peak_week",
        output_name="GFR_t",
    )


def _build_amniotic_fluid_volume(ds: Dataset) -> libcellml.Model:
    """Gaussian-bump AFV trajectory.

    The standard `_build_gaussian` helper expects an amplitude (peak
    excess over baseline) parameter; the AFV dataset entries supply
    the absolute peak instead, so the amplitude = peak - baseline
    subtraction is performed inline.
    """
    sm = next(s for s in SUBMODELS if s.id == "amniotic_fluid_volume_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["amniotic_fluid.afv_early_baseline_ml"]
    peak = ds["amniotic_fluid.afv_peak_ml"]
    center = ds["amniotic_fluid.afv_peak_week"]
    spread = ds["amniotic_fluid.afv_spread_weeks"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    for p in (baseline, peak, center, spread):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "AFV_t", units="dimensionless", initial_value="0")

    bid = parameter_id_to_sbml(baseline.id)
    pid_ = parameter_id_to_sbml(peak.id)
    cid = parameter_id_to_sbml(center.id)
    sid = parameter_id_to_sbml(spread.id)
    # z = (t - center) / spread
    z = _apply("divide", _apply("minus", _ci("t_weeks"), _ci(cid)), _ci(sid))
    # bump = (peak - baseline) * exp(-z^2 / 2)
    bump = _apply(
        "times",
        _apply("minus", _ci(pid_), _ci(bid)),
        _apply(
            "exp",
            _apply(
                "divide",
                _apply("minus", _apply("power", z, _cn("2"))),
                _cn("2"),
            ),
        ),
    )
    rhs = _apply("plus", _ci(bid), bump)
    comp.setMath(_mathml(_apply_assign("AFV_t", rhs)))
    return model


def _build_svr_trajectory(ds: Dataset) -> libcellml.Model:
    """Derived SVR(t) = MAP(t) * 80 / CO(t)."""
    sm = next(s for s in SUBMODELS if s.id == "svr_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    map_b = ds["maternal_cardiovascular.baseline_map_mmhg"]
    map_n = ds["maternal_cardiovascular.map_nadir_drop_mmhg"]
    map_nw = ds["maternal_cardiovascular.map_nadir_week"]
    map_sp = ds["maternal_cardiovascular.map_spread_weeks"]
    co_b = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    co_p = ds["maternal_cardiovascular.peak_excess_cardiac_output_l_per_min"]
    co_pw = ds["maternal_cardiovascular.cardiac_output_peak_week"]
    co_sp = ds["maternal_cardiovascular.cardiac_output_spread_weeks"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    for p in (map_b, map_n, map_nw, map_sp, co_b, co_p, co_pw, co_sp):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "SVR_t", units="dimensionless", initial_value="0")

    def _gauss(center_id: str, spread_id: str) -> str:
        z = _apply(
            "divide",
            _apply("minus", _ci("t_weeks"), _ci(center_id)),
            _ci(spread_id),
        )
        return _apply(
            "exp",
            _apply(
                "divide",
                _apply("minus", _apply("power", z, _cn("2"))),
                _cn("2"),
            ),
        )

    map_expr = _apply(
        "minus",
        _ci(parameter_id_to_sbml(map_b.id)),
        _apply(
            "times",
            _ci(parameter_id_to_sbml(map_n.id)),
            _gauss(parameter_id_to_sbml(map_nw.id), parameter_id_to_sbml(map_sp.id)),
        ),
    )
    co_expr = _apply(
        "plus",
        _ci(parameter_id_to_sbml(co_b.id)),
        _apply(
            "times",
            _ci(parameter_id_to_sbml(co_p.id)),
            _gauss(parameter_id_to_sbml(co_pw.id), parameter_id_to_sbml(co_sp.id)),
        ),
    )
    rhs = _apply("divide", _apply("times", map_expr, _cn("80")), co_expr)
    comp.setMath(_mathml(_apply_assign("SVR_t", rhs)))
    return model


def _build_pao2_trajectory(ds: Dataset) -> libcellml.Model:
    """Linear PaO2 trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "pao2_trajectory_linear")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["maternal_respiratory.baseline_pao2_mmhg"]
    term = ds["maternal_respiratory.pao2_mmhg_term"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "term_week", units="dimensionless", initial_value="40")
    for p in (baseline, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "PaO2_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    t_id = parameter_id_to_sbml(term.id)
    rhs = _apply(
        "plus",
        _ci(b_id),
        _apply(
            "times",
            _apply("minus", _ci(t_id), _ci(b_id)),
            _apply("divide", _ci("t_weeks"), _ci("term_week")),
        ),
    )
    comp.setMath(_mathml(_apply_assign("PaO2_t", rhs)))
    return model


def _build_tidal_volume(ds: Dataset) -> libcellml.Model:
    """Sigmoidal tidal-volume trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "tidal_volume_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["maternal_respiratory.baseline_tidal_volume_ml"]
    term = ds["maternal_respiratory.tidal_volume_ml_term"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "growth_rate_per_week", units="dimensionless", initial_value="0.2")
    _add_variable(comp, "midpoint_week", units="dimensionless", initial_value="20")
    for p in (baseline, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "VT_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    t_id = parameter_id_to_sbml(term.id)
    rhs = _apply(
        "plus",
        _ci(b_id),
        _apply(
            "divide",
            _apply("minus", _ci(t_id), _ci(b_id)),
            _apply(
                "plus",
                _cn("1"),
                _apply(
                    "exp",
                    _apply(
                        "minus",
                        _apply(
                            "times",
                            _ci("growth_rate_per_week"),
                            _apply("minus", _ci("t_weeks"), _ci("midpoint_week")),
                        ),
                    ),
                ),
            ),
        ),
    )
    comp.setMath(_mathml(_apply_assign("VT_t", rhs)))
    return model


def _build_heart_rate_trajectory(ds: Dataset) -> libcellml.Model:
    """Sigmoidal HR trajectory: HR = baseline + (term-baseline)/(1+exp(-r*(t-mid)))."""
    sm = next(s for s in SUBMODELS if s.id == "heart_rate_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["maternal_cardiovascular.baseline_heart_rate_bpm"]
    term = ds["maternal_cardiovascular.term_heart_rate_bpm"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "growth_rate_per_week", units="dimensionless", initial_value="0.2")
    _add_variable(comp, "midpoint_week", units="dimensionless", initial_value="20")
    for p in (baseline, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "HR_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    t_id = parameter_id_to_sbml(term.id)
    rhs = _apply(
        "plus",
        _ci(b_id),
        _apply(
            "divide",
            _apply("minus", _ci(t_id), _ci(b_id)),
            _apply(
                "plus",
                _cn("1"),
                _apply(
                    "exp",
                    _apply(
                        "minus",
                        _apply(
                            "times",
                            _ci("growth_rate_per_week"),
                            _apply("minus", _ci("t_weeks"), _ci("midpoint_week")),
                        ),
                    ),
                ),
            ),
        ),
    )
    comp.setMath(_mathml(_apply_assign("HR_t", rhs)))
    return model


def _build_stroke_volume_trajectory(ds: Dataset) -> libcellml.Model:
    return _build_gaussian(
        ds,
        "stroke_volume_trajectory",
        baseline_pid="maternal_cardiovascular.baseline_stroke_volume_ml",
        amplitude_pid="maternal_cardiovascular.peak_excess_stroke_volume_ml",
        center_pid="maternal_cardiovascular.cardiac_output_peak_week",
        spread_pid="maternal_cardiovascular.cardiac_output_spread_weeks",
        output_name="SV_t",
        sign="plus",
    )


def _build_rpf_trajectory(ds: Dataset) -> libcellml.Model:
    """Gaussian-bump RPF: amplitude = peak - baseline, fixed spread = 8 weeks."""
    sm = next(s for s in SUBMODELS if s.id == "renal_plasma_flow_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["maternal_renal.renal_plasma_flow_baseline_ml_per_min"]
    peak = ds["maternal_renal.renal_plasma_flow_peak_ml_per_min"]
    peak_week = ds["maternal_renal.rpf_peak_week"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "spread_weeks", units="dimensionless", initial_value="8")
    for p in (baseline, peak, peak_week):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "RPF_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    p_id = parameter_id_to_sbml(peak.id)
    pw_id = parameter_id_to_sbml(peak_week.id)
    z = _apply("divide", _apply("minus", _ci("t_weeks"), _ci(pw_id)), _ci("spread_weeks"))
    bump = _apply(
        "times",
        _apply("minus", _ci(p_id), _ci(b_id)),
        _apply(
            "exp",
            _apply(
                "divide",
                _apply("minus", _apply("power", z, _cn("2"))),
                _cn("2"),
            ),
        ),
    )
    rhs = _apply("plus", _ci(b_id), bump)
    comp.setMath(_mathml(_apply_assign("RPF_t", rhs)))
    return model


def _sigmoid_baseline_term(b_id: str, t_id: str) -> str:
    """Helper: MathML for `baseline + (term-baseline)/(1+exp(-r*(t-mid)))`.

    Assumes variables `growth_rate_per_week`, `midpoint_week`, and
    `t_weeks` are present in the same component.
    """
    return _apply(
        "plus",
        _ci(b_id),
        _apply(
            "divide",
            _apply("minus", _ci(t_id), _ci(b_id)),
            _apply(
                "plus",
                _cn("1"),
                _apply(
                    "exp",
                    _apply(
                        "minus",
                        _apply(
                            "times",
                            _ci("growth_rate_per_week"),
                            _apply("minus", _ci("t_weeks"), _ci("midpoint_week")),
                        ),
                    ),
                ),
            ),
        ),
    )


def _build_minute_ventilation(ds: Dataset) -> libcellml.Model:
    """Derived VE(t) = VT(t) * RR(t)."""
    sm = next(s for s in SUBMODELS if s.id == "minute_ventilation_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    vt_b = ds["maternal_respiratory.baseline_tidal_volume_ml"]
    vt_t = ds["maternal_respiratory.tidal_volume_ml_term"]
    rr_b = ds["maternal_respiratory.baseline_respiratory_rate_bpm"]
    rr_t = ds["maternal_respiratory.term_respiratory_rate_bpm"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "growth_rate_per_week", units="dimensionless", initial_value="0.2")
    _add_variable(comp, "midpoint_week", units="dimensionless", initial_value="20")
    for p in (vt_b, vt_t, rr_b, rr_t):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "VE_t", units="dimensionless", initial_value="0")

    vt_expr = _sigmoid_baseline_term(parameter_id_to_sbml(vt_b.id), parameter_id_to_sbml(vt_t.id))
    rr_expr = _sigmoid_baseline_term(parameter_id_to_sbml(rr_b.id), parameter_id_to_sbml(rr_t.id))
    rhs = _apply("times", vt_expr, rr_expr)
    comp.setMath(_mathml(_apply_assign("VE_t", rhs)))
    return model


def _build_arterial_ph_trajectory(ds: Dataset) -> libcellml.Model:
    """Linear arterial-pH trajectory."""
    sm = next(s for s in SUBMODELS if s.id == "arterial_ph_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["maternal_respiratory.baseline_arterial_ph"]
    term = ds["maternal_respiratory.term_arterial_ph"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "term_week", units="dimensionless", initial_value="40")
    for p in (baseline, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "pH_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    t_id = parameter_id_to_sbml(term.id)
    rhs = _apply(
        "plus",
        _ci(b_id),
        _apply(
            "times",
            _apply("minus", _ci(t_id), _ci(b_id)),
            _apply("divide", _ci("t_weeks"), _ci("term_week")),
        ),
    )
    comp.setMath(_mathml(_apply_assign("pH_t", rhs)))
    return model


def _build_sigmoid_baseline_term(
    ds: Dataset,
    sm_id: str,
    *,
    baseline_pid: str,
    term_pid: str,
    output_name: str,
    growth_rate: float,
    midpoint_week: float,
) -> libcellml.Model:
    """Generic baseline->term sigmoid CellML builder."""
    sm = next(s for s in SUBMODELS if s.id == sm_id)
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds[baseline_pid]
    term = ds[term_pid]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(
        comp, "growth_rate_per_week", units="dimensionless", initial_value=str(growth_rate)
    )
    _add_variable(comp, "midpoint_week", units="dimensionless", initial_value=str(midpoint_week))
    for p in (baseline, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, output_name, units="dimensionless", initial_value="0")

    rhs = _sigmoid_baseline_term(parameter_id_to_sbml(baseline.id), parameter_id_to_sbml(term.id))
    comp.setMath(_mathml(_apply_assign(output_name, rhs)))
    return model


def _build_hpl(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "hpl_trajectory",
        baseline_pid="placental_endocrine.hpl_baseline_ug_per_ml",
        term_pid="placental_endocrine.hpl_term_ug_per_ml",
        output_name="hPL_t",
        growth_rate=0.2,
        midpoint_week=24.0,
    )


def _build_progesterone(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "progesterone_trajectory",
        baseline_pid="placental_endocrine.progesterone_baseline_ng_per_ml",
        term_pid="placental_endocrine.progesterone_term_ng_per_ml",
        output_name="progesterone_t",
        growth_rate=0.18,
        midpoint_week=24.0,
    )


def _build_igg_transfer(ds: Dataset) -> libcellml.Model:
    """HYPOTHESIS-ONLY sigmoidal IgG transfer ratio."""
    return _build_sigmoid_baseline_term(
        ds,
        "maternal_fetal_igg_transfer",
        baseline_pid="placental_structure.igg_transfer_ratio_baseline",
        term_pid="placental_structure.igg_transfer_ratio_term",
        output_name="igg_ratio_t",
        growth_rate=0.25,
        midpoint_week=28.0,
    )


def _build_maternal_microchimerism(ds: Dataset) -> libcellml.Model:
    """HYPOTHESIS-ONLY sigmoidal microchimeric-cell accumulation."""
    return _build_sigmoid_baseline_term(
        ds,
        "maternal_microchimerism_trajectory",
        baseline_pid="maternal_blood.fetal_microchimerism_baseline_cells_per_ml",
        term_pid="maternal_blood.fetal_microchimerism_term_cells_per_ml",
        output_name="microchimerism_cells_per_ml_t",
        growth_rate=0.15,
        midpoint_week=24.0,
    )


def _build_fetal_pulmonary_fluid(ds: Dataset) -> libcellml.Model:
    """HYPOTHESIS-ONLY sigmoidal fetal lung-liquid net rate."""
    return _build_sigmoid_baseline_term(
        ds,
        "fetal_pulmonary_fluid_trajectory",
        baseline_pid="fetal_metabolism.pulmonary_fluid_net_rate_baseline_ml_per_kg_h",
        term_pid="fetal_metabolism.pulmonary_fluid_net_rate_term_ml_per_kg_h",
        output_name="pulmonary_fluid_rate_ml_per_kg_h_t",
        growth_rate=0.4,
        midpoint_week=36.0,
    )


def _build_placental_cortisol_gradient(ds: Dataset) -> libcellml.Model:
    """HYPOTHESIS-ONLY: fetal cortisol = maternal * (1 - inactivation)."""
    sm = next(s for s in SUBMODELS if s.id == "placental_cortisol_gradient")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    frac = ds["placental_structure.hsd2_cortisol_inactivation_fraction"]

    _add_variable(comp, "maternal_cortisol_ug_per_dl", units="dimensionless", initial_value="30")
    _add_variable(
        comp,
        parameter_id_to_sbml(frac.id),
        units="dimensionless",
        initial_value=str(frac.value.central),
    )
    _add_variable(comp, "fetal_cortisol_ug_per_dl", units="dimensionless", initial_value="0")

    frac_id = parameter_id_to_sbml(frac.id)
    rhs = _apply(
        "times",
        _ci("maternal_cortisol_ug_per_dl"),
        _apply("minus", _cn("1"), _ci(frac_id)),
    )
    comp.setMath(_mathml(_apply_assign("fetal_cortisol_ug_per_dl", rhs)))
    return model


def _build_placental_fetal_allometry(ds: Dataset) -> libcellml.Model:
    """PW = a * FW^b."""
    sm = next(s for s in SUBMODELS if s.id == "placental_fetal_allometry")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    a = ds["placental_structure.allometric_coefficient_a"]
    b = ds["placental_structure.allometric_exponent_b"]

    _add_variable(comp, "fetal_weight_g", units="dimensionless", initial_value="3500")
    for p in (a, b):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "placental_weight_g", units="dimensionless", initial_value="0")

    a_id = parameter_id_to_sbml(a.id)
    b_id = parameter_id_to_sbml(b.id)
    rhs = _apply("times", _ci(a_id), _apply("power", _ci("fetal_weight_g"), _ci(b_id)))
    comp.setMath(_mathml(_apply_assign("placental_weight_g", rhs)))
    return model


def _build_ua_pi(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "umbilical_artery_pi_trajectory",
        baseline_pid="fetal_circulation.ua_pi_baseline",
        term_pid="fetal_circulation.ua_pi_term",
        output_name="UA_PI_t",
        growth_rate=0.18,
        midpoint_week=28.0,
    )


def _build_mca_pi(ds: Dataset) -> libcellml.Model:
    """Gaussian-bump MCA-PI."""
    sm = next(s for s in SUBMODELS if s.id == "mca_pi_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    baseline = ds["fetal_circulation.mca_pi_baseline"]
    peak = ds["fetal_circulation.mca_pi_peak"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "peak_week", units="dimensionless", initial_value="28")
    _add_variable(comp, "spread_weeks", units="dimensionless", initial_value="8")
    for p in (baseline, peak):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "MCA_PI_t", units="dimensionless", initial_value="0")

    b_id = parameter_id_to_sbml(baseline.id)
    p_id = parameter_id_to_sbml(peak.id)
    z = _apply(
        "divide",
        _apply("minus", _ci("t_weeks"), _ci("peak_week")),
        _ci("spread_weeks"),
    )
    bump = _apply(
        "times",
        _apply("minus", _ci(p_id), _ci(b_id)),
        _apply(
            "exp",
            _apply("divide", _apply("minus", _apply("power", z, _cn("2"))), _cn("2")),
        ),
    )
    rhs = _apply("plus", _ci(b_id), bump)
    comp.setMath(_mathml(_apply_assign("MCA_PI_t", rhs)))
    return model


def _build_cpr(ds: Dataset) -> libcellml.Model:
    """CPR(t) = MCA-PI(t) / UA-PI(t)."""
    sm = next(s for s in SUBMODELS if s.id == "cerebroplacental_ratio")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    ua_b = ds["fetal_circulation.ua_pi_baseline"]
    ua_t = ds["fetal_circulation.ua_pi_term"]
    mca_b = ds["fetal_circulation.mca_pi_baseline"]
    mca_p = ds["fetal_circulation.mca_pi_peak"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "ua_growth_rate", units="dimensionless", initial_value="0.18")
    _add_variable(comp, "ua_midpoint", units="dimensionless", initial_value="28")
    _add_variable(comp, "mca_peak_week", units="dimensionless", initial_value="28")
    _add_variable(comp, "mca_spread_weeks", units="dimensionless", initial_value="8")
    for p in (ua_b, ua_t, mca_b, mca_p):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "CPR_t", units="dimensionless", initial_value="0")

    ua_b_id = parameter_id_to_sbml(ua_b.id)
    ua_t_id = parameter_id_to_sbml(ua_t.id)
    mca_b_id = parameter_id_to_sbml(mca_b.id)
    mca_p_id = parameter_id_to_sbml(mca_p.id)

    ua_expr = _sigmoid_baseline_term(ua_b_id, ua_t_id)
    # Replace growth_rate_per_week / midpoint_week with ua-specific names.
    ua_expr = ua_expr.replace("growth_rate_per_week", "ua_growth_rate").replace(
        "midpoint_week", "ua_midpoint"
    )

    z = _apply(
        "divide",
        _apply("minus", _ci("t_weeks"), _ci("mca_peak_week")),
        _ci("mca_spread_weeks"),
    )
    bump = _apply(
        "times",
        _apply("minus", _ci(mca_p_id), _ci(mca_b_id)),
        _apply(
            "exp",
            _apply("divide", _apply("minus", _apply("power", z, _cn("2"))), _cn("2")),
        ),
    )
    mca_expr = _apply("plus", _ci(mca_b_id), bump)

    rhs = _apply("divide", mca_expr, ua_expr)
    comp.setMath(_mathml(_apply_assign("CPR_t", rhs)))
    return model


def _build_estradiol(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "estradiol_trajectory",
        baseline_pid="placental_endocrine.estradiol_baseline_ng_per_ml",
        term_pid="placental_endocrine.estradiol_term_ng_per_ml",
        output_name="estradiol_t",
        growth_rate=0.15,
        midpoint_week=24.0,
    )


def _build_fhr(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "fetal_heart_rate_trajectory",
        baseline_pid="fetal_circulation.fhr_baseline_bpm",
        term_pid="fetal_circulation.fhr_term_bpm",
        output_name="FHR_t",
        growth_rate=0.2,
        midpoint_week=18.0,
    )


def _build_hcg(ds: Dataset) -> libcellml.Model:
    """Piecewise hCG: quadratic rise from 0 to peak, then exponential decline."""
    import math

    sm = next(s for s in SUBMODELS if s.id == "hcg_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    peak = ds["placental_endocrine.hcg_peak_miu_per_ml"]
    peak_week = ds["placental_endocrine.hcg_peak_week"]
    term = ds["placental_endocrine.hcg_term_miu_per_ml"]
    term_week = 40.0
    decay_rate = -math.log(term.value.central / peak.value.central) / (
        term_week - peak_week.value.central
    )

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "term_week", units="dimensionless", initial_value=str(term_week))
    _add_variable(comp, "decay_rate_per_week", units="dimensionless", initial_value=str(decay_rate))
    for p in (peak, peak_week, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "hCG_t", units="dimensionless", initial_value="0")

    peak_id = parameter_id_to_sbml(peak.id)
    pw_id = parameter_id_to_sbml(peak_week.id)
    # rise = peak * (t/pw)^2
    rise = _apply(
        "times",
        _ci(peak_id),
        _apply("power", _apply("divide", _ci("t_weeks"), _ci(pw_id)), _cn("2")),
    )
    # decline = peak * exp(-decay * (t - pw))
    decline = _apply(
        "times",
        _ci(peak_id),
        _apply(
            "exp",
            _apply(
                "minus",
                _apply(
                    "times",
                    _ci("decay_rate_per_week"),
                    _apply("minus", _ci("t_weeks"), _ci(pw_id)),
                ),
            ),
        ),
    )
    cond = f"<apply>\n<lt/>\n<ci>t_weeks</ci>\n<ci>{pw_id}</ci>\n</apply>"
    rhs = (
        "<piecewise>\n"
        f"<piece>\n{rise}\n{cond}\n</piece>\n"
        f"<otherwise>\n{decline}\n</otherwise>\n"
        "</piecewise>"
    )
    comp.setMath(_mathml(_apply_assign("hCG_t", rhs)))
    return model


def _build_homa_ir(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "homa_ir_trajectory",
        baseline_pid="maternal_endocrine.homa_ir_baseline",
        term_pid="maternal_endocrine.homa_ir_term",
        output_name="HOMA_t",
        growth_rate=0.2,
        midpoint_week=22.0,
    )


def _build_cortisol(ds: Dataset) -> libcellml.Model:
    return _build_sigmoid_baseline_term(
        ds,
        "cortisol_trajectory",
        baseline_pid="maternal_endocrine.cortisol_baseline_ug_per_dl",
        term_pid="maternal_endocrine.cortisol_term_ug_per_dl",
        output_name="cortisol_t",
        growth_rate=0.15,
        midpoint_week=22.0,
    )


def _build_tsh_trajectory(ds: Dataset) -> libcellml.Model:
    """Piecewise-linear TSH (constant nadir before t1_week, then linear)."""
    sm = next(s for s in SUBMODELS if s.id == "tsh_trajectory")
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    t1 = ds["maternal_endocrine.tsh_t1_miu_per_l"]
    term = ds["maternal_endocrine.tsh_term_miu_per_l"]

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    _add_variable(comp, "t1_week", units="dimensionless", initial_value="12")
    _add_variable(comp, "term_week", units="dimensionless", initial_value="40")
    for p in (t1, term):
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "TSH_t", units="dimensionless", initial_value="0")

    t1_id = parameter_id_to_sbml(t1.id)
    term_id = parameter_id_to_sbml(term.id)
    # Linear segment: t1 + (term - t1) * (t - t1_week) / (term_week - t1_week)
    linear = _apply(
        "plus",
        _ci(t1_id),
        _apply(
            "divide",
            _apply(
                "times",
                _apply("minus", _ci(term_id), _ci(t1_id)),
                _apply("minus", _ci("t_weeks"), _ci("t1_week")),
            ),
            _apply("minus", _ci("term_week"), _ci("t1_week")),
        ),
    )
    # MathML piecewise: <piecewise><piece>{value}{cond}</piece>
    # <otherwise>{else}</otherwise></piecewise>
    cond = "<apply>\n<lt/>\n<ci>t_weeks</ci>\n<ci>t1_week</ci>\n</apply>"
    rhs = (
        "<piecewise>\n"
        f"<piece>\n{_ci(t1_id)}\n{cond}\n</piece>\n"
        f"<otherwise>\n{linear}\n</otherwise>\n"
        "</piecewise>"
    )
    comp.setMath(_mathml(_apply_assign("TSH_t", rhs)))
    return model


def _build_hadlock_biometry_growth(
    ds: Dataset, sm_id: str, output_name: str, biometry_prefix: str
) -> libcellml.Model:
    """Cubic-fit biometry growth CellML model."""
    from nidus.export.reference import (
        HADLOCK_ANCHOR_WEEKS,
        hadlock_biometry_cubic_coefficients,
    )

    sm = next(s for s in SUBMODELS if s.id == sm_id)
    model = libcellml.Model()
    model.setName(sm.id)
    _ensure_units(model)

    comp = libcellml.Component()
    comp.setName(sm.id)
    model.addComponent(comp)

    anchors = [ds[f"fetal_growth.{biometry_prefix}_{w}w_mm"] for w in HADLOCK_ANCHOR_WEEKS]
    a3, a2, a1, a0 = hadlock_biometry_cubic_coefficients([p.value.central for p in anchors])

    _add_variable(comp, "t_weeks", units="dimensionless", initial_value="20")
    for p in anchors:
        _add_variable(
            comp,
            parameter_id_to_sbml(p.id),
            units="dimensionless",
            initial_value=str(p.value.central),
        )
    _add_variable(comp, "fit_a3", units="dimensionless", initial_value=str(a3))
    _add_variable(comp, "fit_a2", units="dimensionless", initial_value=str(a2))
    _add_variable(comp, "fit_a1", units="dimensionless", initial_value=str(a1))
    _add_variable(comp, "fit_a0", units="dimensionless", initial_value=str(a0))
    _add_variable(comp, output_name, units="dimensionless", initial_value="0")

    # a3*t^3 + a2*t^2 + a1*t + a0
    rhs = _apply(
        "plus",
        _apply("times", _ci("fit_a3"), _apply("power", _ci("t_weeks"), _cn("3"))),
        _apply("times", _ci("fit_a2"), _apply("power", _ci("t_weeks"), _cn("2"))),
        _apply("times", _ci("fit_a1"), _ci("t_weeks")),
        _ci("fit_a0"),
    )
    comp.setMath(_mathml(_apply_assign(output_name, rhs)))
    return model


def _build_hadlock_bpd_growth(ds: Dataset) -> libcellml.Model:
    return _build_hadlock_biometry_growth(ds, "hadlock_bpd_growth", "BPD_t_mm", "bpd")


def _build_hadlock_hc_growth(ds: Dataset) -> libcellml.Model:
    return _build_hadlock_biometry_growth(ds, "hadlock_hc_growth", "HC_t_mm", "hc")


def _build_hadlock_ac_growth(ds: Dataset) -> libcellml.Model:
    return _build_hadlock_biometry_growth(ds, "hadlock_ac_growth", "AC_t_mm", "ac")


def _build_hadlock_fl_growth(ds: Dataset) -> libcellml.Model:
    return _build_hadlock_biometry_growth(ds, "hadlock_fl_growth", "FL_t_mm", "fl")


# ---- Public API ----------------------------------------------------

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
    "placental_fetal_allometry": _build_placental_fetal_allometry,
    "maternal_fetal_igg_transfer": _build_igg_transfer,
    "placental_cortisol_gradient": _build_placental_cortisol_gradient,
    "maternal_microchimerism_trajectory": _build_maternal_microchimerism,
    "fetal_pulmonary_fluid_trajectory": _build_fetal_pulmonary_fluid,
    "umbilical_artery_pi_trajectory": _build_ua_pi,
    "mca_pi_trajectory": _build_mca_pi,
    "cerebroplacental_ratio": _build_cpr,
    "hadlock_bpd_growth": _build_hadlock_bpd_growth,
    "hadlock_hc_growth": _build_hadlock_hc_growth,
    "hadlock_ac_growth": _build_hadlock_ac_growth,
    "hadlock_fl_growth": _build_hadlock_fl_growth,
}


def build_cellml(ds: Dataset, submodel_id: str, *, version: str = "2.0") -> str:
    """Return the CellML XML for one submodel as a string.

    Args:
        ds: loaded nidus dataset
        submodel_id: registry id
        version: '2.0' (default) or '1.1' (fallback for legacy
            toolchains that haven't moved to 2.0).
    """
    if submodel_id not in _BUILDERS:
        raise KeyError(f"Unknown submodel {submodel_id!r}. Available: {sorted(_BUILDERS)}")
    model = _BUILDERS[submodel_id](ds)
    printer = libcellml.Printer()
    xml: str = printer.printModel(model)

    if version == "1.1":
        # Down-convert: CellML 2.0 namespace -> 1.1 namespace.
        # The mathematical content + variable definitions are
        # compatible at this level; only the root namespace differs.
        xml = xml.replace(
            "http://www.cellml.org/cellml/2.0#",
            "http://www.cellml.org/cellml/1.1#",
        )

    return xml


def write_cellml(ds: Dataset, output_dir: str | Path, *, version: str = "2.0") -> list[Path]:
    """Write all CellML submodels to a directory. Returns the file paths."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for sm in SUBMODELS:
        if sm.id not in _BUILDERS:
            continue
        xml = build_cellml(ds, sm.id, version=version)
        suffix = ".cellml" if version == "2.0" else ".cellml1.cellml"
        path = out_dir / f"{sm.id}{suffix}"
        path.write_text(xml, encoding="utf-8")
        written.append(path)
    return written
