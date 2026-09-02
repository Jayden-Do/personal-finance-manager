from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(
    user_id: int,
    username: str,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_access_token_expire_days
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
