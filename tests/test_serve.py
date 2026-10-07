from fastapi.testclient import TestClient
from src.serve import app


def test_api(trained, monkeypatch):
    monkeypatch.delenv("ARTIFACT_BUCKET", raising=False)
    monkeypatch.setenv("MODEL_PATH", "models/model.joblib")
    with TestClient(app) as client:
        assert client.get("/healthz").json() == {"status": "ok"}
        result = client.post("/score", json={"features": [0.5] * 10})
        assert result.status_code == 200
        pred = result.json()["prediction"]
        assert pred in (0, 1)
        assert result.json()["label"] == ("thu_nhap_cao" if pred else "thu_nhap_thap")
        assert client.post("/score", json={"features": [1, 2]}).status_code == 400
