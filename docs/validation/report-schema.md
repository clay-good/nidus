# Validation Report — JSON Schema

`nidus validate --format json` writes a single JSON object whose shape
is intended to be stable across patch releases. Breaking changes bump
the top-level schema version (when introduced) and land in a release
where the major or minor version of Nidus also changes.

## Top-level object

| Field | Type | Description |
| --- | --- | --- |
| `summary` | object | Counts of cases by `Agreement` bucket. |
| `summary.excellent` | integer | Cases in the `Excellent` bucket. |
| `summary.adequate` | integer | Cases in the `Adequate` bucket. |
| `summary.divergent` | integer | Cases in the `Divergent` bucket. |
| `summary.unvalidatable` | integer | Cases in the `Unvalidatable` bucket. |
| `results` | array of objects | One entry per `ValidationCase`. |

## `results[i]`

| Field | Type | Description |
| --- | --- | --- |
| `case_id` | string | Stable case identifier (`case:<subsystem>:<quantity>`). |
| `component` | string | Subsystem path, e.g. `nidus-maternal:cardio`. |
| `tier` | string | Confidence tier: `A` / `B` / `C` / `D`. |
| `level` | string | `Component` / `Integration` / `Outcome`. |
| `total_points` | integer | Number of reference points evaluated. |
| `points_in_range` | integer | Points where the simulator output fell inside the case's tolerance band. |
| `rms_residual` | number | Root-mean-square residual between simulator and reference means, in the case's native unit. |
| `residuals` | array of numbers | Per-point residuals (simulator − reference). |
| `agreement` | string | One of `Excellent` / `Adequate` / `Divergent` / `Unvalidatable`. |

## Stability guarantees

- Field names are stable; new fields are additive.
- Field order is not guaranteed (consume by name, not by position).
- The `agreement` enum is closed in this minor release; a new bucket
  would be a schema bump.
- `case_id` values are stable strings — downstream tooling can key off
  them across releases.

## Example

```json
{
  "summary": {
    "excellent": 1,
    "adequate": 0,
    "divergent": 0,
    "unvalidatable": 0
  },
  "results": [
    {
      "case_id": "case:maternal-cardio:cardiac-output",
      "component": "nidus-maternal:cardio",
      "tier": "B",
      "level": "Component",
      "total_points": 6,
      "points_in_range": 6,
      "rms_residual": 0.21,
      "residuals": [0.10, -0.15, 0.30, 0.25, -0.20, -0.05],
      "agreement": "Excellent"
    }
  ]
}
```

The example shape is illustrative; exact numbers move as the model and
reference data evolve.
