import pytest

from app.db.models.user import User
from app.services.user import UserService


class FakeUserRepository:
    def __init__(self):
        self.users = []

    def get_by_username(self, username: str):
        for user in self.users:
            if user.username == username:
                return user

        return None

    def get_by_email(self, email: str):
        for user in self.users:
            if user.email == email:
                return user

        return None

    def create(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)

        return user


def test_register_user_successfully():
    repository = FakeUserRepository()
    service = UserService(repository)

    user = service.register_user(
        username="anne",
        email="anne@example.com",
        password="password123",
    )

    assert user.id == 1
    assert user.username == "anne"
    assert user.email == "anne@example.com"
    assert user.password_hash == "password123"


def test_register_user_with_existing_username():
    repository = FakeUserRepository()
    service = UserService(repository)

    repository.create(
        User(
            username="anne",
            email="anne@example.com",
            password_hash="hash",
        )
    )

    with pytest.raises(ValueError, match="Username already exists"):
        service.register_user(
            username="anne",
            email="another@example.com",
            password="password123",
        )


def test_register_user_with_existing_email():
    repository = FakeUserRepository()
    service = UserService(repository)

    repository.create(
        User(
            username="anne",
            email="anne@example.com",
            password_hash="hash",
        )
    )

    with pytest.raises(ValueError, match="Email already exists"):
        service.register_user(
            username="another",
            email="anne@example.com",
            password="password123",
        )
