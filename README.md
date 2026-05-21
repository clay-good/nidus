# NIDUS

**A Research Simulator for Human Gestational Physiology**

*Version 0.1.0 — under active construction.*

Nidus is an open-source, MIT-licensed computational tool for surfacing what
we know, what we do not know, and what would be most valuable to measure
next about human pregnancy. The full design is captured in [SPEC.md](SPEC.md);
this README is a short orientation.

## What Nidus is

Nidus is a research simulator that models the coupled maternal–fetal
physiological system across human pregnancy, from approximately eight weeks
gestational age through forty weeks. It integrates current scientific
understanding of maternal cardiovascular adaptation, placental transport and
endocrinology, and fetal development into a single composable computational
substrate. It is deterministic where the underlying biology is
mechanistically understood and stochastic where the biology is irreducibly
variable. It is built to be reproducible, citable, auditable, and extensible.

The project's defining commitment is that every modelled quantity carries an
explicit confidence tier, every parameter is annotated with its scientific
source, and every output makes the boundary between established knowledge
and active uncertainty visible to the user. Nidus is designed to be honest
about its own limits, because dishonesty about uncertainty is what turns a
useful research tool into a misleading one.

## What Nidus is not

Nidus is **not** a clinical decision support tool. It does not generate
recommendations for the care of any specific pregnancy and is not validated
for any decision affecting a real patient.

Nidus is **not** a control system for a medical device, and it is **not** an
autonomous AI agent or automated medical researcher. It is a
hypothesis-generation tool with humans in the loop at every empirical step:
the simulator generates hypotheses; humans evaluate them, design experiments
to test them, execute those experiments in physical reality, and bring the
results back to update the simulator's parameter database. The loop closes
in the laboratory and the clinic, not in software.

Nidus does not model the embryonic period prior to eight weeks, does not
model labour and delivery, and does not model twin or higher-order
pregnancies in version 0.1.0. Each of these is a substantial modelling
problem in its own right and is intentionally deferred to future work.

## Repository layout

```
nidus/
├── crates/
│   ├── nidus-core/              # deterministic engine: tier infra, tick hierarchy, RNG service
│   ├── nidus-maternal/          # maternal subsystem (planned)
│   ├── nidus-placenta/          # placental interface (planned)
│   ├── nidus-fetal/             # fetal subsystem (planned)
│   ├── nidus-unknown/           # unknown channels registry (planned)
│   ├── nidus-data/              # parameter database + citation index (planned)
│   ├── nidus-validation/        # validation suite (planned)
│   ├── nidus-scenarios/         # scenario configurations (planned)
│   ├── nidus-hypothesis/        # hypothesis generation (planned)
│   ├── nidus-observability/     # dashboards, telemetry, visualisation (planned)
│   ├── nidus-cli/               # command-line interface
│   └── nidus-py/                # Python bindings (planned)
├── SPEC.md                      # full design specification
├── PROGRESS.md                  # which implementation prompts are done
├── CONTRIBUTING.md              # contribution guide, including the tier system
└── CODE_OF_CONDUCT.md
```

## Building

```sh
cargo build --workspace
cargo test --workspace
```

A working Rust toolchain (1.75+) is the only external requirement to build
and run the test suite.

## Contributing

The most valuable contributions are parameter updates derived from
published empirical work. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
confidence tier system, how parameters are reviewed, and what other forms
of contribution look like.

## Licence

MIT. See [LICENSE](LICENSE).
