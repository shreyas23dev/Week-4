# Week 4 — Titanic Survival Prediction API

AI Pioneers Internship (Machine Learning Internship) capstone project.

This is an end-to-end supervised machine-learning application. It trains a Scikit-learn classification pipeline, evaluates it on a held-out test set, saves the fitted pipeline with Joblib, and serves predictions from a FastAPI API and a simple browser form.

## Live deployment

- **Application:** https://week-4-chhg.onrender.com/
- **API documentation:** https://week-4-chhg.onrender.com/docs
- **Health check:** https://week-4-chhg.onrender.com/health

## Project layout

- `train_model.py` — preprocessing, training, testing, metrics, and model serialization.
- `app.py` — FastAPI application with health and prediction endpoints plus a small web form.
- `templates/index.html` — browser-based prediction UI.
- `tests/test_api.py` — API validation and response tests.
- `titanic.csv` — source data.
- `artifacts/titanic_survival_model.joblib` — generated fitted model pipeline.
- `artifacts/model_metadata.json` — generated evaluation and feature metadata.
- `artifacts/test_metrics.json` — held-out performance metrics.
- `presentation.pdf` — capstone presentation slides.
- `presentation_outline.md` and `build_presentation.py` — presentation notes and PDF generator.
- `week4_report.docx` — Word report for internship submission.
- `generate_report_docx.py` — regenerates the Word report from saved evaluation metrics.

## Setup and train

Use Python 3.10+:

```powershell
python -m pip install -r requirements.txt
python train_model.py
```

Training uses a stratified 80/20 train/test split with a fixed random seed. Imputation, encoding, and scaling are inside a Scikit-learn pipeline and are fit on training data only. The output model is the complete preprocessing-plus-classifier pipeline.

On the fixed held-out test split, the trained model achieved 0.810 accuracy, 0.734 F1, and 0.837 ROC AUC. These metrics describe this split and are not a guarantee of future performance.

## Run the API locally

```powershell
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 for the browser form, or http://127.0.0.1:8000/docs for interactive API documentation.

- `GET /health` checks service and model readiness.
- `POST /predict` accepts passenger features and returns the predicted survival class and class probabilities.

Example JSON request:

```json
{
  "pclass": 3,
  "sex": "female",
  "age": 25,
  "sibsp": 0,
  "parch": 0,
  "fare": 8.05,
  "embarked": "S"
}
```

## Tests

Train the model first, then run:

```powershell
pytest -q
```

Regenerate the presentation PDF with `python build_presentation.py`.

## Deploy to Render

The repository includes `render.yaml` for a Render web service. In Render, choose **New + → Blueprint**, connect `shreyas23dev/Week-4`, and deploy the blueprint. Render installs `requirements.txt`, starts Uvicorn on the provided `$PORT`, and checks `/health`. After the first successful deployment, the public service URL can serve the browser form and `/docs` API page. The free instance may sleep when idle and take a short time to wake.

For another ASGI host, use `pip install -r requirements.txt` and `uvicorn app:app --host 0.0.0.0 --port $PORT`.

## Dataset source

Seaborn Titanic example dataset: https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv

Predictions are educational demonstrations from historical data, not authoritative or causal judgments about individuals. Do not use this toy model for consequential real-world decisions.
