# API reference

The full public surface of the `nidus` package. Everything below is type-annotated and covered by tests in [`python/tests/`](https://github.com/claygood/nidus/tree/main/python/tests).

```python
import nidus
```

## Top-level functions

### `nidus.load`

```python
def load(version: str | None = None, path: str | Path | None = None) -> Dataset
```

Load the nidus dataset.

- `version` — *reserved for future use.* Pass-through versions of the dataset will be supported once a version-pinning mechanism is in place. Raises `NotImplementedError` if set.
- `path` — optional directory containing a `parameters/`, `citations/`, `tiers/`, and `schema/` layout. If unset, the bundled dataset is used.

Returns a `Dataset` ready for indexed access and filtering.

### `nidus.validate`

```python
def validate(path: str | Path | None = None) -> None
```

Validate a nidus dataset against the bundled JSON Schemas (draft 2020-12), plus cross-file invariants (unique parameter ids, citation cross-references, citation key/field consistency).

Raises `ValidationError` on any issue; the message aggregates all errors found (capped at 50 lines).

---

## `nidus.Dataset`

A loaded dataset. Acts as a dict from parameter id to `Parameter`.

### Iteration & access

```python
ds[parameter_id]          # -> Parameter; KeyError if unknown
parameter_id in ds        # -> bool
len(ds)                   # -> int
for p in ds: ...          # iterate over Parameter values
```

### Attributes

| Attribute       | Type                   | Description                                                  |
| --------------- | ---------------------- | ------------------------------------------------------------ |
| `parameters`    | `tuple[Parameter, ...]`| All parameters in insertion order.                           |
| `citations`     | `dict[str, Citation]`  | All citations, keyed by citation key.                        |
| `tiers`         | `dict[str, TierDef]`   | Tier definitions keyed by `"A"`, `"B"`, `"C"`, `"D"`.        |

### Methods

```python
ds.ids() -> tuple[str, ...]
```

All parameter ids.

```python
ds.subsystems() -> tuple[str, ...]
```

Sorted list of distinct subsystems present in the dataset.

```python
ds.filter(
    subsystem: str | list[str] | tuple[str, ...] | None = None,
    tier:      str | list[str] | tuple[str, ...] | None = None,
    review_status: str | list[str] | tuple[str, ...] | None = None,
) -> Dataset
```

Return a new `Dataset` containing only matching parameters. Any `None` argument is no constraint. String arguments are equivalent to a single-element list. Citations and tier definitions are carried through unchanged so back-references still resolve.

```python
ds.citations_for(citation_key: str) -> tuple[Parameter, ...]
```

Return all parameters that cite a given citation key. Empty tuple if unknown.

---

## `nidus.Parameter`

Frozen dataclass. Returned from `Dataset[id]` and `Dataset.filter()`.

| Field                | Type                | Notes                                                           |
| -------------------- | ------------------- | --------------------------------------------------------------- |
| `id`                 | `str`               | Dotted, snake_case.                                             |
| `name`               | `str`               |                                                                 |
| `subsystem`          | `str`               | One of the [ten enum values](dataset/subsystems.md).            |
| `value`              | `Value`             |                                                                 |
| `tier`               | `str`               | `"A"` / `"B"` / `"C"` / `"D"`.                                  |
| `tier_rationale`     | `str`               |                                                                 |
| `citations`          | `tuple[Citation, …]`| **Resolved Citation objects**, not keys.                        |
| `extraction`         | `Extraction`        |                                                                 |
| `category`           | `str \| None`       |                                                                 |
| `trajectory`         | `Trajectory \| None`| Optional gestational-age-dependent shape.                       |
| `primary_citation`   | `Citation \| None`  | Most load-bearing citation (resolved).                          |
| `applicability`      | `Applicability \| None` | Population + exclusions.                                    |
| `notes`              | `str \| None`       | Free-text caveats.                                              |

---

## `nidus.Value`

```python
@dataclass(frozen=True)
class Value:
    central: float
    units: str
    low: float | None
    high: float | None
    distribution: str | None
    ci: float | None
```

Most v0.3 records use `distribution="normal"` with `low`/`high` at one sigma (`ci=0.683`); a few are point estimates with no bounds.

---

## `nidus.Citation`

```python
@dataclass(frozen=True)
class Citation:
    key: str
    type: str          # 'journal-article', 'book', 'preprint', ...
    title: str
    authors: tuple[str, ...]
    year: int
    journal: str | None
    publisher: str | None
    doi: str | None
    pmid: str | None
    url: str | None
    volume: str | None
    issue: str | None
    pages: str | None
    open_access: bool | None
    isbn: str | None
    notes: str | None
```

---

## `nidus.Extraction`

```python
@dataclass(frozen=True)
class Extraction:
    review_status: str   # 'unverified' | 'verified' | 'contested'
    method: str | None   # 'table_2_column_3', 'figure_4_digitised', ...
    by: str | None
    date: str | None     # ISO date
    reviewer: str | None
```

---

## `nidus.Trajectory`

```python
@dataclass(frozen=True)
class Trajectory:
    type: str            # 'constant' | 'linear' | 'polynomial' | 'gaussian' | 'logistic' | 'exponential' | 'piecewise'
    params: dict[str, float]
    valid_range_weeks: tuple[float, float] | None
```

Optional gestational-age-dependent shape. Most v0.3 records are scalars and omit `trajectory`; the field is reserved for future curation work.

---

## `nidus.Applicability`

```python
@dataclass(frozen=True)
class Applicability:
    population: str | None
    excludes: tuple[str, ...]
```

---

## `nidus.TierDef`

```python
@dataclass(frozen=True)
class TierDef:
    label: str
    criteria: tuple[str, ...]
    examples: tuple[str, ...]
```

Returned in `Dataset.tiers["A"]`, etc.

---

## `nidus.ValidationError`

`class ValidationError(Exception)` — raised by `nidus.validate()` on any schema or cross-file inconsistency.
