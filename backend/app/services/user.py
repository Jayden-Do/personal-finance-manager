from fastapi import HTTPException, status

from app.db.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> User:

        if self.user_repository.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        if self.user_repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        return self.user_repository.create(user)

    def get_user_by_name(self, username: str) -> User | None:
        return self.user_repository.get_by_username(username)

    def get_user_by_id(self, id: int) -> User | None:
        return self.user_repository.get_by_id(id)
