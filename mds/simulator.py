from __future__ import annotations

import numpy as np


def electrospinning_fiber_diameter(conc_wt: float, voltage_kV: float, noise: float = 1.0) -> float:
    """Toy electrospinning simulator.

    Returns a synthetic 'fiber diameter (nm)' that depends on concentration and voltage.

    This is NOT a physical model. It is only to demonstrate closed-loop optimisation UI/logic.
    """
    conc_wt = float(conc_wt)
    voltage_kV = float(voltage_kV)
    noise = float(noise)

    # Nonlinear response surface with an optimum region.
    base = (
        280
        + 6.0 * (conc_wt - 11.5) ** 2
        + 3.5 * (voltage_kV - 19.0) ** 2
        - 35.0 * np.exp(-((conc_wt - 12.0) ** 2) / 10.0) * np.exp(-((voltage_kV - 18.5) ** 2) / 18.0)
        + 12.0 * np.sin(conc_wt / 2.5)
    )
    rng = np.random.default_rng()
    return float(base + rng.normal(0.0, noise))


def porous_material_sim(x1: float, x2: float, noise: float = 0.5) -> tuple[float, float]:
    """Toy porous material simulator.

    Inputs are in [0,1]. Outputs:
      - surface_area: maximize
      - yield: maximize
    """
    x1 = float(x1)
    x2 = float(x2)
    noise = float(noise)

    # Surface area peaks near (0.65, 0.25)
    surface_area = 900 + 350 * np.exp(-((x1 - 0.65) ** 2) / 0.02 - ((x2 - 0.25) ** 2) / 0.03) + 40 * np.sin(6 * x1)

    # Yield peaks near (0.35, 0.75)
    yld = 60 + 35 * np.exp(-((x1 - 0.35) ** 2) / 0.03 - ((x2 - 0.75) ** 2) / 0.02) + 5 * np.cos(5 * x2)

    rng = np.random.default_rng()
    surface_area += rng.normal(0.0, noise * 10)
    yld += rng.normal(0.0, noise)

    return float(surface_area), float(yld)
