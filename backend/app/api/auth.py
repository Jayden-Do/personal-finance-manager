from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService
from app.dependencies.auth import get_auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return service.register(user_data)
