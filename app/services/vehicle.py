from sqlalchemy.orm import Session

from app.models import Vehicle, User
from app.schemas.vehicle import VehicleCreate
from app.services.audit import AuditService


class VehicleService:
    @staticmethod
    def add_vehicle(db: Session, payload: VehicleCreate, actor: User) -> Vehicle:
        vehicle = Vehicle(
            client_id=payload.client_id,
            vin=payload.vin,
            plate_number=payload.plate_number,
            make=payload.make,
            model=payload.model,
            notes=payload.notes,
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        AuditService.log_action(
            db,
            actor,
            "add_vehicle",
            "Vehicle",
            vehicle.id,
            {"client_id": payload.client_id, "plate_number": payload.plate_number},
        )
        return vehicle

    @staticmethod
    def list_by_client(db: Session, client_id: int):
        return db.query(Vehicle).filter(Vehicle.client_id == client_id).all()
