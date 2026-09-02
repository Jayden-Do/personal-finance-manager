from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.security.jwt import (
    create_access_token,
    decode_access_token,
)
from app.core.config import settings


def test_create_access_token():
    token = create_access_token(
        user_id=1,
        username="anne",
    )

    assert isinstance(token, str)


def test_decode_access_token():
    token = create_access_token(
        user_id=1,
        username="anne",
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "1"
    assert payload["username"] == "anne"
    assert "exp" in payload


def test_expired_access_token():
    expired_token = jwt.encode(
        {
            "sub": "1",
            "username": "anne",
            "exp": datetime.now(timezone.utc) - timedelta(days=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(expired_token)
