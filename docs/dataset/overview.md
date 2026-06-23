# Dataset overview

The nidus dataset lives in [`dataset/`](https://github.com/clay-good/nidus/tree/main/dataset) at the repository root and is bundled into the Python wheel under `nidus/_dataset/` so `nidus.load()` resolves it automatically.

## Layout

```
dataset/
├── parameters/
│   ├── maternal_cardiovascular.json   (14 entries)
│   ├── maternal_blood.json            ( 9)
│   ├── maternal_respiratory.json      ( 5)
│   ├── maternal_renal.json            ( 3)
│   ├── placental_structure.json       ( 5)
│   ├── placental_gas_exchange.json    ( 2)
│   ├── placental_glucose.json         ( 4)
│   ├── fetal_circulation.json         ( 3)
│   ├── fetal_growth.json              ( 7)
│   └── fetal_metabolism.json          ( 2)
├── citations/
│   └── citations.json                 (32 entries)
├── tiers/
│   └── tiers.json
├── schema/
│   ├── parameter.schema.json
│   ├── citation.schema.json
│   └── tier.schema.json
├── jsonld/
│   └── context.jsonld
├── DATASET.md
└── CHANGELOG.md
```

**Total:** 243 parameters across 13 subsystems, 66 citations.

## Versioning

The dataset has its own [semantic version](https://semver.org/), tracked in `dataset/CHANGELOG.md`, independent of the code/package version. Every GitHub release deposits a snapshot to Zenodo with a permanent DOI. The Zenodo *concept* DOI resolves to the latest version; *version* DOIs are stable across releases.

## FAIR compliance

- **Findable** — Zenodo DOI, indexed in [Re3data](https://www.re3data.org/) once first release lands.
- **Accessible** — Open via Zenodo, GitHub, and PyPI. No registration. No paywalled fallback for "premium" data; everything is in the repo.
- **Interoperable** — JSON Schema (draft 2020-12) on the structure; [JSON-LD context](https://github.com/clay-good/nidus/blob/main/dataset/jsonld/context.jsonld) maps the records to [schema.org](https://schema.org/) and [identifiers.org](https://identifiers.org/) URIs.
- **Reusable** — CC-BY-4.0 licence on the dataset; MIT on the tooling. Every parameter carries provenance.

See the [schema reference](schema.md) for the field-level details.

## How the dataset was assembled

The dataset's first parameters were migrated from a curated TOML corpus in the project's earlier (Rust prototype) phase — the migration is captured in [`scripts/migrate_data.py`](https://github.com/clay-good/nidus/blob/main/scripts/migrate_data.py) — and it has since grown to 243 parameters.

28 entries are marked `extraction.review_status: "verified"` (a human has read the source PDF and confirmed the dataset entry); 1 is `contested`; the rest are `unverified` — the central value is drawn from the literature, but no formal re-verification against the original paper has happened yet. Walking every Tier A/B record and promoting it to `verified` is the highest-leverage contribution available between now and a future release.
