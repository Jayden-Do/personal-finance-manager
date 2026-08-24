from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.user import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)


def username_already_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Username already exists"},
    )


def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists"},
    )
