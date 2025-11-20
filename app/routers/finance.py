from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.finance import FinancialTransactionCreate, FinancialTransactionOut
from app.services.finance import FinanceService
from .auth import get_current_user

router = APIRouter(prefix="/finance", tags=["finance"], dependencies=[Depends(get_current_user)])


@router.post("/transactions", response_model=FinancialTransactionOut)
def record_transaction(payload: FinancialTransactionCreate, db: Session = Depends(get_db)):
    return FinanceService.record_transaction(db, payload)


@router.get("/transactions", response_model=list[FinancialTransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return FinanceService.list_transactions(db)


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return FinanceService.summary(db)
