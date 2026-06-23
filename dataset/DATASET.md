# Nidus Dataset

A curated, citation-backed, confidence-tier-annotated dataset of human
gestational physiology parameters covering maternal cardiovascular
adaptation, placental transport, and fetal development from 8 to 40
weeks gestation.

## Layout

```
dataset/
├── parameters/        # one JSON file per subsystem (13 subsystems, 243 parameters)
├── citations/         # citation index (citations.json, 66 records)
├── tiers/             # tier definitions
│   └── tiers.json
├── schema/            # JSON Schema (draft 2020-12)
│   ├── parameter.schema.json
│   ├── citation.schema.json
│   └── tier.schema.json
├── jsonld/            # JSON-LD context + ontology
│   └── context.jsonld
├── DATASET.md         # this file
└── CHANGELOG.md       # dataset semver, independent of code
```

## Schema

Every parameter is validated against `schema/parameter.schema.json`.
Every citation against `schema/citation.schema.json`. The tier
definitions in `tiers/tiers.json` are validated against
`schema/tier.schema.json`.

Schema validation runs in CI on every change.

## Confidence tiers

| Tier | Meaning                                                              |
| ---- | -------------------------------------------------------------------- |
| A    | Well-established. 3+ independent studies, overlapping CIs.           |
| B    | Supported. 1–2 longitudinal studies (n≥100).                         |
| C    | Provisional. Single study, or small n, or cross-sectional.           |
| D    | Unknown. Hypothesised; no quantitative literature.                    |

See [`tiers/tiers.json`](tiers/tiers.json) for machine-readable
criteria.

## Versioning

The dataset uses its own semantic version, tracked in
[`CHANGELOG.md`](CHANGELOG.md). It is independent of code versioning.
Each release is deposited on Zenodo with a permanent DOI.

## Citation

Cite the Zenodo concept DOI (resolves to the latest version). See
`../CITATION.cff` at the repository root.

## Licence

CC-BY-4.0. See `../LICENSE-DATASET`.
