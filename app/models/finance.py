from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, Integer, Numeric, String

from app.core.database import Base


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    direction = Column(String, default=TransactionType.INCOME)
    category = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
