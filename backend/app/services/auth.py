from app.services.user import UserService
from app.schemas.user import UserCreate
from app.security.password import hash_password


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, user_data: UserCreate):
        password_hash = hash_password(user_data.password)

        return self.user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )
