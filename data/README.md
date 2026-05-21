# Parameter Database and Citation Index

This directory holds the structured data the simulator depends on:
every numerical parameter, and the bibliographic citation that backs it.
See [SPEC.md §9](../SPEC.md) for the design rationale and
[CONTRIBUTING.md](../CONTRIBUTING.md) for the contribution workflow.

## Layout

```
data/
├── parameters/
│   ├── maternal/      *.toml files of maternal subsystem parameters
│   ├── placenta/      *.toml files of placental interface parameters
│   └── fetal/         *.toml files of fetal subsystem parameters
└── citations/         *.toml files of bibliographic records
```

The loader (`nidus-data::ParameterDatabase`) accepts any number of
parameter and citation files; it merges them, rejects duplicate ids,
and confirms that every parameter's `citation` field resolves to an
entry in the citation index.

## Schema, by example

A parameter entry:

```toml
[[parameter]]
id = "maternal-hemoglobin-mean-term"   # stable, kebab-case
name = "Maternal hemoglobin concentration (mean, near term)"
description = "Mean maternal hemoglobin concentration in third-trimester pregnancy."
tier = "B"                              # A, B, C, or D
unit = "g/L"
value = { kind = "point", value = 110.0, uncertainty = 8.0 }
citation = "citation-id-from-the-index"
population = "Description of the cohort the value was measured in"
age_range = { min_weeks = 28, max_weeks = 40 }
technique = "Capillary blood, automated hematology analyzer"
caveats = "Threshold definitions vary by source."
```

A citation entry:

```toml
[[citation]]
id = "citation-id-from-the-index"
authors = "Lastname F, Lastname G"
title = "Title of the work"
venue = "Journal Name"
year = 2020
doi = "10.1000/example"        # optional
pmid = "12345678"              # optional
notes = "Anything else useful" # optional
```

The four allowed `value` shapes are `point` (with optional
`uncertainty`), `uniform { low, high }`, `normal { mean, sd }`, and
`lognormal { mu, sigma }`. Unknown fields are rejected so that typos do
not silently pass review.

## Citation policy

Per CONTRIBUTING.md, contributors are expected to cite parameters from
sources they have personally consulted. The review process for
parameter pull requests verifies citations against their originals;
citations that cannot be verified will not be merged.

The data files in this directory are tracked as part of the repository.
Authoring the initial Tier A parameter set (maternal blood properties,
O₂–Hb dissociation constants, placental gas diffusion coefficients, and
GLUT1/GLUT3 glucose transporter kinetics) is the human-contributor
half of Prompt 5 in SPEC.md §13: the loader and schema are in place,
and a working example file (`citations/index.toml` and one parameter
file) is provided so contributors can immediately see the pattern.
