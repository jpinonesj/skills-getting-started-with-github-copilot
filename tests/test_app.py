from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Programming Class"
    email = "not-registered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 404
