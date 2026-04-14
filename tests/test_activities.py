from src import app as app_module


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]
    assert payload["Chess Club"]["schedule"]
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_adds_new_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload == {"detail": "Activity not found"}


def test_signup_returns_400_for_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload == {"detail": "Student already signed up for this activity"}


def test_delete_unregisters_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_delete_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload == {"detail": "Activity not found"}


def test_delete_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload == {"detail": "Participant not found in this activity"}