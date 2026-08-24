from fastapi import Depends

from app.services.user import UserService
from app.services.auth import AuthService
from app.dependencies.user import get_user_service


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
