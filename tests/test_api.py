from fastapi.testclient import TestClient

from maat import __version__
from maat.api import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "system": "MAAT", "version": __version__}
    assert response.headers["x-content-type-options"] == "nosniff"


def test_ready_reports_core() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["core"] == "ready"


def test_demo_ui_is_served() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "MAAT // UNIVERSAL CASEGRAPH" in response.text
    assert "/static/app.js" in response.text


def test_build_case_endpoint() -> None:
    response = client.post(
        "/build-case",
        json={"text": "Sam owns the API. Deployment depends on the API."},
    )
    assert response.status_code == 200
    body = response.json()
    assert "graph" in body
    assert "receipt" in body
    assert body["receipt"]["status"] == "PASS"
    assert body["meta"]["pipeline"][-1] == "RECEIPT"


def test_blank_case_rejected() -> None:
    response = client.post("/build-case", json={"text": "   "})
    assert response.status_code == 422
