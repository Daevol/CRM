from sqlalchemy.orm import Session

from app.models import Client, User
from app.schemas.client import ClientCreate
from app.services.audit import AuditService


class ClientService:
    @staticmethod
    def create_client(db: Session, payload: ClientCreate, actor: User) -> Client:
        client = Client(full_name=payload.full_name, phone=payload.phone, notes=payload.notes)
        db.add(client)
        db.commit()
        db.refresh(client)
        AuditService.log_action(db, actor, "create_client", "Client", client.id, {"phone": payload.phone})
        return client

    @staticmethod
    def list_clients(db: Session):
        return db.query(Client).order_by(Client.created_at.desc()).all()
