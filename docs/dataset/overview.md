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

Records carry an `extraction.review_status`: **28** are `verified` (a human read the source PDF and confirmed the entry); **127** are `pending_human_review` (automated review located the stored value in a real source and attached a verbatim supporting quote in `extraction.source_check`, but no human has signed off); **1** is `contested`; the remaining **87** are `unverified` (illustrative central value drawn from the literature, source not yet confirmed). Automated review never sets `verified` — that stays a human action. Walking the `pending_human_review` and Tier A/B `unverified` records and confirming them against the source (start from [`data/validation/REVIEW_QUEUE.md`](https://github.com/clay-good/nidus/blob/main/data/validation/REVIEW_QUEUE.md)) is the highest-leverage contribution available between now and a future release.
