from sqlmodel import Session, select

from app.db.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)

        return transaction

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        statement = select(Transaction).where(Transaction.id == transaction_id)
        return self.session.exec(statement).first()

    def get_by_user(self, user_id: int) -> Transaction | None:
        statement = select(Transaction).where(Transaction.user_id == user_id)
        return list(self.session.exec(statement).all())
