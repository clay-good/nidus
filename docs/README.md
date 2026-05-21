# Nidus Documentation

The documentation tree mirrors the structure described in
[SPEC.md §12](specs/SPEC.md):

- [`architecture/`](architecture/) — design decisions, module
  relationships, the tier system, and the determinism contract.
- [`modules/`](modules/) — one short page per crate, summarising
  responsibilities, inputs/outputs, and where the line currently
  sits between implemented and scaffolded content.
- [`validation/`](validation/) — the validation framework, the
  agreement classifier, and the per-case docs. Start with
  [`validation/overview.md`](validation/overview.md); see also
  [`validation/extending.md`](validation/extending.md) for the new-case
  workflow and [`validation/report-schema.md`](validation/report-schema.md)
  for the JSON output schema.
- [`contributing/`](contributing/) — extended notes on the
  pull-request workflow for parameter, citation, channel, and code
  contributions.
- [`tutorials/`](tutorials/) — researcher-facing walkthroughs.

The single source of truth for the project's design is
[SPEC.md](specs/SPEC.md). This documentation tree links into the spec
rather than duplicating it.
