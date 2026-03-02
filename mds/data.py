from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def init_runhistory() -> pd.DataFrame:
    return pd.DataFrame(columns=["conc_wt", "voltage_kV", "fiber_diam_nm"])


def append_run(df: pd.DataFrame, x: Iterable[float], y: float) -> pd.DataFrame:
    x = list(map(float, x))
    y = float(y)
    row = {"conc_wt": x[0], "voltage_kV": x[1], "fiber_diam_nm": y}
    return pd.concat([df, pd.DataFrame([row])], ignore_index=True)


def export_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
