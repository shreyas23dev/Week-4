from fastapi.testclient import TestClient

import app as api


client = TestClient(api.app)


class FakeModel:
    named_steps = {"classifier": type("Classifier", (), {"classes_": [0, 1]})()}

    def predict(self, frame):
        assert list(frame.columns) == ["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]
        return [1]

    def predict_proba(self, frame):
        return [[0.2, 0.8]]


def test_health_reports_artifact_availability(monkeypatch, tmp_path):
    monkeypatch.setattr(api, "MODEL_PATH", tmp_path / "model.joblib")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "model_not_trained"


def test_homepage_serves_form():
    response = client.get("/")
    assert response.status_code == 200
    assert "Titanic Survival Estimator" in response.text


def test_predict_returns_class_and_probability(monkeypatch):
    monkeypatch.setattr(api, "load_model", lambda: FakeModel())
    response = client.post(
        "/predict",
        json={
            "pclass": 3,
            "sex": "female",
            "age": 25,
            "sibsp": 0,
            "parch": 0,
            "fare": 8.05,
            "embarked": "S",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["prediction"] == 1
    assert payload["probability_survived"] == 0.8
    assert payload["prediction_label"] == "survived"


def test_predict_rejects_invalid_category():
    response = client.post(
        "/predict",
        json={
            "pclass": 4,
            "sex": "unknown",
            "age": -1,
            "sibsp": 0,
            "parch": 0,
            "fare": 8.05,
            "embarked": "S",
        },
    )
    assert response.status_code == 422


def test_predict_returns_service_unavailable_before_training(monkeypatch):
    def missing_model():
        raise FileNotFoundError("Run train_model.py first")

    monkeypatch.setattr(api, "load_model", missing_model)
    response = client.post(
        "/predict",
        json={
            "pclass": 2,
            "sex": "male",
            "age": 32,
            "sibsp": 0,
            "parch": 0,
            "fare": 13,
            "embarked": "C",
        },
    )
    assert response.status_code == 503
