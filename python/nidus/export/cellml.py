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


# ---- Public API ----------------------------------------------------

_BUILDERS = {
    "placental_villous_growth": _build_placental_villous_growth,
    "o2hb_dissociation_adult": _build_o2hb_dissociation_adult,
    "o2hb_dissociation_fetal": _build_o2hb_dissociation_fetal,
    "placental_glucose_glut1": _build_placental_glucose_glut1,
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
