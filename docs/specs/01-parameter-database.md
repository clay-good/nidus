# Spec 01 — Parameter Database

## Context

Today the parameter database is a working *loader* with one sparsely
populated TOML file:

- [`data/parameters/maternal/blood.toml`](../data/parameters/maternal/blood.toml)
  contains two scaffold entries.
- [`data/parameters/placenta/`](../data/parameters/placenta/) and
  [`data/parameters/fetal/`](../data/parameters/fetal/) directories
  exist but are empty.
- [`data/citations/index.toml`](../data/citations/index.toml) holds
  one real entry and one named `scaffold-template-source`.

Every subsystem (`MaternalCardio`, `PlacentalStructure`,
`PlacentalGasExchange`, `PlacentalGlucoseTransport`,
`FetalCirculation`) hard-codes its numeric defaults inside Rust
`Params` structs and self-flags those defaults as scaffold (see
[`crates/nidus-maternal/src/cardio.rs:71-90`](../crates/nidus-maternal/src/cardio.rs),
[`crates/nidus-placenta/src/structure.rs:36-39`](../crates/nidus-placenta/src/structure.rs),
[`crates/nidus-placenta/src/transport.rs:44-99`](../crates/nidus-placenta/src/transport.rs),
[`crates/nidus-fetal/src/special_circulation.rs:57-59`](../crates/nidus-fetal/src/special_circulation.rs)).

This spec replaces every one of those scaffold values with a real,
cited, tiered, age-resolved entry in `data/`.

## Deliverables

- `data/citations/index.toml`: ≥ 40 verified citations covering every
  parameter shipped in v0.2.0.
- `data/citations/README.md`: documents the verification workflow.
- `data/parameters/maternal/{blood,cardio,respiratory,renal,metabolic,endocrine}.toml`
- `data/parameters/placenta/{structure,gas_transport,glucose_transport,amino_acid_transport,endocrine,barrier}.toml`
- `data/parameters/fetal/{circulation,growth,cardiac,metabolism,organ_maturation,endocrine}.toml`
- Every `*Params` struct gains `from_database(&ParameterDatabase) -> Result<Self, _>`,
  used as the primary constructor by every subscriber.
- Hard-coded defaults survive only inside `#[cfg(test)]` blocks.
- A `--strict-tier` CLI flag that exits non-zero if any parameter
  used by the current scenario is tier C or worse.

## Dependencies

None. This spec is the foundation for everything else.

## Numbered prompts

### Prompt 01.1 — Citation index reset

File: [`data/citations/index.toml`](../data/citations/index.toml),
new file [`data/citations/README.md`](../data/citations/README.md).

Replace the current `index.toml` with verified entries. Each entry
needs `id`, `authors`, `title`, `venue`, `year`, and one of
`doi`/`pmid`, plus a `notes` field listing which parameter files
depend on it. Drop `scaffold-template-source`. The minimum citation
set (extend as needed):

| Domain | Citation seeds |
|---|---|
| O₂–Hb dissociation | Severinghaus 1979, Dash & Bassingthwaighte 2010, Kelman 1966 |
| Maternal blood volume | Hytten & Chamberlain 1980, Bernstein & Ziegler 2001, de Haas 2017 |
| Maternal cardiovascular | Mahendru 2014, Sanghavi & Rutherford 2014, Hunter & Robson 1992 |
| Maternal respiratory | LoMauro & Aliverti 2015, Crapo 1996 |
| Maternal renal | Cheung & Lafayette 2013, Davison & Hytten 1974 |
| Placental morphometry | Mayhew 2014, Carter 2009, Burton 2010 |
| Placental gas diffusion | Mayhew 1986, Carter & Pijnenborg 2011 |
| GLUT1/GLUT3 kinetics | Illsley 2000, Baumann 2002, Brown 2011 |
| Amino acid transport | Cleal & Lewis 2008, Regnault 2002 |
| Fetal growth | Buck Louis (NICHD) 2015, Grewal 2018, Hadlock 1991 |
| Fetal circulation | Rudolph 1985, Kiserud 2000, Sutton 1991 |
| Fetal organ maturation | Avery & Mead 1959 (surfactant), Burri 2006 (lung) |

Write `data/citations/README.md` covering: how to add a citation
(must have read the PDF; PMID/DOI required), how a reviewer verifies
one (open the source, confirm the values used by every dependent
parameter, initial the PR), and the tier-promotion record.

Verification: `cargo test -p nidus-data` passes; every citation in
`index.toml` resolves; no entry contains the substring "scaffold" or
"placeholder".

### Prompt 01.2 — Maternal blood parameters

File: [`data/parameters/maternal/blood.toml`](../data/parameters/maternal/blood.toml).

Author entries with `AgeRange` blocks per trimester (or finer where
data supports). Values use `ValueSpec::normal { mean, sd }`:

- `maternal.blood.volume_l` — total blood volume.
- `maternal.blood.plasma_volume_l`.
- `maternal.blood.red_cell_mass_l`.
- `maternal.blood.hematocrit_fraction`.
- `maternal.blood.hemoglobin_g_per_dl`.
- `maternal.blood.oxyhb_p50_mmhg` — incl. shift in pregnancy.
- `maternal.blood.oncotic_pressure_mmhg`.
- `maternal.blood.fibrinogen_g_per_l`.

Each entry cites the appropriate `id` from `index.toml` and sets
`tier = "A"` or `tier = "B"` per SPEC.md §3.

Verification: `nidus list parameters --search maternal.blood` lists
all entries; `nidus list parameters --tier A` includes them.

### Prompt 01.3 — Maternal cardiovascular parameters

File: new [`data/parameters/maternal/cardio.toml`](../data/parameters/maternal/cardio.toml).

Author entries replacing each hard-coded constant in
[`crates/nidus-maternal/src/cardio.rs:71-90`](../crates/nidus-maternal/src/cardio.rs):

| Database id | Replaces |
|---|---|
| `maternal.cardio.baseline_cardiac_output_l_per_min` | line 75 |
| `maternal.cardio.peak_excess_cardiac_output_l_per_min` | line 76 |
| `maternal.cardio.cardiac_output_peak_week` | line 77 |
| `maternal.cardio.cardiac_output_spread_weeks` | line 78 |
| `maternal.cardio.cardiac_output_individual_sigma` | line 79 |
| `maternal.cardio.baseline_map_mmhg` | line 81 |
| `maternal.cardio.map_nadir_drop_mmhg` | line 82 |
| `maternal.cardio.map_nadir_week` | line 83 |
| `maternal.cardio.map_spread_weeks` | line 84 |
| `maternal.cardio.map_individual_sigma_mmhg` | line 85 |
| `maternal.cardio.baseline_uterine_flow_ml_per_min` | line 87 |
| `maternal.cardio.term_uterine_flow_ml_per_min` | line 88 |
| `maternal.cardio.uterine_flow_growth_rate_per_week` | line 89 |
| `maternal.cardio.uterine_flow_individual_sigma` | line 90 |

Each entry must cite Mahendru 2014, Hunter & Robson 1992, or
Sanghavi & Rutherford 2014.

Verification: `nidus list parameters --search maternal.cardio` shows
all 14 entries.

### Prompt 01.4 — `MaternalCardioParams::from_database`

File: [`crates/nidus-maternal/src/cardio.rs`](../crates/nidus-maternal/src/cardio.rs).

Add:

```rust
impl MaternalCardioParams {
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> { ... }
}
```

Move the current hard-coded defaults into a `#[cfg(test)] fn scaffold() -> Self`
helper so they survive only in tests. Update the
`MaternalCardio::new` and all dispatcher wiring to take a constructed
`Params` instead of relying on `Default`. Remove the `impl Default for
MaternalCardioParams` outside of `#[cfg(test)]`.

Verification: `cargo test -p nidus-maternal`; non-test code path no
longer compiles without a database load.

### Prompt 01.5 — Placental structure & transport parameters

Files:
- new [`data/parameters/placenta/structure.toml`](../data/parameters/placenta/structure.toml)
- new [`data/parameters/placenta/gas_transport.toml`](../data/parameters/placenta/gas_transport.toml)
- new [`data/parameters/placenta/glucose_transport.toml`](../data/parameters/placenta/glucose_transport.toml)

Replace every constant in
[`crates/nidus-placenta/src/structure.rs:36-39`](../crates/nidus-placenta/src/structure.rs)
and [`crates/nidus-placenta/src/transport.rs:44-99`](../crates/nidus-placenta/src/transport.rs):

- `placenta.structure.initial_area_m2`, `placenta.structure.term_area_m2`,
  `placenta.structure.midpoint_week`, `placenta.structure.growth_rate_per_week`
  — cite Mayhew 2014.
- `placenta.gas.half_saturation_area_m2`, `placenta.gas.max_equilibration`
  — cite Carter & Pijnenborg 2011; tier C is acceptable.
- `placenta.glucose.km_mmol_per_l`, `placenta.glucose.vmax_per_area_mmol_per_min_per_m2`
  — cite Illsley 2000 (GLUT1) and Brown 2011 (GLUT3); split into two
  parameters per transporter family if the database supports.

Verification: all eight ids resolve via `db.get(id)`.

### Prompt 01.6 — Placental params: `from_database`

File: [`crates/nidus-placenta/src/structure.rs`](../crates/nidus-placenta/src/structure.rs),
[`crates/nidus-placenta/src/transport.rs`](../crates/nidus-placenta/src/transport.rs).

Mirror Prompt 01.4: add `StructureParams::from_database`,
`GasExchangeParams::from_database`,
`GlucoseTransportParams::from_database`. Move scaffold defaults
behind `#[cfg(test)]`. Update orchestrator wiring.

Verification: `cargo test -p nidus-placenta`.

### Prompt 01.7 — Fetal circulation parameters

Files: new [`data/parameters/fetal/circulation.toml`](../data/parameters/fetal/circulation.toml),
edits to [`crates/nidus-fetal/src/special_circulation.rs:57-59`](../crates/nidus-fetal/src/special_circulation.rs).

Replace `foramen_ovale_streamline_preference`,
`ductus_arteriosus_share`, `systemic_venous_return_po2_mmhg` with
database entries. Cite Rudolph 1985 and Kiserud 2000. Add
`FetalCirculationParams::from_database`.

Verification: `cargo test -p nidus-fetal`; database lookup is the
only non-test constructor.

### Prompt 01.8 — Strict-tier flag

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs).

Add a top-level `--strict-tier <A|B|C>` flag (and equivalent option
on `nidus run`). After scenario load, walk every parameter actually
read by the run and exit non-zero with a clear listing if any entry
is below the requested tier.

Verification: `nidus run normal_term --strict-tier A` exits non-zero
if any tier-B or worse parameter is in use; `--strict-tier B` admits
B-tier parameters.

### Prompt 01.9 — Parameter database hash

File: [`crates/nidus-data/src/database.rs`](../crates/nidus-data/src/database.rs).

Add `ParameterDatabase::sha256() -> String` that returns a stable
hash of the canonical TOML-bytes representation of every loaded
entry (sorted by id). This hash is consumed by Spec 06 (manifest
output) and Spec 08 (release metadata).

Verification: identical databases on two machines produce identical
hashes; a one-byte change in any TOML changes the hash.

### Prompt 01.10 — Parameter coverage report

File: new [`docs/parameter-coverage.md`](../docs/parameter-coverage.md),
generated by `nidus list parameters --coverage` (new subcommand).

`nidus list parameters --coverage` walks the database and produces a
Markdown matrix: subsystem × confidence tier × number of parameters.
Highlights gaps (parameters referenced in code but not yet in the
database).

Verification: running the subcommand on the v0.1 database flags every
scaffold default; running on the post-Spec-01 database reports zero
unfilled references.

## Acceptance for Spec 01

- [ ] `cargo test --workspace` green.
- [ ] `nidus list parameters --tier A` returns ≥ 25 entries.
- [ ] `nidus list parameters --tier B` returns ≥ 15 entries.
- [ ] No `*Params::default()` exists outside `#[cfg(test)]`.
- [ ] `grep -rni "scaffold\|placeholder" data/` returns no matches in
  values or notes (matches in `README.md` describing past state are
  OK).
- [ ] `nidus list parameters --coverage` reports zero unfilled
  references for the four shipped scenarios.
- [ ] Database hash is stable across two clean checkouts.
