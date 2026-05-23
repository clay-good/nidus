"""One-parameter sensitivity sweeps of nidus reference kernels.

Spec 03 §5 calls out a small "re-evaluate a submodel across a parameter
range and emit a CSV" utility as cross-cutting infrastructure for the
expanded submodel registry. This module is that utility.

It works against the pure-NumPy reference kernels in
`nidus.export.reference` (not the SBML/CellML builders) because those
kernels are the cheap, vectorised, side-effect-free path. The same
algebraic relationships are encoded in the SBML/CellML output, so a
sweep here is representative of what a downstream simulator would
compute.

Two public functions:

- ``sweep`` — evaluate ``kernel(independent, **fixed, **{sweep_param: v})``
  for each value in ``sweep_values`` and return a tidy long-form dict
  of NumPy arrays.
- ``write_csv`` — write a sweep result to a CSV file in long format
  (one row per (sweep_value, independent_value) cell).

The module is deliberately schema-agnostic: it does not need to know
how each kernel maps to dataset parameter ids. Callers pass the kernel
and kwargs directly, which keeps the surface small and removes a
maintenance liability (every new submodel would otherwise need a
mapping entry here).
"""

from __future__ import annotations

import csv
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


def sweep(
    kernel: Callable[..., NDArray[np.float64]],
    independent: Sequence[float] | NDArray[np.floating],
    *,
    fixed: dict[str, Any],
    sweep_param: str,
    sweep_values: Sequence[float] | NDArray[np.floating],
    independent_kwarg: str | None = None,
) -> dict[str, NDArray[np.float64]]:
    """Evaluate a reference kernel across one swept parameter.

    Args:
        kernel: a reference kernel from ``nidus.export.reference``
            (or any callable with the same shape: first positional
            argument is the independent variable, remaining are
            keyword-only). The kernel must return a 1-D NumPy array
            broadcast over ``independent``.
        independent: values of the kernel's independent variable
            (e.g. gestational age in weeks).
        fixed: keyword arguments to hold fixed during the sweep.
            Must not contain ``sweep_param``.
        sweep_param: name of the kwarg to vary.
        sweep_values: values of ``sweep_param`` to evaluate.
        independent_kwarg: pass ``independent`` as this kwarg instead
            of positionally (some kernels take a keyword-only
            independent variable).

    Returns:
        Tidy long-form result with keys:
            ``"sweep_param"`` - constant string equal to ``sweep_param``,
                included so the writer can surface what was swept.
            ``"sweep_value"`` - (N_sweep * N_independent,) float array
                of repeated sweep values.
            ``"independent"`` - (N_sweep * N_independent,) float array
                of tiled independent values.
            ``"output"`` - (N_sweep * N_independent,) float array of
                kernel outputs.
    """
    if sweep_param in fixed:
        raise ValueError(
            f"sweep_param {sweep_param!r} also appears in fixed kwargs; "
            "the swept parameter must not be fixed simultaneously."
        )

    t = np.asarray(independent, dtype=np.float64)
    sweep_vals = np.asarray(sweep_values, dtype=np.float64)

    outputs: list[NDArray[np.float64]] = []
    for v in sweep_vals:
        kwargs: dict[str, Any] = {**fixed, sweep_param: float(v)}
        if independent_kwarg is None:
            y = kernel(t, **kwargs)
        else:
            y = kernel(**{independent_kwarg: t, **kwargs})
        y_arr = np.asarray(y, dtype=np.float64)
        if y_arr.shape != t.shape:
            y_arr = np.broadcast_to(y_arr, t.shape).copy()
        outputs.append(y_arr)

    output = np.concatenate(outputs)
    sweep_col = np.repeat(sweep_vals, t.shape[0])
    indep_col = np.tile(t, sweep_vals.shape[0])

    return {
        "sweep_param": np.array([sweep_param] * output.shape[0]),
        "sweep_value": sweep_col,
        "independent": indep_col,
        "output": output,
    }


def write_csv(
    result: dict[str, NDArray[Any]],
    path: str | Path,
    *,
    independent_label: str = "independent",
    output_label: str = "output",
) -> None:
    """Write a sweep result to CSV in long format.

    One row per (sweep_value, independent) cell. The header is
    ``sweep_param,sweep_value,<independent_label>,<output_label>``.
    """
    p = Path(path)
    n = result["output"].shape[0]
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sweep_param", "sweep_value", independent_label, output_label])
        for i in range(n):
            writer.writerow(
                [
                    str(result["sweep_param"][i]),
                    float(result["sweep_value"][i]),
                    float(result["independent"][i]),
                    float(result["output"][i]),
                ]
            )
