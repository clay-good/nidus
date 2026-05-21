"""Pure-NumPy reference kernels for the exported submodels.

Each kernel evaluates a single mechanistic submodel using only numpy.
The exported SBML/CellML/PhysioCell models must produce numerically
matching output (within tolerance) when simulated. The round-trip
validation in the test suite uses these kernels as the ground truth.

These are NOT a new physiological engine. They are unit-test-grade
evaluators of the same algebraic relationships the exported models
encode.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

FloatArrayLike = float | Sequence[float] | NDArray[np.floating]


# ---- 1. Logistic placental villous-surface-area growth -------------


def placental_area_logistic(
    t_weeks: FloatArrayLike,
    *,
    initial_area_m2: float,
    term_area_m2: float,
    growth_rate_per_week: float,
    midpoint_week: float,
) -> NDArray[np.float64]:
    """Logistic villous-surface-area growth.

    `A(t) = A0 + (Aterm - A0) / (1 + exp(-r*(t - t_mid)))`

    Args:
        t_weeks: gestational age(s) in weeks. Scalar or array.
        initial_area_m2: surface area at the early-pregnancy floor.
        term_area_m2: surface area at term plateau.
        growth_rate_per_week: logistic rate parameter (1/week).
        midpoint_week: gestational week at the curve midpoint.

    Returns:
        Surface area at each input week, in m^2.
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_area_m2 - initial_area_m2
    return initial_area_m2 + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 2. Severinghaus O2-Hb dissociation ----------------------------


def severinghaus_o2_saturation(po2_mmhg: FloatArrayLike) -> NDArray[np.float64]:
    """Severinghaus 1979 (PMID 35496) equation 1.

    `S = ((PO2^3 + 150*PO2)^-1 * 23400 + 1)^-1`

    The implicit P50 is 26.6 mmHg (the dataset's
    `maternal_blood.o2_hb_p50_maternal`) and the implicit Hill
    coefficient is ~2.7 (the dataset's
    `maternal_blood.o2_hb_hill_coefficient_maternal`).

    Args:
        po2_mmhg: oxygen partial pressure(s) in mmHg, > 0.

    Returns:
        Fractional saturation in [0, 1].
    """
    p = np.asarray(po2_mmhg, dtype=np.float64)
    if np.any(p <= 0):
        raise ValueError("PO2 must be strictly positive")
    return 1.0 / ((p**3 + 150.0 * p) ** -1 * 23400.0 + 1.0)


# ---- 3. Michaelis-Menten glucose transport (GLUT1) -----------------


def glut1_michaelis_menten(
    substrate_mmol_per_l: FloatArrayLike,
    *,
    km_mmol_per_l: float,
    vmax_per_area: float,
) -> NDArray[np.float64]:
    """Standard Michaelis-Menten rate law.

    `V = Vmax * [S] / (Km + [S])`

    Args:
        substrate_mmol_per_l: glucose concentration(s) in mmol/L.
        km_mmol_per_l: GLUT1 Michaelis constant (nidus
            `placental_glucose.glucose_glut1_km_mmol_per_l`).
        vmax_per_area: GLUT1 maximum flux per villous-surface-area
            (nidus `placental_glucose.glucose_glut1_vmax_per_area_*`).

    Returns:
        Flux per villous-surface-area at each substrate concentration,
        in the same units as `vmax_per_area`.
    """
    s = np.asarray(substrate_mmol_per_l, dtype=np.float64)
    return vmax_per_area * s / (km_mmol_per_l + s)


# ---- 4. Fetal HbF dissociation (Bauer 1969 left-shift) -------------


def fetal_hbf_o2_saturation(
    po2_mmhg: FloatArrayLike,
    *,
    p50_mmhg: float = 19.5,
    hill_coefficient: float = 2.85,
) -> NDArray[np.float64]:
    """Hill-form dissociation for fetal HbF.

    `S = (PO2/P50)^n / (1 + (PO2/P50)^n)`

    HbF P50 ~19.5 mmHg (Bauer 1969, PMID 4980905) — the leftward shift
    relative to adult HbA enables fetal O2 extraction from the low-PO2
    intervillous blood.

    Args:
        po2_mmhg: PO2 in mmHg, > 0.
        p50_mmhg: HbF P50 (default 19.5; nidus
            `fetal_metabolism.fetal_p50_mmhg`).
        hill_coefficient: HbF Hill coefficient (default 2.85 per Bauer
            1969; subtly higher than HbA's 2.7).

    Returns:
        Fractional saturation in [0, 1].
    """
    p = np.asarray(po2_mmhg, dtype=np.float64)
    if np.any(p <= 0):
        raise ValueError("PO2 must be strictly positive")
    ratio = (p / p50_mmhg) ** hill_coefficient
    return ratio / (1.0 + ratio)
