from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import TokenResponse
from app.services.auth import AuthService
from app.dependencies.auth import get_auth_service
from fastapi.security import OAuth2PasswordRequestForm


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
    return service.register(
        username=user_data.username, email=user_data.email, password=user_data.password
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    access_token = service.login(
        username=form_data.username,
        password=form_data.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
