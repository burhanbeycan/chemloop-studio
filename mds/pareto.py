from __future__ import annotations

import numpy as np


def pareto_front(F: np.ndarray, maximize: bool = True) -> np.ndarray:
    """Return boolean mask for Pareto-efficient points.

    F: (n, m) objective values.
    If maximize=True, larger is better. Otherwise smaller is better.
    """
    F = np.asarray(F, dtype=float)
    n = F.shape[0]
    is_eff = np.ones(n, dtype=bool)

    if maximize:
        # Convert to minimisation by negating
        Fm = -F
    else:
        Fm = F.copy()

    for i in range(n):
        if not is_eff[i]:
            continue
        # A point is dominated if another point is <= in all objectives and < in at least one
        dominates = np.all(Fm <= Fm[i], axis=1) & np.any(Fm < Fm[i], axis=1)
        # Keep itself
        dominates[i] = False
        is_eff[dominates] = False
    return is_eff
