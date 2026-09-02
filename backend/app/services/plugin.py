from fastapi import HTTPException, status

from app.db.models.plugin import Plugin
from app.db.models.user_plugin import UserPlugin
from app.repositories.plugin import PluginRepository
from app.repositories.user_plugin import UserPluginRepository
from app.schemas.plugin import PluginResponse


class PluginService:
    def __init__(
        self,
        plugin_repository: PluginRepository,
        user_plugin_repository: UserPluginRepository,
    ):
        self.plugin_repository = plugin_repository
        self.user_plugin_repository = user_plugin_repository

    def get_plugins_for_user(
        self,
        user_id: int,
    ) -> list[PluginResponse]:
        plugins = self.plugin_repository.get_all_with_user_status(user_id)

        return [
            PluginResponse(
                key=plugin.key,
                name=plugin.name,
                icon=plugin.icon,
                description=plugin.description,
                color_theme=plugin.color_theme,
                enabled=user_plugin_id is not None,
            )
            for plugin, user_plugin_id in plugins
        ]

    def update_plugins_for_user(
        self,
        user_id: int,
        plugin_keys: list[str],
    ) -> list[Plugin]:
        if len(plugin_keys) != len(set(plugin_keys)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate plugin keys are not allowed",
            )

        requested_plugins = self.plugin_repository.get_by_keys(plugin_keys)

        if len(requested_plugins) != len(plugin_keys):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more plugins not found",
            )

        current_user_plugins = self.user_plugin_repository.get_by_user(user_id)

        current_plugin_ids = {
            user_plugin.plugin_id for user_plugin in current_user_plugins
        }

        requested_plugin_ids = {plugin.id for plugin in requested_plugins}

        plugins_to_add = requested_plugin_ids - current_plugin_ids
        plugins_to_remove = current_plugin_ids - requested_plugin_ids

        for plugin_id in plugins_to_add:
            self.user_plugin_repository.create(
                UserPlugin(
                    user_id=user_id,
                    plugin_id=plugin_id,
                )
            )

        for plugin_id in plugins_to_remove:
            self.user_plugin_repository.delete(
                user_id=user_id,
                plugin_id=plugin_id,
            )

        plugins = self.plugin_repository.get_all_with_user_status(user_id)

        return [
            PluginResponse(
                key=plugin.key,
                name=plugin.name,
                icon=plugin.icon,
                description=plugin.description,
                color_theme=plugin.color_theme,
                enabled=user_plugin_id is not None,
            )
            for plugin, user_plugin_id in plugins
        ]
