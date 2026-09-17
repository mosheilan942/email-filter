import pytest
from app import app

# Create a fixture to configure the Flask app for testing
@pytest.fixture
def client():
    # Set testing configuration to True so errors propagate beautifully
    app.config['TESTING'] = True
    
    # Establish a test client to simulate HTTP requests
    with app.test_client() as client:
        yield client

# Test the home page route ('/')
def test_home_page(client):
    response = client.get('/')
    
    # Assertions to verify the status code and page content
    assert response.status_code == 200
    assert b"Hello, Developer!" in response.data
    assert b"Current Status:" in response.data

# Test the dynamic user profile route ('/user/<username>')
def test_user_profile_page(client):
    response = client.get('/user/john_doe')
    
    # Verify dynamic content handles parameters correctly
    assert response.status_code == 200
    assert b"Profile page for user: john_doe" in response.data
