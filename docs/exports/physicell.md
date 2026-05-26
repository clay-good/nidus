# PhysioCell export

[PhysioCell](http://physicell.org/) consumes parameters via two XML
files in its config tree. The natural surface for nidus is the
`<user_parameters>` block in `PhysiCell_settings.xml` — scalar values
a PhysioCell-based pregnancy-tissue model would consume directly.

## What you get

```bash
nidus export --format physiocell --output exports/physiocell/
```

produces a single drop-in file:

```
exports/physiocell/
└── nidus-parameters.xml
```

Every nidus parameter appears inside a `<user_parameters>` block, one
element per parameter, with the dotted dataset id flattened to a
PhysiCell-friendly `<subsystem>__<name>` element name:

```xml
<user_parameters>
    <!-- placental_glucose -->
    <placental_glucose__glucose_glut1_km_mmol_per_l
        type="double"
        units="mmol/L"
        description="GLUT1 Michaelis constant; tier=B; review_status=verified; doi=10.1016/...; citation_key=illsley-2000-placental-glucose-transporters"
    >17.0</placental_glucose__glucose_glut1_km_mmol_per_l>
    <!-- ... -->
</user_parameters>
```

The `description` attribute carries the **confidence tier, review
status, primary DOI, and citation key** for every parameter — so
PhysiCell reviewers (and future-you) can trace any value straight back
to the dataset and the cited paper.

## How to wire it into a project

`PhysiCell_settings.xml` `<include>`s `nidus-parameters.xml` by
convention. When a citation is challenged, the workflow is:

1. Update the dataset parameter (with a new `extraction.review_status`
   entry if needed).
2. Re-run `nidus export --format physiocell --output ...`.
3. Re-run the simulation.

No archaeology, no hardcoded constants drifting away from the cited
source.

## Worked example

A real multicellular tissue example ships under
[`docs/examples/physicell_placental_villous/`](https://github.com/clay-good/nidus/tree/main/docs/examples/physicell_placental_villous):
a 2D placental-villous slice with BioFVM diffusion, syncytiotrophoblast
cells running GLUT1/GLUT3 Michaelis–Menten kinetics, and every input
sourced from `nidus-parameters.xml`. The example's `README.md` walks
through building and running it.

See the [tutorial notebook](https://github.com/clay-good/nidus/blob/main/docs/examples/physicell_placental_villous/tutorial.ipynb)
for an end-to-end walkthrough including an IUGR sensitivity scenario.

## Distribution

PhysioCell does not have a central model repository. Nidus reaches the
community via:

- the [PhysioCell GitHub Discussions](https://github.com/MathCancer/PhysiCell/discussions),
- the PhysioCell community Slack (the `#physicell-help` channel),
- a PR to [`MathCancer/PhysiCell-tutorials`](https://github.com/MathCancer/PhysiCell-tutorials)
  adding the worked example,
- the v0.4 outreach essay.

## Validation

`test_export_physiocell.py` asserts:

- the emitted XML parses,
- every nidus parameter appears in the export (no silent drops),
- units and citation keys are preserved on every `<param>` entry,
- the example project's `PhysiCell_settings.xml` parses and references
  the right `user_parameters` keys.
