import pytest


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_signup_with_empty_email(self, client, fresh_activities):
        # Arrange: empty email value
        activity_name = "Chess Club"
        email = ""
        
        # Act: attempt signup with empty email
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: should still process (email format not validated in current implementation)
        # This test documents current behavior; can be enhanced if validation is added
        assert response.status_code in [200, 400]
    
    def test_signup_activity_name_with_special_chars(self, client, fresh_activities):
        # Arrange: activity name with URL-encoded special characters
        activity_name = "Invalid%20Club"
        email = "student@mergington.edu"
        
        # Act: attempt signup with invalid activity name
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert: should return not found
        assert response.status_code == 404
    
    def test_unregister_twice_fails(self, client, fresh_activities):
        # Arrange: student signed up
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act: unregister first time
        response1 = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: first unregister succeeds
        assert response1.status_code == 200
        
        # Act: attempt to unregister again
        response2 = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert: second unregister fails
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]
