import pytest
from fastapi.testclient import TestClient
import copy
from src.app import app, activities as original_activities


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """Reset activities dict to original state before each test (Arrange phase)"""
    # Create a deep copy to avoid modifying the original
    reset_activities = copy.deepcopy(original_activities)
    # Monkeypatch the activities dict in the app module
    monkeypatch.setattr("src.app.activities", reset_activities)
    return reset_activities
