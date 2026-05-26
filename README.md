# Nidus

**A curated, citation-backed dataset of human gestational physiology parameters — annotated with explicit confidence tiers, and exportable into the standard mechanistic-modeling formats (SBML, CellML, PhysioCell, COMBINE).**

> *Nidus* (Latin: "nest") — the implantation site where the blastocyst burrows into the uterine wall and where the most consequential negotiation in mammalian biology begins.

---

## The story this dataset is trying to help us understand

Human pregnancy is one of the most intricate biological coordination problems we know of, and a surprising amount of it is a **negotiation between three genomes** — mother, father, and fetus — that have **partially conflicting interests** and only ten months to settle them. Almost every parameter in this dataset is a measurement of that negotiation in progress.

### Three sets of inputs, one shared bloodstream

**The mother's contribution** is, broadly, an entire restructured circulatory and metabolic state. By term, she carries ~45% more plasma volume, ~50% more cardiac output, ~50% higher GFR, dramatically more clotting factors, a leftward-shifted O₂ dissociation curve to favor offloading, and an immune system that has learned to tolerate a half-foreign tissue she would normally reject. This is not a passive accommodation — it is a coordinated multi-organ adaptation, with timing as precise as the gestational clock allows.

**The fetus contributes a unique haemoglobin** (HbF, with a P50 of ~19.5 mmHg vs. the adult ~26.6 mmHg) that lets it extract oxygen from the relatively oxygen-poor intervillous blood; a fetal circulation with three shunts (ductus venosus, foramen ovale, ductus arteriosus) that route the best-oxygenated blood to the brain; and a metabolism running on glucose and lactate while it grows by a factor of ~600 from 8 weeks to term.

**The placenta** — genetically the fetus, anatomically embedded in the mother — is the negotiator. It transports gases, glucose, amino acids, lipids, IgG, and (carefully) almost nothing else. It produces enormous quantities of hormones (hCG, hPL, progesterone, estriol) that reshape maternal physiology. And it is built by the trophoblast, the most spectacularly invasive non-cancerous human tissue.

### Where the conflict starts

This is the part biology textbooks tend to underplay. The **father's genome, expressed in the fetus, has a different optimum than the mother's**. From an evolutionary-game-theory standpoint (the *parent–offspring conflict* literature, Haig 1993 onward), paternally-imprinted genes favor extracting more resources from this particular pregnancy — more nutrients, more blood flow, larger placenta, larger baby — because the father is not guaranteed to be the parent of the next one. The mother's genome and her body, meanwhile, have to budget across her remaining reproductive lifespan and across her own survival.

So at implantation, the **paternally-driven trophoblast invades aggressively**. It eats its way through the decidua, finds the maternal spiral arteries, and **remodels them** — destroying their smooth-muscle layer so that they become wide, low-resistance, unregulated conduits dumping maternal blood straight into the intervillous space at a rate that will eventually reach ~600 mL/min by term. From the fetus's standpoint this is the goal: a high-throughput, low-resistance perfusion bed that no maternal vasoactive signal can throttle.

The mother says, in effect, *whoa, don't kill me*. She runs a counter-program. She tightens systemic vascular tone. She tries to retain control of perfusion. She presents a placental barrier (the syncytiotrophoblast) that limits what can cross. She raises clotting factors to seal the wound when this whole arrangement detaches in nine months. She mounts a precisely tuned tolerance response — strong enough not to reject the half-foreign tissue, narrow enough not to leave herself open to infection.

When the negotiation works, the result is a healthy term pregnancy: ~3.5 kg of well-perfused baby, a placenta that delivered for forty weeks and then released cleanly, and a mother whose physiology snaps back over the following months. When it goes wrong, you get the syndromes that still drive most maternal and perinatal morbidity worldwide:

- **Pre-eclampsia** — incomplete spiral-artery remodelling, a hypoperfused placenta releasing anti-angiogenic factors (sFlt-1, sEng) into the maternal circulation, and a systemic endothelial crisis that can progress to seizures and stroke.
- **Fetal growth restriction (FGR)** — a placenta that cannot deliver enough; the fetus down-regulates growth, redistributes blood flow to spare the brain (the so-called *brain-sparing* response, visible as a falling MCA pulsatility index), and risks stillbirth.
- **Gestational diabetes** — placental hormones (hPL, progesterone, placental GH) impose insulin resistance to push glucose toward the fetus; in some women the pancreas cannot keep up.
- **Hypercoagulability and VTE** — the same clotting-factor surge that makes delivery survivable also makes pregnancy the highest-VTE-risk state in a healthy adult's life.
- **Postpartum haemorrhage** — when the negotiated detachment of the placenta fails to seal correctly.

These are the consequences of a beautiful, intricate, evolved compromise running at the edge of its tolerances.

### What this dataset is for

The mechanisms above are reasonably understood. The **numbers** — what cardiac output looks like at 24 weeks, what intervillous PO₂ actually is, what the Michaelis constant of placental GLUT1 is, what umbilical vein flow scales as a function of fetal weight — are scattered across forty years of obstetric, physiological, and morphometric literature, much of it paywalled, most of it never collated.

Anyone who wants to **simulate** any of this — a placental gas-exchange model, a fetal-growth model, a hemodynamic model of pre-eclampsia — has to spend weeks rebuilding the parameter table from scratch. Then the next researcher does the same. Then the same numbers get re-typed (and quietly mis-typed) into the next paper's table.

**Nidus is that parameter table**, curated once, citation-backed, machine-readable, exported into the formats the modeling community already uses. Every parameter carries an explicit confidence tier (how good is this number, honestly?), a peer-reviewed citation, the rationale for the tier assignment, and a human-verification status. It is the smallest possible piece of infrastructure that could make pregnancy modeling **honest about uncertainty by default**.

That is the whole project. The dataset is the centerpiece. The Python package, the dashboard, the SBML/CellML/PhysioCell exports — those are presentation layers around the data.

---

## At a glance

- **243 parameters** across **13 subsystems** (maternal cardiovascular / blood / renal / respiratory / endocrine; placental structure / gas exchange / glucose / endocrine; fetal circulation / growth / metabolism; amniotic fluid). Every row in the spec-04 exhaustive parameter catalog is now `shipped`.
- **68 citations**, each verified against Crossref or PubMed metadata.
- **28 parameters human-verified** against the source PDF; 1 `contested`; the remainder are `unverified` (central value from the literature, but a human has not yet eyeballed the source against the dataset entry).
- **41 mechanistic submodels** exportable to SBML L3v2, CellML 2.0 (with 1.1 fallback), and PhysioCell `<user_parameters>`. Four are Phase-C hypothesis-only models that ship with explicit "DO NOT USE FOR PREDICTION" annotations.
- **One composed pregnancy SBML model** wiring all submodels via a shared gestational-time axis.
- **COMBINE archive** (`.omex`) bundling SBML + CellML + PhysioCell + provenance metadata.

See [docs/specs/v0.4/00-overview.md](docs/specs/v0.4/00-overview.md) for the v0.4 design and [docs/specs/v0.4/04-exhaustive-parameter-catalog.md](docs/specs/v0.4/04-exhaustive-parameter-catalog.md) for the full ceiling — every parameter the project could honestly include given the available literature.

## What nidus is

- A **JSON dataset** under [dataset/](dataset/), schema-validated and machine-readable.
- A **Python package** that loads, filters, queries, and exports the dataset.
- A **Streamlit dashboard** for non-coders to browse parameters, citations, and trajectories.
- A **suite of mechanistic-modeling exports** (SBML / CellML / PhysioCell / COMBINE) so the dataset can be consumed directly inside the simulators researchers already use.
- A **citable artifact** — every release gets a Zenodo DOI.

## What nidus is NOT

- **Not a clinical decision-support tool.** Not validated for any decision affecting a real patient.
- **Not a mechanistic simulator.** Nidus exports parameters *into* the simulators ([CellML](https://www.cellml.org/), [COPASI](http://copasi.org/), [PhysioCell](http://physicell.org/), [tellurium](https://tellurium.analogmachine.org/)). It does not integrate ODEs itself.
- **Not an automated medical researcher.** Humans verify every parameter and every citation. LLMs help but do not promote `unverified` to `verified` on their own authority.
- **Not exhaustive.** The declared-scope ceiling enumerated in the [exhaustive parameter catalog](docs/specs/v0.4/04-exhaustive-parameter-catalog.md) has been reached (every catalog row is now `shipped`). Further growth means parameters not yet enumerated — open an issue if you find one that fits the envelope (normal physiology, human, 8–40w singleton).

## Quick start

```bash
pip install nidus                 # core: dataset + loader + CLI
pip install 'nidus[export]'       # adds python-libsbml + libcellml for SBML/CellML
pip install 'nidus[plot]'         # adds matplotlib for built-in trajectory plotting
```

### Load and query the dataset

```python
import nidus

ds = nidus.load()

co = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
print(co.value)                      # Value(central=4.5, low=4.0, high=5.0, units='L/min', ...)
print(co.tier)                       # "B"
print(co.primary_citation.doi)       # the DOI of the canonical source
print(co.extraction.review_status)   # "verified" or "unverified"
print(co.extraction.tier_rationale)  # the explicit reason the tier was assigned

# Filter
b_tier_renal = [p for p in ds if p.tier == "B" and p.subsystem == "maternal_renal"]
```

### Mechanistic-modeling exports

```bash
# One SBML file per submodel
nidus export --format sbml --output exports/sbml

# CellML 2.0 (or 1.1 fallback for legacy tools)
nidus export --format cellml --output exports/cellml
nidus export --format cellml --cellml-version 1.1 --output exports/cellml_1_1

# PhysioCell <user_parameters> drop-in
nidus export --format physiocell --output exports/physicell

# Single composed SBML model wiring all submodels together
nidus export --format composed --output exports/composed

# COMBINE archive bundling everything (.omex)
nidus export --format omex --output exports/nidus.omex
```

### Browse the dashboard

```bash
streamlit run dashboard/app.py
```

Or use the hosted Streamlit Community Cloud deployment linked from the repo description.

## Subsystems

| Subsystem                  | What it covers                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| `maternal_cardiovascular`  | Cardiac output, MAP, SVR, uterine flow, stroke volume, heart rate trajectories.               |
| `maternal_blood`           | Plasma volume, RBC mass, haematocrit, O₂-Hb biophysics, clotting factors, fibrinogen, D-dimer.|
| `maternal_renal`           | GFR, RPF, plasma creatinine/urea/uric acid, sodium/osmolality, urinary protein.               |
| `maternal_respiratory`     | Minute ventilation, tidal volume, PaO₂/PaCO₂, FRC, A-a gradient.                              |
| `maternal_endocrine`       | Cortisol, prolactin, aldosterone, free T4, TSH, insulin sensitivity.                          |
| `placental_structure`      | Villous surface area, weight, cord length, intervillous volume, spiral artery anatomy.        |
| `placental_gas_exchange`   | Intervillous PO₂/PCO₂, diffusing capacity, umbilical-vein/artery gas tensions.                |
| `placental_glucose`        | GLUT1/GLUT3 kinetics, maternal-fetal glucose gradient, transplacental flux.                   |
| `placental_endocrine`      | hCG, hPL, progesterone, estriol, relaxin trajectories.                                        |
| `fetal_circulation`        | Umbilical flow, combined ventricular output, MCA Doppler, ductus venosus, fetal heart rate.   |
| `fetal_growth`             | BPD, HC, AC, FL, EFW at 4-week intervals (NICHD cohort, Hadlock biometry).                    |
| `fetal_metabolism`         | Fetal pH, lactate, glucose, P50 of HbF, fetal cortisol, urine output.                         |
| `amniotic_fluid`           | AFV trajectory, composition (glucose, lactate, creatinine, osmolality).                       |

## Exportable mechanistic submodels

| Submodel id                            | Equation                                                     | Tier driver                |
| -------------------------------------- | ------------------------------------------------------------ | -------------------------- |
| `placental_villous_growth`             | Logistic surface-area expansion                              | placental_structure        |
| `o2hb_dissociation_adult`              | Severinghaus 1979 algebraic saturation                       | maternal_blood             |
| `o2hb_dissociation_fetal`              | Hill-form fetal HbF (Bauer 1969, P50≈19.5 mmHg)              | fetal_metabolism           |
| `placental_glucose_glut1`              | Michaelis–Menten (lower-affinity, higher-Vmax isoform)       | placental_glucose          |
| `placental_glucose_glut3`              | Michaelis–Menten (higher-affinity isoform)                   | placental_glucose          |
| `maternal_cardiac_output_trajectory`   | Gaussian bump (Mahendru 2014 longitudinal fit)               | maternal_cardiovascular    |
| `maternal_map_trajectory`              | Gaussian nadir mid-pregnancy                                 | maternal_cardiovascular    |
| `uterine_artery_flow_logistic`         | Logistic growth, inflection at 24 weeks (Thaler 1990)        | maternal_cardiovascular    |
| `placental_o2_equilibrator`            | Algebraic intervillous → umbilical-vein PO₂ equilibrium      | placental_gas_exchange     |
| `plasma_volume_expansion`              | Sigmoidal (Bernstein 2001 + de Haas 2017 anchors)            | maternal_blood             |
| `hadlock_fetal_weight`                 | Hadlock 1991 four-parameter biometry regression              | fetal_growth               |
| `gfr_logistic_trajectory`              | Logistic GFR rise to ~150 mL/min plateau (Conrad 2001)       | maternal_renal             |
| `amniotic_fluid_volume_trajectory`     | Gaussian-bump approximation to Brace & Wolf 1989 curve       | amniotic_fluid             |
| `svr_trajectory`                       | Derived SVR(t) = MAP(t)·80 / CO(t) (Sanghavi 2014)           | maternal_cardiovascular    |
| `pao2_trajectory_linear`               | Linear PaO₂ rise (Templeton & Kelman 1976, Hegewald 2011)    | maternal_respiratory       |
| `tidal_volume_trajectory`              | Sigmoidal VT rise (LoMauro 2015, Hegewald 2011)              | maternal_respiratory       |
| `heart_rate_trajectory`                | Sigmoidal HR rise from baseline to term (Mahendru 2014)      | maternal_cardiovascular    |
| `stroke_volume_trajectory`             | Gaussian bump co-peaking with CO (Mahendru 2014)             | maternal_cardiovascular    |
| `renal_plasma_flow_trajectory`         | Gaussian bell-shape with mid-pregnancy peak (Dunlop 1981)    | maternal_renal             |
| `minute_ventilation_trajectory`        | Derived VE(t) = VT(t)·RR(t) (LoMauro 2015, Hegewald 2011)    | maternal_respiratory       |
| `arterial_ph_trajectory`               | Linear pH rise from baseline to term (Templeton 1976)        | maternal_respiratory       |
| `hadlock_bpd_growth`                   | Cubic fit to Hadlock 1982 BPD weekly anchors                 | fetal_growth               |
| `hadlock_hc_growth`                    | Cubic fit to Hadlock 1982 HC weekly anchors                  | fetal_growth               |
| `hadlock_ac_growth`                    | Cubic fit to Hadlock 1982 AC weekly anchors                  | fetal_growth               |
| `hadlock_fl_growth`                    | Cubic fit to Hadlock 1982 FL weekly anchors                  | fetal_growth               |
| `homa_ir_trajectory`                   | Sigmoidal insulin resistance rise (Catalano 1991)            | maternal_endocrine         |
| `tsh_trajectory`                       | Piecewise-linear T1 nadir → term recovery (Glinoer 1997)     | maternal_endocrine         |
| `cortisol_trajectory`                  | Sigmoidal total cortisol rise (Allolio 1990)                 | maternal_endocrine         |
| `hpl_trajectory`                       | Sigmoidal hPL rise from undetectable to term (Handwerger 2010) | placental_endocrine      |
| `progesterone_trajectory`              | Sigmoidal progesterone 10x rise (Tulchinsky 1972)            | placental_endocrine        |
| `estradiol_trajectory`                 | Sigmoidal estradiol ~100x rise (Tulchinsky 1972)             | placental_endocrine        |
| `fetal_heart_rate_trajectory`          | Sigmoidal FHR fall from T1 peak to term (Pildner 2013)       | fetal_circulation          |
| `hcg_trajectory`                       | Piecewise quadratic rise then exponential decline (Cole 2010) | placental_endocrine       |
| `umbilical_artery_pi_trajectory`       | Sigmoidal UA-PI fall (Acharya 2005)                          | fetal_circulation          |
| `mca_pi_trajectory`                    | Gaussian bell-shape MCA-PI (Mari 1995)                       | fetal_circulation          |
| `cerebroplacental_ratio`               | Derived CPR = MCA-PI / UA-PI (Baschat 2003)                  | fetal_circulation          |
| `placental_fetal_allometry`            | PW = a·FW^b allometric scaling (Hutcheon 2012, Burton 2010)  | placental_structure        |
| `maternal_fetal_igg_transfer` ⚠️       | **HYPOTHESIS-ONLY** sigmoidal FcRn IgG transfer (Palmeira 2012) | placental_structure      |
| `placental_cortisol_gradient` ⚠️       | **HYPOTHESIS-ONLY** 11β-HSD2 inactivation (Benediktsson 1997) | placental_structure       |
| `maternal_microchimerism_trajectory` ⚠️ | **HYPOTHESIS-ONLY** sigmoidal fetal-cell accumulation (Bianchi 1996) | maternal_blood     |
| `fetal_pulmonary_fluid_trajectory` ⚠️  | **HYPOTHESIS-ONLY** sigmoidal lung-liquid secretion → reabsorption (Strang 1991) | fetal_metabolism |

**Phase A (12/12), Phase B (10/10), and Phase C (4/4)
hypothesis-only models are shipped.** Phase-C submodels use Tier-D
parameters reflecting qualitative published shape only; they emit a
`nidus:reviewStatus = "hypothesis-only"` annotation and a
"DO NOT USE FOR PREDICTION" warning in their SBML/CellML output, so
downstream consumers cannot accidentally treat them as predictive
models. See
[`docs/specs/v0.4/03-submodel-expansion-catalog.md`](docs/specs/v0.4/03-submodel-expansion-catalog.md) section 4.

Each submodel ships with a pure-NumPy reference kernel in [`python/nidus/export/reference.py`](python/nidus/export/reference.py) that the SBML/CellML exports are round-trip validated against.

## Confidence tiers

| Tier  | Meaning                                                                                                |
| ----- | ------------------------------------------------------------------------------------------------------ |
| A     | Well-established. ≥3 independent studies, overlapping CIs, mechanism understood, multiple populations. |
| B     | Supported. 1–2 longitudinal studies (n≥100), plausible mechanism, no strong contradicting evidence.    |
| C     | Provisional. Single study, or cross-sectional only, or small n; mechanism speculative.                 |
| D     | Unknown. Hypothesised channel; no quantitative literature; listed for research-question purposes.      |

When a submodel combines parameters of different tiers, **the worst input tier wins** (the submodel inherits the tier of its weakest input). Exported SBML / CellML / PhysioCell models carry this propagated tier as a `nidus:confidenceTier` RDF annotation.

## How to cite

Cite the dataset by its Zenodo concept DOI (added on first formal release). See [CITATION.cff](CITATION.cff) for machine-readable metadata. Every parameter also has its own underlying citation accessible via `parameter.primary_citation.doi` — when you use a single parameter, cite the dataset AND the primary source.

## Read more

- **[Essay — Confidence tiers for pregnancy physiology](docs/about/essay.md).** A ~2,500-word walkthrough of the design philosophy with the Mahendru-2014 cardiac-output parameter as a worked example. The clearest single explanation of what the dataset is and why the tier system is the load-bearing piece.
- **[v0.3 design spec](docs/specs/v0.3/00-overview.md)** — the dataset-and-dashboard rationale.
- **[v0.4 design spec](docs/specs/v0.4/00-overview.md)** — the mechanistic-modeling interop direction.
- **[v0.4 mechanistic interop spec](docs/specs/v0.4/01-mechanistic-modeling-interop.md)** — per-format model design, annotations, validation strategy.
- **[v0.4 parameter expansion roadmap](docs/specs/v0.4/02-parameter-expansion-roadmap.md)** — phased expansion plan.
- **[v0.4 submodel expansion catalog](docs/specs/v0.4/03-submodel-expansion-catalog.md)** — additional mechanistic submodels.
- **[v0.4 exhaustive parameter catalog](docs/specs/v0.4/04-exhaustive-parameter-catalog.md)** — the project's ceiling: every parameter the literature supports, every citation, every explicit exclusion.
- **[`docs/about/history.md`](docs/about/history.md)** — how the project got here (the project began as a Rust prototype, preserved at the `v0.2-archive` tag).
- **[PhysioCell tissue example](docs/examples/physicell_placental_villous/)** — a 2D placental-villous slice showing the canonical nidus→PhysiCell parameter pattern.

## Licence

- **Code:** MIT. See [LICENSE](LICENSE).
- **Dataset:** CC-BY-4.0. See [LICENSE-DATASET](LICENSE-DATASET). Each parameter entry is data; attribution required, no other restrictions.

## Contributing

The most valuable contributions are verified parameters drawn from published empirical work. See [CONTRIBUTING.md](CONTRIBUTING.md) for the tier system, the review checklist, the citation-verification workflow, and the parameter-addition issue template.

The single highest-leverage contribution today is promoting `unverified` parameters to `verified` by reading the source PDF and confirming (or correcting) the dataset entry.
