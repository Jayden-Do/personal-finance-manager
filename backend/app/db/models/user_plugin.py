from sqlmodel import Field, SQLModel, UniqueConstraint


class UserPlugin(SQLModel, table=True):
    __tablename__ = "user_plugins"
    __table_args__ = (UniqueConstraint("user_id", "plugin_id"),)

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    plugin_id: int = Field(foreign_key="plugins.id")
