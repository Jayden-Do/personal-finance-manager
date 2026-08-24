from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.dependencies.user import get_user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.register_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )
