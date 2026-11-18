"""Train and evaluate two RUL baselines on NASA C-MAPSS FD001."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .cmapss import ROOT, SENSOR_COLUMNS, add_features, load_test, load_train, model_columns
from .metrics import score_predictions


def final_cycle_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values("cycle").groupby("unit", as_index=False).tail(1).sort_values("unit")


def main() -> None:
    subset = "FD001"
    output = ROOT / "reports" / "generated"
    models_dir = ROOT / "models"
    output.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    raw_train = load_train(subset)
    data = add_features(raw_train)
    columns = model_columns(data)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, valid_idx = next(splitter.split(data[columns], data["rul"], groups=data["unit"]))
    train_part = data.iloc[train_idx]
    valid_part = data.iloc[valid_idx]
    valid_last = final_cycle_rows(valid_part)

    models = {
        "ridge": make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
        "random_forest": RandomForestRegressor(
            n_estimators=250, min_samples_leaf=2, max_features=0.8,
            n_jobs=-1, random_state=42,
        ),
    }
    validation = {}
    for name, model in models.items():
        model.fit(train_part[columns], train_part["rul"])
        prediction = np.clip(model.predict(valid_last[columns]), 0, None)
        validation[name] = score_predictions(valid_last["rul"], prediction)

    # Select by validation MAE, then refit on all training engines.
    best_name = min(validation, key=lambda name: validation[name]["mae"])
    best_model = models[best_name]
    best_model.fit(data[columns], data["rul"])

    raw_test, test_truth = load_test(subset)
    test_data = add_features(raw_test)
    test_last = final_cycle_rows(test_data)
    test_prediction = np.clip(best_model.predict(test_last[columns]), 0, None)
    test_metrics = score_predictions(test_truth, test_prediction)
    test_last = test_last.copy()
    test_last["actual_rul"] = test_truth
    test_last["predicted_rul"] = test_prediction
    test_last[["unit", "actual_rul", "predicted_rul"]].to_csv(
        output / "fd001_test_predictions.csv", index=False
    )

    result = {
        "subset": subset,
        "validation_method": "80/20 engine-level split; final observed cycle per held-out engine",
        "validation_engines": int(valid_last["unit"].nunique()),
        "validation": validation,
        "selected_model": best_name,
        "test_engines": int(len(test_truth)),
        "test": test_metrics,
    }
    (output / "metrics.json").write_text(json.dumps(result, indent=2) + "\n")
    joblib.dump({"model": best_model, "columns": columns, "subset": subset}, models_dir / "fd001_rul.joblib")

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.scatter(test_truth, test_prediction, alpha=0.72, color="#147D92", edgecolor="white", linewidth=0.35)
    limit = max(float(np.max(test_truth)), float(np.max(test_prediction)), 1)
    ax.plot([0, limit], [0, limit], linestyle="--", color="#D6633D", label="Ideal prediction")
    ax.set(xlabel="Actual RUL (cycles)", ylabel="Predicted RUL (cycles)",
           title=f"NASA C-MAPSS FD001 test set — {best_name.replace('_', ' ').title()}")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output / "fd001_test_scatter.png", dpi=180)
    plt.close(fig)

    importance = pd.DataFrame({"feature": columns, "importance": best_model.feature_importances_})
    importance = importance.sort_values("importance", ascending=False).head(15)
    importance.to_csv(output / "fd001_feature_importance.csv", index=False)
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    ordered = importance.sort_values("importance")
    ax.barh(ordered["feature"], ordered["importance"], color="#147D92")
    ax.set(title="Top 15 feature importances — FD001", xlabel="Random forest importance")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(output / "fd001_feature_importance.png", dpi=180)
    plt.close(fig)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

