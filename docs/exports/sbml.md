# SBML export

Every mechanistic submodel ships as an [SBML L3v2](https://sbml.org/)
document. A top-level **composed pregnancy model** (`nidus_pregnancy_composed`)
wires every submodel through a shared gestational-time axis.

## What you get

```bash
nidus export --format sbml --output exports/sbml/
```

produces one `.xml` file per submodel plus the composed model:

```
exports/sbml/
├── amniotic_fluid_volume_trajectory.xml
├── arterial_ph_trajectory.xml
├── cerebroplacental_ratio.xml
├── cortisol_trajectory.xml
├── ...
├── nidus_pregnancy_composed.xml    ← top-level composition
└── uterine_artery_flow_logistic.xml
```

All 41 files pass `libsbml.SBMLDocument.checkConsistency()` with zero
errors (warnings tracked but non-blocking).

## Modelling conventions

- **Time axis.** Every time-trajectory submodel uses `t_weeks` (gestational
  age in weeks) as the independent variable. Algebraic submodels
  (Severinghaus O₂-Hb, Michaelis–Menten glucose) use the natural domain
  variable instead — `po2_mmhg`, `substrate_mmol_per_l`, etc.
- **Assignment rules.** Each submodel's primary observable is computed
  by an `<assignmentRule>` rather than a kinetic law, so libSBML, COPASI,
  and tellurium can all evaluate it without an ODE solver where one
  isn't warranted.
- **Units.** `unitDefinition` blocks are emitted for every value with
  explicit units in the dataset (mmHg, mL/min, μg/dL, …).
- **SBO terms.** Each submodel carries the matching Systems Biology
  Ontology accession (`SBO:0000295` logistic, `SBO:0000028`
  Michaelis–Menten, `SBO:0000192` Hill, …) so downstream tools can
  recognise the kinetic form.

## Composed pregnancy model

`nidus_pregnancy_composed.xml` is a single SBML document that imports
every submodel and links them where the literature establishes a
coupling. Couplings are annotated with `nidus:couplingType`:

- `"mechanistic"` — direct causal mechanism in the literature.
- `"empirical"` — co-varies through gestation without a direct mechanism.
- `"sequential"` — one variable feeds another, no feedback loop.

`nidus:couplingNotes` carries prose justification for every non-trivial
edge. The top-level model is tier C by tier-propagation; users are
expected to fork and adjust if they disagree with a coupling.

## Validation

```python
import libsbml
reader = libsbml.SBMLReader()
doc = reader.readSBMLFromFile("exports/sbml/placental_glucose_glut1.xml")
assert doc.getNumErrors() == 0
errors = doc.checkConsistency()
print(f"{errors} consistency issues")
```

The test suite (`test_export_sbml.py`, `test_export_composed.py`)
runs this assertion across every submodel on every push.

## Round-trip against the reference kernels

Each algebraic submodel ships a pure-NumPy reference implementation
under `nidus.export.reference`. When `tellurium` is installed, the
test suite loads the exported SBML, simulates it, and compares against
the reference kernel:

- 1e-6 relative error for algebraic submodels
- 1e-4 relative error for ODE submodels

The reference kernels are *not* a separate simulator — they exist
solely to detect export errors.

## BioModels submission

The COMBINE archive emitted by `nidus export --format omex` is the
intended submission unit. Submit at
<https://www.ebi.ac.uk/biomodels/submit>; expect 4–8 weeks of curator
review before a `BIOMD0000000XXX` accession lands. See [the spec](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.4/01-mechanistic-modeling-interop.md#8-submission-workflow)
for the full submission workflow.

## Companion SED-ML

For every time-trajectory submodel, `nidus.export.build_sedml` emits a
SED-ML L1V4 `<uniformTimeCourse>` (0–40 weeks, 400 sample points,
CVODE) over the SBML's primary observable. These ship inside the
COMBINE archive under `sedml/<submodel>.sedml`, so a downstream tool
can run the canonical simulation experiment without authoring one.

Algebraic submodels parametrised by PO₂ / substrate / etc. are
deliberately skipped — a UniformTimeCourse is the wrong shape for
them.
