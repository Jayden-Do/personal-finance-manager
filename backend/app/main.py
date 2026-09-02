from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.plugin import router as plugin_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(plugin_router)
