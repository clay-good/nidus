# Schema

Every parameter, citation, and tier definition in the nidus dataset validates against a JSON Schema (draft 2020-12). The schemas live in [`dataset/schema/`](https://github.com/claygood/nidus/tree/main/dataset/schema) and are bundled into the package.

Run `nidus.validate()` to validate the whole bundled dataset, or `nidus.validate(path="...")` to validate an external copy.

---

## Parameter

Source: [`parameter.schema.json`](https://github.com/claygood/nidus/blob/main/dataset/schema/parameter.schema.json)

```json
{
  "id": "maternal_cardiovascular.baseline_cardiac_output_l_per_min",
  "name": "Pre-pregnancy cardiac output baseline",
  "subsystem": "maternal_cardiovascular",
  "value": {
    "central": 4.6,
    "low": 4.2,
    "high": 5.0,
    "units": "L/min",
    "distribution": "normal",
    "ci": 0.683
  },
  "tier": "B",
  "tier_rationale": "Multiple longitudinal cohort studies; CIs overlap...",
  "citations": ["mahendru-2014-cardiac-output"],
  "primary_citation": "mahendru-2014-cardiac-output",
  "extraction": {
    "review_status": "verified",
    "method": "table_2_column_3",
    "by": "claygood",
    "date": "2026-05-21"
  },
  "applicability": {
    "population": "Healthy nulliparous women, pre-conception"
  },
  "notes": "Polynomial fit, not mechanistic..."
}
```

| Field              | Required | Notes                                                                                                |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| `id`               | yes      | Dotted, snake_case. Must match the regex `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$`.                    |
| `name`             | yes      | Human-readable.                                                                                      |
| `subsystem`        | yes      | One of the [ten enum values](subsystems.md).                                                         |
| `value.central`    | yes      | Best central estimate.                                                                               |
| `value.units`      | yes      | SI or domain-conventional (`L/min`, `mmHg`, `g`, etc.).                                              |
| `value.low/high`   | no       | Uncertainty bounds at the level given by `ci`.                                                       |
| `value.distribution` | no     | `normal`, `lognormal`, `uniform`, or `empirical`.                                                    |
| `tier`             | yes      | `A` / `B` / `C` / `D`. See [tier system](tiers.md).                                                  |
| `tier_rationale`   | yes      | At least 10 characters; must reference the evidence base.                                            |
| `citations`        | yes      | At least one citation key, each resolving to an entry in `citations.json`.                           |
| `primary_citation` | no       | Most load-bearing citation; must be present in `citations`.                                          |
| `extraction.review_status` | yes | `unverified`, `verified`, or `contested`.                                                       |
| `trajectory`       | no       | Optional gestational-age-dependent shape. Most current entries are scalar.                           |
| `applicability`    | no       | Population the parameter applies to + known exclusions.                                              |
| `notes`            | no       | Free-text caveats.                                                                                   |

Additional properties are rejected (`additionalProperties: false`).

---

## Citation

Source: [`citation.schema.json`](https://github.com/claygood/nidus/blob/main/dataset/schema/citation.schema.json)

```json
{
  "key": "mahendru-2014-cardiac-output",
  "type": "journal-article",
  "title": "A longitudinal study of maternal cardiovascular function...",
  "authors": ["Mahendru AA", "Everett TR", "Wilkinson IB", "Lees CC", "McEniery CM"],
  "year": 2014,
  "journal": "Journal of Hypertension",
  "doi": "10.1097/HJH.0000000000000043",
  "pmid": "24406777"
}
```

| Field      | Required | Notes                                                                                  |
| ---------- | -------- | -------------------------------------------------------------------------------------- |
| `key`      | yes      | Kebab- or snake-case; the JSON object key in `citations.json` must match.              |
| `type`     | yes      | `journal-article`, `book`, `book-chapter`, `conference-paper`, `preprint`, `report`, `dataset`, `thesis`. |
| `title`    | yes      |                                                                                        |
| `authors`  | yes      | Array of strings, "Family, Given" style preferred.                                     |
| `year`     | yes      | 1800–2100.                                                                             |
| `doi` / `pmid` / `url` / `isbn` | no | Journal articles SHOULD carry a DOI or PMID. Books may carry none (predate DOIs). The README rule that Tier A/B parameters cite a DOI/PMID is enforced at the parameter level by CI, not the schema. |
| `journal` / `publisher` / `volume` / `issue` / `pages` | no | |
| `open_access` | no    | Boolean.                                                                               |

---

## Tier

Source: [`tier.schema.json`](https://github.com/claygood/nidus/blob/main/dataset/schema/tier.schema.json)

The four tier definitions live in `dataset/tiers/tiers.json`. The schema requires `label` + `criteria` (non-empty array of strings) for each of `A`, `B`, `C`, `D`. See the [tier system page](tiers.md) for the actual definitions.

---

## Cross-file invariants

The schemas can't express these on their own; `nidus.validate()` enforces them:

- Every `citations[]` entry on a parameter resolves to a real citation key.
- Every `primary_citation` (if present) is in that parameter's `citations` and exists in `citations.json`.
- Parameter `id`s are globally unique across files.
- The dict key in `citations.json` matches the embedded `key` field.
