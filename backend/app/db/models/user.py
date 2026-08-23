from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
