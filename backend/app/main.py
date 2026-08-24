from fastapi import FastAPI

from app.exceptions.handlers import (
    email_already_exists_handler,
    username_already_exists_handler,
)
from app.exceptions.user import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)

from app.api.auth import router as auth_router

app = FastAPI()


app.add_exception_handler(
    UsernameAlreadyExistsError,
    username_already_exists_handler,
)

app.add_exception_handler(
    EmailAlreadyExistsError,
    email_already_exists_handler,
)

app.include_router(auth_router)
