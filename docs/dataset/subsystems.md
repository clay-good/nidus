# Subsystems

Parameters are partitioned across ten subsystems mirroring the conventional anatomical / physiological structure of the maternal–placental–fetal unit.

| Subsystem                  | What it covers                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| `maternal_cardiovascular`  | Cardiac output, mean arterial pressure, uterine artery flow, vascular adaptation trajectories.  |
| `maternal_blood`           | Plasma volume, red-cell mass, haemoglobin, O₂–Hb dissociation, blood viscosity.                  |
| `maternal_respiratory`     | Tidal volume, minute ventilation, alveolar gas tensions, dead-space adjustments.                |
| `maternal_renal`           | GFR, plasma flow, sodium handling.                                                              |
| `placental_structure`      | Villous surface area, mass, branching, syncytial / cytotrophoblast composition.                 |
| `placental_gas_exchange`   | O₂ and CO₂ transfer kinetics across the placental barrier.                                       |
| `placental_glucose`        | GLUT1 / GLUT3 transport kinetics, Km, Vmax, glucose flux.                                       |
| `fetal_circulation`        | Shunt routing (foramen ovale, ductus arteriosus), umbilical artery and vein flow.               |
| `fetal_growth`             | Estimated fetal weight, biparietal diameter, femur length, abdominal circumference.             |
| `fetal_metabolism`         | Oxygen consumption, glucose utilisation, anaerobic metabolism markers.                          |

## Coverage at v0.3.0

Mostly maternal-cardiovascular and fetal-growth-heavy, with thin coverage of placental endocrinology and fetal metabolism — a reasonable honest snapshot of where pregnancy physiology has the strongest published evidence base.

| Subsystem                  | Parameters | Modal tier |
| -------------------------- | ---------- | ---------- |
| `maternal_cardiovascular`  | 14         | B          |
| `maternal_blood`           |  9         | A          |
| `fetal_growth`             |  7         | A          |
| `maternal_respiratory`     |  5         | A          |
| `placental_structure`      |  5         | B          |
| `placental_glucose`        |  4         | B          |
| `maternal_renal`           |  3         | A          |
| `fetal_circulation`        |  3         | C          |
| `placental_gas_exchange`   |  2         | C          |
| `fetal_metabolism`         |  2         | B          |

## Conspicuously absent

These subsystems are deliberately out of scope for v0.3:

- **Maternal immune** — quantitative tolerance / rejection markers are mostly Tier D in the current literature.
- **Placental endocrinology** — hCG, progesterone, lactogen trajectories exist in the literature but were not curated in the v0.2 corpus.
- **Embryonic period (< 8 weeks)** — physiology is qualitatively different; out of scope.
- **Labour and delivery** — out of scope; a substantial modelling problem in its own right.
- **Twin / higher-order pregnancies** — out of scope; would require its own dataset partition.

Contributions extending coverage in these areas are welcome via the [parameter-request issue template](https://github.com/claygood/nidus/issues/new?template=parameter-request.yml) once the contributor has done the underlying citation work.
