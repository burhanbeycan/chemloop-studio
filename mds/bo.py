from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel


@dataclass
class SuggestionMeta:
    y_best: float
    xi: float
    n_candidates: int
    predicted_mean: float
    predicted_std: float


def fit_gp(X: np.ndarray, y: np.ndarray) -> GaussianProcessRegressor:
    """Fit a small GP surrogate model.

    This is intentionally lightweight (scikit-learn GP) so the demo runs everywhere.
    For research-grade batch BO, consider BoTorch + GPyTorch.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=np.ones(X.shape[1]), nu=2.5) + WhiteKernel(noise_level=1.0)
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=3, random_state=0)
    gp.fit(X, y)
    return gp


def expected_improvement(
    X_cand: np.ndarray,
    gp: GaussianProcessRegressor,
    y_best: float,
    xi: float = 0.01,
) -> np.ndarray:
    """Expected Improvement acquisition for **minimisation** problems."""
    mu, std = gp.predict(X_cand, return_std=True)
    std = np.maximum(std, 1e-9)

    # For minimisation: improvement is y_best - mu
    imp = y_best - mu - xi
    Z = imp / std
    ei = imp * norm.cdf(Z) + std * norm.pdf(Z)
    ei = np.maximum(ei, 0.0)
    return ei


def suggest_next(
    bounds: np.ndarray,
    gp: GaussianProcessRegressor,
    y_best: float,
    n_candidates: int = 2000,
    xi: float = 0.01,
    random_state: int = 0,
) -> Tuple[np.ndarray, Dict]:
    """Suggest the next experiment by maximising EI over random candidates."""
    bounds = np.asarray(bounds, dtype=float)
    assert bounds.ndim == 2 and bounds.shape[1] == 2, "bounds should be (d, 2)"
    d = bounds.shape[0]

    rng = np.random.default_rng(int(random_state))
    X_cand = rng.uniform(bounds[:, 0], bounds[:, 1], size=(int(n_candidates), d))

    ei = expected_improvement(X_cand, gp, y_best=float(y_best), xi=float(xi))
    idx = int(np.argmax(ei))
    x_next = X_cand[idx]

    mu, std = gp.predict(x_next.reshape(1, -1), return_std=True)
    meta = SuggestionMeta(
        y_best=float(y_best),
        xi=float(xi),
        n_candidates=int(n_candidates),
        predicted_mean=float(mu[0]),
        predicted_std=float(std[0]),
    )
    return x_next, meta.__dict__
