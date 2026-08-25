from app.services.user import UserService
from app.db.models.user import User
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token

from fastapi import HTTPException, status


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, username: str, email: str, password: str) -> User:
        password_hash = hash_password(password)

        return self.user_service.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
        )

    def login(self, username: str, password: str) -> str:
        user = self.user_service.get_user_by_name(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return create_access_token(user_id=user.id, username=user.username)
