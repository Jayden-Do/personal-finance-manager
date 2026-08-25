import jwt
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.dependencies.auth import get_current_user
from app.db.models.user import User


def test_get_current_user_success():
    user_service = Mock()

    user = User(
        id=1,
        username="anne",
        email="anne@example.com",
        password_hash="hashed-password",
    )

    user_service.get_user_by_id.return_value = user

    with patch(
        "app.dependencies.auth.decode_access_token",
        return_value={
            "sub": "1",
            "username": "anne",
        },
    ):
        result = get_current_user(
            token="valid-token",
            user_service=user_service,
        )

    assert result == user
    user_service.get_user_by_id.assert_called_once_with(1)


def test_get_current_user_invalid_token():
    user_service = Mock()

    with patch(
        "app.dependencies.auth.decode_access_token",
        return_value=None,
    ):
        try:
            get_current_user(
                token="invalid-token",
                user_service=user_service,
            )
        except HTTPException as exc:
            assert exc.status_code == 401
            assert exc.detail == "Invalid or expired token"
        else:
            assert False, "Expected HTTPException"


import pytest


def test_get_current_user_invalid_token():
    user_service = Mock()

    with patch(
        "app.dependencies.auth.decode_access_token",
        side_effect=jwt.InvalidTokenError,
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                token="invalid-token",
                user_service=user_service,
            )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired token"


def test_get_current_user_missing_user_id():
    user_service = Mock()

    with patch(
        "app.dependencies.auth.decode_access_token",
        return_value={
            "username": "anne",
        },
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                token="valid-token",
                user_service=user_service,
            )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"


def test_get_current_user_user_not_found():
    user_service = Mock()
    user_service.get_user_by_id.return_value = None

    with patch(
        "app.dependencies.auth.decode_access_token",
        return_value={
            "sub": "999",
            "username": "unknown",
        },
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                token="valid-token",
                user_service=user_service,
            )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not found"
