from fastapi.testclient import TestClient
from main import app


def test_parts():
    c = TestClient(app)
    r = c.get("/parts")
    assert r.status_code == 200
    assert "box" in r.json()["parts"]


def test_generate_box():
    c = TestClient(app)
    r = c.post(
        "/generate",
        json={"part": "box", "params": {"w": 10, "h": 10, "t": 5}, "format": "step"},
    )
    assert r.status_code == 200
    assert len(r.content) > 0


def test_unknown_part():
    c = TestClient(app)
    r = c.post("/generate", json={"part": "nope", "params": {}})
    assert r.status_code == 400


def test_generate_star():
    c = TestClient(app)
    r = c.post(
        "/generate",
        json={
            "part": "star",
            "params": {"points": 5, "r_out": 10, "r_in": 4, "t": 3},
            "format": "step",
        },
    )
    assert r.status_code == 200
    assert len(r.content) > 0


def test_invalid_params():
    c = TestClient(app)
    r = c.post(
        "/generate",
        json={"part": "box", "params": {"w": -1, "h": 10, "t": 5}},
    )
    assert r.status_code == 400
