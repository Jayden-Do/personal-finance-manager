from unittest.mock import Mock

import pytest

from app.db.models.user import User
from app.services.user import UserService


@pytest.fixture
def user_repository():
    return Mock()


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


def test_create_user_success(user_service, user_repository):
    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = None

    expected_user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    user_repository.create.return_value = expected_user

    result = user_service.create_user(
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    assert result == expected_user

    user_repository.create.assert_called_once()

    created_user = user_repository.create.call_args.args[0]

    assert created_user.username == "anne"
    assert created_user.email == "anne@example.com"
    assert created_user.password_hash == "hashed-password"


def test_create_user_duplicate_username(user_service, user_repository):
    existing_user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    user_repository.get_by_username.return_value = existing_user

    with pytest.raises(ValueError, match="Username already exists"):
        user_service.create_user(
            username="anne",
            email="new@example.com",
            password_hash="hashed-password",
        )

    user_repository.create.assert_not_called()
    user_repository.get_by_email.assert_not_called()


def test_create_user_duplicate_email(user_service, user_repository):
    existing_user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    user_repository.get_by_username.return_value = None
    user_repository.get_by_email.return_value = existing_user

    with pytest.raises(ValueError, match="Email already exists"):
        user_service.create_user(
            username="newuser",
            email="anne@example.com",
            password_hash="hashed-password",
        )

    user_repository.create.assert_not_called()
