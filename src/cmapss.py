"""Data loading and feature engineering for the NASA C-MAPSS benchmark."""
from __future__ import annotations

from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SENSOR_COLUMNS = [f"sensor_{i}" for i in range(1, 22)]
SETTING_COLUMNS = [f"setting_{i}" for i in range(1, 4)]
COLUMNS = ["unit", "cycle", *SETTING_COLUMNS, *SENSOR_COLUMNS]


def ensure_data() -> None:
    """Extract the benchmark archive if it has been downloaded into data/raw."""
    archive = RAW / "CMAPSSData.zip"
    if not archive.exists():
        raise FileNotFoundError(
            "NASA C-MAPSS data not found. Run `python scripts/download_data.py` first."
        )
    if not (RAW / "train_FD001.txt").exists():
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(RAW)


def load_train(subset: str = "FD001") -> pd.DataFrame:
    ensure_data()
    frame = pd.read_csv(RAW / f"train_{subset}.txt", sep=r"\s+", header=None)
    frame = frame.iloc[:, : len(COLUMNS)]
    frame.columns = COLUMNS
    max_cycle = frame.groupby("unit")["cycle"].transform("max")
    frame["rul"] = max_cycle - frame["cycle"]
    return frame


def load_test(subset: str = "FD001") -> tuple[pd.DataFrame, np.ndarray]:
    ensure_data()
    frame = pd.read_csv(RAW / f"test_{subset}.txt", sep=r"\s+", header=None)
    frame = frame.iloc[:, : len(COLUMNS)]
    frame.columns = COLUMNS
    truth = pd.read_csv(RAW / f"RUL_{subset}.txt", sep=r"\s+", header=None).iloc[:, 0]
    return frame, truth.to_numpy(dtype=float)


def add_features(frame: pd.DataFrame, cap: int = 125) -> pd.DataFrame:
    """Add capped RUL and trailing sensor summaries without crossing engine boundaries."""
    result = frame.copy()
    if "rul" in result:
        result["rul"] = result["rul"].clip(upper=cap)
    result["cycle"] = result["cycle"].astype(float)
    # Last-five-cycle summaries provide a compact temporal signal; shifts ensure the
    # current cycle is included and all rolling windows stay within a single engine.
    groups = result.groupby("unit", sort=False)
    selected = SENSOR_COLUMNS
    for col in selected:
        result[f"{col}_mean5"] = groups[col].transform(
            lambda values: values.rolling(5, min_periods=1).mean()
        )
        result[f"{col}_std5"] = groups[col].transform(
            lambda values: values.rolling(5, min_periods=2).std().fillna(0.0)
        )
    return result


def model_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {"unit", "rul"}
    return [c for c in frame.columns if c not in excluded]

