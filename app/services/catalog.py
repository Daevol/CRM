from sqlalchemy.orm import Session

from app.models import Service, User
from app.schemas.service import ServiceCreate
from app.services.audit import AuditService


class ServiceCatalog:
    @staticmethod
    def create_service(db: Session, payload: ServiceCreate, actor: User) -> Service:
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
        AuditService.log_action(
            db,
            actor,
            "create_service",
            "Service",
            service.id,
            {"category": payload.category},
        )
        return service

    @staticmethod
    def list_services(db: Session):
        return db.query(Service).all()
