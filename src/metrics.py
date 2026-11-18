"""Evaluation metrics used by the C-MAPSS RUL project."""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def score_predictions(actual, predicted) -> dict[str, float]:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    error = predicted - actual
    # Standard NASA asymmetric score: late predictions receive a steeper penalty.
    terms = np.where(error < 0, np.expm1(-error / 13.0), np.expm1(error / 10.0))
    return {
        "mae": float(mean_absolute_error(actual, predicted)),
        "rmse": float(mean_squared_error(actual, predicted) ** 0.5),
        "nasa_score": float(terms.sum()),
    }

