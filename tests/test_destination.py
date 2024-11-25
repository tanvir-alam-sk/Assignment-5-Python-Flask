import pytest
from unittest.mock import MagicMock


def test_home(client):
    """
    Test home() endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to User"


def test_register_success(client, mocker):
    """
    Test register() - Successful case.
    """
    mocker.patch("model.user.user_exists", return_value=False)
    mocker.patch("model.user.register_user")

    payload = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_missing_fields(client):
    """
    Test register() - Missing fields.
    """
    payload = {"username": "testuser"}  # Missing email and password
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "Username, Email and password are required"


def test_register_user_exists(client, mocker):
    """
    Test register() - User already exists.
    """
    mocker.patch("model.user.user_exists", return_value=True)

    payload = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "Username or Email already taken"


def test_login_success(client, mocker):
    """
    Test login() - Successful case.
    """
    mocker.patch("model.user.authenticate_user", return_value={"email": "test@example.com"})
    mocker.patch("utility.jwt.create_jwt")

    payload = {"email": "test@example.com", "password": "password123"}
    response = client.post("/login", json=payload)
    assert response.status_code == 201
    assert response.json["message"] == "User logged in successfully"


def test_login_invalid_credentials(client, mocker):
    """
    Test login() - Invalid credentials.
    """
    mocker.patch("model.user.authenticate_user", return_value=None)

    payload = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = client.post("/login", json=payload)
    assert response.status_code == 400
    assert response.json["message"] == "Email or Password is not correct"


def test_login_missing_fields(client):
    """
    Test login() - Missing fields.
    """
    payload = {"email": "test@example.com"}  # Missing password
    response = client.post("/login", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "Email and password are required"


def test_get_profile_success(client, mocker):
    """
    Test get_profile() - Successful case.
    """
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")
    mocker.patch("model.user.read_users", return_value=[
        {"email": "test@example.com", "username": "testuser", "password": "password123", "role": "user"}
    ])

    response = client.get("/profile", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json["username"] == "testuser"


def test_get_profile_invalid_token(client, mocker):
    """
    Test get_profile() - Invalid token.
    """
    mocker.patch("utility.jwt.verify_token", return_value=None)

    response = client.get("/profile", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"


def test_get_profile_user_not_found(client, mocker):
    """
    Test get_profile() - User not found.
    """
    mocker.patch("utility.jwt.verify_token", return_value="unknown@example.com")
    mocker.patch("model.user.read_users", return_value=[
        {"email": "test@example.com", "username": "testuser"}
    ])

    response = client.get("/profile", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_update_profile_success(client, mocker):
    """
    Test update_profile() - Successful case.
    """
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")
    mocker.patch("model.user.update_user_info", return_value=True)

    payload = {"email": "test@example.com", "username": "updateduser"}
    response = client.put("/profile", json=payload, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 201
    assert response.json["message"] == "User Information updated successfully"


def test_update_profile_invalid_token(client, mocker):
    """
    Test update_profile() - Invalid token.
    """
    mocker.patch("utility.jwt.verify_token", return_value=None)

    payload = {"email": "test@example.com", "username": "updateduser"}
    response = client.put("/profile", json=payload, headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"


def test_update_profile_forbidden(client, mocker):
    """
    Test update_profile() - Forbidden access.
    """
    mocker.patch("utility.jwt.verify_token", return_value="test@example.com")

    payload = {"email": "wrong@example.com", "username": "updateduser"}
    response = client.put("/profile", json=payload, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 403
    assert response.json["error"] == "Forbidden Access"
