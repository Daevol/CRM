from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleOut
from app.services.vehicle import VehicleService
from .auth import get_current_user

router = APIRouter(prefix="/vehicles", tags=["vehicles"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=VehicleOut)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    return VehicleService.add_vehicle(db, payload)


@router.get("/client/{client_id}", response_model=list[VehicleOut])
def list_by_client(client_id: int, db: Session = Depends(get_db)):
    return VehicleService.list_by_client(db, client_id)
