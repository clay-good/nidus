#!/usr/bin/env python3
"""One-shot expansion script for the v0.4 Phase 1 + Phase 2 dataset growth.

Adds new citations and parameters consistent with
docs/specs/v0.4/02-parameter-expansion-roadmap.md and
docs/specs/v0.4/04-exhaustive-parameter-catalog.md.

Idempotent: re-running does nothing if the entries already exist.

The values are extracted from the literature consensus values
documented in the catalog spec. Each new parameter ships with
review_status='unverified' and a tier_rationale referencing the
primary source. A human curator promotes to 'verified' after PDF
re-check.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / "dataset"


# ---- New citations -------------------------------------------------

NEW_CITATIONS = {
    "conrad-2001-relaxin-gfr": {
        "key": "conrad-2001-relaxin-gfr",
        "type": "journal-article",
        "authors": ["Conrad KP"],
        "title": "Mechanisms of renal vasodilation and hyperfiltration during pregnancy",
        "journal": "Journal of the Society for Gynecologic Investigation",
        "year": 2001,
        "pmid": "11489744",
        "notes": "Mechanistic review: relaxin-mediated systemic and renal vasodilation; ~50% GFR rise.",
    },
    "dunlop-1981-renal-plasma-flow": {
        "key": "dunlop-1981-renal-plasma-flow",
        "type": "journal-article",
        "authors": ["Dunlop W"],
        "title": "Serial changes in renal haemodynamics during normal human pregnancy",
        "journal": "British Journal of Obstetrics and Gynaecology",
        "year": 1981,
        "pmid": "7259294",
        "notes": "Foundational longitudinal RPF/GFR study; basis for the bell-shaped RPF trajectory.",
    },
    "davison-1981-osmoregulation": {
        "key": "davison-1981-osmoregulation",
        "type": "journal-article",
        "authors": ["Davison JM", "Vallotton MB", "Lindheimer MD"],
        "title": "Plasma osmolality and urinary concentration and dilution during and after pregnancy",
        "journal": "British Journal of Obstetrics and Gynaecology",
        "year": 1981,
        "pmid": "7195807",
        "notes": "Foundational reference for the ~10 mOsm/kg osmolality drop and the ~5 mEq/L plasma sodium drop.",
    },
    "pitkin-1979-wbc": {
        "key": "pitkin-1979-wbc",
        "type": "journal-article",
        "authors": ["Pitkin RM", "Witte DL"],
        "title": "Platelet and leukocyte counts in pregnancy",
        "journal": "JAMA",
        "year": 1979,
        "pmid": "430872",
        "notes": "Reference values for WBC and platelets in pregnancy.",
    },
    "kline-2005-d-dimer": {
        "key": "kline-2005-d-dimer",
        "type": "journal-article",
        "authors": ["Kline JA", "Williams GW", "Hernandez-Nino J"],
        "title": "D-dimer concentrations in normal pregnancy: new diagnostic thresholds are needed",
        "journal": "Clinical Chemistry",
        "year": 2005,
        "pmid": "15764641",
        "notes": "D-dimer values across trimesters; basis for adjusted thresholds in VTE workup.",
    },
    "larsson-2008-serum-proteins": {
        "key": "larsson-2008-serum-proteins",
        "type": "journal-article",
        "authors": ["Larsson A", "Palm M", "Hansson LO", "Axelsson O"],
        "title": "Reference values for clinical chemistry tests during normal pregnancy",
        "journal": "BJOG",
        "year": 2008,
        "doi": "10.1111/j.1471-0528.2008.01709.x",
        "notes": "Reference intervals for serum proteins across pregnancy.",
    },
    "carr-1981-cortisol": {
        "key": "carr-1981-cortisol",
        "type": "journal-article",
        "authors": ["Carr BR", "Parker CR", "Madden JD", "MacDonald PC", "Porter JC"],
        "title": "Maternal plasma adrenocorticotropin and cortisol relationships throughout human pregnancy",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 1981,
        "pmid": "6258437",
        "notes": "Longitudinal ACTH/cortisol/CBG across pregnancy.",
    },
    "glinoer-1997-thyroid": {
        "key": "glinoer-1997-thyroid",
        "type": "journal-article",
        "authors": ["Glinoer D"],
        "title": "The regulation of thyroid function in pregnancy: pathways of endocrine adaptation from physiology to pathology",
        "journal": "Endocrine Reviews",
        "year": 1997,
        "pmid": "9183568",
        "notes": "Canonical review of thyroid axis adaptation; TSH suppression in T1 by hCG.",
    },
    "tyson-1972-prolactin": {
        "key": "tyson-1972-prolactin",
        "type": "journal-article",
        "authors": ["Tyson JE", "Hwang P", "Guyda H", "Friesen HG"],
        "title": "Studies of prolactin secretion in human pregnancy",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 1972,
        "pmid": "4621291",
        "notes": "Foundational prolactin-in-pregnancy reference.",
    },
    "wilson-1980-renin-aldosterone": {
        "key": "wilson-1980-renin-aldosterone",
        "type": "journal-article",
        "authors": ["Wilson M", "Morganti AA", "Zervoudakis I", "Letcher RL", "Romney BM", "Von Oeyon P", "Papera S", "Sealey JE", "Laragh JH"],
        "title": "Blood pressure, the renin-aldosterone system and sex steroids throughout normal pregnancy",
        "journal": "American Journal of Medicine",
        "year": 1980,
        "pmid": "6986818",
        "notes": "Longitudinal renin/aldosterone reference across pregnancy.",
    },
    "catalano-1991-insulin-sensitivity": {
        "key": "catalano-1991-insulin-sensitivity",
        "type": "journal-article",
        "authors": ["Catalano PM", "Tyzbir ED", "Roman NM", "Amini SB", "Sims EA"],
        "title": "Longitudinal changes in insulin release and insulin resistance in nonobese pregnant women",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 1991,
        "pmid": "1951519",
        "notes": "Insulin sensitivity (HOMA-IR-equivalent) falls ~50% in late pregnancy.",
    },
    "cole-2010-hcg": {
        "key": "cole-2010-hcg",
        "type": "journal-article",
        "authors": ["Cole LA"],
        "title": "Biological functions of hCG and hCG-related molecules",
        "journal": "Reproductive Biology and Endocrinology",
        "year": 2010,
        "doi": "10.1186/1477-7827-8-102",
        "pmid": "20735820",
        "notes": "hCG kinetics: peak ~10 weeks, decline to ~10,000 mIU/mL at term.",
    },
    "tulchinsky-1972-steroids": {
        "key": "tulchinsky-1972-steroids",
        "type": "journal-article",
        "authors": ["Tulchinsky D", "Hobel CJ", "Yeager E", "Marshall JR"],
        "title": "Plasma estrone, estradiol, estriol, progesterone, and 17-hydroxyprogesterone in human pregnancy",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 1972,
        "pmid": "5078134",
        "notes": "Foundational longitudinal steroid hormone profile across pregnancy.",
    },
    "handwerger-2010-hpl": {
        "key": "handwerger-2010-hpl",
        "type": "journal-article",
        "authors": ["Handwerger S"],
        "title": "The physiology of placental lactogen in human pregnancy",
        "journal": "Endocrine Reviews",
        "year": 1991,
        "pmid": "1935823",
        "notes": "hPL physiology review; rises linearly through gestation, ~5-10 ug/mL at term.",
    },
    "brace-1989-amniotic-fluid": {
        "key": "brace-1989-amniotic-fluid",
        "type": "journal-article",
        "authors": ["Brace RA", "Wolf EJ"],
        "title": "Normal amniotic fluid volume changes throughout pregnancy",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 1989,
        "pmid": "2782359",
        "notes": "Reference AFV trajectory: rises through 32-34 weeks, peaks ~800 mL, declines toward term.",
    },
    "kiserud-2001-umbilical-vein": {
        "key": "kiserud-2001-umbilical-vein",
        "type": "journal-article",
        "authors": ["Kiserud T", "Rasmussen S", "Skulstad S"],
        "title": "Blood flow and the degree of shunting through the ductus venosus in the human fetus",
        "journal": "American Journal of Obstetrics and Gynecology",
        "year": 2000,
        "pmid": "10739512",
        "notes": "Umbilical vein flow Doppler reference; DV shunt fraction ~30% at term.",
    },
    "rudolph-1985-fetal-circulation": {
        "key": "rudolph-1985-fetal-circulation",
        "type": "journal-article",
        "authors": ["Rudolph AM"],
        "title": "Distribution and regulation of blood flow in the fetal and neonatal lamb",
        "journal": "Circulation Research",
        "year": 1985,
        "pmid": "3893852",
        "notes": "Canonical fetal-circulation distribution reference. Sheep model; human values inferred and consistent with subsequent Doppler studies. Mixed-species citation noted.",
    },
    "von-steinburg-2013-fhr": {
        "key": "von-steinburg-2013-fhr",
        "type": "journal-article",
        "authors": ["Pildner von Steinburg S", "Boulesteix AL", "Lederer C", "Grunow S", "Schiermeier S", "Hatzmann W", "Schneider KT", "Daumer M"],
        "title": "What is the normal fetal heart rate?",
        "journal": "PeerJ",
        "year": 2013,
        "doi": "10.7717/peerj.82",
        "pmid": "23761161",
        "notes": "Longitudinal FHR reference: ~170 bpm in T1 falling to ~140 bpm at term.",
    },
    "templeton-1976-blood-gas": {
        "key": "templeton-1976-blood-gas",
        "type": "journal-article",
        "authors": ["Templeton A", "Kelman GR"],
        "title": "Maternal blood-gases, PAo2-Pao2, hysiological shunt and VD/VT in normal pregnancy",
        "journal": "British Journal of Anaesthesia",
        "year": 1976,
        "pmid": "1247088",
        "notes": "Reference for non-pregnant and pregnant PaO2, PaCO2, A-a gradient.",
    },
}


# ---- Helper builders ----------------------------------------------


def param(
    *,
    pid: str,
    name: str,
    subsystem: str,
    central: float,
    low: float | None,
    high: float | None,
    units: str,
    tier: str,
    rationale: str,
    citation_keys: list[str],
    primary: str | None = None,
    notes: str | None = None,
    population: str | None = None,
    distribution: str = "normal",
    ci: float = 0.683,
) -> dict:
    value: dict = {"central": central, "units": units}
    if low is not None:
        value["low"] = low
    if high is not None:
        value["high"] = high
    if distribution:
        value["distribution"] = distribution
    if ci is not None and low is not None:
        value["ci"] = ci
    rec = {
        "id": pid,
        "name": name,
        "subsystem": subsystem,
        "value": value,
        "tier": tier,
        "tier_rationale": rationale,
        "citations": citation_keys,
        "extraction": {
            "review_status": "unverified",
            "date": "2026-05-22",
            "reviewer": "v0.4-phase1-expansion-script",
        },
    }
    if primary or citation_keys:
        rec["primary_citation"] = primary or citation_keys[0]
    if population:
        rec["applicability"] = {"population": population}
    if notes:
        rec["notes"] = notes
    return rec


# ---- New parameter records -----------------------------------------


# Fetal growth: multi-week biometry from Buck Louis 2015 / Hadlock 1991.
# 50th-percentile values; CIs approximated from cohort variability.
BIOMETRY = {
    # (week, metric): (central, low, high)
    "bpd": {  # mm
        16: (35.0, 32.5, 37.5),
        20: (47.0, 44.0, 50.0),
        24: (61.0, 58.0, 64.0),
        32: (82.0, 78.5, 85.5),
        36: (89.0, 85.0, 93.0),
        40: (93.0, 89.0, 97.0),
    },
    "hc": {  # mm
        16: (124.0, 117.0, 131.0),
        20: (175.0, 167.0, 183.0),
        24: (225.0, 215.0, 235.0),
        28: (267.0, 256.0, 278.0),
        32: (297.0, 285.0, 309.0),
        36: (322.0, 309.0, 335.0),
        40: (343.0, 329.0, 357.0),
    },
    "ac": {  # mm
        16: (105.0, 98.0, 112.0),
        20: (152.0, 143.0, 161.0),
        24: (198.0, 187.0, 209.0),
        28: (240.0, 227.0, 253.0),
        32: (282.0, 267.0, 297.0),
        36: (322.0, 305.0, 339.0),
        40: (354.0, 335.0, 373.0),
    },
    "fl": {  # mm
        16: (21.0, 19.0, 23.0),
        20: (33.0, 31.0, 35.0),
        24: (44.0, 41.5, 46.5),
        32: (62.0, 59.0, 65.0),
        36: (70.0, 67.0, 73.0),
        40: (76.0, 72.5, 79.5),
    },
    "efw": {  # grams; weeks not already shipped: 16, 24, 32
        16: (145.0, 130.0, 160.0),
        24: (650.0, 590.0, 715.0),
        32: (1800.0, 1640.0, 1965.0),
    },
}

METRIC_LONG = {
    "bpd": "Biparietal diameter",
    "hc": "Head circumference",
    "ac": "Abdominal circumference",
    "fl": "Femur length",
    "efw": "Estimated fetal weight",
}


def biometry_params() -> list[dict]:
    out: list[dict] = []
    for metric, weeks in BIOMETRY.items():
        units = "g" if metric == "efw" else "mm"
        for week, (c, lo, hi) in weeks.items():
            pid = f"fetal_growth.{metric}_{week}w_{units.replace('/', '_per_')}" if metric == "efw" else f"fetal_growth.{metric}_{week}w_mm"
            # Match existing naming convention
            pid = f"fetal_growth.{metric}_{week}w_g" if metric == "efw" else f"fetal_growth.{metric}_{week}w_mm"
            out.append(param(
                pid=pid,
                name=f"{METRIC_LONG[metric]} at {week} weeks",
                subsystem="fetal_growth",
                central=c, low=lo, high=hi, units=units,
                tier="A",
                rationale=(
                    "Tier A from Buck Louis 2015 NICHD Fetal Growth Studies "
                    "(n=2334 low-risk singletons; longitudinal ultrasound, "
                    "Voluson E8). 50th-percentile pooled-cohort value at this "
                    "gestational age. Hadlock 1991 provides the underlying "
                    "biometry-to-weight regression. PDF re-verification of "
                    f"the specific {METRIC_LONG[metric].lower()} percentile pending."
                ),
                citation_keys=["buck-louis-2015-nichd-growth", "hadlock-1991-fetal-weight"],
                primary="buck-louis-2015-nichd-growth",
                population="NICHD Fetal Growth Studies singleton cohort",
                notes=(
                    f"{METRIC_LONG[metric]} 50th-percentile pooled value at "
                    f"week {week}. Provenance against Buck Louis 2015 source "
                    "tables needs human re-verification."
                ),
            ))
    return out


def mat_cardio_params() -> list[dict]:
    return [
        param(
            pid="maternal_cardiovascular.baseline_heart_rate_bpm",
            name="Maternal baseline heart rate",
            subsystem="maternal_cardiovascular",
            central=70.0, low=60.0, high=80.0, units="bpm",
            tier="A",
            rationale=(
                "Tier A from Mahendru 2014 cohort: pre-pregnancy resting HR "
                "is well-characterised at ~70 bpm in healthy nulliparous "
                "women; multiple independent studies converge."
            ),
            citation_keys=["mahendru-2014-cardiac-output"],
        ),
        param(
            pid="maternal_cardiovascular.peak_excess_heart_rate_bpm",
            name="Heart rate rise from baseline to term",
            subsystem="maternal_cardiovascular",
            central=15.0, low=10.0, high=20.0, units="bpm",
            tier="A",
            rationale=(
                "Tier A from Mahendru 2014: HR rises ~15 bpm over gestation, "
                "peaks late T3; replicated across Sanghavi 2014 review."
            ),
            citation_keys=["mahendru-2014-cardiac-output", "sanghavi-rutherford-2014-cardio-review"],
            primary="mahendru-2014-cardiac-output",
        ),
        param(
            pid="maternal_cardiovascular.baseline_stroke_volume_ml",
            name="Maternal baseline stroke volume",
            subsystem="maternal_cardiovascular",
            central=70.0, low=60.0, high=80.0, units="mL",
            tier="B",
            rationale=(
                "Tier B from Sanghavi 2014 review synthesis of multiple "
                "echocardiographic studies: non-pregnant SV ~65-75 mL in "
                "healthy nulliparous women."
            ),
            citation_keys=["sanghavi-rutherford-2014-cardio-review"],
        ),
        param(
            pid="maternal_cardiovascular.peak_excess_stroke_volume_ml",
            name="Stroke volume rise from baseline to peak",
            subsystem="maternal_cardiovascular",
            central=15.0, low=10.0, high=20.0, units="mL",
            tier="B",
            rationale=(
                "Tier B from Sanghavi 2014: SV rises ~15-20 mL during "
                "pregnancy; the increment is the dominant driver of the CO "
                "rise in early-mid pregnancy."
            ),
            citation_keys=["sanghavi-rutherford-2014-cardio-review"],
        ),
        param(
            pid="maternal_cardiovascular.baseline_svr_dyn_s_cm5",
            name="Maternal non-pregnant systemic vascular resistance",
            subsystem="maternal_cardiovascular",
            central=1300.0, low=1100.0, high=1500.0, units="dyn*s/cm^5",
            tier="B",
            rationale=(
                "Tier B from Sanghavi 2014 review: non-pregnant SVR ~1200-1400 "
                "dyn*s/cm^5 in healthy women; computed as MAP*80/CO."
            ),
            citation_keys=["sanghavi-rutherford-2014-cardio-review"],
        ),
        param(
            pid="maternal_cardiovascular.term_svr_dyn_s_cm5",
            name="Maternal term systemic vascular resistance",
            subsystem="maternal_cardiovascular",
            central=980.0, low=850.0, high=1100.0, units="dyn*s/cm^5",
            tier="B",
            rationale=(
                "Tier B from Sanghavi 2014: SVR falls ~25% during pregnancy "
                "(systemic vasodilation); ~950-1000 dyn*s/cm^5 at term."
            ),
            citation_keys=["sanghavi-rutherford-2014-cardio-review"],
        ),
    ]


def mat_renal_params() -> list[dict]:
    return [
        param(
            pid="maternal_renal.baseline_gfr_ml_per_min",
            name="Maternal non-pregnant GFR",
            subsystem="maternal_renal",
            central=100.0, low=90.0, high=110.0, units="mL/min",
            tier="A",
            rationale=(
                "Tier A: non-pregnant GFR in healthy adult women is "
                "~100 mL/min; this is the textbook baseline against "
                "which the ~50% pregnancy rise is measured (Conrad 2001, "
                "Davison 1974, Cheung 2013 review)."
            ),
            citation_keys=["conrad-2001-relaxin-gfr", "davison-hytten-1974-gfr", "cheung-lafayette-2013-renal"],
            primary="conrad-2001-relaxin-gfr",
        ),
        param(
            pid="maternal_renal.gfr_peak_week",
            name="Gestational week of peak GFR",
            subsystem="maternal_renal",
            central=16.0, low=12.0, high=24.0, units="weeks",
            tier="B",
            rationale=(
                "Tier B from Conrad 2001 mechanistic review and Dunlop 1981 "
                "longitudinal data: GFR peaks ~T1/early T2 driven by relaxin-"
                "mediated renal vasodilation."
            ),
            citation_keys=["conrad-2001-relaxin-gfr", "dunlop-1981-renal-plasma-flow"],
            primary="conrad-2001-relaxin-gfr",
        ),
        param(
            pid="maternal_renal.gfr_logistic_rate_per_week",
            name="Logistic GFR rise rate",
            subsystem="maternal_renal",
            central=0.4, low=0.25, high=0.6, units="1/week",
            tier="C",
            rationale=(
                "Tier C: empirical logistic-fit rate to Conrad 2001 / "
                "Dunlop 1981 trajectories. Single-fit value, no "
                "independent meta-analytic confirmation."
            ),
            citation_keys=["conrad-2001-relaxin-gfr"],
        ),
        param(
            pid="maternal_renal.renal_plasma_flow_baseline_ml_per_min",
            name="Maternal non-pregnant renal plasma flow",
            subsystem="maternal_renal",
            central=600.0, low=500.0, high=700.0, units="mL/min",
            tier="B",
            rationale=(
                "Tier B from Dunlop 1981 longitudinal cohort: non-pregnant "
                "RPF ~600 mL/min."
            ),
            citation_keys=["dunlop-1981-renal-plasma-flow"],
        ),
        param(
            pid="maternal_renal.renal_plasma_flow_peak_ml_per_min",
            name="Maternal peak renal plasma flow",
            subsystem="maternal_renal",
            central=900.0, low=750.0, high=1050.0, units="mL/min",
            tier="B",
            rationale=(
                "Tier B from Dunlop 1981: RPF peaks ~50-70% above baseline "
                "in T2, declines somewhat by term."
            ),
            citation_keys=["dunlop-1981-renal-plasma-flow"],
        ),
        param(
            pid="maternal_renal.rpf_peak_week",
            name="Week of peak renal plasma flow",
            subsystem="maternal_renal",
            central=24.0, low=20.0, high=28.0, units="weeks",
            tier="B",
            rationale=(
                "Tier B from Dunlop 1981: RPF peak ~24 weeks; the "
                "bell-shaped trajectory falls toward term."
            ),
            citation_keys=["dunlop-1981-renal-plasma-flow"],
        ),
        param(
            pid="maternal_renal.filtration_fraction_term",
            name="Filtration fraction at term",
            subsystem="maternal_renal",
            central=0.18, low=0.16, high=0.20, units="dimensionless",
            tier="B",
            rationale=(
                "Tier B from Cheung 2013 review: FF drops in mid-pregnancy "
                "(RPF rises faster than GFR) then partly recovers; ~0.18 "
                "at term."
            ),
            citation_keys=["cheung-lafayette-2013-renal", "dunlop-1981-renal-plasma-flow"],
            primary="cheung-lafayette-2013-renal",
        ),
        param(
            pid="maternal_renal.plasma_osmolality_drop_mosm_per_kg",
            name="Plasma osmolality drop from baseline",
            subsystem="maternal_renal",
            central=10.0, low=8.0, high=12.0, units="mOsm/kg",
            tier="A",
            rationale=(
                "Tier A from Davison 1981: plasma osmolality falls ~10 "
                "mOsm/kg in early pregnancy and remains low through term. "
                "Well-replicated; the osmotic-threshold-reset is the "
                "underlying mechanism."
            ),
            citation_keys=["davison-1981-osmoregulation"],
        ),
        param(
            pid="maternal_renal.plasma_sodium_drop_meq_per_l",
            name="Plasma sodium drop from baseline",
            subsystem="maternal_renal",
            central=5.0, low=3.0, high=7.0, units="mEq/L",
            tier="A",
            rationale=(
                "Tier A from Davison 1981: plasma sodium falls ~5 mEq/L "
                "in pregnancy, reflecting the osmolality reset."
            ),
            citation_keys=["davison-1981-osmoregulation"],
        ),
        param(
            pid="maternal_renal.bun_term_mg_per_dl",
            name="Blood urea nitrogen at term",
            subsystem="maternal_renal",
            central=8.0, low=6.0, high=11.0, units="mg/dL",
            tier="A",
            rationale=(
                "Tier A from Cheung 2013 review: BUN falls from ~13 mg/dL "
                "non-pregnant to ~8 mg/dL in pregnancy due to GFR rise + "
                "plasma volume expansion."
            ),
            citation_keys=["cheung-lafayette-2013-renal"],
        ),
    ]


def mat_resp_params() -> list[dict]:
    return [
        param(
            pid="maternal_respiratory.baseline_tidal_volume_ml",
            name="Maternal non-pregnant tidal volume",
            subsystem="maternal_respiratory",
            central=450.0, low=400.0, high=500.0, units="mL",
            tier="A",
            rationale=(
                "Tier A from LoMauro 2015 review: non-pregnant VT ~450 mL "
                "in healthy adult women; well-established."
            ),
            citation_keys=["lomauro-aliverti-2015-respiratory"],
        ),
        param(
            pid="maternal_respiratory.baseline_respiratory_rate_bpm",
            name="Maternal non-pregnant respiratory rate",
            subsystem="maternal_respiratory",
            central=16.0, low=12.0, high=20.0, units="breaths/min",
            tier="A",
            rationale=(
                "Tier A: non-pregnant adult RR ~12-20/min; LoMauro 2015 "
                "review confirms RR is approximately constant through pregnancy."
            ),
            citation_keys=["lomauro-aliverti-2015-respiratory"],
        ),
        param(
            pid="maternal_respiratory.term_respiratory_rate_bpm",
            name="Maternal term respiratory rate",
            subsystem="maternal_respiratory",
            central=16.0, low=12.0, high=20.0, units="breaths/min",
            tier="A",
            rationale=(
                "Tier A from LoMauro 2015: RR is essentially unchanged in "
                "pregnancy; the minute-ventilation rise is driven almost "
                "entirely by tidal volume."
            ),
            citation_keys=["lomauro-aliverti-2015-respiratory"],
        ),
        param(
            pid="maternal_respiratory.baseline_pao2_mmhg",
            name="Maternal non-pregnant arterial PO2",
            subsystem="maternal_respiratory",
            central=100.0, low=95.0, high=105.0, units="mmHg",
            tier="A",
            rationale=(
                "Tier A: non-pregnant PaO2 at sea level ~100 mmHg; "
                "Templeton & Kelman 1976 confirms the modest pregnancy rise."
            ),
            citation_keys=["templeton-1976-blood-gas", "lomauro-aliverti-2015-respiratory"],
            primary="templeton-1976-blood-gas",
        ),
        param(
            pid="maternal_respiratory.baseline_arterial_ph",
            name="Maternal non-pregnant arterial pH",
            subsystem="maternal_respiratory",
            central=7.40, low=7.38, high=7.42, units="dimensionless",
            tier="A",
            rationale=(
                "Tier A: non-pregnant arterial pH 7.40 ± 0.02; baseline "
                "against which the mild pregnancy alkalosis (pH ~7.44) is "
                "measured."
            ),
            citation_keys=["templeton-1976-blood-gas", "lomauro-aliverti-2015-respiratory"],
            primary="templeton-1976-blood-gas",
        ),
    ]


def mat_endocrine_params() -> list[dict]:
    return [
        param(
            pid="maternal_endocrine.cortisol_baseline_ug_per_dl",
            name="Maternal non-pregnant total plasma cortisol",
            subsystem="maternal_endocrine",
            central=10.0, low=5.0, high=20.0, units="ug/dL",
            tier="A",
            rationale=(
                "Tier A: non-pregnant morning plasma cortisol ~10 ug/dL "
                "(wide normal range 5-20). Carr 1981 baseline."
            ),
            citation_keys=["carr-1981-cortisol"],
        ),
        param(
            pid="maternal_endocrine.cortisol_term_ug_per_dl",
            name="Maternal term total plasma cortisol",
            subsystem="maternal_endocrine",
            central=30.0, low=25.0, high=40.0, units="ug/dL",
            tier="B",
            rationale=(
                "Tier B from Carr 1981: total cortisol rises ~3x by term, "
                "largely driven by CBG rise; free cortisol also rises "
                "modestly."
            ),
            citation_keys=["carr-1981-cortisol"],
        ),
        param(
            pid="maternal_endocrine.free_t4_term_ng_per_dl",
            name="Maternal free T4 at term",
            subsystem="maternal_endocrine",
            central=0.9, low=0.7, high=1.1, units="ng/dL",
            tier="B",
            rationale=(
                "Tier B from Glinoer 1997: free T4 falls slightly through "
                "gestation; total T4 rises (TBG-mediated)."
            ),
            citation_keys=["glinoer-1997-thyroid"],
        ),
        param(
            pid="maternal_endocrine.tsh_t1_miu_per_l",
            name="Maternal TSH in first trimester",
            subsystem="maternal_endocrine",
            central=0.6, low=0.1, high=2.5, units="mIU/L",
            tier="B",
            rationale=(
                "Tier B from Glinoer 1997: TSH suppressed in T1 by hCG "
                "cross-reactivity at the TSH receptor; recovers by T2/T3."
            ),
            citation_keys=["glinoer-1997-thyroid"],
        ),
        param(
            pid="maternal_endocrine.tsh_term_miu_per_l",
            name="Maternal TSH at term",
            subsystem="maternal_endocrine",
            central=2.0, low=0.4, high=4.0, units="mIU/L",
            tier="B",
            rationale=(
                "Tier B from Glinoer 1997: TSH recovers to within "
                "non-pregnant range by term."
            ),
            citation_keys=["glinoer-1997-thyroid"],
        ),
        param(
            pid="maternal_endocrine.prolactin_term_ng_per_ml",
            name="Maternal term plasma prolactin",
            subsystem="maternal_endocrine",
            central=200.0, low=150.0, high=300.0, units="ng/mL",
            tier="B",
            rationale=(
                "Tier B from Tyson 1972: prolactin rises ~10x by term to "
                "prime lactogenesis; estradiol-driven lactotroph hyperplasia."
            ),
            citation_keys=["tyson-1972-prolactin"],
        ),
        param(
            pid="maternal_endocrine.aldosterone_term_ng_per_dl",
            name="Maternal term plasma aldosterone",
            subsystem="maternal_endocrine",
            central=40.0, low=25.0, high=60.0, units="ng/dL",
            tier="B",
            rationale=(
                "Tier B from Wilson 1980: aldosterone rises ~5-10x by term, "
                "matching the cumulative sodium retention."
            ),
            citation_keys=["wilson-1980-renin-aldosterone"],
        ),
        param(
            pid="maternal_endocrine.homa_ir_baseline",
            name="Maternal non-pregnant HOMA-IR",
            subsystem="maternal_endocrine",
            central=2.0, low=1.0, high=3.0, units="dimensionless",
            tier="B",
            rationale=(
                "Tier B from Catalano 1991: pre-pregnancy HOMA-IR ~2.0 in "
                "non-obese women; baseline against which the ~50% rise is "
                "measured."
            ),
            citation_keys=["catalano-1991-insulin-sensitivity"],
        ),
        param(
            pid="maternal_endocrine.homa_ir_term",
            name="Maternal term HOMA-IR",
            subsystem="maternal_endocrine",
            central=4.0, low=2.5, high=6.0, units="dimensionless",
            tier="B",
            rationale=(
                "Tier B from Catalano 1991: insulin sensitivity falls ~50% "
                "by late T3; HOMA-IR roughly doubles. Placental hormones "
                "(hPL, progesterone, placental GH) drive insulin resistance."
            ),
            citation_keys=["catalano-1991-insulin-sensitivity"],
        ),
    ]


def placental_endocrine_params() -> list[dict]:
    return [
        param(
            pid="placental_endocrine.hcg_peak_miu_per_ml",
            name="Maternal serum hCG at peak",
            subsystem="placental_endocrine",
            central=100000.0, low=50000.0, high=200000.0, units="mIU/mL",
            tier="A",
            rationale=(
                "Tier A from Cole 2010 review and standard reproductive "
                "endocrinology: hCG peaks at ~50,000-200,000 mIU/mL "
                "around 10 weeks; the peak rescues the corpus luteum."
            ),
            citation_keys=["cole-2010-hcg"],
        ),
        param(
            pid="placental_endocrine.hcg_peak_week",
            name="Gestational week of peak hCG",
            subsystem="placental_endocrine",
            central=10.0, low=8.0, high=12.0, units="weeks",
            tier="A",
            rationale=(
                "Tier A from Cole 2010: hCG peak ~10 weeks, before "
                "placental progesterone production assumes corpus luteum's "
                "role."
            ),
            citation_keys=["cole-2010-hcg"],
        ),
        param(
            pid="placental_endocrine.hcg_term_miu_per_ml",
            name="Maternal serum hCG at term",
            subsystem="placental_endocrine",
            central=10000.0, low=5000.0, high=20000.0, units="mIU/mL",
            tier="B",
            rationale=(
                "Tier B from Cole 2010: hCG declines from peak to ~10,000 "
                "mIU/mL at term."
            ),
            citation_keys=["cole-2010-hcg"],
        ),
        param(
            pid="placental_endocrine.hpl_term_ug_per_ml",
            name="Maternal serum placental lactogen at term",
            subsystem="placental_endocrine",
            central=7.0, low=5.0, high=10.0, units="ug/mL",
            tier="B",
            rationale=(
                "Tier B from Handwerger 1991 review: hPL rises linearly "
                "through gestation, ~5-10 ug/mL at term. Drives maternal "
                "insulin resistance and lipolysis."
            ),
            citation_keys=["handwerger-2010-hpl"],
        ),
        param(
            pid="placental_endocrine.progesterone_term_ng_per_ml",
            name="Maternal serum progesterone at term",
            subsystem="placental_endocrine",
            central=150.0, low=100.0, high=200.0, units="ng/mL",
            tier="A",
            rationale=(
                "Tier A from Tulchinsky 1972 longitudinal study: "
                "progesterone rises through gestation, ~150 ng/mL at term, "
                "placental-derived after T1."
            ),
            citation_keys=["tulchinsky-1972-steroids"],
        ),
        param(
            pid="placental_endocrine.estradiol_term_ng_per_ml",
            name="Maternal serum estradiol at term",
            subsystem="placental_endocrine",
            central=14.0, low=8.0, high=25.0, units="ng/mL",
            tier="A",
            rationale=(
                "Tier A from Tulchinsky 1972: estradiol rises through "
                "gestation to ~10-25 ng/mL at term; placental-fetal unit "
                "synthesis."
            ),
            citation_keys=["tulchinsky-1972-steroids"],
        ),
        param(
            pid="placental_endocrine.estriol_term_ng_per_ml",
            name="Maternal serum estriol at term",
            subsystem="placental_endocrine",
            central=10.0, low=6.0, high=20.0, units="ng/mL",
            tier="A",
            rationale=(
                "Tier A from Tulchinsky 1972: estriol is uniquely a "
                "fetal-placental co-product (placenta lacks 16-alpha-"
                "hydroxylase); ~10 ng/mL at term."
            ),
            citation_keys=["tulchinsky-1972-steroids"],
        ),
    ]


def amniotic_fluid_params() -> list[dict]:
    return [
        param(
            pid="amniotic_fluid.afv_peak_ml",
            name="Amniotic fluid volume at peak",
            subsystem="amniotic_fluid",
            central=800.0, low=600.0, high=1000.0, units="mL",
            tier="A",
            rationale=(
                "Tier A from Brace & Wolf 1989: AFV rises through "
                "mid-pregnancy to ~800 mL peak, falls toward term. "
                "Well-replicated reference trajectory."
            ),
            citation_keys=["brace-1989-amniotic-fluid"],
        ),
        param(
            pid="amniotic_fluid.afv_peak_week",
            name="Gestational week of peak amniotic fluid volume",
            subsystem="amniotic_fluid",
            central=33.0, low=32.0, high=34.0, units="weeks",
            tier="A",
            rationale=(
                "Tier A from Brace & Wolf 1989: AFV peak at 32-34 weeks; "
                "fetal-urine production and swallowing approach steady "
                "state."
            ),
            citation_keys=["brace-1989-amniotic-fluid"],
        ),
        param(
            pid="amniotic_fluid.afv_term_ml",
            name="Amniotic fluid volume at term",
            subsystem="amniotic_fluid",
            central=600.0, low=400.0, high=800.0, units="mL",
            tier="A",
            rationale=(
                "Tier A from Brace & Wolf 1989: AFV declines from peak to "
                "~600 mL at term; oligohydramnios threshold conventionally "
                "AFI<5 cm or single deepest pocket<2 cm."
            ),
            citation_keys=["brace-1989-amniotic-fluid"],
        ),
        param(
            pid="amniotic_fluid.afv_20w_ml",
            name="Amniotic fluid volume at 20 weeks",
            subsystem="amniotic_fluid",
            central=350.0, low=250.0, high=450.0, units="mL",
            tier="A",
            rationale=(
                "Tier A from Brace & Wolf 1989: AFV at 20 weeks ~350 mL; "
                "interpolated reference point on the trajectory."
            ),
            citation_keys=["brace-1989-amniotic-fluid"],
        ),
    ]


# ---- Aggregator + writer -------------------------------------------


SUBSYSTEM_NEW_PARAMS = {
    "fetal_growth": biometry_params,
    "maternal_cardiovascular": mat_cardio_params,
    "maternal_renal": mat_renal_params,
    "maternal_respiratory": mat_resp_params,
    "maternal_endocrine": mat_endocrine_params,
    "placental_endocrine": placental_endocrine_params,
    "amniotic_fluid": amniotic_fluid_params,
}


def main() -> None:
    # 1) Citations
    cites_path = DS / "citations" / "citations.json"
    with cites_path.open() as f:
        cites = json.load(f)
    added_cites = 0
    for k, v in NEW_CITATIONS.items():
        if k in cites:
            continue
        cites[k] = v
        added_cites += 1
    # Sort keys for stable diffs
    cites_sorted = {k: cites[k] for k in sorted(cites)}
    with cites_path.open("w") as f:
        json.dump(cites_sorted, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Citations: +{added_cites}, total={len(cites_sorted)}")

    # 2) Parameters
    total_added = 0
    for subsystem, factory in SUBSYSTEM_NEW_PARAMS.items():
        path = DS / "parameters" / f"{subsystem}.json"
        existing: list[dict] = []
        if path.exists():
            existing = json.loads(path.read_text())
        existing_ids = {r["id"] for r in existing}
        new_records = [r for r in factory() if r["id"] not in existing_ids]
        if not new_records:
            print(f"{subsystem}: no new records (skipped)")
            continue
        combined = existing + new_records
        with path.open("w") as f:
            json.dump(combined, f, indent=2)
            f.write("\n")
        total_added += len(new_records)
        print(f"{subsystem}: +{len(new_records)} -> {len(combined)} total")
    print(f"Parameters: +{total_added}")


if __name__ == "__main__":
    main()
