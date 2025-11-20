from sqlalchemy.orm import Session

from app.models import Client
from app.schemas.client import ClientCreate


class ClientService:
    @staticmethod
    def create_client(db: Session, payload: ClientCreate) -> Client:
        client = Client(full_name=payload.full_name, phone=payload.phone, notes=payload.notes)
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def list_clients(db: Session):
        return db.query(Client).order_by(Client.created_at.desc()).all()
