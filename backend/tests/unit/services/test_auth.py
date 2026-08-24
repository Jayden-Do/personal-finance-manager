from unittest.mock import Mock, patch

import pytest

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import AuthService


@pytest.fixture
def user_service():
    return Mock()


@pytest.fixture
def auth_service(user_service):
    return AuthService(user_service)


def test_register_success(auth_service, user_service):
    user_data = UserCreate(
        username="anne",
        email="anne@example.com",
        password="plain-password",
    )

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
        result = auth_service.register(user_data)

    assert result == created_user

    mock_hash_password.assert_called_once_with("plain-password")

    user_service.create_user.assert_called_once_with(
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )
