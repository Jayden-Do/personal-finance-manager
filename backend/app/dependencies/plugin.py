from fastapi import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.repositories.plugin import PluginRepository
from app.repositories.user_plugin import UserPluginRepository
from app.services.plugin import PluginService


def get_plugin_repository(
    session: Session = Depends(get_session),
) -> PluginRepository:
    return PluginRepository(session)


def get_user_plugin_repository(
    session: Session = Depends(get_session),
) -> UserPluginRepository:
    return UserPluginRepository(session)


def get_plugin_service(
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
    user_plugin_repository: UserPluginRepository = Depends(get_user_plugin_repository),
) -> PluginService:
    return PluginService(
        plugin_repository=plugin_repository,
        user_plugin_repository=user_plugin_repository,
    )
