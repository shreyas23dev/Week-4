"""Train, evaluate, and serialize the Titanic survival pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "titanic.csv"
ARTIFACT_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "titanic_survival_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "test_metrics.json"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"
NUMERIC_FEATURES = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_FEATURES = ["pclass", "sex", "embarked"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "survived"
RANDOM_STATE = 42


def make_pipeline() -> Pipeline:
    """Build an end-to-end preprocessing and classification pipeline."""
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ]
    )
    classifier = RandomForestClassifier(
        n_estimators=250,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    return Pipeline([("preprocessor", preprocessing), ("classifier", classifier)])


def train_and_evaluate() -> dict[str, Any]:
    """Fit on training records, evaluate on a held-out test set, and save artifacts."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")
    data = pd.read_csv(DATA_PATH)
    missing = set(FEATURES + [TARGET]).difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

    X = data[FEATURES]
    y = data[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    model = make_pipeline()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics: dict[str, Any] = {
        "model": "RandomForestClassifier",
        "random_state": RANDOM_STATE,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=[0, 1]).tolist(),
        "classification_report": classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["not_survived", "survived"],
            output_dict=True,
            zero_division=0,
        ),
    }

    ARTIFACT_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    metadata = {
        "model": metrics["model"],
        "features": FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "target": TARGET,
        "classes": {"0": "not survived", "1": "survived"},
        "dataset_rows": int(len(data)),
        "test_metrics_file": METRICS_PATH.name,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    results = train_and_evaluate()
    print("Held-out test metrics:")
    for metric in ("accuracy", "precision", "recall", "f1", "roc_auc"):
        print(f"  {metric}: {results[metric]:.3f}")
    print(f"Saved fitted pipeline: {MODEL_PATH}")
    print(f"Saved test metrics: {METRICS_PATH}")
