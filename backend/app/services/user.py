from app.db.models.user import User
from app.repositories.user import UserRepository
from app.exceptions.user import EmailAlreadyExistsError, UsernameAlreadyExistsError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> User:

        existing_user = self.user_repository.get_by_username(username)

        if existing_user:
            raise UsernameAlreadyExistsError()

        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise EmailAlreadyExistsError()

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        return self.user_repository.create(user)
