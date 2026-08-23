from app.db.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:

        existing_user = self.user_repository.get_by_username(username)

        if existing_user:
            raise ValueError("Username already exists")

        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            username=username,
            email=email,
            password_hash=password,  # temporary
        )

        return self.user_repository.create(user)
