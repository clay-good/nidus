"""SED-ML simulation-descriptor generation.

Each time-trajectory nidus submodel exports a SED-ML L1V4 document
that says, in the standard format the systems-biology tooling
already understands, *how to simulate that SBML model* —
specifically: integrate from 0 to 40 weeks at 400 evenly-spaced
sample points, report time and the primary observable.

Spec 03 §5 cross-cutting infrastructure item. The SED-ML descriptors
land in the COMBINE archive alongside the SBML / CellML / PhysioCell
exports so that downstream tools (tellurium, COPASI, etc.) can open
the archive and run a canonical simulation experiment without the
user having to author one.

Algebraic submodels whose independent variable is not time (e.g.
the Severinghaus oxygen-Hb dissociation, parameterised by PO2 rather
than gestational age) do not get a SED-ML — a UniformTimeCourse
descriptor is the wrong shape for them.
"""

from __future__ import annotations

import re
from pathlib import Path

from nidus.export.registry import SUBMODELS, Submodel
from nidus.export.sbml import build_sbml
from nidus.load import Dataset

SEDML_NS = "http://sed-ml.org/sed-ml/level1/version4"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"
# KISAO:0000019 = CVODE; the conventional default integrator for stiff/non-stiff ODEs.
DEFAULT_ALGORITHM_KISAO = "KISAO:0000019"

# Time domain — the gestational axis used everywhere in nidus.
DEFAULT_OUTPUT_START_WEEKS = 0.0
DEFAULT_OUTPUT_END_WEEKS = 40.0
DEFAULT_NUMBER_OF_POINTS = 400


def _primary_observable(sbml_xml: str) -> str | None:
    """Return the id of the first assignmentRule target in the SBML.

    Nidus per-submodel SBMLs always assign their main observable via
    an assignmentRule (the trajectory equation evaluated at t). The
    first assignmentRule target is therefore the variable the SED-ML
    report should expose.
    """
    match = re.search(r'<assignmentRule[^>]+variable="([^"]+)"', sbml_xml)
    return match.group(1) if match else None


def build_sedml(
    ds: Dataset,
    submodel_id: str,
    *,
    sbml_filename: str | None = None,
    output_start_weeks: float = DEFAULT_OUTPUT_START_WEEKS,
    output_end_weeks: float = DEFAULT_OUTPUT_END_WEEKS,
    number_of_points: int = DEFAULT_NUMBER_OF_POINTS,
) -> str | None:
    """Build a SED-ML L1V4 descriptor for one time-trajectory submodel.

    Returns ``None`` if the submodel's independent variable is not
    ``"t_weeks"`` — a UniformTimeCourse is the wrong shape for
    algebraic submodels parametrised by PO2, substrate, etc.

    ``sbml_filename`` is the relative path the SED-ML's ``model``
    element should reference; defaults to ``"{submodel_id}.xml"``.
    """
    sm = next((s for s in SUBMODELS if s.id == submodel_id), None)
    if sm is None:
        raise KeyError(f"Unknown submodel {submodel_id!r}")
    if sm.independent_variable != "t_weeks":
        return None

    sbml_xml = build_sbml(ds, submodel_id)
    observable = _primary_observable(sbml_xml)
    if observable is None:
        return None

    src = sbml_filename if sbml_filename is not None else f"{submodel_id}.xml"
    sm_id_safe = _safe_id(submodel_id)
    obs_id_safe = _safe_id(observable)

    return _render_sedml(
        sm_id_safe=sm_id_safe,
        obs_id_safe=obs_id_safe,
        observable=observable,
        sbml_source=src,
        submodel=sm,
        output_start=output_start_weeks,
        output_end=output_end_weeks,
        number_of_points=number_of_points,
    )


def _safe_id(raw: str) -> str:
    """Map an arbitrary id to a SED-ML XML-id-safe form (alnum + underscore)."""
    return re.sub(r"[^A-Za-z0-9_]", "_", raw)


def _xpath_target(parameter_id: str) -> str:
    """XPath into an SBML L3 document selecting a top-level parameter by id."""
    return f"/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='{parameter_id}']"


def _render_sedml(
    *,
    sm_id_safe: str,
    obs_id_safe: str,
    observable: str,
    sbml_source: str,
    submodel: Submodel,
    output_start: float,
    output_end: float,
    number_of_points: int,
) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<sedML xmlns="{SEDML_NS}" level="1" version="4">\n'
        f"  <!-- {submodel.name} -->\n"
        "  <listOfModels>\n"
        f'    <model id="model_{sm_id_safe}" '
        'language="urn:sedml:language:sbml.level-3.version-2" '
        f'source="{sbml_source}"/>\n'
        "  </listOfModels>\n"
        "  <listOfSimulations>\n"
        f'    <uniformTimeCourse id="sim_{sm_id_safe}" '
        f'initialTime="{output_start}" outputStartTime="{output_start}" '
        f'outputEndTime="{output_end}" numberOfPoints="{number_of_points}">\n'
        f'      <algorithm kisaoID="{DEFAULT_ALGORITHM_KISAO}"/>\n'
        "    </uniformTimeCourse>\n"
        "  </listOfSimulations>\n"
        "  <listOfTasks>\n"
        f'    <task id="task_{sm_id_safe}" '
        f'modelReference="model_{sm_id_safe}" '
        f'simulationReference="sim_{sm_id_safe}"/>\n'
        "  </listOfTasks>\n"
        "  <listOfDataGenerators>\n"
        '    <dataGenerator id="dg_time">\n'
        "      <listOfVariables>\n"
        '        <variable id="var_time" '
        'symbol="urn:sedml:symbol:time" '
        f'taskReference="task_{sm_id_safe}"/>\n'
        "      </listOfVariables>\n"
        f'      <math xmlns="{MATHML_NS}"><ci>var_time</ci></math>\n'
        "    </dataGenerator>\n"
        f'    <dataGenerator id="dg_{obs_id_safe}">\n'
        "      <listOfVariables>\n"
        f'        <variable id="var_{obs_id_safe}" '
        f'target="{_xpath_target(observable)}" '
        f'taskReference="task_{sm_id_safe}"/>\n'
        "      </listOfVariables>\n"
        f'      <math xmlns="{MATHML_NS}"><ci>var_{obs_id_safe}</ci></math>\n'
        "    </dataGenerator>\n"
        "  </listOfDataGenerators>\n"
        "  <listOfOutputs>\n"
        f'    <report id="report_{sm_id_safe}" name="{submodel.name}">\n'
        "      <listOfDataSets>\n"
        '        <dataSet id="ds_time" label="time_weeks" dataReference="dg_time"/>\n'
        f'        <dataSet id="ds_{obs_id_safe}" label="{observable}" '
        f'dataReference="dg_{obs_id_safe}"/>\n'
        "      </listOfDataSets>\n"
        "    </report>\n"
        "  </listOfOutputs>\n"
        "</sedML>\n"
    )


def write_sedml(ds: Dataset, output_dir: str | Path) -> list[Path]:
    """Write one ``.sedml`` per time-trajectory submodel.

    Algebraic submodels (e.g. ``o2hb_dissociation_adult``) are
    silently skipped because a UniformTimeCourse SED-ML is the wrong
    shape for them.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for sm in SUBMODELS:
        sedml = build_sedml(ds, sm.id)
        if sedml is None:
            continue
        path = out_dir / f"{sm.id}.sedml"
        path.write_text(sedml)
        written.append(path)
    return written
