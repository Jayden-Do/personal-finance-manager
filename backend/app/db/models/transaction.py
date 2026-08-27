from enum import Enum
from decimal import Decimal
from datetime import date
from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")

    name: str = Field(max_length=255)

    type: TransactionType

    amount: Decimal = Field(max_digits=19, decimal_places=4)

    transaction_date: date

    note: str | None = None
