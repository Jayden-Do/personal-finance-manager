from fastapi import APIRouter, Depends, status
from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.dependencies.user import get_user_service
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
