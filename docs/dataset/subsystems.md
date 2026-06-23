# Subsystems

Parameters are partitioned across thirteen subsystems mirroring the conventional anatomical / physiological structure of the maternal–placental–fetal unit.

| Subsystem                  | What it covers                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| `maternal_cardiovascular`  | Cardiac output, mean arterial pressure, uterine artery flow, vascular adaptation trajectories.  |
| `maternal_blood`           | Plasma volume, red-cell mass, haemoglobin, O₂–Hb dissociation, coagulation / fibrinolysis.       |
| `maternal_respiratory`     | Tidal volume, minute ventilation, alveolar gas tensions, dead-space adjustments.                |
| `maternal_renal`           | GFR, renal plasma flow, sodium and osmolar handling.                                            |
| `maternal_endocrine`       | Cortisol, thyroid, prolactin, renin–aldosterone and sex-steroid trajectories.                   |
| `placental_structure`      | Villous surface area, mass, branching, syncytial / cytotrophoblast composition.                 |
| `placental_gas_exchange`   | O₂ and CO₂ transfer kinetics across the placental barrier.                                       |
| `placental_glucose`        | GLUT1 / GLUT3 transport kinetics, Km, Vmax, glucose flux.                                       |
| `placental_endocrine`      | hCG, progesterone, placental lactogen, relaxin and placental-GH trajectories.                   |
| `fetal_circulation`        | Shunt routing (foramen ovale, ductus arteriosus), umbilical and middle-cerebral-artery flow.    |
| `fetal_growth`             | Estimated fetal weight, biparietal diameter, femur length, abdominal circumference.             |
| `fetal_metabolism`         | Oxygen consumption, glucose utilisation, cortisol, anaerobic metabolism markers.                |
| `amniotic_fluid`           | Amniotic fluid volume trajectory, fetal swallowing and urine production, turnover.              |

## Coverage

Fetal-growth, maternal-blood, and maternal-cardiovascular heavy, thinning toward placental glucose transport and gas exchange — a reasonable honest snapshot of where pregnancy physiology has the strongest published evidence base.

| Subsystem                  | Parameters | Modal tier |
| -------------------------- | ---------- | ---------- |
| `fetal_growth`             | 36         | A          |
| `maternal_blood`           | 34         | B          |
| `maternal_cardiovascular`  | 33         | B          |
| `placental_structure`      | 20         | C          |
| `maternal_renal`           | 19         | B          |
| `fetal_circulation`        | 18         | B          |
| `maternal_respiratory`     | 18         | B          |
| `fetal_metabolism`         | 14         | B          |
| `placental_endocrine`      | 13         | B          |
| `amniotic_fluid`           | 11         | B          |
| `maternal_endocrine`       | 11         | B          |
| `placental_gas_exchange`   | 10         | C          |
| `placental_glucose`        |  6         | B          |

## Conspicuously absent

These subsystems are deliberately out of scope:

- **Maternal immune** — quantitative tolerance / rejection markers are mostly Tier D in the current literature.
- **Maternal hepatic / gastrointestinal** — bile-acid and transaminase trajectories are sparse and mostly disease-anchored.
- **Embryonic period (< 8 weeks)** — physiology is qualitatively different; out of scope.
- **Labour and delivery** — out of scope; a substantial modelling problem in its own right.
- **Twin / higher-order pregnancies** — out of scope; would require its own dataset partition.

Contributions extending coverage in these areas are welcome via the [parameter-request issue template](https://github.com/clay-good/nidus/issues/new?template=parameter-request.yml) once the contributor has done the underlying citation work.
