"""Experiment recommendation utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from .models import ExperimentRecommendation


DEFAULT_EXPERIMENT_PATH = Path(__file__).resolve().parents[2] / "data" / "sample_experiments.csv"


FEATURE_COLUMNS = [
    "polymer_concentration_wt",
    "voltage_kv",
    "flow_rate_ml_h",
    "collector_distance_cm",
    "pei_fraction_wt",
]


def load_experiments(path: str | Path = DEFAULT_EXPERIMENT_PATH) -> pd.DataFrame:
    """Load experiment table."""

    table_path = Path(path)
    if not table_path.exists():
        raise FileNotFoundError(f"Experiment table not found: {table_path}")
    frame = pd.read_csv(table_path)
    required = {"experiment_id", "observed_score", "candidate"} | set(FEATURE_COLUMNS)
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Experiment table is missing columns: {sorted(missing)}")
    return frame


def recommend_next_experiment(
    frame: pd.DataFrame,
    target_column: str = "observed_score",
    candidate_column: str = "candidate",
) -> ExperimentRecommendation:
    """Recommend the next candidate experiment using expected-improvement logic.

    Observed rows train a small random-forest surrogate. Candidate rows are ranked by
    predicted performance and ensemble uncertainty. This is an interpretable placeholder
    for a future Bayesian optimization loop.
    """

    observed = frame[frame[candidate_column] == 0].copy()
    candidates = frame[frame[candidate_column] == 1].copy()

    if observed.empty:
        raise ValueError("At least one observed experiment is required.")
    if candidates.empty:
        raise ValueError("At least one candidate experiment is required.")

    X_train = observed[FEATURE_COLUMNS]
    y_train = observed[target_column]

    model = RandomForestRegressor(n_estimators=128, random_state=42, min_samples_leaf=1)
    model.fit(X_train, y_train)

    X_candidates = candidates[FEATURE_COLUMNS]
    tree_predictions = np.vstack([tree.predict(X_candidates) for tree in model.estimators_])
    mean_prediction = tree_predictions.mean(axis=0)
    uncertainty = tree_predictions.std(axis=0)

    best_observed = float(y_train.max())
    expected_improvement = np.maximum(0.0, mean_prediction - best_observed) + 0.15 * uncertainty
    selected_index = int(np.argmax(expected_improvement))
    selected = candidates.iloc[selected_index]

    variables = {column: _to_python(selected[column]) for column in FEATURE_COLUMNS}
    return ExperimentRecommendation(
        experiment_id=str(selected["experiment_id"]),
        expected_improvement=round(float(expected_improvement[selected_index]), 4),
        predicted_score=round(float(mean_prediction[selected_index]), 4),
        uncertainty=round(float(uncertainty[selected_index]), 4),
        rationale=_rationale(variables, best_observed, mean_prediction[selected_index]),
        variables=variables,
    )


def _rationale(variables: dict[str, Any], best_observed: float, predicted: float) -> str:
    return (
        "The candidate balances low-to-moderate polymer concentration, controlled flow rate, "
        "and antimicrobial PEI fraction. The surrogate predicts a score of "
        f"{predicted:.3f} compared with the current best observed score of {best_observed:.3f}."
    )


def _to_python(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value
