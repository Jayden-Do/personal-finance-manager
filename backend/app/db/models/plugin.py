from sqlmodel import Field, SQLModel


class Plugin(SQLModel, table=True):
    __tablename__ = "plugins"

    id: int | None = Field(default=None, primary_key=True)

    key: str = Field(
        max_length=100,
        unique=True,
        nullable=False,
    )

    name: str = Field(
        max_length=255,
        nullable=False,
    )

    icon: str = Field(
        max_length=255,
        nullable=False,
    )

    description: str = Field(
        max_length=255,
        nullable=False,
    )

    color_theme: str = Field(
        max_length=255,
        nullable=False,
    )
