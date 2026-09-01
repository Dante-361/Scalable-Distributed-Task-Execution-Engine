from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Distributed Job System API"
    }


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "task": "calculate_sum",
            "payload": {
                "a": 10,
                "b": 20
            }
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["task"] == "calculate_sum"
    assert data["payload"] == {
        "a": 10,
        "b": 20
    }

def test_get_job():
    create_response = client.post(
        "/jobs",
        json={
            "task": "calculate_sum",
            "payload": {
                "a": 10,
                "b": 20,
            },
        },
    )

    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["id"] == job_id


def test_get_nonexistent_job():
    response = client.get(
        "/jobs/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404