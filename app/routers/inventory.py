from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.inventory import StockItemCreate, StockItemOut, StockMovementCreate, StockMovementOut
from app.services.inventory import InventoryService
from .auth import get_current_user, require_roles
from app.models import UserRole, User

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(require_roles(UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER, UserRole.EMPLOYEE, UserRole.SUPPLIER))],
)


@router.post("/items", response_model=StockItemOut)
def create_item(payload: StockItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.create_item(db, payload, current_user)


@router.get("/items", response_model=list[StockItemOut])
def list_items(db: Session = Depends(get_db)):
    return InventoryService.list_items(db)


@router.post("/movements", response_model=StockMovementOut)
def create_movement(payload: StockMovementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.record_movement(db, payload, current_user)


@router.get("/movements", response_model=list[StockMovementOut])
def list_movements(db: Session = Depends(get_db)):
    return InventoryService.list_movements(db)
