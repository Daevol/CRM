from typing import Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models import AuditLog, User


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        actor: Optional[User],
        action: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[dict] = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=actor.id if actor else None,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=jsonable_encoder(details or {}),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
