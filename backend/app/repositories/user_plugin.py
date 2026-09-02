from sqlmodel import Session, select

from app.db.models.user_plugin import UserPlugin


class UserPluginRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_plugin: UserPlugin) -> UserPlugin:
        self.session.add(user_plugin)
        self.session.commit()
        self.session.refresh(user_plugin)
        return user_plugin

    def get_by_user(
        self,
        user_id: int,
    ) -> list[UserPlugin]:
        statement = select(UserPlugin).where(UserPlugin.user_id == user_id)

        return list(self.session.exec(statement).all())

    def delete(
        self,
        user_id: int,
        plugin_id: int,
    ) -> None:
        statement = select(UserPlugin).where(
            UserPlugin.user_id == user_id,
            UserPlugin.plugin_id == plugin_id,
        )

        user_plugin = self.session.exec(statement).first()

        if user_plugin is None:
            return

        self.session.delete(user_plugin)
        self.session.commit()
