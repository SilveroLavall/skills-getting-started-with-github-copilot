class TestRedirect:
    """Test GET / redirect endpoint"""
    
    def test_root_redirects_to_static(self, client):
        # Arrange: request root path
        
        # Act: make GET request to root
        response = client.get("/", follow_redirects=False)
        
        # Assert: verify redirect
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
    
    def test_root_redirect_followed(self, client):
        # Arrange: follow redirects enabled
        
        # Act: make GET request with follow_redirects
        response = client.get("/", follow_redirects=True)
        
        # Assert: should eventually reach a valid response
        assert response.status_code == 200
