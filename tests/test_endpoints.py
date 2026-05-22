import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        # Arrange: activities are already loaded in fixture
        
        # Act: fetch activities
        response = client.get("/activities")
        
        # Assert: verify response
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9  # Should have all 9 activities
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_structure(self, client, fresh_activities):
        # Arrange: expected activity fields
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act: fetch activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert: each activity has required fields
        for activity_name, activity_data in data.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_get_activities_participant_count(self, client, fresh_activities):
        # Arrange: known initial participant counts
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Basketball Team": 1
        }
        
        # Act: fetch activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert: verify participant counts
        for activity, count in expected_counts.items():
            assert len(data[activity]["participants"]) == count


class TestSignup:
    """Test POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, fresh_activities):
        # Arrange: new student and activity
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act: sign up for activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: verify response and side effects
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in fresh_activities[activity_name]["participants"]
        assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1
    
    def test_signup_duplicate_error(self, client, fresh_activities):
        # Arrange: student already signed up
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act: attempt to sign up again
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: verify error response
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_activity_not_found(self, client, fresh_activities):
        # Arrange: invalid activity name
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act: attempt to sign up for invalid activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: verify not found error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregister:
    """Test POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, fresh_activities):
        # Arrange: student currently signed up
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act: unregister from activity
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: verify response and side effects
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in fresh_activities[activity_name]["participants"]
        assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1
    
    def test_unregister_not_signed_up_error(self, client, fresh_activities):
        # Arrange: student not signed up for activity
        activity_name = "Tennis Club"
        email = "michael@mergington.edu"  # Not in Tennis Club
        
        # Act: attempt to unregister
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: verify error response
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_activity_not_found(self, client, fresh_activities):
        # Arrange: invalid activity name
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act: attempt to unregister from invalid activity
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: verify not found error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
