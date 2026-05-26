# CellML export

Every mechanistic submodel ships as a [CellML 2.0](https://www.cellml.org/)
document, with a CellML 1.1 fallback emitted alongside for toolchains
that haven't moved off the legacy format (notably some legacy
OpenCOR setups and a number of historical Physiome Model Repository
entries).

## What you get

```bash
nidus export --format cellml --output exports/cellml/                  # CellML 2.0
nidus export --format cellml --output exports/cellml-1.1/ --cellml-version 1.1
```

produces one `.cellml` file per submodel:

```
exports/cellml/
├── amniotic_fluid_volume_trajectory.cellml
├── ...
└── uterine_artery_flow_logistic.cellml
```

Every file passes `libcellml.Validator.validateModel()` with zero
issues. The 1.1 variant is generated from the same source by switching
the libcellml `Printer` version flag, so the two stay byte-equivalent
at the modelling layer; the maintenance cost is bounded.

## Modelling conventions

- **Components.** CellML's component model maps cleanly onto nidus
  submodels: every submodel becomes one component whose variables
  expose the parameters (`baseline_value`, `peak_excess`, etc.) and
  the primary observable.
- **MathML.** Equations are emitted as Content MathML, so OpenCOR /
  libcellml / Cardiac Electrophysiology Web Lab can all consume them
  directly.
- **Annotations.** MIRIAM RDF (`bqbiol:isDescribedBy`) and nidus
  predicates ride on `cmeta:id`-targeted RDF blocks per CellML
  convention; see the [annotation reference](annotations.md).

## Validation

```python
import libcellml
parser = libcellml.Parser()
with open("exports/cellml/placental_glucose_glut1.cellml") as fh:
    model = parser.parseModel(fh.read())

validator = libcellml.Validator()
validator.validateModel(model)
assert validator.issueCount() == 0
```

The test suite (`test_export_cellml.py`) runs this assertion across
every submodel and both CellML versions on every push.

## Physiome Model Repository submission

The Physiome workflow uses Mercurial:

```bash
hg clone https://models.physiomeproject.org/workspace/<new-workspace>
cp exports/cellml/*.cellml exports/cellml-1.1/*.cellml <workspace>/
cd <workspace>
hg commit -m "Initial nidus v0.4 deposit"
hg push
```

The workspace becomes immediately citable via its persistent URL.
Promotion to an "exposure" (curated, versioned view) is optional polish
and runs on the curator's timeline.

See [the spec](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.4/01-mechanistic-modeling-interop.md#8-submission-workflow)
for the full workflow.

## Round-trip against the reference kernels

When a CellML simulator (e.g. OpenCOR's command-line build, or
`libcellml`'s analyser + interpreter) is available, the test suite
loads the exported model, evaluates it on the canonical sample grid,
and compares against the pure-NumPy reference kernel under
`nidus.export.reference`. Tolerances mirror [the SBML case](sbml.md#round-trip-against-the-reference-kernels).
