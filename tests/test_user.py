import pytest
from unittest.mock import MagicMock
from flask import Flask, jsonify, request
from app import home, register, login, get_profile, update_profile  # Import your functions here
from utility.jwt import create_jwt, verify_token

@pytest.fixture
def client():
    app = Flask(__name__)
    app.testing = True

    app.add_url_rule("/", "home", home)
    app.add_url_rule("/register", "register", register, methods=["POST"])
    app.add_url_rule("/login", "login", login, methods=["POST"])
    app.add_url_rule("/profile", "get_profile", get_profile, methods=["GET"])
    app.add_url_rule("/profile", "update_profile", update_profile, methods=["PUT"])

    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home route."""
    response = client.get("/")
    assert response.data == b"Welcome to User"
    assert response.status_code == 200


def test_register_success(client, mocker):
    """Test successful registration."""
    mocker.patch("model.user.user_exists", return_value=False)
    mocker.patch("model.user.register_user")

    payload = {"username": "test_user", "email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=payload)

    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_missing_fields(client):
    """Test registration with missing fields."""
    payload = {"username": "test_user", "email": "test@example.com"}
    response = client.post("/register", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Username, Email and password are required"


def test_register_user_exists(client, mocker):
    """Test registration when username or email already exists."""
    mocker.patch("model.user.user_exists", return_value=True)

    payload = {"username": "test_user", "email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Username or Email already taken"


def test_login_success(client, mocker):
    """Test successful login."""
    mocker.patch("model.user.authenticate_user", return_value=True)
    mocker.patch("utility.jwt.create_jwt", return_value="mock_jwt_token")

    payload = {"email": "test@example.com", "password": "password123"}
    response = client.post("/login", json=payload)

    assert response.status_code == 201
    assert response.json["message"] == "User logged in successfully"


def test_login_missing_fields(client):
    """Test login with missing fields."""
    payload = {"email": "test@example.com"}
    response = client.post("/login", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Email and password are required"


def test_login_invalid_credentials(client, mocker):
    """Test login with invalid credentials."""
    mocker.patch("model.user.authenticate_user", return_value=None)

    payload = {"email": "test@example.com", "password": "wrongpassword"}
    response = client.post("/login", json=payload)

    assert response.status_code == 400
    assert response.json["message"] == "Email or Password is not correct"


def test_get_profile_success(client, mocker):
    """Test get profile successfully."""
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")
    mocker.patch("model.user.read_users", return_value=[
        {"username": "test_user", "email": "test@example.com", "password": "password123", "role": "user"}
    ])

    response = client.get("/profile", headers={"Authorization": verify_token})

    assert response.status_code == 200
    assert response.json["username"] == "test_user"


def test_get_profile_invalid_token(client, mocker):
    """Test get profile with invalid token."""
    mocker.patch("utility.jwt.verify_token", return_value=None)

    response = client.get("/profile", headers={"Authorization": verify_token})

    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"


def test_update_profile_success(client, mocker):
    """Test successful profile update."""
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")
    mocker.patch("model.user.update_user_info", return_value=True)

    payload = {"email": "test@example.com", "username": "new_username"}
    response = client.put("/profile", json=payload, headers={"Authorization": verify_token})

    assert response.status_code == 201
    assert response.json["message"] == "User Information updated successfully"


def test_update_profile_forbidden(client, mocker):
    """Test profile update with forbidden access."""
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")

    payload = {"email": "wrong_email@example.com", "username": "new_username"}
    response = client.put("/profile", json=payload, headers={"Authorization": verify_token})

    assert response.status_code == 403
    assert response.json["error"] == "Forbidden Access"
