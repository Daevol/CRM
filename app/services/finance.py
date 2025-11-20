from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import FinancialTransaction, TransactionType
from app.schemas.finance import FinancialTransactionCreate


class FinanceService:
    @staticmethod
    def record_transaction(db: Session, payload: FinancialTransactionCreate) -> FinancialTransaction:
        transaction = FinancialTransaction(
            direction=payload.direction,
            category=payload.category,
            amount=payload.amount,
            description=payload.description,
            reference=payload.reference,
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def summary(db: Session):
        income = db.query(func.coalesce(func.sum(FinancialTransaction.amount), 0)).filter(
            FinancialTransaction.direction == TransactionType.INCOME
        ).scalar()
        expense = db.query(func.coalesce(func.sum(FinancialTransaction.amount), 0)).filter(
            FinancialTransaction.direction == TransactionType.EXPENSE
        ).scalar()
        balance = income - expense
        return {"income": float(income), "expense": float(expense), "balance": float(balance)}

    @staticmethod
    def list_transactions(db: Session):
        return db.query(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).all()
