from fastapi.testclient import TestClient

from maat.api import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "system": "MAAT"}


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
