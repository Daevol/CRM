from sqlalchemy.orm import Session

from app.models import Service
from app.schemas.service import ServiceCreate


class ServiceCatalog:
    @staticmethod
    def create_service(db: Session, payload: ServiceCreate) -> Service:
        service = Service(
            name=payload.name,
            category=payload.category,
            duration_minutes=payload.duration_minutes,
            price=payload.price,
            materials=payload.materials,
        )
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def list_services(db: Session):
        return db.query(Service).all()
