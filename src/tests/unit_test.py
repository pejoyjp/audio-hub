import json
from fastapi.testclient import TestClient
from ..database import Base, SessionLocal, engine
from ..main import app  # Assuming your FastAPI app is in a module named "main"

client = TestClient(app)
db = SessionLocal()

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # metadata.drop_all()
    db.commit()

def test_create_user():
    reset_db()


    valid_user1_data = {
        "username": "testuser1valid",
        "email": "testuser1@example.com",
        "password": "TestPassword123",
        "alias": "TestAlias"
    }

    # Send a POST request to the /users endpoint with the valid user data
    response = client.post("/users", json=valid_user1_data)

    # Assert that the response has a 201 status code, indicating success
    assert response.status_code == 201

    # Parse the response JSON and assert that it matches the expected user data
    user_response = response.json()
    assert user_response["username"] == valid_user1_data["username"]
    assert user_response["email"] == valid_user1_data["email"]
    assert user_response["alias"] == valid_user1_data["alias"]

    # A new user with the same alias. Should be possible
    valid_user2_data = {
        "username": "testuser2valid",
        "email": "testuser2@example.com",
        "password": "TestPassword132",
        "alias": "TestAlias"
    }

    # Send a POST request to the /users endpoint with the valid user data
    response = client.post("/users", json=valid_user2_data)

    # Assert that the response has a 201 status code, indicating success
    assert response.status_code == 201

    # Define an invalid user payload with a password that doesn't meet validation criteria
    invalid_user1_data = {
        "username": "invaliduser1",
        "email": "invaliduser1@example.com",
        "password": "invalid",
        "alias": "invaliduseralias"
    }

    # Send a POST request to the /users endpoint with the invalid user data
    response = client.post("/users", json=invalid_user1_data)

    # Assert that the response has a 422 status code, indicating validation error
    assert response.status_code == 422

    # Define an invalid user payload with a username that doesn't meet validation criteria
    invalid_user2_data = {
        "username": "testuser1valid",
        "email": "invaliduser2@example.com",
        "password": "Invalid2_00",
        "alias": "invaliduser2alias"
    }

    # Send a POST request to the /users endpoint with the invalid user data
    response = client.post("/users", json=invalid_user2_data)

    # Assert that the response has a 400 status code, indicating username repetition error
    assert response.status_code == 400

    # Define an invalid user payload with a username that doesn't meet validation criteria
    invalid_user3_data = {
        "username": "invaliduser3",
        "email": "testuser2@example.com",
        "password": "Invalid3_00",
        "alias": "invaliduser3alias"
    }

    # Send a POST request to the /users endpoint with the invalid user data
    response = client.post("/users", json=invalid_user3_data)

    # Assert that the response has a 400 status code, indicating email repetition error
    assert response.status_code == 400
    reset_db()

def test_login():
    reset_db()

    # Create a user for testing
    valid_user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPassword123",
        "alias": "TestAlias"
    }
    client.post("/users", json=valid_user_data)

    # Test valid login
    login_data = {
        "username": "testuser",
        "password": "TestPassword123"
    }
    response = client.post("/login", data=login_data)

    # Assert that the response has a 200 status code, indicating success
    assert response.status_code == 200

    # Validate the response JSON
    token_response = response.json()
    assert "access_token" in token_response
    assert "refresh_token" in token_response

    # Test login with invalid password
    invalid_login_data = {
        "username": "testuser",
        "password": "InvalidPassword"
    }
    response = client.post("/login", data=invalid_login_data)

    # Assert that the response has a 401 status code, indicating invalid credentials
    assert response.status_code == 401

    # Test login with invalid username
    invalid_username_data = {
        "username": "invaliduser",
        "password": "TestPassword123"
    }
    response = client.post("/login", data=invalid_username_data)

    # Assert that the response has a 404 status code, indicating user not registered
    assert response.status_code == 404

    # Test login with missing credentials
    missing_credentials_data = {}
    response = client.post("/login", data=missing_credentials_data)

    # Assert that the response has a 422 status code, indicating validation error
    assert response.status_code == 422
    reset_db()

