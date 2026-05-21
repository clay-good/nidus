# Quickstart

Five minutes from `pip install` to a chart of the dataset.

## Load the dataset

```python
import nidus

ds = nidus.load()
ds                  # <nidus.Dataset: 54 parameters, 32 citations>
len(ds)             # 54
len(ds.citations)   # 32
list(ds.subsystems())
# ['fetal_circulation', 'fetal_growth', 'fetal_metabolism',
#  'maternal_blood', 'maternal_cardiovascular', 'maternal_renal',
#  'maternal_respiratory', 'placental_gas_exchange',
#  'placental_glucose', 'placental_structure']
```

## Inspect a single parameter

```python
p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]

p.name                       # 'Pre-pregnancy cardiac output baseline'
p.value.central              # 4.6
p.value.units                # 'L/min'
p.value.low, p.value.high    # (4.2, 5.0)  one-sigma bounds
p.value.distribution         # 'normal'
p.tier                       # 'B'
p.tier_rationale             # multi-line synthesised rationale
p.primary_citation.doi       # '10.1097/HJH.0000000000000043'
p.applicability.population   # 'Healthy nulliparous women, ...'
```

`p.citations` is a tuple of resolved `Citation` objects (not citation keys), so chasing provenance is one attribute hop:

```python
for c in p.citations:
    print(f"{c.year} {c.authors[0]} — {c.title}")
```

## Filter

```python
# By subsystem
cardio = ds.filter(subsystem="maternal_cardiovascular")

# By tier (single or multiple)
tier_a = ds.filter(tier="A")
tier_ab = ds.filter(tier=["A", "B"])

# By review status
verified = ds.filter(review_status="verified")

# Combinations
target = ds.filter(
    subsystem="placental_glucose",
    tier=["A", "B"],
)
```

Filter returns a new `Dataset`; citations and tier definitions pass through unchanged so back-references still resolve.

## Inverse citation lookup

```python
# Which parameters cite a specific paper?
parameters = ds.citations_for("mahendru-2014-cardiac-output")
for p in parameters:
    print(f"[{p.tier}] {p.id}")
```

## Validate

```python
nidus.validate()                # bundled dataset
nidus.validate(path="my_dataset/")   # any layout matching the schemas
```

Raises `ValidationError` on any schema mismatch, with all errors aggregated into one readable message (capped at 50 lines).

## Quick chart

```python
from collections import Counter
import matplotlib.pyplot as plt

counts = Counter(p.tier for p in ds)
plt.bar(list("ABCD"), [counts.get(t, 0) for t in "ABCD"])
plt.ylabel("Parameters")
plt.title(f"Tier distribution across {len(ds)} parameters")
plt.show()
```

## Next steps

- The five [reference notebooks](../tutorials/index.md) walk through filtering, tiers, uncertainty propagation, and citation provenance.
- The [API reference](../api.md) documents every public class and method.
- The [interactive dashboard](https://nidus.streamlit.app) (placeholder URL) offers the same exploration without writing code.
