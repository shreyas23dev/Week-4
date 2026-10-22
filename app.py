"""FastAPI serving the saved Titanic survival model."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "titanic_survival_model.joblib"
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"

app = FastAPI(
    title="Titanic Survival Prediction API",
    description="Educational FastAPI service for a serialized Scikit-learn survival classifier.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static", check_dir=False), name="static")


class PassengerInput(BaseModel):
    """Validated passenger feature values accepted by the prediction API."""

    model_config = ConfigDict(extra="forbid")

    pclass: Literal[1, 2, 3] = Field(description="Passenger ticket class")
    sex: Literal["female", "male"]
    age: float = Field(ge=0, le=100, description="Passenger age in years")
    sibsp: int = Field(ge=0, le=10, description="Siblings or spouses aboard")
    parch: int = Field(ge=0, le=10, description="Parents or children aboard")
    fare: float = Field(ge=0, le=600, description="Ticket fare")
    embarked: Literal["C", "Q", "S"] = Field(description="Port: Cherbourg, Queenstown, or Southampton")


_model = None


def load_model():
    """Load the serialized pipeline on first use; fail clearly before training."""
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {MODEL_PATH}. Run train_model.py first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> HTMLResponse:
    if not TEMPLATE_PATH.exists():
        raise HTTPException(status_code=500, detail="Prediction form is missing")
    return HTMLResponse(TEMPLATE_PATH.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str | bool]:
    ready = MODEL_PATH.exists()
    return {"status": "ok" if ready else "model_not_trained", "model_loaded": _model is not None, "model_artifact_available": ready}


@app.post("/predict")
def predict(passenger: PassengerInput) -> dict[str, int | str | float]:
    try:
        model = load_model()
    except (FileNotFoundError, OSError, ValueError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    row = pd.DataFrame([passenger.model_dump()])
    prediction = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    classes = list(model.named_steps["classifier"].classes_)
    positive_index = classes.index(1)
    return {
        "prediction": prediction,
        "prediction_label": "survived" if prediction == 1 else "did not survive",
        "probability_not_survived": float(probabilities[classes.index(0)]),
        "probability_survived": float(probabilities[positive_index]),
        "model": "RandomForestClassifier",
        "notice": "Educational estimate only; not for consequential decisions.",
    }
