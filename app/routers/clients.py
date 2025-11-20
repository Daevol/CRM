from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.client import ClientCreate, ClientOut
from app.services.client import ClientService
from .auth import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    return ClientService.create_client(db, payload)


@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return ClientService.list_clients(db)
