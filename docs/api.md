# API reference

The full public surface of the `nidus` package. Everything below is
auto-generated from the source docstrings in
[`python/nidus/`](https://github.com/clay-good/nidus/tree/main/python/nidus)
via [mkdocstrings](https://mkdocstrings.github.io/), so this page cannot
drift out of sync with the code.

```python
import nidus
```

The public surface is intentionally small: one `load` function, one
`validate` function, one `Dataset` class, and a handful of frozen
dataclasses returned from them.

---

## Top-level functions

::: nidus.load.load
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.validate.validate
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.validate.ValidationError
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

---

## Dataset

::: nidus.load.Dataset
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false
      members:
        - __getitem__
        - __contains__
        - __iter__
        - __len__
        - __repr__
        - parameters
        - ids
        - subsystems
        - filter
        - citations_for
        - citations
        - tiers

---

## Dataclasses

The loader returns frozen, slot-using dataclasses. They are hashable and
safe to share across threads.

::: nidus.models.Parameter
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Value
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Citation
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Trajectory
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Extraction
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Applicability
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.TierDef
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

---

## Type aliases

::: nidus.models.Tier
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false

::: nidus.models.Subsystem
    options:
      heading_level: 3
      show_root_heading: true
      show_root_full_path: false
