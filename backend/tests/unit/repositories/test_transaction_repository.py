from datetime import date
from decimal import Decimal
from unittest.mock import Mock

from app.db.models.transaction import Transaction, TransactionType
from app.repositories.transaction import TransactionRepository


def test_create():
    session = Mock()
    repository = TransactionRepository(session)

    transaction = Transaction(
        user_id=1,
        name="Lunch",
        type=TransactionType.EXPENSE,
        amount=Decimal("50000"),
        transaction_date=date(2026, 8, 27),
    )

    result = repository.create(transaction)

    session.add.assert_called_once_with(transaction)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(transaction)

    assert result == transaction


def test_get_by_id():
    session = Mock()

    transaction = Transaction(
        id=1,
        user_id=1,
        name="Lunch",
        type=TransactionType.EXPENSE,
        amount=Decimal("50000"),
        transaction_date=date(2026, 8, 27),
    )

    session.exec.return_value.first.return_value = transaction

    repository = TransactionRepository(session)

    result = repository.get_by_id(1)

    assert result == transaction
    session.exec.assert_called_once()


def test_get_by_id_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = TransactionRepository(session)

    result = repository.get_by_id(999)

    assert result is None


def test_get_by_user():
    session = Mock()

    transactions = [
        Transaction(
            id=1,
            user_id=1,
            name="Lunch",
            type=TransactionType.EXPENSE,
            amount=Decimal("50000"),
            transaction_date=date(2026, 8, 27),
        ),
        Transaction(
            id=2,
            user_id=1,
            name="Coffee",
            type=TransactionType.EXPENSE,
            amount=Decimal("30000"),
            transaction_date=date(2026, 8, 27),
        ),
    ]

    session.exec.return_value.all.return_value = transactions

    repository = TransactionRepository(session)

    result = repository.get_by_user(1)

    assert result == transactions
    assert len(result) == 2
    session.exec.assert_called_once()


def test_get_by_user_not_found():
    session = Mock()

    session.exec.return_value.all.return_value = []

    repository = TransactionRepository(session)

    result = repository.get_by_user(999)

    assert result == []
