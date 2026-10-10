import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_activity_names():
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Programming Class" in payload
    assert "Gym Class" in payload
    assert "Chess Club" in payload


def test_duplicate_signup_is_rejected():
    # Arrange
    # Act
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "emma@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    # Arrange
    # Act
    response = client.delete(
        "/activities/Programming%20Class/unregister",
        params={"email": "emma@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert "emma@mergington.edu" not in response.json()["participants"]
