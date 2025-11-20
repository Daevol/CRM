from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.client import ClientCreate, ClientOut
from app.services.client import ClientService
from .auth import get_current_user, require_roles
from app.models import UserRole, User

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(require_roles(UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER, UserRole.EMPLOYEE))],
)


@router.post("", response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ClientService.create_client(db, payload, current_user)


@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return ClientService.list_clients(db)
