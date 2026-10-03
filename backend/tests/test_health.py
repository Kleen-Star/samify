from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["data"]["database"] == "connected"


def test_unknown_route_uses_error_format():
    r = client.get("/api/nope")
    assert r.status_code == 404
    assert r.json()["success"] is False


def test_cors_allows_configured_origin():
    r = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_rejects_other_origin():
    r = client.get("/api/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in r.headers
