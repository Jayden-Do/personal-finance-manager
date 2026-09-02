from unittest.mock import Mock

from app.db.models.user import User
from app.repositories.user import UserRepository


def test_create():
    session = Mock()
    repository = UserRepository(session)

    user = User(
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    result = repository.create(user)

    session.add.assert_called_once_with(user)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(user)

    assert result == user


def test_get_by_id():
    session = Mock()

    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    session.exec.return_value.first.return_value = user

    repository = UserRepository(session)

    result = repository.get_by_id(1)

    assert result == user
    session.exec.assert_called_once()


def test_get_by_id_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = UserRepository(session)

    result = repository.get_by_id(999)

    assert result is None


def test_get_by_username():
    session = Mock()

    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    session.exec.return_value.first.return_value = user

    repository = UserRepository(session)

    result = repository.get_by_username("anne")

    assert result == user
    session.exec.assert_called_once()


def test_get_by_username_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = UserRepository(session)

    result = repository.get_by_username("unknown")

    assert result is None


def test_get_by_email():
    session = Mock()

    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    session.exec.return_value.first.return_value = user

    repository = UserRepository(session)

    result = repository.get_by_email("anne@example.com")

    assert result == user
    session.exec.assert_called_once()


def test_get_by_email_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = UserRepository(session)

    result = repository.get_by_email("unknown@example.com")

    assert result is None
