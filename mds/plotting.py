from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor


def plot_history(runs: pd.DataFrame):
    fig = plt.figure()
    ax = plt.gca()
    if len(runs) > 0:
        ax.plot(np.arange(1, len(runs) + 1), runs["fiber_diam_nm"].to_numpy(), marker="o")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Fiber diameter (nm)")
        ax.set_title("Objective history (minimise)")
    return fig


def plot_gp_surface(bounds: np.ndarray, gp: GaussianProcessRegressor, runs: pd.DataFrame, x_next: np.ndarray | None = None):
    # 2D grid visualisation
    x1 = np.linspace(bounds[0, 0], bounds[0, 1], 60)
    x2 = np.linspace(bounds[1, 0], bounds[1, 1], 60)
    X1, X2 = np.meshgrid(x1, x2)
    Xg = np.column_stack([X1.ravel(), X2.ravel()])
    mu, std = gp.predict(Xg, return_std=True)

    fig = plt.figure()
    ax = plt.gca()
    c = ax.contourf(X1, X2, mu.reshape(X1.shape), levels=25)
    plt.colorbar(c, ax=ax, label="Predicted mean (nm)")
    ax.set_xlabel("Concentration (wt%)")
    ax.set_ylabel("Voltage (kV)")
    ax.set_title("GP surrogate mean")

    if len(runs) > 0:
        ax.scatter(runs["conc_wt"], runs["voltage_kV"], marker="x", label="Runs")
    if x_next is not None:
        ax.scatter([x_next[0]], [x_next[1]], marker="o", label="Suggested")
    ax.legend(loc="best")
    return fig


def plot_pareto(df: pd.DataFrame, mask: np.ndarray):
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(df["surface_area"], df["yield"], alpha=0.5, label="Samples")
    ax.scatter(df.loc[mask, "surface_area"], df.loc[mask, "yield"], marker="o", label="Pareto front")
    ax.set_xlabel("Surface area (a.u.)")
    ax.set_ylabel("Yield (a.u.)")
    ax.set_title("Pareto front (approx.)")
    ax.legend(loc="best")
    return fig
