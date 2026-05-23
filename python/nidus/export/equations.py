"""LaTeX equation strings for nidus submodels.

Spec 03 §5 calls for symbolic equation export so the docs surface the
mathematical form of each submodel, not just the English description.

Each Submodel registry entry carries a plain-text equation in its
`description`. This module mirrors that with a LaTeX fragment — what
you would drop into a docstring, README table, or paper appendix.

The map is incomplete by design: it covers the canonical kernel
families (logistic, Gaussian bump, Michaelis-Menten, Hill, linear,
piecewise-linear, polynomial, algebraic-combinator) with one
representative submodel per family. Submodels not in the map share
their family's form. Adding more entries is mechanical when a docs
consumer needs them.

Notation conventions
--------------------

- ``t``           gestational age in weeks (or whatever the kernel's
                  independent variable is)
- ``y_0``         baseline value
- ``y_T``         term value
- ``y_p``         peak excess value (for Gaussian-bump kernels)
- ``k``           rate constant (logistic / sigmoidal)
- ``t_{1/2}``     midpoint week
- ``t_p``         peak week (Gaussian-bump)
- ``\\sigma``     spread weeks (Gaussian-bump)

These keep the LaTeX compact and consistent across families; the
specific numerical parameter ids are documented in each Submodel's
``parameter_ids`` field rather than re-encoded in the LaTeX.
"""

from __future__ import annotations

# Canonical equation strings, grouped by kernel family. Keys are the
# Submodel.id values in nidus.export.registry.
_EQUATIONS: dict[str, str] = {
    # --- Logistic / sigmoidal: baseline -> term ---
    "placental_villous_growth": (r"A(t) = A_0 + \frac{A_T - A_0}{1 + e^{-k(t - t_{1/2})}}"),
    "uterine_artery_flow_logistic": (
        r"Q_{UA}(t) = Q_0 + \frac{Q_T - Q_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "gfr_logistic_trajectory": (
        r"\mathrm{GFR}(t) = \mathrm{GFR}_0 + "
        r"\frac{\mathrm{GFR}_\mathrm{peak} - \mathrm{GFR}_0}"
        r"{1 + e^{-k(t - t_{1/2})}}"
    ),
    "plasma_volume_expansion": (r"V(t) = V_0 + \frac{V_T - V_0}{1 + e^{-k(t - t_{1/2})}}"),
    "tidal_volume_trajectory": (
        r"V_T(t) = V_{T,0} + \frac{V_{T,T} - V_{T,0}}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "homa_ir_trajectory": (
        r"\mathrm{HOMA{-}IR}(t) = y_0 + \frac{y_T - y_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "hpl_trajectory": (r"\mathrm{hPL}(t) = y_0 + \frac{y_T - y_0}{1 + e^{-k(t - t_{1/2})}}"),
    "progesterone_trajectory": (r"P(t) = P_0 + \frac{P_T - P_0}{1 + e^{-k(t - t_{1/2})}}"),
    "estradiol_trajectory": (
        r"E_2(t) = E_{2,0} + \frac{E_{2,T} - E_{2,0}}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "fetal_heart_rate_trajectory": (
        r"\mathrm{FHR}(t) = \mathrm{FHR}_0 + "
        r"\frac{\mathrm{FHR}_T - \mathrm{FHR}_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "umbilical_artery_pi_trajectory": (
        r"\mathrm{UA{-}PI}(t) = y_0 + \frac{y_T - y_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "maternal_fetal_igg_transfer": (
        r"\mathrm{IgG}_f / \mathrm{IgG}_m = y_0 + \frac{y_T - y_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "maternal_microchimerism_trajectory": (
        r"C(t) = C_0 + \frac{C_T - C_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    "fetal_pulmonary_fluid_trajectory": (r"R(t) = R_0 + \frac{R_T - R_0}{1 + e^{-k(t - t_{1/2})}}"),
    # --- Gaussian-bump ---
    "maternal_cardiac_output_trajectory": (
        r"\mathrm{CO}(t) = \mathrm{CO}_0 + \mathrm{CO}_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    "maternal_map_trajectory": (
        r"\mathrm{MAP}(t) = \mathrm{MAP}_0 - \Delta_{\mathrm{nadir}} \, "
        r"\exp\!\left(-\frac{(t - t_{\mathrm{nadir}})^2}{2\sigma^2}\right)"
    ),
    "stroke_volume_trajectory": (
        r"\mathrm{SV}(t) = \mathrm{SV}_0 + \mathrm{SV}_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    "heart_rate_trajectory": (
        r"\mathrm{HR}(t) = \mathrm{HR}_0 + \mathrm{HR}_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    "renal_plasma_flow_trajectory": (
        r"\mathrm{RPF}(t) = \mathrm{RPF}_0 + \mathrm{RPF}_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    "mca_pi_trajectory": (
        r"\mathrm{MCA{-}PI}(t) = y_0 + y_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    "amniotic_fluid_volume_trajectory": (
        r"\mathrm{AFV}(t) = V_0 + V_p \, "
        r"\exp\!\left(-\frac{(t - t_p)^2}{2\sigma^2}\right)"
    ),
    # --- Linear (T1 -> term anchor) ---
    "pao2_trajectory_linear": r"\mathrm{PaO_2}(t) = a \, t + b",
    "arterial_ph_trajectory": r"\mathrm{pH}(t) = a \, t + b",
    "tsh_trajectory": r"\mathrm{TSH}(t) = a \, t + b \quad \text{(piecewise-linear)}",
    "cortisol_trajectory": (
        r"\mathrm{cortisol}(t) = y_0 + \frac{y_T - y_0}{1 + e^{-k(t - t_{1/2})}}"
    ),
    # --- O2-Hb dissociation ---
    "o2hb_dissociation_adult": (
        r"S = \frac{1}{1 + \exp\!\left[-\,n_H \ln\!\frac{P_{O_2}}{P_{50}}\right]} \quad "
        r"\text{(Severinghaus 1979)}"
    ),
    "o2hb_dissociation_fetal": (
        r"S = \frac{(P_{O_2}/P_{50})^{n_H}}{1 + (P_{O_2}/P_{50})^{n_H}} \quad "
        r"\text{(Hill, } P_{50} \approx 19.5\,\mathrm{mmHg}\text{)}"
    ),
    # --- Michaelis-Menten ---
    "placental_glucose_glut1": (r"J_{GLUT1} = \frac{V_{\max} \, [S]}{K_m + [S]}"),
    "placental_glucose_glut3": (r"J_{GLUT3} = \frac{V_{\max} \, [S]}{K_m + [S]}"),
    # --- Placental gas equilibrator (saturation toward UV PO2) ---
    "placental_o2_equilibrator": (
        r"P_{O_2,UV} = P_{O_2,IV} \cdot \frac{A_{\mathrm{villous}}}{K_{1/2} + A_{\mathrm{villous}}}"
    ),
    # --- Derived / algebraic ---
    "svr_trajectory": (r"\mathrm{SVR}(t) = 80 \cdot \mathrm{MAP}(t) / \mathrm{CO}(t)"),
    "minute_ventilation_trajectory": (r"\dot{V}_E(t) = V_T(t) \cdot \mathrm{RR}(t)"),
    "cerebroplacental_ratio": (r"\mathrm{CPR}(t) = \mathrm{MCA{-}PI}(t) \,/\, \mathrm{UA{-}PI}(t)"),
    "placental_fetal_allometry": (r"W_{\mathrm{placenta}} = a \, W_{\mathrm{fetus}}^{\,b}"),
    "placental_cortisol_gradient": (
        r"\mathrm{cortisol}_f = \mathrm{cortisol}_m \cdot (1 - f_{HSD2})"
    ),
    # --- Polynomial biometry (cubic in GA) ---
    "hadlock_bpd_growth": r"\mathrm{BPD}(t) = a_3 t^3 + a_2 t^2 + a_1 t + a_0",
    "hadlock_hc_growth": r"\mathrm{HC}(t) = a_3 t^3 + a_2 t^2 + a_1 t + a_0",
    "hadlock_ac_growth": r"\mathrm{AC}(t) = a_3 t^3 + a_2 t^2 + a_1 t + a_0",
    "hadlock_fl_growth": r"\mathrm{FL}(t) = a_3 t^3 + a_2 t^2 + a_1 t + a_0",
    # --- Hadlock IV regression (4-parameter biometry) ---
    "hadlock_fetal_weight": (
        r"\log_{10} W = 1.3596 + 0.0064\,\mathrm{HC} + 0.0424\,\mathrm{AC} "
        r"+ 0.174\,\mathrm{FL} + 6.1\!\times\!10^{-4}\,\mathrm{BPD}\cdot\mathrm{AC} "
        r"- 3.86\!\times\!10^{-3}\,\mathrm{AC}\cdot\mathrm{FL}"
    ),
    # --- Piecewise hCG (rise then decline) ---
    "hcg_trajectory": (
        r"\mathrm{hCG}(t) = \begin{cases} "
        r"\mathrm{hCG}_p \cdot (t/t_p)^2 & t \le t_p \\ "
        r"\mathrm{hCG}_T + (\mathrm{hCG}_p - \mathrm{hCG}_T)\, e^{-\lambda(t - t_p)} & t > t_p "
        r"\end{cases}"
    ),
}


def equation_latex(submodel_id: str) -> str | None:
    """Return the LaTeX equation for a submodel, or None if unmapped.

    The intended use is in documentation, dashboard tooltips, and paper
    appendices. Pass the value to a LaTeX-rendering layer (MathJax,
    matplotlib.text(usetex=True), Quarto, etc.) — this function returns
    a fragment, not a complete LaTeX document.
    """
    return _EQUATIONS.get(submodel_id)


def list_equations() -> dict[str, str]:
    """Return the full LaTeX equation map as a fresh dict."""
    return dict(_EQUATIONS)
