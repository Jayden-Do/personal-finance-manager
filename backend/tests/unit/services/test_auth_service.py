from unittest.mock import Mock, patch
from fastapi import HTTPException, status

import pytest

from app.db.models.user import User
from app.services.auth import AuthService


@pytest.fixture
def user_service():
    return Mock()


@pytest.fixture
def auth_service(user_service):
    return AuthService(user_service)


def test_register_success(auth_service, user_service):

    created_user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    user_service.create_user.return_value = created_user

    with patch(
        "app.services.auth.hash_password",
        return_value="hashed-password",
    ) as mock_hash_password:
        result = auth_service.register(
            username="anne", email="anne@example.com", password="plain-password"
        )

    assert result == created_user

    mock_hash_password.assert_called_once_with("plain-password")

    user_service.create_user.assert_called_once_with(
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )


def test_login_success(auth_service, user_service):
    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )
    user_service.get_user_by_name.return_value = user

    with (
        patch(
            "app.services.auth.verify_password",
            return_value=True,
        ) as mock_verify_password,
        patch(
            "app.services.auth.create_access_token",
            return_value="access-token",
        ) as mock_create_access_token,
    ):
        result = auth_service.login(
            username="anne",
            password="plain-password",
        )

    assert result == "access-token"

    user_service.get_user_by_name.assert_called_once_with("anne")
    mock_verify_password.assert_called_once_with(
        "plain-password",
        "hashed-password",
    )
    mock_create_access_token.assert_called_once_with(
        user_id=1,
        username="anne",
    )


def test_login_user_not_found(auth_service, user_service):
    user_service.get_user_by_name.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        auth_service.login(
            username="anne",
            password="plain-password",
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid username or password"

    user_service.get_user_by_name.assert_called_once_with("anne")


def test_login_wrong_password(auth_service, user_service):
    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )
    user_service.get_user_by_name.return_value = user

    with patch(
        "app.services.auth.verify_password",
        return_value=False,
    ) as mock_verify_password:
        with pytest.raises(HTTPException) as exc_info:
            auth_service.login(
                username="anne",
                password="wrong-password",
            )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid username or password"

    user_service.get_user_by_name.assert_called_once_with("anne")
    mock_verify_password.assert_called_once_with(
        "wrong-password",
        "hashed-password",
    )
