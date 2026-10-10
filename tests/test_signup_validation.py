import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "emma@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    response = client.delete(
        "/activities/Programming%20Class/unregister",
        params={"email": "emma@mergington.edu"},
    )

    assert response.status_code == 200
    assert "emma@mergington.edu" not in response.json()["participants"]
