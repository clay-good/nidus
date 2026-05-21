# Nidus Specifications

The active design is split across two release-targeted directories:
**v0.3** (dataset, Python package, dashboard, outreach essay) and
**v0.4** (mechanistic-modeling interop with SBML, CellML, and
PhysioCell).

## v0.3 — Dataset, package, dashboard, essay

Lives in [`v0.3/`](v0.3/).

| Spec | File                                                                | Status                                                                |
| ---- | ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 00   | [`v0.3/00-overview.md`](v0.3/00-overview.md)                        | **READ FIRST for v0.3.** What we are doing and why.                  |
| 01   | [`v0.3/01-dataset-and-dashboard.md`](v0.3/01-dataset-and-dashboard.md) | **Active.** Dataset + Python package + Streamlit dashboard.       |
| 03   | [`v0.3/03-outreach-and-essay.md`](v0.3/03-outreach-and-essay.md)    | **Active.** Essay in the repository + Zenodo deposit on release.    |

## v0.4 — Mechanistic-modeling interop

Lives in [`v0.4/`](v0.4/). The earlier conditional SBML/CellML plan
was promoted to active primary work and expanded to include PhysioCell
once community adoption became the binding constraint (not maintenance
load).

| Spec | File                                                                                  | Status                                                                |
| ---- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 00   | [`v0.4/00-overview.md`](v0.4/00-overview.md)                                          | **READ FIRST for v0.4.** Why interop is now primary.                  |
| 01   | [`v0.4/01-mechanistic-modeling-interop.md`](v0.4/01-mechanistic-modeling-interop.md)  | **Active.** Full implementation plan: SBML, CellML, PhysioCell + repository submissions + composed top-level pregnancy model. |

## Earlier (pre-pivot) specs

The pre-v0.3 spec files (the original Rust-simulator design and
twelve numbered work-stream plans) lived alongside this README until
the dataset-first pivot. They were marked superseded for a while; once
nothing in the active design references them any more, they were
deleted. The original content is preserved in git history; recover any
of them with:

```
git log --all --diff-filter=D -- docs/specs/SPEC.md
git show <commit>:docs/specs/01-parameter-database.md
```

The pivot reasoning is captured in [`v0.3/00-overview.md`](v0.3/00-overview.md);
the prior architectural state is preserved at the `v0.2-archive` git
tag.
