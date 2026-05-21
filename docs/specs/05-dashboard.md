# Spec 05 — Interactive Dashboard

## Context

SPEC.md §13 Prompt 15 specified an interactive web dashboard. The
v0.1 milestone explicitly deferred this:

> The interactive **web dashboard** described in SPEC.md §13 prompt 15
> is intentionally **deferred to v0.2** — it is a separate frontend
> deliverable with its own UX surface. What ships in v0.1.0 is the
> data pipeline the dashboard will consume.

The pipeline that the dashboard consumes already exists: telemetry
events emitted by every subscriber, NDJSON export
([`crates/nidus-observability/src/export.rs`](../crates/nidus-observability/src/export.rs)),
and a CLI capable of writing them to stdout
([`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs)).

This spec builds the frontend.

## Deliverables

- `dashboard/` directory at the repo root: Vite + React + TypeScript
  SPA.
- `nidus serve` subcommand: a localhost websocket server that
  streams NDJSON from a running simulation.
- Five default views: maternal vitals, placental transport, fetal
  growth (vs NICHD), unknown-channels panel, scenario diff.
- Tier-as-colour throughout; click-to-show-citations on every
  plotted point.
- Build and bundle: `cargo run -p nidus-cli -- serve --scenario
  normal_term --port 7878 --open` opens the browser to the
  dashboard.

## Dependencies

Requires Spec 02 (the modules whose telemetry the dashboard
visualises) and Spec 03 (NICHD reference for the fetal growth view).
Not required for Specs 06–08.

## Numbered prompts

### Prompt 05.1 — `nidus serve` websocket subcommand

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs)
plus new module
[`crates/nidus-cli/src/serve.rs`](../crates/nidus-cli/src/serve.rs).

Behaviour:
- Spawns the simulator in a background thread.
- Buffers telemetry into a bounded mpsc channel.
- Exposes a websocket at `ws://127.0.0.1:<port>/stream` that emits
  newline-delimited JSON identical to `nidus run --emit ndjson -`.
- Exposes HTTP at `/manifest` returning the run manifest (after
  Spec 06).
- Exposes HTTP at `/parameters` returning the parameter database
  table (JSON).
- Embeds the static dashboard build (via `include_dir!`) at `/`.

Dependencies: `tokio`, `tokio-tungstenite`, `axum`. Add to
workspace; gate behind a `dashboard` feature flag so the headless
CLI stays minimal.

Verification: `nidus serve --scenario normal_term --port 7878` then
`websocat ws://127.0.0.1:7878/stream` prints NDJSON events; killing
the server severs the socket cleanly.

### Prompt 05.2 — Vite/React scaffold

Files: new `dashboard/` (Vite + React + TypeScript template, with
`pnpm` lockfile). Tooling: ESLint, Prettier, Vitest, Playwright.

Verification: `cd dashboard && pnpm install && pnpm dev` opens a
working dev server.

### Prompt 05.3 — Websocket client + telemetry store

File: `dashboard/src/lib/telemetry.ts`.

A Zustand (or Redux Toolkit) store: connects to
`ws://localhost:<port>/stream`, buffers events keyed by `(quantity,
age_weeks)`, exposes typed selectors for each subsystem. Handles
disconnects with visible status.

Verification: opening the dashboard against `nidus serve` shows
events arriving within 1 s; killing the server flips a "disconnected"
banner.

### Prompt 05.4 — Tier-aware plot primitive

File: `dashboard/src/components/TieredPlot.tsx`.

Wraps a chart (uPlot or Plotly-lite). Lines coloured by tier
(A green, B blue, C amber, D red); clicking a point opens a side
panel with the citation list returned by `/parameters` lookup.

### Prompt 05.5 — Maternal vitals view

File: `dashboard/src/views/Maternal.tsx`.

Plots cardiac output, MAP, uterine artery flow, minute ventilation,
GFR vs age. One `TieredPlot` per quantity, arranged in a grid.

### Prompt 05.6 — Placental transport view

File: `dashboard/src/views/Placenta.tsx`.

Plots placental surface area, gas-exchange equilibration, glucose
flux, amino-acid flux, with maternal and fetal interfacing
concentrations overlaid.

### Prompt 05.7 — Fetal growth view

File: `dashboard/src/views/Fetal.tsx`.

Plots fetal weight, length, head/abdominal circumference, overlaid
on NICHD reference percentiles from Spec 03. Heart rate and
descending-aortic PO₂ as smaller panels.

### Prompt 05.8 — Unknown-channels panel

File: `dashboard/src/views/Unknown.tsx`.

Renders the contents of the unknown-channel registry: each channel,
its current mode, supporting and questioning citations, and the
quantities downstream of it. Researcher can pivot a channel's mode
and re-run via the websocket control channel (HTTP POST
`/channels/:id/mode`).

### Prompt 05.9 — Scenario diff view

File: `dashboard/src/views/Diff.tsx`.

Two simultaneously-streamed scenarios (e.g. normal_term vs
placental_insufficiency) on the same axes; difference lines drawn
below. Requires `nidus serve` to support `--scenario` repeated
twice.

### Prompt 05.10 — Embedded static build

File: [`crates/nidus-cli/build.rs`](../crates/nidus-cli/build.rs)
(new).

`build.rs` runs `pnpm install && pnpm build` inside `dashboard/`
when the `dashboard` feature is enabled, then `include_dir!` ships
the bundle inside the binary. The build script is skipped if the
bundle directory already exists (incremental dev).

Verification: a release build with `--features dashboard` is a
single self-contained executable.

### Prompt 05.11 — Smoke test

File: new `dashboard/tests/smoke.spec.ts` (Playwright).

Starts `nidus serve` as a subprocess, navigates to the dashboard,
asserts the maternal cardiac-output plot has ≥ one data point within
ten seconds, then kills the server and asserts the disconnected
banner.

### Prompt 05.12 — User-facing docs

File: new [`docs/dashboard.md`](../docs/dashboard.md).

Covers: launching, the views, what tier colours mean, click-to-cite,
how to add a custom view (link to `dashboard/README.md`).

Update [`docs/architecture/overview.md:12`](../docs/architecture/overview.md)
to remove "(planned: web dashboard, Jupyter)" — both are now
shipped.

## Acceptance for Spec 05

- [ ] `nidus serve --scenario normal_term --port 7878 --open` opens
  a working dashboard.
- [ ] All five views render within ten seconds of starting.
- [ ] Tier colours visible; clicking a point opens citations.
- [ ] Killing `nidus serve` produces a visible disconnect banner,
  not a silent freeze.
- [ ] Playwright smoke test green in CI.
- [ ] `docs/dashboard.md` exists and is linked from `docs/README.md`.
