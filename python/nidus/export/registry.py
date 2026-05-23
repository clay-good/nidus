"""Registry of exportable submodels and the nidus parameters that feed them.

Each submodel has:
- a stable `id` string used as the filename stem in exports/,
- a human-readable `name`,
- a `tier` (worst-input tier across its parameters, recomputed at
  export time),
- a `parameter_ids` list — the nidus dataset parameter ids that supply
  the submodel's numerical inputs,
- a `description` paragraph for the model's annotation block.

The registry is data, not code — generators in sbml.py / cellml.py /
physiocell.py consume it directly so adding a new submodel doesn't
require duplicate code per format.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Submodel:
    id: str
    name: str
    description: str
    sbo_term: str | None  # systems-biology ontology, where applicable
    parameter_ids: tuple[str, ...]
    independent_variable: str | None = None  # e.g. "t" (weeks), "PO2" (mmHg)
    output_units: str = "dimensionless"


SUBMODELS: tuple[Submodel, ...] = (
    Submodel(
        id="placental_villous_growth",
        name="Placental villous-surface-area growth (logistic)",
        description=(
            "Logistic ODE for the expansion of placental villous "
            "surface area across gestation. A(t) = A0 + (Aterm-A0) / "
            "(1 + exp(-r*(t-t_mid)))."
        ),
        sbo_term="SBO:0000295",  # logistic equation
        parameter_ids=(
            "placental_structure.initial_area_m2",
            "placental_structure.term_area_m2",
            "placental_structure.growth_rate_per_week",
            "placental_structure.midpoint_week",
        ),
        independent_variable="t_weeks",
        output_units="m^2",
    ),
    Submodel(
        id="o2hb_dissociation_adult",
        name="Adult O2-Hb dissociation (Severinghaus 1979)",
        description=(
            "Severinghaus 1979 (PMID 35496) equation 1 for adult human "
            "O2-Hb saturation: S = ((PO2^3 + 150*PO2)^-1 * 23400 + 1)^-1. "
            "Implicit P50=26.6 mmHg and Hill coefficient ~2.7."
        ),
        sbo_term="SBO:0000192",  # Hill function
        parameter_ids=(
            "maternal_blood.o2_hb_p50_maternal",
            "maternal_blood.o2_hb_hill_coefficient_maternal",
        ),
        independent_variable="po2_mmhg",
        output_units="dimensionless (fractional saturation)",
    ),
    Submodel(
        id="o2hb_dissociation_fetal",
        name="Fetal O2-Hb dissociation (HbF)",
        description=(
            "Hill-form dissociation for fetal HbF with P50 ~19.5 mmHg "
            "(Bauer 1969, PMID 4980905). The leftward P50 shift enables "
            "fetal extraction of O2 from low-PO2 intervillous blood."
        ),
        sbo_term="SBO:0000192",  # Hill function
        parameter_ids=("fetal_metabolism.fetal_p50_mmhg",),
        independent_variable="po2_mmhg",
        output_units="dimensionless (fractional saturation)",
    ),
    Submodel(
        id="placental_glucose_glut1",
        name="Placental glucose transport, GLUT1 (Michaelis-Menten)",
        description=(
            "Michaelis-Menten flux for GLUT1-mediated placental glucose "
            "transport on the syncytiotrophoblast: V = Vmax*[S]/(Km+[S])."
        ),
        sbo_term="SBO:0000028",  # irreversible Michaelis-Menten
        parameter_ids=(
            "placental_glucose.glucose_glut1_km_mmol_per_l",
            "placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2",
        ),
        independent_variable="substrate_mmol_per_l",
        output_units="mmol/min/m^2",
    ),
    Submodel(
        id="placental_glucose_glut3",
        name="Placental glucose transport, GLUT3 (Michaelis-Menten)",
        description=(
            "Michaelis-Menten flux for GLUT3-mediated placental glucose "
            "transport on the syncytial microvillous membrane: "
            "V = Vmax*[S]/(Km+[S]). GLUT3 is the higher-affinity (lower "
            "Km) isoform and dominates uptake early in gestation."
        ),
        sbo_term="SBO:0000028",
        parameter_ids=(
            "placental_glucose.glucose_glut3_km_mmol_per_l",
            "placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2",
        ),
        independent_variable="substrate_mmol_per_l",
        output_units="mmol/min/m^2",
    ),
    Submodel(
        id="maternal_cardiac_output_trajectory",
        name="Maternal cardiac output trajectory (Gaussian)",
        description=(
            "Gaussian-bump trajectory for cardiac output across "
            "gestation: CO(t) = baseline + peak_excess * "
            "exp(-((t - peak_week)/spread)^2 / 2). Fit to Mahendru 2014 "
            "longitudinal cohort + Sanghavi 2014 review."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_cardiac_output_l_per_min",
            "maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
            "maternal_cardiovascular.cardiac_output_peak_week",
            "maternal_cardiovascular.cardiac_output_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="L/min",
    ),
    Submodel(
        id="maternal_map_trajectory",
        name="Maternal MAP trajectory (Gaussian nadir)",
        description=(
            "Gaussian-nadir trajectory for mean arterial pressure: "
            "MAP(t) = baseline - nadir_drop * exp(-((t - nadir_week)/"
            "spread)^2 / 2). The mid-pregnancy dip reflects systemic "
            "vasodilation; pressure recovers toward term."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_map_mmhg",
            "maternal_cardiovascular.map_nadir_drop_mmhg",
            "maternal_cardiovascular.map_nadir_week",
            "maternal_cardiovascular.map_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="mmHg",
    ),
    Submodel(
        id="uterine_artery_flow_logistic",
        name="Uterine-artery flow logistic growth",
        description=(
            "Logistic growth of bilateral uterine-artery flow across "
            "gestation: Q(t) = baseline + (term - baseline) / "
            "(1 + exp(-r*(t - 24))). The mid-pregnancy reference week "
            "(24) is the inflection point of the curve fit to Thaler "
            "1990 Doppler-cohort means."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_cardiovascular.baseline_uterine_flow_ml_per_min",
            "maternal_cardiovascular.term_uterine_flow_ml_per_min",
            "maternal_cardiovascular.uterine_flow_growth_rate_per_week",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="placental_o2_equilibrator",
        name="Placental O2 venous-equilibrator (algebraic)",
        description=(
            "Algebraic equilibrium between maternal intervillous PO2 "
            "and umbilical vein PO2 across the syncytiotrophoblast "
            "barrier. Umbilical vein PO2 = intervillous PO2 * "
            "max_equilibration (typically ~60-80% of the maternal-side "
            "PO2 in a healthy term placenta)."
        ),
        sbo_term=None,
        parameter_ids=(
            "placental_gas_exchange.maternal_intervillous_po2_mmhg",
            "placental_gas_exchange.gas_max_equilibration",
        ),
        independent_variable="maternal_intervillous_po2_mmhg",
        output_units="mmHg",
    ),
    Submodel(
        id="plasma_volume_expansion",
        name="Maternal plasma volume across gestation (algebraic)",
        description=(
            "Sigmoidal plasma-volume expansion across gestation: "
            "PV(t) = early + (term - early) / (1 + exp(-0.2*(t - 22))). "
            "Fit to de Haas 2017 (PMID 28169502) meta-analysis pooled "
            "trajectory + Bernstein 2001 (PMID 11339913) early "
            "first-trimester anchor."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_blood.plasma_volume_early_l",
            "maternal_blood.plasma_volume_l",
        ),
        independent_variable="t_weeks",
        output_units="L",
    ),
    Submodel(
        id="gfr_logistic_trajectory",
        name="Maternal GFR logistic trajectory",
        description=(
            "Logistic-rise trajectory for maternal glomerular "
            "filtration rate across gestation: GFR(t) = baseline + "
            "(peak - baseline) / (1 + exp(-r*(t - t_peak))). Anchored "
            "to Conrad 2001 (PMID 11489744) review of relaxin-mediated "
            "renal vasodilation and the ~50% rise above non-pregnant "
            "baseline. Logistic is an approximation; the true curve "
            "plateaus and declines slightly toward term."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_renal.baseline_gfr_ml_per_min",
            "maternal_renal.gfr_ml_per_min",
            "maternal_renal.gfr_logistic_rate_per_week",
            "maternal_renal.gfr_peak_week",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="amniotic_fluid_volume_trajectory",
        name="Amniotic fluid volume trajectory (Gaussian-bump approximation)",
        description=(
            "Gaussian-bump approximation to the Brace & Wolf 1989 "
            "(PMID 2782359) amniotic-fluid-volume curve: AFV(t) = "
            "baseline + amplitude * exp(-((t - t_peak)/sigma)^2 / 2), "
            "where amplitude = peak - baseline. Peaks at ~33 weeks "
            "(~800 mL) and declines symmetrically. The published "
            "reference is piecewise; this Gaussian approximation "
            "carries the worst-input Tier C from the empirical spread."
        ),
        sbo_term=None,
        parameter_ids=(
            "amniotic_fluid.afv_early_baseline_ml",
            "amniotic_fluid.afv_peak_ml",
            "amniotic_fluid.afv_peak_week",
            "amniotic_fluid.afv_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="mL",
    ),
    Submodel(
        id="svr_trajectory",
        name="Maternal systemic vascular resistance trajectory (derived)",
        description=(
            "Derived SVR across gestation from the maternal MAP and "
            "cardiac-output trajectories: SVR(t) = MAP(t) * 80 / CO(t), "
            "where the conventional 80 factor converts mmHg*min/L into "
            "dyn*s*cm^-5. MAP(t) is the Gaussian-nadir trajectory and "
            "CO(t) is the Gaussian-bump trajectory; both are already in "
            "the registry. Sanghavi 2014 (PMC4172642) is the reference "
            "for the 80 convention in pregnancy."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_map_mmhg",
            "maternal_cardiovascular.map_nadir_drop_mmhg",
            "maternal_cardiovascular.map_nadir_week",
            "maternal_cardiovascular.map_spread_weeks",
            "maternal_cardiovascular.baseline_cardiac_output_l_per_min",
            "maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
            "maternal_cardiovascular.cardiac_output_peak_week",
            "maternal_cardiovascular.cardiac_output_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="dyn*s/cm^5",
    ),
    Submodel(
        id="pao2_trajectory_linear",
        name="Maternal arterial PaO2 trajectory (linear)",
        description=(
            "Linear PaO2 rise across gestation reflecting hyperventilation-"
            "induced respiratory alkalosis: PaO2(t) = baseline + "
            "(term - baseline) * (t / 40). Templeton & Kelman 1976 "
            "(PMID 1247088) and Hegewald 2011 describe the modest "
            "~5 mmHg rise from non-pregnant baseline to term."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_respiratory.baseline_pao2_mmhg",
            "maternal_respiratory.pao2_mmhg_term",
        ),
        independent_variable="t_weeks",
        output_units="mmHg",
    ),
    Submodel(
        id="tidal_volume_trajectory",
        name="Maternal tidal volume trajectory (sigmoidal)",
        description=(
            "Sigmoidal tidal-volume rise across gestation: "
            "VT(t) = baseline + (term - baseline) / "
            "(1 + exp(-0.2*(t - 20))). LoMauro 2015 (PMID 25624458) "
            "and Hegewald 2011 describe the ~30-40% rise from non-"
            "pregnant baseline to term tidal volume; the inflection "
            "is mid-pregnancy."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_respiratory.baseline_tidal_volume_ml",
            "maternal_respiratory.tidal_volume_ml_term",
        ),
        independent_variable="t_weeks",
        output_units="mL",
    ),
    Submodel(
        id="heart_rate_trajectory",
        name="Maternal heart rate trajectory (sigmoidal)",
        description=(
            "Sigmoidal HR rise across gestation: "
            "HR(t) = baseline + (term - baseline) / "
            "(1 + exp(-0.2*(t - 20))). Mahendru 2014 (PMID 25053730) "
            "reports the ~10-20 bpm rise from non-pregnant baseline. "
            "Multiplied by the stroke-volume trajectory it reproduces "
            "the cardiac-output bump."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_cardiovascular.baseline_heart_rate_bpm",
            "maternal_cardiovascular.term_heart_rate_bpm",
        ),
        independent_variable="t_weeks",
        output_units="bpm",
    ),
    Submodel(
        id="stroke_volume_trajectory",
        name="Maternal stroke volume trajectory (Gaussian)",
        description=(
            "Gaussian-bump stroke-volume trajectory mirroring the "
            "cardiac-output bump's peak week and spread: SV(t) = "
            "baseline + peak_excess * exp(-((t - peak_week)/spread)^2 "
            "/ 2). Mahendru 2014 (PMID 25053730) shows SV is the "
            "larger contributor to the mid-late-pregnancy CO peak; "
            "peak_week and spread are shared with the CO submodel."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_cardiovascular.baseline_stroke_volume_ml",
            "maternal_cardiovascular.peak_excess_stroke_volume_ml",
            "maternal_cardiovascular.cardiac_output_peak_week",
            "maternal_cardiovascular.cardiac_output_spread_weeks",
        ),
        independent_variable="t_weeks",
        output_units="mL",
    ),
    Submodel(
        id="renal_plasma_flow_trajectory",
        name="Maternal renal plasma flow trajectory (Gaussian)",
        description=(
            "Gaussian-bump renal-plasma-flow trajectory: RPF(t) = "
            "baseline + (peak - baseline) * exp(-((t - peak_week)/8)^2 "
            "/ 2). Dunlop 1981 (PMID 7259294) longitudinal cohort: "
            "RPF rises ~80% above non-pregnant baseline, peaks "
            "mid-pregnancy, then declines toward term. The spread is "
            "fixed at 8 weeks (no curated empirical spread parameter); "
            "the curve matches Dunlop's published trajectory within "
            "the longitudinal scatter."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_renal.renal_plasma_flow_baseline_ml_per_min",
            "maternal_renal.renal_plasma_flow_peak_ml_per_min",
            "maternal_renal.rpf_peak_week",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="minute_ventilation_trajectory",
        name="Maternal minute ventilation trajectory (VT x RR)",
        description=(
            "Derived minute ventilation across gestation: VE(t) = "
            "VT(t) * RR(t), where VT(t) is the sigmoidal tidal-volume "
            "trajectory and RR(t) is the sigmoidal respiratory-rate "
            "trajectory. The product reproduces the ~30-50% rise in "
            "VE characteristic of pregnancy. LoMauro 2015 (PMID "
            "25624458) and Hegewald 2011 cover the mechanism."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_respiratory.baseline_tidal_volume_ml",
            "maternal_respiratory.tidal_volume_ml_term",
            "maternal_respiratory.baseline_respiratory_rate_bpm",
            "maternal_respiratory.term_respiratory_rate_bpm",
        ),
        independent_variable="t_weeks",
        output_units="mL/min",
    ),
    Submodel(
        id="arterial_ph_trajectory",
        name="Maternal arterial pH trajectory (linear)",
        description=(
            "Linear arterial-pH rise across gestation reflecting "
            "compensated respiratory alkalosis: pH(t) = baseline + "
            "(term - baseline) * (t / 40). Baseline ~7.40, term ~7.44 "
            "(Templeton & Kelman 1976, PMID 1247088; Hegewald 2011). "
            "The actual trajectory plateaus after T1 but linear "
            "interpolation across 0-40 weeks captures the endpoints "
            "within published scatter."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_respiratory.baseline_arterial_ph",
            "maternal_respiratory.term_arterial_ph",
        ),
        independent_variable="t_weeks",
        output_units="dimensionless",
    ),
    Submodel(
        id="hadlock_bpd_growth",
        name="Fetal biparietal diameter growth (cubic fit to Hadlock 1982 anchors)",
        description=(
            "Cubic polynomial fit of biparietal diameter vs gestational "
            "age: BPD(t) = a3*t^3 + a2*t^2 + a1*t + a0, with "
            "coefficients fit at export time to the seven weekly "
            "anchors curated from Hadlock 1982 (PMID 7058748). Max "
            "residual at the anchors is <1 mm; the cubic is a smooth "
            "interpolant of the published reference."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_growth.bpd_16w_mm",
            "fetal_growth.bpd_20w_mm",
            "fetal_growth.bpd_24w_mm",
            "fetal_growth.bpd_28w_mm",
            "fetal_growth.bpd_32w_mm",
            "fetal_growth.bpd_36w_mm",
            "fetal_growth.bpd_40w_mm",
        ),
        independent_variable="t_weeks",
        output_units="mm",
    ),
    Submodel(
        id="hadlock_hc_growth",
        name="Fetal head circumference growth (cubic fit to Hadlock 1982 anchors)",
        description=(
            "Cubic polynomial fit of head circumference vs gestational "
            "age: HC(t) = a3*t^3 + a2*t^2 + a1*t + a0, fit at export "
            "time to the seven weekly anchors from Hadlock 1982. Max "
            "residual at the anchors is ~2.4 mm out of ~340 mm at "
            "term (sub-1% error)."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_growth.hc_16w_mm",
            "fetal_growth.hc_20w_mm",
            "fetal_growth.hc_24w_mm",
            "fetal_growth.hc_28w_mm",
            "fetal_growth.hc_32w_mm",
            "fetal_growth.hc_36w_mm",
            "fetal_growth.hc_40w_mm",
        ),
        independent_variable="t_weeks",
        output_units="mm",
    ),
    Submodel(
        id="hadlock_ac_growth",
        name="Fetal abdominal circumference growth (cubic fit to Hadlock 1982 anchors)",
        description=(
            "Cubic polynomial fit of abdominal circumference vs "
            "gestational age: AC(t) = a3*t^3 + a2*t^2 + a1*t + a0, "
            "fit at export time to the seven weekly anchors from "
            "Hadlock 1982. Max residual ~1.4 mm."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_growth.ac_16w_mm",
            "fetal_growth.ac_20w_mm",
            "fetal_growth.ac_24w_mm",
            "fetal_growth.ac_28w_mm",
            "fetal_growth.ac_32w_mm",
            "fetal_growth.ac_36w_mm",
            "fetal_growth.ac_40w_mm",
        ),
        independent_variable="t_weeks",
        output_units="mm",
    ),
    Submodel(
        id="hadlock_fl_growth",
        name="Fetal femur length growth (cubic fit to Hadlock 1982 anchors)",
        description=(
            "Cubic polynomial fit of femur length vs gestational age: "
            "FL(t) = a3*t^3 + a2*t^2 + a1*t + a0, fit at export time "
            "to the seven weekly anchors from Hadlock 1982. Max "
            "residual <0.5 mm."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_growth.fl_16w_mm",
            "fetal_growth.fl_20w_mm",
            "fetal_growth.fl_24w_mm",
            "fetal_growth.fl_28w_mm",
            "fetal_growth.fl_32w_mm",
            "fetal_growth.fl_36w_mm",
            "fetal_growth.fl_40w_mm",
        ),
        independent_variable="t_weeks",
        output_units="mm",
    ),
    Submodel(
        id="homa_ir_trajectory",
        name="Maternal insulin resistance (HOMA-IR) trajectory",
        description=(
            "Sigmoidal HOMA-IR rise across gestation: HOMA(t) = "
            "baseline + (term - baseline) / (1 + exp(-0.2*(t - 22))). "
            "Catalano 1991 (PMID 1957840) and Sonagra 2014 document "
            "the ~2-3x rise from non-pregnant baseline driven by "
            "placental lactogen, hPL, and cortisol antagonism of "
            "insulin signalling. The inflection sits in late T2."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_endocrine.homa_ir_baseline",
            "maternal_endocrine.homa_ir_term",
        ),
        independent_variable="t_weeks",
        output_units="dimensionless",
    ),
    Submodel(
        id="tsh_trajectory",
        name="Maternal TSH trajectory (T1 nadir to term recovery)",
        description=(
            "Linear TSH interpolation across gestation: TSH(t) = "
            "tsh_t1 + (term - t1) * ((t - 12) / 28), clamped at the "
            "T1 nadir value before week 12. The T1 nadir is driven "
            "by hCG cross-stimulation of the TSH receptor (Glinoer "
            "1997, Korevaar 2014); the value rises modestly back "
            "toward term as hCG falls. A fuller Hill-form suppression "
            "by hCG is Phase B item 3.4 but requires an additional "
            "coupling-coefficient parameter not yet curated."
        ),
        sbo_term=None,
        parameter_ids=(
            "maternal_endocrine.tsh_t1_miu_per_l",
            "maternal_endocrine.tsh_term_miu_per_l",
        ),
        independent_variable="t_weeks",
        output_units="mIU/L",
    ),
    Submodel(
        id="cortisol_trajectory",
        name="Maternal total cortisol trajectory (sigmoidal)",
        description=(
            "Sigmoidal total cortisol rise across gestation: "
            "cortisol(t) = baseline + (term - baseline) / "
            "(1 + exp(-0.15*(t - 22))). Allolio 1990, Jung 2011: "
            "total cortisol rises 2-3x by term, driven by "
            "estrogen-induced CBG plus loss of HPA axis sensitivity. "
            "The diurnal-rhythm overlay (Phase B 3.3) would add a "
            "cosine term scaled by a separate amplitude parameter "
            "not yet in the dataset."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "maternal_endocrine.cortisol_baseline_ug_per_dl",
            "maternal_endocrine.cortisol_term_ug_per_dl",
        ),
        independent_variable="t_weeks",
        output_units="ug/dL",
    ),
    Submodel(
        id="hpl_trajectory",
        name="Maternal placental lactogen trajectory (sigmoidal)",
        description=(
            "Sigmoidal hPL rise across gestation from non-pregnant "
            "baseline (operationally zero; hPL is exclusively "
            "placental) to ~5-10 ug/mL at term. Handwerger 2010 / "
            "Handwerger 1991 document the steady rise driven by "
            "syncytiotrophoblast mass; hPL is a major driver of "
            "maternal insulin resistance and lipolysis."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "placental_endocrine.hpl_baseline_ug_per_ml",
            "placental_endocrine.hpl_term_ug_per_ml",
        ),
        independent_variable="t_weeks",
        output_units="ug/mL",
    ),
    Submodel(
        id="progesterone_trajectory",
        name="Maternal serum progesterone trajectory (sigmoidal)",
        description=(
            "Sigmoidal progesterone trajectory across gestation: "
            "from the mid-luteal non-pregnant baseline (~10 ng/mL) "
            "to term (~150 ng/mL). Corpus luteum supplies progesterone "
            "for the first ~8 weeks before placental takeover; "
            "Tulchinsky 1972 documents the 10-20x rise. The single "
            "sigmoid is a simplification of the actual two-source "
            "kinetics."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "placental_endocrine.progesterone_baseline_ng_per_ml",
            "placental_endocrine.progesterone_term_ng_per_ml",
        ),
        independent_variable="t_weeks",
        output_units="ng/mL",
    ),
    Submodel(
        id="estradiol_trajectory",
        name="Maternal serum estradiol trajectory (sigmoidal)",
        description=(
            "Sigmoidal estradiol trajectory across gestation from "
            "the mid-luteal pre-pregnancy baseline (~0.1 ng/mL) to "
            "term (~14 ng/mL); ~100x rise driven by placental "
            "aromatisation. Tulchinsky 1972 / O'Leary 1991. Single "
            "sigmoid simplifies the actual rapid early rise + slower "
            "late rise."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "placental_endocrine.estradiol_baseline_ng_per_ml",
            "placental_endocrine.estradiol_term_ng_per_ml",
        ),
        independent_variable="t_weeks",
        output_units="ng/mL",
    ),
    Submodel(
        id="fetal_heart_rate_trajectory",
        name="Fetal heart rate trajectory (sigmoidal fall)",
        description=(
            "Sigmoidal FHR fall across gestation: FHR(t) = baseline "
            "+ (term - baseline) / (1 + exp(-0.2*(t - 18))). FHR "
            "peaks ~170 bpm at weeks 9-10, then declines toward "
            "~140 bpm at term as parasympathetic tone develops "
            "(Pildner von Steinburg 2013). Because (term - baseline) "
            "is negative, the same sigmoidal form encodes the fall."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "fetal_circulation.fhr_baseline_bpm",
            "fetal_circulation.fhr_term_bpm",
        ),
        independent_variable="t_weeks",
        output_units="bpm",
    ),
    Submodel(
        id="hcg_trajectory",
        name="Maternal serum hCG trajectory (piecewise rise then exponential decline)",
        description=(
            "Piecewise hCG kinetics: quadratic rise from zero to "
            "peak by `hcg_peak_week` (Cole 2010 doubling-time pattern "
            "approximated as a quadratic), then exponential decline "
            "from peak toward `hcg_term` over the remainder of "
            "gestation. The decline-rate constant is fit at build "
            "time so the model passes exactly through (peak_week, "
            "peak) and (40w, term)."
        ),
        sbo_term=None,
        parameter_ids=(
            "placental_endocrine.hcg_peak_miu_per_ml",
            "placental_endocrine.hcg_peak_week",
            "placental_endocrine.hcg_term_miu_per_ml",
        ),
        independent_variable="t_weeks",
        output_units="mIU/mL",
    ),
    Submodel(
        id="umbilical_artery_pi_trajectory",
        name="Umbilical artery pulsatility index trajectory (sigmoidal fall)",
        description=(
            "Sigmoidal UA-PI fall across gestation from baseline "
            "(~1.5 at 16-20 weeks) to term (~0.85) as placental "
            "vascular resistance drops with villous-tree expansion. "
            "Acharya 2005 (PMID 15776417) reference ranges. The same "
            "baseline -> term sigmoid form encodes the fall because "
            "(term - baseline) is negative."
        ),
        sbo_term="SBO:0000295",  # logistic
        parameter_ids=(
            "fetal_circulation.ua_pi_baseline",
            "fetal_circulation.ua_pi_term",
        ),
        independent_variable="t_weeks",
        output_units="dimensionless",
    ),
    Submodel(
        id="mca_pi_trajectory",
        name="Middle cerebral artery pulsatility index trajectory (Gaussian bell)",
        description=(
            "Gaussian bell-shape for MCA-PI across gestation: "
            "MCA-PI(t) = baseline + (peak - baseline) * "
            "exp(-((t - 28)/8)^2 / 2). Rises through T2, peaks "
            "~2.0 at ~28 weeks, then falls back toward ~1.5 at term "
            "as the fetal brain-sparing reflex drops cerebral "
            "resistance (Mari 1995, PMID 7900181). Peak week and "
            "spread are hardcoded; the published cohort means are "
            "the curve anchors."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_circulation.mca_pi_baseline",
            "fetal_circulation.mca_pi_peak",
        ),
        independent_variable="t_weeks",
        output_units="dimensionless",
    ),
    Submodel(
        id="cerebroplacental_ratio",
        name="Cerebroplacental ratio (CPR), derived",
        description=(
            "Derived CPR(t) = MCA-PI(t) / UA-PI(t), the canonical "
            "fetal-compromise screen: CPR > 1 is normal; CPR < 1 "
            "flags reduced cerebral resistance relative to placental "
            "resistance (brain-sparing under chronic hypoxia). "
            "Baschat 2003 review; the ratio composes the MCA-PI and "
            "UA-PI submodels with no additional parameters."
        ),
        sbo_term=None,
        parameter_ids=(
            "fetal_circulation.ua_pi_baseline",
            "fetal_circulation.ua_pi_term",
            "fetal_circulation.mca_pi_baseline",
            "fetal_circulation.mca_pi_peak",
        ),
        independent_variable="t_weeks",
        output_units="dimensionless",
    ),
    Submodel(
        id="hadlock_fetal_weight",
        name="Hadlock IV fetal weight from biometry",
        description=(
            "Hadlock 1991 (PMID 1887021) four-parameter sonographic "
            "fetal-weight regression: log10(EFW) = 1.3596 + 0.0064*HC "
            "+ 0.0424*AC + 0.174*FL + 0.00061*BPD*AC - 0.00386*AC*FL. "
            "Validated against n=1771 fetuses with 3.3% mean absolute "
            "error."
        ),
        sbo_term=None,
        parameter_ids=("fetal_growth.hadlock_coefficient",),
        independent_variable="biometry_mm",
        output_units="g",
    ),
)


def list_submodels() -> list[dict[str, object]]:
    """Return a JSON-serialisable list of submodel summaries."""
    return [
        {
            "id": sm.id,
            "name": sm.name,
            "sbo_term": sm.sbo_term,
            "n_parameters": len(sm.parameter_ids),
            "parameter_ids": list(sm.parameter_ids),
            "output_units": sm.output_units,
        }
        for sm in SUBMODELS
    ]
