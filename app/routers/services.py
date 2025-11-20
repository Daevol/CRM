from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service import ServiceCreate, ServiceOut
from app.services.catalog import ServiceCatalog
from .auth import get_current_user, require_roles
from app.models import UserRole, User

router = APIRouter(
    prefix="/services",
    tags=["services"],
    dependencies=[Depends(require_roles(UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER))],
)


@router.post("", response_model=ServiceOut)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ServiceCatalog.create_service(db, payload, current_user)


@router.get("", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return ServiceCatalog.list_services(db)
