from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.finance import TransactionType


class FinancialTransactionBase(BaseModel):
    direction: TransactionType
    category: str
    amount: float
    description: Optional[str] = None
    reference: Optional[str] = None


class FinancialTransactionCreate(FinancialTransactionBase):
    pass


class FinancialTransactionOut(FinancialTransactionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
