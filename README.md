# Predictive Maintenance of Aircraft Turbofan Engines Using Machine Learning

This project estimates remaining useful life (RUL) from multivariate turbofan sensor sequences. It uses NASA's simulated C-MAPSS benchmark and currently implements a reproducible FD001 baseline.

**Public GitHub repository:** https://github.com/kaushikkakad/PDS-project

**Project status:** approximately 40% complete and still in progress. The current implementation covers the FD001 data pipeline and first baseline evaluation. Error analysis, more robust validation, broader comparisons, and final refinement remain.

## Current result

The current run compares Ridge regression and a Random Forest. Validation holds out complete engines (80/20 split, seed 42) and scores the final observed cycle for each held-out engine. The Random Forest was selected by validation MAE and then refit on all FD001 training engines.

| Evaluation | Model | Engines | MAE (cycles) | RMSE (cycles) | NASA score (lower is better) |
|---|---:|---:|---:|---:|---:|
| Engine-level validation | Ridge | 20 | 4.44 | 7.55 | 18.44 |
| Engine-level validation | Random Forest | 20 | 1.89 | 2.20 | 4.32 |
| Official FD001 test set | Selected Random Forest | 100 | 13.83 | 18.87 | 632.61 |

The gap between validation and official test performance is a central finding. The validation split alone is not sufficient to claim robust generalization. Results in `reports/generated/metrics.json` are from the current run.

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python scripts/download_data.py
python -m src.train
```

The download script saves NASA's public C-MAPSS archive to `data/raw/`. Raw data, trained model files, and generated plots are excluded from Git by `.gitignore`; they are recreated locally by the commands above.

## Project structure

```text
src/cmapss.py       Data loading, target creation, and rolling features
src/metrics.py      MAE, RMSE, and asymmetric NASA score
src/train.py        Engine-level validation, model selection, test evaluation, plots
scripts/download_data.py
reports/             Update report and generated experiment artifacts
```

## Method

- **Target:** cycles remaining until run-to-failure, capped at 125 cycles.
- **Features:** operating settings, current sensor measurements, and per-engine trailing five-cycle sensor means and standard deviations.
- **Validation:** complete engines are held out with `GroupShuffleSplit`, avoiding cycles from the same engine on both sides.
- **Models:** scaled Ridge regression and a 250-tree Random Forest.
- **Metrics:** MAE and RMSE in cycles, plus the standard asymmetric NASA score.
- **Primary subset:** FD001 (single operating condition and one simulated fault mode).

## Limitations and next work

This benchmark is simulated and does not establish safety or operational readiness for real aircraft. Current results cover FD001 only; the official test score is substantially worse than the validation score. Next steps are to diagnose this gap, evaluate the other C-MAPSS subsets, compare temporal models such as GRU/LSTM, and document reproducibility and error analysis.

## Data citation

Saxena, A., & Goebel, K. (2008). *Turbofan Engine Degradation Simulation Data Set*. NASA Ames Prognostics Data Repository, NASA Ames Research Center. The C-MAPSS dataset is described on the [NASA Prognostics Center of Excellence repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) and the [NASA Open Data Portal](https://data.nasa.gov/dataset/c-mapss-aircraft-engine-simulator-data).

