from sqlmodel import Session, select

from app.db.models.plugin import Plugin
from app.db.models.user_plugin import UserPlugin


class PluginRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Plugin]:
        statement = select(Plugin)
        return list(self.session.exec(statement).all())

    def get_by_id(self, plugin_id: int) -> Plugin | None:
        statement = select(Plugin).where(Plugin.id == plugin_id)
        return self.session.exec(statement).first()

    def get_by_keys(
        self,
        plugin_keys: list[str],
    ) -> list[Plugin]:
        statement = select(Plugin).where(Plugin.key.in_(plugin_keys))

        return list(self.session.exec(statement).all())

    def get_all_with_user_status(
        self,
        user_id: int,
    ) -> list[tuple[Plugin, int | None]]:
        statement = select(Plugin, UserPlugin.id).join(
            UserPlugin,
            (Plugin.id == UserPlugin.plugin_id) & (UserPlugin.user_id == user_id),
            isouter=True,
        )

        return list(self.session.exec(statement).all())
