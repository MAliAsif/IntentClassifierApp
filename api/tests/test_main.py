

import pytest

from fastapi.testclient import TestClient
from api.main import app  # Import the FastAPI app from the main module
import time

import uuid


client = TestClient(app)

# Ensure the model is loaded before testing
@pytest.fixture(scope="module", autouse=True)
def setup_model():
    # Simply make a request to the root endpoint to trigger the startup event
    with TestClient(app) as client:
        client.get("/")  # This will trigger the startup event to load the model

    time.sleep(1)  # Sleep for a second to allow model loading if necessary

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health_check():
    # Simulate a GET request to the /api/health endpoint
    response = client.get("/api/health")
    assert response.status_code == 200
    


# Register a user and return JWT token
@pytest.fixture()
def register_user():
   # Generate a unique email using uuid
    unique_email = f"{uuid.uuid4().hex}@xyz.com"
    
    # Simulate user registration with the unique email
    response = client.post("/user/signup", json={
        "fullname": "Joe Doe", 
        "email": unique_email,  # Use the generated unique email
        "password": "any"
    })

    print("Response status code:", response.status_code)
    print("Response content:", response.json())  # Print the response for debugging
    
    assert response.status_code == 200
    return response.json()["access_token"]  # Return the JWT token for use in tests


def test_classify(register_user):
    # Simulate a valid single query request with JWT token
    response = client.post(
        "/api/classify", 
        json={"text": "Search hotels."},
        headers={"Authorization": f"Bearer {register_user}"}  # Adding the token here only for this test
    )
    
    if response.status_code != 200:
        print("ERROR DIAGNOSED TO BE HERE")
        print(response.json())  # Print response content for debugging
    
    assert response.status_code == 200
    assert "intent" in response.json()
    assert "confidence" in response.json()


def test_classify_invalid_input(register_user):
    # Simulate an invalid input (missing text field)
    response = client.post(
        "/api/classify", 
        json={}, 
        headers={"Authorization": f"Bearer {register_user}"}  # Adding the token here for invalid input test
    )
    
    if response.status_code != 200:
        print("ERROR DIAGNOSED TO BE HERE")
        print(response.json())  # Print response content for debugging
    
    assert response.status_code == 422  # 403 because invalid input will return a "Wrong login details" message, whose code is 403



def test_classify_batch(register_user):
    # Simulate a valid batch request with JWT token
    response = client.post(
        "/api/classify/batch", 
        json={"texts": ["How can I build a website?", "What's the weather like today?"]},
        headers={"Authorization": f"Bearer {register_user}"}  # Adding the token here only for this test
    )
    
    if response.status_code != 200:
        print("ERROR DIAGNOSED TO BE HERE")
        print(response.json())  # Print response content for debugging
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Make sure each result contains "query", "intent", and "confidence"
    for result in response.json():
        assert "query" in result
        assert "intent" in result
        assert "confidence" in result




def test_classify_batch_invalid_input(register_user):
    # Simulate an invalid batch input (missing texts field)
    response = client.post(
        "/api/classify/batch", 
        json={}, 
        headers={"Authorization": f"Bearer {register_user}"}  # Adding the token here for invalid input test
    )
    
    if response.status_code != 200:
        print("ERROR DIAGNOSED TO BE HERE")
        print(response.json())  # Print response content for debugging
    
    assert response.status_code == 422  # 403 for invalid input

